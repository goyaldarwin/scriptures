"""MMS's starts and ends (mms_align.py) → aligned.json and check.json for make_timings.py (tools/audio/METHOD.md, steps 2–4).

    python3 tools/audio/mms_merge.py tools/works/<work>/audio/<source> [--lean SECONDS]

- Each start is moved earlier by the recording's lean against the owner's by-ear starts (--lean; METHOD.md: 0.6 s until the
  owner has set 20 or so by ear on this recording, then the median of MMS's start minus his).
- A verse MMS scores below 0.5 keeps the transcript's start (it is left out of aligned.json).
- A verse's end is kept (aligned.json value [start, end]) when MMS heard it end; make_timings.py uses it only where the next
  verse starts more than 1.5 s later (a refrain, music, a pause), so the light leaves the verse when the reciting does.
- check.json lists, for the owner's ear, every verse the checks of step 4 flag:
    low score   MMS scored it below 0.5;
    disagree    MMS and the transcript's start (windows.json "rough") differ by more than 2 s;
    pace        its length (to the next start) for its letters is under half or over double the median of the 20 verses
                around it (an overrun shows as one verse too long and the next too short);
    order       it starts before the verse before it.
  A verse the owner has set by ear (owner.json) is never listed.
Prints the counts, for the recording's aligned.md.
"""
import collections, json, os, statistics, sys

def main(src, lean):
    W = json.load(open(os.path.join(src, 'mms', 'windows.json'), encoding='utf-8'))
    rough, order, rom = {}, collections.defaultdict(list), {}
    for w in W:
        for l in w['lines']:
            if l['id'] in w['keep']: rough[l['id']] = l['rough']; order[w['yt']].append(l['id']); rom[l['id']] = len(l['rom'].replace(' ', ''))
    OWN = json.load(open(os.path.join(src, 'owner.json'))) if os.path.exists(os.path.join(src, 'owner.json')) else {}
    own = {k for v in OWN.values() for k in v}
    aligned, flags = {}, collections.defaultdict(set)
    for yt, ids in order.items():
        p = os.path.join(src, 'mms', yt + '.json')
        if not os.path.exists(p): print(yt, 'not aligned yet'); continue
        M = json.load(open(p))
        A = aligned[yt] = {}
        for i in ids:
            if i not in M: continue
            st, en, sc = M[i]
            if sc < 0.5: flags['low score'].add(i); continue
            A[i] = [round(max(0.0, st - lean), 2), round(en, 2)]
            if rough[i] is not None and abs(A[i][0] - rough[i]) > 2: flags['disagree'].add(i)
        # pace and order on the starts make_timings will use: MMS's, else the transcript's
        S = [(i, A[i][0] if i in A else rough[i]) for i in ids]
        S = [x for x in S if x[1] is not None]
        for k in range(1, len(S)):
            if S[k][1] <= S[k - 1][1]: flags['order'].add(S[k][0])
        r = [(S[k][0], (S[k + 1][1] - S[k][1]) / max(8, rom[S[k][0]])) for k in range(len(S) - 1)]
        for k, (i, x) in enumerate(r):
            near = [y for _, y in r[max(0, k - 10):k + 11] if y > 0]
            m = statistics.median(near) if near else 0
            if m and (x < m / 2 or x > 2 * m): flags['pace'].add(i)
    allf = {i for s in flags.values() for i in s} - own
    ids_order = [i for yt in order for i in order[yt]]
    json.dump({yt: A for yt, A in aligned.items()}, open(os.path.join(src, 'aligned.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    with open(os.path.join(src, 'check.json'), 'w', encoding='utf-8') as f:
        json.dump({'why': f"Verses the automatic checks of tools/audio/METHOD.md step 4 flag, for the owner's ear: MMS's score below 0.5 (the transcript's start is kept), MMS and the transcript more than 2 s apart, a length out of pace with the verses around it, or a start before the verse before (tools/audio/mms_merge.py, lean {lean} s).",
                   'ids': [i for i in ids_order if i in allf]}, f, ensure_ascii=False, indent=1); f.write('\n')
    n = sum(len(A) for A in aligned.values())
    print(f'{n} starts from MMS (lean {lean} s) of {len(rough)} verses; flagged: ' + ', '.join(f'{k} {len(v - own)}' for k, v in sorted(flags.items())) + f'; to check {len(allf)}')

if __name__ == '__main__':
    a = sys.argv[1:]; lean = 0.6
    if '--lean' in a: k = a.index('--lean'); lean = float(a[k + 1]); a = a[:k] + a[k + 2:]
    main(os.path.abspath(a[0]), lean)
