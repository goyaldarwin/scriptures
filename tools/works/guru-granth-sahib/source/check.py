"""Checks text.txt (reconciliation.md §4): the structure always; the witnesses when given.

    python3 tools/works/guru-granth-sahib/source/check.py [--db DB] [--darpan FILE] [--faridkot-pdf PDF] [--out DIR]

1. Always (with the database): text.txt is what make.py makes; the Japji Sahib's and the Sukhmani Sahib's lines equal
   the database's (the Japji's Mool Mantar on four lines, the database's on one); every line is Gurmukhi and ends with ॥
   or a number mark (or is one of the Granth's closing words of a group: ਛਕਾ, ਜੁਮਲਾ, ਸੁਧੁ …); no bare vowel bearer;
   a whole bani cut into pauris numbers them 1, 2, 3 … without a gap.
2. The witnesses, word by word (scratch copies, never committed):
     --darpan FILE        Prof. Sahib Singh's Sri Guru Granth Darpan as `tools/meanings/teeka.py fetch` converts it
                          (~/.cache/scriptures-dict/darpan.txt): its Gurbani is set in a font whose text layer keeps the
                          visual order (the sihari ਿ before its letter, a pairin ਰ as ਰ੍ after it); those lines are put
                          in Unicode order here, then compared.
     --faridkot-pdf PDF   the Faridkot Teeka's PDF (scriptures-data, reference/pa/commentaries/faridkot-teeka/): its text
                          layer is the legacy encoding with ੳ/ਅ and ਣ/ਂ on swapped keys (A ਅ … in GurbaniAkhar is ੳ here),
                          converted here with those keys swapped; its Gurbani lines (a line that ends “ ॥” or with a
                          number mark and converts cleanly) are compared.
   Each witness's words are aligned with the text's by anchors (runs of six words found once in each), then word by
   word between anchors; a word of the text that the witness gives otherwise is a difference, listed with its verse in
   OUT/<witness>.tsv (decided in reconciliation.md and source/decisions.tsv). Where a witness gives nothing between two
   anchors (a line it leaves out, or its commentary) nothing is counted.
"""
import collections, difflib, os, re, subprocess, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE); WORKS = os.path.dirname(WORK)
sys.path.insert(0, HERE); import shabados, make
sys.path.insert(0, WORKS); import textfile
import gurmukhi   # on the path through shabados

CLOSING = re.compile(r'(ਛਕਾ|ਛਕੇ|ਜੁਮਲਾ|ਸੁਧੁ|ਦੁਤੁਕੇ|ਜੋੜੁ|ਪੈਤੀਸ|ਚਉਤੀਸ|ਅਸਟਪਦੀਆ|ਚਉਪਦੇ|ਮਹਲੇ ਚਉਥੇ ਕੇ|ਪੰਚਪਦੇ)')


def structure(T, U, V):
    own = [x for x in V if 'take' not in x]
    assert [x['v'] for x in T] == [[l['v'] for l in x['lines']] for x in own], 'text.txt is stale: run make.py'
    JAP, SUKH = make.takes(U)
    for work, ks in (('japji-sahib', JAP), ('sukhmani-sahib', SUKH)):
        mine = [l for x in textfile.read(os.path.join(WORKS, work, 'text.txt')) for l in x['v']]
        db = [l['v'] for k in sorted(ks) for l in U[k]['lines']]
        if work == 'japji-sahib': mine = [' '.join(mine[:4])] + mine[4:]
        assert mine == db, f'{work}: its lines differ from the database'
    odd = []
    for x in T:
        for l in x['v']:
            assert re.fullmatch(r'[਀-੿ ॥]+', l), (x['id'], l)
            assert not re.search(r'[ੳੲ](?![ਾਿੀੁੂੇੈੋੌ])', l.replace('ੳੁ', '')), (x['id'], l)
            if not (l.endswith('॥') or CLOSING.search(l)): odd.append((x['id'], l))
    for vid, l in odd: print(f'    a line that does not end with ॥: {vid} {l}')
    # pauris of a cut bani: 1, 2, 3 …
    runs, prev = [], None
    for x in V:
        if x.get('comp') and x['y'] == 'pauri':
            n = make.chain(x['lines'][-1]['v'])[0]
            if prev and prev[0] == x['comp']: assert n == prev[1] + 1, (x['comp'], prev, n)
            prev = (x['comp'], n)
    print(f'1. structure: {len(T)} verses of its own, {sum(len(x["v"]) for x in T)} lines; the Japji and Sukhmani '
          f'equal the database; every line Gurmukhi; {len(odd)} lines without a closing ॥ (the Granth prints them so)')


