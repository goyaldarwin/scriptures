"""Śrī Rudram: the owner's shlokam.org printouts (PDF) → source/<part>_raw.json.

Usage: python3 extract.py <namakam.pdf> <chamakam.pdf> [private folder for the page's English]
The PDFs are private (scriptures-data: hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/printouts/shlokam/).
For every text block on the page this keeps, in reading order: the heading above it ("1st Anuvaka", "Shanti Mantra"),
its Devanagari lines (size 21.8 type) and its transliteration lines. The Devanagari text layer has known breaks
(repeated svaras and vowel signs, a dropped reph); these are settled in settle.py against the transliteration and
the page images, see ../reconciliation.md.
"""
import json, os, re, sys, pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))

def lines(pdf):
    out = []
    for pi, p in enumerate(pymupdf.open(pdf)):
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                sp = [s for s in l['spans'] if s['text'].strip()]
                if not sp: continue
                t = ''.join(s['text'] for s in l['spans']).strip()
                f = sp[0]['font']; size = round(sp[0]['size'], 1)
                if f == 'Times-Roman' or t.startswith('Visit Shlokam.org'): continue
                bold = any(':' in s['text'] for s in sp[:2]) and sp[0]['font'] not in ('NotoSerif-Italic',)
                kind = ('S' if size == 21.8 else 'H' if size in (11.2, 8.2) else 'I' if f == 'NotoSerif-Italic' else 'B')
                out.append({'pg': pi + 1, 'y': round(l['bbox'][1], 1), 'k': kind, 't': t})
    return out

def blocks(L):
    """S-run → block; following B lines up to the first I line = transliteration; I = page English; B after I = glosses."""
    res, cur, head, state = [], None, '', None
    for r in L:
        if r['k'] == 'H':
            if 'Anuvaka' in r['t'] or 'Shanti' in r['t'] or 'प्रश्न' in r['t']: head = r['t']
            if r['t'] in ('SANSKRIT', 'TRANSLITERATION', 'TRANSLATION', 'WORD-MEANINGS'): pass
            continue
        if r['k'] == 'S':
            if state != 'S':
                cur = {'head': head, 'pg': r['pg'], 'v': [], 't': [], 'en_page': [], 'gloss': []}; res.append(cur)
            cur['v'].append(r['t']); state = 'S'; continue
        if cur is None: continue
        if r['k'] == 'I':
            cur['en_page'].append(r['t']); state = 'I'; continue
        if state == 'S' or state == 'T':
            cur['t'].append(r['t']); state = 'T'
        else:
            cur['gloss'].append(r['t']); state = 'G'
    return res

if __name__ == '__main__':
    # Only the Sanskrit and its transliteration are kept here. The page's English and word glosses are the
    # publisher's own text: they are read as a guide for our meanings and are written, if a 3rd argument
    # (a private folder) is given, only there, never into this public repository.
    priv = sys.argv[3] if len(sys.argv) > 3 else None
    for name, pdf in zip(('namakam', 'chamakam'), sys.argv[1:3]):
        B = blocks(lines(pdf))
        if priv: json.dump(B, open(os.path.join(priv, name + '_page.json'), 'w'), ensure_ascii=False, indent=0)
        # the page's English introduction is laid out between the first block's lines; keep transliteration only
        EN = re.compile(r'\b(the|and|of|is|to|in|with)\b|^[a-z]+\.$')
        B = [{'head': b['head'], 'pg': b['pg'], 'v': b['v'], 't': [t for t in b['t'] if not EN.search(t)]} for b in B]
        json.dump(B, open(os.path.join(HERE, name + '_raw.json'), 'w'), ensure_ascii=False, indent=0)
        print(name, len(B), 'blocks', sum(len(b['v']) for b in B), 'Devanagari lines')
