"""Prove that library/ is exactly what the generators make.

    python3 tools/site/regen_check.py          only the works whose inputs or outputs changed since the last pass here
    python3 tools/site/regen_check.py --full   every work (the CI always runs this: it has no record of a last pass)

First runs every work's text generator that reads only files in this repository (GENERATORS: the scripts in
tools/works/<work>/source/ that write its text.txt, book.json or copied meanings) in a copy of tools/, and fails if any
file it writes differs from the committed one: a text edited by hand would be undone by the next run of its generator; and
runs tools/audio/mms_merge.py on each recording with MMS's raw results (mms/), which must give its aligned.json and check.json.
Then makes the works again in an empty folder that holds only what is edited by hand (index.json, removed.json,
apps.json and glossary/): each work with tools/works/export.py (works that take nothing from each other side by side,
one process each), then each recording's timings with tools/audio/make_timings.py (a recording that takes its timings
from another work after that work's), then compares both folders file by file. It fails on any difference, so:
  - a hand edit to a generated file (it would be undone by the next regeneration) is caught;
  - a generator changed without regenerating its output is caught;
  - a file whose work, meaning source or recording is gone (an orphan) is caught, a part file of a work loaded by part too,
    and so is a folder in library/ that is no work's;
  - a work that takes verses or timings from another (the Sundarakāṇḍa, the Hanumān āratī) cannot drift from it;
  - a recording's timings cannot lag behind its text (the starts not set by ear are spread by the length of each verse,
    so a changed verse moves them).
`sources` and `glossary` in work.json are written by build.py, not the exporters (and checked by it), so they are left
out of the comparison.

What is skipped, and why it is safe: a pass records, per work, a hash of everything its export reads (its folder, the
folders of the works it takes from, and the shared inputs: every script under tools/ that is not the app or a test,
and library/'s hand-edited files) and of everything it writes (its library/<path>/ folder). A work whose two hashes are
both what the last pass recorded is the same as when it passed, so it is not made again. Anything else changed (a
work's text, a meaning, a script the exporters use, a generated file edited by hand) makes that work, and every work that
takes from it, run again. The record is kept outside the repository (~/.cache/scriptures/regen.json); --full ignores it.
"""
import glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
WORKS = os.path.join(REPO, 'tools', 'works')
sys.path.insert(0, WORKS); import export as EXPORT

# the scripts that make a work's text.txt (and its other source files) from data in its source/ folder, in the order they run
GENERATORS = [('manas', ['make_appdata.py', 'make.py']), ('ramayan-aarti', ['make.py']), ('ramraksha', ['make.py']), ('sukhmani-sahib', ['make.py']),
              ('katha-upanishad', ['settle.py']), ('shri-rudram', ['settle.py']),
              ('guru-granth-sahib', ['make.py'])]
BY_HAND = ['index.json', 'removed.json', 'apps.json', 'glossary']   # library/ files no generator makes
GENERATED_KEYS = ('sources', 'glossary')   # work.json keys build.py writes
# files under tools/ that no export, generator or timing reads: a change to them never changes library/
NOT_INPUT = ('tools/site/app.js', 'tools/site/index_template.html', 'tools/site/privacy.html', 'tools/site/ux_test.py',
             'tools/site/smoke_test.py', 'tools/site/check.py', 'tools/site/history_check.py', 'tools/site/regen_check.py',
             'tools/site/split_fixture.py', 'tools/site/fixtures/', 'tools/store/', 'tools/fonts/')
CACHE = os.path.join(os.environ.get('XDG_CACHE_HOME') or os.path.expanduser('~/.cache'), 'scriptures', 'regen.json')

def files(root):
    return {os.path.relpath(os.path.join(d, f), root): os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs}

def same(a, b):
    if a.endswith('.json'):
        x, y = json.load(open(a, encoding='utf-8')), json.load(open(b, encoding='utf-8'))
        if os.path.basename(a) == 'work.json' and isinstance(x, dict) and isinstance(y, dict):
            x, y = ({k: v for k, v in z.items() if k not in GENERATED_KEYS} for z in (x, y))
        return x == y
    return open(a, 'rb').read() == open(b, 'rb').read()

