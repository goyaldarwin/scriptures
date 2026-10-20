"""The order rule for audio timings — the same rule as the app (tools/site/app.js, buildAudio), kept in one place so the
app and make_timings.py can be checked against each other (tools/site/ux_test.py does so on every build).

keep_order(a, own, heard, lengths, dur) takes one recording's rows [item index, start, end-or-None] in text order and
returns the re-placed rows (in text order) and the indices of the verses that were moved:
- a verse set by ear (own) is used exactly as given;
- a set end later than the next set start (the nearest verse after it that was set by ear) is cut back to it;
- a verse not set by ear cannot start before the one before it has started, or before that verse's set end, or at or after
  the next set start: such a verse is placed again, by its text length, between the nearest good times on either side
  (when there is no room at all between them, at the next good start);
- starts only guessed by text length (never heard) next to a verse set by ear are guessed again between that verse's time
  (its end if set, else its start plus its length) and the next good start (or 98% of the recording), so they move with it.
Times are rounded to 0.1 s the way the app does (half up), so both give the same figures.
"""
import math

def r1(x): return math.floor(x * 10 + 0.5) / 10   # JavaScript's Math.round(x * 10) / 10

def keep_order(a, own, heard, lengths, dur):
    """a: [[i, start, end|None], …] in text order; own(i), heard(i): predicates on the item index; lengths(i): text length;
    dur: the recording's length in seconds. Returns (rows, moved) — rows in text order, moved a list of item indices."""
    a = [[i, s, e] for i, s, e in a]
    moved = []
    n_ = len(a)
    ln = lambda k: lengths(a[k][0])
    is_own = lambda k: own(a[k][0])
    def next_own(k):
        for j in range(k + 1, n_):
            if is_own(j): return a[j][1]
        return float('inf')
    for k in range(n_):
        if a[k][2] is not None and a[k][2] > next_own(k): a[k][2] = next_own(k)
    good, lo = [True] * n_, -1.0
    for k in range(n_):
        if not is_own(k) and (a[k][1] <= lo or a[k][1] >= next_own(k)): good[k] = False; continue
        lo = max(a[k][1], a[k][2] - 0.01 if a[k][2] is not None else -1)
    k = 0
    while k < n_:
        if good[k]: k += 1; continue
        e = k
        while e + 1 < n_ and not good[e + 1]: e += 1
        p, n = k - 1, e + 1
        L = max(a[p][1] + 0.5, a[p][2] if a[p][2] is not None else 0) if p >= 0 else 0.0
        U = a[n][1] if n < n_ else L + 4 * (e - k + 2)
        if U < L: L = U
        tot = sum(ln(j) for j in range(k, e + 1)) + (0 if n < n_ else ln(e)); acc = 0
        for j in range(k, e + 1):
            a[j][1] = r1(L + (U - L) * acc / tot); acc += ln(j); moved.append(a[j][0])
        k = e + 1
    gs = lambda k: not heard(a[k][0]) and not is_own(k)
    k = 0
    while k < n_:
        if not gs(k): k += 1; continue
        e = k
        while e + 1 < n_ and gs(e + 1): e += 1
        p, n = k - 1, e + 1
        if (p >= 0 and is_own(p)) or (n < n_ and is_own(n)):
            pre = ln(p) if p >= 0 and a[p][2] is None else 0
            L0 = (a[p][2] if a[p][2] is not None else a[p][1]) if p >= 0 else a[k][1]
            U = a[n][1] if n < n_ else dur * 0.98
            tot = pre + sum(ln(j) for j in range(k, e + 1)); acc = pre
            if U - L0 > 0.3 * (e - k + 1 + (1 if pre else 0)):
                for j in range(k, e + 1):
                    st = r1(L0 + (U - L0) * acc / tot); acc += ln(j)
                    if st != a[j][1]: a[j][1] = st; moved.append(a[j][0])
        k = e + 1
    return a, moved
