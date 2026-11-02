"""Compare Gita Press with a witness, Kanda by Kanda, independent of how either divides sargas.

1. Every Gita Press line is matched to its most similar witness line (normalised); confident matches
   (similarity >= 88) that keep both texts in order (longest increasing run) are anchors.
2. Each Gita Press sarga is compared letter by letter with the witness lines its anchors span
   (extended to the sarga's first and last line).
"""
import json, sys, numpy as np
sys.path.insert(0, sys.argv[1]); import align
from rapidfuzz import fuzz, process

B = {k['kanda']: k for k in json.load(open(sys.argv[2]))}
W = json.load(open(sys.argv[3])); kind = sys.argv[5]

def wit_lines(k):
    out = []
    for s in k['sargas']:
        for v in s['verses']:
            ls = v['text']['dv'] if kind == 'iitk' else v['sanskrit']
            for h in align.halves(' '.join(ls)):
                out.append(((s['number'], v.get('refs')), h))
    return out

def lis(pairs):
    """longest run of pairs increasing in both coordinates (pairs sorted by the first)"""
    import bisect
    tails, idx, prev = [], [], [None] * len(pairs)
    for i, (_, w) in enumerate(pairs):
        k = bisect.bisect_left(tails, w)
        if k == len(tails): tails.append(w); idx.append(i)
        else: tails[k] = w; idx[k] = i
        prev[i] = idx[k - 1] if k else None
    out, i = [], idx[-1] if idx else None
    while i is not None:
        out.append(pairs[i]); i = prev[i]
    return out[::-1]

out, stats, cover = [], [], []
for ki, k in enumerate(W['kandas']):
    kd = align.KANDAS[ki]
    WL = wit_lines(k); WN = [align.norm_line(l) for _, l in WL]
    G = [(si, n, l) for si, s in enumerate(B[kd]['sargas']) for n, l in align.gp_lines(s)]
    GN = [align.norm_line(l) for _, _, l in G]
    pairs = []
    for c0 in range(0, len(GN), 2000):
        M = process.cdist(GN[c0:c0 + 2000], WN, scorer=fuzz.ratio, workers=-1, dtype=np.uint8)
        best = M.argmax(axis=1)
        for r, j in enumerate(best):
            if M[r, j] >= 88:
                pairs.append((c0 + r, int(j)))
    anchors = lis(pairs)
    amap = dict(anchors)
    agp = sorted(amap)
    import bisect
    for si, s in enumerate(B[kd]['sargas']):
        rows = [i for i, g in enumerate(G) if g[0] == si]
        a, b = rows[0], rows[-1]
        inside = [i for i in agp[bisect.bisect_left(agp, a):bisect.bisect_right(agp, b)]]
        if not inside:
            stats.append((kd, si + 1, None, None)); continue
        j0 = max(0, amap[inside[0]] - (inside[0] - a))
        j1 = min(len(WL) - 1, amap[inside[-1]] + (b - inside[-1]))
        d, r = align.diff([(G[i][1], G[i][2]) for i in rows], [l for _, l in WL[j0:j1 + 1]])
        stats.append((kd, si + 1, round(r, 4), len(d), len(inside), len(rows)))
        for x in d:
            x.update(kanda=kd, sarga=si + 1); out.append(x)
json.dump({'stats': stats, 'diffs': out}, open(sys.argv[4], 'w'), ensure_ascii=False)
print(len(out), 'differences')
print('no anchors:', [s[:2] for s in stats if s[2] is None])
print('lowest:', sorted([s for s in stats if s[2] is not None], key=lambda x: x[2])[:10])
for kd in align.KANDAS:
    print(kd, sum(x[3] or 0 for x in stats if x[0] == kd))
