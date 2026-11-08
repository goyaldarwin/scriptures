"""Score MMS's starts and the transcript's on the owner's starts set by ear, before a recording switches to MMS
(tools/audio/METHOD.md, "Before a new recording uses steps 2–5").

    python3 tools/audio/mms_score.py tools/works/<work>/audio/<source>

Needs the recording's mms/<video id>.json (the align workflow) and its owner.json. Compares, verse by verse, the owner's
start with (a) the transcript matched to the text alone (make_timings.py run in a copy without owner.json, fixes.json and
aligned.json) and (b) MMS's start (score 0.5 or more) minus the recording's lean, the median of MMS's start minus the
owner's (0.6 s, METHOD.md's default, when he has set fewer than 20). Prints the lean and the table for aligned.md, and
"switch" when MMS is better on both counts (more within 1 s, no more over 3 s off), else "keep".
"""
import glob, json, os, shutil, statistics, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))

def owner_starts(src):
    O = json.load(open(os.path.join(src, 'owner.json'), encoding='utf-8')) if os.path.exists(os.path.join(src, 'owner.json')) else {}
    return {yt: {i: (v[0] if isinstance(v, list) else v) for i, v in d.items()} for yt, d in O.items()}

def transcript_alone(src):
    """{video: {verse: start}} from the transcript matched to the text, with nothing set by hand or by MMS."""
    meta = json.load(open(os.path.join(src, 'source.json'), encoding='utf-8'))
    with tempfile.TemporaryDirectory() as tmp:
        lib = os.path.join(tmp, 'library', meta['work']); os.makedirs(os.path.join(lib, 'audio'))
        shutil.copy(os.path.join(REPO, 'library', meta['work'], 'work.json'), lib)
        os.symlink(os.path.join(REPO, 'tools'), os.path.join(tmp, 'tools'))
        cp = os.path.join(tmp, 'src'); shutil.copytree(src, cp, ignore=shutil.ignore_patterns('owner.json', 'fixes.json', 'aligned.json', 'mms'))
        r = subprocess.run([sys.executable, os.path.join(HERE, 'make_timings.py'), cp], capture_output=True, text=True, env=dict(os.environ, SCRIPTURES_REPO=tmp))
        if r.returncode: sys.exit('make_timings.py failed: ' + (r.stdout + r.stderr)[-800:])
        A = json.load(open(os.path.join(lib, 'audio', meta['id'] + '.json'), encoding='utf-8'))
    out = {}
    for i, v in A['at'].items(): out.setdefault(A['tracks'][v[0]]['yt'], {})[i] = v[1]
    return out

def table(name, diffs):
    d = sorted(abs(x) for x in diffs); n = len(d) or 1
    w1, w3 = sum(x <= 1 for x in d), sum(x > 3 for x in d)
    return w1, w3, f"| {name} | {w1} ({round(100 * w1 / n)}%) | {len(d) - w1 - w3} | {w3} | {statistics.median(d) if d else 0:.2f} s | {statistics.mean(d) if d else 0:.2f} s |"

def main(src):
    own = owner_starts(src); tr = transcript_alone(src)
    mms = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(src, 'mms', '*.json')) if not f.endswith('windows.json')}
    pairs = [(yt, i, s) for yt, d in own.items() for i, s in d.items() if i in (mms.get(yt) or {}) and mms[yt][i][2] >= 0.5 and i in (tr.get(yt) or {})]
    if not pairs: sys.exit('no verse has an owner start, an MMS start and a transcript start: nothing to score')
    raw = [mms[yt][i][0] - s for yt, i, s in pairs]
    lean = round(statistics.median(raw), 2) if len(pairs) >= 20 else 0.6
    a1, a3, ra = table('Whisper transcript matched to the text (`make_timings.py` alone)', [tr[yt][i] - s for yt, i, s in pairs])
    b1, b3, rb = table(f'MMS, lean {lean} s removed', [mms[yt][i][0] - lean - s for yt, i, s in pairs])
    print(f'{len(pairs)} owner starts scored; lean {lean} s (median of MMS minus the owner: {statistics.median(raw):.2f} s)')
    print('| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |\n|---|---|---|---|---|---|\n' + ra + '\n' + rb)
    print('switch' if b1 > a1 and b3 <= a3 else 'keep')
    return {'n': len(pairs), 'lean': lean, 'switch': b1 > a1 and b3 <= a3, 'rows': [ra, rb]}

if __name__ == '__main__': main(os.path.abspath(sys.argv[1]))
