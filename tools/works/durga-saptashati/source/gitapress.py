"""The Sanskrit of the 13 adhyāyas from the owner's Gita Press book (code 118), the witness of the text.

    python3 tools/works/durga-saptashati/source/gitapress.py <sanskrit-hindi.pdf>

<sanskrit-hindi.pdf> is in scriptures-data at hinduism/stotra/durga/durga-saptashati/books/gitapress/. Its text layer
is in the Chanakya font, read without OCR by tools/works/valmiki-ramayana/source/chanakya.py (docs/PLAYBOOK.md §11),
with the codes this book adds (ADD: the nukta, ! and ?, ट्ठ and ड्ड in the Hindi, the half ह of वह्नि and चिह्न), each
confirmed by the words it occurs in. The mantras are its large lines (the Sanskrit is set in ChanakyaBold at 15–17.5 pt
and the speakers' lines in ChanakyaItalic; the Hindi translation is smaller), footnote marks (smaller digits, *) left
out, cut at each ॥ N॥. Writes witness/gitapress.json: {adhyāya: {mantra number: [its lines]}}, 700 mantras.
compare.py compares it with the text.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'works', 'valmiki-ramayana', 'source'))
import fitz, chanakya

ADD = {184: '़', 33: '!', 63: '?', 95: 'ट्ठ', 97: 'ड्ड', 177: 'ह्'}
DIG = str.maketrans('०१२३४५६७८९', '0123456789')
SPEAKS = re.compile(r'(?:उ|ु|ो)वाच|ऊचुः')

def rows(pdf):
    """The large (Sanskrit) lines of the book in page order: (page, fonts, text)."""
    chanakya.CODE.update(ADD)
    d = fitz.open(pdf); out = {}
    for pn in range(d.page_count):
        for b in d[pn].get_text('rawdict')['blocks']:
            for l in b.get('lines', []):
                sp = [s for s in l['spans'] if ''.join(c['c'] for c in s['chars']).strip()]
                if not sp: continue
                mx = max(s['size'] for s in sp)
                big = mx >= 14 or any(s['size'] >= 12.4 and 'Chanakya' in s['font'] and s['font'].split('+')[-1] != 'Chanakya' for s in sp)
                if not big: continue
                for s in sp:
                    if 'Chanakya' not in s['font']: continue
                    u = chanakya.decode(''.join(c['c'] for c in s['chars']))
                    if s['size'] < mx - 1.5 and re.fullmatch(r'[\s०-९*]+', u): continue      # a footnote mark
                    out.setdefault((pn + 1, round(l['bbox'][1])), []).append((s['bbox'][0], u, s['font'].split('+')[-1]))
    return [(p, {f for _, _, f in xs}, re.sub(r'\s+', ' ', ' '.join(u for _, u, _ in sorted(xs))).strip()) for (p, y), xs in out.items()]

def adhyayas(R):
    out = {}; ch = 0; buf = []; started = skip = False
    for p, f, t in R:
        if p < 59: continue
        if t.startswith('इति श्रीमार्कण्डेय'): buf = []; started = False; skip = True; continue
        if t.endswith('ऽध्यायः') and len(t) < 22 and any(x.startswith('ChanakyaBold') for x in f):
            ch += 1; out[ch] = {}; buf = []; started = skip = False; continue
        if skip or not ch: continue
        if not started and not SPEAKS.search(t): continue          # the heading, viniyoga and dhyāna before the first mantra
        started = True
        nums = list(re.finditer(r'॥\s*([०-९]+)\s*॥', t))
        if not nums: buf.append(t); continue
        last = 0
        for m in nums:
            buf.append(t[last:m.end()].strip()); last = m.end()
            out[ch][int(m.group(1).translate(DIG))] = buf; buf = []
        if t[last:].strip(): buf.append(t[last:].strip())
    return out

def main(pdf):
    V = adhyayas(rows(pdf))
    for c in range(1, 14): assert sorted(V[c]) == list(range(1, len(V[c]) + 1)), c
    assert sum(len(v) for v in V.values()) == 700
    json.dump({str(c): {str(n): l for n, l in V[c].items()} for c in V}, open(os.path.join(HERE, 'witness', 'gitapress.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print({c: len(v) for c, v in V.items()})

if __name__ == '__main__':
    main(sys.argv[1])
