"""Kaṭha Upaniṣad: source/pdf_raw.json (the owner's PDF, see extract.py) → ../text.json (the settled text).

The PDF's Devanagari layer is unreadable (legacy font), its IAST transliteration is clean. The Devanagari is
therefore made from the transliteration (iast2deva: a letter-for-letter conversion, no guessing), in the
library's house style, and ../check.py compares it with a Devanagari witness (shlokam.org / sanskritdocuments.org),
see ../reconciliation.md. The transliteration `t` is made back from the settled Devanagari (deva2iast), in
the library's IAST convention (ṁ, ’ for the avagraha, ॥ and the number as in the other works).

Items: shanti.1 (the opening śānti), 1.1.1 … 2.3.18 (adhyāya.vallī.mantra, the standard numbering: 29+25+17 and
15+15+18 = 119 mantras), shanti.2 (the closing śānti, the author's "2.3.19"). Sections (pages) are the vallīs.
Run: python3 settle.py   (then ../export.py)
"""
import json, os, re, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- IAST → Devanagari ----
V = {'a': '', 'ā': 'ा', 'i': 'ि', 'ī': 'ी', 'u': 'ु', 'ū': 'ू', 'ṛ': 'ृ', 'ṝ': 'ॄ', 'e': 'े', 'ai': 'ै', 'o': 'ो', 'au': 'ौ'}
IV = {'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ', 'ṛ': 'ऋ', 'ṝ': 'ॠ', 'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ'}
C = {'kh': 'ख', 'gh': 'घ', 'ch': 'छ', 'jh': 'झ', 'ṭh': 'ठ', 'ḍh': 'ढ', 'th': 'थ', 'dh': 'ध', 'ph': 'फ', 'bh': 'भ',
     'k': 'क', 'g': 'ग', 'ṅ': 'ङ', 'c': 'च', 'j': 'ज', 'ñ': 'ञ', 'ṭ': 'ट', 'ḍ': 'ड', 'ṇ': 'ण', 't': 'त', 'd': 'द', 'n': 'न',
     'p': 'प', 'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'ś': 'श', 'ṣ': 'ष', 's': 'स', 'h': 'ह'}
TOK = sorted(list(V) + list(C), key=len, reverse=True)

def iast2deva_word(w):
    if w == 'om̐' or w == 'oṃ': return 'ॐ'
    if w.endswith('-'): return iast2deva_word(w[:-1]) + '-'     # a word broken at the line end
    r, i, prev_c = '', 0, False
    while i < len(w):
        ch = w[i]
        if ch in "'’": r += 'ऽ'; i += 1; prev_c = False; continue
        if ch in 'ṁṃ': r += 'ं'; i += 1; prev_c = False; continue
        if w.startswith('m̐', i): r += 'ँ'; i += 2; prev_c = False; continue
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
    return r

def iast2deva(line):
    out = []
    for w in line.replace(',', '').split():   # the author's two commas (1.1.1, 1.3.14) are not part of the text
        if w == '|': out.append('।')
        elif w == '||': out.append('।।')
        else: out.append(iast2deva_word(w.rstrip('|')) + (' ।' if w.endswith('|') else ''))
    return ' '.join(out)

# ---- Devanagari → IAST (as tools/works/shri-rudram/source/settle.py, without svaras) ----
CONS = dict(zip('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह',
    'k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh m y r l v ś ṣ s h'.split()))
VOW = dict(zip('अआइईउऊऋॠऌएऐओऔ', 'a ā i ī u ū ṛ ṝ ḷ e ai o au'.split()))
MAT = dict(zip('ािीुूृॄॢेैोौ', 'ā i ī u ū ṛ ṝ ḷ e ai o au'.split()))
DIG = dict(zip('०१२३४५६७८९', '0123456789'))
def deva2iast(s):
    out = []; pend = False
    for c in s:
        if c in CONS:
            if pend: out.append('a')
            out.append(CONS[c]); pend = True
        elif c == '्': pend = False
        elif c in MAT: out.append(MAT[c]); pend = False
        elif c in VOW:
            if pend: out.append('a'); pend = False
            out.append(VOW[c])
        else:
            if pend: out.append('a'); pend = False
            if c == 'ं': out.append('ṁ')
            elif c == 'ः': out.append('ḥ')
            elif c == 'ँ': out.append('̐')
            elif c == 'ऽ': out.append('’')
            elif c == 'ॐ': out.append('oṁ')
            elif c in DIG: out.append(DIG[c])
            else: out.append(c)
    if pend: out.append('a')
    t = unicodedata.normalize('NFC', ''.join(out))
    t = re.sub(r'\s*।।(\d+)।।', r' ॥\1॥', t)
    t = re.sub(r'\s*।।', ' ॥', t)
    t = re.sub(r'\s*।\s*$', ',', t)
    t = re.sub(r'\s*।\s*', ', ', t)
    return t.strip()

DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))
VALLI = [('1', '1', 29), ('1', '2', 25), ('1', '3', 17), ('2', '1', 15), ('2', '2', 15), ('2', '3', 18)]

def item(id_, p, s, y, n, lines):
    v = [l.strip() for l in lines if l.strip()]
    return {'id': id_, 'p': p, 's': s, 'y': y, 'n': n, 'v': v, 't': [deva2iast(l) for l in v]}

def main():
    R = json.load(open(os.path.join(HERE, 'pdf_raw.json'), encoding='utf-8'))
    sh = [iast2deva(l) for l in R['shanti']['t']]
    assert sh[0].startswith('ॐ') and sh[-1].endswith('।।'), sh
    items = [item('shanti.1', 0, 'shanti', 'shanti', '', sh)]
    for a, va, cnt in VALLI:
        for m in range(1, cnt + 1):
            vid = '%s.%s.%d' % (a, va, m)
            lines = [iast2deva(l) for l in R[vid]['t']]
            assert lines and not lines[-1].endswith('।'), (vid, lines)   # the last line carries no bar: the number goes there
            lines[-1] += ' ।।%s।।' % DEV(m)
            items.append(item(vid, int(a) - 1, 'v%s.%s' % (a, va), 'mantra', vid, lines))
    items.append(item('shanti.2', 1, 'shanti2', 'shanti', '', sh))
    assert len(items) == 121, len(items)
    json.dump({'items': items}, open(os.path.join(HERE, '..', 'text.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(items), 'items')

if __name__ == '__main__':
    main()
