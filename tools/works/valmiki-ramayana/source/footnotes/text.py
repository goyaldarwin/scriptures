import pickle,json,re,sys,collections
sys.path.insert(0,'code')
from english import WORD
notes=pickle.load(open('fn/notes_mapped.pkl','rb'))
B=json.load(open('book.json'))
from english import convert
corpus=[]
for k in B:
    for s in k['sargas']:
        for e in s['en']: corpus.append(convert(e['text']).replace('­','|'))
for n in notes:
    for r in n['rows']: corpus.append(r['text'])
words=collections.Counter(w.lower() for t in corpus for w in re.findall(WORD+r"(?:-"+WORD+r")*",t))
hy=[]
def join(n):
    s=''
    for r in n['rows']:
        t=r['text']
        if not s: s=t; continue
        m=re.search(r"("+WORD+r")-$",s)
        if m and not s.endswith(' -'):
            b=re.match(WORD,t)
            a=m[1]; bw=b[0] if b else ''
            h=(a+'-'+bw).lower(); j=(a+bw).lower()
            keep = words[h]>=words[j] or words[j]==0
            hy.append((n['page'],a,bw,words[h],words[j],keep))
            s = (s+t) if keep else (s[:-1]+t)
        elif s.endswith('—') or s.endswith('-'):
            s=s+t
        else:
            s=s+' '+t
    s=re.sub(r'^\s*(?:[*†‡]\s*)+','',s)
    s=re.sub(r'^\s*\d{1,2}\.\s*','',s)
    return re.sub(r'  +',' ',s).strip()
out=[]
for n in notes:
    t=join(n)
    if False:
        parts=re.split(r'\s(?=[2-8]\.\s)',t)
        for i,pt in enumerate(parts):
            out.append(dict(n,mark=str(i+1),text=re.sub(r'^\d\.\s*','',pt)))
        continue
    if n['page']==1326 and n['mark']=='15': t=t.replace('—15. ','—')
    out.append(dict(n,text=t))
pickle.dump(out,open('fn/notes_text.pkl','wb'))
for h in hy: print('HY',*h)
