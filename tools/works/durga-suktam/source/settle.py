"""Durgā Sūkta: source/durga-suktam_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: the seven
mantras of the Taittirīya Āraṇyaka's tenth prapāṭhaka (the Mahānārāyaṇa), the Durgā Gāyatrī, the closing words and the
śānti, with the sections and our topic headings).

The Devanagari, with its svaras, is the page's own. Its transliteration is a second witness: every line is compared
with it (tools/works/shlokam.py); here the two agree on every line. Then the page's heading is left out (`HEADING`)
and the corrections below made (`FIX`), each recorded in ../reconciliation.md. The library's transliteration is made by
the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py durga-suktam)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import shlokam, textfile

WITNESS = set()
# an editor's heading on the page (as the Śrī Rudram's अथ श्रीरुद्रप्रश्नः): our topic names the place
HEADING = {'1': 'अथ दुर्गा सूक्तम्'}
FIX = [
    ('1', 'सोम॑ मरातीय॒तो', 'सोम॑मरातीय॒तो'),     # सोमम् + अरातीयतः: the space falls inside the word सोमम्
    ('5', 'पृ॒त॒ना॒ जित॒ग्ं॒', 'पृ॒त॒ना॒जित॒ग्ं॒'),    # one compound, पृतनाजितम् "victor in battles"
]

def item(id_, s, y, n, v):
    return {'id': id_, 'p': 0, 's': s, 'y': y, 'n': n, 'v': v}

if __name__ == '__main__':
    L = shlokam.settled(os.path.join(HERE, 'durga-suktam_raw.json'), HEADING, WITNESS, FIX)
    assert list(L) == [str(k) for k in range(1, 10)] and len(L['9']) == 2
    I = [item('m%02d' % k, 'sukta', 'mantra', str(k), L[str(k)]) for k in range(1, 8)]
    I.append(item('gayatri', 'end', 'gayatri', '', L['8']))
    I.append(item('iti', 'end', 'iti', '', L['9'][:1]))
    I.append(item('shanti.end', 'end', 'shanti', '', L['9'][1:]))
    topics = [{'id': 'm01', 'hi': 'अग्नि हमें सब दुर्गतियोंसे पार ले जाएँ', 'en': 'Agni, carry us across every hardship'},
              {'id': 'gayatri', 'hi': 'दुर्गा गायत्री और समापन', 'en': 'Durga Gayatri and closing'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Durgā Sūkta (Taittirīya Āraṇyaka, prapāṭhaka 10), shlokam.org. Made by source/settle.py from the page',
        '(scriptures-data); do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items')
