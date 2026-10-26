"""Checks the Gurmukhi conversion of every printed line (source/lines.json) — run it after extract.py.

1. Conversion: every legacy line converts without an unknown character, and the result contains no bare vowel
   bearer (ੳ ੲ without their vowel sign) and nothing outside the Gurmukhi block, digits, ॥ and spaces.
2. Consonant skeleton against the PDF's own transliteration line. Both sides are reduced to the sequence of
   their consonants, by place of articulation (ਕ ਖ = k kh → K; ਤ ਥ ਟ ਠ = t th → T; ਦ ਧ ਡ ਢ = d Dh dh → D; ਰ ੜ = r rh → R …),
   ignoring vowels. A tippi/bindi may be read as n, m or nothing; a doubled consonant (addak) may be written
   twice; "bh", "rh", "kh" … may also be a letter followed by ਹ (ਕਬਹੂ kabhoo, ਪਰਹਰੈ parharai); ਞ is "nj". Any line whose skeletons still differ is printed, and is listed with its explanation in
   reconciliation.md → "Skeleton exceptions". The check fails on any line not listed there.
3. Optional witnesses (not committed, scratch copies; see reconciliation.md):
     --shabados <database.sqlite>   the Shabad OS database (@shabados/database on npm): its Sukhmani Sahib bani,
                                    in the same ASCII encoding, compared letter by letter with the PDF's
     --gurmukhi-utils <package dir> an independent ASCII→Unicode converter (gurmukhi-utils on npm, run with node),
                                    compared with ours on every line
Usage: python3 tools/works/sukhmani-sahib/source/check.py [--shabados DB] [--gurmukhi-utils DIR]
"""
import json, os, re, sys, unicodedata, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gurmukhi import to_unicode

HERE = os.path.dirname(os.path.abspath(__file__))

GCLASS = {}
for cls, letters in {'K': 'ਕਖ', 'G': 'ਗਘ', 'C': 'ਚਛ', 'J': 'ਜਝ', 'N': 'ਙਞਣਨ', 'T': 'ਟਠਤਥ', 'D': 'ਡਢਦਧ', 'P': 'ਪਫ',
                     'B': 'ਬਭ', 'M': 'ਮ', 'Y': 'ਯੵ', 'R': 'ਰੜ', 'L': 'ਲ', 'V': 'ਵ', 'S': 'ਸ', 'H': 'ਹੑ', '~': 'ੰਂ'}.items():
    for c in letters: GCLASS[c] = cls
TDIGRAPH = [('chh', 'C'), ('ch', 'C'), ('kh', 'K'), ('gh', 'G'), ('jh', 'J'), ('th', 'T'), ('dh', 'D'), ('bh', 'B'),
            ('rh', 'R'), ('ph', 'P')]
TSINGLE = {'k': 'K', 'g': 'G', 'j': 'J', 't': 'T', 'd': 'D', 'p': 'P', 'f': 'P', 'b': 'B', 'm': 'M', 'n': 'N',
           'r': 'R', 'l': 'L', 'v': 'V', 'w': 'V', 's': 'S', 'h': 'H'}


def gskel(u):
    u = unicodedata.normalize('NFD', u).replace('ਮਃ', 'ਮਹਲਾ').replace('ੴ', 'ਇਕਓਅੰਕਾਰ')
    return [x for c in u if c in GCLASS for x in (['N', 'J'] if c == 'ਞ' else [GCLASS[c]])]


def tskel(t):
    t = re.sub(r'\|\|[\d|]*\|\|', ' ', t).replace('N', '')     # verse numbers; a raised N marks nasalisation
    t = t.lower()
    out, i = [], 0
    while i < len(t):
        for dg, c in TDIGRAPH:
            if t.startswith(dg, i): out.append(c + ('|' + TSINGLE.get(dg[0], c) if dg.endswith('h') else '')); i += len(dg); break
        else:
            ch = t[i]
            if ch == 'y':   # "ay" is the vowel ੇ; y after a hyphen or at a word start is the consonant ਯ / yakash
                if i == 0 or not t[i - 1].isalpha(): out.append('Y')
            elif ch in TSINGLE: out.append(TSINGLE[ch])
            i += 1
    return out