# ---- words, as compared ----
NUM = re.compile(r'॥?[੦-੯]+॥?')
# what the Darpan's Gurbani font loses or writes otherwise, folded on both sides so it is not taken for a difference: the
# half ਹ (ੑ), the kanna with bindi (left as a gap), the hora with an aunkar (ਗੋੁਪਾਲ: a private glyph for the hora), the
# pairin ਵ and ਹ, the yakash (written ਯ੍ਯ੍)
FOLD = [('ੑ', ''), ('ਾਂ', ' '), ('\uf02b', 'ੋ'), ('ੋੁ', 'ੋ'), ('੍ਵ', ''), ('੍ਹ', ''), ('ਯ੍ਯ੍', 'ੵ'), ('ò', ''), ('\u200d', ''), ('\u200c', '')]
FOLD += [(chr(c), '') for c in range(0xF040, 0xF060)]   # the small numerals some headings carry (ਪੰਚਪਦੇ₆), set as private glyphs
def words(s):
    s = unicodedata.normalize('NFC', s)
    for a, b in FOLD: s = s.replace(a, b)
    s = re.sub(r'[॥।{}\[\]()0-9੦-੯,;:.!?\-—–\'"‘’“”*]|ਪੰਨਾ', ' ', s)
    return [w for w in s.split() if re.search('[ਁ-ੴ]', w)]


def text_words(T, U):
    """The whole Granth's words in order, with the verse each is in (the taken banis from the database's lines)."""
    JAP, SUKH = make.takes(U)
    out, Ti = [], iter(T)
    V = make.verses([dict(u, lines=[dict(l) for l in u['lines']]) for u in U])
    for x in V:
        if 'take' in x:
            ks = sorted(JAP if x['take'] == 'japji' else SUKH)
            for k in ks:
                for l in U[k]['lines']:
                    out += [(w, f"{x['take']}:{l['ang']}") for w in words(l['v'])]
            continue
        t = next(Ti)
        for l in t['v']: out += [(w, t['id']) for w in words(l)]
    return out


# ---- the witnesses ----
SIG = re.compile(r'(^|[\sਾੀੁੂੇੈੋੌੰਂ])ਿ')   # a sihari after a space or a vowel sign: the visual order of the Darpan's Gurbani
CONS = '[ਕ-ਹੜੲੳਅ]'
def darpan_lines(path):
    L = open(path, encoding='utf-8').read().split('\n')
    g = [bool(SIG.search(l)) for l in L]
    keep = [g[i] or (0 < i < len(L) - 1 and g[i - 1] and g[i + 1]) for i in range(len(L))]
    out = []
    for i, l in enumerate(L):
        if not keep[i]: continue
        l = re.sub(r'\{ਪੰਨਾ[^}]*\}', ' ', l)
        l = re.sub(f'({CONS}[਼]?)ਰ੍', r'\1੍ਰ', l)                       # a pairin rara typed after its letter
        l = re.sub(f'ਿ({CONS}[਼]?(?:੍[ਰਹਵ]|[ੑੵ])?)', r'\1ਿ', l)            # the sihari after its letter
        l = re.sub(f'ਿ੍({CONS})', r'੍\1ਿ', l)                             # … and after a half letter under it (ਸ੍ਰਿਸ੍ਟਿ)
        l = l.replace('ਂ ੀ', 'ੀਂ').replace('ੰ ੀ', 'ੀੰ')                     # a bindi or tippi before its bihari (ਨੀਂਦ)
        l = re.sub(r'ੲ ੀ', 'ਈ', l)                                          # ਈਂ set as ੲ and a bihari after a gap
        out.append((i + 1, unicodedata.normalize('NFC', l)))
    return out


