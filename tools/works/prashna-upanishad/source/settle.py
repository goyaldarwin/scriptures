"""Praśna Upaniṣad: source/page_raw.json (shlokam.org's page, see extract.py) → ../text.txt (the settled text).

The Devanagari is the page's own. Two witnesses settle it (../reconciliation.md):
  1. the page's own transliteration, converted back to Devanagari (tr2deva) and compared word by word with the page's
     Devanagari; the comparison folds only the writing standard's conventions (standard.fold: a class nasal or ꣳ as ं).
     Every difference must be one listed in TRANSLIT (where the two halves of the page disagree), or the run fails;
  2. the corrections in FIX: the page's slips, each settled in ../reconciliation.md (some by the grammar alone, some on
     the independent witnesses that check.py compares the text with).
Then: each praśna's closing words (इति प्रश्नोपनिषदि … प्रश्नः) become an item of their own, the page's numbers ॥ १.१॥
are written as the mantra's own number (॥१॥), and the opening śānti is laid out as the Māṇḍūkya's, which it must equal.
The transliteration is made by the exporter (tools/text/standard.py).

Items: shanti.1, then 1.1 … 6.8 (praśna.mantra; n is the mantra's number in its praśna, as the page prints it:
16 + 13 + 12 + 11 + 7 + 8 = 67 mantras) and 1.iti … 6.iti. Parts are the six praśnas, each one section (page).
Run: python3 settle.py   (then python3 tools/works/export.py prashna-upanishad)
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); WORKS = os.path.join(HERE, '..', '..')
sys.path.insert(0, WORKS); import textfile
sys.path.insert(0, os.path.join(WORKS, '..', 'text')); import standard

COUNT = {1: 16, 2: 13, 3: 12, 4: 11, 5: 7, 6: 8}
DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))
ORD = ['प्रथमः', 'द्वितीयः', 'तृतीयः', 'चतुर्थः', 'पञ्चमः', 'षष्ठः']

def norm(s):
    """The page's Devanagari as text: NFC, no zero-width space (U+200B) or joiner (U+200D: श‍ृ is शृ), single spaces."""
    s = unicodedata.normalize('NFC', s).replace('​', '').replace('‍', '')
    return re.sub(r'\s+', ' ', s).strip()

