"""Kaṭha Upaniṣad: the owner's PDF (Swami Gurubhaktananda, "Katha Upanishad — A Leap into the Beyond", Sandeepany
Text 20; scriptures-data: <work path>/books/sandeepany/katha-upanishad-gurubhaktananda.pdf) → pdf_raw.json.

Each mantra is printed as a block: its Devanagari (in the legacy font "BRH Devanagari", whose text layer is
unreadable), then its IAST transliteration (readable, but the PDF's font maps the accented letters to Latin-1
symbols: ¡ = ā, ¾ = ś …), then the author's word-by-word English (© the author; not extracted).
This script keeps, per mantra, the transliteration lines with the symbols decoded (`t`); settle.py makes the
Devanagari from them.

Usage: python3 extract.py <the PDF>     (needs pdftotext)
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYM = {'¡': 'ā', '£': 'e', 'µ': 'o', '¯': 'ṃ', '§': 'ī', '¾': 'ś', '»': 'ṛ', '¦': 'ḥ', '½': 'ṣ', '³': 'ṇ',
       '°': 'm̐', 'À': 'ū', '¿': 'ṭ', '±': 'ṅ', '²': 'ñ', '¢': 'ḍ'}
LEGACY = re.compile('[Éû]')                       # every legacy-font Devanagari line has the vertical bar glyph É (or û)
HEAD = re.compile(r'^\x0c?\s*(\d\.\d\.\d+):')     # "1.1.1:   The Sacrifice of Nachiketas' Father"

def decode(s):
    s = s.replace(":'", "'")                      # the avagraha comes out as :'
    s = re.sub(r'\|\|\s*\d\.\d\.\d+\s*\|\|', '', s)   # the verse number at the end
    return ''.join(SYM.get(c, c) for c in s).strip()

def main(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], check=True, capture_output=True).stdout.decode('utf-8')
    L = txt.split('\n')
    # Each mantra's transliteration ends with its number, "|| 1.3.4||". The lines before it, back to the last
    # Devanagari (legacy) line or English line, are its transliteration. (Headings group some mantras: "1.3.3 & 4:".)
    out, buf = {}, []
    body = next(i for i, l in enumerate(L) if HEAD.match(l) and 'Sacrifice' in l and i > 300)   # past the contents
    for l in L[body:]:
        s = l.strip()
        if not s or s.isdigit(): continue                 # blank, or a page number
        if LEGACY.search(s) or re.search('[A-Z]', s): buf = []; continue   # Devanagari; English (headings, word-by-word, prose)
        m = re.search(r'\|\|\s*(\d\.\d\.\d+)\s*\|\|\s*$', s)
        buf.append(decode(s))
        if m:
            vid = m.group(1); assert vid not in out, vid
            out[vid] = {'t': buf}; buf = []
    want = ['%d.%d.%d' % (a, v, m) for a, v, n in [(1, 1, 29), (1, 2, 25), (1, 3, 17), (2, 1, 15), (2, 2, 15), (2, 3, 18)] for m in range(1, n + 1)]
    assert list(out) == want, (set(want) ^ set(out))     # the author's 2.3.19 (the śānti again) has no transliteration
    # the śānti mantra (opening page "Chapter 1.0", and again as the author's 2.3.19): its transliteration
    j = next(i for i, l in enumerate(L) if 'PEACE INVOCATION' in l)
    sh = [decode(l) for l in L[j:j + 12] if re.search('[¡§µ£¯½¾¦]', l) and not LEGACY.search(l)]
    assert len(sh) == 3, sh
    out['shanti'] = {'t': sh}
    json.dump(out, open(os.path.join(HERE, 'pdf_raw.json'), 'w'), ensure_ascii=False, indent=1)
    n = sum(len(v['t']) for v in out.values())
    print(len(out) - 1, 'mantras + śānti;', n, 'transliteration lines')

if __name__ == '__main__':
    main(sys.argv[1])
