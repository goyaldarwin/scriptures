import json,re,collections,unicodedata
vt=json.load(open('verify_tr.json')); m=json.load(open('merged.json'))
wf=collections.Counter()
for it in m['items']:
    for l in it['v']:
        for w in re.sub(r'[।॥|,.;:!?\-—‘’“”\'"()\[\]0-9०-९]',' ',l).split(): wf[unicodedata.normalize('NFC',w)]+=1
art=re.compile(r'µ|् |[A-Za-z§]|^\s*$')
V={}
for k,v in vt.items():
    for a,b in v:
        if art.search(a) or art.search(b) or not a.strip(): continue
        aw=a.split(); bw=b.split()
        if len(aw)!=len(bw): continue
        for x,y in zip(aw,bw):
            if x==y: continue
            if wf[y]==0: continue           # alt never occurs as a real word -> likely transliteration artifact
            if x.replace('ा','')==y.replace('ा','') and wf[y]<3: continue
            typo = wf[x]<=1 and wf[y]>=5
            V.setdefault(k,[]).append([x,y,1 if typo else 0])
json.dump(V,open('variants.json','w'),ensure_ascii=False)
print(len(V),sum(len(v) for v in V.values()),'typo',sum(1 for v in V.values() for x in v if x[2]))
for k,v in V.items(): print(k,v)
