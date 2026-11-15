"""Śrī Sūkta: source/sri-suktam_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: the fifteen
ṛks of the sūkta (Ṛgveda khila 2.6), its phalaśruti, the verses in praise of Lakṣmī the page adds after them, and its
closing, numbered 1–37 as the page prints them, with the sections and our topic headings).

The Devanagari is the page's own; the page has no svaras. Its transliteration is a second witness: every line is
compared with it (tools/works/shlokam.py); here the two agree on every line. Then the page's headings are left out
(`HEADING`) and the corrections below made (`FIX`), each recorded in ../reconciliation.md. The library's transliteration
is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py shri-suktam)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import shlokam, textfile

WITNESS = set()
# an editor's heading on the page, not recited: our topics name these places
HEADING = {'16': 'फलश्रुतिः', '17': 'स्तोत्रम्'}
FIX = [
    ('17', 'पद्म ऊरु पद्माक्षी', 'पद्म ऊरु पद्माक्षि'),     # the vocative, as पद्मदलायताक्षि (24)
    ('17', 'भजस्व पद्माक्षी', 'भजस्व पद्माक्षि'),
    ('22', 'मात्सर्य न', 'मात्सर्यं न'),                   # मात्सर्यम्, subject like क्रोधः and लोभः
    ('30', 'भजेहमाद्यां', 'भजेऽहमाद्यां'),                  # भजे + अहम्: the elided a's avagraha
    ('30', 'जगदीस्वरीं', 'जगदीश्वरीं'),                    # ईश्वरी
    ('35', 'महियते', 'महीयते'),                            # the verb महीयते
    # on the witnesses (Wikisource's two texts, GRETIL's khila 2.6: source/check.py)
    ('17', 'पद्मासम्भवे', 'पद्मसम्भवे'),                   # "lotus-born", as all three; पद्मा-, "born of Padmā", has no sense here
    ('22', 'श्रीसूक्तं जपेत्सदा', 'श्रीसूक्तं जपेत्'),        # सदा breaks the anuṣṭubh (ten syllables); the khila and Wikisource 1 lack it
    ('30', 'त्रिणेत्रां', 'त्रिनेत्रां'),                     # त्रिनेत्र, as all three: no ण in it
]

def item(id_, s, y, n, v):
    return {'id': id_, 'p': 0, 's': s, 'y': y, 'n': n, 'v': v}

if __name__ == '__main__':
    L = shlokam.settled(os.path.join(HERE, 'sri-suktam_raw.json'), HEADING, WITNESS, FIX)
    assert list(L) == [str(k) for k in range(1, 38)]
    I = []
    for k in range(1, 38):
        y = ('mantra' if k <= 15 else 'phalashruti' if k == 16 else 'gayatri' if k == 34 else 'uttara' if k == 37
             else 'shloka')
        s = 'sukta' if k <= 15 else 'phala' if k == 16 else 'stotra'
        I.append(item('m%02d' % k, s, y, str(k), L[str(k)]))
    topics = [{'id': 'm01', 'hi': 'लक्ष्मीका आवाहन', 'en': 'Calling Lakshmi to the home'},
              {'id': 'm16', 'hi': 'फलश्रुति', 'en': 'Phalashruti'},
              {'id': 'm17', 'hi': 'लक्ष्मीकी स्तुति', 'en': 'Verses in praise of Lakshmi'},
              {'id': 'm37', 'hi': 'समापन', 'en': 'Closing'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Śrī Sūkta (Ṛgveda khila 2.6) with its phalaśruti and the verses the page adds, shlokam.org. Made by',
        'source/settle.py from the page (scriptures-data); do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items')
