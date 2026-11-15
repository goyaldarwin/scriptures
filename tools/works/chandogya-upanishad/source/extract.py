"""Chāndogya Upaniṣad: the shlokam.org page (HTML) → source/chandogya_raw.json.

Usage: python3 extract.py <scriptures-data>/hinduism/veda/samaveda/upanishad/chandogya-upanishad/printouts/shlokam/chandogya-upanishad.html
The page is private (scriptures-data). For every block of the page (div.verse-section) this keeps its place as the page
gives it (data-chapter, data-section, data-verse: prapāṭhaka, khaṇḍa, mantra), its Devanagari (div.detail-sanskrit) and
the page's own transliteration (the div.detail-text after it), each split into lines at <br>, with zero-width spaces
removed. The page's English and word glosses are © shlokam.org and are not read.
"""
import html, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = re.compile(r'<div class="verse-section" ([^>]*)>(.*?)(?=<div class="verse-section" |\Z)', re.S)
DEVA = re.compile(r'<div class="detail-text detail-sanskrit">(.*?)</div>', re.S)
ROMAN = re.compile(r'<div class="detail-section" data-field="roman">.*?<div class="detail-text">(.*?)</div>', re.S)

def lines(fragment):
    fragment = re.sub(r'<span class="text-roman-verse-ref">[^<]*</span>', '', fragment)
    out = []
    for l in re.split(r'<br\s*/?>', fragment):
        assert '<' not in l, l
        l = unicodedata.normalize('NFC', html.unescape(l)).replace('​', '')
        l = ' '.join(l.split())
        if l: out.append(l)
    return out

def blocks(page):
    out = []
    for attrs, body in BLOCK.findall(page):
        a = dict(re.findall(r'(data-[a-z-]+)="([^"]*)"', attrs))
        ref = re.search(r'<span class="text-roman-verse-ref">([^<]*)</span>', body)
        out.append({'id': a['data-content-id'], 'ch': int(a['data-chapter']), 'sec': int(a['data-section']),
                    'n': int(a['data-verse']), 'ref': ref.group(1) if ref else '',
                    'v': lines(DEVA.search(body).group(1)), 't': lines(ROMAN.search(body).group(1))})
    return out

if __name__ == '__main__':
    B = blocks(open(sys.argv[1], encoding='utf-8').read())
    with open(os.path.join(HERE, 'chandogya_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(B, f, ensure_ascii=False, indent=0); f.write('\n')
    print(len(B), 'blocks')
