import json,re,collections
m=json.load(open('merged.json')); items=m['items']; eg=m['en_groups']
eu=json.load(open('en_units.json'))
toc_en=json.load(open('en_toc.json')); toc_hi=json.load(open('hi_toc.json'))
toc_en['1']=('Invocations',1); toc_en['2']=('Salutations to the Guru',3)
# hindi topics with kand
KMAP={'बालकाण्ड':'bal','अयोध्याकाण्ड':'ayodhya','अरण्यकाण्ड':'aranya','किष्किन्धाकाण्ड':'kishkindha','सुन्दरकाण्ड':'sundar','लङ्काकाण्ड':'lanka','उत्तरकाण्ड':'uttar'}
def h2e(n):
    if n<=126: return n-3
    if n in (127,128): return n-3
    if n==129: return 127
    if 130<=n<=136: return n-2
    if n==137: return 134
    if 138<=n<=143: return n-3
    if 144<=n<=148: return n-3
    if n==149: return 146
    if 150<=n<=173: return n-2
    if n==174: return 171
    return n-3
topics=[];k=None
for e in toc_hi:
    if e[0]=='K': k=KMAP[e[1]]; continue
    n,name=e
    if k and 4<=n<=221:
        en=toc_en[str(h2e(n))]
        topics.append({'n':n,'kand':k,'hi':name,'en':en[0],'page':en[1]})
# english unit -> first hindi item index
eu2item={}
for e,g in eg.items():
    if g['items']: eu2item[int(e)]=g['items'][0]
# for each item: english page of its group
item_page={}
for e,g in eg.items():
    for i in g['items']: item_page[i]=eu[int(e)]['p']
out=collections.defaultdict(list)
for t in topics:
    P=t['page']+18
    cands=[i for i in range(len(items)) if items[i]['kand']==t['kand'] and P-1<=item_page.get(i,-99)<=P+1]
    c=[]
    for i in cands:
        it=items[i]; g=eg[str(it['en_g'][0])] if it['en_g'] else None
        c.append({'id':it['id'],'pdfpage':item_page[i],'text':it['v'][0][:60],'en':(g['text'][:140] if g else '')})
    t['cands']=c
    out[t['kand']].append(t)
for k,v in out.items(): json.dump(v,open(f'topics_{k}.json','w'),ensure_ascii=False,indent=0)
print({k:len(v) for k,v in out.items()}, sum(len(t['cands']) for v in out.values() for t in v))
