import json,re,collections
D='०१२३४५६७८९'
def num(s): return int(s.translate(str.maketrans(D,'0123456789')))
MK=re.compile(r'॥\s*([०-९]+)(?:\s*[-–—]\s*([०-९]+))?\s*॥')
book=json.load(open('book.json'))
def clean(t):
    t=re.sub(r'\s+',' ',t).strip()
    t=re.sub(r'\s+([।?!,;])',r'\1',t)
    return t
probs=[]; out={}; fix=[]
for sk in book:
    for a in sk['adh']:
        txt=''; marks_at=[]
        for t,para,marks,key in a['hindi']:
            if txt.endswith(('-','—')): txt+=t
            else: txt=(txt+' '+t) if txt else t
            if marks: marks_at.append((len(txt),marks))
        chunks=[]; pos=0
        for m in MK.finditer(txt):
            body=txt[pos:m.start()]
            a1=num(m.group(1)); a2=num(m.group(2)) if m.group(2) else a1
            chunks.append(dict(a=a1,b=a2,t=clean(body),mark=m.group(0),start=pos,end=m.end()))
            pos=m.end()
        # misprinted marks, repaired by the sequence (each repair logged)
        for i,c in enumerate(chunks):
            pb=chunks[i-1]['b'] if i else 0
            nxt=chunks[i+1]['a'] if i+1<len(chunks) else None
            if c['a']==pb+1: continue
            dd=str(c['a'])
            if nxt is not None and len(dd)==2 and int(dd[0])==pb+1 and int(dd[1])==pb+2 and nxt==pb+3 and c['a']==c['b']:
                fix.append((sk['n'],a['n'],'mark %s read as %d-%d'%(c['mark'],pb+1,pb+2))); c['a'],c['b']=pb+1,pb+2; c['fixed']=True; continue
            if nxt is not None and c['a']==c['b'] and nxt==pb+2:
                fix.append((sk['n'],a['n'],'mark %s read as %d'%(c['mark'],pb+1))); c['a']=c['b']=pb+1; c['fixed']=True; continue
            if c['b']>c['a'] and c['a']<=pb and c['b']>pb:
                fix.append((sk['n'],a['n'],'mark %s read as %d-%d'%(c['mark'],pb+1,c['b']))); c['a']=pb+1; c['fixed']=True; continue
        tail=txt[pos:].strip()
        if tail: probs.append((sk['n'],a['n'],'tail',tail[:80]))
        vn=[v['n'] for v in a['verses']]
        cov=[]
        for c in chunks: cov+=list(range(c['a'],c['b']+1))
        if cov!=vn:
            missing=sorted(set(vn)-set(cov)); extra=sorted(set(cov)-set(vn)); dup=[k for k,v in collections.Counter(cov).items() if v>1]
            order=cov==sorted(cov)
            probs.append((sk['n'],a['n'],'cover','missing',missing[:10],'extra',extra[:10],'dup',dup[:5],'ordered',order))
        a['mchunks']=chunks; a['hmarks']=marks_at
json.dump(book,open('book2.json','w'),ensure_ascii=False)
print(len(probs)); [print('FIX',f) for f in fix]; json.dump(fix,open('hfix.json','w'),ensure_ascii=False)
for p in probs: print(p)
