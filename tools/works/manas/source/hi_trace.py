import os,pymupdf,collections,json,pickle
d=pymupdf.open(os.environ.get('HINDI_PDF','Hindi.pdf'))
pages=[]
mapped=collections.defaultdict(collections.Counter); unm=collections.Counter(); fonts=collections.Counter()
for i,p in enumerate(d):
    spans=[]
    for s in p.get_texttrace():
        f=s['font']; fonts[f]+=len(s['chars'])
        ch=[(c[0],c[1],c[3]) for c in s['chars']]  # unicode,gid,bbox
        spans.append((f,round(s['size'],1),ch))
        for u,g,b in ch:
            if u==65533: unm[(f,g)]+=1
            else: mapped[(f,g)][u]+=1
    pages.append(spans)
pickle.dump(pages,open('hi_trace.pkl','wb'))
print(fonts)
print('unmapped distinct',len(unm),'total',sum(unm.values()))
amb={k:v for k,v in mapped.items() if len(v)>1}
print('ambiguous mapped',len(amb), list(amb.items())[:10])
json.dump({'unm':[[f,g,n] for (f,g),n in unm.most_common()]},open('hi_unmapped.json','w'),ensure_ascii=False)
