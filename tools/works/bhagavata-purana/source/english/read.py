"""The owner's wisdomlib copy (scriptures-data: printouts/wisdomlib/bhagavata-purana.json) read into chapters:
each with the Gita Press verses (number, Sanskrit, Hindi) and Tagare's English as groups of his verse numbers.
The copy puts each English entry beside the Gita Press verse of the same number; the entries are taken back out
and renumbered from the text itself:
- an entry may hold later verses, each printed with its number on a new line ("24-25(A). …", "20(A). …"); they
  are split there, and verse numbers that share a part ("24-25(A)", "25(B)-27") form one group;
- an entry may start with its own number ("12. …"), which then wins over the copy's; a later one (the page's
  "40. 41. …": the copy's 40 holds Tagare's 41) joins the verses up to it into one passage;
- what follows a bracketed line such as "[ Padaratnāvalī’s Text adds:]" is another recension's verse: left out;
- where Tagare's numbers step back (10.30: 31 holds 32(A) and 33(B), then comes 32), the rest are counted on."""
import json,re
TYPO={'831':'83','111-12':'11-12'}     # misprinted numbers inside two entries (m.6.83, 10.60.11-12)
MK=re.compile(r'\n\s*(\d+)(?:\s*\(([A-Za-z])\))?(?:\s*[-–]\s*(\d+)(?:\s*\(([A-Za-z])\))?)?\.\s')

def segments(nums,text):
    for a,b in TYPO.items(): text=text.replace('\n'+a+'.','\n'+b+'.')
    out=[]; pos=0; lo,hi=min(nums),max(nums)
    m0=re.match(r'(\d+)(?:\s*\([A-Za-z]\))?(?:\s*[-–]\s*(\d+))?\.\s',text)
    if m0 and abs(int(m0.group(1))-lo)<=3:
        a=int(m0.group(1)); b=int(m0.group(2)) if m0.group(2) else a; pos=m0.end()
        # a later number at the start of the copy's entry ("40. 41. …" on the page): that verse and the ones up
        # to it are one passage; an earlier number wins over the copy's
        lo,hi=(lo,b) if a>lo else (a,b)
    for m in MK.finditer(text):
        out.append([lo,hi,text[pos:m.start()]]); pos=m.end()
        lo=int(m.group(1)); hi=int(m.group(3)) if m.group(3) else lo
    out.append([lo,hi,text[pos:]])
    res=[]
    for lo,hi,s in out:
        parts=re.split(r'\n\s*\[[^\]\n]*\]\s*(?=\n|$)',s)
        s=re.sub(r'\s+',' ',parts[0].replace('{GL_NOTE::}','')).strip()
        if s: res.append((lo,hi,s))
        if len(parts)>1: break
    return res

def groups(entries):
    segs=[]; add=0
    for e in entries:
        for k,(lo,hi,s) in enumerate(segments(e['nums'],e['text'])):
            lo+=add; hi+=add
            if segs and lo<segs[-1][1]:
                d=segs[-1][1]-lo; add+=d; lo+=d; hi+=d
            segs.append((lo,hi,s,e['fn'] if k==0 else []))
    G=[]
    for lo,hi,s,fn in segs:
        if G and lo<=G[-1]['hi'] and hi>=G[-1]['lo']:
            g=G[-1]; g['lo']=min(g['lo'],lo); g['hi']=max(g['hi'],hi); g['text']+=' '+s; g['fn']+=fn
        else: G.append(dict(lo=lo,hi=hi,text=s,fn=list(fn)))
    return G

def chapters(path):
    d=json.load(open(path,encoding='utf-8'))
    out=[]
    for s in d['sections']:
        for c in s['chapters']:
            sec=('m' if s['id']=='mahatmya' else s['id'].split('-')[1])+'.'+str(c['number'])
            gp=[]; ent={}
            for v in c['verses']:
                gp.append(dict(n=v['number'],sanskrit=v['sanskrit'],hindi=v.get('hindi') or {}))
                e=v.get('english') or {}
                if e.get('verses') and e.get('text'):
                    ent.setdefault(tuple(e['verses']),dict(nums=list(e['verses']),text=e['text'],fn=list(e.get('footnotes',[]))))
            entries=sorted(ent.values(),key=lambda x:x['nums'])
            out.append(dict(sec=sec,gp=gp,wl=groups(entries),fnotes=c['footnotes']['en'],counts=c['verse_counts']))
    return out
