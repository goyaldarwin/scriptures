"""Kena Upaniṣad: source/pdf_raw.json (the owner's PDF, see extract.py) → ../text.txt (the settled text).

The PDF's Devanagari layer is unreadable (legacy font), its IAST transliteration is clean. The Devanagari is
therefore made from the transliteration (iast2deva: a letter-for-letter conversion, no guessing; the Kaṭha's,
tools/works/katha-upanishad/source/settle.py, with the pluta ३ this text has), in the library's daṇḍas (॥), and
check.py compares it with the Devanagari witnesses in witness/, see ../reconciliation.md. The transliteration is made
by the exporter (tools/text/standard.py).

Items: shanti.1 (the Sāmaveda's śānti, आप्यायन्तु, as the book prints it before the text), 1.1 … 4.9 (ids and
citations khaṇḍa.mantra; n is the mantra's number in its khaṇḍa, as the book prints it: 8 + 5 + 12 + 9 = 34 mantras,
the book's 1.3 in two halves kept as one mantra), and each khaṇḍa's closing words, 1.iti … 4.iti (the fourth's with
the Upaniṣad's). Parts and sections (pages) are the khaṇḍas.
Run: python3 settle.py   (then ../export.py)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile

# ---- IAST → Devanagari (the Kaṭha's) ----
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
    for w in line.replace(',', '').split():   # the author's commas (3.1, 4.1, 4.6) are not part of the text
        if w == '|': out.append('।')
        elif w == '||': out.append('॥')
        elif w.rstrip('*') == '3': out[-1] += '३'   # the pluta (4.4 व्यद्युतदा३, न्यमीमिषदा३); * marks the book's footnote
        else: out.append(iast2deva_word(w.rstrip('|')) + (' ।' if w.endswith('|') else ''))
    return ' '.join(out)

# ---- corrections to the book's reading, each checked against the book's own Devanagari and the witnesses (../reconciliation.md) ----
FIX = {   # item: [(book, settled)]; each must occur exactly once in the item's text
    'shanti.1': [('धर्माह्', 'धर्माः')],                    # the IAST's dharmāh; the book's Devanagari has धर्माः
    '2.1': [('मीमाँस्येमेव', 'मीमाँस्यमेव')],              # mīmāṃsyam eva; the book's -sye- is a broken form
    '3.5': [('तस्मिन्स्त्वयि', 'तस्मिंस्त्वयि')],            # the IAST's tasminstvayi; the book's Devanagari has तस्मिंस्त्वयि
    '3.10': [('शशाकादतुं', 'शशाकादातुं')],                # ādātum, to take (ā-dā); the book's ādatum is a broken form
    '4.2': [('पस्पर्शुह्', 'पस्पर्शुः'), ('विदाञ्', 'विदाञ्-')],   # the IAST's pasparśuh (the Devanagari has ः); विदाञ्-/चकार broken at the line end
    '4.3': [('विदाञ्', 'विदाञ्-')],
    '4.5': [('यद्देतद्', 'यदेतद्')],                       # yad etad; the book's yaddetad is no sandhi of any words
    '4.8': [('तसै', 'तस्यै')],                             # the IAST's tasai; the book's Devanagari has तस्यै
    '4.9': [('प्रतितिष्ठतेएति', 'प्रतितिष्ठतीति')],         # the IAST's pratitiṣṭhateeti; the book's Devanagari has प्रतितिष्ठतीति
}
MID = {'1.3': 1}   # a line the book ends without a daṇḍa that takes one: the end of the first half of 1.3 (its 1.3.1)

DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))
KHANDA = [(1, 8), (2, 5), (3, 12), (4, 9)]
ORD = {1: 'प्रथमः', 2: 'द्वितीयः', 3: 'तृतीयः', 4: 'चतुर्थः'}

def item(id_, p, s, y, n, lines):
    v = [l.strip() for l in lines if l.strip()]
    return {'id': id_, 'p': p, 's': s, 'y': y, 'n': n, 'v': v}

def fix(vid, lines):
    for wrong, right in FIX.get(vid, []):
        assert sum(l.count(wrong) for l in lines) == 1, (vid, wrong)
        lines = [l.replace(wrong, right) for l in lines]
    return lines

def main():
    R = json.load(open(os.path.join(HERE, 'pdf_raw.json'), encoding='utf-8'))
    sh = fix('shanti.1', [iast2deva(l) for l in R['shanti']['t']])
    assert sh[0].startswith('ॐ आप्यायन्तु') and sh[-1] == 'ॐ शान्तिः शान्तिः शान्तिः ॥', sh
    items = [item('shanti.1', 0, 'shanti', 'shanti', '', sh)]
    for k, cnt in KHANDA:
        for m in range(1, cnt + 1):
            vid = '%d.%d' % (k, m)
            lines = fix(vid, [iast2deva(l) for l in R[vid]['t']])
            if vid in MID: assert not lines[MID[vid]].endswith('।'); lines[MID[vid]] += ' ।'
            lines[-1] = re.sub(r'\s*।$', '', lines[-1]) + ' ॥%s॥' % DEV(m)    # the number ends the last line (3.1's bar goes)
            items.append(item(vid, k - 1, 'k%d' % k, 'mantra', str(m), lines))   # n: the mantra's number in its khaṇḍa, as printed; cited khaṇḍa.mantra (work.json → cite)
        iti = [iast2deva(l) + ' ॥' for l in R['iti'][str(k)]]
        assert iti[0] == 'इति केनोपनिषदि %s खण्डः ॥' % ORD[k], iti
        items.append(item('%d.iti' % k, k - 1, 'k%d' % k, 'iti', '', iti))
    assert len(items) == 1 + 34 + 4, len(items)
    TOPICS = [
     {"id": "shanti.1", "hi": "शान्तिपाठ", "en": "Shanti Paath"},
     {"id": "1.1", "hi": "प्रथम खण्ड — मन, प्राण, वाणीको कौन चलाता है; कानका कान, मनका मन",
      "en": "Khanda 1 — Who moves the mind, breath and speech; the ear of the ear, the mind of the mind"},
     {"id": "2.1", "hi": "द्वितीय खण्ड — जो जाननेका दावा करता है वह नहीं जानता",
      "en": "Khanda 2 — The one who claims to know does not know"},
     {"id": "3.1", "hi": "तृतीय खण्ड — देवताओंका अभिमान और यक्ष",
      "en": "Khanda 3 — The pride of the gods and the mysterious being (yaksha)"},
     {"id": "4.1", "hi": "चतुर्थ खण्ड — उमाका उपदेश; ब्रह्मकी उपासना",
      "en": "Khanda 4 — Uma's teaching; meditation on Brahman"},
    ]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, TOPICS, ['1', '2', '3', '4'], 'sa', [
        'Kena Upaniṣad: the śānti mantra, mantras 1.1 … 4.9 and the closing words of each khaṇḍa. Made by source/settle.py',
        'from the owner\'s book; do not edit here. Every correction and choice: reconciliation.md; source/check.py compares it',
        'with the Devanagari witnesses.'])
    print(len(items), 'items')

if __name__ == '__main__':
    main()
