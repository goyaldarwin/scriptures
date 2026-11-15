"""Muṇḍaka Upaniṣad: source/mundaka-upanishad_raw.json (the shlokam.org page, see extract.py) → ../text.txt (the settled text).

The page's Devanagari is the base. Its own transliteration is the second witness: every Devanagari line is read back
from it (deva_of) and the two must agree letter for letter before anything is changed; they do on every line, so the
page's slips below are in both scripts and are corrected on the page's own word-by-word lists (the Devanagari headwords),
the grammar and the metre (../reconciliation.md). The page has no svara marks, so neither does the text. The
transliteration is made by the exporter (tools/text/standard.py).

Items: shanti.1 (the śānti), 1.1.1 … 3.2.10 (ids and citations muṇḍaka.khaṇḍa.mantra; n is the mantra's number in its
khaṇḍa, as printed), and the closing words of each khaṇḍa the page prints (1.1.iti …). Parts are the three muṇḍakas,
sections (pages) the six khaṇḍas.
Run: python3 settle.py   (then python3 tools/works/export.py mundaka-upanishad)
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile

# ---- the page's ISO 15919 transliteration → Devanagari, letter for letter (for the witness check only) ----
V = {'a': '', 'ā': 'ा', 'i': 'ि', 'ī': 'ी', 'u': 'ु', 'ū': 'ू', 'ṛ': 'ृ', 'ṝ': 'ॄ', 'e': 'े', 'ai': 'ै', 'o': 'ो', 'au': 'ौ'}
IV = {'a': 'अ', 'ā': 'आ', 'i': 'इ', 'ī': 'ई', 'u': 'उ', 'ū': 'ऊ', 'ṛ': 'ऋ', 'ṝ': 'ॠ', 'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ'}
C = {'kh': 'ख', 'gh': 'घ', 'ch': 'छ', 'jh': 'झ', 'ṭh': 'ठ', 'ḍh': 'ढ', 'th': 'थ', 'dh': 'ध', 'ph': 'फ', 'bh': 'भ',
     'k': 'क', 'g': 'ग', 'ṅ': 'ङ', 'c': 'च', 'j': 'ज', 'ñ': 'ञ', 'ṭ': 'ट', 'ḍ': 'ड', 'ṇ': 'ण', 't': 'त', 'd': 'द', 'n': 'न',
     'p': 'प', 'b': 'ब', 'm': 'म', 'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'ś': 'श', 'ṣ': 'ष', 's': 'स', 'h': 'ह'}
TOK = sorted(list(V) + list(C), key=len, reverse=True)

def deva_of(line):
    out = []
    for w in line.split():
        if w == 'oṃ': out.append('ॐ'); continue
        r, i, prev_c = '', 0, False
        while i < len(w):
            if w.startswith('gͫ', i): r += 'ꣳ'; i += 2; prev_c = False; continue
            if w.startswith('m̐', i): r += ('्म' if prev_c else 'म') + 'ँ'; i += 2; prev_c = False; continue
            ch = w[i]
            if ch in "'’": r += 'ऽ'; i += 1; prev_c = False; continue
            if ch == 'ṃ': r += 'ं'; i += 1; prev_c = False; continue
            if ch == 'ḥ': r += 'ः'; i += 1; prev_c = False; continue
            t = next((t for t in TOK if w.startswith(t, i)), None)
            if t is None:
                if prev_c: r += '्'
                r += ch; i += 1; prev_c = False; continue
            if t in C:
                if prev_c: r += '्'
                r += C[t]; prev_c = True
            else:
                r += V[t] if prev_c else IV[t]; prev_c = False
            i += len(t)
        if prev_c: r += '्'
        out.append(r)
    return unicodedata.normalize('NFC', ' '.join(out))

def key(s):
    """For comparison: letters only (no spaces, hyphens, daṇḍas, full stops or digits); the page writes यस्मिँल् as yasmim̐l."""
    return re.sub(r'[\s\-.।॥|0-9०-९]', '', s).replace('म्ँ', 'ँ').replace('मँ', 'ँ')

# ---- corrections to the page, each in both its scripts (../reconciliation.md); each must occur exactly once in the item ----
FIX = {
    'shanti.1': [('श्रुणुयाम', 'शृणुयाम'), ('तुष्टुवाꣳसस्', 'तुष्टुवांसस्'), ('बृहस्पतिर्दधातु।', 'बृहस्पतिर्दधातु ॥'),
                 ('॥ ॐ शान्तिः शान्तिः शान्तिः ॥', 'ॐ शान्तिः शान्तिः शान्तिः ॥')],
    '1.1.2': [('ब्रह्माऽथर्वा तं', 'ब्रह्माऽथर्वा तां')],
    '1.1.9': [('ज्ञानमयं तापः', 'ज्ञानमयं तपः'), ('च जायाते', 'च जायते')],
    '1.2.9': [('अविद्यायं', 'अविद्यायां')],
    '2.1.4': [('अग्नीर्मूर्धा', 'अग्निर्मूर्धा')],
    '2.2.4': [('शारो ह्यात्मा', 'शरो ह्यात्मा')],
    '2.2.9': [('ज्योतिषं ज्योतिस्तद्', 'ज्योतिषां ज्योतिस्तद्')],
    '3.1.4': [('प्रणो ह्येष', 'प्राणो ह्येष')],
    '3.1.2': [('निमग्नोऽनिशया', 'निमग्नोऽनीशया')],
    '3.1.7': [('पश्यन्त्विहैव', 'पश्यत्स्विहैव')],
    '3.1.8': [('कर्मण वा', 'कर्मणा वा')],
    '3.1.10': [('ह्यर्चयेत् भूतिकामः', 'ह्यर्चयेद्भूतिकामः')],
    '3.2.5': [('वीतरागाः प्रशान्ताः', 'वीतरागाः प्रशान्ताः ।')],
    '3.2.8': [('समुद्रेऽ', 'समुद्रेऽ-')],
}
TITLE = 'मुण्डकोपनिषत्'          # the page's heading above the śānti, not part of it
ITI = re.compile(r'^॥ इति मुण्डकोपनिषदि \S+मुण्डके \S+ खण्डः ॥$')

def house(l):
    """The page's daṇḍas as the library writes them: the verse number inside ॥ without spaces (॥ १॥ → ॥१॥)."""
    return re.sub(r'\s*॥\s*([०-९]+)\s*॥', r' ॥\1॥', l).strip()

