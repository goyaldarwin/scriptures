"""Overlap check: is our meaning of a verse its own wording, or does it reuse a copyrighted source's?

Copyright protects wording, not meaning. Our meanings are written from the verse itself; this script proves, verse by
verse, that they do not reuse the copyrighted source's sentences (docs/handoff/2026-10-19-own-meanings.md, rule 4).

    python3 tools/meanings/overlap.py OURS THEIRS [--n 10] [--note 6] [--only PREFIX ...] [--report]

OURS and THEIRS are meaning files: a library source (`{"m": {id: [text, footnotes?]}}`) or a plain `{id: text}` map.
Only verses in both are compared, and only the meaning text (not footnotes).

Fails (exit 1) when any verse shares a run of N or more consecutive words with the other (default 10: a copied
sentence), after normalising: punctuation, quotation marks, brackets, dashes, verse numbers (।।१।।, digits), ZWNJ/ZWJ
and case are ignored; Devanagari nukta and candrabindu are kept (they are spelling). Runs of --note words or more
(default 6) up to N are listed, not failed: a person reads each beside the other meaning, keeps it when it is simply the
natural words or the verse's own list ("साम दान भय और भेद", "in my dream a monkey"), and rewrites it otherwise.
(The limit was 6 until the owner relaxed it on 2026-10-19: our meanings are made from the verse and its words, so a
natural phrase that happens to match is fine; rewriting it only to dodge the check made sentences less natural.)

It also lists (never fails on) sentences that are nearly one of theirs — the same words in the same order with a word
or two swapped (a name for a pronoun, a synonym), which breaks a run but is still their sentence (found in the pilot
review): a person reads each and rewrites it unless it is simply the natural sentence.
And it reports a looser signal, `close`: the longest common subsequence of words divided by our
length. A high value with no long run can still mean a sentence-by-sentence rewording, so --report lists the verses
above 0.6 for a person to read side by side.

Reviewed exceptions (a run that is unavoidable, e.g. a list of names in the verse's own order) go in
tools/meanings/overlap_allow.json: {"<item id>": ["<the shared run, normalised>", ...]}, each with a reason in git.

As a module: `check(ours, theirs, n=6)` returns [(id, run_words, close)] for every verse, longest run first.
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOW = os.path.join(HERE, 'overlap_allow.json')

_PUNCT = re.compile(r"[।॥|,.;:!?\-–—‘’“”'\"()\[\]{}<>/\\*_…·•]|[०-९0-9]+")
_JOIN = re.compile('[‌‍]')

def words(text):
    """Normalised word list of one meaning."""
    t = unicodedata.normalize('NFC', text)
    t = _JOIN.sub('', t).lower()
    return _PUNCT.sub(' ', t).split()

def text_of(v):
    if isinstance(v, str): return v
    if isinstance(v, list) and v and isinstance(v[0], str): return v[0]
    return ''

def load(path):
    d = json.load(open(path, encoding='utf-8'))
    m = d['m'] if isinstance(d, dict) and 'm' in d and isinstance(d['m'], dict) else d
    return {k: text_of(v) for k, v in m.items()}

def runs_at_least(a, b, n):
    """Every maximal shared run of n+ words (as word lists), longest first, without repeats."""
    L = [[0] * (len(b) + 2) for _ in range(len(a) + 2)]
    for i in range(len(a) - 1, -1, -1):          # L[i][j]: shared run starting at a[i], b[j]
        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]: L[i][j] = L[i + 1][j + 1] + 1
    out = set()
    for i in range(len(a)):
        for j in range(len(b)):
            if L[i][j] >= n and (i == 0 or j == 0 or L[i - 1][j - 1] == 0):   # maximal: not inside a longer run
                out.add(tuple(a[i:i + L[i][j]]))
    return [list(r) for r in sorted(out, key=len, reverse=True)]

def close(a, b):
    """Longest common subsequence of words / len(a)."""
    if not a or not b: return 0.0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[-1]))
        prev = cur
    return prev[-1] / len(a)

_SENT = re.compile(r'[।?!;.]+|\s—\s')

def sentences(text):
    """Normalised word lists of each sentence (split at । ? ! ; . and a spaced dash)."""
    return [w for w in (words(x) for x in _SENT.split(unicodedata.normalize('NFC', text))) if w]

def lcs(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]

def near_copies(t, u, min_words=8, ratio=0.75):   # shorter sentences that match are the verse's own words
    """Our sentences that are nearly one of theirs — the same words in the same order with a word or two swapped
    (a name for a pronoun, a synonym), which a run count misses: [(score, our sentence, their sentence)]."""
    out = []
    for a in sentences(t):
        if len(a) < min_words: continue
        best = max(((lcs(a, b) / max(len(a), len(b)), b) for b in sentences(u)), default=(0, []), key=lambda r: r[0])
        if best[0] >= ratio: out.append((round(best[0], 2), ' '.join(a), ' '.join(best[1])))
    return out

def phrase_share(t, u):
    """Share of our three-word phrases that also occur in theirs. A sentence-by-sentence rewording with only the
    subject or a word swapped keeps most of them, which a run count and the near-copy check miss (found in the
    Sukhmani review, 2026-10-23: a pauri that reused six of ten sentences with only its refrain changed). Not
    decisive alone — short verses and refrains share phrases naturally — so --report lists the highest for a reader."""
    tri = lambda ws: [tuple(ws[i:i + 3]) for i in range(len(ws) - 2)]
    a, b = tri(words(t)), set(tri(words(u)))
    return sum(1 for g in a if g in b) / len(a) if a else 0.0

def allowed():
    if not os.path.exists(ALLOW): return {}
    return {k: {' '.join(words(p)) for p in v} for k, v in json.load(open(ALLOW, encoding='utf-8')).items()}

def check(ours, theirs, n=10):
    """[(id, longest shared run as words, close)] for every verse in both; longest run first."""
    allow, res = allowed(), []
    for k, t in ours.items():
        if k not in theirs or not t or not theirs[k]: continue
        a, b = words(t), words(theirs[k])
        runs = [r for r in runs_at_least(a, b, 1) if ' '.join(r) not in allow.get(k, ())]
        run = runs[0] if runs else []
        res.append((k, run, close(a, b)))
    res.sort(key=lambda r: (-len(r[1]), -r[2]))
    return res

def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('ours'); ap.add_argument('theirs')
    ap.add_argument('--n', type=int, default=10, help='fail on a shared run of this many words (default 10)')
    ap.add_argument('--note', type=int, default=6, help='list shared runs of this many words or more (default 6)')
    ap.add_argument('--only', nargs='*', default=[], help='only item ids starting with these prefixes')
    ap.add_argument('--report', action='store_true', help='also list close rewordings and the distribution')
    a = ap.parse_args(argv)
    ours, theirs = load(a.ours), load(a.theirs)
    if a.only: ours = {k: v for k, v in ours.items() if k.startswith(tuple(a.only))}
    res = check(ours, theirs, a.n)
    bad = [r for r in res if len(r[1]) >= a.n]
    for k, run, c in bad:
        print(f'OVERLAP {k}: {len(run)} words shared: “{" ".join(run)}”')
    for k, run, c in res:
        if a.note <= len(run) < a.n: print(f'read {k}: {len(run)} words shared: “{" ".join(run)}”')
    near = [(k, nc) for k in ours if k in theirs for nc in near_copies(ours[k], theirs[k])]
    for k, (sc, x, y) in near: print(f'read {k}: a sentence nearly theirs ({sc}): “{x}” ~ “{y}”')
    if a.report:
        hist = {}
        for _, run, _ in res: hist[len(run)] = hist.get(len(run), 0) + 1
        print('longest shared run (words: verses):', dict(sorted(hist.items())))
        for k, run, c in sorted(res, key=lambda r: -r[2]):
            if c > 0.6: print(f'close {c:.2f} {k} (longest run {len(run)})')
        ps = sorted(((phrase_share(ours[k], theirs[k]), k) for k, _, _ in res), reverse=True)
        top = ps[:max(5, len(ps) // 6)]
        print('highest shares of shared three-word phrases (read these beside theirs):', ', '.join(f'{k} {v:.2f}' for v, k in top))
    print(f'{len(res)} verses compared, {len(bad)} with a shared run of {a.n}+ words, {len(near)} sentences nearly theirs to read')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
