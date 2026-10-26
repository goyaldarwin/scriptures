import os,pymupdf, json, re
d=pymupdf.open(os.environ.get('ENGLISH_PDF','English.pdf'))
MARKS='°Ú'
def build_row(chars):
    # chars: list of (c,x0,x1,font,size)
    base=[c for c in chars if not (c[0] in MARKS and c[3].startswith('Chanakya'))]
    marks=[c for c in chars if (c[0] in MARKS and c[3].startswith('Chanakya'))]
    base.sort(key=lambda c:c[1])
    # drop raised dots that overlap the previous glyph (part of chandrabindu drawn as ~ + .)
    b2=[]
    for c in base:
        if c[0]=='.' and b2 and b2[-1][0]!=' ' and c[1] < b2[-1][2]-0.3: continue
        b2.append(c)
    base=b2
    out=[]; prev=None
    for c in base:
        if prev is not None and c[0]!=' ' and prev[0]!=' ' and c[1]-prev[2]>1.2: out.append([' ',c[1],c[1],'',0])
        out.append(list(c)); prev=c
    for m in marks:
        # insert after the base char containing m.x0
        idx=None
        for i,c in enumerate(out):
            if c[0] not in ' ,.;:!?-()' and c[1]-0.3<=m[1]<=c[2]+0.6: idx=i
        if idx is None:
            idx=max([i for i,c in enumerate(out) if c[1]<=m[1]] or [-1])
        out.insert(idx+1,list(m))
    return out
rows_all=[]
for pi,p in enumerate(d):
    raw=p.get_text('rawdict')
    lines=[]
    for b in raw['blocks']:
        for l in b.get('lines',[]):
            ch=[]
            for s in l['spans']:
                for c in s['chars']:
                    ch.append((c['c'],c['bbox'][0],c['bbox'][2],s['font'],round(s['size'],1)))
            if ch: lines.append((l['bbox'][1],l['bbox'][3],ch))
    lines.sort(key=lambda t:t[0])
    # cluster: by vertical overlap (chandrabindu lines included)
    clusters=[]
    for y0,y1,ch in lines:
        nonmark=[c for c in ch if c[0].strip() and not (c[0] in MARKS and c[3].startswith('Chanakya'))]
        if clusters and (abs(y0-clusters[-1]['y'])<=4.6 or not nonmark):
            clusters[-1]['ch']+=ch
        else: clusters.append({'y':y0,'ch':list(ch)})
    for cl in clusters:
        row=build_row(cl['ch'])
        txt=re.sub(r' {2,}',' ',''.join(c[0] for c in row)).strip()
        fonts={}
        for c in row:
            if c[0].strip() and c[0] not in MARKS: fonts[c[3]]=fonts.get(c[3],0)+1
        sizes={}
        for c in row:
            if c[0].strip(): sizes[c[4]]=sizes.get(c[4],0)+1
        rows_all.append({'p':pi+1,'y':round(cl['y'],1),'t':txt,'f':fonts,'s':max(sizes,key=sizes.get) if sizes else 0})
json.dump(rows_all,open('en_rows.json','w'),ensure_ascii=False)
print(len(rows_all))
