"""Finds where Tagare's numbering parts from the Gita Press's, for placement.json: the names and other Sanskrit
words of each English verse (its capitalised and diacritic words) are looked for in the Gita Press verse and its
Hindi (both in plain Roman); a path through the adhyāya that may shift Tagare's numbers by up to ±8 is chosen
(a shift costs 5), and every shift that holds for 4 verses or more and finds clearly more words (6 or more) is
listed. Each listed adhyāya is then read by hand and settled in placement.json.
  python3 shifts.py <wisdomlib copy>       (needs: pip install indic-transliteration)"""
import sys,os,re,math,unicodedata
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from read import chapters
from indic_transliteration import sanscript as S
def asc(t): return ''.join(c for c in unicodedata.normalize('NFD',t) if not unicodedata.combining(c)).lower()
STOP=set('the and that this with from which were they their them have been when then there what will shall into upon your thou thee thine said also those these whom whose being after before even like such only very other unto over about where while spoke replied'.split())
def rom(t): return re.sub(r'[^a-z]','',asc(S.transliterate(t,'devanagari','iast')))
def pre(t): return t[:min(6,max(4,len(t)-2))]
OFF=range(-8,9)
for c in chapters(sys.argv[1]):
    G=c['gp']; W=c['wl']
    if not W: continue
    hi={}
    for g in G:                                  # a joint Hindi paragraph counts for each verse it covers
        h=g['hindi']
        for k in h.get('verses',[g['n']]):
            if h.get('text'): hi[k]=hi.get(k,'')+rom(h['text'])
    blob=[rom(' '.join(g['sanskrit']))+' '+hi.get(g['n'],'') for g in G]
    Sm=[[0.0]*len(W) for _ in G]
    for j,w in enumerate(W):
        toks={asc(t) for t in re.findall(r"[^\W\d_]+",w['text']) if len(t)>=4 and (re.search(r'[^\x00-\x7f]',t) or t[0].isupper())}-STOP
        for t in toks:
            hits=[i for i,b in enumerate(blob) if pre(t) in b]
            if hits and len(hits)<=max(3,len(G)*0.25):
                for i in hits: Sm[i][j]+=math.log(len(G)/len(hits))
    num2j={k:j for j,w in enumerate(W) for k in range(w['lo'],w['hi']+1)}
    e=lambda i,o: Sm[i][num2j[G[i]['n']+o]] if G[i]['n']+o in num2j else 0.0
    V=[{o:e(0,o)-(0 if o==0 else 2) for o in OFF}]; B=[{}]
    for i in range(1,len(G)):
        v={};b={}
        for o in OFF:
            s,p=max((V[-1][p]-(0 if p==o else 5),p) for p in OFF); v[o]=s+e(i,o); b[o]=p
        V.append(v); B.append(b)
    o=max(V[-1],key=V[-1].get); path=[o]
    for i in range(len(G)-1,0,-1): o=B[i][o]; path.append(o)
    path=path[::-1]
    runs=[]
    for i,o in enumerate(path):
        if runs and runs[-1][2]==o: runs[-1][1]=i
        else: runs.append([i,i,o])
    found=[(G[a]['n'],G[b]['n'],o) for a,b,o in runs if o and b-a+1>=4 and sum(e(i,o)-e(i,0) for i in range(a,b+1))>=6]
    if found: print(c['sec'],'Gita Press verses a–b look like Tagare n+k:',found)
