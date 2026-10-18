"""Make an audio source: transcripts → library/<work>/audio/<id>.json (verse start times).

Usage:  python3 tools/audio/make_timings.py tools/works/<work>/audio/<source-id>

The source folder holds:
  source.json      {"id", "work": "<library path>", "type": "youtube", "title": {"hi", "en"}, "order"?}
  recordings.json  [{"yt": video id, "file": original file name, "dur": seconds, "order": n}]
  transcripts/     <video id>.jsonl from transcribe.py (+ .done when finished)
  fixes.json       optional hand-checked verse starts {video id: {item id: seconds}}, with the evidence in fixes.md
Only finished transcripts are used. The alignment is cached per recording in transcripts/<video id>.align.json:
one row per transcript segment, [start, end, [[item id, characters of that half-line], …]]. Delete it to realign.
A segment that covers several half-lines is shared among them by length, so a verse that begins in the
middle of a long breath gets the time it begins, not the time the breath begins.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import align as A

SRC = os.path.abspath(sys.argv[1]); TR = os.path.join(SRC, 'transcripts')
meta = json.load(open(os.path.join(SRC, 'source.json')))
REC = sorted(json.load(open(os.path.join(SRC, 'recordings.json'))), key=lambda r: r['order'])
work = json.load(open(os.path.join(REPO, 'library', meta['work'], 'work.json')))
IT = work['items']; ID = {x['id']: i for i, x in enumerate(IT)}
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
# ONLY=<ids>: just make the alignment caches of those recordings (run several in parallel), then run once without it
ONLY = [x for x in os.environ.get('ONLY', '').split(',') if x]
tracks, at = [], {}
for r in REC:
    v = r['yt']; p = os.path.join(TR, v + '.jsonl')
    if not os.path.exists(p + '.done'): continue
    if ONLY and v not in ONLY: continue
    cache = os.path.join(TR, v + '.align.json')
    if not os.path.exists(cache):
        S = A.load(p); r0 = A.locate(S); R, pairs = A.align(S, r0)
        rows = {}
        for si, rj in pairs: rows.setdefault(si, []).append([IT[R[rj][0]]['id'], len(R[rj][2])])
        json.dump([[S[si]['s'], S[si]['e'], rows[si]] for si in sorted(rows)], open(cache, 'w'), ensure_ascii=False)
    first = {}
    for s0, e0, parts in json.load(open(cache)):
        tot = sum(n for _, n in parts) or 1; acc = 0
        for iid, n in parts:
            first.setdefault(ID[iid], s0 + (e0 - s0) * acc / tot); acc += n
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
            if a + 1 < b <= a + 8:
                tot = sum(L(x) for x in range(a, b)); acc = L(a)
                for x in range(a + 1, b): full.append([x, round(ta + (tb - ta) * acc / tot, 2)]); acc += L(x)
    i0, t0 = full[0]; ds = max(s for s in starts if s <= i0)
    if 0 < i0 - ds <= 4:                      # back-fill the first verses of the day
        pre, t = [], t0
        for x in range(i0 - 1, ds - 1, -1): t = max(0, t - L(x) * rate); pre.append([x, round(t, 2)])
        full = pre[::-1] + full
    ti = len(tracks)
    tracks.append({'yt': v, 'dur': r['dur'], 'first': IT[full[0][0]]['id'], 'last': IT[full[-1][0]]['id']})
    for i, t in full: at.setdefault(IT[i]['id'], [ti, t])
    print(v, len(full), tracks[-1]['first'], '→', tracks[-1]['last'])

if ONLY: sys.exit(0)
out = os.path.join(REPO, 'library', meta['work'], 'audio', meta['id'] + '.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
doc = {k: meta[k] for k in ('id', 'type', 'title', 'order') if k in meta}
doc.update(tracks=tracks, at=at)
json.dump(doc, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print('verses with audio', len(at), 'of', len(IT), '→', os.path.relpath(out, REPO))
