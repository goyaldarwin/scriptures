import json
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import io
unm=json.load(open('hi_unmapped.json'))['unm']
fonts={'NotoSansDevanagari':TTFont('font_19.ttf'),'NotoSansDevanagari-Bold':TTFont('font_16.ttf')}
def path_of(f,gid):
    gs=f.getGlyphSet(); n=f.getGlyphOrder()[gid]
    pen=DecomposingRecordingPen(gs); gs[n].draw(pen)
    verts=[];codes=[]
    for op,args in pen.value:
        if op=='moveTo': verts.append(args[0]);codes.append(Path.MOVETO); start=args[0]
        elif op=='lineTo': verts.append(args[0]);codes.append(Path.LINETO)
        elif op=='qCurveTo':
            pts=list(args)
            if pts[-1] is None: pts=pts[:-1]
            for i in range(len(pts)-1):
                c=pts[i]; nxt=pts[i+1] if i==len(pts)-2 else ((pts[i][0]+pts[i+1][0])/2,(pts[i][1]+pts[i+1][1])/2)
                verts+=[c,nxt]; codes+=[Path.CURVE3,Path.CURVE3]
        elif op=='curveTo': verts+=list(args); codes+=[Path.CURVE4]*3
        elif op=='closePath': verts.append(start); codes.append(Path.CLOSEPOLY)
    return verts,codes
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
cells=[]
for fn,g,n in unm:
    f=fonts[fn]; v,c=path_of(f,g)
    fig=plt.figure(figsize=(1.6,1.6),dpi=70); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(-1000,1800); ax.set_ylim(-700,2100); ax.axis('off')
    ax.axvline(0,color='#f99',lw=0.6); ax.axvline(f['hmtx'][f.getGlyphOrder()[g]][0],color='#9f9',lw=0.6); ax.axhline(0,color='#ccc',lw=0.5)
    if v: ax.add_patch(PathPatch(Path(v,c),fc='black',ec='none'))
    b=io.BytesIO(); fig.savefig(b,format='png'); plt.close(fig); b.seek(0)
    im=Image.open(b).convert('RGB'); d=ImageDraw.Draw(im); d.text((2,2),f"{'B' if 'Bold' in fn else 'R'}{g}",fill='blue',font=fnt)
    cells.append(im)
W=112; cols=10
for s in range(0,len(cells),70):
    chunk=cells[s:s+70]; rows=(len(chunk)+cols-1)//cols
    sh=Image.new('RGB',(cols*W,rows*W),'white')
    for i,im in enumerate(chunk): sh.paste(im,((i%cols)*W,(i//cols)*W))
    sh.save(f'sheets/glyphs_{s//70}.png')
print(len(cells))
