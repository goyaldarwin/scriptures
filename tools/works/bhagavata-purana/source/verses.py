import json,re,collections
D='०१२३४५६७८९'
def num(s): return int(s.translate(str.maketrans(D,'0123456789')))
END=re.compile(r'॥\s*([०-९]+)\s*(॥)?\s*$')
PM=re.compile(r'॥\s*([०-९]+)\s*॥')
book=json.load(open('raw.json'))
import os
MISSING=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'missing.json')))
probs=[]; total=0; fixes=[]
for sk in book:
    if sk['n']==12: sk['adh']=sk['adh'][:13]
    for a in sk['adh']:
        vs=[]; cur=[]; spk=[]; prose=''
        def flush_prose(final=False):
            global prose
        def _A(d):
            global pend
            d['nm']=pend; pend=[]; vs.append(d)
        pend=[]   # the book's note marks (* † ‡) on Sanskrit lines, given to the verse they end up in
        for kind,t,marks,key,x,y in a['san']:
            pend+=[(key,y,ch) for ch in (marks or '') if ch in '*†‡']
            if kind=='g':
                if cur: probs.append((sk['n'],a['n'],'prose inside verse',cur[-1][1][:40]))
                if spk and not prose: pspk=spk; spk=[]
                elif not prose: pspk=[]
                if prose.endswith('-'): prose=prose[:-1]+t
                else: prose=(prose+' '+t).strip()
                while '॥॥' in prose:
                    nn=(vs[-1]['n']+1) if vs else 1
                    fixes.append((sk['n'],a['n'],nn,'prose ends with a bare ॥॥: number inferred',prose[:40]))
                    prose=prose.replace('॥॥','॥'+str(nn).translate(str.maketrans('0123456789',D))+'॥',1)
                while True:
                    m=PM.search(prose)
                    if not m: break
                    body=prose[:m.end()]; prose=prose[m.end():].strip()
                    _A(dict(n=num(m.group(1)),spk=pspk,lines=[('g',body.replace('-',''),marks)],kind='g',pg=key)); pspk=[]
                continue
            if prose:
                m=END.search(prose)
                if m: _A(dict(n=num(m.group(1)),spk=pspk,lines=[('g',prose.replace('-',''),[])],kind='g',pg=key))
                else: spk=spk+[prose.replace('-','')]
                prose=''
            if kind=='spk' and not cur: spk.append(t); continue
            cur.append((kind,t,marks))
            m=END.search(t)
            if m:
                _A(dict(n=num(m.group(1)),spk=spk,lines=cur,kind='v',pg=key)); cur=[]; spk=[]
            elif re.search(r'॥\s*$',t):
                nn=(vs[-1]['n']+1) if vs else 1
                fixes.append((sk['n'],a['n'],nn,'verse ends with a bare ॥: number inferred',t))
                cur[-1]=(kind,re.sub(r'॥\s*$','॥'+str(nn).translate(str.maketrans('0123456789',D)),t),marks)
                _A(dict(n=nn,spk=spk,lines=cur,kind='v',pg=key,inferred=True)); cur=[]; spk=[]
        if cur: probs.append((sk['n'],a['n'],'leftover',[c[1] for c in cur][:3]))
        if prose: probs.append((sk['n'],a['n'],'prose leftover',prose[:50]))
        # a verse printed again at a page turn (its last lines repeated with the same number): drop the repeat
        out=[]
        for v in vs:
            if out and v['n']==out[-1]['n'] and [l[1] for l in v['lines']]==[l[1] for l in out[-1]['lines']][-len(v['lines']):]:
                fixes.append((sk['n'],a['n'],v['n'],'lines repeated at a page turn dropped',v['lines'][0][1])); continue
            out.append(v)
        vs=out
        out=[]
        for v in vs:
            if out and out[-1].get('inferred') and out[-1]['n']==v['n']:
                p=out[-1]; L=p['lines']; L[-1]=(L[-1][0],re.sub(r'॥[०-९]+$',' ।',L[-1][1]),L[-1][2])
                fixes[-1]=None
                fixes.append((sk['n'],a['n'],v['n'],'a ॥ printed for । inside the verse',L[-1][1]))
                p['lines']=L+v['lines']; p['nm']=p.get('nm',[])+v.get('nm',[]); p.pop('inferred'); continue
            out.append(v)
        vs=out
        # verses the e-book leaves out, from the witnesses (src/missing.json)
        for k,m in MISSING.items():
            ks,ka,kn=map(int,k.split('.'))
            if (ks,ka)==(sk['n'],a['n']) and kn not in [v['n'] for v in vs]:
                i=next(j for j,v in enumerate(vs) if v['n']>kn)
                vs.insert(i,dict(n=kn,spk=[],lines=[('v',l,[]) for l in m['lines']],kind='v',pg=None,witness=m['witness']))
                fixes.append((ks,ka,kn,'verse missing in the e-book, taken from '+m['witness'],m['lines'][0]))
        # a misprinted number: the neighbours agree on what it must be
        for i in range(1,len(vs)-1):
            if vs[i]['n']!=vs[i-1]['n']+1 and vs[i+1]['n']==vs[i-1]['n']+2:
                nn=vs[i-1]['n']+1; fixes.append((sk['n'],a['n'],nn,'printed number %d, the sequence needs %d'%(vs[i]['n'],nn),vs[i]['lines'][-1][1]))
                L=vs[i]['lines']; L[-1]=(L[-1][0],END.sub(lambda m:'॥'+str(nn).translate(str.maketrans('0123456789',D))+('॥' if m.group(2) else ''),L[-1][1]),L[-1][2]); vs[i]['n']=nn
        a['verses']=vs; total+=len(vs)
        ns=[v['n'] for v in vs]
        if ns!=list(range(1,len(ns)+1)):
            bad=[(i+1,n) for i,n in enumerate(ns) if n!=i+1][:4]
            probs.append((sk['n'],a['n'],'seq',bad,len(ns)))
        cn=re.search(r'॥\s*([०-९]+)\s*॥\s*$',' '.join(a['col']))
        if not cn or num(cn.group(1))!=a['n']: probs.append((sk['n'],a['n'],'colophon',a['col'][-1:] ))
json.dump(book,open('book.json','w'),ensure_ascii=False)
fixes=[f for f in fixes if f]
json.dump(fixes,open('fixes.json','w'),ensure_ascii=False,indent=0)
print('fixes',len(fixes))
for f in fixes: print(f)
print('verses',total,'problems',len(probs))
for p in probs[:80]: print(p)
