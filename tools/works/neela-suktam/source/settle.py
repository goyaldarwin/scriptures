"""Nīlā Sūkta: source/neela-suktam_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: the
invocation the page opens with, the two mantras of the Taittirīya Saṃhitā (4.4.12) it gives, the Nīlā Gāyatrī and the
closing śānti, with the sections and our topic headings).

The Devanagari, with its svaras, is the page's own. Its transliteration is a second witness: every line is compared
with it (tools/works/shlokam.py); here the two agree on every line. The corrections below (`FIX`) are recorded in
../reconciliation.md. The library's transliteration is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py neela-suktam)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import shlokam, textfile

WITNESS = set()
HEADING = {}
FIX = [   # missing spaces between words that make no sandhi, and one misspelt word
    ('2', 'पय॑स्वती॒रन्ति॒राशा॑नो', 'पय॑स्वती॒ रन्ति॒राशा॑ नो'),   # पयस्वतीः रन्तिः आशा नः
    ('2', 'ऽस्येशा॑ना॒सह॑सो॒या म॒नोता᳚', 'ऽस्येशा॑ना॒ सह॑सो॒ या म॒नोता᳚'),   # ईशाना सहसः या मनोता
    ('3', 'वा॒युस्स॑न्धुवा॒नावाता॑', 'वा॒युस्स॑न्धुवा॒ना वाता॑'),     # सन्धुवानाः वाताः
    ('3', 'दि॒वोध॒रुणः॑', 'दि॒वो ध॒रुणः॑'),                          # दिवः धरुणः
    ('3', 'अ॒स्येश्या॑ना॒', 'अ॒स्येशा॑ना॒'),       # ईशाना, as in the mantra before (अस्येशाना): ईश्याना is no word
    # on the witness (Wikisource's accented Taittirīya Saṃhitā 4.4.12.5, source/check.py): after दि॒शां the svarita
    # falls on वि (वि॑ष्णुप॒त्न्य); the page puts it on ष्णु, as in mantra 2, where it follows जग॑तो॒
    ('2', 'विँष्णु॑प॒त्न्य', 'विँ॑ष्णुप॒त्न्य'),
]

def item(id_, s, y, n, v):
    return {'id': id_, 'p': 0, 's': s, 'y': y, 'n': n, 'v': v}

if __name__ == '__main__':
    L = shlokam.settled(os.path.join(HERE, 'neela-suktam_raw.json'), HEADING, WITNESS, FIX)
    assert list(L) == [str(k) for k in range(1, 6)]
    I = [item('mangala', 'sukta', 'mangala', '', L['1']),
         item('m01', 'sukta', 'mantra', '1', L['2']),
         item('m02', 'sukta', 'mantra', '2', L['3']),
         item('gayatri', 'end', 'gayatri', '', L['4']),
         item('shanti.end', 'end', 'shanti', '', L['5'])]
    topics = [{'id': 'mangala', 'hi': 'नीळा देवीकी शरण', 'en': 'Refuge in Neela Devi'},
              {'id': 'm01', 'hi': 'विष्णुपत्नी, दिशाओंकी ध्रुव स्वामिनी', 'en': 'Vishnu’s consort, steadfast ruler of the quarters'},
              {'id': 'gayatri', 'hi': 'नीळा गायत्री और शान्ति', 'en': 'Neela Gayatri and shanti'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Nīlā Sūkta (Taittirīya Saṃhitā 4.4.12), shlokam.org. Made by source/settle.py from the page (scriptures-data);',
        'do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items')
