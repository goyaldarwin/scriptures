"""The book's notes (टिप्पणी): each adhyāya's notes, printed after its closing words, matched to the note marks
(* † ‡) in its verses and its Hindi, taken in page order. The book sometimes prints the last note of an adhyāya with
the next adhyāya's notes, so the matching runs over a whole skandha: marks and notes are aligned in order, a pair
needing the same symbol and the note printed in the mark's adhyāya or the next one.
-> book2.json gets a['fnotes']: [(target, 'v'|'h', mark, text)]; notes_unpaired.json lists every mark or note left over."""
import json,re
book=json.load(open('book2.json'))
VAR=re.compile(r'^(?:[०-९]+[.\-]\s*)?(?:प्रा०|पा०)|^—')
VAR2=re.compile(r'^(?:[०-९]+\.\s*[^।॥]{1,25}[।॥]\s*)+$')   # vol. 2 prints its variants as bare "१. ऽम्बुपूरिताः। २. …"
NUM1=re.compile(r'^(?:\S+ — )?१[.\-—]')
def clean(t): return re.sub(r'\s+',' ',t).strip()

def blocks_of(a):
    """The adhyāya's notes as [(symbol, text)], variant readings (प्रा० पा०) left out."""
    blocks=[]; cur=None; head=''
    for t,x,marks,bold,tm in a['notes']:
        body=tm.lstrip()
        if VAR.match(re.sub(r'^[*†‡\s]+','',body)) or (body[:1] not in '*†‡' and VAR2.match(clean(body))) or (marks and body[:1] not in '*†‡' and not re.search(r'[।]\s*[*†‡]\s',body)):
            m=re.search(r'।\s*([*†‡])\s+(.*)$',body)       # a note can start after the variants on the same line
            if m: cur=dict(kind='note',mark=m.group(1),lines=[m.group(2)]); blocks.append(cur)
            else: cur=dict(kind='var',lines=[t]); blocks.append(cur)
            continue
        sym=body[:1] if body[:1] in '*†‡' else ''
        rest=re.sub(r'^[*†‡\s]+','',body)
        if sym and cur is not None and cur['kind']=='note' and re.match(r'^[२-९][.\-—]',rest) and NUM1.match(cur['lines'][0]):
            cur['lines'].append(rest); continue                  # a stray mark on the 2nd, 3rd … point of one note
        if sym:
            cur=dict(kind='note',mark=sym,lines=[(head+' — ' if head else '')+rest]); blocks.append(cur); head=''; continue
        if x>180 and len(t)<30 and not re.search(r'[।॥]',t):
            head=t; continue                                     # a heading over the next note
        if cur is not None: cur['lines'].append(tm)
    notes=[]
    for b in blocks:
        if b['kind']!='note': continue
        txt=''
        for l in b['lines']:
            txt=txt+l if txt.endswith(('-','—')) else (txt+' '+l if txt else l)
        parts=re.split(r'(?<=[।!?])\s*([†‡])\s+',clean(txt))  # "* पौराणिक। † वंशका … ‡ …": several notes on a line
        notes.append((b['mark'],parts[0]))
        for i in range(1,len(parts),2): notes.append((parts[i],parts[i+1]))
    return notes

bad=[]; n_ok=0
for sk in book:
    sp='m' if sk['n']==0 else str(sk['n'])
    M=[]; N=[]
    for ai,a in enumerate(sk['adh']):
        sec=f"{sp}.{a['n']}"; a['fnotes']=[]
        ms=[]
        for v in a['verses']:
            for k,y,ch in v.get('nm',[]): ms.append((tuple(k),y,ch,'v',f"{sec}.{v['n']}"))
        for c in a['mchunks']:
            for k,y,ch in c.get('nm',[]): ms.append((tuple(k),y,ch,'h',f"{sec}.{c['b']}"))
        ms.sort()
        M+=[(ai,)+m for m in ms]
        N+=[(ai,s,t) for s,t in blocks_of(a)]
    # longest alignment in order: same symbol, note in the mark's adhyāya (3) or the next (2)
    I,J=len(M),len(N)
    S=[[0]*(J+1) for _ in range(I+1)]
    def w(i,j):
        m,n=M[i],N[j]
        if m[3]!=n[1]: return None
        return 3 if n[0]==m[0] else 2 if n[0]==m[0]+1 else None
    for i in range(I-1,-1,-1):
        for j in range(J-1,-1,-1):
            best=max(S[i+1][j],S[i][j+1]); s=w(i,j)
            if s is not None: best=max(best,s+S[i+1][j+1])
            S[i][j]=best
    i=j=0; used_m=set(); used_n=set()
    while i<I and j<J:
        s=w(i,j)
        if s is not None and S[i][j]==s+S[i+1][j+1]:
            ai,k,y,ch,kind,tid=M[i]; sk['adh'][ai]['fnotes'].append((tid,kind,ch,N[j][2])); used_m.add(i); used_n.add(j); n_ok+=1; i+=1; j+=1
        elif S[i][j]==S[i+1][j]: i+=1
        else: j+=1
    for i,m in enumerate(M):
        if i not in used_m: bad.append(dict(kind='mark',at=m[5],mark=m[3]))
    for j,n in enumerate(N):
        if j not in used_n: bad.append(dict(kind='note',sec=f"{sp}.{sk['adh'][n[0]]['n']}",mark=n[1],text=n[2][:80]))
json.dump(book,open('book2.json','w'),ensure_ascii=False)
json.dump(bad,open('notes_unpaired.json','w'),ensure_ascii=False,indent=1)
print('notes paired',n_ok,'; left over',len(bad))
for b in bad: print(b)
