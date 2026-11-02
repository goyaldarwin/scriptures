import json,collections,sys,re,pickle
sys.path.insert(0,'code'); sys.path.insert(0,'fn')
from english import convert
import parse2
from foot import foot, PAGES, pg, body
import foot as _F
L=_F.L
book=parse2.parse(L)
# check identical to book.json
B=json.load(open('book.json'))
for k1,k2 in zip(book,B):
    for s1,s2 in zip(k1['sargas'],k2['sargas']):
        a=[(e['from'],e['to'],e['text']) for e in s1['en']]; b=[(e['from'],e['to'],e['text']) for e in s2['en']]
        assert a==b,(k1['kanda'],s1['heading'])
print('parse2 matches book.json')
# line id -> (kanda, sargakey, sarga, offset)
where={}
order=[]  # global reading order
for k in book:
    reg=0;pk=0
    for sg in k['sargas']:
        if 'प्रक्षिप्त' in sg['heading']: pk+=1; key=f'p{pk}'
        else: reg+=1; key=str(reg)
        sg['key']=key
        for i,l in enumerate(sg.get('en_objs',[])):
            where[id(l)]=(k['kanda'],key,sg,sg['line_offs'][i])
def para_at(sg,off):
    for j,e in enumerate(sg['raw_en']):
        if e['s']<=off<e['e'] or (j==len(sg['raw_en'])-1 and off>=e['s']): return j
    # offset before first para start? (in printed mark region) 
    for j,e in enumerate(sg['raw_en']):
        if off<e['e']: return j
    return None
pickle.dump(None,open('/dev/null','wb'))
import parse
from notes import rows, MARKRE
SKIP_PAGES={71}
TWO_COL={1326,1327}
def txt(l): return convert(l['text']) if l['kind']!='sa' else l['text']
def page_rows(p):
    if p not in TWO_COL: return rows(p)
    out=[]
    for col in (0,2,1):
        for l in sorted([l for l in foot(p) if l['col']==col and txt(l).strip()],key=lambda l:l['y']):
            out.append({'page':p,'y':l['y'],'text':txt(l).strip(),'cols':[col],'kinds':[l['kind']]})
    return out
notes=[]
for p in PAGES:
    if p in SKIP_PAGES: continue
    for r in page_rows(p):
        m=MARKRE.match(r['text'])
        if p in TWO_COL and m and m[1].endswith('.') and notes and notes[-1].get('pre'):
            notes[-1]['rows'].append(r); del notes[-1]['pre']; continue
        if p in TWO_COL and m and m[1].endswith('.'):
            notes.append({'page':p,'mark':m[1].rstrip('.'),'rows':[r]}); continue
        if p in TWO_COL and r['text'].startswith('We have read in the B'):
            notes.append({'page':p,'mark':'15','rows':[r],'pre':True}); continue
        if m and not (m[1].endswith('.') and r['kinds'][0]=='sa'):
            notes.append({'page':p,'mark':m[1].rstrip('.'),'rows':[r]})
        elif notes and notes[-1].get('pre'):
            notes[-1]['rows'].append(r); del notes[-1]['pre']
        elif notes and (notes[-1]['rows'][-1]['page']==p or (m and r['kinds'][0]=='sa')):
            notes[-1]['rows'].append(r)
        else:
            assert notes
            notes[-1]['rows'].append(r); notes[-1]['cont']=p
# 1793: eight numbered notes printed run-on in one paragraph
def jointext(rows_):
    return ' '.join(r['text'] for r in rows_)
out=[]
for n in notes:
    if n['page']==1793 and n['mark']=='1':
        t=jointext(n['rows'])
        parts=re.split(r'\s(?=[2-8]\.\s)',t)
        for i,pt in enumerate(parts):
            out.append({'page':1793,'mark':str(i+1),'rows':[dict(n['rows'][0],text=pt if i else pt)]})
        continue
    out.append(n)
notes=out
# fix the '15' intro placement: the "We have read" row precedes item 15
fixed=[]
for n in notes:
    if n['mark']=='15' and n['page']==1326 and n['rows'][0]['text'].startswith('We have'):
        pass
    fixed.append(n)
# marks
def host(sup,p):
    cands=[l for l in pg[p] if body(l) and l['col']==sup['col'] and -1<=l['y']-sup['y']<=9]
    if not cands: cands=[l for l in pg[p] if body(l) and -1<=l['y']-sup['y']<=9]
    return min(cands,key=lambda l:abs(l['y']-sup['y']-4)) if cands else None
def page_marks(p):
    fy={id(l) for l in foot(p)}
    ordr=[l for l in parse.page_order(pg[p]) if id(l) not in fy]
    rank={id(l):i for i,l in enumerate(ordr)}
    out=[]
    for l in ordr:
        if l['size']<9:
            if re.fullmatch(r'[\d\s]+',l['text']):
                h=host(l,p)
                for d in l['text'].split():
                    out.append({'kind':'sup','mark':d,'line':h,'sup':l,'idx':None})
            continue
        for i,ch in enumerate(l['text']):
            if ch in '*†‡': out.append({'kind':'sym','mark':ch,'line':l,'idx':i})
    return out
