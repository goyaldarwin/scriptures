import json,re
d=json.load(open('app_data.json'));eg=d['eg'];it=d['it']
from collections import defaultdict
m=defaultdict(list)
for i,x in enumerate(it):
    if x.get('g') is not None: m[x['g']].append(i)
def segs(x):
    # split after . ? ! ; : followed by space (keep punctuation), avoid splitting on abbreviations like 'Śrī.' rare
    parts=re.split(r'(?<=[.;:?!])\s+(?=[\'‘“(A-ZŚṢĀĪŪṚḌṬṆÑ0-9—])|(?<=[;:])\s+',x)
    return [p for p in parts if p]
groups=[]
for g,v in m.items():
    if len(v)<2: continue
    s=segs(eg[str(g)]['x'])
    groups.append({'g':g,'items':[{'id':it[i]['id'],'tr':' / '.join(it[i].get('t') or []),'hi':it[i]['h']} for i in v],'seg':s})
groups.sort(key=lambda z:z['g'])
json.dump(groups,open('split/groups.json','w'),ensure_ascii=False)
# chunk by ~90k chars
ch=[];cur=[];n=0
for z in groups:
    L=len(json.dumps(z,ensure_ascii=False))
    if n+L>110000 and cur: ch.append(cur);cur=[];n=0
    cur.append(z);n+=L
ch.append(cur)
for k,c in enumerate(ch):
    with open(f'split/chunk{k:02d}.txt','w') as f:
        for z in c:
            f.write(f"### GROUP {z['g']}  ({len(z['items'])} items)\n")
            for j,x in enumerate(z['items']): f.write(f"ITEM {j} [{x['id']}]\n  TR: {x['tr']}\n  HI: {x['hi']}\n")
            for j,s in enumerate(z['seg']): f.write(f"SEG {j}: {s}\n")
            f.write("\n")
print(len(groups),len(ch),[len(c) for c in ch])
import statistics
print('groups where segs<items:',sum(1 for z in groups if len(z['seg'])<len(z['items'])))
