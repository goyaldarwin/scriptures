"""A verse's number as it is cited: one rule per work, the one source of every number the app shows or finds.

Every number a reader sees for a verse comes from here: the player ("Verse 106.3", "Mantra 2.1.1"), Resume, the
footer's ranges, a verse's place, the number search ("2.1.1", "106.3", "दोहा ४५") and the number at the end of our
meanings where the verse prints none (the Śrī Rudram). The exporter (tools/works/export.py) writes it into every item as
`c`; the app reads `c` and never builds a number of its own; tools/site/library.py checks it (`check`).

The hierarchy of a work is part › section › verse (docs/LIBRARY.md §2). An item's `n` is its number at its own level,
as the book prints it (॥१॥ at the end of the Kaṭha's 1.1.1 → n "1"; a dohā ॥१०६॥ → n "106"). The citation joins the
levels the work names, with ".":

    work.json → "cite": {
      "by":    ["part", "sec", "n"],     the levels, in order (default ["n"]):
                                         part: the part's key (the Kaṭha's adhyāyas are keyed "1", "2");
                                         sec:  the number the section id ends with (v1.2 → 2, nam-a03 → 3), left out when
                                               it has none or it is 0 (the Mānas's opening ślokas, section "0");
                                         n:    the verse's own number.
      "types": {"do": ["n"]},            per verse type, other levels (a dohā is cited by its own number)
      "sec":   {"hi": "दोहा", "en": "Doha"},   the name of a numbered section (the Mānas counts by dohā); without it a
                                         section is never called by a number of its own
      "word":  {"cau": {"hi": "पद", "en": "Verse"}},   the word the player and Resume use for a type instead of its
                                         name, where the name would not fit ("Verse 106.3": the third verse under Doha 106)
      "mark":  "sec"                     what the number printed at a verse's end counts: "n" (default) the verse, "sec"
                                         its section (the Śrī Rudram prints only the anuvāka's number, at its end)
      "repeat": ["aranya.20.cha1_2"]     verses the book itself numbers again, as another verse of the same type before
                                         them in the same section (a second run of chhands under one dohā starts at 1)
    }

A verse taken from another work keeps that work's citation: its number is its place in its own work (the Mānas's
chhand ॥१॥ after dohā 236, in the Kṛpālu stuti, is Chhand 236.1). A verse without `n` has no citation (c ""): it is named by its type alone (Shanti Mantra, Closing words).
Checks (library.py): within a part (and a named section, work.json → sections), no two numbered verses of one type
share a citation, so every number the app shows finds exactly one verse (but those in `repeat`); and the number a verse prints at its end is the level `mark` names.
"""
import json, re

DIGITS = str.maketrans('०१२३४५६७८९੦੧੨੩੪੫੬੭੮੯', '01234567890123456789')
LEVELS = ('part', 'sec', 'n')

def rule(M):
    """The work's citation rule (work.json → cite), with its defaults, checked."""
    C = M.get('cite') or {}
    assert isinstance(C, dict), 'cite must be an object'
    bad = set(C) - {'by', 'types', 'sec', 'word', 'mark', 'repeat'}
    assert not bad, f'cite: unknown keys {sorted(bad)}'
    by = C.get('by', ['n']); types = C.get('types', {})
    for lv in [by] + list(types.values()):
        assert isinstance(lv, list) and lv and set(lv) <= set(LEVELS) and lv[-1] == 'n', f'cite: levels {lv} must be of {LEVELS} and end with n'
    assert C.get('mark', 'n') in ('n', 'sec'), 'cite: mark is "n" or "sec"'
    assert isinstance(C.get('repeat', []), list), 'cite: repeat is a list of verse ids'
    return {'by': by, 'types': types, 'mark': C.get('mark', 'n'), 'repeat': set(C.get('repeat', []))}

def sec_num(s):
    """The number a section id ends with, '' for none or 0: '106' → '106', 'v1.2' → '2', 'nam-a03' → '3', '0' → ''."""
    m = re.search(r'(\d+)$', s or '')
    return str(int(m.group(1))) if m and int(m.group(1)) else ''

def of(item, R, part_key):
    """The citation of one item: '106.3', '2.1.1', '3क', '' (no number)."""
    n = (item.get('n') or '').translate(DIGITS)
    if not n: return ''
    val = {'part': str(part_key or ''), 'sec': sec_num(item.get('s')), 'n': n}
    return '.'.join(val[lv] for lv in R['types'].get(item['y'], R['by']) if val[lv])

def compute(items, M):
    """Write `c` into every item, by the work's rule."""
    R = rule(M); keys = [p.get('key') for p in M['parts']['list']]
    for it in items: it['c'] = of(it, R, keys[it['p']] if it['p'] < len(keys) else '')

