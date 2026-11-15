"""Nārāyaṇa Sūkta: source/narayana-suktam_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: the
śānti pāṭha the page opens with, the sūkta of the Taittirīya Āraṇyaka's tenth prapāṭhaka (the Mahānārāyaṇa) in fourteen
verses as the page divides it, the Nārāyaṇa Gāyatrī and the closing śānti, with the sections and our topic headings).

The Devanagari, with its svaras, is the page's own. Its transliteration is a second witness: every line is compared
with it (tools/works/shlokam.py); here the two agree on every line. The correction below (`FIX`) is recorded in
../reconciliation.md. The library's transliteration is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py narayana-suktam)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import shlokam, textfile

WITNESS = set()
HEADING = {}
FIX = [
    ('13', 'द्वि॒ध्युल्ले॑खेव॒', 'द्वि॒द्युल्ले॑खेव॒'),   # विद्युत्, "lightning" (वि + द्युत्): ध्यु is a misspelling
]

def item(id_, s, y, n, v):
    return {'id': id_, 'p': 0, 's': s, 'y': y, 'n': n, 'v': v}

if __name__ == '__main__':
    L = shlokam.settled(os.path.join(HERE, 'narayana-suktam_raw.json'), HEADING, WITNESS, FIX)
    assert list(L) == [str(k) for k in range(1, 18)]
    I = [item('shanti.1', 'shanti', 'shanti', '', L['1'])]
    I += [item('m%02d' % k, 'sukta', 'mantra', str(k), L[str(k + 1)]) for k in range(1, 15)]
    I.append(item('gayatri', 'end', 'gayatri', '', L['16']))
    I.append(item('shanti.end', 'end', 'shanti', '', L['17']))
    topics = [{'id': 'shanti.1', 'hi': 'शान्तिपाठ', 'en': 'Shanti Paath'},
              {'id': 'm01', 'hi': 'नारायण ही सब कुछ, सबसे परे', 'en': 'Narayana, all that is and beyond all'},
              {'id': 'm07', 'hi': 'हृदय-कमलमें अग्निशिखा और परमात्मा', 'en': 'The flame in the lotus of the heart, and the Supreme within it'},
              {'id': 'gayatri', 'hi': 'नारायण गायत्री और शान्ति', 'en': 'Narayana Gayatri and shanti'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Nārāyaṇa Sūkta (Taittirīya Āraṇyaka, prapāṭhaka 10), shlokam.org. Made by source/settle.py from the page',
        '(scriptures-data); do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items')
