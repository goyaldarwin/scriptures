import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pickle,re,hb,collections
T=pickle.load(open('table.pkl','rb'))
H='्'
CONS=[chr(c) for c in range(0x915,0x93A)]+['ळ']
VS=['','ा','ि','ी','ु','ू','ृ','ॄ','े','ै','ो','ौ',H]
NAS=['','ं','ँ','ः']
seen=collections.Counter()
C='[क-हळ]़?'
for f in ('p1.pkl','p2.pkl'):
    for pg in pickle.load(open(f,'rb')):
        for l in pg:
            for s in l:
                if s['ok'] is True and s['t']:
                    for m in re.findall(f'(?:{C}{H}){{1,3}}{C}',s['t']): seen[m]+=1
cl3=[c for c in seen if c.count(H)>=2]
print(len(seen),len(cl3))
new=set()
for c in seen:
    if c.count(H)>=2: new.add(c)
    if c.count(H)<=2:
        for x in CONS: new.add(x+H+c); new.add(c+H+x)
n=0
for b in (False,True):
    tab=T[b]
    for cl in new:
        for r in ('','र्'):
            for v in VS:
                for na in NAS:
                    if v==H and na: continue
                    s=r+cl+v+na; g=tuple(hb.shape(s,b)); n+=1
                    tab.setdefault(g,[])
                    if s not in tab[g]: tab[g].append(s)
print(n)
pickle.dump(T,open('table.pkl','wb'))
