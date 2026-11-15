"""Kena Upaniṣad: the owner's PDF (Swami Gurubhaktananda, "Kena Upanishad — Know That Alone as Brahman", Sandeepany
Text 38; scriptures-data: <work path>/books/sandeepany/kena-upanishad-gurubhaktananda.pdf) → pdf_raw.json.

The book is the same series and typesetting as the Kaṭha's (tools/works/katha-upanishad/source/extract.py): each
mantra is printed as its Devanagari (in the legacy font "BRH Devanagari", whose text layer is unreadable), then its
IAST transliteration (readable once the font's Latin-1 symbols are decoded: ¡ = ā, ¾ = ś …), then the author's
word-by-word English (© the author; not extracted). This script keeps, per mantra, the transliteration lines with the
symbols decoded (`t`), the śānti mantra's (the Sāmaveda's आप्यायन्तु, page "B. PEACE INVOCATION"), and the closing
words of each khaṇḍa and of the Upaniṣad (`iti`); settle.py makes the Devanagari from them.

The book prints mantra 1.3 in two halves, "|| 1.3.1 ||" and "|| 1.3.2 ||" (its headings "Verse 1.3a", "1.3b"); they
are kept as the two halves of 1.3 (`t` is their lines in order).

Usage: python3 extract.py <the PDF>     (needs PyMuPDF)
"""
import json, os, re, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
SYM = {'¡': 'ā', '£': 'e', 'µ': 'o', '¯': 'ṃ', '§': 'ī', '¾': 'ś', '»': 'ṛ', '¦': 'ḥ', '½': 'ṣ', '³': 'ṇ',
       '°': 'm̐', 'À': 'ū', '¿': 'ṭ', '±': 'ṅ', '²': 'ñ', '¢': 'ḍ'}
LEGACY = re.compile('[ÉûÌÍÎÏÇ]')                  # letters of the legacy-font Devanagari (É, the vertical bar, on nearly every line)
NUM = re.compile(r'\|\|\s*(\d)\.(\d+)(?:\.(\d))?\s*\|\|\s*$')   # "|| 1.4 ||", "|| 1.3.2 ||" at a line's end
ITI = re.compile(r'^\|\|\s*(iti [^|]*?)\s*\|\|$')
COUNT = {1: 8, 2: 5, 3: 12, 4: 9}                # the book's mantras per khaṇḍa (its 1.3 in two halves)

def decode(s):
    s = NUM.sub('', s).replace(":'", "'")         # the avagraha comes out as :'
    s = re.sub(r':\s*$', '-', s.rstrip())         # … and as : at a line's end, the next line starting with ' (indro- / 'titarām)
    return ''.join(SYM.get(c, c) for c in s).strip()

def lines(pdf):
    return [l for p in pymupdf.open(pdf) for l in p.get_text().split('\n')]

def main(pdf):
    L = lines(pdf)
    body = next(i for i, l in enumerate(L) if l.strip().startswith('Verse 1.1:'))
    out, iti, buf, khanda = {}, {}, [], 1
    for l in L[body:]:
        s = l.strip()
        if not s or s.isdigit() or s == '*****': continue           # blank, a page number, a rule
        m = ITI.match(s)
        if m:
            if LEGACY.search(s): continue                           # the Devanagari of the closing words
            iti.setdefault(str(khanda), []).append(decode(m.group(1)))
            if 'khaṇḍaḥ' in iti[str(khanda)][-1] and khanda < 4: khanda += 1
            buf = []; continue
        if LEGACY.search(s) or re.search('[A-Z]', s): buf = []; continue   # Devanagari; English (headings, word-by-word, prose)
        m = NUM.search(s)
        if m and not NUM.sub('', s).strip() and not buf: continue   # the number under a Devanagari block
        if NUM.sub('', s).strip(): buf.append(decode(s))
        if m:
            vid = '%s.%s' % (m.group(1), m.group(2))
            if m.group(3): out.setdefault(vid, {'t': []})['t'] += buf     # 1.3.1, 1.3.2: the halves of 1.3
            else: assert vid not in out, vid; out[vid] = {'t': buf}
            buf = []
    want = ['%d.%d' % (k, n) for k, c in COUNT.items() for n in range(1, c + 1)]
    assert list(out) == want, (set(want) ^ set(out))
    assert [len(v) for v in iti.values()] == [1, 1, 1, 2], iti      # each khaṇḍa's; the fourth's and the Upaniṣad's
    # the śānti mantra: its transliteration, after the Devanagari on the page "B. PEACE INVOCATION"
    j = next(i for i, l in enumerate(L) if 'PEACE INVOCATION' in l)
    sh = []
    for l in L[j:]:
        s = l.strip()
        if not s or LEGACY.search(s) or re.search('[A-Z]', s): continue
        sh.append(decode(s))
        if 'śāntiḥ śāntiḥ śāntiḥ' in sh[-1]: break
    assert sh[0].startswith('om̐ āpyāyantu') and len(sh) == 11, sh
    out['shanti'] = {'t': sh}
    out['iti'] = iti
    json.dump(out, open(os.path.join(HERE, 'pdf_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    n = sum(len(v['t']) for k, v in out.items() if k != 'iti')
    print(len(want), 'mantras + śānti;', n, 'transliteration lines;', sum(map(len, iti.values())), 'closing lines')

if __name__ == '__main__':
    main(sys.argv[1])