def distance(g, t):
    """Edit distance where a nasal '~' may match n/m or vanish, and a repeated consonant in t costs nothing."""
    INF = 10 ** 9
    D = [[INF] * (len(t) + 1) for _ in range(len(g) + 1)]
    D[0][0] = 0
    for a in range(len(g) + 1):
        for b in range(len(t) + 1):
            d = D[a][b]
            if d == INF: continue
            if a < len(g):   # skip a Gurmukhi token
                D[a + 1][b] = min(D[a + 1][b], d + (0 if g[a] == '~' else 1))
            if b < len(t):   # skip a transliteration token
                free = b > 0 and t[b][0] == t[b - 1][0]
                D[a][b + 1] = min(D[a][b + 1], d + (0 if free else 1))
            if a < len(g) and b < len(t):
                ok = g[a] == t[b][0] or (g[a] == '~' and t[b][0] in 'NM')
                D[a + 1][b + 1] = min(D[a + 1][b + 1], d + (0 if ok else 1))
                if '|' in t[b] and a + 1 < len(g) and g[a] == t[b][2] and g[a + 1] == 'H':   # "bh" read as ਬ + ਹ
                    D[a + 2][b + 1] = min(D[a + 2][b + 1], d)
    return D[len(g)][len(t)]


ALLOWED = re.compile(r'^[ਁ-ੵ ॥।]*$')


def main(argv):
    L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8'))
    exc = {}
    rp = os.path.join(HERE, '..', 'reconciliation.md')
    if os.path.exists(rp):   # "- `legacy line` — reason" lines under the heading "Skeleton exceptions"
        sec = open(rp, encoding='utf-8').read().split('## Skeleton exceptions', 1)
        if len(sec) > 1:
            for m in re.finditer(r'^- `([^`]+)`', sec[1].split('\n## ', 1)[0], re.M): exc[m.group(1)] = True
    bad, flagged = [], []
    for x in L:
        u = to_unicode(x['g'])
        if not ALLOWED.match(u) or re.search(r'[ੳੲ](?![ੁੂੋਿੀੇ])', u): bad.append((x['pg'], x['g'], u))
        d = distance(gskel(u), tskel(x['t']))
        if d: flagged.append((d, x['pg'], x['g'], u, x['t']))
    print(f'1. conversion: {len(L)} lines, {len(bad)} with a problem')
    for b in bad: print('   ', b)
    unexplained = [f for f in flagged if f[2] not in exc]
    print(f'2. skeleton vs transliteration: {len(L) - len(flagged)} of {len(L)} lines agree; '
          f'{len(flagged)} differ ({len(flagged) - len(unexplained)} explained in reconciliation.md)')
    for f in flagged: print(('    ' if f[2] in exc else '  ! ') + f'p{f[1]} d={f[0]}  {f[3]}  |  {f[4]}  |  {f[2]}')
    ok = not bad and not unexplained

    if '--shabados' in argv:
        import sqlite3, difflib
        db = sqlite3.connect(argv[argv.index('--shabados') + 1])
        bid = db.execute("select id from banis where name_english='Sukhmani Sahib'").fetchone()[0]
        ref = [r[0] for r in db.execute('select l.gurmukhi from bani_lines bl join lines l on l.id=bl.line_id '
                                        'where bl.bani_id=? order by l.order_id', (bid,))]
        strip = lambda s: re.sub(r'\s+', ' ', re.sub(r'[;.,]', '', s)).strip()   # vishraam marks
        A = ' '.join(strip(x['g']) for x in L).split(); B = ' '.join(strip(r) for r in ref).split()
        sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
        diffs = [(op, ' '.join(A[i1:i2]), ' '.join(B[j1:j2]), ' '.join(A[max(0, i1 - 4):i1])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
        print(f'3a. Shabad OS witness: {len(A)} words in the PDF, {len(B)} in Shabad OS; {len(diffs)} differences')
        for d in diffs: print(f'    {d[0]:8} PDF {d[1]!r:30} Shabad OS {d[2]!r:30} after “{d[3]}”')
    if '--gurmukhi-utils' in argv:
        pkg = os.path.abspath(argv[argv.index('--gurmukhi-utils') + 1])
        js = "const g=require(process.argv[1]);const L=JSON.parse(require('fs').readFileSync(0,'utf8'));" \
             "process.stdout.write(JSON.stringify(L.map(s=>g.toUnicode(s))))"
        theirs = json.loads(subprocess.run(['node', '-e', js, pkg], input=json.dumps([x['g'] for x in L]),
                                           capture_output=True, text=True, check=True).stdout)
        n = 0
        for x, t in zip(L, theirs):
            mine = to_unicode(x['g']); t = unicodedata.normalize('NFC', t)
            if mine != t:
                n += 1; print(f'    p{x["pg"]}  ours {mine}  | gurmukhi-utils {t}  | {x["g"]}')
        print(f'3b. gurmukhi-utils witness: {len(L) - n} of {len(L)} lines identical, {n} differ')
    if not ok: sys.exit('CHECK FAILED')


if __name__ == '__main__':
    main(sys.argv[1:])
