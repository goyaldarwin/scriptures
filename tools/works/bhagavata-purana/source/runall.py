import fitz, json, sys, pickle, collections
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import page_runs
fn,out=sys.argv[1],sys.argv[2]
d=fitz.open(fn); pages=[]; unk=collections.Counter()
for i in range(len(d)):
    L=page_runs(d[i]); pages.append(L)
    for l in L:
        for s in l:
            if s['ok'] is not True: unk[tuple(s['ok'][2])]+=1
pickle.dump(pages,open(out,'wb'))
print(fn,len(pages),'unknown runs',sum(unk.values()),len(unk))
json.dump([[list(k),v] for k,v in unk.most_common()],open(out+'.unk.json','w'))
