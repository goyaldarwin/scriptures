"""Japji Sahib (Guru Nanak Dev Ji): the owner's PDF text (source/pdf.txt, made by extract.py) → ../text.txt.

The PDF's legacy ASCII Gurmukhi is converted with the Sukhmani Sahib's converter
(tools/works/sukhmani-sahib/source/gurmukhi.py). Lines follow the bani's own divisions: every pada ends with ॥ (the
PDF's wrapping of long padas is undone); the Mool Mantar, which has no ॥ inside, keeps the four lines the PDF prints.
One choice differs from the PDF (reconciliation.md): the title is ॥ ਜਪੁ ॥, as Sri Guru Granth Sahib prints it.

Items (ids are permanent):  mool  · jap (heading) · salok.open (n 1) · p1 … p38 (pauri n) · salok.close (n 1)
It checks the structure and stops on any failure. Then: python3 tools/works/export.py japji-sahib.
"""
import os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(WORK)); import textfile
sys.path.insert(0, os.path.join(WORK, '..', '..', 'text')); import standard
sys.path.append(os.path.join(WORK, '..', 'sukhmani-sahib', 'source')); from gurmukhi import to_unicode

GDIG = str.maketrans('0123456789', '੦੧੨੩੪੫੬੭੮੯')


def read_pdf():
    """The printed lines (legacy ASCII), page headers dropped."""
    return [l for l in open(os.path.join(HERE, 'pdf.txt'), encoding='utf-8').read().split('\n')
            if l and not l.startswith('@page')]


def padas(text):
    """Split running legacy text into padas, each ending with ] or ]N] (or ]N]M])."""
    text = re.sub(r'(?<!\d)\s*\]', ' ]', re.sub(r'\s+', ' ', text))
    out = re.findall(r'.*?\](?:\d+\])*', text)
    rest = text[sum(map(len, out)):].strip()
    assert not rest, rest
    return [p.strip() for p in out if p.strip()]


def uni(ascii_line):
    u = to_unicode(ascii_line)
    u = re.sub(r'\s*॥', ' ॥', u.translate(GDIG))
    u = re.sub(r'॥\s*([੦-੯]+)\s*॥', r'॥\1॥', u)
    return unicodedata.normalize('NFC', re.sub(r'\s+', ' ', u).strip())


def build():
    lines = read_pdf()
    # the Mool Mantar: the PDF's first four printed lines, ending ]
    assert lines[3].strip() == 'gur pRswid ]', lines[:4]
    mool = [uni(l.replace(']', ' ]')) for l in lines[:4]]
    assert lines[4].strip() == 'jpu ]', lines[4]
    ps = padas(' '.join(lines[5:]))
    items = [{'id': 'mool', 'y': 'mool', 'n': '', 'v': mool},
             {'id': 'jap', 'y': 'heading', 'n': '', 'v': ['॥ ਜਪੁ ॥']}]
    cur = []; k = 0
    for p in ps:
        cur.append(uni(p))
        m = re.search(r'\](\d+)\]$', p)
        if not m: continue
        n = int(m.group(1))
        if not items[2:]:
            assert n == 1; items.append({'id': 'salok.open', 'y': 'salok', 'n': '1', 'v': cur})
        elif k < 38:
            k += 1; assert n == k, (k, p); items.append({'id': f'p{k}', 'y': 'pauri', 'n': str(k), 'v': cur})
        else:
            assert n == 1 and cur[0] == 'ਸਲੋਕੁ ॥', cur
            items.append({'id': 'salok.close', 'y': 'salok', 'n': '1', 'v': cur})
        cur = []
    assert not cur, cur
    return items


def check(items):
    assert [x['id'] for x in items] == ['mool', 'jap', 'salok.open'] + [f'p{k}' for k in range(1, 39)] + ['salok.close']
    for x in items:
        for l in x['v']:
            assert re.fullmatch(r'[਀-੿ ॥]+', l), (x['id'], l)
            assert not re.search(r'[ੳੲ](?![ਾਿੀੁੂੇੈੋੌ])', l.replace('ੳੁ', '')), (x['id'], l)   # no bare vowel bearer
        if x['y'] in ('pauri', 'salok'):
            assert x['v'][-1].endswith(f"॥{x['n'].translate(GDIG)}॥"), (x['id'], x['v'][-1])
            assert all(l.endswith('॥') for l in x['v']), x['id']
    assert items[0]['v'][0].startswith('ੴ ਸਤਿ ਨਾਮੁ')


def gur2dev(s):
    """Gurmukhi → Devanagari, letter for letter (topic names in the Hindi interface)."""
    s = re.sub(r'ੱ(.)', lambda m: chr(ord(m.group(1)) - 0x100) + '्' + m.group(1), s)
    out = []
    for c in s:
        o = ord(c)
        if c == 'ੰ': out.append('ं')
        elif c == 'ੵ': out.append('्य')
        elif c == 'ੑ': out.append('्ह')
        elif c == 'ੜ': out.append('ड़')
        elif c == 'ੴ': out.append('१ॐ')
        elif 0x0A00 <= o <= 0x0A7F: out.append(chr(o - 0x100))
        else: out.append(c)
    return ''.join(out)


def pratik(line):
    """A passage of Gurbani is cited by its first line: the Hindi name in Devanagari letters, the English its ISO 15919."""
    first = re.sub(r'\s*॥.*$', '', line)
    tr = standard.iso_line(standard.gurmukhi(first))
    return {'hi': gur2dev(first), 'en': tr[:1].upper() + tr[1:]}


if __name__ == '__main__':
    items = build(); check(items)
    for x in items: x['p'] = 0; x['s'] = x['id']
    topics = [{'id': 'mool', 'hi': 'मूल मंत्र', 'en': 'Mool Mantar'},
              {'id': 'salok.open', **pratik(items[2]['v'][0])}]
    topics += [{'id': x['id'], **pratik(x['v'][0])} for x in items if x['y'] == 'pauri']
    topics.append({'id': 'salok.close', **pratik(items[-1]['v'][1])})
    textfile.write(os.path.join(WORK, 'text.txt'), items, topics, ['japji'], 'pa', [
        'Japji Sahib, Sri Guru Granth Sahib, Ang 1–8. Made by source/make.py from the owner\'s PDF; do not edit here.',
        'Every choice: reconciliation.md; source/check.py checks the text against its witnesses.'])
    print(f"{len(items)} items, {sum(len(x['v']) for x in items)} lines")