def digest(paths):
    """One hash of these files and folders (their names and contents); __pycache__ and .pyc left out."""
    h = hashlib.sha1()
    for p in sorted(paths):
        full = os.path.join(REPO, p)
        fs = [full] if os.path.isfile(full) else sorted(v for k, v in files(full).items() if '__pycache__' not in k and not k.endswith('.pyc')) if os.path.isdir(full) else []
        for f in fs:
            h.update(os.path.relpath(f, REPO).encode() + b'\0')
            with open(f, 'rb') as fh:
                for block in iter(lambda: fh.read(1 << 20), b''): h.update(block)
    return h.hexdigest()

def shared_inputs():
    """Everything a work's export, generator or timings may read besides the works' own folders."""
    out = ['library/' + f for f in BY_HAND]
    for d, ds, fs in os.walk(os.path.join(REPO, 'tools')):
        rel = os.path.relpath(d, REPO).replace(os.sep, '/')
        if rel == 'tools/works': ds[:] = []; fs = [f for f in fs]   # the exporter and the format; the works' folders are their own
        ds[:] = [x for x in ds if x != '__pycache__']
        for f in fs:
            p = rel + '/' + f
            if not p.endswith('.pyc') and not any(p == n or (n.endswith('/') and p.startswith(n)) for n in NOT_INPUT): out.append(p)
    return out

def audio_takes(wid):
    """The works whose recordings' timings this work's recordings copy (audio/<source>/source.json → "take")."""
    return sorted({json.load(open(s, encoding='utf-8')).get('take') for s in glob.glob(os.path.join(WORKS, wid, 'audio', '*', 'source.json'))} - {None})

def deps(wid, seen=None):
    """The works this work's library files are made from, itself included."""
    seen = set() if seen is None else seen
    if wid in seen: return seen
    seen.add(wid)
    for t in EXPORT.takes(wid) + audio_takes(wid): deps(t, seen)
    return seen

def generators(only):
    """Run each text generator of these works in a copy of tools/; return the files it writes that differ from the committed ones."""
    bad = []; todo = [(w, s) for w, s in GENERATORS if w in only]
    if not todo: return bad
    with tempfile.TemporaryDirectory() as tmp:
        tools = os.path.join(tmp, 'tools'); shutil.copytree(os.path.join(REPO, 'tools'), tools, ignore=shutil.ignore_patterns('__pycache__', 'transcripts'))
        def one(job):
            wid, scripts = job; out = []
            src = os.path.join(tools, 'works', wid, 'source'); before = {k: os.path.getmtime(v) for k, v in files(os.path.join(tools, 'works', wid)).items()}
            for sc in scripts:
                r = subprocess.run([sys.executable, sc], cwd=src, capture_output=True, text=True)
                if r.returncode: return [f'{wid}/source/{sc} failed: {(r.stdout + r.stderr)[-400:]}']
            for k, v in files(os.path.join(tools, 'works', wid)).items():
                orig = os.path.join(REPO, 'tools', 'works', wid, k)
                if k.endswith('.pyc') or (k in before and os.path.getmtime(v) == before[k]): continue
                if not os.path.exists(orig): out.append(f'{wid}/{k}: written by its generator, not in the repository')
                elif not same(v, orig): out.append(f'{wid}/{k}: differs from what {wid}/source/{"+".join(scripts)} makes')
            return out
        with ThreadPoolExecutor(min(len(todo), os.cpu_count() or 2)) as ex:
            for r in ex.map(one, todo): bad += r
    return bad

