import pickle,json,re,difflib,collections,unicodedata,glob,sys
sys.path.insert(0,'.')
from hi_decode import R,B,decode
pages=pickle.load(open('hi_trace.pkl','rb'))
def nrm(s): 
    s=unicodedata.normalize('NFC',s).replace('‌','').replace('‍','')
    return re.sub(r'[^ऀ-ॣ०-ॿ]','',s)
stats=collections.defaultdict(lambda:[0,0]); base=[0,0]; bad=collections.defaultdict(list)
for f in sorted(glob.glob('ocr1/p*.txt')):
    pi=int(f[-8:-4])-1
    if pi<31: continue
    words=[]
    for fn,size,ch in pages[pi]:
        if not ch: continue
        tab=B if 'Bold' in fn else R
        # split span on spaces
        cur=[]
        for u,g,b in ch+[(32,0,None)]:
            if u==32:
                if cur:
                    w=nrm(decode([(x,y) for x,y in cur],tab)); gs={(('B' if 'Bold' in fn else 'R'),y) for x,y in cur if x==65533}
                    y1=max(c[2][3] for c in [(0,0,bb) for _,_,bb in []]) if False else None
                    if w: words.append((w,gs,cur))
                cur=[]
            else: cur.append((u,g))
    # order: texttrace order is reading order presumably
    ocr=[nrm(w) for w in re.split(r'\s+',open(f).read())]; ocr=[w for w in ocr if w]
    a=[w for w,_,_ in words]
    sm=difflib.SequenceMatcher(None,a,ocr,autojunk=False)
    ok=[False]*len(a)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): ok[blk.a+k]=True
    for (w,gs,_),o in zip(words,ok):
        if not gs: base[0]+=o; base[1]+=1
        for g in gs:
            stats[g][0]+=o; stats[g][1]+=1
            if not o and len(bad[g])<6: bad[g].append(w)
print('baseline agreement',round(base[0]/base[1]*100,1),base[1])
rows=[]
for g,(o,n) in stats.items(): rows.append((o/n,n,g))
rows.sort()
for r,n,g in rows[:40]: print(g,n,round(r*100,1),bad[g])
json.dump({str(g):[o,n] for g,(o,n) in stats.items()},open('glyph_stats.json','w'))