def printed(item):
    """The number printed at the end of the verse's last line (॥२९॥ → '29', ॥३० (क)॥ → '30क', ॥१३अ॥ → '13अ', ॥੮॥੧॥ → '8'), or ''."""
    m = re.search(r'॥\s*([0-9०-९੦-੯]+)(?:\s*\(([^()\s]{1,4})\)|([^\s॥()0-9०-९੦-੯]{1,2}))?॥(?:[^॥]*॥)*\s*$', item['v'][-1]) if item.get('v') else None
    return (m.group(1) + (m.group(2) or m.group(3) or '')).translate(DIGITS) if m else ''

def check(w):
    """Problems with a library work's citations: [message, …]."""
    out = []
    try: R = rule(w)
    except AssertionError as e: return [str(e)]
    seen = {}
    ids = {it['id'] for it in w['items']}
    out += [f'cite: repeat names {x}, which is not a verse' for x in sorted(R['repeat'] - ids)]
    for it in w['items']:
        if 'c' not in it: out.append(f"{it['id']}: no citation c (export through tools/works/export.py)"); continue
        if it.get('n') and not it['c']: out.append(f"{it['id']}: n {it['n']!r} but no citation")
        if it['c']:
            k = (it['p'], json.dumps((w.get('sections') or {}).get(it['s'])), it['y'], it['c'])
            if k in seen and it['id'] not in R['repeat']: out.append(f"{it['id']}: cited {it['y']} {it['c']} like {seen[k]} in the same part")
            seen[k] = it['id']
        p = printed(it)
        if not p and it.get('v') and re.search(r'॥[^॥]*[0-9०-९੦-੯][^॥]*॥\s*$', it['v'][-1]):
            out.append(f"{it['id']}: its number mark is not written as the others (॥१॥, ॥३ (क)॥, ॥१३अ॥): {it['v'][-1][-14:]}")
        if p and it.get('n'):
            want = sec_num(it.get('s')) if R['mark'] == 'sec' else it['n'].translate(DIGITS)
            if want and p != want: out.append(f"{it['id']}: the verse prints ॥{p}॥ but its {'section' if R['mark'] == 'sec' else 'n'} is {want!r}")
    return out

# ---- cases the build checks (tools/site/library.py), each a mistake this module must never make ----
_MANAS = {'cite': {'by': ['sec', 'n'], 'types': {'do': ['n'], 'so': ['n']}}, 'parts': {'list': [{'key': 'bal'}]}}
_KATHA = {'cite': {'by': ['part', 'sec', 'n']}, 'parts': {'list': [{'key': '1'}, {'key': '2'}]}}
CASES = [
    (_MANAS, {'p': 0, 's': '106', 'y': 'cau', 'n': '3'}, '106.3'),       # a chaupai under its doha
    (_MANAS, {'p': 0, 's': '106', 'y': 'do', 'n': '106'}, '106'),        # the doha by its own number
    (_MANAS, {'p': 0, 's': '3', 'y': 'do', 'n': '३क'}, '3क'),            # Devanagari digits, a lettered doha
    (_MANAS, {'p': 0, 's': '0', 'y': 'shloka', 'n': '1'}, '1'),          # the opening ślokas: section 0 is no number
    (_MANAS, {'p': 0, 's': 'end', 'y': 'shloka', 'n': '2'}, '2'),
    (_KATHA, {'p': 1, 's': 'v2.1', 'y': 'mantra', 'n': '1'}, '2.1.1'),   # adhyāya.vallī.mantra, from the part key and the section
    (_KATHA, {'p': 0, 's': 'shanti', 'y': 'shanti', 'n': ''}, ''),       # no number: no citation
    ({'parts': {'list': [{}]}}, {'p': 0, 's': 'sh13a', 'y': 'shloka', 'n': '13अ'}, '13अ'),   # the default: the verse's own number
]

def selftest():
    bad = []
    for M, it, want in CASES:
        got = of(dict(it), rule(M), M['parts']['list'][it['p']].get('key'))
        if got != want: bad.append((f'{it}', want, got))
    w = {'parts': {'list': [{}]}, 'items': [{'id': 'a', 'p': 0, 's': 'x', 'y': 'pad', 'n': '1', 'c': '1', 'v': ['… ॥२॥']},
                                            {'id': 'b', 'p': 0, 's': 'y', 'y': 'pad', 'n': '1', 'c': '1', 'v': ['…']}]}
    w['items'].append({'id': 'c', 'p': 0, 's': 'z', 'y': 'do', 'n': '101क', 'c': '101क', 'v': ['… ॥१०१ क॥']})   # a lettered number without brackets
    if len(check(w)) != 3: bad.append(('check: a printed number that is not n, a number cited twice, a mark written otherwise', 3, check(w)))
    return bad
