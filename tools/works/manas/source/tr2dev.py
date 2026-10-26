import re,unicodedata
V={'a':('अ',''),'å':('आ','ा'),'i':('इ','ि'),'∂':('ई','ी'),'u':('उ','ु'),'µu':('ऊ','ू'),'æ':('ऋ','ृ'),'e':('ए','े'),'ai':('ऐ','ै'),'o':('ओ','ो'),'au':('औ','ौ')}
C={'kh':'ख','gh':'घ','ch':'छ','jh':'झ','¢h':'ठ','Œh':'ढ','th':'थ','dh':'ध','ph':'फ','bh':'भ','Rh':'ढ़',
   'k':'क','g':'ग','∆':'ङ','c':'च','j':'ज','¤':'ञ','¢':'ट','Œ':'ड','ƒ':'ण','t':'त','d':'द','n':'न','p':'प','b':'ब','m':'म','y':'य','r':'र','l':'ल','v':'व','‹':'श','›':'श','¶':'ष','s':'स','h':'ह','R':'ड़'}
TOK=sorted(list(V)+list(C)+['≈','Ú','°','¨','~',"'"],key=len,reverse=True)
def conv_word(w):
    w=w.lower().replace('Ã','≈') if False else w
    i=0; out=[]; prev=None  # prev: 'C' consonant pending (no vowel yet), 'V' vowel
    toks=[]
    while i<len(w):
        for t in TOK:
            if w.startswith(t,i): toks.append(t); i+=len(t); break
        else:
            toks.append(w[i]); i+=1
    res=''; pend=False; lastv=False
    for t in toks:
        if t in C:
            if pend: res+='्'
            res+=C[t]; pend=True; lastv=False
        elif t in V:
            if pend: res+=V[t][1]; pend=False
            else: res+=V[t][0]
            lastv=True
        elif t in ('≈','Ú'):
            if pend: res+='ं'; pend=False   # rare
            else: res+='ं'
        elif t=='°': res+='ँ'
        elif t=='¨': 
            if pend: res+='्'; pend=False
            res+='ः'
        elif t=='~':
            nasal_next=True
            continue
        else:
            if pend: res+='्'; pend=False
            res+=t
    if pend: res+='्'
    return res
def fix_hiatus(w):
    # handle '~' : vowel after ~ independent -> mark by inserting a break
    return w
def tr_clean(s):
    s=re.sub(r'uµ\s*','µu',s)
    s=s.replace('í','’')
    s=re.sub(r'(~(?:µu|ai|au|[aåi∂ueo]))\s*\.(?=\s*[A-Za-zåæ∂µ¶‹›¢Œƒ≈R])',r'\1',s)
    s=re.sub(r'~(µu|ai|au|[aåi∂ueo])°?',r'\1°',s)
    s=re.sub(r'°\s+([,.])',r'°\1',s)
    return s
def tr2dev(s):
    s=tr_clean(s)
    s=s.replace('Ú','≈').replace('’','')
    words=re.split(r'(\s+|[,.;!?\-]+|\d+)',s)
    out=[]
    for w in words:
        if not w or re.fullmatch(r'\s+|[,.;!?\-]+|\d+',w): out.append(w); continue
        # split at ~ : treat subsequent vowel as independent
        parts=w.split('~')
        o=conv_word(parts[0])
        for p in parts[1:]:
            o+=conv_word(p) if p and p[0] not in 'aåi∂uµæeo' else conv_word2(p)
        out.append(o)
    return unicodedata.normalize('NFC',''.join(out))
def conv_word2(p):
    # starts with vowel: independent
    return conv_word(p)
if __name__=='__main__':
    for s in ['samåcåra kahi janaka sunåe, jehi kårana mah∂pa saba åe.','hædaya° na hara¶u bi¶ådu kachu bole ‹r∂raghub∂ru.270.','ba≈da~u° guru pada paduma parågå','kahu jaRa janaka dhanu¶a kai torå.','socahiÚ sakala tråsa ura bhår∂.3.','vi‹uddhavij¤ånau','svånta¨sukhåya']:
        print(s,'->',tr2dev(s))