def faridkot_lines(pdf):
    raw = subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', pdf, '-'], capture_output=True, text=True, check=True).stdout
    T = dict(gurmukhi.TABLE)
    T['A'], T['a'], T['N'], T['x'] = gurmukhi.TABLE['a'], gurmukhi.TABLE['A'], gurmukhi.TABLE['x'], gurmukhi.TABLE['N']
    keep, gurmukhi.TABLE = gurmukhi.TABLE, T
    out = []
    try:
        for i, line in enumerate(raw.split('\n')):
            s = line.strip()
            if not re.search(r'(\s\]|\]\d+\](?:\d+\])*)\s*$', s) or re.search(r'[()!?:;,]', s): continue
            try: u = gurmukhi.to_unicode(re.sub(r'\s+', ' ', s))
            except ValueError: continue
            out.append((i + 1, unicodedata.normalize('NFC', u)))
    finally:
        gurmukhi.TABLE = keep
    return out


def align(A, B, n=6):
    """A: [(word, where)], B: [(word, line)] → the differences [(text words, witness words, where, witness line)]."""
    a = [w for w, _ in A]; b = [w for w, _ in B]
    def grams(s):
        c = collections.Counter(tuple(s[i:i + n]) for i in range(len(s) - n + 1)); pos = {}
        for i in range(len(s) - n + 1):
            g = tuple(s[i:i + n])
            if c[g] == 1: pos[g] = i
        return pos
    ga, gb = grams(a), grams(b)
    pairs = sorted((ga[g], gb[g]) for g in ga.keys() & gb.keys())
    # the longest chain increasing in both (patience LIS on the witness positions)
    import bisect
    tails, prev, idx = [], [None] * len(pairs), []
    for k, (_, j) in enumerate(pairs):
        p = bisect.bisect_left(tails, j)
        if p == len(tails): tails.append(j); idx.append(k)
        else: tails[p] = j; idx[p] = k
        prev[k] = idx[p - 1] if p else None
    chain, k = [], idx[-1] if idx else None
    while k is not None: chain.append(pairs[k]); k = prev[k]
    chain.reverse()
    diffs, ia, ib, covered = [], 0, 0, 0
    for (i, j) in chain + [(len(a), len(b))]:
        if i < ia or j < ib: continue
        sa, sb = a[ia:i], b[ib:j]
        if sa and sb and len(sb) <= 3 * len(sa) + 6:
            sm = difflib.SequenceMatcher(None, sa, sb, autojunk=False)
            for op, x1, x2, y1, y2 in sm.get_opcodes():
                if op == 'equal': covered += x2 - x1; continue
                if op == 'insert': continue                         # the witness has more: its commentary, or a heading
                if op == 'delete' and (x2 - x1) > 3: continue      # the witness leaves out a stretch: not compared
                diffs.append((' '.join(sa[x1:x2]), ' '.join(sb[y1:y2]), A[ia + x1][1], B[ib + y1][1] if y1 < len(sb) else B[ib + y1 - 1][1]))
        step = min(n, len(a) - i)
        covered += step; ia, ib = i + step, j + step
    return diffs, covered


