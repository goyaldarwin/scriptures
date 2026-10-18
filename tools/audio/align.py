"""Match a transcript (speech recognised as Hindi text, with times) to the verses of a work.

The verses are split into half-lines (at ।). Both sides are reduced to a "key" that ignores
spelling differences speech recognition makes (vowel length, nasal marks, ब/व, श/ष/स …).
locate() finds where in the work the recording starts; align() pairs transcript segments with
half-lines by dynamic programming, skipping what the reciter adds (refrains, repeats, kīrtana).
Works for Devanagari texts; other scripts need their own key().
"""
import json,re,sys,difflib,unicodedata,collections
REF=[]  # (item index, half-line text, key)
GURU={0x0A70:'ं',0x0A71:'',0x0A72:'इ',0x0A73:'उ',0x0A75:''}   # tippi, addak (doubling), bearers ੲ ੳ, yakash
def gur2dev(s):
    # Gurmukhi and Devanagari share the ISCII layout, so most letters map by a fixed offset (ਕ U+0A15 → क U+0915)
    return ''.join(GURU.get(ord(c), chr(ord(c)-0x100)) if 0x0A00<=ord(c)<=0x0A7F else c for c in s)
def key(s):
    s=unicodedata.normalize('NFC',gur2dev(s))
    s=re.sub(r'[\u0951-\u0954\u1CD0-\u1CFF\uA8E0-\uA8FF]','',s)   # Vedic svara and accent marks (॑ ॒ ꣳ …) are not heard as letters
    s=re.sub(r'[^ऀ-ॿ ]',' ',s)
    s=re.sub(r'[०-९।॥]',' ',s)
    s=s.replace('ँ','').replace('ं','').replace('़','').replace('्','').replace('ः','')
    for a,b in [('ा','अ'),('ी','ि'),('ू','ु'),('ै','े'),('ौ','ो'),('ई','इ'),('ऊ','उ'),('ऐ','ए'),('औ','ओ'),('आ','अ'),('ण','न'),('श','स'),('ष','स'),('व','ब'),('य','ज'),('ृ','ि'),('ऋ','रि'),('ढ','ड'),('क्ष','छ'),('ळ','ल')]:   # ळ: Marathi; speech recognition often writes ल
        s=s.replace(a,b)
    s=re.sub(r'[ाअ]','',s)  # drop inherent/long a marks for robustness
    return re.sub(r'\s+','',s)
def init(items):
    """items: the work's items (each with 'v', its verse lines)."""
    REF.clear()
    for i,x in enumerate(items):
        for l in x['v']:
            for p in [p for p in re.split(r'(?<=।)\s*(?!।)',l) if p.strip(' ।')]:
                k=key(p)
                if k: REF.append((i,p,k))
def over(sk,cat):
    # a segment cannot hold much more text than it has: penalise merging half-lines the recogniser did not hear
    return 3.0*max(0.0,len(cat)/max(1,len(sk))-1.2)
def sim(a,b):
    if not a or not b: return 0
    return difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()
def load(path):
    S=[json.loads(l) for l in open(path)]
    return [s for s in S if key(s['t'])]
