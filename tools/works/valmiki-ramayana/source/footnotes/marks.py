import json,collections,sys,re
sys.path.insert(0,'code'); sys.path.insert(0,'fn')
from english import convert
from foot import foot, PAGES, pg, body
def marks(p):
    """(kind, mark, line) for every footnote mark in the page body"""
    fy={id(l) for l in foot(p)}
    out=[]
    for l in pg[p]:
        if id(l) in fy: continue
        t=l['text']
        if l['size']<9:
            if re.fullmatch(r'\s*\d{1,2}\s*',t): out.append(('sup',t.strip(),l))
            continue
        for ch in '*†‡':
            for _ in range(t.count(ch)): out.append(('sym',ch,l))
    return out
if __name__=='__main__':
    notes=json.load(open('fn/notes_raw.json'))
    bypage=collections.defaultdict(list)
    for n in notes:
        if n['mark']: bypage[n['page']].append(n['mark'])
    allp=set(bypage)|{p for p in PAGES if marks(p)}
    tot=0
    for p in sorted(allp):
        mk=[m[1] for m in marks(p)]
        tot+=len(mk)
        nm=[x.rstrip('.') for x in bypage[p]]
        if sorted(mk)!=sorted(nm): print(p,'marks',mk,'notes',nm,[ (m[0],m[2]['kind'],m[2]['size'],m[2]['text'][:40]) for m in marks(p)])
    print('total marks',tot)
