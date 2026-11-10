"""python3 tools/meanings/pa_words_prepare.py OUT_DIR  (after tools/meanings/teeka.py fetch)

Batches for the Punjabi senses of library/glossary/pa.json: each word with its entry, lines where it occurs
(Sukhmani, Japji, then the Granth) and the Darpan/Faridkot ਪਦਅਰਥ glosses of it."""
import json, re, os, sys, unicodedata
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G=json.load(open(f'{R}/library/glossary/pa.json'))
lines=[]
for w in ('sukhmani-sahib','japji-sahib','guru-granth-sahib'):
    cur=None
    for l in open(f'{R}/tools/works/{w}/text.txt',encoding='utf-8'):
        l=l.rstrip('\n')
        if l.startswith('['): cur=l.split(']')[0][1:].split()[0]; l=l.split(']',1)[1].strip()
        if not l or l[0] in '#@': continue
        if re.search('[਀-੿]',l): lines.append((w.split('-')[0]+':'+(cur or ''),l))
idx={}
for i,(ref,l) in enumerate(lines):
    for t in set(re.findall(r'[਀-੿]+',l)): idx.setdefault(t,[]).append(i)
gl={}
for src in ('darpan','faridkot'):
    for l in open(os.path.expanduser(f'~/.cache/scriptures-dict/{src}.txt'),encoding='utf-8'):
        for m in re.finditer(r'([਀-੿]+(?: [਀-੿]+)?)\s*[—–-]\s*([^।|]{1,80})',l):
            for k in {m.group(1), m.group(1).split()[0]}:
                L=gl.setdefault(k,{}).setdefault(src,[])
                g=m.group(2).strip()
                if g not in L and len(L)<4: L.append(g)
OUT=sys.argv[1]
keys=list(G); n=125; os.makedirs(OUT,exist_ok=True)
stat=[0,0]
for b in range(0,len(keys),n):
    with open(f'{OUT}/batch-{b//n+1:02d}.md','w',encoding='utf-8') as f, open(f'{OUT}/batch-{b//n+1:02d}.keys','w') as fk:
        for k in keys[b:b+n]:
            e=G[k]; fk.write(k+'\n')
            f.write(f"## {k}\nentry: hi {e.get('hi')} | en {e.get('en')} | g {e.get('g','')}\n")
            for i in idx.get(k,[])[:3]: f.write(f"line ({lines[i][0]}): {lines[i][1]}\n")
            gg=gl.get(k,{})
            stat[0]+=bool(gg); stat[1]+=1
            for src,L in gg.items(): f.write(f"{src}: "+' · '.join(L)+"\n")
            f.write('\n')
print(len(keys),'words',(len(keys)+n-1)//n,'batches; with a commentary gloss',stat[0])
