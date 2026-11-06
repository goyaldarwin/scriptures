import json,collections,sys
sys.path.insert(0,'code')
from english import convert
L=json.load(open('se_lines.json'))
pg=collections.defaultdict(list)
for l in L:
    if l['y']>30 and l['page']>=59: pg[l['page']].append(l)
def small(l): return 9<l['size']<10.95
for p in sorted(pg):
    sm=[l for l in pg[p] if small(l)]
    if not sm: continue
    y0=min(l['y'] for l in sm)
    below=[l for l in pg[p] if l['y']>y0+2 and not small(l) and l['size']>9]
    if below:
        print(p,y0,[(l['col'],l['y'],l['kind'],l['size'],(convert(l['text']) if l['kind']!='sa' else l['text'])[:50]) for l in below][:6])
