"""Checks text.json against the owner's printout of shlokam.org (the source of truth for the text).

The printout's Devanagari text layer drops every र् (पूणम् for पूर्णम्) and doubles some vowel signs, so it
can't be compared directly; its transliteration layer is clean. This script:
  1. reads the printout's transliteration of each verse (the Latin lines ending in |, || or || N ||),
  2. converts it to Devanagari and compares it with text.json → v; the only differences allowed are the
     corrections listed in reconciliation.md (EXPECTED below),
  3. converts text.json → t to Devanagari and checks it equals v (our transliteration matches our text).
The Devanagari of every verse is also checked by eye against the page images (reconciliation.md).

Usage: python3 tools/works/isha-upanishad/check.py <scriptures-data>/hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/printouts/shlokam/isha-upanishad.pdf
Without the PDF it runs step 3 only.
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = json.load(open(os.path.join(HERE, 'text.json'), encoding='utf-8'))['items']

V = {'a': '', 'ā': 'ा', 'i': 'ि', 'ī': 'ी', 'u': 'ु', 'ū': 'ू', 'ṛ': 'ृ', 'ṝ': 'ॄ', 'e': 'े', 'ai': 'ै', 'o': 'ो', 'au': 'ौ'}
IV = {'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ', 'ṛ': 'ऋ', 'ṝ': 'ॠ', 'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ'}
C = {'kh': 'ख', 'gh': 'घ', 'ch': 'छ', 'jh': 'झ', 'ṭh': 'ठ', 'ḍh': 'ढ', 'th': 'थ', 'dh': 'ध', 'ph': 'फ', 'bh': 'भ',
     'k': 'क', 'g': 'ग', 'ṅ': 'ङ', 'c': 'च', 'j': 'ज', 'ñ': 'ञ', 'ṭ': 'ट', 'ḍ': 'ड', 'ṇ': 'ण', 't': 'त', 'd': 'द', 'n': 'न',
     'p': 'प', 'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'ś': 'श', 'ṣ': 'ष', 's': 'स', 'h': 'ह'}
TOK = sorted(list(V) + list(C), key=len, reverse=True)

def deva(s):
    """IAST → Devanagari, for comparison only (word by word; no digits or punctuation)."""
    out = []
    for w in s.split():
        r, i, prev_c = '', 0, False
        while i < len(w):
            ch = w[i]
            if ch in "'’": r += 'ऽ'; i += 1; prev_c = False; continue
            if ch in 'ṁṃ': r += 'ं'; i += 1; prev_c = False; continue
            if ch == 'ḥ': r += 'ः'; i += 1; prev_c = False; continue
            t = next((t for t in TOK if w.startswith(t, i)), None)
            if t is None: raise ValueError('unknown letter %r in %r' % (ch, w))
            if t in C:
                if prev_c: r += '्'
                r += C[t]; prev_c = True
            else:
                r += V[t] if prev_c else IV[t]; prev_c = False
            i += len(t)
        if prev_c: r += '्'
        out.append(r)
    return ' '.join(out)

def words_v(lines):   # our Devanagari, without daṇḍas and numbers
    return ' '.join(re.sub(r'[।॥|,0-9०-९]', ' ', ' '.join(lines)).split())
def words_t(lines):
    return deva(' '.join(re.sub(r'[।॥|,0-9]', ' ', ' '.join(lines)).split()))

bad = 0
for x in ITEMS:   # step 3
    a, b = words_v(x['v']), words_t(x['t'])
    if a != b: bad += 1; print('t ≠ v', x['id'], '\n  v:', a, '\n  t:', b)

# step 2: the printout's own transliteration, with the corrections recorded in reconciliation.md
EXPECTED = {   # item: [(printout, settled)]
    'shanti.1': [('pūrṇamevāvaśiṣyate', 'pūrṇamevāvaśiṣyate oṁ śāntiḥ śāntiḥ śāntiḥ')],
    'm08': [('asnāviraṁśuddham apāpaviddham', 'asnāviraṁ śuddhamapāpaviddham'), ('syayambhūr', 'svayambhūr')],
    'm09': [('tamoya u', 'tamo ya u')],
}
if len(sys.argv) > 1:
    import pymupdf
    doc = pymupdf.open(sys.argv[1])
    lines = [l.strip() for p in doc for l in p.get_text().split('\n')]
    lat = [unicodedata.normalize('NFC', l) for l in lines if (re.search(r'[āīūṛṣṇśṃḥ]', l) or re.fullmatch(r'\d+ \|\|', l)) and not re.search(r'[ऀ-ॿ()–=]', l)]
    # the verse lines: from "oṃ | pūrṇamadaḥ" on, each line ends in |, || or a number; a lone "16 ||" continues the line above
    start = next(i for i, l in enumerate(lat) if l.startswith('oṃ | pūrṇamadaḥ'))
    # A verse's first line ends in a single |; a line ending in a letter is a wrapped continuation (outside a
    # verse it is other text, e.g. the Vārtika quoted on page 5); a verse closes with || N || (the śānti with ||).
    verses, cur = [], []
    for l in lat[start:]:
        if re.search(r'(^|[^|])\|$', l): cur = [l]; continue
        if not cur: continue
        cur.append(l)
        if re.search(r'\d+ \|\|$', l) or (not verses and l.endswith('||')): verses.append(cur); cur = []
        if len(verses) == 19: break
    assert len(verses) == 19, [v[0][:25] for v in verses]
    for x, pv in zip(ITEMS, verses):
        page = ' '.join(re.sub(r'\|+|\d+', ' ', ' '.join(pv)).split()).replace('ṃ', 'ṁ').replace("'", '’')
        for old, new in EXPECTED.get(x['id'], []):
            assert old in page, (x['id'], old); page = page.replace(old, new)
        a, b = words_v(x['v']), deva(page)
        if a != b: bad += 1; print('printout ≠ text.json', x['id'], '\n  text.json:', a, '\n  printout: ', b)
    print('compared with the printout:', len(verses), 'verses')
print('OK' if not bad else '%d differences' % bad); sys.exit(1 if bad else 0)
