import json,re,glob,os
def segs(x):
    parts=re.split(r'(?<=[.;:?!])\s+(?=[\'‘“(A-ZŚṢĀĪŪṚḌṬṆÑ0-9—])|(?<=[;:])\s+',x)
    return [p for p in parts if p]
def apply(out, groups, d='split'):
    S={}
    for f in sorted(glob.glob(os.path.join(d,'out_*.json'))): S.update(json.load(open(f)))
    from collections import defaultdict
    m=defaultdict(list)
    for i,x in enumerate(out):
        if x.get('g') is not None: m[x['g']].append(i)
    nxt=max(int(k) for k in groups)+1; done=0; bad=[]
    # groups whose English the book prints together with the following verse: merge, then split by start phrases
    MAN={'bal.14.so14घ':['I bow to the lotus feet','I reverence, all the four Vedas','I greet the dust','Making obeisance'],
         'uttar.117.do117क':['After kindling','Having obtained this pure ghee','Extracting cotton','In this manner one should light']}
    for first,phr in MAN.items():
        i0=next(i for i,x in enumerate(out) if x['id']==first); ge=out[i0]['g']
        if groups[str(ge)]['x'].strip(): continue
        mem=[i for i in m[ge]]; gn=out[mem[-1]+1]['g']; mem+=m[gn]
        x=groups[str(gn)]['x']; cut=[x.index(ph) for ph in phr]+[len(x)]
        assert cut==sorted(cut) and cut[0]==0 and len(mem)==len(phr), first
        for n,i in enumerate(mem):
            ng=str(nxt); nxt+=1; e={'x':x[cut[n]:cut[n+1]].strip(),'l':groups[str(gn)].get('l'),'i':[i]}
            if n==len(mem)-1:
                f=(groups[str(ge)].get('f') or [])+(groups[str(gn)].get('f') or [])
                if f: e['f']=f
            groups[ng]=e; out[i]['g']=int(ng); out[i]['gl']=1
        del groups[str(ge)]; del groups[str(gn)]; m.pop(ge); m.pop(gn); done+=1
    for g,v in m.items():
        if len(v)<2 or str(g) not in S: continue
        st=S[str(g)]; sg=segs(groups[str(g)]['x'])
        # positions -> (seg, word)
        pos=[]
        for p in st:
            if isinstance(p,str) and ':' in p: a,b=p.split(':'); pos.append((int(a),int(b)))
            else: pos.append((int(p),0))
        words=[]  # flat list of (seg,word,text)
        for j,s in enumerate(sg):
            for w,t in enumerate(s.split(' ')): words.append((j,w,t))
        idx=[]
        ok=len(pos)==len(v) and pos[0]==(0,0)
        for p in pos:
            k=next((n for n,(a,b,_) in enumerate(words) if (a,b)==p),None)
            if k is None: ok=False;break
            idx.append(k)
        if not ok or any(idx[n]>=idx[n+1] for n in range(len(idx)-1)): bad.append(g); continue
        idx.append(len(words))
        parts=[]
        for n in range(len(v)):
            seg=words[idx[n]:idx[n+1]]; txt=''
            for q,(a,b,t) in enumerate(seg):
                if q and a!=seg[q-1][0]: txt+=' '
                elif q: txt+=' '
                txt+=t
            parts.append(txt.strip())
        for n in range(1,len(parts)):
            w0,_,rest=parts[n].partition(' ')
            mm=re.match(r'^(.+?[a-zāīū][.!?:;”’]+)([A-Z‘“].*)$',w0)
            if mm: parts[n-1]+=' '+mm.group(1); parts[n]=(mm.group(2)+' '+rest).strip()
        assert ' '.join(parts).replace(' ','')==groups[str(g)]['x'].replace(' ',''), g
        base=groups[str(g)]
        for n,i in enumerate(v):
            ng=str(nxt); nxt+=1
            e={'x':parts[n],'l':base.get('l'),'i':[i]}
            if n==len(v)-1 and base.get('f'): e['f']=base['f']
            groups[ng]=e; out[i]['g']=int(ng); out[i]['gl']=1
        del groups[str(g)]
        done+=1
    for v in groups.values(): v['x']=re.sub(r'([a-zāīūṇṁ][.!?])([A-Z‘“ŚṢĀĪŪṚ])',r'\1 \2',v['x'])
    relink_notes(out,groups)
    print('english split groups',done,'bad',bad)

M='*†‡§#¶'
def relink_notes(out,groups):
    # order groups by their first item
    first={}
    for i,x in enumerate(out):
        g=x.get('g')
        if g is not None and str(g) not in first: first[str(g)]=i
    order=sorted(first,key=lambda k:first[k])
    pos={k:n for n,k in enumerate(order)}
    # split each group's footnote lines into notes
    notes=[]  # (group pos, symbol, lines)
    for k in order:
        f=groups[k].get('f') or []; cur=None
        for l in f:
            c=l.strip()[:1]
            if c in M: cur=[l]; notes.append([pos[k],c,cur])
            elif cur is not None: cur.append(l)
            else: cur=[l]; notes.append([pos[k],None,cur])
    markers=[]  # [group pos, symbol, used]
    for k in order:
        for c in groups[k]['x']:
            if c in M: markers.append([pos[k],c,False])
    newf={k:[] for k in order}; moved=0
    for gp,c,lines in notes:
        tgt=gp
        if c:
            cand=[m for m in markers if not m[2] and m[1]==c and gp-25<=m[0]<=gp]
            if cand: m=cand[0]; m[2]=True; tgt=m[0]
        if tgt!=gp: moved+=1
        newf[order[tgt]].extend(lines)
    for k in order:
        if newf[k]: groups[k]['f']=newf[k]
        elif 'f' in groups[k]: del groups[k]['f']
    print('footnotes relinked',moved,'unmatched markers',sum(1 for m in markers if not m[2]))
