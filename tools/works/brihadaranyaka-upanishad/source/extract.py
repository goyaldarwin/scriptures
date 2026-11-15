"""Bṛhadāraṇyaka Upaniṣad: the owner's printout of sanskritdocuments.org (bribasic.html, printed from Chrome) → source/pdf_raw.json.

Usage: python3 extract.py <brihadaranyaka.pdf>
The PDF is private (scriptures-data: hinduism/veda/yajurveda/shukla-yajurveda/upanishad/brihadaranyaka-upanishad/
printouts/sanskritdocuments/brihadaranyaka.pdf).

Chrome writes each Devanagari cluster whose glyphs do not map one to one onto letters (a conjunct, a reph, a pre-base ि)
as a marked-content span carrying the cluster's letters (/ActualText); every other glyph has its letter in the font's
ToUnicode map. A plain text extraction reads both the span's letters and its glyphs' own letters, which doubles vowel
signs and syllables (मधुु, सूर्यश्चश्चक्षुु). This reads the content stream itself: inside an /ActualText span the span's
letters, once; outside it, each glyph's ToUnicode letters. Lines are the text matrix's rows (Tm); spaces are the
space glyph. Every page line is kept with its font (the page's running heads and footers are dropped), and the
lines are grouped into the śānti, the headings and the mantras ("मन्त्र N [I.ii.N]").
"""
import json, os, re, sys, unicodedata
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = re.compile(rb'<<|>>|<[0-9A-Fa-f\s]*>|\((?:\\.|[^\\)])*\)|/[^\s/<>\[\]()]+|\[|\]|[-+]?\d*\.?\d+|[A-Za-z\'"*]+')


def tounicode(doc, font_xref):
    """The font's ToUnicode CMap: glyph code → letters."""
    desc = doc.xref_get_key(font_xref, 'ToUnicode')
    m = {}
    if desc[0] != 'xref': return m
    cm = doc.xref_stream(int(desc[1].split()[0])).decode('latin-1')
    for blk in re.findall(r'beginbfchar(.*?)endbfchar', cm, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            m[int(a, 16)] = bytes.fromhex(b).decode('utf-16-be')
    for blk in re.findall(r'beginbfrange(.*?)endbfrange', cm, re.S):
        for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            first = bytes.fromhex(c).decode('utf-16-be')
            for k in range(int(a, 16), int(b, 16) + 1):
                m[k] = first[:-1] + chr(ord(first[-1]) + k - int(a, 16))
    return m


def page_lines(doc, page):
    """[(y, font name, size, text)] in content order, one entry per text-matrix row."""
    fonts = {f[4]: (f[3].split('+')[-1], tounicode(doc, f[0])) for f in page.get_fonts()}
    toks = TOKEN.findall(page.read_contents())
    out, stack, pending, font, size, y, cur = [], [], None, None, 0, None, None
    for i, t in enumerate(toks):
        if t == b'BDC':
            # /Span <</ActualText <FEFF…> >> BDC  — the tokens before BDC
            j = i - 1; d = None
            while j >= 0 and toks[j] != b'<<': j -= 1
            seg = toks[j:i]
            if b'/ActualText' in seg:
                h = seg[seg.index(b'/ActualText') + 1]
                d = bytes.fromhex(h[1:-1].decode()).decode('utf-16-be') if h.startswith(b'<') else h[1:-1].decode('latin-1')
            stack.append(d)
            if d is not None: pending = d.lstrip('\ufeff')     # written at the span's first glyph, on that glyph's row
        elif t == b'EMC':
            if stack: stack.pop()
        elif t == b'Tf':
            font, size = toks[i - 2][1:].decode(), float(toks[i - 1])
        elif t == b'Tm':
            ny = round(float(toks[i - 1]), 1)
            if cur is None or ny != y or fonts[font][0] != cur[1]:
                cur = [ny, fonts[font][0], size, []]; out.append(cur)
            y = ny
        elif t == b'Tj':
            s = toks[i - 1]
            if any(x is not None for x in stack):             # the span's letters stand for its glyphs
                if pending is not None: cur[3].append(pending); pending = None
                continue
            codes = bytes.fromhex(s[1:-1].decode()) if s.startswith(b'<') else s[1:-1]
            m = fonts[font][1]
            cur[3].append(''.join(m.get(codes[k] << 8 | codes[k + 1], '�') for k in range(0, len(codes) - 1, 2)))
    return [(y, f, sz, unicodedata.normalize('NFC', ''.join(p))) for y, f, sz, p in out]


TEXT_FONTS = ('DevanagariMT', 'DevanagariMT-Bold', 'AnnaiMN-Regular', 'TimesNewRomanPSMT')   # AnnaiMN: the ꣳ sign
ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12,
         'XIII': 13, 'XIV': 14, 'XV': 15}
