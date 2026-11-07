"""Shape generated syllables with the reference fonts; record glyph tuple -> texts."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hb, pickle, itertools
H='्'
CONS=[chr(c) for c in range(0x915,0x93A)]+['ळ','क़','ख़','ग़','ज़','ड़','ढ़','फ़','य़']
VS=['','ा','ि','ी','ु','ू','ृ','ॄ','े','ै','ो','ौ','ॅ','ॉ',H,'ॢ']
NAS=['','ं','ँ','ः']
IND=['अ','आ','इ','ई','उ','ऊ','ऋ','ॠ','ऌ','ए','ऐ','ओ','औ','ऑ','ऍ','अं','अः']
MISC=[chr(c) for c in range(0x966,0x970)]+['।','॥','॰','ऽ','ॐ',' ','-','—','‘','’','“','”','(',')','!','?',',','.',':',';','/','*','+','=','[',']','‌','‍','॑','॒','ॆ','ॊ','ॲ','ँ','ं','ः','़','x','a']
def gen():
    for s in IND+MISC:
        for n in NAS: yield s+n
        yield s
    clusters=list(CONS)
    clusters+= [a+H+b for a in CONS for b in CONS]
    for a in CONS:
        for b in CONS:
            for c in ['र','य','व','न','म','ण','त','थ','ट','ठ','क','प','ल','स','ष','श','ह','च','ञ']:
                clusters.append(a+H+b+H+c)
    for cl in clusters:
        short = cl.count(H)<2
        for r in ('','र्'):
            for v in VS:
                for n in (NAS if short or v in ('','ि','ा','ी','े','ो') else ['']):
                    if not short and n not in ('','ं'): continue
                    if v==H and n: continue
                    yield r+cl+v+n
        yield cl+H+'‌'; yield cl+H+'‍'
        yield cl+'़'
T={}
for bold in (False,True):
    tab={}
    n=0
    for s in gen():
        g=tuple(hb.shape(s,bold)); n+=1
        tab.setdefault(g,[])
        if s not in tab[g]: tab[g].append(s)
    T[bold]=tab; print('bold' if bold else 'reg', n, len(tab), file=sys.stderr)
pickle.dump(T,open('table.pkl','wb'))
