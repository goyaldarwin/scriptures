import json,re,unicodedata,collections
from align import norm_loose, words_dev
hu=json.load(open('hi_units_raw.json')); eu=json.load(open('en_units.json'))
KANDS=['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar']
DIG=str.maketrans('०१२३४५६७८९','0123456789')
# ---- A. Hindi items
items=[]; pauses=[]; kand_of={}
uttar_done=False
for i,u in enumerate(hu):
    if uttar_done: break
    if u['kind']=='colophon' and u['kand']=='uttar': uttar_done=True
    if u['kind']=='pause':
        pauses.append((u['v'],len(items)-1)); continue
    if u['kind']!='verse': continue
    v=u['v']; first=v[0]
    m=re.match(r'^(दो|सो|छं|चौ)०\s*[—-]\s*',first)
    if re.match(r'^श्लोक\s*[—-]',first): typ='shloka'; v=[re.sub(r'^श्लोक\s*[—-]\s*','',first)]+v[1:]
    elif m: typ={'दो':'do','सो':'so','छं':'cha','चौ':'cau'}[m.group(1)]; v=[first[m.end():]]+v[1:]
    else: typ='cau'
    allv=' '.join(v); mean=' '.join(u['m'])
    num=None
    mm=re.search(r'।।\s*([०-९]+)\s*(?:\(([क-ङचछ])\))?\s*।।\s*$',allv)
    if mm: num=mm.group(1).translate(DIG)+(mm.group(2) or '')
    mn=re.search(r'।।\s*([०-९]+(?:\s*-\s*[०-९]+)?)\s*(?:\(([क-ङचछ])\))?\s*।।\s*$',mean)
    mnum=mn.group(1).translate(DIG).replace(' ','')+(mn.group(2) or '') if mn else None
    items.append({'src':i,'kand':u['kand'],'type':typ,'v':v,'hi':mean,'fn':u.get('fn',[]),'p':u['p'],'num':num,'mnum':mnum})
# type fixes
INT=re.compile(r'।\s*[^\s।०-९()]')
prev=None
for it in items:
    if it['type']=='cau' and it['num'] and prev is not None and prev['kand']==it['kand'] and prev['type'] in ('do','so','shloka','cha'):
        it['type']=prev['type']
    elif it['type']=='cau' and not any(INT.search(l) for l in it['v']):
        if prev is not None and prev['kand']==it['kand'] and prev['type'] in ('do','so','shloka','cha'):
            it['type']=prev['type']
        else:
            it['type']='shloka'
    prev=it
for k in KANDS:
    ks=[it for it in items if it['kand']==k]
    # sections
    buf=[]; sec_started=False; first_cau_seen=False
    for it in ks:
        if it['type']=='cau': first_cau_seen=True
        if not first_cau_seen and it['type'] in ('shloka','so','do'):
            it['sec']='0'; continue
        buf.append(it)
        nn=it['num'] or it['mnum']
        if it['type'] in ('do','so') and nn and it['sec'] if False else (it['type'] in ('do','so') and nn):
            base=re.match(r'\d+',nn).group(0)
            for b in buf: b['sec']=base
            buf=[]
    for b in buf: b['sec']='end'
# fix Uttar end shlokas typed shloka already; chhand numbering per section
for k in KANDS:
    cnt=collections.Counter()
    for it in [x for x in items if x['kand']==k]:
        key=(it['sec'],it['type'])
        cnt[key]+=1
        if it['type']=='cau': it['n']=it['mnum'] or str(cnt[key])
        elif it['type'] in ('do','so'): it['n']=(it['num'] or it['mnum'] or 'u'+str(cnt[key]))
        elif it['type']=='shloka': it['n']=(it['num'] or it['mnum'] or str(cnt[key]))
        else: it['n']=(it['num'] or it['mnum'] or str(cnt[key]))
for idx,it in enumerate(items):
    it['id']=f"{it['kand']}.{it['sec']}.{it['type']}{it['n']}".replace('(','').replace(')','')
seen=collections.Counter()
for it in items:
    seen[it['id']]+=1
    if seen[it['id']]>1: it['id']+=f"_{seen[it['id']]}"
ids=collections.Counter(it['id'] for it in items)
dups=[k for k,v in ids.items() if v>1]
print('items',len(items),'dups',len(dups),dups[:10])
for k in KANDS:
    ks=[it for it in items if it['kand']==k]
    secs=[it['sec'] for it in ks if it['type'] in('do','so') and it['num']]
    print(k,len(ks),'dohas/sorathas numbered',len(secs),'last',secs[-1] if secs else None, collections.Counter(it['type'] for it in ks))
json.dump({'items':items,'pauses':pauses},open('hi_items.json','w'),ensure_ascii=False)
