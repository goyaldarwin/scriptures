"""Make an audio source: transcripts → library/<work>/audio/<id>.json (verse start times).

Usage:  python3 tools/audio/make_timings.py tools/works/<work>/audio/<source-id>

The source folder holds:
  source.json      {"id", "work": "<library path>", "type": "youtube", "title": {"hi", "en"}, "order"?, "draft"?: "<why it is not published yet>", "align"?: "anchors", "fill"?: n, "anchor_min"?: 0.45, "estimate"?: true}
  recordings.json  [{"yt": video id, "file": original file name, "dur": seconds, "order": n}]
  transcripts/     <video id>.jsonl from transcribe.py (+ .done when finished)
  fixes.json       optional hand-checked verse starts {video id: {item id: seconds}}, with the evidence in fixes.md
Only finished transcripts are used. The alignment is cached per recording in transcripts/<video id>.align.json:
one row per transcript segment, [start, end, [[item id, characters of that half-line], …]]. Delete it to realign.
A segment that covers several half-lines is shared among them by length, so a verse that begins in the
middle of a long breath gets the time it begins, not the time the breath begins.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.environ.get('SCRIPTURES_REPO') or os.path.dirname(os.path.dirname(HERE))   # SCRIPTURES_REPO: a copy to work in (tests)
sys.path.insert(0, HERE)
import align as A
import order as O

SRC = os.path.abspath(sys.argv[1]); TR = os.path.join(SRC, 'transcripts')
meta = json.load(open(os.path.join(SRC, 'source.json')))
REC = sorted(json.load(open(os.path.join(SRC, 'recordings.json'))), key=lambda r: r['order'])
work = json.load(open(os.path.join(REPO, 'library', meta['work'], 'work.json')))
IT = work['items']; ID = {x['id']: i for i, x in enumerate(IT)}
# work.json "renamed" (old id → new id, e.g. a joint caupāī split into one item each): an old id in an alignment cache,
# fixes.json, owner.json or recordings.json counts as its new id; the later parts of a split verse are placed by length
import re
SPLIT = {}   # old id of a split joint caupāī → its new items (indices), in order
for old, new in work.get('renamed', {}).items():
    if old not in ID and new in ID:
        ID[old] = ID[new]
        m = re.fullmatch(r'(.+\.cau)(\d+)-(\d+)', old)
        if m: SPLIT[old] = [ID[m.group(1) + str(n)] for n in range(int(m.group(2)), int(m.group(3)) + 1) if m.group(1) + str(n) in ID]
A.init(IT)

# where each reading day starts (any plan): the start of a recording may be back-filled up to it
starts = {0}
for p in work.get('plans', []):
    for e in p['end']: starts.add(ID[e] + 1)
starts = sorted(starts)
L = lambda i: max(8, len(''.join(IT[i]['v'])))   # text length, used to spread time over unmatched verses

# fixes.json (optional): {video id: {item id: seconds}} — when the verse's first word is heard, checked by ear or in the transcript,
# for lines the speech recogniser missed. Write the evidence beside each fix in fixes.md.
FP = os.path.join(SRC, 'fixes.json'); FIX = json.load(open(FP)) if os.path.exists(FP) else {}
# owner.json (optional): {video id: {item id: seconds or [start, end]}} — starts (and ends) the owner set by ear in the app's timing mode (sent through
# a GitHub issue and written by tools/audio/apply_owner_timing.py). They are used exactly as given and win over everything.
OP = os.path.join(SRC, 'owner.json'); OWN = json.load(open(OP)) if os.path.exists(OP) else {}
# ONLY=<ids>: just make the alignment caches of those recordings (run several in parallel), then run once without it
ONLY = [x for x in os.environ.get('ONLY', '').split(',') if x]
tracks, at, heard = [], {}, set()   # heard: verses whose start was found in the recording (matched, or checked by hand)
for r in REC:
    v = r['yt']; p = os.path.join(TR, v + '.jsonl')
    if not os.path.exists(p + '.done') and meta.get('estimate'):
        # source.json "estimate": true and no transcript: spread the verses over the recording by their length, as a
        # starting point for the owner to mark by ear (Settings › Audio timing); every start is listed to be checked
        a0 = ID[r['from']] if r.get('from') else 0; a1 = ID[r['to']] if r.get('to') else len(IT) - 1
        t0, t1 = float(r.get('lead', 0)), r['dur'] * 0.98; tot = sum(L(x) for x in range(a0, a1 + 1)); acc = 0; ti = len(tracks)
        tracks.append({'yt': v, 'dur': r['dur'], 'first': IT[a0]['id'], 'last': IT[a1]['id']})
        for x in range(a0, a1 + 1): at.setdefault(IT[x]['id'], [ti, round(t0 + (t1 - t0) * acc / tot, 1)]); acc += L(x)
        for iid, t in FIX.get(v, {}).items(): at[iid] = [ti, round(max(0, t - 0.4), 2)]; heard.add(iid)
        print(v, 'estimated by length:', a1 - a0 + 1, 'verses'); continue
    if not os.path.exists(p + '.done'): continue
    if ONLY and v not in ONLY: continue
    cache = os.path.join(TR, v + '.align.json')
    if not os.path.exists(cache):
        S = A.load(p)
        # recordings.json may say where a recording starts ("from": item id); otherwise it is located by matching words,
        # which can fail on texts whose lines repeat a lot (the Rudram's "namo … namaḥ")
        r0 = next(k for k, ref in enumerate(A.REF) if ref[0] == ID[r['from']]) if r.get('from') else A.locate(S)
        if meta.get('align') == 'anchors':
            # source.json "align": "anchors" — for recordings heard only in patches (see align.anchors). A match on a
            # verse's later line still gives its start: back by the letters before that line at the reciter's pace.
            r1 = max(k for k, ref in enumerate(A.REF) if ref[0] == ID[r['to']]) + 1 if r.get('to') else None   # "to": its last item
            R, pairs, rate = A.anchors(S, r0, thr=meta.get('anchor_min', 0.45), r1=r1)   # "anchor_min": how alike a match must be
            rows = {}
            for si, rj in pairs:
                k = rj
                while k > 0 and R[k - 1][0] == R[rj][0]: k -= 1
                rows.setdefault(si, []).append([IT[R[rj][0]]['id'], len(R[rj][2]), round(rate * sum(len(R[q][2]) for q in range(k, rj)), 2)])
        else:
            R, pairs = A.align(S, r0, split=bool(meta.get('split')))
            rows = {}
            for si, rj in pairs: rows.setdefault(si, []).append([IT[R[rj][0]]['id'], len(R[rj][2])])
        json.dump([[S[si]['s'], S[si]['e'], rows[si]] for si in sorted(rows)], open(cache, 'w'), ensure_ascii=False)
    first, halves = {}, {}
    for s0, e0, parts in json.load(open(cache)):
        tot = sum(p[1] for p in parts) or 1; acc = 0
        for p in parts:
            t = s0 + (e0 - s0) * acc / tot - (p[2] if len(p) > 2 else 0); acc += p[1]
            first[ID[p[0]]] = min(first.get(ID[p[0]], t), t)
            if p[0] in SPLIT: halves.setdefault(p[0], []).append(t)
    # a split joint caupāī whose every half-line was matched: each part starts at its own first half-line (two half-lines a line)
    for old, h in halves.items():
        h.sort(); lines = [len(IT[i]['v']) for i in SPLIT[old]]
        if len(h) == 2 * sum(lines):
            c = 0
            for i, nl in zip(SPLIT[old], lines): first[i] = h[2 * c]; c += nl
    items = {i: round(max(0, t - 0.4), 2) for i, t in first.items()}
    for iid, t in FIX.get(v, {}).items(): items[ID[iid]] = round(max(0, t - 0.4), 2)   # hand-checked starts win (fixes.json), with the same small lead
    items = sorted(items.items())
    clean, last = [], -1                       # drop matches that go backwards in time
    for i, t in items:
        if t > last: clean.append([i, t]); last = t
    rates = sorted((clean[k + 1][1] - clean[k][1]) / L(clean[k][0]) for k in range(len(clean) - 1) if clean[k + 1][0] == clean[k][0] + 1)
    rate = rates[len(rates) // 2] if rates else 0.25
    full = []
    for k in range(len(clean)):               # fill short gaps by text length
        full.append(clean[k])
        if k + 1 < len(clean):
            a, ta = clean[k]; b, tb = clean[k + 1]
            if a + 1 < b <= a + meta.get('fill', 8):   # source.json "fill": the longest run of unheard verses to place by text length
                tot = sum(L(x) for x in range(a, b)); acc = L(a)
                for x in range(a + 1, b): full.append([x, round(ta + (tb - ta) * acc / tot, 2)]); acc += L(x)
    i0, t0 = full[0]; ds = max(s for s in starts if s <= i0)
    if r.get('from'): ds = max(ds, min(i0, ID[r['from']]))   # never back-fill verses before where the recording starts
    if 0 < i0 - ds <= 4:                      # back-fill the first verses of the day
        pre, t = [], t0
        for x in range(i0 - 1, ds - 1, -1): t = max(0, t - L(x) * rate); pre.append([x, round(t, 2)])
        full = pre[::-1] + full
    ti = len(tracks)
    tracks.append({'yt': v, 'dur': r['dur'], 'first': IT[full[0][0]]['id'], 'last': IT[full[-1][0]]['id']})
    heard |= {IT[i]['id'] for i, _ in clean}
    for i, t in full: at.setdefault(IT[i]['id'], [ti, t])
    print(v, len(full), tracks[-1]['first'], '→', tracks[-1]['last'])

if ONLY: sys.exit(0)
own_ids = set()
for ti, tr in enumerate(tracks):
    for iid, t in OWN.get(tr['yt'], {}).items():   # seconds, or [start, end] when the owner also set where the verse ends
        if iid in ID: iid = IT[ID[iid]]['id']; at[iid] = [ti, round(float(t[0]), 2), round(float(t[1]), 2)] if isinstance(t, list) else [ti, round(float(t), 2)]; own_ids.add(iid)
# keep the text's order around the owner's times — the same rule as the app (tools/site/app.js, buildAudio), kept in
# tools/audio/order.py: a verse cannot start before the one before it, or before that verse's set end; a verse not set by
# ear that breaks this is placed again, by its length, between the nearest good times; a set end later than the next set
# start is cut back to it. The start each moved verse had before the rule is kept as "raw", so the app can apply the same
# rule from the same starting point and show exactly what the next send will publish.
moved, raw = [], {}
if own_ids:
    for ti in range(len(tracks)):
        a = sorted([[ID[k], v[1], v[2] if len(v) > 2 else None] for k, v in at.items() if v[0] == ti])
        before = {i: st for i, st, _ in a}
        rows, mv = O.keep_order(a, lambda i: IT[i]['id'] in own_ids, lambda i: IT[i]['id'] in heard, lambda i: max(8, len(''.join(IT[i]['v']))), tracks[ti]['dur'])
        for i, st, en in rows: at[IT[i]['id']] = [ti, st, en] if en is not None else [ti, st]
        for i in mv: raw[IT[i]['id']] = before[i]
        moved += [IT[i]['id'] for i in mv]
# a source marked "draft" in source.json (its timings are not good enough yet) is written with "draft": the app plays it only
# for someone reviewing timings (Settings › Audio timing), so readers never get audio that starts in the wrong place.
# Remove "draft" once the timings are checked.
out = os.path.join(REPO, 'library', meta['work'], 'audio', meta['id'] + '.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
doc = {k: meta[k] for k in ('id', 'type', 'title', 'order', 'draft') if k in meta}
# "check": verses whose start is only estimated (placed by text length between heard ones), or, for a draft, every verse
# not yet checked by hand; the app lists them for review in Settings › Audio timing. Starts set by the owner never count.
byhand = set(k for v in FIX.values() for k in v) | set(k for v in OWN.values() for k in v)
check = [] if meta.get('checked') else [x['id'] for x in IT if x['id'] in at and x['id'] not in byhand and (meta.get('draft') or x['id'] not in heard)]   # "checked": published by the owner after hearing it through
doc.update(tracks=tracks, at=at)
if check: doc['check'] = check
guess = [x['id'] for x in IT if x['id'] in at and x['id'] not in heard and x['id'] not in own_ids]
if guess: doc['guess'] = guess   # starts only guessed by text length (never heard): guessed again around the owner's times
if own_ids: doc['own'] = [x['id'] for x in IT if x['id'] in own_ids]   # verses set by ear by the owner: the app keeps them as given and links their neighbours
if moved: doc['moved'] = sorted(set(moved), key=lambda k: ID[k]); doc['raw'] = {k: raw[k] for k in doc['moved']}   # verses placed again around the owner's times (the app shows them as moved), with the start each had before
json.dump(doc, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print('verses with audio', len(at), 'of', len(IT), '→', os.path.relpath(out, REPO), '(draft)' if meta.get('draft') else '')
