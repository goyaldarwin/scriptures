"""Prove that library/ is exactly what the generators make.

    python3 tools/site/regen_check.py

Copies library/ to a temporary folder, runs every work's tools/works/<work>/export.py into it (in dependency order:
the Mānas first, then the Sundarakāṇḍa, which reads it, then the rest; the āratīs last, as they take the Hanumān
āratī from the Sundarakāṇḍa), then makes every recording's timings again (tools/audio/make_timings.py, for each
tools/works/<work>/audio/<source>; then the āratīs once more, as they copy the Sundarakāṇḍa's), and compares every JSON
file with library/. It fails on any difference, so:
  - a hand edit to a generated file (it would be undone by the next regeneration) is caught;
  - a generator changed without regenerating its output is caught;
  - a work that copies another (the Sundarakāṇḍa, the Hanumān āratī) cannot drift from it;
  - a recording's timings cannot lag behind its text (the starts not set by ear are spread by the length of each verse,
    so a changed verse moves them).
`sources` and `glossary` in work.json are written by build.py, not the exporters, and are compared after build.py's
own registration has run on both sides.
"""
import glob, json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); import library

FIRST, LAST = ['ramcharitmanas', 'sundarkand'], ['aartis']

def exporters():
    names = sorted(d for d in os.listdir(os.path.join(REPO, 'tools', 'works')) if os.path.exists(os.path.join(REPO, 'tools', 'works', d, 'export.py')))
    return [d for d in FIRST if d in names] + [d for d in names if d not in FIRST + LAST] + [d for d in LAST if d in names]

def files(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.json'): p = os.path.join(d, f); out[os.path.relpath(p, root)] = p
    return out

def main():
    lib = os.path.join(REPO, 'library')
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'library'); shutil.copytree(lib, out)
        def run(args, env=None):
            r = subprocess.run([sys.executable] + args, capture_output=True, text=True, env=env)
            if r.returncode: print(f'FAIL {" ".join(os.path.relpath(a, REPO) for a in args)}:\n{r.stderr[-2000:]}'); sys.exit(1)
        for d in exporters(): run([os.path.join(REPO, 'tools', 'works', d, 'export.py'), out])
        env = dict(os.environ, SCRIPTURES_REPO=tmp); os.symlink(os.path.join(REPO, 'tools'), os.path.join(tmp, 'tools'))
        for src in sorted(glob.glob(os.path.join(REPO, 'tools', 'works', '**', 'audio', '*', 'source.json'), recursive=True)):
            run([os.path.join(REPO, 'tools', 'audio', 'make_timings.py'), os.path.dirname(src)], env)
        for d in LAST: run([os.path.join(REPO, 'tools', 'works', d, 'export.py'), out])
        library.prepare(out)   # register sources on the regenerated side, as build.py does
        A, B = files(lib), files(out)
        diff = sorted(set(A) ^ set(B)) + sorted(k for k in set(A) & set(B) if json.load(open(A[k], encoding='utf-8')) != json.load(open(B[k], encoding='utf-8')))
        if diff:
            print('FAIL: library/ differs from what the generators make (regenerate, or put the change in the generator):')
            for k in diff[:30]: print('  ', k)
            sys.exit(1)
    print(f'regen check: library/ equals the output of {len(exporters())} exporters and of make_timings.py for every recording')

if __name__ == '__main__': main()
