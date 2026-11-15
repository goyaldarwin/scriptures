"""Aitareya Upaniṣad: the owner's PDF (Swami Gurubhaktananda, "Aitareya Upanishad", Sandeepany Text 34;
scriptures-data: <work path>/books/sandeepany/aitareya-upanishad-gurubhaktananda.pdf) → pdf_raw.json.

The book is the Kaṭha's series and typesetting: each mantra (the book's "Verse 1.1" … "Verse 6.1") is printed in
Devanagari (legacy font "BRH Devanagari", unreadable), beside or above its IAST transliteration (font "BRH Latin",
readable once the Latin-1 symbols are decoded with the Kaṭha's map: tools/works/katha-upanishad/source/extract.py),
then the author's word-by-word English (© the author; not extracted). The two columns share lines, so the
transliteration is read by font from PyMuPDF's spans, not from the page text.

The book numbers its chapters 1–6: chapters 1, 2 and 3 (3A, 3B) are adhyāya 1's three khaṇḍas, chapter 4 is
adhyāya 2, chapter 5 adhyāya 3, chapter 6 the śānti mantra (which the book prints only at the end). Its "Verse 5.3A"
and "5.3B" are one mantra, 3.1.3. Each line's leading number (the author's line count, "11." or "1)") is dropped.
This script keeps, per mantra, the transliteration lines with the symbols decoded (`t`); settle.py makes the
Devanagari from them.

Usage: python3 extract.py <the PDF>     (needs PyMuPDF: pip install pymupdf)
"""
import importlib.util, json, os, re, sys
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
_k = importlib.util.spec_from_file_location('katha_extract', os.path.join(HERE, '..', '..', 'katha-upanishad', 'source', 'extract.py'))
katha = importlib.util.module_from_spec(_k); _k.loader.exec_module(katha)

VERSE = re.compile(r'^\s*Verse (\d)\.(\d+)([AB]?):')       # "Verse 1.4:    The Eight Chief Devatas …"
NUM = re.compile(r'^\s*(\d\)|\d+\.?)\s*')                 # the author's line number: "11.", "11 ", "1)" (a line may have two: "8.  1)")
CHAPTER = {1: ('1', '1'), 2: ('1', '2'), 3: ('1', '3'), 4: ('2', '1'), 5: ('3', '1')}   # the book's chapter → adhyāya, khaṇḍa
ANNOUNCE = "|| yath¡ sth¡na¯ garbhi³ya¦ ||"               # the teacher's closing call after 2.1.6 (not a mantra)

def lines(pdf):
    """(page, kind, text) in reading order: kind 'V' for a verse heading, 'L' for a line in the BRH Latin font."""
    for pn, page in enumerate(fitz.open(pdf)):
        rows = {}
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    if not s['text'].strip(): continue
                    latin = s['font'].startswith('BRH Latin')
                    if not latin and not VERSE.match(s['text']): continue
                    rows.setdefault(round(s['bbox'][1] / 3), []).append((s['bbox'][0], latin, s['text']))
        for y in sorted(rows):
            r = sorted(rows[y])
            lat = ' '.join(t.strip() for x, latin, t in r if latin)
            if lat: yield pn + 1, 'L', lat
            else: yield pn + 1, 'V', ''.join(t for x, latin, t in r)

def main(pdf):
    out, cur = {}, None
    for pn, kind, s in lines(pdf):
        if kind == 'V':
            if pn < 10: continue                            # the contents pages
            ch, v, ab = VERSE.match(s).groups(); ch, v = int(ch), int(v)
            cur = 'shanti' if ch == 6 else '%s.%s.%d' % (*CHAPTER[ch], v)
            if ab != 'B': assert cur not in out, cur; out[cur] = {'t': []}
            continue
        if cur is None: continue
        if s.strip() == ANNOUNCE: continue
        while NUM.match(s): s = NUM.sub('', s, count=1)
        if not s: continue                                  # a line number on a line of its own
        out[cur]['t'].append(' '.join(katha.decode(s).split()))
    want = ['%d.%d.%d' % (a, k, m) for a, k, n in [(1, 1, 4), (1, 2, 5), (1, 3, 14), (2, 1, 6), (3, 1, 4)] for m in range(1, n + 1)] + ['shanti']
    assert list(out) == want, set(want) ^ set(out)
    json.dump(out, open(os.path.join(HERE, 'pdf_raw.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(out) - 1, 'mantras + śānti;', sum(len(v['t']) for v in out.values()), 'transliteration lines')

if __name__ == '__main__':
    main(sys.argv[1])
