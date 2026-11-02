import fitz,sys,warnings
warnings.filterwarnings('ignore')
d=fitz.open('/home/claude/scriptures-data/hinduism/granth/valmiki/ramayana/books/gitapress/sanskrit-english.pdf')
p=int(sys.argv[1]); y0=float(sys.argv[2]); y1=float(sys.argv[3]) if len(sys.argv)>3 else 672
d[p-1].get_pixmap(dpi=200,clip=fitz.Rect(0,y0,444,y1)).save(f'fn/img/f{p}.png')