def witness_check(B):
    bad = []
    for b in B:
        for d, t in zip(b['v'], b['t']):
            if key(d) != key(deva_of(t.lower())): bad.append((b['ref'], d, t))
    assert not bad, '\n'.join('%s\n  page Devanagari: %s\n  its transliteration: %s' % x for x in bad)

def items(B):
    out, part = [], {'1': 0, '2': 1, '3': 2}
    for b in B:
        m, k, n = b['ref'].split('.'); lines = list(b['v'])
        if b['ref'] == '1.0.0':
            assert lines[0] == TITLE, lines[0]
            out.append({'id': 'shanti.1', 'p': 0, 's': 'shanti', 'y': 'shanti', 'n': '', 'v': lines[1:]}); continue
        iti = [l for l in lines if ITI.match(l)]
        lines = [l for l in lines if not ITI.match(l)]
        out.append({'id': b['ref'], 'p': part[m], 's': 'k%s.%s' % (m, k), 'y': 'mantra', 'n': n, 'v': lines})
        for l in iti: out.append({'id': '%s.%s.iti' % (m, k), 'p': part[m], 's': 'k%s.%s' % (m, k), 'y': 'iti', 'n': '', 'v': [l]})
    for x in out:
        for a, b_ in FIX.get(x['id'], []):
            assert sum(l.count(a) for l in x['v']) == 1, (x['id'], a)
            x['v'] = [l.replace(a, b_) for l in x['v']]
        x['v'] = [house(l) for l in x['v']]
        if x['y'] == 'mantra': assert x['v'][-1].endswith('॥%s॥' % ''.join('०१२३४५६७८९'[int(c)] for c in x['n'])), (x['id'], x['v'][-1])
    return out

TOPICS = [
    ('shanti.1', 'शान्तिपाठ', 'Shanti Paath'),
    ('1.1.1', 'प्रथम मुण्डक, प्रथम खण्ड — शौनकका प्रश्न; परा और अपरा विद्या', 'Mundaka 1, Khanda 1 — Shaunaka’s question; the higher and the lower knowledge'),
    ('1.2.1', 'प्रथम मुण्डक, द्वितीय खण्ड — यज्ञकर्मकी सीमा; गुरुकी शरण', 'Mundaka 1, Khanda 2 — The limits of ritual; going to a teacher'),
    ('2.1.1', 'द्वितीय मुण्डक, प्रथम खण्ड — अक्षर पुरुषसे सारी सृष्टि', 'Mundaka 2, Khanda 1 — All creation from the imperishable Person'),
    ('2.2.1', 'द्वितीय मुण्डक, द्वितीय खण्ड — ॐ धनुष, आत्मा बाण, ब्रह्म लक्ष्य', 'Mundaka 2, Khanda 2 — Om the bow, the self the arrow, Brahman the target'),
    ('3.1.1', 'तृतीय मुण्डक, प्रथम खण्ड — एक वृक्षपर दो पक्षी; सत्यमेव जयते', 'Mundaka 3, Khanda 1 — Two birds on one tree; truth alone prevails'),
    ('3.2.1', 'तृतीय मुण्डक, द्वितीय खण्ड — नदियाँ समुद्रमें; ब्रह्मवेत्ता ब्रह्म ही', 'Mundaka 3, Khanda 2 — Rivers into the sea; the knower of Brahman is Brahman'),
]

if __name__ == '__main__':
    B = json.load(open(os.path.join(HERE, 'mundaka-upanishad_raw.json'), encoding='utf-8'))
    witness_check(B)
    I = items(B)
    ids = [x['id'] for x in I]; assert len(ids) == len(set(ids))
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, [{'id': a, 'hi': h, 'en': e} for a, h, e in TOPICS], ['1', '2', '3'], 'sa', [
        'Muṇḍaka Upaniṣad: the śānti mantra, mantras 1.1.1 … 3.2.10 and the closing words of each khaṇḍa. Made by source/settle.py',
        'from the shlokam.org page; do not edit here. Every correction and choice: reconciliation.md.'])
    print(sum(x['y'] == 'mantra' for x in I), 'mantras,', len(I), 'items')
