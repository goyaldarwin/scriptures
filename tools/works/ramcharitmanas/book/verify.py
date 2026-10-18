import json,re,difflib,collections,sys
from align import norm_loose,words_dev,key
from tr2dev import tr2dev
m=json.load(open('merged.json')); items=m['items']
def hwords(it): return [w for l in it['v'] for w in words_dev(l)]
def ewords(it):
    ws=[w for l in it['tr'] for w in words_dev(tr2dev(l))]
    return ws
diffs=collections.Counter(); per_item={}
for it in items:
    h=hwords(it); e=ewords(it)
    h=[w for w in h if w not in ('क','ख','ग','घ','ङ','च','छ')]
    e=[w for w in e if not re.fullmatch(r'[A-G]|I+',w)]
    hk=[key(w) for w in h]; ek=[key(w) for w in e]
    if ''.join(hk)==''.join(ek): per_item[it['id']]=[]; continue
    # merge split words in e when concat matches
    j=0; ek2=[]; e2=[]
    while j<len(ek):
        if j+1<len(ek) and (ek[j]+ek[j+1]) in hk and ek[j] not in hk: ek2.append(ek[j]+ek[j+1]); e2.append(e[j]+e[j+1]); j+=2
        else: ek2.append(ek[j]); e2.append(e[j]); j+=1
    sm=difflib.SequenceMatcher(None,hk,ek2,autojunk=False)
    bad=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal':
            bad.append((' '.join(h[i1:i2]),' '.join(e2[j1:j2])))
    per_item[it['id']]=bad
    for b in bad: diffs[b]+=1
n_items=sum(1 for v in per_item.values() if v)
print('items with any diff',n_items,'of',len(items))
for (a,b),n in diffs.most_common(int(sys.argv[1]) if len(sys.argv)>1 else 50): print(n,a,'|',b)
json.dump(per_item,open('verify_tr.json','w'),ensure_ascii=False)
