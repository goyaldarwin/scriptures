import fitz, pickle, unicodedata, sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hb
T=pickle.load(open('table.pkl','rb'))
MAXL=12
# fallbacks (cost 5): marks drawn without a base (the e-book's shaper inserts no dotted circle),
# and ई drawn as इ + the reph-shaped hook (glyph 181) by the e-book's shaper
FB={(g,):ch for g,ch in [(66,'ा'),(81,'्'),(5,'ँ'),(6,'ं'),(75,'े'),(79,'ो'),(69,'ु'),(70,'ू'),(76,'ै'),(80,'ौ')]}
FB[(11,181)]='ई'; FB[(11,181,6)]='ईं'; FB[(11,181,5)]='ईं'.replace('ं','ँ')
def pick(texts):
    return sorted(texts,key=lambda s:(('‍' in s) or ('‌' in s), len(s), s))[0]
class Unknown(Exception): pass
def decode_run(gids,bold):
    tab=T[bold]; n=len(gids)
    # DP: fewest pieces
    best=[None]*(n+1); best[0]=(0,None,None)
    for i in range(n):
        if best[i] is None: continue
        for L in range(1,min(MAXL,n-i)+1):
            t=tuple(gids[i:i+L])
            if t in tab or t in FB:
                c=best[i][0]+(1 if t in tab else 5)
                if best[i+L] is None or c<best[i+L][0]: best[i+L]=(c,i,t)
    if best[n] is None:
        # find first unreachable point
        far=max(i for i in range(n+1) if best[i] is not None)
        raise Unknown((far,gids[far:far+6]))
    parts=[]; j=n
    while j>0:
        c,i,t=best[j]; parts.append(pick(tab[t]) if t in tab else FB[t]); j=i
    return ''.join(reversed(parts))
def page_runs(page):
    """chars in content order -> list of lines; each line list of segs (noto,bold,size,text,ok,x0,y)"""
    chars=[]
    for s in page.get_texttrace():
        noto=s['font'].startswith('Noto'); bold='Bold' in s['font']
        for c in s['chars']: chars.append((noto,bold,round(s['size'],1),c))
    lines=[];line=None;lastx=lasty=None
    for ch in chars:
        c=ch[3]; x=c[2][0]; y=c[2][1]
        if line is None or x<lastx-20 or abs(y-lasty)>8:
            line=[]; lines.append(line); lastx=x
        lastx=max(lastx,x); lasty=y; line.append(ch)
    out=[]
    for L in lines:
        # tokens: split noto runs at glyph 3 spaces
        segs=[]; cur=None
        for k,(noto,bold,size,c) in enumerate(L):
            if noto and c[1]==3:
                # space: zero-advance if next char starts at this x
                nxt=L[k+1][3] if k+1<len(L) else None
                zero = nxt is not None and abs(nxt[2][0]-c[2][0])<0.3
                segs.append(dict(sp=True,zero=zero,bold=bold,size=size)); cur=None; continue
            key=(noto,bold,size)
            if cur is None or cur['key']!=key:
                cur=dict(key=key,ch=[]); segs.append(cur)
            cur['ch'].append(c)
        res=[]
        for sg in segs:
            if sg.get('sp'): res.append(dict(t='‌' if sg['zero'] else ' ',bold=sg['bold'],size=sg['size'],ok=True,sp=True)); continue
            noto,bold,size=sg['key']; cs=sg['ch']
            if noto:
                g=[c[1] for c in cs]
                try:
                    t=decode_run(g,bold); ok=True
                    if tuple(hb.shape(t,bold))!=tuple(g): ok=('rt',t,g)
                except Unknown as e: t='�'; ok=('unk',e.args[0],g)
            else:
                t=''.join(chr(c[0]) for c in cs); ok=True
            res.append(dict(t=t,bold=bold,size=size,ok=ok,x0=round(cs[0][3][0],1),y=round(cs[0][2][1],1)))
        out.append(res)
    return out
if __name__=='__main__':
    fn,a,b=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
    d=fitz.open(fn)
    for i in range(a,b):
        for L in page_runs(d[i]):
            print(''.join(s['t'] if s['ok'] is True else '[?%s]'%(s['ok'][2],) for s in L).replace('‌','|'))
