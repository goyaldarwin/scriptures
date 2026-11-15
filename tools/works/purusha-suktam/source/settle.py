"""Puruṣa Sūkta: source/purusha-suktam_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: the
eighteen mantras of Taittirīya Āraṇyaka 3.12, the six of the Uttaranārāyaṇa, 3.13, and the śānti pāṭha the page closes
with, with the sections and our topic headings).

The Devanagari, with its svaras, is the page's own. Its transliteration is a second witness: every line is compared
with it (tools/works/shlokam.py; `WITNESS` names the lines where the two differ, and why). Then the page's headings are
left out (`HEADING`) and the corrections below made (`FIX`), each recorded in ../reconciliation.md. The library's
transliteration is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py purusha-suktam)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import shlokam, textfile

# the page's verse 18, line 2: महि॒मानः॑ सचन्ते in Devanagari, mahi̠māna̍-ssachantē (the -स्स spelling) in the
# transliteration, the same words; verse 25, line 1: the heading शान्ति मन्त्रः, "Shanti Mantra" in the transliteration
WITNESS = {('18', 1), ('25', 0)}
# an editor's heading on the page, not recited: our topics name these places
HEADING = {'19': 'उत्तरनारायणम्', '25': 'शान्ति मन्त्रः'}
FIX = [
    ('2', 'उ॒तामृ॑त॒त्व स्येशा॑नः', 'उ॒तामृ॑त॒त्वस्येशा॑नः'),   # one word, अमृतत्वस्य: a space inside it
    ('6', 'श॒रध्ध॒विः', 'श॒रद्ध॒विः'),                     # शरद् + हविः: द्ध (ध्ध is no Sanskrit spelling)
    ('12', 'क॒ति॒था', 'क॒ति॒धा'),                          # कतिधा, "in how many ways" (कतिथा is no word)
    ('16', 'वद॒न्॒, यदा', 'वद॒न्॒ यदा'),                    # a stray comma inside the pāda
]

def item(id_, s, y, n, v):
    return {'id': id_, 'p': 0, 's': s, 'y': y, 'n': n, 'v': v}

if __name__ == '__main__':
    L = shlokam.settled(os.path.join(HERE, 'purusha-suktam_raw.json'), HEADING, WITNESS, FIX)
    assert list(L) == [str(k) for k in range(1, 26)]
    I = [item('m%02d' % k, 'purusha' if k <= 18 else 'uttara', 'mantra', str(k), L[str(k)]) for k in range(1, 25)]
    # the page prints the śānti pāṭha's eight short phrases on one line: two to a line here, as they pair in sense
    ph = L['25'][0].rstrip(' ।').split(' । ')
    assert len(ph) == 8 and len(L['25']) == 2
    I.append(item('shanti.end', 'shanti', 'shanti', '', [' । '.join(ph[k:k + 2]) + ' ।' for k in range(0, 8, 2)] + L['25'][1:]))
    topics = [{'id': 'm01', 'hi': 'सहस्रशीर्षा पुरुष', 'en': 'The Person of a thousand heads'},
              {'id': 'm06', 'hi': 'पुरुषका यज्ञ और सृष्टि', 'en': 'The sacrifice of the Person, and creation'},
              {'id': 'm16', 'hi': 'पुरुषको जानकर अमृतत्व', 'en': 'Knowing the Person, one becomes immortal'},
              {'id': 'm19', 'hi': 'उत्तरनारायण', 'en': 'Uttara Narayana'},
              {'id': 'shanti.end', 'hi': 'शान्तिपाठ', 'en': 'Shanti Paath'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Puruṣa Sūkta (Taittirīya Āraṇyaka 3.12–13), shlokam.org. Made by source/settle.py from the page (scriptures-data);',
        'do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items')
