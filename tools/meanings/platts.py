"""Look a Hindi, Awadhi or Braj word up in Platts, A Dictionary of Urdū, Classical Hindī and English (1884), the main
dictionary for those languages (tools/meanings/style.md §11). The book is in the private scriptures-data repository;
its text is read from there and kept outside this repository (never copied in).

  python3 tools/meanings/platts.py fetch [SCRIPTURES_DATA]   text of the private copy → ~/.cache/scriptures-dict/platts.txt
      SCRIPTURES_DATA: a checkout of scriptures-data holding reference/hi/dictionaries/platts/ (default ../scriptures-data).
      Only that folder is needed: git clone --filter=blob:none --no-checkout --depth 1 <scriptures-data url> DIR, then
      git -C DIR sparse-checkout set --no-cone /reference/hi/dictionaries/platts/ and git -C DIR checkout.
  python3 tools/meanings/platts.py look WORD [WORD ...]
      every entry whose headword is WORD: its Devanagari, or its roman spelling compared loosely (the PDF's Devanagari is
      often garbled, क्षुद्र reads "क्षुि", and a Persian or Arabic word has none; its roman spelling is reliable).
"""
import os, re, subprocess, sys, unicodedata

CACHE = os.path.join(os.path.expanduser('~'), '.cache', 'scriptures-dict', 'platts.txt')
PDF = os.path.join('reference', 'hi', 'dictionaries', 'platts', 'urdu-classical-hindi-english-1884.pdf')
START = re.compile(r'^[APHST] ')   # an entry starts with its source: Arabic, Persian, Hindī, Sanskrit, Turkish
ARABIC = re.compile(r'[؀-ۿﭐ-﻿‎‏‪-‮]+')
DEVA = re.compile(r'[ऀ-ॿ][ऀ-ॿ‌‍]*')
ROMAN = re.compile(r"[a-zāīūṛṙṝḷṅñṭḍṇśṣḥṃćĕŏ`'-]{2,}")

def fetch(root):
    pdf = os.path.join(root, PDF)
    if not os.path.exists(pdf): sys.exit(f'no {pdf}: check out reference/hi/dictionaries/platts/ of scriptures-data (see the help)')
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', pdf, CACHE], check=True)   # -raw: an entry's lines stay together (two columns a page)
    print('Platts text:', CACHE)

def entries():
    """(Devanagari headword or '', roman headword, entry text without the Arabic script)."""
    if not os.path.exists(CACHE): sys.exit('run: python3 tools/meanings/platts.py fetch [SCRIPTURES_DATA]')
    text = []
    def done():
        t = ARABIC.sub('', ' '.join(text)); head = t[2:80]
        d = DEVA.search(head); r = ROMAN.search(head[d.end():] if d else head)
        return (d.group(0) if d else ''), (r.group(0) if r else ''), t
    for line in open(CACHE, encoding='utf-8'):
        if START.match(line) and text: yield done(); text = []
        if START.match(line) or text: text.append(line.strip())
    if text: yield done()

V = {'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 'ऋ': 'ri', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au'}
M = {'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū', 'ृ': 'ri', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ॉ': 'o'}
C = dict(zip('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह', 'k kh g gh n ch chh j jh n ṭ ṭh ḍ ḍh n t th d dh n p ph b bh m y r l w sh sh s h'.split()))
C.update({'ड़': 'ṛ', 'ढ़': 'ṛh', 'क़': 'k', 'ख़': 'kh', 'ग़': 'g', 'ज़': 'z', 'फ़': 'f'})

def roman(w):
    """A Devanagari word in a roman spelling close to Platts's."""
    w = unicodedata.normalize('NFC', w); out = []; i = 0
    while i < len(w):
        c = w[i]
        if w[i:i + 2] in C: c = w[i:i + 2]; i += 1
        if c in C:
            out.append(C[c]); nx = w[i + 1:i + 2]
            if nx == '्': i += 1
            elif nx in M: out.append(M[nx]); i += 1
            elif nx: out.append('a')
        elif c in V: out.append(V[c])
        elif c in 'ंँ': out.append('n')
        i += 1
    return ''.join(out)

def skel(t):
    """A spelling key: no diacritics, ć = ch = c, v = w, sh = s, short a and doubled letters ignored."""
    t = ''.join(ch for ch in unicodedata.normalize('NFD', t.lower()) if not unicodedata.combining(ch)).replace('`', '').replace("'", '').replace('-', '')
    t = t.replace('v', 'w').replace('sh', 's').replace('ch', 'c').replace('a', '')
    return re.sub(r'(.)\1', r'\1', t)

def look(words):
    found = {w: [] for w in words}; key = {w: skel(roman(w)) for w in words}
    for d, r, t in entries():
        k = skel(r) if r else None
        for w in words:
            if d == w or (k and k == key[w]): found[w].append(t[:700])
    return found

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['fetch']: fetch(a[1] if len(a) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'scriptures-data'))
    elif a[:1] == ['look'] and len(a) > 1:
        for w, es in look(a[1:]).items():
            print(f'== {w}: {len(es)} entr{"y" if len(es) == 1 else "ies"}')
            for e in es: print('  ' + e)
    else: sys.exit(__doc__)
