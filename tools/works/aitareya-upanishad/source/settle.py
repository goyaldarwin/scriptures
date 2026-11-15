"""Aitareya Upaniṣad: source/pdf_raw.json (the owner's PDF, see extract.py) → ../text.txt (the settled text).

As for the Kaṭha (same series, same typesetting): the book's IAST is converted letter for letter to Devanagari with the
Kaṭha's iast2deva (tools/works/katha-upanishad/source/settle.py), the corrections below are applied, each checked
against the witnesses (check.py, ../reconciliation.md), and the exporter makes the transliteration.

Items: shanti.1 (the Ṛgveda śānti वाङ् मे मनसि, which the book prints once, at the end, as its chapter 6; here it opens
the work, as the library's Upaniṣads do), then the 33 mantras 1.1.1 … 3.1.4 (ids and citations adhyāya.khaṇḍa.mantra,
the standard numbering; n is the mantra's number in its khaṇḍa: 4+5+14, 6, 4). Sections (pages) are the khaṇḍas.
Run: python3 settle.py   (then ../check.py, ../../export.py aitareya-upanishad)
"""
import importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
_k = importlib.util.spec_from_file_location('katha_settle', os.path.join(HERE, '..', '..', 'katha-upanishad', 'source', 'settle.py'))
katha = importlib.util.module_from_spec(_k); _k.loader.exec_module(katha)

DEV = katha.DEV
KHANDA = [('1', '1', 4), ('1', '2', 5), ('1', '3', 14), ('2', '1', 6), ('3', '1', 4)]

def iast2deva(line):
    """One line of the book's IAST → Devanagari. Bars become separate words (the book writes "śāntiḥ||"), a visarga the
    font gives as ":" is ḥ (prāṇādvāyu:, prahāsī:), and the pluta's 3 joins its vowel (itī 3 → इती३)."""
    line = line.replace('?', '')                               # 1.3.11 "atha ko'hamiti ?": the author's mark
    line = re.sub(r':(?=\s|\||$)', 'ḥ', line)
    line = re.sub(r'(?<=\w)-(?=\w)', '', line)                 # 1.3.12 "etan-nāndanam": the author's hyphen inside a sandhi
    line = re.sub(r'\s*(\|\|?)\s*', r' \1 ', line)
    out = []
    for w in line.split():
        if w.isdigit(): out[-1] += DEV(w)                       # the pluta: इती३
        else: out.append(katha.iast2deva(w))
    return ' '.join(out)

# ---- corrections to the book's reading, each checked against the witnesses (../reconciliation.md) ----
FIX = {   # item: [(book, settled)]; each must occur exactly once in the item's text
    '1.1.2': [('इमाँ ल्लोकानसृजत', 'इमाँल्लोकानसृजत'),                         # one word (imām̐l lokān), as every witness writes it
              ('प्रतिष्ठा- ।', 'प्रतिष्ठा-'),                                  # a bar inside the sandhi प्रतिष्ठाऽन्तरिक्षं
              ('अधस्तात्त आपः', 'अधस्तात्ता आपः')],                           # tāḥ āpaḥ (those are the waters), as the book's own word-by-word
    '1.1.4': [('निरभिद्येतं ना', 'निरभिद्येतां ना'), ('निरभिद्येतमक्षी', 'निरभिद्येतामक्षी'),   # the dual nirabhidyetām, as the book's own word-by-word
              ('प्राणःप्राणाद्', 'प्राणः प्राणाद्')],                          # two words
    '1.2.1': [('तमशनापिपासाभ्याम', 'तमशनायापिपासाभ्याम')],                   # aśanāyā (hunger), as 1.2.5 and the book's own word-by-word
    '1.2.4': [('भूत्वा ऽक्षिणी', 'भूत्वाऽक्षिणी')],                              # a space before the avagraha
    '1.2.5': [('भागिन्न्यौ', 'भागिन्यौ')],                                    # bhāginyau
    '1.3.5': [('ग्रहीतुन्', 'ग्रहीतुं'), ('हैवानमत्रप्स्यत्', 'हैवान्नमत्रप्स्यत्')],   # grahītuṃ before स, as 1.3.4–9; haiva annam, as 1.3.3–8
    '1.3.6': [('यद्धैनच्छ्रोतेणा', 'यद्धैनच्छ्रोत्रेणा')],                        # śrotreṇa, as the same line's first half
    '1.3.9': [('यद्वित्सृज्य', 'यद्विसृज्य'), ('हैवानमत्रप्स्यत्', 'हैवान्नमत्रप्स्यत्')],   # visṛjya (having emitted), as the book's own word-by-word
    '1.3.10': [('यद्वायुरनायुर्वा', 'यद्वायुरन्नायुर्वा')],                      # annāyuḥ (whose life is food), as the book's own word-by-word
    '1.3.11': [('प्रपद्या इति ॥', 'प्रपद्या इति ।')],                          # a ॥ inside the mantra
    '1.3.13': [('इदमदर्शनमिती३', 'इदमदर्शमिती३')],                          # adarśam (I have seen), as the book's own word-by-word
    '2.1.1': [('आत्मन्येवऽऽत्मानं', 'आत्मन्येवाऽऽत्मानं')],                   # eva ātmānam: the long ā the book's ऽऽ stands for, as 3.1.4 prājñenā''tmanā
    '2.1.3': [('गर्भ बिभर्ति', 'गर्भं बिभर्ति'), ('भावयत्येषं', 'भावयत्येषां')],   # garbhaṃ (object); eṣāṃ lokānāṃ (genitive plural)
    '2.1.4': [('अथास्यायामितर अत्मा', 'अथास्यायमितर आत्मा')],                 # ayam itara ātmā
    '2.1.6': [('उत्क्राम्य', 'उत्क्रम्य')],                                    # the gerund utkramya, as 3.1.4
    '3.1.2': [('धृतिमतिर्मनीषा', 'धृतिर्मतिर्मनीषा')],                          # dhṛtiḥ and matiḥ, two of the sixteen, as the book's own word-by-word
    '3.1.3': [('वायुराकाश अपो', 'वायुराकाश आपो'),                             # āpaḥ, the waters
              ('यच्च स्थावरं ॥', 'यच्च स्थावरं')],                            # the end of the book's "Verse 5.3A", inside the mantra
    'shanti': [('॥ ॐ शान्तिः शान्तिः शान्तिः ॥', 'ॐ शान्तिः शान्तिः शान्तिः ॥')],
}

