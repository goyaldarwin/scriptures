"""Write a recording's aligned.md from its files: how its MMS starts were made, how many it takes, what is listed to check,
and how good they are on the owner's starts set by ear (tools/audio/mms_score.py, where he has set some).

    python3 tools/audio/aligned_md.py tools/works/<work>/audio/<source> [--print]

Every figure is read from the recording's own files (mms/windows.json, mms/<video id>.json, aligned.json, check.json,
fixes.json, owner.json, recordings.json); nothing is typed by hand, so the page says what the data is. The lean is
measured: each start in aligned.json is MMS's minus it.
"""
import json, os, re, statistics, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def load(src, f, default=None):
    p = os.path.join(src, f)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default

def main(src, show=False):
    S, REC = load(src, 'source.json'), load(src, 'recordings.json', [])
    W, A, C = load(src, 'mms/windows.json', []), load(src, 'aligned.json', {}), load(src, 'check.json', {'ids': []})
    F, O = load(src, 'fixes.json', {}), load(src, 'owner.json', {})
    work = json.load(open(os.path.join(os.path.dirname(os.path.dirname(src)), 'work.json'), encoding='utf-8'))
    title = S['title']['en'] if isinstance(S.get('title'), dict) else S['id']
    kept = {}
    for w in W:
        for l in w['lines']:
            if l['id'] in w['keep']: kept.setdefault(w['yt'], []).append(l['id'])
    fx = sorted({i for v in F.values() for i in (v if isinstance(v, dict) else {})}) if isinstance(F, dict) else []
    rows, leans, low = [], [], []
    for yt, ids in kept.items():
        M = load(src, f'mms/{yt}.json', {})
        for i in ids:
            if i not in M: continue
            st, en, sc = M[i]
            if sc < 0.5: low.append(i)
            elif i in A.get(yt, {}): leans.append(round(st - A[yt][i][0], 2))
    lean = statistics.median(leans) if leans else float(re.search(r'lean ([\d.]+) s', C.get('why', '')).group(1))
    assert all(abs(x - lean) < 0.011 or x < lean for x in leans), f'aligned.json is not MMS less one lean: {sorted(set(leans))[:8]}'
    n_all = sum(len(v) for v in kept.values()); n_al = sum(len(v) for v in A.values())
    vids = 'YouTube ' + ', '.join(f'`{r["yt"]}`' + (f', its track {r["start"]}–{r.get("end", r["dur"])} s' if 'start' in r else '') for r in REC)
    own = sum(len(v) for v in O.values()) if O else 0
    owned = {i for v in O.values() for i in v}
    out = ['# Verse starts from Meta\'s MMS forced aligner (`aligned.json`)', '',
           f'**What:** for every verse of {title}\'s recording of {work["title"]["en"]} ({vids}), the start and end found by '
           'torchaudio\'s `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every '
           'two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows '
           '`mms_windows.py` cut from the transcript\'s rough starts (`mms/windows.json`); one run per recording in the public '
           f'`align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean {lean:g}` writes '
           f'`aligned.json` and `check.json`. Each start is MMS\'s minus {lean:g} s'
           + (', the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it).' if abs(lean - 0.6) < 0.011 else '.')
           + f' {n_al} of the {n_all} verses MMS was given take its start; '
           + (f'{len(low)} it scored below 0.5 and are left to the transcript' + ''.join(
                 f'{"; " if k else ": "}{t} {", ".join(x)}' for k, (t, x) in enumerate([(t, x) for t, x in (
                 ('listed to check', [i for i in low if i in C['ids']]), ('set by hand', [i for i in low if i in fx and i not in C['ids']]),
                 ('set by the owner by ear', [i for i in low if i in owned and i not in fx and i not in C['ids']]),
                 ('not sung', [i for i in low if i not in C['ids'] and i not in fx and i not in owned])) if x])) + '.' if low else 'none scored below 0.5.'),
           '']
    if fx: out += [f'**By hand:** {len(fx)} start{"s" if len(fx) > 1 else ""} set by hand win over these (`fixes.json`, each with the 5-s '
                   f'windows or words it was read from in `fixes.md`): {", ".join(fx)}.', '']
    r = subprocess.run([sys.executable, os.path.join(HERE, 'mms_score.py'), src], capture_output=True, text=True) if own else None
    scored = int(re.search(r'(\d+) owner starts scored', r.stdout).group(1)) if r and re.search(r'(\d+) owner starts scored', r.stdout) else 0
    if own and scored < 20:
        out += [f'**How good:** not scored yet: of the owner\'s {own} starts set by ear here, {scored} are timed by both MMS and the '
                'transcript, fewer than the 20 or so a score needs (`tools/audio/mms_score.py`).', '']
    elif own:
        lines = r.stdout.strip().split('\n'); verdict = lines[-1].strip() if lines and lines[-1].strip() in ('switch', 'keep') else ''
        out += [f'**How good:** scored on the owner\'s {own} starts set by ear (`owner.json`; `tools/audio/mms_score.py`):', ''] + [l for l in lines if l.strip() not in ('switch', 'keep')] + \
               ([''] + ['MMS is better on both counts.' if verdict == 'switch' else 'MMS is not better on both counts here; his starts win over both wherever he has set them.'] if verdict else []) + ['']
    else: out += ['**How good:** not scored yet: the owner has not set starts by ear on this recording. His first 20 or so will measure '
                  'its lean and score MMS against the transcript (`tools/audio/mms_score.py`).', '']
    out += [f'**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): {len(C["ids"])}.',
            'The owner\'s starts (`owner.json`) and hand fixes (`fixes.json`) win over these.']
    text = '\n'.join(out) + '\n'
    if show: print(text)
    else: open(os.path.join(src, 'aligned.md'), 'w', encoding='utf-8').write(text)

if __name__ == '__main__': main(sys.argv[1].rstrip('/'), '--print' in sys.argv)
