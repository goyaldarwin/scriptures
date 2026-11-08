"""Japji Sahib: the owner's PDF → source/pdf.txt, its text layer as printed (legacy ASCII Gurmukhi, one printed
line per line, each page headed by a line "@page N").

The PDF (SikhNet, "1 - Japji [Gurmukhi]", 37 pages) prints only the Gurmukhi, in the GurbaniAkharHeavy font (the
common legacy encoding: ASCII letters drawn as Gurmukhi; source/make.py converts it with
tools/works/sukhmani-sahib/source/gurmukhi.py). Page 1 is a cover without text.
Only needed again if the PDF changes:
    python3 tools/works/japji-sahib/source/extract.py <the PDF>
"""
import os, sys
import pypdf

HERE = os.path.dirname(os.path.abspath(__file__))
r = pypdf.PdfReader(sys.argv[1])
out = []
for i, page in enumerate(r.pages, 1):
    lines = [l.strip() for l in page.extract_text().split('\n')]
    lines = [l for l in lines if l]
    if lines: out += [f'@page {i}'] + lines
open(os.path.join(HERE, 'pdf.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'{len(r.pages)} pages, {sum(not l.startswith("@") for l in out)} printed lines → source/pdf.txt')
