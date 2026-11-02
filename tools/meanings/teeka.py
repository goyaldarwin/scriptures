"""Search the two Gurbani commentaries in the private scriptures-data repository (tools/meanings/style.md §11, §12):
Prof. Sahib Singh's Sri Guru Granth Darpan and the Faridkot Teeka. Both PDFs are in the common legacy ASCII Gurmukhi
encoding; their text is converted to Unicode and kept outside this repository (never copied in).

  python3 tools/meanings/teeka.py fetch [SCRIPTURES_DATA]   → ~/.cache/scriptures-dict/darpan.txt, faridkot.txt
      SCRIPTURES_DATA: a checkout of scriptures-data holding reference/pa/commentaries/ (default ../scriptures-data).
      Only that folder is needed: git clone --filter=blob:none --no-checkout --depth 1 <scriptures-data url> DIR, then
      git -C DIR sparse-checkout set --no-cone /reference/pa/commentaries/ and git -C DIR checkout.
  python3 tools/meanings/teeka.py look WORD [--lines N]   every place WORD is in either commentary, with N lines after it
      The commentary's prose and its ਪਦਅਰਥ word glosses convert cleanly; a Gurbani line quoted in the Darpan comes from
      another font and may show the sihari ਿ on the letter before it.

Mahan Kosh (reference/pa/dictionaries/mahan-kosh/) cannot be read this way: its body font maps each glyph to a Korean
code point and keeps no keyboard code for most of them, so its text is not recoverable without reading the glyphs.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'works', 'sukhmani-sahib', 'source')); import gurmukhi
CACHE = os.path.join(os.path.expanduser('~'), '.cache', 'scriptures-dict')
BOOKS = {'darpan': 'reference/pa/commentaries/sahib-singh-darpan/sri-guru-granth-darpan.pdf',
         'faridkot': 'reference/pa/commentaries/faridkot-teeka/faridkot-wala-teeka.pdf'}

def fetch(root):
    T = dict(gurmukhi.TABLE)
    for ch in '()-!?,;:.\'"/*+=%$#@_|{}…–—‘’“”':   # punctuation of the commentaries' prose, kept as it is
        T.setdefault(ch, (ch, 'P'))
    T.setdefault('ƒ', ('ਨੂੰ', 'P'))
    gurmukhi.TABLE = T
    os.makedirs(CACHE, exist_ok=True)
    for name, rel in BOOKS.items():
        pdf = os.path.join(root, rel)
        if not os.path.exists(pdf): sys.exit(f'no {pdf}: check out reference/pa/commentaries/ of scriptures-data (see the help)')
        raw = subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', pdf, '-'], capture_output=True, text=True, check=True).stdout
        out = []
        for line in raw.split('\n'):
            try: out.append(gurmukhi.to_unicode(line))
            except ValueError: out.append(line)   # English, or a line from another font: kept as it is
        open(os.path.join(CACHE, name + '.txt'), 'w', encoding='utf-8').write('\n'.join(out))
        print(name, os.path.join(CACHE, name + '.txt'))

def look(word, n):
    for name in BOOKS:
        p = os.path.join(CACHE, name + '.txt')
        if not os.path.exists(p): sys.exit('run: python3 tools/meanings/teeka.py fetch [SCRIPTURES_DATA]')
        L = open(p, encoding='utf-8').read().split('\n')
        for i, l in enumerate(L):
            if word in l: print(f'== {name}:{i + 1}'); print('\n'.join(L[i:i + n + 1]))

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['fetch']: fetch(a[1] if len(a) > 1 else os.path.join(HERE, '..', '..', '..', 'scriptures-data'))
    elif a[:1] == ['look'] and len(a) > 1: look(a[1], int(a[a.index('--lines') + 1]) if '--lines' in a else 2)
    else: sys.exit(__doc__)
