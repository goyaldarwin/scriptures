import json,collections,sys,re
sys.path.insert(0,'code')
from english import convert
import parse
L=json.load(open('se_lines.json'))
pg=collections.defaultdict(list)
for l in L:
    if l['y']>30: pg[l['page']].append(l)
PAGES=[p for _,a,b in parse.KANDA_PAGES for p in range(a,b+1)]
def body(l):
    f=','.join(l['fonts'])
    if l['kind'] in('en','mix') and 'Nalandahel' in f and l['size']>=10.3: return True
    if l['kind']=='sa' and l['size']>=13: return True
    if l['kind']=='en' and l['size']>=11.5: return True
    return False
def foot(p):
    ls=pg[p]
    bys=[l['y'] for l in ls if body(l)]
    my=max(bys) if bys else 0
    return [l for l in ls if l['y']>my and (l['size']>9 or re.fullmatch(r'[.\s]{4,}',l['text']))]
if __name__=='__main__':
    tot=0
    for p in PAGES:
        f=foot(p)
        if f:
            tot+=1
            for l in parse.page_order(f):
                t=convert(l['text']) if l['kind']!='sa' else l['text']
                print(f"{p}\t{l['col']}\t{l['y']}\t{l['kind']}\t{l['size']:.1f}\t{','.join(l['fonts'])}\t{t}")
    print(tot,file=sys.stderr)
