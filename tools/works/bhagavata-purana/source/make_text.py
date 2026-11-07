"""book2.json (the decoded, structured book) -> text.txt, meanings/hi/gitapress.json, topics; see README.md"""
import json,re,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
import textfile
D='०१२३४५६७८९'; DEV=str.maketrans('0123456789',D)
def dev(n): return str(n).translate(DEV)
HERE=os.path.dirname(os.path.abspath(__file__)); CWD=os.getcwd()
OUT=sys.argv[1]
book=json.load(open(os.path.join(CWD,'book2.json')))
COR=json.load(open(os.path.join(HERE,'corrections.json')))
sys.path.insert(0,os.path.join(HERE,'..','..','..','text'))
from standard import sanskrit as _san
STD=lambda w: _san(w)
HAL=json.load(open(os.path.join(HERE,'halant.json')))   # words whose ्य the e-book drops (halant.py)
EN={}
for l in open(os.path.join(HERE,'topics_en.tsv'),encoding='utf-8'):
    k,v=l.rstrip('\n').split('\t'); EN[k]=v
END=re.compile(r'॥\s*([०-९]+)\s*(॥)?\s*$')
def fix_title(t): return re.sub(r'-\s+','-',t)
items=[]; topics=[]; mean={}; notes={}; part_keys=[]; ends={}
for pi,sk in enumerate(book):
    pk='mahatmya' if sk['n']==0 else str(sk['n']); part_keys.append(pk)
    sp='m' if sk['n']==0 else str(sk['n'])
    for a in sk['adh']:
        sec=f"{sp}.{a['n']}"
        ty='mshloka' if sk['n']==0 else 'shloka'
        first=True
        def add(it):
            global first
            items.append(it)
            if first: topics.append(dict(id=it['id'],hi=fix_title(a['title']),en=EN[sec])); first=False
        if sk['n']==0 and a['n']==1:
            add(dict(id='m.1.0',p=pi,s=sec,y=ty,n='',v=[re.sub(r'॥$',' ॥',l) for l in sk['pre']]))
        for v in a['verses']:
            vid=f"{sec}.{v['n']}"
            lines=[l for k,l,m in v['lines']]
            # the e-book wraps a long pāda in two lines: a half-verse of four lines is two pādas
            if v['kind']=='v':
                segs=[]; cur=[]
                for l in lines:
                    cur.append(l)
                    if re.search(r'[।॥]',l): segs.append(cur); cur=[]
                if cur: segs.append(cur)
                out=[]
                for sg in segs:
                    if len(sg)==4:
                        for i in (0,2):
                            x,y=sg[i],sg[i+1]
                            out.append(x[:-1]+y if x.endswith('-') else x+' '+y)
                    else: out+=sg
                lines=out
            lines=[l for l in lines]
            lines[-1]=END.sub(lambda m:' ॥'+m.group(1)+'॥',lines[-1])
            lines=v['spk']+lines
            def hal(t):
                core=t.rstrip('-'); tail=t[len(core):]
                k=core if core in HAL else STD(core)
                return HAL[k]+tail if k in HAL else t
            lines=[' '.join(hal(t) for t in l.split(' ')) for l in lines]
            for old,new,why in COR.get(vid,[]):
                assert any(old in l for l in lines),(vid,old)
                lines=[l.replace(old,new) for l in lines]
            add(dict(id=vid,p=pi,s=sec,y=('gadya' if v['kind']=='g' else ty),n=str(v['n']),v=lines))
        col=' '.join(a['col']); col=re.sub(r'\s*॥\s*([०-९]+)\s*॥\s*$',r' ॥\1॥',col)
        add(dict(id=f"{sec}.iti",p=pi,s=sec,y='iti',n='',v=[col]))
        ends[sec]=f"{sec}.iti"
        # meanings: each chunk under the last verse it covers
        for c in a['mchunks']:
            mk='॥ '+dev(c['a'])+('-'+dev(c['b']) if c['b']!=c['a'] else '')+' ॥' if c.get('fixed') else re.sub(r'॥\s*(.*?)\s*॥',r'॥ \1 ॥',c['mark'])
            mean[f"{sec}.{c['b']}"]=(c['t']+' '+mk+c.get('after','')).strip()
        # the book's notes (source/notes.py), under the meaning that carries their mark, in the order printed
        for tid,kind,ch,txt in a.get('fnotes',[]):
            if kind=='v':
                n=int(tid.rsplit('.',1)[1]); tid=next(f"{sec}.{c['b']}" for c in a['mchunks'] if c['a']<=n<=c['b'])
            notes.setdefault(tid,[]).append(ch+' '+txt)
ids=[x['id'] for x in items]; IDS=set(ids)
assert not [k for k in notes if k not in mean]
bad=[k for k in mean if k not in IDS]; assert not bad,bad[:5]
textfile.write(os.path.join(OUT,'text.txt'),items,topics,part_keys,'sa',[
 'Śrīmad Bhāgavata Mahāpurāṇa with the Śrīmad Bhāgavata Māhātmya: made by source/make_text.py from the owner\'s Gita Press',
 'books (codes 26–27, read from their glyph ids, no OCR); change it there, not here. Every correction and choice: reconciliation.md.'])
M={"about":"Gita Press, Śrīmad Bhāgavata Mahāpurāṇa with its simple Hindi commentary (codes 26–27), read from its glyph ids (source/decode.py); each paragraph's meaning sits under the last verse its mark names, every mark kept as printed (a misprinted mark corrected: reconciliation.md); the book's notes (*, †, ‡) under the meaning that carries their mark (source/notes.py)",
   "title":{"hi":"गीताप्रेस — सरल हिन्दी व्याख्या","en":"Gita Press — Hindi commentary"},"order":1,"copied":True,"m":{k:mean[k] for k in ids if k in mean},
   "notes":{k:notes[k] for k in ids if k in notes}}
os.makedirs(os.path.join(OUT,'meanings','hi'),exist_ok=True)
sys.path.insert(0,os.path.join(HERE,'..','..','..'))
import jsonio
jsonio.dump_meanings(os.path.join(OUT,'meanings','hi','gitapress.json'),M)
json.dump(dict(part_keys=part_keys,ends=ends),open(os.path.join(CWD,'ends.json'),'w'))
print(len(items),'items',len(topics),'topics',len(M['m']),'meanings')
