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
  A verse the owner has set by ear (owner.json), or a session by hand from 5-s windows (fixes.json), is not listed, but for
  those the session lists itself because the windows did not settle them (check.json → "also", the reason in fixes.md).
Prints the counts, for the recording's aligned.md.

A source timed line by line (mms/<video id>.json with "verses" and "lines", from line_align.py) also gets lines.json,
{video id: {item id: [[line, start, end], …]}}: every singing of every line MMS scores 0.5 or more, its start less the
lean, in time order; a verse's start in aligned.json is its first singing's. check.json then lists, for the owner's ear:
    title       what MMS hears (its letters) is unlike the verse, or more like another verse of the work: the recording may
                not sing the verse its title names;
    unsung      a line of the verse (not a heading) has no singing scored 0.5 or more;
    first       a line's first singing in the text's order differs by more than 2 s between the search for every singing
                and the plain in-order alignment, for more than a quarter of the verse's lines.
"""
import collections, json, os, statistics, sys

def by_line(src, lean, W):
    import line_align as LA
    meta = json.load(open(os.path.join(src, 'source.json')))
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IT = json.load(open(os.path.join(repo, 'library', meta['work'], 'work.json'), encoding='utf-8'))['items']
    TXT = {x['id']: ''.join(LA.rom(t) for t in (x.get('t') or [])) for x in IT}
    GR = {k: LA.trigrams(v) for k, v in TXT.items()}
    OWN = json.load(open(os.path.join(src, 'owner.json'))) if os.path.exists(os.path.join(src, 'owner.json')) else {}
    own = {k for v in OWN.values() for k in v}
    aligned, lines, flags = {}, {}, collections.defaultdict(set)
    n = collections.Counter(); order = []
    for w in W:
        p = os.path.join(src, 'mms', w['yt'] + '.json')
        if not os.path.exists(p): print(w['yt'], 'not aligned yet'); continue
        M = json.load(open(p))
        heard = LA.trigrams(M.get('read', ''))
        for it in w['items']:
            i = it['id']
            if i not in w['keep']: continue
            order.append(i)
            U, _ = LA.units(it)
            want = [u['k'] for u in U if u['rom'] and not u['head']]
            occ = M['lines'].get(i, [])
            good = [o for o in occ if o[3] >= 0.5]
            n['lines'] += len(want); n['singings'] += len(good); n['dropped'] += len(occ) - len(good)
            got = {o[0] for o in good}
            n['started'] += len([k for k in want if k in got])
            if [k for k in want if k not in got]: flags['unsung'].add(i)
            # the title: what is heard, against this verse and against the best other verse of the work
            like = len(heard & GR[i]) / max(1, len(heard))
            other = max((len(heard & g) / max(1, len(heard)), k) for k, g in GR.items() if k != i)
            if like < 0.5 or other[0] > like + 0.05: flags['title'].add(i); print(w['yt'], i, 'heard like', round(like, 2), '; most like', other[1], round(other[0], 2))
            first = {}
            for o in good: first.setdefault(o[0], o[1])
            ino = {o[0]: o[1] for o in M.get('inorder', {}).get(i, []) if o[3] >= 0.5}
            off = [k for k in first if k in ino and abs(first[k] - ino[k]) > 2]
            n['first differs'] += len(off)
            if len(off) > len(want) / 4: flags['first'].add(i)
            if good:
                aligned.setdefault(w['yt'], {})[i] = [round(max(0.0, good[0][1] - lean), 2), round(max(o[2] for o in good), 2)]
                lines.setdefault(w['yt'], {})[i] = [[o[0], round(max(0.0, o[1] - lean), 2), o[2]] for o in good]
    allf = {i for s in flags.values() for i in s} - own
    json.dump(aligned, open(os.path.join(src, 'aligned.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    json.dump(lines, open(os.path.join(src, 'lines.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    with open(os.path.join(src, 'check.json'), 'w', encoding='utf-8') as f:
        json.dump({'why': f"Verses the line-by-line checks flag, for the owner's ear: the recording may not sing the verse its title names, a line with no singing MMS scores 0.5 or more, or first singings that differ between the search for every singing and the in-order alignment (tools/audio/mms_merge.py, lean {lean} s).",
                   'ids': [i for i in order if i in allf]}, f, ensure_ascii=False, indent=1); f.write('\n')
    print(f"{n['started']} of {n['lines']} lines have a start; {n['singings']} singings (MMS scored {n['dropped']} more below 0.5, dropped); "
          f"first singings differing from the in-order alignment by more than 2 s: {n['first differs']}; verses flagged: " + ', '.join(f'{k} {len(v - own)}' for k, v in sorted(flags.items())) + f'; to check {len(allf)}')

def main(src, lean):
    W = json.load(open(os.path.join(src, 'mms', 'windows.json'), encoding='utf-8'))
    if any(w.get('items') for w in W): return by_line(src, lean, W)
    rough, order, rom = {}, collections.defaultdict(list), {}
    for w in W:
        for l in w['lines']:
            if l['id'] in w['keep']: rough[l['id']] = l['rough']; order[w['yt']].append(l['id']); rom[l['id']] = len(l['rom'].replace(' ', ''))
    OWN = json.load(open(os.path.join(src, 'owner.json'))) if os.path.exists(os.path.join(src, 'owner.json')) else {}
    FIX = json.load(open(os.path.join(src, 'fixes.json'))) if os.path.exists(os.path.join(src, 'fixes.json')) else {}
    # neither a start the owner set by ear nor one set by hand from 5-s windows (fixes.json, its windows in fixes.md) is left to check
    own = {k for v in OWN.values() for k in v} | {k for v in FIX.values() if isinstance(v, dict) for k in v}
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
    # a session may list a verse its windows did not settle (check.json → "also", the reason in fixes.md): kept, and listed
    prev = json.load(open(os.path.join(src, 'check.json'), encoding='utf-8')) if os.path.exists(os.path.join(src, 'check.json')) else {}
    also = [i for i in prev.get('also', []) if i not in {k for v in OWN.values() for k in v}]
    allf = ({i for s in flags.values() for i in s} - own) | set(also)
    ids_order = [i for yt in order for i in order[yt]]
    json.dump({yt: A for yt, A in aligned.items()}, open(os.path.join(src, 'aligned.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    with open(os.path.join(src, 'check.json'), 'w', encoding='utf-8') as f:
        json.dump({'why': f"Verses the automatic checks of tools/audio/METHOD.md step 4 flag, for the owner's ear: MMS's score below 0.5 (the transcript's start is kept), MMS and the transcript more than 2 s apart, a length out of pace with the verses around it, or a start before the verse before (tools/audio/mms_merge.py, lean {lean} s).",
                   'ids': [i for i in ids_order if i in allf], **({'also': also} if also else {})}, f, ensure_ascii=False, indent=1); f.write('\n')
    n = sum(len(A) for A in aligned.values())
    print(f'{n} starts from MMS (lean {lean} s) of {len(rough)} verses; flagged: ' + ', '.join(f'{k} {len(v - own)}' for k, v in sorted(flags.items())) + f'; to check {len(allf)}')

if __name__ == '__main__':
    a = sys.argv[1:]; lean = 0.6
    if '--lean' in a: k = a.index('--lean'); lean = float(a[k + 1]); a = a[:k] + a[k + 2:]
    main(os.path.abspath(a[0]), lean)
