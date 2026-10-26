import os,pymupdf,pickle,json,collections
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import io
pages=pickle.load(open('hi_trace.pkl','rb'))
unm=json.load(open('hi_unmapped.json'))['unm']
fontfile={'NotoSansDevanagari':'font_19.ttf'}
# bold font extract
d=pymupdf.open(os.environ.get('HINDI_PDF','Hindi.pdf'))
name,ext,typ,buf=d.extract_font(16); open('font_16.ttf','wb').write(buf); fontfile['NotoSansDevanagari-Bold']='font_16.ttf'
fonts={k:TTFont(v) for k,v in fontfile.items()}
def glyph_img(fname,gid):
    f=fonts[fname]; gs=f.getGlyphSet(); go=f.getGlyphOrder(); n=go[gid]
    pen=DecomposingRecordingPen(gs); gs[n].draw(pen)
    verts=[];codes=[]
    for op,args in pen.value:
        if op=='moveTo': verts.append(args[0]);codes.append(Path.MOVETO)
        elif op=='lineTo': verts.append(args[0]);codes.append(Path.LINETO)
        elif op=='qCurveTo':
            pts=list(args); 
            # convert implied on-curve
            cur=verts[-1] if verts else (0,0)
            for i in range(len(pts)-1):
                c=pts[i]; nxt=pts[i+1] if i==len(pts)-2 else ((pts[i][0]+pts[i+1][0])/2,(pts[i][1]+pts[i+1][1])/2)
                verts+= [c,nxt]; codes+=[Path.CURVE3,Path.CURVE3]
        elif op=='curveTo':
            verts+=list(args); codes+=[Path.CURVE4]*3
        elif op=='closePath': verts.append((0,0)); codes.append(Path.CLOSEPOLY)
    fig=plt.figure(figsize=(1.2,1.2),dpi=80); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(-300,1200); ax.set_ylim(-500,1100); ax.axis('off')
    if verts: ax.add_patch(PathPatch(Path(verts,codes),fc='black',ec='none'))
    ax.axhline(0,color='#ccc',lw=0.5)
    b=io.BytesIO(); fig.savefig(b,format='png'); plt.close(fig); b.seek(0); return Image.open(b).convert('RGB')
# find contexts: page, bbox of the glyph -> expand to word
ctx=collections.defaultdict(list)
for pi,spans in enumerate(pages):
    for f,size,ch in spans:
        for i,(u,g,b) in enumerate(ch):
            if u==65533 and len(ctx[(f,g)])<2:
                # word extent
                j=i
                while j>0 and ch[j-1][0]!=32: j-=1
                k=i
                while k<len(ch)-1 and ch[k+1][0]!=32: k+=1
                x0=min(c[2][0] for c in ch[j:k+1]); x1=max(c[2][2] for c in ch[j:k+1])
                y0=min(c[2][1] for c in ch[j:k+1]); y1=max(c[2][3] for c in ch[j:k+1])
                ctx[(f,g)].append((pi,(x0-2,y0-4,x1+2,y1+4),b))
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16) if __import__('os').path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else ImageFont.load_default()
items=[(f,g,n) for f,g,n in unm]
per=24
for si in range(0,len(items),per):
    sheet=Image.new('RGB',(1100,per//2*110),'white'); dr=ImageDraw.Draw(sheet)
    for k,(f,g,n) in enumerate(items[si:si+per]):
        col=k%2; row=k//2; X=col*550; Y=row*110
        dr.text((X+5,Y+5),f"{'B' if 'Bold' in f else 'R'}{g} n={n}",fill='red',font=fnt)
        sheet.paste(glyph_img(f,g).resize((90,90)),(X+5,Y+20))
        xx=X+105
        for (pi,r,b) in ctx[(f,g)]:
            pix=d[pi].get_pixmap(clip=pymupdf.Rect(*r),dpi=200)
            im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
            # mark glyph position
            dd=ImageDraw.Draw(im); sc=200/72
            dd.line([((b[0]-r[0])*sc,im.height-3),((b[2]-r[0])*sc,im.height-3)],fill='red',width=3)
            if im.width>210: im=im.resize((210,int(im.height*210/im.width)))
            sheet.paste(im,(xx,Y+20)); xx+=220
    sheet.save(f'sheets/sheet_{si//per:02d}.png')
print('sheets',(len(items)+per-1)//per)
