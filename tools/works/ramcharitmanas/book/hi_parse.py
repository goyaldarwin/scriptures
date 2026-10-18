import json,re,unicodedata,collections
t=json.load(open('hi_text.json'))
KANDS=['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar']
DIG=str.maketrans('०१२३४५६७८९','0123456789')
ORD={'पहला':1,'दूसरा':2,'तीसरा':3,'चौथा':4,'पाँचवाँ':5,'छठा':6,'सातवाँ':7,'आठवाँ':8,'नवाँ':9,'दसवाँ':10,'ग्यारहवाँ':11,'बारहवाँ':12,'तेरहवाँ':13,'चौदहवाँ':14,'पंद्रहवाँ':15,'पन्द्रहवाँ':15,'सोलहवाँ':16,'सत्रहवाँ':17,'अठारहवाँ':18,'उन्नीसवाँ':19,'बीसवाँ':20,'इक्कीसवाँ':21,'बाईसवाँ':22,'तेईसवाँ':23,'चौबीसवाँ':24,'पचीसवाँ':25,'पच्चीसवाँ':25,'छब्बीसवाँ':26,'सत्ताईसवाँ':27,'अट्ठाईसवाँ':28,'उनतीसवाँ':29,'उन्तीसवाँ':29,'तीसवाँ':30}
def clean(s):
    s=unicodedata.normalize('NFC',s)
    s=re.sub(r'।\s*।','।।',s); s=re.sub(r'।\s*।','।।',s)
    s=re.sub(r'।।\s*([०-९]+)\s*(\([^)]*\))?\s*।।',lambda m:'।।'+m.group(1)+(' '+m.group(2) if m.group(2) else '')+'।।',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s
lines=[]
for pi in range(31,len(t)):
    for l in t[pi]:
        lines.append(dict(l,p=pi+1,t=clean(l['t'])))
units=[]; ki=-1; cur=None; mode=None
def new(kind):
    global cur
    cur={'kand':KANDS[ki] if ki>=0 else None,'kind':kind,'v':[],'m':[],'p':None,'fn':[]}
    units.append(cur)
for l in lines:
    s=l['t']; sz=l['s']
    if sz>=29: ki+=1; units.append({'kand':KANDS[ki],'kind':'kandstart','p':l['p']}); mode=None; continue
    m=re.search(r'(मास|नवाह्न)पारायण[,\s]*(\S+)\s*विश्राम',s)
    if m:
        n=ORD.get(m.group(2))
        units.append({'kand':KANDS[ki],'kind':'pause','v':('M' if m.group(1)=='मास' else 'N')+str(n),'raw':s,'p':l['p']}); mode=None
        # a line may contain both
        for m2 in list(re.finditer(r'(मास|नवाह्न)पारायण[,\s]*(\S+)\s*विश्राम',s))[1:]:
            units.append({'kand':KANDS[ki],'kind':'pause','v':('M' if m2.group(1)=='मास' else 'N')+str(ORD.get(m2.group(2))),'raw':s,'p':l['p']})
        continue
    if sz>=20 or (sz>=17 and l['b']) or s in ('।। श्रीगणेशाय नमः ।।',):
        units.append({'kand':KANDS[ki],'kind':'heading','t':s,'p':l['p']}); mode=None; continue
    if s.startswith('इति श्रीमद्'):
        units.append({'kand':KANDS[ki],'kind':'colophon','t':s,'p':l['p']}); mode='colo'; continue
    if mode=='colo' and sz<17:
        units[-1]['t']+=' '+s; continue
    if sz<12:
        if cur: cur['fn'].append(s)
        continue
    if sz>=17:  # verse
        if mode!='v':
            new('verse'); cur['p']=l['p']
        cur['v'].append(s); mode='v'; continue
    # meaning line
    if mode=='v' or mode=='m':
        cur['m'].append(s); mode='m'
        if re.search(r'।।[०-९]+[^।]*।।\s*$',s) or re.search(r'।।\s*$',s): mode='mdone'
    elif mode=='mdone' and cur is not None and l['x']<80:
        cur['m'].append(s)   # continuation (e.g. after number on separate line)
    else:
        units.append({'kand':KANDS[ki] if ki>=0 else None,'kind':'prose','t':s,'p':l['p']}); mode='prose' if mode!='prose' else 'prose'
json.dump(units,open('hi_units_raw.json','w'),ensure_ascii=False)
c=collections.Counter((u['kand'],u['kind']) for u in units)
print(c)
pz=[u['v'] for u in units if u['kind']=='pause']; print(len(pz),pz)
for u in units:
    if u['kind']=='prose': print('PROSE',u['p'],u['t'][:80])