# ---- the page's transliteration → Devanagari (the second witness; no svaras: the page has none) ----
V = {'a': '', 'ā': 'ा', 'i': 'ि', 'ī': 'ी', 'u': 'ु', 'ū': 'ू', 'ṛ': 'ृ', 'ṝ': 'ॄ', 'e': 'े', 'ai': 'ै', 'o': 'ो', 'au': 'ौ'}
IV = {'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ', 'ṛ': 'ऋ', 'ṝ': 'ॠ', 'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ'}
C = {'kh': 'ख', 'gh': 'घ', 'ch': 'छ', 'jh': 'झ', 'ṭh': 'ठ', 'ḍh': 'ढ', 'th': 'थ', 'dh': 'ध', 'ph': 'फ', 'bh': 'भ',
     'k': 'क', 'g': 'ग', 'ṅ': 'ङ', 'c': 'च', 'j': 'ज', 'ñ': 'ञ', 'ṭ': 'ट', 'ḍ': 'ड', 'ṇ': 'ण', 't': 'त', 'd': 'द', 'n': 'न',
     'p': 'प', 'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'ś': 'श', 'ṣ': 'ष', 's': 'स', 'h': 'ह'}
TOK = sorted(list(V) + list(C), key=len, reverse=True)

def tr2deva_word(w):
    if w == 'oṃ': return 'ॐ'
    r, i, prev_c = '', 0, False
    while i < len(w):
        if w.startswith('gͫ', i): r += 'ꣳ'; i += 2; prev_c = False; continue
        ch = w[i]
        if ch in "'’": r += 'ऽ'; i += 1; prev_c = False; continue
        if ch in 'ṁṃ': r += 'ं'; i += 1; prev_c = False; continue
        if ch == 'ḥ': r += 'ः'; i += 1; prev_c = False; continue
        if ch == '-': r += '-'; i += 1; continue
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

def words(s, latin=False):
    """A line's words, without daṇḍas and numbers, folded by the writing standard."""
    s = re.sub(r'[.।॥|0-9०-९]', ' ', s)
    return [standard.fold(tr2deva_word(w) if latin else w) for w in s.split()]

# ---- where the page's transliteration spells a word otherwise than its Devanagari: (verse, Devanagari, transliteration) ----
TRANSLIT = []

# ---- corrections of the page's slips (../reconciliation.md); each must occur exactly once in the verse ----
FIX = {   # (praśna, verse): [(page, settled)]
    (1, 0): [('स्थिरैरङ्गैस्तुष्तुवाꣳसस्', 'स्थिरैरङ्गैस्तुष्टुवांसस्')],
    (1, 3): [('भगवन् कुते ह', 'भगवन् कुतो ह')],
    (1, 12): [('शुक्लः प्रणस्', 'शुक्लः प्राणस्')],
    (2, 4): [('तस्मिंष्च', 'तस्मिंश्च'), ('प्रातिष्टन्त', 'प्रातिष्ठन्त'), ('वाङ्मनष्चक्षुः', 'वाङ्मनश्चक्षुः'),
             ('सर्व एवोत्क्रमन्ते', 'सर्वा एवोत्क्रमन्ते'), ('सर्व एव प्रातिष्ठन्त', 'सर्वा एव प्रातिष्ठन्त')],
    (2, 11): [('प्राणैकर्षरत्ता', 'प्राणैकर्षिरत्ता')],
    (3, 1): [('कौशल्यश्चाश्वलायनः', 'कौसल्यश्चाश्वलायनः')],
    (3, 4): [('सम्रादेवाधिकृतान्', 'सम्राडेवाधिकृतान्'), ('एतन् ग्रामानोतान्', 'एतान् ग्रामानेतान्')],
    (3, 10): [('तथासङ्कल्पितं', 'यथासङ्कल्पितं')],
    (3, 11): [('तदेषः श्लोकः', 'तदेष श्लोकः')],
    (4, 1): [('सौर्यायणि', 'सौर्यायणी')],
    (4, 6): [('यदैतस्मिञ्शरीर', 'तदैतस्मिञ्शरीर')],
    (4, 7): [('सोभ्य', 'सोम्य'), ('वसोवृक्षं', 'वासोवृक्षं')],
    (4, 8): [('यादौ च गन्तव्यं', 'पादौ च गन्तव्यं')],
    (5, 4): [('विभुतिमनुभूय', 'विभूतिमनुभूय')],
    (5, 5): [('पुरुषमभि-\nध्यायीत स तेजसि', 'पुरुषमभिध्यायीत\nस तेजसि')],
    (5, 6): [('अन्योन्यसक्ताः', 'अन्योन्यसक्ता')],
    (6, 1): [('नार्हम्यनृतं', 'नार्हाम्यनृतं')],
    (6, 2): [('यस्मिन्नताः', 'यस्मिन्नेताः')],
    (6, 3): [('ईक्षाचक्रे', 'ईक्षांचक्रे')],
    (6, 4): [('नाम च\n॥ ६.४॥', 'नाम च ॥ ६.४॥')],
    (6, 6): [('वेद यथ मा', 'वेद यथा मा')],
}

def compare(B):
    """The page's Devanagari against its own transliteration; returns the differences not listed in TRANSLIT."""
    bad = []
    for b in B:
        assert len(b['v']) == len(b['t']), (b['prashna'], b['verse'])
        for dv, tr in zip(b['v'], b['t']):
            a, c = words(norm(dv)), words(tr, latin=True)
            if a == c: continue
            for x, y in zip(a, c):
                if x != y and ((b['prashna'], b['verse']), x, y) not in TRANSLIT: bad.append(((b['prashna'], b['verse']), x, y))
            if len(a) != len(c): bad.append(((b['prashna'], b['verse']), ' '.join(a), ' '.join(c)))
    return bad

def house(l):
    """The page's ॥ १.१॥ (praśna.mantra) as the library writes a mantra's own number: ॥१॥."""
    return re.sub(r'\s*॥\s*[०-९]+\.([०-९]+)\s*॥$', r' ॥\1॥', l).strip()

def mandukya_shanti():
    M = textfile.read(os.path.join(WORKS, 'mandukya-upanishad', 'text.txt'))
    return next(x['v'] for x in M if x['id'] == 'shanti.1')

def main():
    B = json.load(open(os.path.join(HERE, 'page_raw.json'), encoding='utf-8'))
    bad = compare(B)
    for d in bad: print('Devanagari ≠ transliteration', d)
    assert not bad, '%d differences between the page\'s Devanagari and its transliteration' % len(bad)
    assert [(b['prashna'], b['verse']) for b in B] == [(1, 0)] + [(p, m) for p in COUNT for m in range(1, COUNT[p] + 1)]
    items, used = [], set()
    for b in B:
        p, m = b['prashna'], b['verse']
        text = '\n'.join(norm(l) for l in b['v'])
        for wrong, right in FIX.get((p, m), []):
            assert text.count(wrong) == 1, (p, m, wrong)
            text = text.replace(wrong, right); used.add((p, m, wrong))
        text = text.replace('ꣳ', 'ं')   # ꣳ belongs to the Yajurveda's recitation; this is the Atharvaveda (PLAYBOOK §3)
        lines = text.split('\n')
        if m == 0:
            # the opening śānti, in the Māṇḍūkya's lines (the same mantra of the Atharvaveda's Upaniṣads)
            sh = [lines[0] + ' ' + lines[1], lines[2][:-1].rstrip() + ' ।', lines[3] + ' ' + lines[4], lines[5] + ' ' + lines[6], lines[7]]
            assert sh == mandukya_shanti(), (sh, mandukya_shanti())
            items.append({'id': 'shanti.1', 'p': 0, 's': 'shanti', 'y': 'shanti', 'n': '', 'v': sh}); continue
        iti = None
        if m == COUNT[p]:
            iti = lines.pop()
            assert iti == 'इति प्रश्नोपनिषदि %s प्रश्नः ॥' % ORD[p - 1], iti
        assert re.search(r'॥ %s\.%s॥$' % (DEV(p), DEV(m)), lines[-1]), (p, m, lines[-1])
        lines = [house(l) for l in lines]
        items.append({'id': '%d.%d' % (p, m), 'p': p - 1, 's': 'p%d' % p, 'y': 'mantra', 'n': str(m), 'v': lines})
        if iti: items.append({'id': '%d.iti' % p, 'p': p - 1, 's': 'p%d' % p, 'y': 'iti', 'n': '', 'v': [iti]})
    assert len(used) == sum(len(f) for f in FIX.values())
    assert len(items) == 1 + 67 + 6, len(items)
    TOPICS = [
        {'id': 'shanti.1', 'hi': 'शान्तिपाठ', 'en': 'Shanti Paath'},
        {'id': '1.1', 'hi': 'प्रथम प्रश्न — प्रजा कहाँसे उत्पन्न होती है: रयि और प्राण', 'en': 'Prashna 1 — Where do creatures come from: matter and life'},
        {'id': '2.1', 'hi': 'द्वितीय प्रश्न — इन्द्रियोंमें प्राण सबसे श्रेष्ठ', 'en': 'Prashna 2 — Prana, the greatest of the powers'},
        {'id': '3.1', 'hi': 'तृतीय प्रश्न — प्राणका जन्म, शरीरमें आना और बँटना', 'en': 'Prashna 3 — How prana is born, enters the body and divides itself'},
        {'id': '4.1', 'hi': 'चतुर्थ प्रश्न — स्वप्न, गहरी नींद और अक्षर आत्मा', 'en': 'Prashna 4 — Dream, deep sleep and the imperishable Self'},
        {'id': '5.1', 'hi': 'पञ्चम प्रश्न — ओंकारका ध्यान', 'en': 'Prashna 5 — Meditation on Om'},
        {'id': '6.1', 'hi': 'षष्ठ प्रश्न — सोलह कलाओंवाला पुरुष', 'en': 'Prashna 6 — The Person of sixteen parts'},
    ]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, TOPICS, ['1', '2', '3', '4', '5', '6'], 'sa', [
        'Praśna Upaniṣad: the śānti mantra, the six praśnas (mantras 1.1 … 6.8) and their closing words. Made by',
        'source/settle.py from shlokam.org\'s page; do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(items), 'items')

if __name__ == '__main__':
    main()