def merges(only):
    """Run mms_merge.py on a copy of each recording of these works that uses MMS's starts (aligned.json, from mms/), with the
    lean its check.json names; return the recordings whose aligned.json or check.json differs from what it makes."""
    bad = []
    for w in sorted(only):
        for d in sorted(glob.glob(os.path.join(WORKS, w, 'audio', '*', 'mms', 'windows.json'))):
            src = os.path.dirname(os.path.dirname(d)); rel = os.path.relpath(src, WORKS)
            if not os.path.exists(os.path.join(src, 'aligned.json')): continue   # a run not used yet (mms/score.md says why)
            if not os.path.exists(os.path.join(src, 'aligned.md')): bad.append(f'{rel}: uses MMS but has no aligned.md, how its starts were made and how good they are (tools/audio/aligned_md.py writes it)')
            if not os.path.exists(os.path.join(src, 'check.json')): bad.append(f'{rel}: uses MMS but has no check.json (run mms_merge.py)'); continue
            m = re.search(r'lean ([\d.]+) s', json.load(open(os.path.join(src, 'check.json'), encoding='utf-8')).get('why', ''))
            with tempfile.TemporaryDirectory() as tmp:
                cp = os.path.join(tmp, 's'); shutil.copytree(src, cp, ignore=shutil.ignore_patterns('transcripts'))
                r = subprocess.run([sys.executable, os.path.join(REPO, 'tools', 'audio', 'mms_merge.py'), cp, '--lean', m.group(1) if m else '0.6'], capture_output=True, text=True)
                if r.returncode: bad.append(f'{rel}: mms_merge.py failed: {(r.stdout + r.stderr)[-300:]}'); continue
                bad += [f'{rel}/{f}: differs from what mms_merge.py makes (run it with --lean {m.group(1) if m else "0.6"})' for f in ('aligned.json', 'check.json')
                        if not os.path.exists(os.path.join(src, f)) or not same(os.path.join(cp, f), os.path.join(src, f))]
    return bad

def listed(only):
    """Every verse a recording's check.json lists (and the owner has not set by ear) is on its to-check list in library/."""
    bad = []
    for w in sorted(only):
        for c in sorted(glob.glob(os.path.join(WORKS, w, 'audio', '*', 'check.json'))):
            src = os.path.dirname(c); S = json.load(open(os.path.join(src, 'source.json'), encoding='utf-8'))
            if S.get('take'): continue
            O = json.load(open(os.path.join(src, 'owner.json'), encoding='utf-8')) if os.path.exists(os.path.join(src, 'owner.json')) else {}
            own = {k for v in O.values() for k in v}
            A = json.load(open(os.path.join(REPO, 'library', S['work'], 'audio', S['id'] + '.json'), encoding='utf-8'))
            at = A.get('at') or {}
            miss = [i for i in json.load(open(c, encoding='utf-8'))['ids'] if i not in own and i in at and i not in (A.get('check') or [])]
            if miss: bad.append(f'{os.path.relpath(src, WORKS)}: check.json lists {miss[:5]}, which the to-check list leaves out')
    return bad

def groups(wids):
    """The works in sets that take nothing from one another's, each in the order export.py makes them."""
    left, out = set(wids), []
    while left:
        w = min(left); g = {w}; grew = True
        while grew:
            grew = False
            for x in list(left - g):
                if deps(x) & g or any(x in deps(y) for y in g): g.add(x); grew = True
        left -= g; out.append([x for x in EXPORT.order(sorted(g)) if x in g])
    return out

def fail(msg, lines):
    print(msg)
    for k in lines[:30]: print('  ', k)
    sys.exit(1)

