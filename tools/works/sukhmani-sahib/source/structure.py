"""Sukhmani Sahib: source/lines.json (the PDF's printed lines) → the work's items, in reading order.

The bani (Sri Guru Granth Sahib, ang 262–296) is 24 Ashtapadis. Each opens with a Salok ("ਸਲੋਕੁ ॥" + a couplet
numbered ॥੧॥), then "ਅਸਟਪਦੀ ॥" and eight pauris of ten padas, numbered ॥੧॥ … ॥੮॥ (the last also carries the
Ashtapadi's number: ॥੮॥੧॥ … ॥੮॥੨੪॥). Before the first Salok stands the title "ਗਉੜੀ ਸੁਖਮਨੀ ਮਃ ੫ ॥", and after the
first pauri the Rahaa-o couplet "ਸੁਖਮਨੀ ਸੁਖ ਅੰਮ੍ਰਿਤ ਪ੍ਰਭ ਨਾਮੁ ॥ …".

Items (ids are permanent):
  a01.title   heading   ਗਉੜੀ ਸੁਖਮਨੀ ਮਃ ੫ ॥                         (only in Ashtapadi 1)
  aNN.salok   salok     ਸਲੋਕੁ ॥ + the couplet (Ashtapadi 1: ਸਲੋਕੁ ॥, ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥ and four lines)
  aNN.p1      pauri     ਅਸਟਪਦੀ ॥ + ten padas ॥੧॥
  a01.rahao   rahao     ਸੁਖਮਨੀ ਸੁਖ ਅੰਮ੍ਰਿਤ ਪ੍ਰਭ ਨਾਮੁ ॥ ਭਗਤ ਜਨਾ ਕੈ ਮਨਿ ਬਿਸ੍ਰਾਮ ॥ ਰਹਾਉ ॥   (only in Ashtapadi 1)
  aNN.p2 … aNN.p8
The headings ਸਲੋਕੁ ॥ and ਅਸਟਪਦੀ ॥ are Gurbani text, so they stay, as the first line of the item they introduce.
One verse line = one pada: where the PDF prints two padas on one line, they are split at the ॥ (and the
transliteration at its "."), so every pauri has ten lines.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gurmukhi import to_unicode

HERE = os.path.dirname(os.path.abspath(__file__))


def split_padas(u, t):
    """'… ਪਾਵੈ ॥ ਤਿਉ … ਪ੍ਰਗਟਾਵੈ ॥' → two lines; the transliteration is split the same way when it has as many."""
    vs = [p.strip() for p in re.split(r'(?<=॥)\s+(?!ਰਹਾਉ)(?=[^\s॥੦-੯])', u)]
    if len(vs) == 1: return vs, [t]
    ts = [p.strip() for p in re.split(r'(?<=\.)\s+(?!\|\|)(?!rahaa-o)', t)]
    assert len(ts) == len(vs), (u, t)
    return vs, ts


def build():
    L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8'))
    items, cur, a, pending = [], None, 0, []   # pending: heading lines waiting for the item they introduce

    def new(id_, y, n=''):
        nonlocal cur
        cur = {'id': id_, 'p': a - 1, 's': id_, 'y': y, 'n': n, 'v': [], 't': [], 'e': [], 'pg': None}
        items.append(cur)
        for h in pending: add(*h)
        pending.clear()

    def add(u, t, e, pg):
        vs, ts = split_padas(u, t)
        cur['v'] += vs; cur['t'] += ts; cur['e'].append(e); cur['pg'] = cur['pg'] or pg

    for j, x in enumerate(L):
        g, u = x['g'], to_unicode(x['g'])
        rahao_next = j + 1 < len(L) and 'rhwau' in L[j + 1]['g']
        line = (u, x['t'], x['e'], x['pg'])
        if 'mÚ' in g:                                   # the title
            a = 1; new('a01.title', 'heading'); add(*line); cur = None
        elif g == 'sloku ]':
            if items and items[-1]['id'] != 'a01.title': a += 1
            pending.append(line); new(f'a{a:02d}.salok', 'salok')
        elif g == 'AstpdI ]':
            pending.append(line); cur = None; k = 1
        elif rahao_next and cur is None:               # the Rahaa-o couplet: its second line ends "ਰਹਾਉ ॥"
            new(f'a{a:02d}.rahao', 'rahao'); add(*line)
        elif 'rhwau' in g:
            assert cur['y'] == 'rahao'
            add(*line); cur = None
        else:
            if cur is None:
                new(f'a{a:02d}.p{k}', 'pauri', str(k))
            elif cur['y'] == 'rahao':
                raise ValueError(cur)
            add(*line)
            m = re.search(r'॥([੦-੯]+)॥', u)
            if m and cur['y'] == 'pauri':
                num = int(''.join(str(ord(c) - 0x0A66) for c in m.group(1)))
                assert num == k, (cur['id'], u)
                k += 1; cur = None
            elif m and cur['y'] == 'salok':
                cur = None
    return items


def check(items):
    assert len({x['id'] for x in items}) == len(items)
    parts = sorted({x['p'] for x in items})
    assert parts == list(range(24)), parts
    for p in parts:
        its = [x for x in items if x['p'] == p]
        ps = [x for x in its if x['y'] == 'pauri']
        assert [x['n'] for x in ps] == [str(i) for i in range(1, 9)], (p, [x['id'] for x in its])
        last = ps[-1]['v'][-1]
        assert last.endswith('॥੮॥' + ''.join(chr(0x0A66 + int(d)) for d in str(p + 1)) + '॥'), last
        for x in ps:   # ten padas (pauri 1 also carries the heading ਅਸਟਪਦੀ ॥)
            assert len(x['v']) == (11 if x['n'] == '1' else 10), (x['id'], len(x['v']))
    return True


if __name__ == '__main__':
    its = build(); check(its)
    import collections
    print(len(its), collections.Counter(x['y'] for x in its))
    for x in its[:4]: print(json.dumps(x, ensure_ascii=False)[:600])
    print(collections.Counter(len(x['v']) for x in its if x['y'] == 'salok'))
