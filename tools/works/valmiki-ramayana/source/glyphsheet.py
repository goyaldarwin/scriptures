# Render every glyph of the embedded Chanakya font by its code, with the MacRoman char the PDF text layer shows.
import io,sys
from fontTools.cffLib import CFFFontSet
from fontTools.pens.basePen import BasePen
from PIL import Image,ImageDraw,ImageChops,ImageFont
class Flat(BasePen):
    def __init__(s,gs):super().__init__(gs);s.contours=[];s.cur=[]
    def _moveTo(s,p):s.cur=[p]
    def _lineTo(s,p):s.cur.append(p)
    def _curveToOne(s,a,b,c):
        p0=s.cur[-1]
        for i in range(1,13):
            t=i/12;u=1-t
            s.cur.append((u**3*p0[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t**3*c[0],u**3*p0[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t**3*c[1]))
    def _closePath(s):
        if s.cur:s.contours.append(s.cur);s.cur=[]
    _endPath=_closePath
def render(cs,name,size=90):
    g=cs[name];p=Flat(cs);g.draw(p)
    W,H=150,130;img=Image.new('1',(W,H),0)
    for c in p.contours:
        m=Image.new('1',(W,H),0)
        pts=[(40+x*size/1000,95-y*size/1000) for x,y in c]
        if len(pts)>2:ImageDraw.Draw(m).polygon(pts,fill=1)
        img=ImageChops.logical_xor(img,m)
    return img
f=sys.argv[1];out=sys.argv[2]
c=CFFFontSet();c.decompile(io.BytesIO(open(f,'rb').read()),None);t=c[c.fontNames[0]];cs=t.CharStrings
codes=[(i,n) for i,n in enumerate(t.Encoding) if n not in('.notdef','space')]
lab=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
cols=10;W,H=160,165
sheet=Image.new('RGB',(cols*W,((len(codes)+cols-1)//cols)*H),'white');dr=ImageDraw.Draw(sheet)
for k,(i,n) in enumerate(codes):
    x,y=(k%cols)*W,(k//cols)*H
    g=render(cs,n).convert('L');g=Image.eval(g,lambda v:255-v)
    sheet.paste(g.convert('RGB'),(x+5,y+28))
    ch=bytes([i]).decode('mac_roman')
    dr.text((x+4,y+4),f"{i} '{ch}'",fill='blue',font=lab)
    dr.line([(x+45,y+28+95),(x+150,y+28+95)],fill=(255,180,180))
    dr.rectangle([x,y,x+W-1,y+H-1],outline='#bbb')
sheet.save(out);print(len(codes),'glyphs')
