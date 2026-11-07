import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pickle,hb
from fontTools.ttLib import TTFont
T=pickle.load(open('table.pkl','rb'))
H='्'
cm=TTFont('Ref-Regular.ttf').getBestCmap()
IND=['अ','आ','इ','ई','उ','ऊ','ऋ','ॠ','ऌ','ए','ऐ','ओ','औ','ऑ']
NAS=['','ं','ँ','ः']
VS=['','ा','ि','ी','ु','ू','ृ','ॄ','े','ै','ो','ौ',H]
S=set(chr(u) for u in cm if u>=0x20)
for v in IND:
    for n in NAS: S.add('र्'+v+n); S.add(v+n)
CONS=[chr(c) for c in range(0x915,0x93A)]+['ळ']
for c in CONS:
    for n in ['़']:
        for v in VS:
            for na in NAS: S.add(c+n+v+na); S.add('र्'+c+n+v+na)
for b in (False,True):
    for s in S:
        g=tuple(hb.shape(s,b)); T[b].setdefault(g,[])
        if s not in T[b][g]: T[b][g].append(s)
pickle.dump(T,open('table.pkl','wb'))
