import os,pymupdf, json, collections
d=pymupdf.open(os.environ.get('ENGLISH_PDF','English.pdf'))
pages=[]
for i,p in enumerate(d):
    lines=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            spans=[(s['font'],s['text'],s['bbox'][0],s['size']) for s in l['spans'] if s['text']]
            if spans: lines.append({'y':round(l['bbox'][1],1),'x':round(l['bbox'][0],1),'y2':round(l['bbox'][3],1),'spans':spans})
    pages.append(lines)
json.dump(pages,open('en_spans.json','w'),ensure_ascii=False)
fonts=collections.Counter()
for pg in pages:
    for l in pg:
        for f,t,x,s in l['spans']: fonts[f]+=len(t)
print(fonts.most_common())
