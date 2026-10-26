"""Sukhmani Sahib: the owner's PDF → source/lines.json (the PDF's lines, in order, as printed).

Usage:  python3 tools/works/sukhmani-sahib/source/extract.py <the PDF>
        (private copy: scriptures-data/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/books/sant-singh-khalsa/sukhmani-sahib.pdf)

The PDF (225 pages, "Sukhmani Sahib with phonetic transliteration & English translation, Gurmukhi", K. Thind, 2003)
prints every line of the bani as three lines, each in its own font:
  GurbaniAkharThick 14 pt   the Gurmukhi, in the legacy ASCII font encoding (converted by gurmukhi.py)
  Tahoma 14 pt              the romanised transliteration, then the English translation (Sant Singh Khalsa),
                            each possibly wrapped over several lines; a 9 pt Tahoma "N" is a raised nasal mark
The text layer is clean, so it is read directly (no OCR). A Gurmukhi line sometimes holds two padas
("ijau mhw ... pwvY ] iqau swDU ... pRgtwvY ]"); the split happens in structure.py, not here.

Which Tahoma lines are transliteration: the transliteration ends a pada with "." and a numbered line with "||n||",
exactly as the Gurmukhi ends each pada with "]" (and "]n]"). So lines are taken as transliteration until it has
as many pada ends as the Gurmukhi line (and, for a numbered line, its "||n||", which can wrap onto a line of its
own); the rest is English. The checks in check.py confirm the split.

Output: [{"pg": page (1-based), "g": legacy Gurmukhi, "t": transliteration, "e": English}, …] — wrap breaks
joined with a space, a line-end hyphen ("well-\nbeing") kept as printed but without the space.
"""
import json, os, re, sys
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))


def pada_ends_g(g):
    """How many padas a legacy Gurmukhi line ends: every ']' that closes words (not ']1]' numbers or 'rhwau ]')."""
    s = re.sub(r'\]\d+', ']', g)            # ]1] → ]] ; ]8]10] → ]]]
    s = re.sub(r'\](\s*\])+', ']', s)        # one end per run
    s = re.sub(r'\]\s*rhwau\s*\]', ']', s)   # "... ibsRwm ] rhwau ]": the pause is not a pada
    return s.count(']')


def pada_ends_t(t):
    s = re.sub(r'\|\|[\d|]*\|\|', '.', t)    # ||1|| / ||8||10|| end a pada like "."
    s = re.sub(r'\.(\s*\.)+', '.', s)
    s = re.sub(r'\.\s*rahaa-o\.', '.', s)
    return len(re.findall(r'\.(\s|$)', s + ' '))


def join(lines):
    out = ''
    for l in lines:
        l = l.strip()
        if not out: out = l
        elif re.search(r'[A-Za-z]-$', out) and not re.search(r'\s-$', out): out += l   # a word broken at its hyphen
        else: out += ' ' + l
    return re.sub(r'\s+', ' ', out).strip()


def main(pdf):
    d = pymupdf.open(pdf)
    groups = []
    for pn, page in enumerate(d):
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                font = l['spans'][0]['font']
                text = ''.join(s['text'] for s in l['spans'])
                if font.startswith('GurbaniAkhar'):
                    groups.append({'pg': pn + 1, 'g': text.strip(), 'tl': []})
                elif font == 'Tahoma' and groups:
                    groups[-1]['tl'].append(text)
    out = []
    for x in groups:
        need, tl = pada_ends_g(x['g']), x['tl']
        k = 1
        num = re.search(r'\](\d+)\]', x['g'])   # a numbered line: its transliteration also carries ||n|| (it may wrap)
        while k < len(tl) and (pada_ends_t(join(tl[:k])) < need or (num and '||' not in join(tl[:k]))): k += 1
        t, e = join(tl[:k]), join(tl[k:])
        assert e, f"page {x['pg']}: no English after {x['g']!r}"
        out.append({'pg': x['pg'], 'g': x['g'], 't': t, 'e': e})
    p = os.path.join(HERE, 'lines.json')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write('[\n' + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in out) + '\n]\n')
    print(f'{len(out)} printed lines from {d.page_count} pages → {os.path.relpath(p)}')


if __name__ == '__main__':
    main(sys.argv[1])
