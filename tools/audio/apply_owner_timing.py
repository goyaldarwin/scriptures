"""Apply audio starts the owner set by ear in the app (Settings › Audio timing › Send to the library).

Usage:  python3 tools/audio/apply_owner_timing.py <file with the GitHub issue body>
The body carries one JSON block: {"path": "<library path of the work>", "source": "<audio source id>",
"starts": {"<video id>": {"<item id>": seconds or [start, end]}}, "publish"?: true}.
It merges the starts into tools/works/<work>/audio/<source>/owner.json (later sends win), removes "draft" from that
source's source.json when "publish" is true, and re-makes the source's timings with make_timings.py. It prints one
line per change and exits non-zero with a reason when the body is not valid, so the workflow can say so on the issue.
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
def fail(msg): print('ERROR: ' + msg); sys.exit(1)
body = open(sys.argv[1]).read()
m = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.S) or re.search(r'(\{.*\})', body, re.S)
if not m: fail('no JSON block in the issue')
try: doc = json.loads(m.group(1))
except Exception as e: fail('the JSON block does not parse: %s' % e)
path, sid, starts = doc.get('path'), doc.get('source'), doc.get('starts') or {}
src = None
for sj in glob.glob(os.path.join(REPO, 'tools', 'works', '*', 'audio', '*', 'source.json')):
    meta = json.load(open(sj))
    if meta.get('work') == path and meta.get('id') == sid: src = os.path.dirname(sj); break
if not src: fail('no audio source %r for the work %r' % (sid, path))
work = json.load(open(os.path.join(REPO, 'library', path, 'work.json'))); ids = {x['id'] for x in work['items']}
vids = {r['yt'] for r in json.load(open(os.path.join(src, 'recordings.json')))}
OP = os.path.join(src, 'owner.json'); own = json.load(open(OP)) if os.path.exists(OP) else {}
n = 0
for vid, items in starts.items():
    if vid not in vids: fail('video %r is not a recording of %s' % (vid, sid))
    for iid, sec in items.items():
        if iid not in ids: fail('unknown verse id %r' % iid)
        ok = (isinstance(sec, (int, float)) and sec >= 0) or (isinstance(sec, list) and len(sec) == 2 and all(isinstance(x, (int, float)) for x in sec) and 0 <= sec[0] < sec[1])
        if not ok: fail('bad time for %s: %r (seconds, or [start, end])' % (iid, sec))
        own.setdefault(vid, {})[iid] = [round(float(x), 2) for x in sec] if isinstance(sec, list) else round(float(sec), 2); n += 1; print('time', vid, iid, sec)
json.dump(own, open(OP, 'w'), ensure_ascii=False, indent=1, sort_keys=True); open(OP, 'a').write('\n')
if doc.get('publish'):
    sp = os.path.join(src, 'source.json'); meta = json.load(open(sp))
    if meta.pop('draft', None) is not None:
        open(sp, 'w').write(json.dumps(meta, ensure_ascii=False) + '\n'); print('published', sid)
print('%d starts applied' % n)
# re-make the timings, and make sure nothing changed except the verses in this issue: the rest of the published work is
# never touched by a manual correction
meta = json.load(open(os.path.join(src, 'source.json'))); out = os.path.join(REPO, 'library', path, 'audio', meta['id'] + '.json')
before = json.load(open(out))['at'] if os.path.exists(out) else {}
subprocess.run([sys.executable, os.path.join(HERE, 'make_timings.py'), src], check=True)
after = json.load(open(out))['at']
sent = {iid for items in starts.values() for iid in items}
refit = set(json.load(open(out)).get('moved', []))   # neighbours placed again around the owner's times (make_timings.py)
moved = sorted(k for k in set(before) | set(after) if k not in sent and k not in refit and before.get(k) != after.get(k))
if moved: fail('other verses would change too (%d, e.g. %s); nothing was applied' % (len(moved), moved[:5]))
print('only the %d verses sent changed%s' % (len(sent), ', and %d neighbours placed around them' % len(refit) if refit else ''))
