import os,pickle,pymupdf,sys,json,unicodedata,re
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'.')
from hi_decode import R,B,decode
pages=pickle.load(open('hi_trace.pkl','rb'))
d=pymupdf.open(os.environ.get('HINDI_PDF','Hindi.pdf'))
m=json.load(open('merged.json')); IT={x['id']:x for x in m['items']}
def find(item_id,word):
    it=IT[item_id]
    for pi in (it['p']-1,it['p']):
        for f,size,ch in pages[pi]:
            if not ch: continue
            w=decode([(u,g) for u,g,b in ch],B if 'Bold' in f else R)
            if unicodedata.normalize('NFC',w)==unicodedata.normalize('NFC',word) and size>16:
                x0=min(c[2][0] for c in ch);x1=max(c[2][2] for c in ch);y0=min(c[2][1] for c in ch);y1=max(c[2][3] for c in ch)
                return pi,(x0-60,y0-5,x1+60,y1+5)
    return None
def sheet(pairs,out):
    fnt=ImageFont.truetype(os.environ.get('DEV_FONT','NotoSansDevanagari-Regular.ttf'),24)
    rows=[]
    for iid,w,alt in pairs:
        r=find(iid,w)
        if not r: rows.append((iid,w,alt,None)); continue
        pix=d[r[0]].get_pixmap(clip=pymupdf.Rect(*r[1]),dpi=200)
        rows.append((iid,w,alt,Image.frombytes('RGB',(pix.width,pix.height),pix.samples)))
    H=sum((im.height if im else 30)+40 for *_,im in rows)
    sh=Image.new('RGB',(900,H),'white'); dr=ImageDraw.Draw(sh); y=0
    for iid,w,alt,im in rows:
        dr.text((5,y+2),f'{iid}: decoded={w}  english-book={alt}',fill='blue',font=fnt); y+=36
        if im: sh.paste(im,(10,y)); y+=im.height+4
        else: dr.text((10,y),'NOT FOUND',fill='red',font=fnt); y+=30
    sh.save(out)
pairs=[tuple(x) for x in json.loads(sys.argv[1])]
sheet(pairs,sys.argv[2])
