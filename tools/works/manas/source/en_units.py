import json,re
rows=json.load(open('en_rows.json'))
KANDS=[('BÅLA','bal'),('AYODHYÅ','ayodhya'),('ARAƒYA','aranya'),('KI¸KINDHÅ','kishkindha'),('SUNDARA','sundar'),('LA¥KÅ','lanka'),('UTTARA','uttar')]
def cls(r):
    t=r['t']; f=r['f']
    if not t: return 'skip'
    if '"""' in t: return 'skip'
    if r['y']<85: return 'hdr'
    if re.fullmatch(r'\d+',t): return 'skip'
    if 'PAUSE' in t and 'RECITATION' in t: return 'pause'
    tot=sum(f.values()) or 1
    ch=sum(v for k,v in f.items() if k.startswith('Chanakya'))
    if ch/tot>0.6: return 'dev'
    if re.match(r'^(Cau|Do|So|Cha≈|Ca≈|cha≈|do|›loka)\s?\.?\s?\.?:',t): return 'tr'
    nb=f.get('NalandahelBold',0)
    if nb/tot>0.6: return 'tr'
    if f.get('NalandahelItalic',0)/tot>0.5: return 'ital'
    if r['s']<=9.5 and 'Nalandahel' in f: return 'fn'
    return 'en'
units=[]; kand=None; cur=None; state=None; log=[]
for r in rows:
    c=cls(r); t=re.sub(r'([,.;:])([°Ú])',r'\2\1',r['t'])
    if c=='hdr': continue
    md=re.match(r'^Descent (One|Two|Three|Four|Five|Six|Seven)$',t)
    if md and r['p']>15:
        kand=['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar'][['One','Two','Three','Four','Five','Six','Seven'].index(md.group(1))]
        units.append({'type':'kandstart','kand':kand,'p':r['p']}); state=None; cur=None; continue
    if c=='skip': continue
    if c=='pause':
        m=re.search(r'PAUSE\s+(\w+)\s+FOR A (THIRTY|NINE)',t); n=m.group(1); n=1 if n=='I' else int(n)
        units.append({'type':'pause','v':('M' if m.group(2)=='THIRTY' else 'N')+str(n),'kand':kand,'p':r['p']}); state=None; continue
    if c=='dev':
        if state!='dev':
            cur={'type':None,'kand':kand,'p':r['p'],'dev':[],'tr':[],'en':[],'fn':[],'label':None}
            units.append(cur); state='dev'
        cur['dev'].append(t); continue
    if c=='tr':
        if cur is None or state not in ('dev','tr'):
            cur={'type':None,'kand':kand,'p':r['p'],'dev':[],'tr':[],'en':[],'fn':[],'label':None}
            units.append(cur)
        m=re.match(r'^(Cau|Do|So|Cha≈|Ca≈|cha≈|do|›loka)\s?\.?\s?\.?:\s*',t)
        if m:
            ty=m.group(1).lower().replace('ca≈','cha≈')
            ty={'cau':'cau','do':'do','so':'so','cha≈':'cha','›loka':'shloka'}[ty]
            if cur['type'] and cur['tr']:
                cur={'type':None,'kand':kand,'p':r['p'],'dev':[],'tr':[],'en':[],'fn':[],'label':None}; units.append(cur)
            cur['type']=ty; t=t[m.end():]
        cur['tr'].append(t); state='tr'; continue
    if c=='en':
        if cur is None: continue
        if state=='done':
            # stray english (intro text etc.)
            units.append({'type':'prose','kand':kand,'p':r['p'],'en':[t]}); state='prose'; cur=units[-1]; continue
        cur.setdefault('en',[]).append(t); state='en' if state!='prose' else 'prose'
        m=re.search(r'\(([^()]*\d[^()]*)\)\s*$',t)
        if m and cur.get('type') is not None and state=='en':
            cur['label']=m.group(1); cur['en'][-1]=t[:m.start()].rstrip(); state='done'
        continue
    if c=='fn':
        if cur is not None: cur.setdefault('fn',[]).append(t)
        continue
    if c=='ital':
        units.append({'type':'colophon','kand':kand,'p':r['p'],'en':[t]}); state='done'; continue
json.dump(units,open('en_units.json','w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter((u['kand'],u['type']) for u in units))
nolab=[u for u in units if u['type'] in ('cau','do','so','cha','shloka') and not u.get('label')]
print('no label',len(nolab))
for u in nolab[:10]: print(u['p'],u['type'],u['tr'][:1],(u.get('en') or [''])[-1][-80:])
