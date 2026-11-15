"""Muṇḍaka Upaniṣad: the shlokam.org page (HTML) → source/mundaka-upanishad_raw.json.

Usage: python3 extract.py <mundaka-upanishad.html>
The page is private (scriptures-data: hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/printouts/shlokam/).
For every verse block on the page (div.verse-section) this keeps its place (data-chapter = muṇḍaka, data-section = khaṇḍa,
data-verse = mantra; 1.0.0 is the śānti), its Devanagari lines (div.detail-sanskrit, split at <br>) and the page's own
transliteration lines (the div.detail-text that follows it), without the page's verse-reference tag. Zero-width spaces
are removed and the text is NFC. The page's English, its readable romanisation, its translation and its word glosses are
the publisher's own text and are never read here.
"""
import html, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'mundaka-upanishad_raw.json')

def clean(s):
    s = re.sub(r'<span class="text-roman-verse-ref">.*?</span>', '', s)
    s = html.unescape(re.sub(r'<[^>]+>', '', s)).replace('​', '')
    return unicodedata.normalize('NFC', ' '.join(s.split()))

def blocks(page):
    out = []
    for sec in re.split(r'(?=<div class="verse-section")', page)[1:]:
        place = re.search(r'data-chapter="(\d+)" data-section="(\d+)" data-verse="(\d+)"', sec)
        deva = re.search(r'<div class="detail-text detail-sanskrit">(.*?)</div>', sec, re.S)
        roman = re.search(r'data-field="roman">.*?<div class="detail-text">(.*?)</div>', sec, re.S)
        assert place and deva and roman, sec[:300]
        v = [clean(l) for l in deva.group(1).split('<br>')]
        t = [clean(l) for l in roman.group(1).split('<br>')]
        assert len(v) == len(t), (place.groups(), v, t)
        out.append({'ref': '.'.join(place.groups()), 'v': [l for l in v if l], 't': [l for l in t if l]})
    return out

if __name__ == '__main__':
    B = blocks(open(sys.argv[1], encoding='utf-8').read())
    json.dump(B, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(B), 'blocks', sum(len(b['v']) for b in B), 'Devanagari lines →', os.path.relpath(OUT))
