import json,re,difflib,unicodedata,os,collections
m=json.load(open('merged.json')); items=m['items']
vt=json.load(open('verify_tr.json'))
def nrm(w):
    w=unicodedata.normalize('NFC',w).replace('‌','').replace('‍','')
    return re.sub(r'[^ऀ-ॣ०-ॿ]','',w)
def toks(s): return [x for x in (nrm(w) for w in re.split(r'[\s।॥|,;:!?—\-()\[\]‘’“”]+',s)) if x and not re.fullmatch(r'[०-९]+',x)]
OC={}
def ocr(p):
    if p not in OC:
        f=f'ocr1/p{p:04d}.txt'; OC[p]=toks(open(f).read()) if os.path.exists(f) else None
    return OC[p]
res={}; agg=collections.Counter()
for it in items:
    p=it['p']; w=[]
    for q in (p,p+1):
        o=ocr(q)
        if o is None: w=None; break
        w+=o
    if w is None: continue
    vw=toks(' '.join(it['v'])); hw=toks(it['hi'])
    def match(a):
        sm=difflib.SequenceMatcher(None,a,w,autojunk=False); ok=[False]*len(a)
        for b in sm.get_matching_blocks():
            for k in range(b.size): ok[b.a+k]=True
        return ok
    vok=match(vw); hok=match(hw)
    trbad=set()
    for a,b in vt.get(it['id'],[]):
        for x in a.split(): trbad.add(nrm(x))
    flagged=[x for x,o in zip(vw,vok) if not o and x in trbad]
    res[it['id']]={'v':[sum(vok),len(vw)],'h':[sum(hok),len(hw)],'flag':flagged}
    agg['vw']+=len(vw); agg['vok']+=sum(vok); agg['hw']+=len(hw); agg['hok']+=sum(hok)
    agg['items']+=1; agg['tr_clean']+= not vt.get(it['id'])
    if flagged: agg['flag_items']+=1; agg['flag_words']+=len(flagged)
json.dump(res,open('verify_ocr.json','w'),ensure_ascii=False)
print(dict(agg)); print('verse-ocr %',round(agg['vok']/agg['vw']*100,2),'meaning-ocr %',round(agg['hok']/agg['hw']*100,2))
fl=[(k,v['flag']) for k,v in res.items() if v['flag']]
for k,f in fl[:40]: print(k,f, vt.get(k))
