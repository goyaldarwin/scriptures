import pickle,re,sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from hi_decode import *
pages=pickle.load(open('hi_trace.pkl','rb'))
outp=[]
for pi,spans in enumerate(pages):
    items=[]
    dec=[]
    for f,size,ch in spans:
        tab=B if 'Bold' in f else R
        dec.append(decode([(u,g) for u,g,b in ch],tab) if ch else '')
    for si,(f,size,ch) in enumerate(spans):
        if not ch: continue
        txt=dec[si]
        if len(ch)==1 and ch[0][0]==32 and 0<si<len(spans)-1 and spans[si+1][2] and abs(spans[si+1][2][0][2][0]-ch[0][2][0])<0.3:
            a=dec[si-1]; nb=dec[si+1]
            if a.endswith('्'): txt='\u200c'
            elif a and nb and a[-1] in CONS and nb[0] in CONS: txt='्'
            else: txt=''
        x0=min(c[2][0] for c in ch); y1=max(c[2][3] for c in ch); y0=min(c[2][1] for c in ch)
        items.append((round(y1,1),x0,txt,'B' if 'Bold' in f else '',size,y0))
    # group lines by y1 tolerance
    items.sort(key=lambda t:(t[0],t[1]))
    lines=[]
    for it in items:
        if lines and abs(it[0]-lines[-1]['y'])<4:
            lines[-1]['it'].append(it)
        else: lines.append({'y':it[0],'it':[it]})
    res=[]
    for l in lines:
        l['it'].sort(key=lambda t:t[1])
        t=''.join(i[2] for i in l['it'])
        t=re.sub(r'\s+',' ',t).strip()
        if t: res.append({'y':l['y'],'x':l['it'][0][1],'t':t,'b':any(i[3] for i in l['it']),'s':max(i[4] for i in l['it'])})
    outp.append(res)
json.dump(outp,open('hi_text.json','w'),ensure_ascii=False)
open('hi_text_p60.txt','w').write('\n'.join(l['t'] for l in outp[59]))
print(open('hi_text_p60.txt').read()[:1500])
import collections
unk=collections.Counter(m for pg in outp for l in pg for m in re.findall(r'⟨\d+⟩',l['t']))
print(unk)
