"""Cache every text span of the Gita Press Sanskrit–English PDF (font, size, bbox, text, each glyph's x).

    python3 extract.py <sanskrit-english.pdf> <spans.pkl>
"""
import sys, pickle, fitz

d = fitz.open(sys.argv[1])
pages = []
for i in range(d.page_count):
    pg = d[i]; out = []
    for b in pg.get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                t = ''.join(c['c'] for c in s['chars'])
                out.append((s['font'], round(s['size'], 1), [round(x, 1) for x in s['bbox']], t,
                            [round(c['bbox'][0], 1) for c in s['chars']], [round(c['bbox'][2], 1) for c in s['chars']]))
    pages.append((pg.rect.width, pg.rect.height, out))
pickle.dump(pages, open(sys.argv[2], 'wb'))
