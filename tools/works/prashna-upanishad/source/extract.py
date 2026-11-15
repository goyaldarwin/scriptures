"""Praśna Upaniṣad: shlokam.org's page (saved HTML) → source/page_raw.json.

Usage: python3 extract.py <scriptures-data>/hinduism/veda/atharvaveda/upanishad/prashna-upanishad/printouts/shlokam/prashnopanishad.html
The HTML is private (scriptures-data). For every verse block of the page (div.verse-section) this keeps, in page order:
its praśna and verse number (data-chapter, data-verse: 0 is the opening śānti), its Devanagari lines (div.detail-sanskrit,
split at <br>) and the page's own transliteration lines (the div.detail-text that follows it, data-field "roman"), as
the page has them. settle.py mends and settles them (../reconciliation.md). The page's English, its word notes and its
commentary are the publisher's text and are never kept in this repository.
"""
import html, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

def lines(div):
    """A div's inner HTML → its lines: split at <br>, tags dropped, entities read, NFC."""
    out = []
    for l in re.split(r'<br\s*/?>', div):
        l = re.sub(r'<span class="text-roman-verse-ref">[^<]*</span>', '', l)   # the page's reference label ("1.0")
        l = unicodedata.normalize('NFC', html.unescape(re.sub(r'<[^>]+>', '', l))).strip()
        if l: out.append(l)
    return out

def blocks(page):
    out = []
    for sec in re.split(r'<div class="verse-section"', page)[1:]:
        head = re.match(r'[^>]*data-chapter="(\d+)"[^>]*data-verse="(\d+)"', sec)
        dev = re.search(r'<div class="detail-text detail-sanskrit">(.*?)</div>', sec, re.S)
        rom = re.search(r'data-field="roman">.*?<div class="detail-text">(.*?)</div>', sec, re.S)
        assert head and dev and rom, sec[:200]
        out.append({'prashna': int(head.group(1)), 'verse': int(head.group(2)), 'v': lines(dev.group(1)), 't': lines(rom.group(1))})
    return out

if __name__ == '__main__':
    B = blocks(open(sys.argv[1], encoding='utf-8').read())
    with open(os.path.join(HERE, 'page_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(B, f, ensure_ascii=False, indent=0); f.write('\n')
    print(len(B), 'blocks', sum(len(b['v']) for b in B), 'Devanagari lines')
