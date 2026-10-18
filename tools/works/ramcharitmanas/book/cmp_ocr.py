import json,re,difflib,collections,glob,os,sys
txt=json.load(open('hi_text.json'))
import unicodedata
def norm(s):
    s=unicodedata.normalize('NFC',s)
    s=s.replace('‌','').replace('‍','')
    s=re.sub(r'[।|॥]+','।',s)
    s=re.sub(r'[^ऀ-ॿ ]',' ',s)
    s=s.replace('।',' ')
    return s.split()
pairs=collections.Counter(); tot=0; same=0; ex={}
for f in sorted(glob.glob('ocr1/p*.txt')):
    pi=int(f[-8:-4])-1
    a=norm(' '.join(l['t'] for l in txt[pi])); b=norm(open(f).read())
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': same+=i2-i1
        elif op=='replace' and i2-i1==j2-j1:
            for x,y in zip(a[i1:i2],b[j1:j2]): pairs[(x,y)]+=1; ex.setdefault((x,y),pi+1)
        tot+=0
    tot+=len(a)
print('words decoded',tot,'equal',same, round(same/tot*100,2))
for (x,y),n in pairs.most_common(int(sys.argv[1]) if len(sys.argv)>1 else 60): print(n,x,'|',y,ex[(x,y)])
