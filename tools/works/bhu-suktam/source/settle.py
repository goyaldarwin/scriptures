"""Bhū Sūkta: source/bhoomi-suktam_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: the
eighteen verses of the Atharvaveda's Pṛthivī Sūkta (12.1) the page gives, numbered 1–18 as it prints them, with our
topic headings).

The Devanagari is the page's own; the page has no svaras. Its transliteration is a second witness: every line is
compared with it (tools/works/shlokam.py); here the two agree on every line. The one correction (`FIX`) is
recorded in ../reconciliation.md. The library's transliteration is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py bhu-suktam)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import shlokam, textfile

WITNESS = set()
HEADING = {}
FIX = [
    ('16', 'मधु पृथिवी धेहि', 'मधु पृथिवि धेहि'),   # the vocative, addressed by धेहि, as the page's पृथिवि in 11, 12, 15
]

if __name__ == '__main__':
    L = shlokam.settled(os.path.join(HERE, 'bhoomi-suktam_raw.json'), HEADING, WITNESS, FIX)
    assert list(L) == [str(k) for k in range(1, 19)]
    I = [{'id': 'm%02d' % k, 'p': 0, 's': 'sukta', 'y': 'mantra', 'n': str(k), 'v': L[str(k)]} for k in range(1, 19)]
    topics = [{'id': 'm01', 'hi': 'सत्य, ऋत और तप पृथ्वीको धारण करते हैं', 'en': 'Truth, order and austerity uphold the Earth'},
              {'id': 'm10', 'hi': 'पृथ्वी माता, मैं उसका पुत्र', 'en': 'The Earth is my mother, I her son'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Bhū Sūkta: the eighteen verses of the Atharvaveda\'s Pṛthivī Sūkta (12.1) on shlokam.org\'s Bhoomi Suktam. Made by',
        'source/settle.py from the page (scriptures-data); do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items')
