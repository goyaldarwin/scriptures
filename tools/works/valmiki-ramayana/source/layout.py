"""Lines of a page of the Gita Press Sanskrit–English Rāmāyaṇa, in reading order, from the text layer.

A page has a running head, then two columns. Each line is (column, y, kind, text, raw):
kind 'sa' for a Chanakya (Sanskrit) line, 'en' for an English (Nalanda) line, 'mix' when both share it.
"""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import chanakya as K

def lines(page):
    w, h, spans = page
    mid = w / 2
    rows = []
    for sp in spans:
        font, size, bb, text, xs = sp[:5]
        x1s = sp[5] if len(sp) > 5 else None
        if x1s and 'Chanakya' in font:      # two words inside one span with only a visible gap: a space
            t2, xs2 = [], []
            for i, ch in enumerate(text):
                if i and ch != ' ' and text[i - 1] != ' ' and xs[i] - max(x1s[:i]) > 2.5:
                    t2.append(' '); xs2.append(xs[i] - 0.1)
                t2.append(ch); xs2.append(xs[i])
            text, xs = ''.join(t2), xs2
        if not text.strip() and 'Chanakya' not in font:
            continue                       # a Chanakya space is its own span on some lines: it divides words
        x0, y0, x1, y1 = bb
        col = 0 if x1 <= mid + 4 else (1 if x0 >= mid - 4 else 2)   # 2 = across both columns
        base = round(y1, 0)
        rows.append([col, base, x0, x1, font, size, text, xs])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = []
    for r in rows:
        if out and out[-1]['col'] == r[0] and abs(out[-1]['y'] - r[1]) <= 2.5:
            out[-1]['spans'].append(r)
        else:
            out.append({'col': r[0], 'y': r[1], 'spans': [r]})
    res = []
    for ln in out:
        sp = sorted(ln['spans'], key=lambda r: r[2])
        sa = all('Chanakya' in r[4] for r in sp)
        en = all('Chanakya' not in r[4] for r in sp)
        kind = 'sa' if sa else 'en' if en else 'mix'
        # join spans: a gap wider than ~1.5 pt is a space
        pieces = []
        last_x1 = None
        for r in sp:
            txt = K.dedupe(r[6], r[7]) if 'Chanakya' in r[4] else r[6]
            if last_x1 is not None and r[2] - last_x1 > (3 if 'Chanakya' in r[4] else 1.5) and not (pieces and pieces[-1][1].endswith(' ')) and not txt.startswith(' '):
                pieces.append((r[4], ' '))
            pieces.append((r[4], txt))
            last_x1 = r[3]
        if kind == 'sa':
            raw = ''.join(t for _, t in pieces)
            text = ' '.join(K.decode(raw).split())
        else:
            raw = ''.join(t for _, t in pieces)
            text = ''.join(K.decode(t) if 'Chanakya' in f else t for f, t in pieces)
        res.append({'col': ln['col'], 'y': ln['y'], 'kind': kind, 'text': text, 'raw': raw,
                    'size': max(r[5] for r in sp), 'fonts': sorted({r[4] for r in sp}),
                    'en_size': max([r[5] for r in sp if 'Chanakya' not in r[4] and r[6].strip()] or [0])})
    return res