def locate(S):
    # trigram index on ref keys
    idx=collections.defaultdict(list)
    for r,(i,p,k) in enumerate(REF):
        for j in range(len(k)-2): idx[k[j:j+3]].append(r)
    votes=collections.Counter()
    for n,s in enumerate(S[:40]):
        k=key(s['t']); c=collections.Counter()
        for j in range(len(k)-2):
            for r in set(idx.get(k[j:j+3],[])): c[r]+=1
        if c:
            r,_=c.most_common(1)[0]; votes[(r-n*1)//50]+=1
    b,_=votes.most_common(1)[0]
    return max(0,b*50-200)
def align(S, r0, span=None, split=False):
    # split=True (source.json "split": true) also lets one long half-line span two or three short segments; off by default so
    # recordings already timed keep exactly the alignment they were published with
    span=span or int(len(S)*1.6)+400
    R=REF[r0:r0+span]; n,m=len(S),len(R)
    SK=[key(s['t']) for s in S]
    INF=1e9
    # dp[i][j]: cost aligning first i segs with first j refs
    import numpy as np
    dp=np.full((n+1,m+1),INF); bt=np.zeros((n+1,m+1),dtype=np.int8)
    dp[0,:]=0  # free start in ref
    SKIP_S=0.55; SKIP_R=0.75
    for i in range(1,n+1):
        sk=SK[i-1]
        for j in range(0,m+1):
            best=dp[i-1,j]+SKIP_S; b=1
            if j>=1:
                c=dp[i,j-1]+SKIP_R
                if c<best: best=c; b=2
                c=dp[i-1,j-1]+(1-sim(sk,R[j-1][2]))
                if c<best: best=c; b=3
            if j>=2:
                cat=R[j-2][2]+R[j-1][2]; c=dp[i-1,j-2]+(1-sim(sk,cat))+0.05+over(sk,cat)
                if c<best: best=c; b=4
            if j>=3:
                cat=R[j-3][2]+R[j-2][2]+R[j-1][2]; c=dp[i-1,j-3]+(1-sim(sk,cat))+0.1+over(sk,cat)
                if c<best: best=c; b=5
            if j>=4:   # a reciter often runs four half-lines (a whole caupāī) into one breath
                cat=R[j-4][2]+R[j-3][2]+R[j-2][2]+R[j-1][2]; c=dp[i-1,j-4]+(1-sim(sk,cat))+0.15+over(sk,cat)
                if c<best: best=c; b=6
            # one long half-line heard across two or three short segments (Vedic chant: the recogniser cuts mid-line)
            if split and j>=1 and i>=2:
                cs=SK[i-2]+sk; c=dp[i-2,j-1]+(1-sim(cs,R[j-1][2]))+0.05+over(R[j-1][2],cs)
                if c<best: best=c; b=7
            if split and j>=1 and i>=3:
                cs=SK[i-3]+SK[i-2]+sk; c=dp[i-3,j-1]+(1-sim(cs,R[j-1][2]))+0.1+over(R[j-1][2],cs)
                if c<best: best=c; b=8
            dp[i,j]=best; bt[i,j]=b
    j=int(dp[n].argmin()); i=n; pairs=[]
    while i>0:
        b=int(bt[i,j])   # a plain int: numpy int8 arithmetic would overflow on long recordings
        if b==1: i-=1
        elif b==2: j-=1
        elif b in (7,8):
            k=b-5   # 2 or 3 segments → one ref
            for q in range(k): pairs.append((i-1-q,j-1))
            i-=k; j-=1
        else:
            k={3:1,4:2,5:3,6:4}[b]
            for q in range(k): pairs.append((i-1,j-1-q))
            i-=1; j-=k
    pairs.reverse()
    return R,pairs

def anchors(S, r0=0, thr=0.45, r1=None):
    """A second way to align, for recordings the recogniser hears only in patches (sung āratīs, Vedic chant):
    each segment is matched on its own to the one, two or three consecutive half-lines it resembles most; matches
    below `thr` are dropped; then the heaviest chain that moves forward in both time and text is kept.
    Returns (pairs [(segment, half-line)], seconds per letter of text, estimated from neighbouring matches)."""
    R=REF[r0:r1]; cands=[]
    for i,s in enumerate(S):
        k=key(s['t'])
        if len(k)<6: continue
        sc,j=max(((sim(k,''.join(R[j+q][2] for q in range(n)))-0.03*(n-1),j) for j in range(len(R)) for n in (1,2,3) if j+n<=len(R)), default=(0,0))
        if sc>=thr: cands.append((i,j,sc))
    n=len(cands); val=[c[2] for c in cands]; prev=[-1]*n
    for a in range(n):
        for b in range(a):
            if cands[b][1]<=cands[a][1] and val[b]+cands[a][2]>val[a]: val[a]=val[b]+cands[a][2]; prev[a]=b
    chain=[]
    a=max(range(n),key=lambda x:val[x]) if n else -1
    while a>=0: chain.append(cands[a]); a=prev[a]
    chain.reverse()
    rates=[]
    for (i1,j1,_),(i2,j2,_) in zip(chain,chain[1:]):
        if 0<j2-j1<=3:
            ch=sum(len(R[q][2]) for q in range(j1,j2))
            if ch: rates.append((S[i2]['s']-S[i1]['s'])/ch)
    rates.sort(); rate=rates[len(rates)//2] if rates else 0.25
    return R,[(i,j) for i,j,_ in chain],rate
