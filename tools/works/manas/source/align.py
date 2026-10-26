import json,re,unicodedata,difflib,collections
from tr2dev import tr2dev
hu=json.load(open('hi_units_raw.json')); eu=json.load(open('en_units.json'))
KANDS=['bal','ayodhya','aranya','kishkindha','sundar','lanka','uttar']
def norm_loose(w):
    w=unicodedata.normalize('NFC',w)
    w=w.replace('ँ','ं').replace('‌','').replace('‍','')
    w=re.sub(r'[ङञणनम]्(?=[क-ह])','ं',w)
    return w
def words_dev(s):
    s=re.sub(r'^(दो|सो|छं|चौ)०\s*[—-]\s*','',s)
    s=re.sub(r'[।॥|,.;:!?\-—‘’“”\'"()\[\]0-9०-९]',' ',s)
    s=s.replace('ऽ','')
    return [w for w in s.split() if w]
def key(w):
    w=norm_loose(w)
    w=w.replace('ौ','उ').replace('ै','इ').replace('औ','अउ').replace('ऐ','अइ')
    w=w.replace('ू','ु').replace('ऊ','उ').replace('ी','ि').replace('ई','इ')
    w=w.replace('ं','').replace('़','')
    return w
res={}
def run():
    for k in KANDS:
        H=[]  # (word, unit index)
        for i,u in enumerate(hu):
            if u['kand']==k and u['kind']=='verse':
                for li,line in enumerate(u['v']):
                    for w in words_dev(line): H.append((w,i,li))
        E=[]
        for i,u in enumerate(eu):
            if u.get('kand')==k and u.get('tr'):
                for li,line in enumerate(u['tr']):
                    d=tr2dev(line)
                    for w in words_dev(d): E.append((w,i,li))
        a=[key(w) for w,*_ in H]; b=[key(w) for w,*_ in E]
        sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
        eq=sum(bl.size for bl in sm.get_matching_blocks())
        res[k]=(len(a),len(b),eq)
        print(k,len(a),len(b),eq,round(eq/max(len(a),1)*100,2))
        json.dump({'H':H,'E':E,'ops':sm.get_opcodes()},open(f'align_{k}.json','w'),ensure_ascii=False)


if __name__=="__main__": run()
