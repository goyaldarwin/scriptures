"""Prove that library/ is exactly what the generators make.

    python3 tools/site/regen_check.py

Makes the library again in an empty folder that holds only what is edited by hand (index.json, removed.json,
apps.json and glossary/): every work with tools/works/export.py, then every recording's timings with
tools/audio/make_timings.py (a recording that takes its timings from another work after that work's), then compares
both folders file by file. It fails on any difference, so:
  - a hand edit to a generated file (it would be undone by the next regeneration) is caught;
  - a generator changed without regenerating its output is caught;
  - a file whose work, meaning source or recording is gone (an orphan) is caught;
  - a work that takes verses or timings from another (the Sundarakāṇḍa, the Hanumān āratī) cannot drift from it;
  - a recording's timings cannot lag behind its text (the starts not set by ear are spread by the length of each verse,
    so a changed verse moves them).
`sources` and `glossary` in work.json are written by build.py, not the exporters, and are compared after build.py's
own registration has run on both sides.
"""
import glob, json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import library

BY_HAND = ['index.json', 'removed.json', 'apps.json', 'glossary']   # library/ files no generator makes

def files(root):
    return {os.path.relpath(os.path.join(d, f), root): os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs}

def same(a, b):
    if a.endswith('.json'): return json.load(open(a, encoding='utf-8')) == json.load(open(b, encoding='utf-8'))
    return open(a, 'rb').read() == open(b, 'rb').read()

def main():
    lib = os.path.join(REPO, 'library')
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'library'); os.makedirs(out)
        for f in BY_HAND:
            (shutil.copytree if os.path.isdir(os.path.join(lib, f)) else shutil.copy)(os.path.join(lib, f), os.path.join(out, f))
        def run(args, env=None):
            r = subprocess.run([sys.executable] + args, capture_output=True, text=True, env=env)
            if r.returncode: print(f'FAIL {" ".join(os.path.relpath(a, REPO) if os.path.isabs(a) else a for a in args)}:\n{(r.stdout + r.stderr)[-2000:]}'); sys.exit(1)
        run([os.path.join(REPO, 'tools', 'works', 'export.py'), '--out', out])
        env = dict(os.environ, SCRIPTURES_REPO=tmp); os.symlink(os.path.join(REPO, 'tools'), os.path.join(tmp, 'tools'))
        srcs = sorted(glob.glob(os.path.join(REPO, 'tools', 'works', '*', 'audio', '*', 'source.json')))
        takes = lambda s: bool(json.load(open(s, encoding='utf-8')).get('take'))
        for s in [s for s in srcs if not takes(s)] + [s for s in srcs if takes(s)]:
            run([os.path.join(REPO, 'tools', 'audio', 'make_timings.py'), os.path.dirname(s)], env)
        library.prepare(out)   # register sources on the regenerated side, as build.py does
        A, B = files(lib), files(out)
        diff = [f'only in library/: {k}' for k in sorted(set(A) - set(B))] + [f'not in library/: {k}' for k in sorted(set(B) - set(A))] \
             + [f'differs: {k}' for k in sorted(set(A) & set(B)) if not same(A[k], B[k])]
        if diff:
            print('FAIL: library/ differs from what the generators make (regenerate, or put the change in the generator):')
            for k in diff[:30]: print('  ', k)
            sys.exit(1)
    print(f'regen check: library/ equals the output of tools/works/export.py and of make_timings.py for {len(srcs)} recordings')

if __name__ == '__main__': main()