def kind(d, witness=''):
    """A difference's kind: 'division' (the same letters, divided into words otherwise), 'heading' (the witness does not
    print a heading or ੴ line), 'unaligned' (the witness's words there are its commentary: nothing alike), 'word'."""
    a, b = d[0], d[1]
    if a.replace(' ', '') == b.replace(' ', ''): return 'division'
    if not b: return 'heading' if 'ੴ' in a or re.search('ਮਹਲਾ|ਰਾਗੁ|ਸਲੋਕ|ਪਉੜੀ', a) else 'omitted'
    if abs(len(a.split()) - len(b.split())) > 1 or difflib.SequenceMatcher(None, a, b).ratio() < 0.6: return 'unaligned'
    bare = lambda x: sorted(re.sub(r'[ੁੂੰਂ\s◌]|[^਀-੿]', '', x))
    if sorted(a.replace(' ', '')) == sorted(b.replace(' ', '')): return 'order'       # the same signs, set in another order
    if bare(a) == bare(b) and len(b) < len(a): return 'lost'   # an aunkar, dulainkar or nasal the witness's font drops
    sub = lambda x, y: (lambda it: all(c in it for c in x))(iter(y))   # x's letters, in order, within y
    if witness == 'darpan' and (re.search(r'[^਀-੿\s]', b) or 'ੲ ੀ' in b or 'ਯ੍' in b or sub(b.replace(' ', ''), a)):
        return 'font'   # the Darpan's font: a stray glyph, ਈ split, a yakash set as ਯ੍, a ligature (ਲੁੰ) dropped
    return 'word'


DECIDE = {'word': 'the text kept: one witness alone, the other reading with the text (§3)',
          'division': 'the text kept: the witness divides the words otherwise (§3)',
          'lost': "the text kept: the witness's font drops the sign (§3)",
          'order': "the text kept: the witness's font sets the signs in another order (§3)",
          'font': "the text kept: the witness's font sets the word otherwise (§3)"}
def ang_key(v):
    m = re.match(r'(\d+)\.(\d+)$', v)
    return (int(m.group(1)), int(m.group(2))) if m else (int(re.sub(r'\D', '', v) or 0), 0)


def main(argv):
    db = argv[argv.index('--db') + 1] if '--db' in argv else shabados.EXTRACT   # the committed extract, or the database
    U = shabados.units(db); V = make.verses([dict(u, lines=[dict(l) for l in u['lines']]) for u in U])
    T = textfile.read(os.path.join(WORK, 'text.txt'))
    structure(T, shabados.units(db), V)
    out = argv[argv.index('--out') + 1] if '--out' in argv else os.path.join(os.path.expanduser('~'), '.cache', 'scriptures-dict', 'ggs-check')
    wit = []
    if '--darpan' in argv: wit.append(('darpan', darpan_lines(argv[argv.index('--darpan') + 1])))
    if '--faridkot-pdf' in argv: wit.append(('faridkot', faridkot_lines(argv[argv.index('--faridkot-pdf') + 1])))
    if not wit: return
    A = text_words(T, shabados.units(db))
    os.makedirs(out, exist_ok=True)
    rec = []
    for name, lines in wit:
        B = [(w, ln) for ln, l in lines for w in words(l)]
        diffs, cov = align(A, B)
        kinds = collections.Counter(kind(d, name) for d in diffs)
        with open(os.path.join(out, name + '.tsv'), 'w', encoding='utf-8') as f:
            for d in diffs: f.write('\t'.join([kind(d, name)] + list(map(str, d))) + '\n')
        print(f'   by kind: {dict(kinds)}')
        rec += [(d[2], d[0], name, d[1], kind(d, name)) for d in diffs if kind(d, name) in DECIDE]
        print(f'2. {name}: {len(A)} words in the text, {len(B)} in the witness\'s Gurbani lines; {cov} words of the text '
              f'compared ({100 * cov / len(A):.1f}%), {len(diffs)} differences → {out}/{name}.tsv')
    if '--record' in argv and len(wit) == 2:   # every difference of a word, with its decision (reconciliation.md §3)
        key = lambda r: (r[0], r[1])
        agree = collections.Counter(key(r) for r in rec if r[4] == 'word')
        with open(os.path.join(HERE, 'differences.tsv'), 'w', encoding='utf-8') as f:
            f.write('# verse\ttext\twitness\twitness reads\tkind\tdecision   (made by check.py --record; reconciliation.md §3)\n')
            for r in sorted(rec, key=lambda r: (ang_key(r[0]), r[2])):
                f.write('\t'.join(r) + '\t' + DECIDE[r[4]] + '\n')
        print(f'   recorded {len(rec)} differences in source/differences.tsv')


if __name__ == '__main__':
    main(sys.argv[1:])
