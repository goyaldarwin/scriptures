"""The Gita Press Sanskrit–English Rāmāyaṇa as kāṇḍas → sargas → verses (Sanskrit lines) and English paragraphs.

Reading order on a page: full-width bands (sarga ends and headings, footnotes) divide it into regions;
in each region the left column, then the right.
"""
import json, re, sys, collections

KANDA_PAGES = [('bala', 59, 282), ('ayodhya', 283, 714), ('aranya', 715, 928), ('kishkindha', 929, 1169),
               ('sundara', 1192, 1459), ('yuddha', 1460, 2011), ('uttara', 2012, 2303)]
DIG = str.maketrans('०१२३४५६७८९', '0123456789')
ORD = {}

def page_order(lines):
    """Lines of one page in reading order (running head and folio dropped)."""
    body = [l for l in lines if l['y'] > 30]
    bands = sorted({l['y'] for l in body if l['col'] == 2})
    def region(y):
        return sum(1 for b in bands if b < y)
    out = []
    keyed = []
    for l in body:
        if l['col'] == 2 or any(abs(l['y'] - b) <= 3 for b in bands):   # a line level with a band belongs to it
            keyed.append((region(l['y'] - 3.5) * 2 + 1, l['col'] % 2, l['y'], l))
        elif False:
            keyed.append((region(l['y']) * 2 + 1, 0, l['y'], l))
        else:
            keyed.append((region(l['y']) * 2, l['col'], l['y'], l))
    keyed.sort(key=lambda k: k[:3])
    return [k[3] for k in keyed]

def is_heading(l):
    return l['kind'] == 'sa' and l['size'] >= 19 and l['text'].rstrip('॥ ०१२३४५६७८९').endswith('सर्गः')

def is_colophon(l):
    return l['kind'] == 'sa' and l['text'].startswith('इत्यार्षे')

# the book's verse-number marks, with its slips: ॥॥४०, ॥ 4॥ (a Latin digit), विना९॥, ॥ ६८ (no closing ॥), ॥ ३१॥ ॥
VERSE_END = re.compile(r'(?:॥\s*)*([०-९0-9]+)\s*(?:॥\s*)*$')
COLOPHON_TAIL = re.compile(r'सर्गः?\s*॥(\s*[०-९]+\s*॥)?\s*$')
EN_END = re.compile(r'\(\s*(\d+)\s*(?:[-óñ–—]\s*(\d+))?\s*\)\s*[.•*†‡]*\s*$')

# a verse mark; the book's slips: "14)" without its "(", "(I)" and "(l00)" with letters for 1
MARK = re.compile(r'(?:\(\s*|(?<=[\s:;.,!?îí])(?=\d+\)))([\dIl]+)\s*(?:[-óñ–—]\s*([\dIl]+))?\s*\)')
def _num(x):
    return int(x.replace('I', '1').replace('l', '1'))

# The book's English where its verse marks fail; each is recorded in reconciliation.md.
# (kāṇḍa, sarga, verse): the words where the next verse's English begins (the mark is missing in the book)
EN_SPLIT = {('bala', 70, 37): 'ìSagaraís son', ('uttara', 76, 24): 'ëIn this Yuga'}
# (kāṇḍa, sarga, printed mark): the verses the paragraph really covers (the book prints no English before it)
EN_ONLY = {('uttara', 15, '(6)'): (6, 6)}

def apply_en_fixes(kanda, sarga, paras):
    out = []
    for e in paras:
        key = (kanda, sarga, e['printed'])
        if key in EN_ONLY:
            e = dict(e, **{'from': EN_ONLY[key][0], 'to': EN_ONLY[key][1]})
        cut = EN_SPLIT.get((kanda, sarga, e['from']))
        if cut and e['to'] == e['from'] + 1:
            i = e['text'].index(cut)
            out.append(dict(e, to=e['from'], printed='', text=e['text'][:i].strip()))
            e = dict(e, **{'from': e['to'], 'text': e['text'][i:].strip()})
        out.append(e)
    return out

