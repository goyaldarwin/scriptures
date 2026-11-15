"""Bhū Sūkta: source/ts-1.5.3_raw.txt (Taittirīya Saṃhitā 1.5.3.1–2 from Sanskrit Wikisource, made by extract.py) →
../text.txt (the settled text: the sūkta's seven ṛks, one item each, its lines at the page's daṇḍas, and the closing
śānti the recording sings, with our topic headings).

The words and svaras are the page's own; the recording's ॐ before the first ṛk and its closing śānti are added
(../reconciliation.md). The library's transliteration is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py bhu-suktam)
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
import textfile

# the recording's closing (its transcript), worded as Sanskrit Wikisource's accented Taittirīya Āraṇyaka closes its
# Upaniṣad prapāṭhakas (ओं शान्ति॒श्शान्ति॒श्शान्तिः॑, the Nārāyaṇa Sūkta's witness), in the Sūktas' spelling
SHANTI = 'ॐ शान्ति॒-श्शान्ति॒-श्शान्तिः॑ ॥'

if __name__ == '__main__':
    raw = open(os.path.join(HERE, 'ts-1.5.3_raw.txt'), encoding='utf-8').read().strip()
    rks = [r.strip() for r in raw.split('।।') if r.strip()]
    assert len(rks) == 7, len(rks)
    I = []
    for k, r in enumerate(rks, 1):
        lines = [l.strip() for l in r.split('।')]
        v = [l + ' ।' for l in lines[:-1]] + [lines[-1] + ' ॥']
        if k == 1: v[0] = 'ॐ ' + v[0]          # the recording opens with ॐ (its transcript)
        I.append({'id': 'm%02d' % k, 'p': 0, 's': 'sukta', 'y': 'mantra', 'n': str(k), 'v': v})
    I.append({'id': 'shanti.end', 'p': 0, 's': 'end', 'y': 'shanti', 'n': '', 'v': [SHANTI]})
    topics = [{'id': 'm01', 'hi': 'भूमि, द्युलोक और अन्तरिक्ष; अग्निका आधान', 'en': 'Earth, sky and mid-air; the fire laid down'},
              {'id': 'm05', 'hi': 'क्रोधसे बिखरी अग्निको फिर प्रज्वलित करना', 'en': 'Kindling again the fire scattered in anger'},
              {'id': 'shanti.end', 'hi': 'शान्तिपाठ', 'en': 'Shanti Paath'}]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['sukta'], 'sa', [
        'Bhū Sūkta (Taittirīya Saṃhitā 1.5.3.1–2), Sanskrit Wikisource. Made by source/settle.py from',
        'source/ts-1.5.3_raw.txt; do not edit here. Every choice: reconciliation.md.'])
    print(len(I), 'items')
