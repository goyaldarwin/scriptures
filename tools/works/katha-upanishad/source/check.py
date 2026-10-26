"""Checks text.txt (the Kaṭha Upaniṣad) against the Devanagari witnesses in source/witness/.

Every verse in a witness file (plain text: verses separated by blank lines, each ending in ॥ N॥; the first
   block without a number is the śānti mantra; a line "# 1.2" names the vallī the following verses belong to,
the default being 1.1) must spell the same words as text.txt. Daṇḍas, bars, numbers and hyphens at line
breaks are ignored; ॐ is read as ओं too. The only differences allowed are those listed in reconciliation.md
(EXPECTED below).
Usage: python3 tools/works/katha-upanishad/source/check.py
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
ITEMS = textfile.read(os.path.join(HERE, '..', 'text.txt'))
BY = {x['id']: x for x in ITEMS}

def words(s):
    s = re.sub(r'-\s*\n\s*', '', s)                 # a word broken over two lines (मे-/ऽनश्नन्)
    s = s.replace('ॐ', 'ओं').replace('\u200d', '')      # the witness writes श‍ृ with a joiner
    return ' '.join(re.sub(r'[।॥|,0-9०-९\-]', ' ', s).split())

EXPECTED = {   # item id: [(witness, ours)]: differences recorded in reconciliation.md
    '1.2.18': [('विपश्चिन्नायं', 'विपश्चिन् नायं')],         # the book breaks the line inside the sandhi
    '2.1.1': [('स्वयम्भूस्तस्मात्पराङ्पश्यति', 'स्वयम्भूः तस्मात्पराङ्पश्यति'), ('प्रत्यगात्मानमैक्षदावृत्त', 'प्रत्यगात्मानमैक्षद् आवृत्त')],
    '2.3.17': [('प्रवृहेन्मुञ्जादिवेषीकां', 'प्रवृहेन् मुञ्जादिवेषीकां')],
}

def witness(path):
    txt = open(path, encoding='utf-8').read()
    valli, n, bad, seen = '1.1', 0, 0, 0
    for blk in re.split(r'\n\s*\n', txt.strip()):
        blk = blk.strip()
        if not blk: continue
        if blk.startswith('#'): valli = blk[1:].strip(); continue
        m = re.search(r'॥\s*([०-९0-9]+)\s*॥\s*$', blk)
        if m:
            num = int(''.join(str('०१२३४५६७८९'.find(c)) if c in '०१२३४५६७८९' else c for c in m.group(1)))
            vid = '%s.%d' % (valli, num)
        else: vid = 'shanti.1'
        if vid == '2.3.19': continue      # the witness's closing śānti; the work ends with 2.3.18
        if vid not in BY: print(path, 'has', vid, 'which is not in text.txt'); bad += 1; continue
        a, b = words(blk), words('\n'.join(BY[vid]['v']))
        for w, o in EXPECTED.get(vid, []): a = a.replace(w, o)
        seen += 1
        if a != b:
            bad += 1; A, B = a.split(), b.split()
            print('≠', vid, '\n  witness:', ' '.join(x for x in A if x not in B) or a, '\n  ours:   ', ' '.join(x for x in B if x not in A) or b)
    return seen, bad

bad = 0
for path in sorted(glob.glob(os.path.join(HERE, 'witness', '*.txt'))):
    seen, b = witness(path); bad += b
    print(os.path.basename(path) + ':', seen, 'verses compared,', b, 'differences')
sys.exit(1 if bad else 0)
