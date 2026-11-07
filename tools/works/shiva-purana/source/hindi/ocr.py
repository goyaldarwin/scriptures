"""OCR of the Hindi in the owner's scans of the Śiva Purāṇa: the raw passes only (they are checked later, every flag read by
eye on the page image: hindi/README.md). The scans have no text layer; the owner's choice for them is OCR, with every
word the checks flag read by eye (docs/PLAYBOOK.md §11 stays the rule for every other book).

    python3 ocr.py <scan.pdf> <layout> <first page> <last page> <out folder>

layout: "sh"  — Gita Press code 2223: Sanskrit in the left column, its Hindi in the right (the Hindi column is read);
        "hh"  — Kalyan 2018: Hindi in both columns, read band by band (a line across the gutter, such as an adhyāya's
                closing line and the next heading, ends a band), each band left column then right.
For each page it writes <out>/p<NNNN>.json: the gutter found, and for each Hindi column the two passes — Tesseract's
`hin` model and its `Devanagari` script model, which make different mistakes — and, for the whole page, a `hin` pass
in reading order (the adhyāya titles and closing lines run across both columns). In the Devanagari pass a dash whose
ink is as long as an em dash (Gita Press's —, after बोले and before an explanation) is written —, where Tesseract
reads it as a hyphen.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

DPI = 300
EM = 30          # an em dash's ink at 300 dpi is about 45 px long, a hyphen's about 15

def render(pdf, p, d):
    base = os.path.join(d, f'p{p}')
    subprocess.run(['pdftoppm', '-f', str(p), '-l', str(p), '-r', str(DPI), '-gray', '-singlefile', '-png', pdf, base], check=True)
    return Image.open(base + '.png').convert('L')

def gutter(im):
    """The column gap: the least inked band between 42% and 62% of the width, over the page's body."""
    a = np.array(im) < 128; h, w = a.shape
    body = a[int(h * .25):int(h * .9)].mean(axis=0)
    sm = np.convolve(body, np.ones(25) / 25, 'same')
    lo, hi = int(w * .42), int(w * .62)
    return lo + int(sm[lo:hi].argmin())

def bands(im, g, top, bottom):
    """For a page with Hindi in both columns: the bands between the lines that run across the gutter (an adhyāya's
    closing line and the next one's heading), so each band is read left column, then right — the book's order."""
    a = np.array(im) < 128; h = a.shape[0]
    prof = a[int(h * .1):int(h * .95), g - 40:g + 41].mean(axis=0)
    r = g - 40 + int(prof.argmax())                                       # the printed rule between the columns
    rows = a[:, 40:-40].copy(); rows[:, r - 52:r - 28] = False             # ignore the rule's own band
    inked = rows.any(axis=1)
    cuts, y = [], top
    while y < bottom:                                                     # each printed line: a run of inked rows
        if not inked[y]: y += 1; continue
        y0 = y
        while y < bottom and inked[y]: y += 1
        L, R = a[y0:y, r - 22:r - 10], a[y0:y, r + 8:r + 20]              # the white margins beside the rule
        if y - y0 >= 15 and L.mean() > 0.15 and R.mean() > 0.15: cuts.append((y0, y))   # both inked: a line across
    out, start = [], top
    for y0, y1 in cuts:
        if y0 - start > 40: out.append((start, y0))
        start = y1
    if bottom - start > 40: out.append((start, bottom))
    return out or [(top, bottom)]

def tess(img, lang, psm=6, tsv=False):
    with tempfile.NamedTemporaryFile(suffix='.png') as f:
        img.save(f.name)
        cmd = ['tesseract', f.name, '-', '-l', lang, '--psm', str(psm)] + (['tsv'] if tsv else [])
        return subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, 'OMP_THREAD_LIMIT': '1'}).stdout

def bars(sub):
    """The dashes in a word's box, left to right, as their ink length: a bar at mid-height (40–80% of the box, below
    the headline that joins the letters) with blank rows above and below it."""
    hh = sub.shape[0]; found = {}
    for r in range(int(hh * .4), int(hh * .8)):
        if r - 6 < 0 or r + 6 >= hh: continue
        c0 = None
        for i, v in enumerate(list(sub[r]) + [False]):
            if v and c0 is None: c0 = i
            if not v and c0 is not None:
                if i - c0 >= 8 and sub[r - 6:r - 3, c0:i].mean() < .15 and sub[r + 3:r + 6, c0:i].mean() < .15:
                    k = next((k for k in found if abs(k - c0) < 6), c0); found[k] = max(found.get(k, 0), i - c0)
                c0 = None
    return [found[k] for k in sorted(found)]

def deva_with_dashes(img):
    """The Devanagari pass, line by line from its word boxes, with each hyphen whose ink is em-dash long written —."""
    rows = [r.split('\t') for r in tess(img, 'Devanagari', 6, tsv=True).splitlines()[1:]]
    a = np.array(img) < 140
    lines, fixed = {}, 0
    for r in rows:
        if len(r) < 12 or r[0] != '5' or not r[11].strip(): continue
        key = (int(r[2]), int(r[3]), int(r[4]))
        word = r[11]
        if '-' in word:
            x, y, w, h = map(int, r[6:10])
            L = bars(a[y:y + h, x:x + w])
            if len(L) == word.count('-'):                                  # each hyphen read, by its own bar
                it = iter(L); word = ''.join(('—' if next(it) >= EM else '-') if ch == '-' else ch for ch in word)
                fixed += word.count('—')
        lines.setdefault(key, []).append(word)
    return '\n'.join(' '.join(ws) for _, ws in sorted(lines.items())) + '\n', fixed

def page(pdf, layout, p, out):
    with tempfile.TemporaryDirectory() as d:
        im = render(pdf, p, d); w, h = im.size
        g = gutter(im)
        top, bottom = int(h * .055), h - 60                              # below the running header
        if layout == 'sh':
            cols = [('right', im.crop((g + 12, top, w - 40, bottom)))]
        else:                                                              # band by band, left then right
            cols = [(f'{side}{i}', im.crop((x0, y0, x1, y1))) for i, (y0, y1) in enumerate(bands(im, g, top, bottom))
                    for side, x0, x1 in (('left', 40, g - 12), ('right', g + 12, w - 40))]
        res = {'page': p, 'layout': layout, 'gutter': g, 'size': [w, h], 'cols': [], 'full': tess(im, 'hin', 3)}
        if layout == 'hh': res['bands'] = bands(im, g, top, bottom)
        for side, c in cols:
            deva, dashes = deva_with_dashes(c)
            res['cols'].append({'side': side, 'hin': tess(c, 'hin', 6), 'deva': deva, 'em_dashes': dashes})
    json.dump(res, open(os.path.join(out, f'p{p:04d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

if __name__ == '__main__':
    pdf, layout, a, b, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    assert layout in ('sh', 'hh'), layout
    os.makedirs(out, exist_ok=True)
    for p in range(a, b + 1):
        if os.path.exists(os.path.join(out, f'p{p:04d}.json')): continue      # resumable
        page(pdf, layout, p, out); print('page', p, flush=True)