def main(argv):
    full = '--full' in argv
    lib = os.path.join(REPO, 'library')
    wids = EXPORT.folders(); path = {w: EXPORT.manifest(w)['path'] for w in wids}
    # every folder of library/ that holds a work.json is a work's (an orphan work is never skipped)
    found = {os.path.relpath(os.path.dirname(f), lib).replace(os.sep, '/') for f in glob.glob(os.path.join(lib, '**', 'work.json'), recursive=True)}
    orphan = sorted(found - set(path.values()))
    roots = [f + ('/' if os.path.isdir(os.path.join(lib, f)) else '') for f in BY_HAND] + [p + '/' for p in path.values()]
    orphan += sorted(k for k in files(lib) if not any(k.replace(os.sep, '/') == r or k.replace(os.sep, '/').startswith(r) for r in roots if r.endswith('/') or k == r))
    if orphan: fail('FAIL: library/ holds works no folder in tools/works makes (remove them, or add the work):', orphan)
    shared = digest(shared_inputs())
    ins = {w: digest(['tools/works/' + d for d in sorted(deps(w))]) for w in wids}
    outs = {w: digest(['library/' + path[w]]) for w in wids}
    last = {} if full or not os.path.exists(CACHE) else json.load(open(CACHE))
    if last.get('shared') != shared: last = {}
    dirty = {w for w in wids if (last.get('works') or {}).get(w) != [ins[w], outs[w]]}
    dirty |= {w for w in wids if deps(w) & dirty}
    if not dirty:
        print(f'regen check: nothing has changed since the last pass ({len(wids)} works; --full makes them all again)'); return
    bad = generators(dirty)
    if bad: fail("FAIL: a work's source file differs from what its generator makes (put the change in the generator, or run it):", bad)
    bad = listed(dirty)
    if bad: fail("FAIL: a start in doubt is not on the owner's to-check list (tools/audio/make_timings.py):", bad)
    bad = merges(dirty)
    if bad: fail("FAIL: a recording's MMS starts or to-check list differ from what tools/audio/mms_merge.py makes from its raw results:", bad)
    need = set().union(*(deps(w) for w in dirty))
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'library'); os.makedirs(out)
        for f in BY_HAND:
            (shutil.copytree if os.path.isdir(os.path.join(lib, f)) else shutil.copy)(os.path.join(lib, f), os.path.join(out, f))
        for w in sorted(need - dirty):   # a clean work another one takes from: as committed (it passed)
            shutil.copytree(os.path.join(lib, path[w]), os.path.join(out, path[w]))
        def run(args, env=None):
            r = subprocess.run([sys.executable] + args, capture_output=True, text=True, env=env)
            return '' if not r.returncode else f'FAIL {" ".join(os.path.relpath(a, REPO) if os.path.isabs(a) else a for a in args)}:\n{(r.stdout + r.stderr)[-2000:]}'
        with ThreadPoolExecutor(os.cpu_count() or 2) as ex:
            errs = [e for e in ex.map(lambda g: run([os.path.join(WORKS, 'export.py'), '--out', out] + g), groups(dirty)) if e]
        if errs: print(errs[0]); sys.exit(1)
        env = dict(os.environ, SCRIPTURES_REPO=tmp); os.symlink(os.path.join(REPO, 'tools'), os.path.join(tmp, 'tools'))
        srcs = sorted(s for w in dirty for s in glob.glob(os.path.join(WORKS, w, 'audio', '*', 'source.json')))
        takes = lambda s: bool(json.load(open(s, encoding='utf-8')).get('take'))
        for batch in ([s for s in srcs if not takes(s)], [s for s in srcs if takes(s)]):
            with ThreadPoolExecutor(os.cpu_count() or 2) as ex:
                errs = [e for e in ex.map(lambda s: run([os.path.join(REPO, 'tools', 'audio', 'make_timings.py'), os.path.dirname(s)], env), batch) if e]
            if errs: print(errs[0]); sys.exit(1)
        diff = []
        for w in sorted(dirty):
            A, B = files(os.path.join(lib, path[w])), files(os.path.join(out, path[w]))
            p = path[w] + '/'
            diff += [f'only in library/: {p}{k}' for k in sorted(set(A) - set(B))] + [f'not in library/: {p}{k}' for k in sorted(set(B) - set(A))] \
                  + [f'differs: {p}{k}' for k in sorted(set(A) & set(B)) if not same(A[k], B[k])]
        if diff: fail('FAIL: library/ differs from what the generators make (regenerate, or put the change in the generator):', diff)
    rec = {'shared': shared, 'works': {**{w: v for w, v in (last.get('works') or {}).items() if w in wids}, **{w: [ins[w], outs[w]] for w in dirty}}}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True); json.dump(rec, open(CACHE, 'w'))
    gen = [w for w, _ in GENERATORS if w in dirty]
    print(f'regen check: {len(gen)} works\' texts equal what their generators make; library/ equals the output of tools/works/export.py and of make_timings.py for {len(dirty)} of {len(wids)} works and {len(srcs)} recordings'
          + ('' if len(dirty) == len(wids) else f' (the other {len(wids) - len(dirty)} are unchanged since their last pass)'))

if __name__ == '__main__': main(sys.argv[1:])
