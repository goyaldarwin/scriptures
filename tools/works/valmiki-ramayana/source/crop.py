"""Crop the printed lines of a verse from the Gita Press PDF (for checking a reading by eye)."""
import fitz, json, sys, pickle
sys.path.insert(0, __file__.rsplit('/', 1)[0]); import layout
PDF = '/home/claude/scriptures-data/hinduism/granth/valmiki/ramayana/books/gitapress/sanskrit-english.pdf'
_d = fitz.open(PDF)
_lines = None
def verse_lines(page, texts):
    """bounding boxes of the page's Sanskrit lines whose decoded text is one of `texts`"""
    global _lines
    if _lines is None:
        _lines = {}
        for l in json.load(open(__file__.rsplit('/', 2)[0] + '/se_lines.json')):
            _lines.setdefault(l['page'], []).append(l)
    out = []
    pg = _d[page - 1]; W = pg.rect.width
    for l in _lines[page]:
        if l['kind'] == 'sa' and l['text'] in texts:
            x0, x1 = (0, W / 2 + 4) if l['col'] == 0 else (W / 2 - 4, W) if l['col'] == 1 else (0, W)
            out.append(fitz.Rect(x0, l['y'] - 15, x1, l['y'] + 5))
    return out
def crop(page, rects, path, dpi=170):
    from PIL import Image
    ims = []
    for r in rects:
        pm = _d[page - 1].get_pixmap(dpi=dpi, clip=r)
        ims.append(Image.frombytes('RGB', (pm.width, pm.height), pm.samples))
    if not ims: return False
    W = max(i.width for i in ims); H = sum(i.height for i in ims)
    o = Image.new('RGB', (W, H), 'white'); y = 0
    for i in ims: o.paste(i, (0, y)); y += i.height
    o.save(path); return True