def split_english(lines, last):
    """The sarga's English cut at its verse marks (N) / (N-M), taken in order: a mark is accepted only if it
    starts at or after the next verse expected and ends within the sarga; a mark repeating the previous
    number (a misprint, (35) for (36)) is read as the next. A paragraph whose mark is missing joins the next."""
    text = ''
    global OFFS
    OFFS = []
    for p, t in lines:
        OFFS.append(len(text) + (0 if not text else (0 if text.endswith('-') and not text.endswith(' -') else 1)))
        if text.endswith('-') and not text.endswith(' -'):
            text = text[:-1] + '\u00ad' + t   # a line-end hyphen, marked: decided later (english.py → hyphens)
        else:
            text = (text + ' ' + t) if text else t
    out = []
    expect = 1
    start = 0
    marks = [m for m in MARK.finditer(text) if re.fullmatch(r'\d+', m[1]) or len(m[1]) <= 3]
    nums = [_num(m[1]) for m in marks]
    for i, m in enumerate(marks):
        a = nums[i]; b = _num(m[2]) if m[2] else a
        if b < a:                              # (133-34): the second number abbreviated
            b = int(str(a)[:len(str(a)) - len(str(b))] + str(b))
        if not m[0].startswith('('):           # "14)": only where it fills the gap before the next mark
            nxt = next((nums[j] for j in range(i + 1, len(marks)) if marks[j][0].startswith('(')), None)
            if a != expect or nxt != expect + 1:
                continue
        if a > expect + 3 and any(n < a for n in nums[i + 1:i + 4]):
            if m[2]:
                continue
            a = b = expect                     # a misprinted number ((99) for (69)) still ends its paragraph
        if a == expect - 1 and b == a and out and out[-1]['to'] == a:
            a = b = expect                     # repeated number
        if a < expect or b > last or a > b:
            continue
        out.append({'from': expect, 'to': b, 'printed': m[0], 'text': text[start:m.start()].strip(), 's': start, 'e': m.end()})
        expect = b + 1
        start = m.end()
    tail = text[start:].strip()
    if tail:
        out.append({'from': expect, 'to': None, 'printed': '', 'text': tail, 's': start, 'e': len(text)})
    return out

def parse(L):
    pages = collections.defaultdict(list)
    for l in L:
        pages[l['page']].append(l)
    book = []
    for kanda, p0, p1 in KANDA_PAGES:
        sargas = []
        cur = None
        sa_buf, en_buf = [], []
        for p in range(p0, p1 + 1):
            for l in page_order(pages[p]):
                if is_heading(l):
                    cur = {'kanda': kanda, 'heading': l['text'], 'page': p, 'verses': [], 'en': [], 'colophon': None,
                           'title_en': [], 'other': []}
                    sargas.append(cur); sa_buf, en_buf = [], []
                    continue
                if cur is None:
                    continue
                if is_colophon(l):
                    cur['colophon'] = l['text'] + (cur['colophon'] or ''); cur['colophon_page'] = p
                    cur['in_colophon'] = not COLOPHON_TAIL.search(l['text'])
                    continue
                if l['kind'] == 'sa' and len(l['text']) < 45 and COLOPHON_TAIL.search(l['text']) and cur['verses']:
                    cur['colophon'] = (cur['colophon'] or '') + ' ' + l['text']   # a colophon's wrapped tail
                    cur['in_colophon'] = False
                    continue
                if cur.get('in_colophon') and l['kind'] == 'sa':
                    cur['colophon'] += ' ' + l['text']
                    cur['in_colophon'] = not COLOPHON_TAIL.search(l['text'])
                    continue
                if l['kind'] == 'sa' and l['size'] >= 11.5 and l['col'] != 2:
                    sa_buf.append(l['text'])
                    m = VERSE_END.search(l['text'])
                    if m and '॥' in m[0] or (m and re.search('[ािीुूृेैोौंःक-ह]' + m[1] + '॥', l['text'])):
                        cur['verses'].append({'n': int(m[1].translate(DIG)), 'lines': sa_buf, 'page': p})
                        sa_buf = []
                    continue
                if l['kind'] == 'en' and 10.5 <= l['size'] <= 11.5 and l['col'] != 2 and 'Nalandahel' in l['fonts'][0]:
                    cur.setdefault('en_lines', []).append((p, l['text'])); cur.setdefault('en_objs', []).append(l)
                    continue
                if not cur['verses'] and l['kind'] == 'en' and l['size'] >= 11.5:
                    cur['title_en'].append(l['text'])
                    continue
                cur['other'].append((p, l['col'], l['kind'], l['size'], l['text'][:120]))
            # a verse or paragraph may continue on the next page: buffers carry over
        for sg in sargas:
            raw = split_english(sg.get('en_lines', []), max([v['n'] for v in sg['verses']] or [0]))
            sg['line_offs'] = OFFS
            sg['raw_en'] = raw
            sg['en'] = apply_en_fixes(kanda, sargas.index(sg) + 1, [dict(x) for x in raw])
        book.append({'kanda': kanda, 'sargas': sargas})
    return book

if False:
    L = json.load(open(sys.argv[1]))
    book = parse(L)
    json.dump(book, open(sys.argv[2], 'w'), ensure_ascii=False)
    for k in book:
        print(k['kanda'], len(k['sargas']), 'sargas', sum(len(s['verses']) for s in k['sargas']), 'verses')
