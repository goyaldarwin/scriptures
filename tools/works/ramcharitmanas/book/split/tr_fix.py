import re,unicodedata,difflib,sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tr2dev import tr2dev
INV=[('r̥','æ'),('ā','å'),('ī','∂'),('ū','µu'),('ṁ','≈'),('ḥ','¨'),('ṅ','∆'),('ñ','¤'),('ṭ','¢'),('ḍ','Œ'),('ṇ','ƒ'),('ś','‹'),('ṣ','¶'),('ṛ','R'),('̐','°')]
def u2d(w):
    w=unicodedata.normalize('NFC',w)
    for a,b in INV: w=w.replace(a,b)
    return tr2dev(w)
def strict(w):
    w=unicodedata.normalize('NFC',w).replace('ँ','ं').replace('‌','').replace('‍','').replace('ऽ','')
    w=re.sub(r'[ङञणनम]्(?=[क-ह])','ं',w)
    w=w.replace('ौ','उ').replace('ै','इ').replace('औ','अउ').replace('ऐ','अइ')
    return w
def hwords(lines):
    out=[]
    for s in lines:
        s=re.sub(r'\(\s*[क-ह]\s*\)',' ',s)
        s=re.sub(r'[।॥|,.;:!?\-—‘’“”\'"()\[\]0-9०-९]',' ',s)
        out+= [w for w in s.split() if w]
    return out
TOKRE=re.compile(r"[^\s,.;:!?॥()\-—0-9]+")
LONG={'a':'ā','i':'ī','u':'ū','ā':'a','ī':'i','ū':'u'}
def variants(w):
    yield w.replace('§','')
    yield re.sub(r'([aiu])̐([āīū])', lambda m: {'a':'ā','i':'ī','u':'ū'}[m.group(1)]+'̐' if LONG[m.group(1)]==m.group(2) else m.group(0), w)
    yield re.sub(r'([kgcjṭḍtdpbs]h?)ṁ', r'ṁ\1', w)
    yield w.replace('nḍ','ṇḍ').replace('nṭ','ṇṭ')
    for k,ch in enumerate(w):
        if ch in LONG and not (k+1<len(w) and w[k+1] in 'iu' and ch=='a'):
            yield w[:k]+LONG[ch]+w[k+1:]
def fix_item(v, t):
    H=hwords(v); hk=[strict(w) for w in H]
    toks=[]  # (line, start, end, text)
    for li,l in enumerate(t):
        for m in TOKRE.finditer(l):
            if re.fullmatch(r'[A-G]|I+',m.group(0)): continue
            toks.append([li,m.start(),m.end(),m.group(0)])
    ek=[strict(u2d(x[3])) for x in toks]
    if hk==ek: return t, 0
    sm=difflib.SequenceMatcher(None,hk,ek,autojunk=False)
    edits=[]  # (tok index range, new text)
    regs=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': regs.append(None); continue
        if regs and regs[-1]: r=regs[-1]; regs[-1]=(r[0],i2,r[2],j2)
        else: regs.append((i1,i2,j1,j2))
    for r in regs:
        if not r: continue
        i1,i2,j1,j2=r
        if i2==i1 or j2==j1: continue
        target=''.join(hk[i1:i2])
        span=toks[j1:j2]
        if len({s[0] for s in span})!=1: continue
        joined=''.join(s[3] for s in span)
        done=False
        for cand in ([joined]+[c for c in variants(joined)] if i2-i1==1 else []):
            for c2 in [cand]+list(variants(cand)):
                if strict(u2d(c2))==target:
                    if i2-i1==1 or c2==joined:
                        edits.append((j1,j2,c2 if i2-i1==1 else None)); done=True; break
            if done: break
        if not done and i2-i1>1:
            # greedy: group consecutive tokens so each group spells one Hindi word
            k=j1; groups=[]
            for hi in range(i1,i2):
                acc=None
                for e in range(k+1,j2+1):
                    c=''.join(s[3] for s in toks[k:e])
                    if strict(u2d(c))==hk[hi]: acc=(k,e,c); break
                if not acc: groups=None; break
                groups.append(acc); k=acc[1]
            if groups and k==j2:
                for (a,b,c) in groups:
                    if b-a>1 or c!=toks[a][3]: edits.append((a,b,c))
                done=True
        if not done and i2-i1==j2-j1:
            for a in range(j2-j1):
                for c in variants(span[a][3]):
                    if strict(u2d(c))==hk[i1+a]: edits.append((j1+a,j1+a+1,c)); break
    n=0
    t=list(t)
    for j1,j2,new in sorted([e for e in edits if e[2]], key=lambda e:-e[0]):
        li=toks[j1][0]; a=toks[j1][1]; b=toks[j2-1][2]
        old=t[li][a:b]; t[li]=t[li][:a]+new+t[li][b:]; n+=1
    return t, n
def normalize_end(t, v):
    t=list(t)
    if not t: return t
    l=t[-1]
    l=re.sub(r'\s*I{2}\s*$',' ॥',l)
    t=[re.sub(r'\s*\bII\s*$',' ॥',x) for x in t]
    m=re.search(r'[.\s]*(\d+)\s*(\([A-Z]+\))?\s*\.?\s*$',l)
    if m and not re.search(r'॥\s*$',l):
        l=l[:m.start()].rstrip(' .,')+' ॥'+m.group(1)+(m.group(2) or '')+'॥'
    t[-1]=l
    return t
def fix(out):
    tot=0; items=0
    for x in out:
        t=x.get('t')
        if not t: continue
        t2,n=fix_item(x['v'],t)
        t2=normalize_end(t2,x['v'])
        t2=[re.sub(r'\s{2,}',' ',l).replace(' ,',',') for l in t2]
        if n: items+=1; tot+=n
        x['t']=t2
    print('transliteration fixes',tot,'in',items,'verses')
