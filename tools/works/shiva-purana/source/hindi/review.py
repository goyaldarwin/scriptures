"""Read the flagged words by eye: each flag's printed line cut from the page image, a dozen lines to a sheet, with the
OCR reading beside it (hindi/README.md). The page images are made here from the owner's PDF; nothing of them is kept.

    python3 review.py prepare <book> <scan.pdf> <out folder> [--per 12] [--sheets 20]
        → <out>/sheet-NNNN.png (the lines, numbered) and <out>/sheet-NNNN.json ([{n, flags: [{k, id, word, why, alt}], ocr}])
          and <out>/batch-NN.txt (the sheets of one reader's batch)
    python3 review.py apply <book> <out folder>
        → reads <out>/sheet-NNNN.out.json ({"n": {"line": "the line as printed", "words": [word as printed, one per flag]}},
          written by the readers following READER.md) into hindi/<book>.read.json: {"at": {"page|side|line|j": word}, "unknown": {word: as printed}}
          (j: the flag's order among its line's flags; a word both passes read alike, read once, holds everywhere),
          used by make_hindi.py;
          a "?" is left out (the place stays doubtful) and listed

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

def prepare(book, pdf, out, per=12, sheets=20, only=None):
    """only: {(page, side, line)} — the redo pass: just those lines, each cut from the page with a wide margin
    (the column crops can clip a line's first or last letters on a leaning page)."""
    os.makedirs(out, exist_ok=True)
    F = [json.loads(l) for l in open(os.path.join(HERE, f'{book}.flags.jsonl'), encoding='utf-8')]
    seen, todo = set(), collections.OrderedDict()
    for f in F:
        if f['why'] == 'unknown':
            if f['word'] in seen: continue
            seen.add(f['word'])
        todo.setdefault((f['page'], f['side'], f['line']), []).append(f)
    items = [x for x in todo.items() if only is None or x[0] in only]
    pages = {}
    def column(page, side):
        if page not in pages:
            pages.clear()
            P = json.load(open(os.path.join(HERE, 'ocr', book, f'p{page:04d}.json'), encoding='utf-8'))
            with tempfile.TemporaryDirectory() as d:
                im = O.render(pdf, page, d)
            w, h = im.size; g = P['gutter']; top, bottom = int(h * .055), h - 60
            if P['layout'] == 'sh': boxes = {'right': (g + 12, top, w - 40, bottom)}
            else:                                                          # the same band crops ocr.py read
                boxes = {f'{side}{i}': (x0, y0, x1, y1) for i, (y0, y1) in enumerate(P['bands'])
                         for side, x0, x1 in (('left', 40, g - 12), ('right', g + 12, w - 40))}
            pages[page] = {}
            for s_, b in boxes.items():
                c = im.crop(b); lb = line_boxes(c)
                if only is not None:                                       # wide: the line's box moved onto the page
                    lb = [(0, b[1] + y0, 0, b[1] + y1) for _, y0, _, y1 in lb]
                    c = im.crop((0, 0, w, h) if P['layout'] == 'sh' else (max(0, b[0] - 160), 0, min(w, b[2] + 160), h))   # sh: notes run under both columns
                pages[page][s_] = (c, lb, next(x for x in P['cols'] if x['side'] == s_))
        return pages[page][side]
    try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
    except Exception: font = ImageFont.load_default()
    n_sheet = 0
    for i in range(0, len(items), per):
        chunk = items[i:i + per]; crops, meta = [], []
        for j, ((page, side, line), fl) in enumerate(chunk):
            col, boxes, C = column(page, side)
            if line < len(boxes):
                x0, y0, x1, y1 = boxes[line]; m = 12 if only is None else 40
                crop = col.crop((0, max(0, y0 - m), col.size[0], min(col.size[1], y1 + m)))
            else:
                crop = Image.new('L', (col.size[0], 60), 255)
            c = Image.new('L', (crop.size[0] + 70, crop.size[1]), 255); c.paste(crop, (70, 0))
            ImageDraw.Draw(c).text((8, crop.size[1] // 2 - 16), str(j + 1), fill=0, font=font)
            crops.append(c)
            dl = C['deva'].splitlines(); ocr_line = dl[line] if line < len(dl) else ''
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

def apply(book, *outs):
    """The readers' answers, folder by folder: a later folder (a redo pass) overrides an earlier one. Each folder
    keeps the flags its sheets were made from (flags.jsonl), so a later merge, which may renumber, changes nothing."""
    import unicodedata, glob
    nfc = lambda t: unicodedata.normalize('NFC', t).strip()
    got, unknown, missing = {}, {}, []           # place page|side|line|j → (flag, answer or None for a doubt, where)
    for out in outs:
        ff = os.path.join(out, 'flags.jsonl')
        F = [json.loads(l) for l in open(ff if os.path.exists(ff) else os.path.join(HERE, f'{book}.flags.jsonl'), encoding='utf-8')]
        pos, at = {}, collections.Counter()     # each flag's place: j is its order among its line's flags
        for f in F:
            key = f"{f['page']}|{f['side']}|{f['line']}"
            pos.setdefault((f['id'], f['k'], f['word'], f['page']), []).append((f"{key}|{at[key]}", f)); at[key] += 1
        for sj in sorted(glob.glob(os.path.join(out, 'sheet-*[0-9].json'))):
            meta = json.load(open(sj, encoding='utf-8')); oj = sj[:-5] + '.out.json'
            if not os.path.exists(oj): missing.append(os.path.basename(sj)[:-5]); continue
            R = json.load(open(oj, encoding='utf-8'))
            for e in meta:
                words = (R.get(str(e['n'])) or {}).get('words') or []
                ok = len(words) == len(e['flags'])
                for i, f in enumerate(e['flags']):
                    wd = nfc(words[i]) if ok else '⟨?⟩'
                    if wd == '⟨?⟩' or (wd == '?' and '?' not in [f['word']] + f['alt']): wd = None
                    where = (e['page'], os.path.basename(out), os.path.basename(sj), e['n'])
                    for p, full in pos.get((f['id'], f['k'], f['word'], e['page']), []):
                        got[p] = (full, wd, where)
                    if f['why'] == 'unknown' and wd is not None: unknown[f['word']] = wd
    read, doubt, same, extra = {}, [], 0, []
    for p, (f, wd, where) in got.items():
        if wd is None:
            if not (f['why'] == 'unknown' and f['word'] in unknown): doubt.append((*where, f['word']))
            continue
        same += wd == f['word']
        if f['k'] is None:                              # read by one pass only, and not in the text: printed after all?
            if wd: extra.append((f['id'], *where, wd))
            continue
        read[p] = wd
    json.dump({'at': read, 'unknown': unknown}, open(os.path.join(HERE, f'{book}.read.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, sort_keys=True)
    json.dump(sorted(set(doubt)), open(os.path.join(HERE, f'{book}.doubt.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump(extra, open(os.path.join(HERE, f'{book}.extra.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    F = [json.loads(l) for l in open(os.path.join(HERE, f'{book}.flags.jsonl'), encoding='utf-8')]
    at = collections.Counter(); n = 0
    for f in F:
        key = f"{f['page']}|{f['side']}|{f['line']}"; p = f"{key}|{at[key]}"; at[key] += 1
        n += f['k'] is not None and (p in read or (f['why'] == 'unknown' and f['word'] in unknown))
    print(f'{book}: {n} of {sum(f["k"] is not None for f in F)} flagged places in the text read ({same} as the OCR had them); '
          f'sheets not read: {len(missing)}; still in doubt: {len(set(doubt))} ({book}.doubt.json); '
          f'printed words one pass alone read: {len(extra)} ({book}.extra.json)')

def lines(book, *outs):
    """The readers' whole lines set against the text the merge built: where one word of a line differs (a word
    both passes misread alike, so never flagged: फलको for फलकी), the printed word is taken.
    → <book>.lines.json: {verse id: [[word before, as merged, word after, as printed], …]}, applied by make_hindi.py after the flags."""
    import unicodedata, glob, difflib
    sys.path.insert(0, HERE); import make_hindi
    text = make_hindi.texts(book)                    # {verse id: the paragraph with the flags read}
    nf = lambda t: re.sub(r'(?<=[\u0900-\u097F]):', 'ः', unicodedata.normalize('NFC', t).replace('\u200c', '').replace('\u200d', ''))
    core = lambda w: re.sub(r"^[‘’'\"“”(\[—-]+|[‘’'\"“”)\],;!?।॥—-]+$", '', w)
    fix = {}
    for out in outs:
        for sj in sorted(glob.glob(os.path.join(out, 'sheet-*[0-9].json'))):
            R = json.load(open(sj[:-5] + '.out.json', encoding='utf-8'))
            for e in json.load(open(sj, encoding='utf-8')):
                line = (R.get(str(e['n'])) or {}).get('line') or ''
                if not line or '⟨?⟩' in line or line.lstrip().startswith('?'): continue
                vid = e['flags'][0]['id']
                if vid not in text: continue
                P, L = text[vid].split(), nf(line).split()
                if len(L) < 3: continue
                sm = difflib.SequenceMatcher(None, [core(x) for x in P], [core(x) for x in L], autojunk=False)
                for op, i1, i2, j1, j2 in sm.get_opcodes():
                    if op != 'replace' or i2 - i1 != 1 or j2 - j1 != 1 or not 0 < j1 < len(L) - 1: continue
                    a, b = core(P[i1]), core(L[j1])            # whole words inside the line (its ends may be cut)
                    if not a or not b or a == b or re.fullmatch(r'[०-९½/—-]+', a): continue
                    if difflib.SequenceMatcher(None, a, b).ratio() < .75: continue
                    k = [core(P[i1 - 1]) if i1 else '', a, core(P[i1 + 1]) if i1 + 1 < len(P) else '', b]   # with its neighbours
                    if k not in fix.setdefault(vid, []): fix[vid].append(k)
    json.dump(fix, open(os.path.join(HERE, f'{book}.lines.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print(f'{book}: {sum(len(v) for v in fix.values())} words set right from the readers\' lines')

if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        prepare(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'redo':                     # redo <book> <scan.pdf> <first out folder> <redo folder>
        import glob
        book, pdf, first, out = sys.argv[2:6]
        F = [json.loads(l) for l in open(os.path.join(HERE, f'{book}.flags.jsonl'), encoding='utf-8')]
        only = set()
        ff = os.path.join(first, 'flags.jsonl')
        if os.path.exists(ff): F = [json.loads(l) for l in open(ff, encoding='utf-8')]
        for sj in sorted(glob.glob(os.path.join(first, 'sheet-*[0-9].json'))):
            R = json.load(open(sj[:-5] + '.out.json', encoding='utf-8'))
            for e in json.load(open(sj, encoding='utf-8')):
                ws = (R.get(str(e['n'])) or {}).get('words') or []
                if len(ws) != len(e['flags']) or any(x == '⟨?⟩' or (x == '?' and '?' not in [f['word']] + f['alt']) for x, f in zip(ws, e['flags'])):
                    f0 = e['flags'][0]
                    only |= {(f['page'], f['side'], f['line']) for f in F if f['id'] == f0['id'] and f['k'] == f0['k'] and f['word'] == f0['word']}
        prepare(book, pdf, out, per=6, sheets=20, only=only)
        import shutil; shutil.copy(os.path.join(HERE, f'{book}.flags.jsonl'), os.path.join(out, 'flags.jsonl'))
    elif sys.argv[1] == 'lines':                    # lines <book> <out folder> [<redo folder> …]
        lines(sys.argv[2], *sys.argv[3:])
    elif sys.argv[1] == 'apply':                    # apply <book> <out folder> [<redo folder> …]
        apply(sys.argv[2], *sys.argv[3:])
