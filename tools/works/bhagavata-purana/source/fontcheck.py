import fitz, sys, io
from fontTools.ttLib import TTFont
pdf=fitz.open(sys.argv[1])
seen={}
for pno in range(0,len(pdf),97):
    for f in pdf.get_page_fonts(pno):
        xref,ext,typ,name=f[0],f[1],f[2],f[3]
        if name in seen: continue
        seen[name]=xref
for name,xref in seen.items():
    if 'Noto' not in name: print(name);continue
    n,ext,typ,buf=pdf.extract_font(xref)
    emb=TTFont(io.BytesIO(buf)); ref=TTFont('Ref-Bold.ttf' if 'Bold' in name else 'Ref-Regular.ttf')
    eg=emb.getGlyphOrder(); rg=ref.getGlyphOrder()
    eglyf=emb['glyf']; rglyf=ref['glyf']; same=diff=empty=0
    for i,gn in enumerate(eg):
        g=eglyf[gn]
        if g.numberOfContours==0: empty+=1; continue
        if i>=len(rg): diff+=1; continue
        r=rglyf[rg[i]]
        a=g.getCoordinates(eglyf)[0] if g.numberOfContours else None
        b=r.getCoordinates(rglyf)[0]
        if list(a)==list(b) and emb['hmtx'][gn][0]==ref['hmtx'][rg[i]][0]: same+=1
        else: diff+=1
    print(name,xref,len(eg),len(rg),'same',same,'diff',diff,'empty',empty)
