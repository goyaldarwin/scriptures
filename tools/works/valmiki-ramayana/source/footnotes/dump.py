import json,collections,sys
sys.path.insert(0,'code')
from english import convert
import parse
L=json.load(open('se_lines.json'))
pg=collections.defaultdict(list)
for l in L: pg[l['page']].append(l)
out=open('fn/small.txt','w')
for p in range(59,2304):
    ls=[l for l in parse.page_order(pg[p]) if l['size']<10.95 and l['y']>30]
    for l in ls:
        t=convert(l['text']) if l['kind']!='sa' else l['text']
        out.write(f"{p}\t{l['col']}\t{l['y']}\t{l['kind']}\t{l['size']:.1f}\t{','.join(l['fonts'])}\t{t}\n")