def item(id_, p, s, y, n, lines):
    return {'id': id_, 'p': p, 's': s, 'y': y, 'n': n, 'v': [l.strip() for l in lines if l.strip()]}

def settled(R):
    """{item id: Devanagari lines}, the book's lines converted, laid out and corrected."""
    T = {k: list(v['t']) for k, v in R.items()}
    # om̐ puruṣe ha vā ayam- / ādito …: the book breaks one word (ayamādito) over two lines; they are one line here
    assert T['2.1.1'][0].endswith('ayam-'), T['2.1.1'][0]
    T['2.1.1'][0:2] = [T['2.1.1'][0][:-1] + T['2.1.1'][1]]
    L = {k: [iast2deva(l) for l in t] for k, t in T.items()}
    # the book ends its "Verse 3.2" with तदेनत्सृष्टं पराङ्त्यजिघांसत्, the first words of mantra 1.3.3 in every witness
    first = L['1.3.2'].pop(); assert first.startswith('तदेनत्सृष्टं') and first.endswith(' ॥'), first
    L['1.3.3'].insert(0, first[:-2])
    assert L['1.3.2'][-1].endswith(' ।'); L['1.3.2'][-1] = L['1.3.2'][-1][:-2] + ' ॥'
    for vid, fixes in FIX.items():
        for wrong, right in fixes:
            assert sum(l.count(wrong) for l in L[vid]) == 1, (vid, wrong)
            L[vid] = [l.replace(wrong, right) for l in L[vid]]
    return L

def main():
    R = json.load(open(os.path.join(HERE, 'pdf_raw.json'), encoding='utf-8'))
    L = settled(R)
    sh = L['shanti']
    assert sh[0].startswith('ॐ') and sh[-1] == 'ॐ शान्तिः शान्तिः शान्तिः ॥', sh
    items = [item('shanti.1', 0, 'shanti', 'shanti', '', sh)]
    for a, k, cnt in KHANDA:
        for m in range(1, cnt + 1):
            vid = '%s.%s.%d' % (a, k, m)
            lines = L[vid]
            assert lines[-1].endswith(' ॥') and not any('॥' in l for l in lines[:-1]), (vid, lines)
            lines[-1] = lines[-1][:-2] + ' ॥%s॥' % DEV(m)
            items.append(item(vid, int(a) - 1, 'k%s.%s' % (a, k), 'mantra', str(m), lines))   # cited adhyāya.khaṇḍa.mantra (work.json → cite)
    assert len(items) == 34, len(items)   # the śānti and 33 mantras; the śānti is not repeated at the end
    TOPICS = [
     {"id": "shanti.1", "hi": "शान्तिपाठ", "en": "Shanti Paath"},
     {"id": "1.1.1", "hi": "प्रथम अध्याय, प्रथम खण्ड — आत्मासे लोकों और लोकपालोंकी सृष्टि", "en": "Adhyay 1, Khand 1 — The Self creates the worlds and their guardians"},
     {"id": "1.2.1", "hi": "प्रथम अध्याय, द्वितीय खण्ड — देवताओंके लिये शरीरमें स्थान", "en": "Adhyay 1, Khand 2 — Dwellings in the body for the gods"},
     {"id": "1.3.1", "hi": "प्रथम अध्याय, तृतीय खण्ड — अन्नकी सृष्टि; आत्माका शरीरमें प्रवेश", "en": "Adhyay 1, Khand 3 — Food is made; the Self enters the body"},
     {"id": "2.1.1", "hi": "द्वितीय अध्याय — आत्माके तीन जन्म", "en": "Adhyay 2 — The three births of the self"},
     {"id": "3.1.1", "hi": "तृतीय अध्याय — आत्मा कौन है? प्रज्ञान ही ब्रह्म है", "en": "Adhyay 3 — Who is the Self? Consciousness is Brahman"},
    ]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, TOPICS, ['1', '2', '3'], 'sa', [
        'Aitareya Upaniṣad: the śānti mantra and mantras 1.1.1 … 3.1.4. Made by source/settle.py from the owner\'s book; do not',
        'edit here. Every correction and choice: reconciliation.md; source/check.py compares it with the Devanagari witnesses.'])
    print(len(items), 'items')

if __name__ == '__main__':
    main()
