import json,re
pages=json.load(open('en_spans.json'))
KANDS=[('BÅLA','bal'),('AYODHYÅ','ayodhya'),('ARAƒYA','aranya'),('KI¸KINDHÅ','kishkindha'),('SUNDARA','sundar'),('LA¥KÅ','lanka'),('UTTARA','uttar')]
def kind(spans):
    fonts={f for f,t,x,s in spans if t.strip() and t.strip() not in '°Ú'}
    if not fonts: return 'misc'
    if all(f.startswith('Chanakya') for f in fonts): return 'dev'
    sizes={round(s) for f,t,x,s in spans if f=='Nalandahel' and t.strip()}
    if 'NalandahelBold' in fonts or any(re.match(r'^\s*(Cau|Do|So|Cha≈|›loka|Ca≈|cha≈|do)\s?\.?\s?:',t) for f,t,x,s in spans[:1]):
        return 'tr'
    if sizes and max(sizes)<=9: return 'fn'
    return 'en'
out=[]
for pi,pg in enumerate(pages):
    # cluster into visual lines
    ls=sorted(pg,key=lambda l:(l['y'],l['x']))
    rows=[]
    for l in ls:
        if rows and abs(l['y']-rows[-1]['y'])<=4.5 and not (kind(l['spans'])!=kind(rows[-1]['spans']) and kind(l['spans']) not in ('misc',) and kind(rows[-1]['spans'])!='misc'):
            rows[-1]['spans']+= [tuple(s) for s in l['spans']]
        else: rows.append({'y':l['y'],'spans':[tuple(s) for s in l['spans']]})
    for r in rows:
        r['spans'].sort(key=lambda s:s[2])
        txt=''.join(s[1] for s in r['spans'])
        k=kind(r['spans'])
        if r['y']<85 and ('*' in txt or re.fullmatch(r'\s*\d+\s*',txt) or '"""' in txt): 
            m=[c for n,c in KANDS if n in txt]
            if m: out.append({'k':'kand','v':m[0],'p':pi+1})
            continue
        if '"""' in txt: continue
        if re.fullmatch(r'\s*\d+\s*',txt): continue
        if 'PAUSE' in txt and 'RECITATION' in txt:
            m=re.search(r'PAUSE\s+(\w+)\s+FOR A (THIRTY|NINE)',txt); n=m.group(1); n=1 if n=='I' else int(n)
            out.append({'k':'pause','v':('M' if m.group(2)=='THIRTY' else 'N')+str(n),'p':pi+1}); continue
        out.append({'k':k,'t':txt,'p':pi+1,'y':r['y']})
json.dump(out,open('en_lines.json','w'),ensure_ascii=False)
print(len(out))
