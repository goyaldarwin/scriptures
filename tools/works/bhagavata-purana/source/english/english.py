"""Tagare's English on the Gita Press verses -> meanings/en/tagare.json.
  python3 english.py <wisdomlib copy> <work folder>
Each Gita Press verse takes Tagare's verse of the same number, unless placement.json says otherwise for its
adhyāya ({"gp":[a,b],"off":k}: verses a–b take Tagare's n+k; {"gp":[a,b],"wl":[x,y]}: verses a–b together take
Tagare's x–y; {"gp":[a,b],"none":true}: no English). Gita Press verses and Tagare's verses that are linked form
one meaning, under the last of the Gita Press verses, with their numbers when there are several ("(24–27)");
Tagare's footnotes go with it. shifts.py finds the adhyāyas whose numbers part, for placement.json."""
import json,os,re,sys,collections
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE); sys.path.insert(0,os.path.join(HERE,'..','..','..','..'))
from read import chapters
import jsonio
SRC,WORK=sys.argv[1],sys.argv[2]
PL=json.load(open(os.path.join(HERE,'placement.json')))
ids=[m.group(1) for m in re.finditer(r'^\[(\S+)',open(os.path.join(WORK,'text.txt'),encoding='utf-8').read(),re.M)]
IDS=set(ids)
def clean(t): return re.sub(r'\s+',' ',t.replace('{GL_NOTE::}','')).strip()
M={}; N={}; st=collections.Counter(); left=[]
for c in chapters(SRC):
    sec=c['sec']; W=c['wl']
    if not W: st['adhyāyas without English']+=1; continue
    tgt={g['n']:{g['n']} for g in c['gp']}
    for r in PL.get(sec,[]):
        for n in range(r['gp'][0],r['gp'][1]+1):
            if n not in tgt: continue
            tgt[n]=set() if r.get('none') else {n+r['off']} if 'off' in r else set(range(r['wl'][0],r['wl'][1]+1))
    num2g={k:i for i,g in enumerate(W) for k in range(g['lo'],g['hi']+1)}
    par={}
    def f(x):
        while par.setdefault(x,x)!=x: x=par[x]
        return x
    for n,ks in tgt.items():
        for k in ks:
            if k in num2g: par[f(('g',n))]=f(('w',num2g[k]))
    comp=collections.defaultdict(lambda:(set(),set()))
    for x in list(par): comp[f(x)][0 if x[0]=='g' else 1].add(x[1])
    used=set(); covered=set()
    for gp,wl in comp.values():
        if not gp or not wl: continue
        gp=sorted(gp); wl=sorted(wl); vid=f"{sec}.{gp[-1]}"
        assert vid in IDS,vid
        used|=set(wl); covered|=set(gp)
        M[vid]=' '.join(clean(W[i]['text']) for i in wl)+(f" ({gp[0]}–{gp[-1]})" if len(gp)>1 else '')
        fn=[]
        for i in wl:
            for k in W[i]['fn']:
                t=c['fnotes'].get(str(k))
                if t and clean(t) not in fn: fn.append(clean(t))
        if fn: N[vid]=fn
    st['Gita Press verses with English']+=len(covered)
    st['Gita Press verses without']+=len(tgt)-len(covered)
    for i,g in enumerate(W):
        if i not in used: left.append(f"{sec}: Tagare {g['lo']}{'–'+str(g['hi']) if g['hi']>g['lo'] else ''}")
st['meanings']=len(M); st['footnotes']=sum(map(len,N.values())); st["Tagare's verses not placed"]=len(left)
order=[i for i in ids if i in M]
jsonio.dump_meanings(os.path.join(WORK,'meanings','en','tagare.json'),{
 "about":"G. V. Tagare's English translation (Motilal Banarsidass, Ancient Indian Tradition and Mythology), from the owner's copy of wisdomlib.org, with Tagare's footnotes. Tagare translates another edition, so his verses are placed on the Gita Press verses by their content (source/english/): a translation covering several Gita Press verses sits under the last of them with their numbers; a verse his edition lacks, or that the copy has lost, has none",
 "title":{"hi":"तगारे — अंग्रेज़ी अनुवाद","en":"Tagare — English translation"},"order":2,"copied":True,
 "m":{k:M[k] for k in order},"notes":{k:N[k] for k in order if k in N}})
print(dict(st))
open(os.path.join(HERE,'not_placed.txt'),'w',encoding='utf-8').write("Tagare's verses not placed on a Gita Press verse (written by english.py)\n"+'\n'.join(left)+'\n')
