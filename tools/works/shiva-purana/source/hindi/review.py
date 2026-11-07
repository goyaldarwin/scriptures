"""Read the flagged words by eye: each flag's printed line cut from the page image, a dozen lines to a sheet, with the
OCR reading beside it (hindi/README.md). The page images are made here from the owner's PDF; nothing of them is kept.

    python3 review.py prepare <book> <scan.pdf> <out folder> [--per 12] [--sheets 20]
        → <out>/sheet-NNNN.png (the lines, numbered) and <out>/sheet-NNNN.json ([{n, flags: [{k, id, word, why, alt}], ocr}])
          and <out>/batch-NN.txt (the sheets of one reader's batch)
    python3 review.py apply <book> <out folder>
        → reads <out>/sheet-NNNN.out.json ({"n": {"k": "word as printed", …, "line": "the line as printed"}}) into
          hindi/<book>.read.json: {id: {k: word}}, used by make_hindi.py

A distinct word both passes read alike that the word list lacks (why "unknown") is shown once, at its first place; what
the reader finds there holds for the word everywhere (confirmed.txt, or a correction for every place it occurs).
"""
import json, os, re, subprocess, sys, tempfile, collections
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ocr as O

def line_boxes(col):
    """The boxes of the Devanagari pass's lines in a column crop, in the order ocr.py wrote its lines."""
    rows = [r.split('\t') for r in O.tess(col, 'Devanagari', 6, tsv=True).splitlines()[1:]]
    L = {}
    for r in rows:
        if len(r) < 12 or r[0] != '5' or not r[11].strip(): continue
        x, y, w, h = map(int, r[6:10]); key = (int(r[2]), int(r[3]), int(r[4]))
        a = L.setdefault(key, [x, y, x + w, y + h])
        a[0], a[1], a[2], a[3] = min(a[0], x), min(a[1], y), max(a[2], x + w), max(a[3], y + h)
    return [L[k] for k in sorted(L)]

def prepare(book, pdf, out, per=12, sheets=20):
    os.makedirs(out, exist_ok=True)
    F = [json.loads(l) for l in open(os.path.join(HERE, f'{book}.flags.jsonl'), encoding='utf-8')]
    seen, todo = set(), collections.OrderedDict()
    for f in F:
        if f['why'] == 'unknown':
            if f['word'] in seen: continue
            seen.add(f['word'])
        todo.setdefault((f['page'], f['side'], f['line']), []).append(f)
    items = list(todo.items())
    pages = {}
    def column(page, side):
        if page not in pages:
            pages.clear()
            P = json.load(open(os.path.join(HERE, 'ocr', book, f'p{page:04d}.json'), encoding='utf-8'))
            with tempfile.TemporaryDirectory() as d:
                im = O.render(pdf, page, d)
            w, h = im.size; g = P['gutter']; top, bottom = int(h * .055), h - 60
            cols = {'right': im.crop((g + 12, top, w - 40, bottom))} if P['layout'] == 'sh' else \
                   {'left': im.crop((40, top, g - 12, bottom)), 'right': im.crop((g + 12, top, w - 40, bottom))}
            pages[page] = {s: (c, line_boxes(c), P) for s, c in cols.items()}
        return pages[page][side]
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
    except Exception: font = ImageFont.load_default()
    n_sheet = 0
    for i in range(0, len(items), per):
        chunk = items[i:i + per]; crops, meta = [], []
        for j, ((page, side, line), fl) in enumerate(chunk):
            col, boxes, P = column(page, side)
            if line < len(boxes):
                x0, y0, x1, y1 = boxes[line]; crop = col.crop((0, max(0, y0 - 12), col.size[0], min(col.size[1], y1 + 12)))
            else:
                crop = Image.new('L', (col.size[0], 60), 255)
            c = Image.new('L', (crop.size[0] + 70, crop.size[1]), 255); c.paste(crop, (70, 0))
            ImageDraw.Draw(c).text((8, crop.size[1] // 2 - 16), str(j + 1), fill=0, font=font)
            crops.append(c)
            ocr_line = [t for t in (P['cols'][0 if side == P['cols'][0]['side'] else 1]['deva'].splitlines() + [''])][line] if line < len(P['cols'][0]['deva'].splitlines()) else ''
            meta.append({'n': j + 1, 'page': page, 'ocr': ocr_line,
                         'flags': [{'k': f['k'], 'id': f['id'], 'word': f['word'], 'why': f['why'], 'alt': f['alt']} for f in fl]})
        W = max(c.size[0] for c in crops); H = sum(c.size[1] + 6 for c in crops)
        sheet = Image.new('L', (W, H), 255); y = 0
        for c in crops: sheet.paste(c, (0, y)); y += c.size[1] + 6
        sheet = sheet.resize((W * 2 // 3, H * 2 // 3))
        n_sheet += 1
        sheet.save(os.path.join(out, f'sheet-{n_sheet:04d}.png'))
        json.dump(meta, open(os.path.join(out, f'sheet-{n_sheet:04d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    for b in range(0, n_sheet, sheets):
        open(os.path.join(out, f'batch-{b // sheets + 1:02d}.txt'), 'w').write('\n'.join(f'sheet-{k:04d}' for k in range(b + 1, min(b + sheets, n_sheet) + 1)) + '\n')
    print(f'{len(items)} lines to read on {n_sheet} sheets, {-(-n_sheet // sheets)} batches')

if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        prepare(sys.argv[2], sys.argv[3], sys.argv[4])
