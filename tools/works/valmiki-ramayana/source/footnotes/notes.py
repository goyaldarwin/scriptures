import json,collections,sys,re
sys.path.insert(0,'code'); sys.path.insert(0,'fn')
from english import convert
from foot import foot, PAGES, pg
RANK={0:0,2:1,1:2}
SKIP_PAGES={71}
def txt(l):
    if re.fullmatch(r'[.\s]{4,}',l['text']): return '…'
    return convert(l['text']) if l['kind']!='sa' else l['text']
def rows(p):
    ls=[l for l in foot(p) if txt(l).strip() and not (l['kind']=='sa' and txt(l).strip()=='.')]
    D=lambda l: bool(re.fullmatch(r'[.\s]{4,}',l['text']))
    ey=lambda l: l['y']+4 if D(l) else l['y']
    ls.sort(key=ey)
    groups=[]
    for l in ls:
        if groups and ey(l)-ey(groups[-1][-1])<=2.5: groups[-1].append(l)
        else: groups.append([l])
    out=[]
    for g in groups:
        g.sort(key=lambda l:(RANK[l['col']], (0 if l['col']==1 else 2) if D(l) else 1))
        s=''
        for l in g:
            t=txt(l)
            if not s: s=t
            elif re.match(r'\s*[.,;)]',t) : s=s.rstrip()+t.strip()
            else: s=s.rstrip()+' '+t.strip()
        out.append({'page':p,'y':g[0]['y'],'text':re.sub(r'  +',' ',s.strip()),'cols':[l['col'] for l in g],'kinds':[l['kind'] for l in g]})
    return out
MARKRE=re.compile(r'^([*†‡•]|\d{1,2}\.)\s*')
if __name__=='__main__':
    notes=[]
    for p in PAGES:
        if p in SKIP_PAGES: continue
        for r in rows(p):
            m=MARKRE.match(r['text'])
            if m and not (m[1].endswith('.') and r['kinds'][0]=='sa'):
                notes.append({'page':p,'mark':m[1],'y':r['y'],'rows':[r]})
            elif notes and (notes[-1]['rows'][-1]['page']==p or (m and r['kinds'][0]=='sa')):
                notes[-1]['rows'].append(r)
            else:
                notes.append({'page':p,'mark':None,'y':r['y'],'rows':[r]})
    json.dump(notes,open('fn/notes_raw.json','w'),ensure_ascii=False,indent=0)
    print(len(notes), collections.Counter(n['mark'] for n in notes))
    for n in notes:
        if n['mark'] is None: print('CONT',n['page'],n['rows'][0]['text'][:80])