# global reading order of lines for fallback
seq=[]
for k in book:
    pass
allorder=[]
for kn,a,b in parse.KANDA_PAGES:
    for p in range(a,b+1):
        fy={id(l) for l in foot(p)}
        allorder+= [l for l in parse.page_order(pg[p]) if id(l) not in fy]
gpos={id(l):i for i,l in enumerate(allorder)}
def locate(line,idx):
    """verse id for a mark in a body line; (vid, how)"""
    how='mark'
    if line['kind']=='sa':
        # a mark on a Sanskrit verse: the English paragraph covering that verse
        i=gpos[id(line)]
        while not re.search(r'॥\s*[०-९]+\s*॥',allorder[i]['text']) or allorder[i]['kind']!='sa': i+=1
        vn=int(re.search(r'॥\s*([०-९]+)\s*॥',allorder[i]['text'])[1].translate(parse.DIG))
        j0=i
        while id(allorder[j0]) not in where: j0+=1
        kn,key,sg,off=where[id(allorder[j0])]
        for j,e in enumerate(sg['raw_en']):
            if e['from']<=vn<=(e['to'] or e['from']):
                return kn,key,sg,j,e,f'mark on the Sanskrit of verse {vn}: its English paragraph'
    if id(line) not in where:
        i=gpos[id(line)]
        while i>=0 and id(allorder[i]) not in where: i-=1
        if i<0: print('NOPREV',line); raise SystemExit
        line=allorder[i]; idx=None; how='mark (line not in parsed English: preceding English line used)'
    kn,key,sg,off=where[id(line)]
    t=line['text']
    if idx is None:
        a=para_at(sg,off); b=para_at(sg,off+len(t)-1)
        if a!=b: how+=f'; LINE SPANS TWO PARAGRAPHS'
        j=a
    else:
        pos=off+idx
        j=para_at(sg,pos)
        if j and pos-sg['raw_en'][j]['s']<=1:
            j-=1; how+=' (mark follows the verse number: previous paragraph)'
    e=sg['raw_en'][j]
    return kn,key,sg,j,e,how
res=[]
bypage=collections.defaultdict(list)
for n in notes: bypage[n['page']].append(n)
orphans=[]
for p in sorted(set(bypage)|{p for p in PAGES if page_marks(p)}):
    mk=page_marks(p); ns=bypage[p]
    used=set()
    for n in ns:
        cands=[i for i,m in enumerate(mk) if m['mark']==n['mark'] and i not in used]
        if cands:
            i=cands[0]; used.add(i); n['m']=mk[i]
        else: n['m']=None
    for i,m in enumerate(mk):
        if i not in used: orphans.append((p,m['mark'],convert(m['line']['text']) if m['line'] else None))
for n in notes:
    m=n['m']
    if m and m['line'] is not None:
        kn,key,sg,j,e,how=locate(m['line'],m['idx'])
        n['how']=how; n['ctx']=convert(m['line']['text'])
    else:
        # position: last English line before the note on the page
        p=n['page']
        prev=[l for l in allorder if l['page']==p and id(l) in where]
        line=prev[-1]
        kn,key,sg,j,e,how=locate(line,len(line['text'])-1)
        n['how']='POSITION (no mark found)'; n['ctx']=convert(line['text'])
    if n['page']==1220:
        e=next(x for x in sg['raw_en'] if x['to']==2); n['how']='NO MARK PRINTED: attached by content (the note glosses "without passing through the gate", English of verses 1-2); by position it would be sundara.4.3'
    if n['page']==871:
        kn='aranya'; key='p1'; sg=next(x for x in book[2]['sargas'] if x.get('key')=='p1'); e=sg['raw_en'][0]
        n['how']='mark on the heading "An Interpolated Canto*": attached to the first paragraph of that canto'
    to=e['to']
    if to is None: n['how']+='; paragraph has no closing verse mark'; to=e['from']
    n['vid']=f"{kn}.{key}.{to}"; n['para']=(e['from'],e['to'],e['printed'])
for i,n in enumerate(notes):
    if n['page']==1326 and n['mark']=='*':
        nx=notes[i+1]; n['vid']=nx['vid']; n['para']=nx['para']; n['how']='NO MARK PRINTED: heading of the numbered notes 1-15 that follow; attached with note 1'
print('orphan marks',orphans)
pickle.dump([{k:v for k,v in n.items() if k!='m'} for n in notes],open('fn/notes_mapped.pkl','wb'))
# body English lines the parser left out (for the report)
drop=collections.Counter(); ex=collections.defaultdict(list)
for l in allorder:
    if l['col']==2 or id(l) in where: continue
    if l['kind'] in ('en','mix') and 'Nalandahel' in ','.join(l['fonts']) and 10.3<=l['size']<=12.5:
        k=(l['kind'],l['size'],l['fonts'][0])
        drop[k]+=1; ex[k].append(l['page'])
for k,v in drop.most_common(): print('DROPPED',k,v,ex[k][:8])
for l in pg[2151]:
    if '*' in l['text'] and l['y']>30:
        r=locate(l,l['text'].index('*')); print('ORPHAN2151',f"{r[0]}.{r[1]}.{r[4]['to']}")
