"""Match a transcript (speech recognised as Hindi text, with times) to the verses of a work.

The verses are split into half-lines (at ।). Both sides are reduced to a "key" that ignores
spelling differences speech recognition makes (vowel length, nasal marks, ब/व, श/ष/स …).
locate() finds where in the work the recording starts; align() pairs transcript segments with
half-lines by dynamic programming, skipping what the reciter adds (refrains, repeats, kīrtana).
Works for Devanagari texts; other scripts need their own key().
"""
import json,re,sys,difflib,unicodedata,collections
REF=[]  # (item index, half-line text, key)
def key(s):
    s=unicodedata.normalize('NFC',s)
    s=re.sub(r'[^ऀ-ॿ ]',' ',s)
    s=re.sub(r'[०-९।॥]',' ',s)
    s=s.replace('ँ','').replace('ं','').replace('़','').replace('्','').replace('ः','')
    for a,b in [('ा','अ'),('ी','ि'),('ू','ु'),('ै','े'),('ौ','ो'),('ई','इ'),('ऊ','उ'),('ऐ','ए'),('औ','ओ'),('आ','अ'),('ण','न'),('श','स'),('ष','स'),('व','ब'),('य','ज'),('ृ','ि'),('ऋ','रि'),('ढ','ड'),('क्ष','छ')]:
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
def align(S, r0, span=None):
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
            dp[i,j]=best; bt[i,j]=b
    j=int(dp[n].argmin()); i=n; pairs=[]
    while i>0:
        b=bt[i,j]
        if b==1: i-=1
        elif b==2: j-=1
        else:
            k={3:1,4:2,5:3,6:4}[b]
            for q in range(k): pairs.append((i-1,j-1-q))
            i-=1; j-=k
    pairs.reverse()
    return R,pairs