REF = re.compile(r'\[\s*\.?([IVX]+)\.([ivx]+)\.(\d+)\.?\s*\]')       # the page's own slips: [I.v.5.], [.I.v.8]
MANTRA = re.compile(r'^मन्त्र\s*([०-९]+)\s*' + REF.pattern + '$')


def rows(doc):
    """Every printed line of the text: {pg, y, bold, t} (the running footer, the URL and the file's metadata dropped)."""
    out = []
    for pi, page in enumerate(doc):
        cur = None
        for y, f, sz, t in page_lines(doc, page):
            if f not in TEXT_FONTS: continue
            if cur is None or y != cur['y']:
                cur = {'pg': pi + 1, 'y': y, 'bold': f.endswith('Bold'), 't': ''}; out.append(cur)
            cur['t'] += t
    for r in out: r['t'] = re.sub(r'\s+', ' ', r['t']).strip()
    return [r for r in out if r['t'] and r['t'] != 'BACK TO TOP']


def blocks(R):
    """Rows → [{kind: head | shanti | mantra, ref?, printed?, rows}] in reading order. A mantra runs from its heading
    ("मन्त्र N [I.ii.N]") to the next heading or structural line (अथ … ब्राह्मणम्, इति … ब्राह्मणम्, the adhyāya lines)."""
    out, cur = [], None
    START = R.index(next(r for r in R if r['t'].startswith('ॐ पूर्णमदः')))
    out.append({'kind': 'contents', 'rows': [r['t'] for r in R[:START]]})
    out.append({'kind': 'shanti', 'rows': [r['t'] for r in R[START:START + 3]]})
    for r in R[START + 3:]:
        t = r['t']
        m = MANTRA.match(t)
        ref = REF.search(t)
        if m or (ref and 'ब्राह्मणम्' in t):
            a, b, n = ROMAN[ref.group(1)], ROMAN[ref.group(2).upper()], int(ref.group(3))
            if not m:      # "अथ द्वादशं ब्राह्मणम् । [V.xii.1]": a heading that carries its only mantra's reference
                out.append({'kind': 'head', 'rows': [REF.sub('', t).strip()]})
            cur = {'kind': 'mantra', 'ref': '%d.%d.%d' % (a, b, n), 'printed': m.group(1) if m else '', 'pg': r['pg'], 'y': r['y'],
                   'rows': []}
            out.append(cur); continue
        if r['bold'] or re.search(r'(ब्राह्मणम्|ब्रह्मणम्|ब्राहमणम्)\s*[।॥]$', t) or re.search(r'ध्यायः\s*[।॥]$', t) or 'समाप्ता' in t \
                or t.startswith('Encoded and proofread'):
            out.append({'kind': 'head', 'rows': [t]}); cur = None; continue
        if cur is None: raise SystemExit('text outside a mantra: page %d: %s' % (r['pg'], t))
        cur['rows'].append({'pg': r['pg'], 'y': r['y'], 't': t})
    return out


if __name__ == '__main__':
    B = blocks(rows(pymupdf.open(sys.argv[1])))
    json.dump(B, open(os.path.join(HERE, 'pdf_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    M = [b for b in B if b['kind'] == 'mantra']
    print(len(M), 'mantras,', sum(len(b['rows']) for b in M), 'lines,', sum(b['kind'] == 'head' for b in B), 'headings')
