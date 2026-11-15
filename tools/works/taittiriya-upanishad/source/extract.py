"""Taittirīya Upaniṣad: the shlokam.org page (HTML) → source/taittiriya_raw.json.

Usage: python3 extract.py <taittiriya-upanishad.html>
The page is private (scriptures-data: hinduism/veda/yajurveda/krishna-yajurveda/upanishad/taittiriya-upanishad/
printouts/shlokam/taittiriya-upanishad.html, fetched from https://shlokam.org/text/taittiriya-upanishad.htm).
For every verse block of the page (div.verse-section) this keeps, in reading order: its reference (data-chapter,
data-section, data-verse: vallī, anuvāka, paragraph, as the page numbers them), its Devanagari lines
(div.detail-sanskrit) and its transliteration lines (the div.detail-text after it), split at <br>, with zero-width
spaces removed. The page's English (the colloquial spelling, the translation) is the publisher's and is not kept.
The page has no svaras. settle.py makes text.txt from this file (../reconciliation.md).
"""
import html.parser, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

class Page(html.parser.HTMLParser):
    """Collects each verse-section's Devanagari and transliteration as text with '\\n' at every <br>."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.field, self.depth, self.buf, self.in_ref = [], None, 0, [], False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get('class') or '').split()
        if tag == 'div' and 'verse-section' in cls:
            self.blocks.append({'ref': '%s.%s.%s' % (a['data-chapter'], a['data-section'], a['data-verse']), 'v': None, 't': None})
            self.want = None
        if tag == 'div' and a.get('data-field') in ('sanskrit', 'roman'):
            self.want = a['data-field']
        if tag == 'div' and 'detail-text' in cls and self.field is None and getattr(self, 'want', None):
            self.field, self.depth, self.buf = self.want, 1, []; return
        if self.field:
            if tag == 'div': self.depth += 1
            if tag == 'br': self.buf.append('\n')
            if tag == 'span' and 'text-roman-verse-ref' in cls: self.in_ref = True

    def handle_endtag(self, tag):
        if not self.field: return
        if tag == 'span' and self.in_ref: self.in_ref = False; return
        if tag == 'div':
            self.depth -= 1
            if self.depth == 0:
                text = unicodedata.normalize('NFC', ''.join(self.buf).replace('​', ''))
                lines = [re.sub(r'\s+', ' ', l).strip() for l in text.split('\n')]
                self.blocks[-1]['v' if self.field == 'sanskrit' else 't'] = [l for l in lines if l]
                self.field = self.want = None

    def handle_data(self, data):
        if self.field and not self.in_ref: self.buf.append(data)

if __name__ == '__main__':
    p = Page(); p.feed(open(sys.argv[1], encoding='utf-8').read())
    B = p.blocks
    assert all(b['v'] and b['t'] for b in B), [b['ref'] for b in B if not (b['v'] and b['t'])]
    json.dump(B, open(os.path.join(HERE, 'taittiriya_raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(B), 'blocks,', sum(len(b['v']) for b in B), 'Devanagari lines')
