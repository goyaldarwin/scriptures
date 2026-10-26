"""Kaṭha Upaniṣad: source/pdf_raw.json (the owner's PDF, see extract.py) → ../text.json (the settled text).

The PDF's Devanagari layer is unreadable (legacy font), its IAST transliteration is clean. The Devanagari is
therefore made from the transliteration (iast2deva: a letter-for-letter conversion, no guessing), in the
library's daṇḍas (॥), and ../check.py compares it with the Devanagari witnesses in witness/,
see ../reconciliation.md. The transliteration is made by the exporter (tools/text/standard.py).

Items: shanti.1 (the opening śānti), 1.1.1 … 2.3.18 (adhyāya.vallī.mantra, the standard numbering: 29+25+17 and
15+15+18 = 119 mantras). The closing śānti the book prints as "2.3.19" is left out. Sections (pages) are the vallīs.
Run: python3 settle.py   (then ../export.py)
"""
import json, os, re
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
        elif w == '||': out.append('॥')
        else: out.append(iast2deva_word(w.rstrip('|')) + (' ।' if w.endswith('|') else ''))
    return ' '.join(out)

# ---- Devanagari → IAST (as tools/works/shri-rudram/source/settle.py, without svaras) ----
CONS = dict(zip('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह',
    'k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh m y r l v ś ṣ s h'.split()))
VOW = dict(zip('अआइईउऊऋॠऌएऐओऔ', 'a ā i ī u ū ṛ ṝ ḷ e ai o au'.split()))
MAT = dict(zip('ािीुूृॄॢेैोौ', 'ā i ī u ū ṛ ṝ ḷ e ai o au'.split()))
DIG = dict(zip('०१२३४५६७८९', '0123456789'))
# ---- corrections to the book's reading, each checked against the Devanagari witnesses (../reconciliation.md) ----
FIX = {   # item: [(book, settled)]; each must occur exactly once in the item's text
    '1.1.26': [('जरयंति', 'जरयन्ति')],                      # the book's jarayaṃti; the text has the dental न्
    '1.2.15': [('तपांसि', 'तपाꣳसि'), ('पदं', 'पदꣳ'), ('संग्रहेण', 'सङ्ग्रहेण')],   # ꣳ before a sibilant, ङ् before ग, as the Devanagari witness writes
    '1.2.23': [('तनूं', 'तनूꣳ')],
    '1.3.3': [('रथितं', 'रथिनं')],                          # rathinam (rathin, the lord of the chariot); the book's rathitaṃ is a slip
    '2.1.3': [('स्पर्शांश्च', 'स्पर्शाꣳश्च')],
    '2.2.2': [('वसुरान्तरिक्षसद्', 'वसुरन्तरिक्षसद्')],      # vasur antarikṣasat (Ṛgveda 4.40.5); the book's -rā- is a slip
    '2.3.2': [('किंच', 'किं च')],                            # two words, as the witness divides them
}

DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))
VALLI = [('1', '1', 29), ('1', '2', 25), ('1', '3', 17), ('2', '1', 15), ('2', '2', 15), ('2', '3', 18)]

def item(id_, p, s, y, n, lines):
    v = [l.strip() for l in lines if l.strip()]
    return {'id': id_, 'p': p, 's': s, 'y': y, 'n': n, 'v': v}

def main():
    R = json.load(open(os.path.join(HERE, 'pdf_raw.json'), encoding='utf-8'))
    sh = [iast2deva(l) for l in R['shanti']['t']]
    assert sh[0].startswith('ॐ') and sh[-1].endswith('॥'), sh
    items = [item('shanti.1', 0, 'shanti', 'shanti', '', sh)]
    for a, va, cnt in VALLI:
        for m in range(1, cnt + 1):
            vid = '%s.%s.%d' % (a, va, m)
            lines = [iast2deva(l) for l in R[vid]['t']]
            for wrong, right in FIX.get(vid, []):
                assert sum(l.count(wrong) for l in lines) == 1, (vid, wrong)
                lines = [l.replace(wrong, right) for l in lines]
            assert lines and not lines[-1].endswith('।'), (vid, lines)   # the last line carries no bar: the number goes there
            lines[-1] += ' ॥%s॥' % DEV(m)
            items.append(item(vid, int(a) - 1, 'v%s.%s' % (a, va), 'mantra', vid, lines))
    assert len(items) == 120, len(items)   # the work ends with 2.3.18: no closing śānti
    json.dump({'items': items}, open(os.path.join(HERE, '..', 'text.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(items), 'items')

if __name__ == '__main__':
    main()
