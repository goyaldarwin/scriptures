"""pages pkl -> flat list of line records: page, x0, y, size (main), bold, text (ZWNJ joins removed)"""
import pickle,sys,json,re
def lines(fn,book):
    P=pickle.load(open(fn,'rb')); out=[]
    for pi,pg in enumerate(P):
        for l in pg:
            segs=[s for s in l if not s.get('sp')]
            if not segs: continue
            t=''.join(s['t'] for s in l).replace('‌','')
            if 'ebook converter' in t: continue
            sizes=[s['size'] for s in segs if s['t'].strip()]
            big=max(sizes) if sizes else 15.0
            sup=[i for i,s in enumerate(l) if not s.get('sp') and s['size']==11.2]
            # superscript footnote marks inside a 15pt line: drop them, remember
            marks=''
            if big==15.0 and sup:
                marks=''.join(l[i]['t'] for i in sup)
                t=''.join(s['t'] for i,s in enumerate(l) if i not in sup).replace('‌','')
            out.append(dict(b=book,pg=pi+1,x=segs[0].get('x0'),y=segs[0].get('y'),size=big,bold=all(s['bold'] for s in segs if s['t'].strip()),t=t,marks=marks,ok=all(s['ok'] is True for s in l)))
    return out
if __name__=='__main__':
    L=lines('p1.pkl',1)+lines('p2.pkl',2)
    json.dump(L,open('lines.json','w'),ensure_ascii=False)
    print(len(L), sum(1 for x in L if not x['ok']))
