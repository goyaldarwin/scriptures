import json,re,unicodedata,os,glob
m=json.load(open('merged.json')); items=m['items']; eg=m['en_groups']; pauses=m['pauses']
from tr2dev import tr_clean
KANDS=['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar']
KHI=['बालकाण्ड','अयोध्याकाण्ड','अरण्यकाण्ड','किष्किन्धाकाण्ड','सुन्दरकाण्ड','लङ्काकाण्ड','उत्तरकाण्ड']
KEN=['Bāla-kāṇḍa','Ayodhyā-kāṇḍa','Araṇya-kāṇḍa','Kiṣkindhā-kāṇḍa','Sundara-kāṇḍa','Laṅkā-kāṇḍa','Uttara-kāṇḍa']
def en_fix(s):
    rep=[('ì','“'),('î','”'),('í','’'),('ë','‘'),('ó','—'),('µu','ū'),('µ','ū'),('å','ā'),('Å','Ā'),('∂','ī'),('æ','r̥'),('≈','ṁ'),('¢','ṭ'),('Œ','ḍ'),('ƒ','ṇ'),('‹','ś'),('›','Ś'),('¶','ṣ'),('¨','ḥ'),('∆','ṅ'),('¤','ñ'),('°','̐')]
    for a,b in rep: s=s.replace(a,b)
    s=re.sub(r'\s+',' ',s).strip()
    s=s.replace(' ,',',').replace(' .','.')
    return unicodedata.normalize('NFC',s)
def tr_fix(s):
    s=tr_clean(s)
    s=s.replace('Ú','≈'); s=re.sub(r'(?<=[a-zåæ∂µ¶¢Œƒ≈°‹])R','ṛ',s)
    s=en_fix(s)
    s=re.sub(r'\.(\d+[A-Z]?)\.$',r' ॥\1॥',s)
    s=re.sub(r'\.$',' ।',s).replace(',',' ।',1) if False else s
    return s
def hi_fix(s):
    s=unicodedata.normalize('NFC',s)
    s=re.sub(r'\s+',' ',s).strip()
    return s
# items
out=[]; idindex={}
for i,it in enumerate(items):
    k=KANDS.index(it['kand'])
    d={'id':it['id'],'k':k,'s':it['sec'],'y':it['type'],'n':it['n'],'v':[hi_fix(x) for x in it['v']],'h':hi_fix(it['hi']),'t':[tr_fix(x) for x in it['tr']]}
    if it['fn']: d['f']=[hi_fix(x) for x in it['fn']]
    if it['en_g']: d['g']=it['en_g'][0]
    out.append(d); idindex[it['id']]=i
groups={}
for gid,g in eg.items():
    if not g['items']: continue
    groups[gid]={'x':en_fix(g['text']),'l':en_fix(g['label'] or ''),'i':g['items']}
    if g['fn']: groups[gid]['f']=[en_fix(x) for x in g['fn']]
# mark last item of group
for gid,g in groups.items():
    last=max(g['i']); out[last]['gl']=1
# pauses
P={'M':{},'N':{}}
for v,i in pauses: P[v[0]][int(v[1:])]=i
# vidhi
t=json.load(open('hi_text.json'))
vb=[]
for pi in range(16,31):
    for l in t[pi]:
        s=hi_fix(re.sub(r'।\s*।','।।',l['t'])); s=re.sub(r'।।\s*([०-९]+)\s*।।',r'।।\1।।',s)
        if s.startswith('।। श्रीहरिः'): continue
        if l['s']>=20: vb.append(['h',s])
        elif l['s']>=17: vb.append(['v',s])
        else:
            if vb and vb[-1][0]=='p' and l['x']<80: vb[-1][1]+=' '+s
            else: vb.append(['p',s])
aarti=[hi_fix(re.sub(r'।\s*।','।।',l['t'])) for l in t[971]]
# english procedure pages 14-18
er=json.load(open('en_rows.json'))
evb=[]
for r in er:
    if 14<=r['p']<=18 and r['y']>=85 and '"""' not in r['t'] and not re.fullmatch(r'[\[\]XVI\d ]+',r['t']):
        f=r['f']; tot=sum(f.values()) or 1
        if sum(v for k2,v in f.items() if k2.startswith('Chanakya'))/tot>0.5: continue
        kind='v' if f.get('NalandahelBold',0)/tot>0.5 else 'p'
        s=tr_fix(r['t']) if kind=='v' else en_fix(r['t'])
        if r['s']>=12.5 and kind=='p' and len(s)<40: kind='h'
        if evb and evb[-1][0]==kind and kind=='p' and not evb[-1][1].endswith(('.','”',':—','—')): evb[-1][1]+=' '+s
        else: evb.append([kind,s])
FX=json.load(open('text_fixes.json')); nf=0
for d in out:
    for a,b in FX.get(d['id'],[]):
        nv=[l.replace(a,b) for l in d['v']]
        if nv==d['v']: print('FIX NOT APPLIED',d['id'],a)
        else: nf+=1
        d['v']=nv
print('fixes applied',nf)
import sys; sys.path.insert(0,'split'); from apply_lib import apply as _sp; from tr_fix import fix as _tfix; _tfix(out); from en_fix2 import fix as _ef; _ef(groups); _sp(out,groups)
data={'kands':[{'hi':KHI[i],'en':KEN[i]} for i in range(7)],'it':out,'eg':groups,'P':P,'vidhi':dict(zip(('hi','en'),__import__('vidhi').build(vb,evb,out)),aarti=aarti)}
if os.path.exists('topics_final.json'): data['topics']=json.load(open('topics_final.json'))
if os.path.exists('gloss_final.json'): data['gloss']=json.load(open('gloss_final.json'))
from vidhi_gloss import vg as _vg, aarti_gloss as _ag
data['vg']=_vg()
for _k,_v in _ag().items(): data['gloss'].setdefault(_k,_v)
s=json.dumps(data,ensure_ascii=False,separators=(',',':'))
open('app_data.json','w').write(s)
print('size MB',round(len(s.encode())/1e6,2))
print(out[13]); print(groups[str(out[13]['g'])]['x'][:200])
print(evb[:6])
