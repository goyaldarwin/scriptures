"""Every check before a commit, in one command, side by side: the build first, then the regeneration check, the history
check, the smoke test and the UX test (in shards) at once. Each check is the same script the CI runs; this only runs
them together and gates on their exit codes.

    python3 tools/site/check.py              everything (a few minutes; the UX test alone, unsharded, takes longest)
    python3 tools/site/check.py --fast       the build, regen_check and history_check only (data changes: about 30 s,
                                             a few once regen_check has passed here and only some works changed);
                                             the browser tests still run in CI on the pull request
    python3 tools/site/check.py --works a,b  the build, regen_check, history_check, the smoke test, and the UX test's
                                             per-work checks for these works only (a change to their data, not the app)
    python3 tools/site/check.py --browser    the smoke test and the UX test only (the CI runs the others as steps of their own)
    python3 tools/site/check.py --shards 6   more UX shards (default 4: shard 0 runs the checks of the whole app, the
                                             others share the per-work checks)
regen_check makes again only the works whose inputs or outputs changed since its last pass on this machine (its
docstring says why that is safe); the CI makes every work (--full).

A failed check prints its output's last lines and every FAIL line; the full output is in <tmp>/check-<name>.log.
"""
import os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))

def run(name, args):
    log = os.path.join(tempfile.gettempdir(), f'check-{name}.log'); t0 = time.time()
    with open(log, 'w') as f: rc = subprocess.run([sys.executable] + args, cwd=REPO, stdout=f, stderr=subprocess.STDOUT).returncode
    return name, rc, time.time() - t0, log

def main(argv):
    fast, browser = '--fast' in argv, '--browser' in argv
    only = argv[argv.index('--works') + 1] if '--works' in argv else None
    shards = int(argv[argv.index('--shards') + 1]) if '--shards' in argv else 4
    t0 = time.time(); jobs = []
    if not browser:
        name, rc, dt, log = run('build', ['tools/site/build.py'])
        print(f'{"ok  " if rc == 0 else "FAIL"} build  {dt:5.0f} s', flush=True)
        if rc: print(open(log).read()[-3000:]); sys.exit('CHECKS FAILED: build')
        jobs = [('regen_check', ['tools/site/regen_check.py']), ('history_check', ['tools/site/history_check.py'])]
    if not fast:
        jobs.append(('smoke_test', ['tools/site/smoke_test.py']))
        if only:   # the per-work checks of these works, shared among the shards; the app-wide ones (shard 0) left to the CI
            n = min(shards - 1, len(only.split(','))) or 1
            jobs += [(f'ux_test-{k}', ['tools/site/ux_test.py', '--works', only, '--shard', f'{k}/{n + 1}']) for k in range(1, n + 1)]
        else: jobs += [(f'ux_test-{k}', ['tools/site/ux_test.py', '--shard', f'{k}/{shards}']) for k in range(shards)]
    bad = []
    with ThreadPoolExecutor(len(jobs)) as ex:
        for name, rc, dt, log in ex.map(lambda j: run(*j), jobs):
            out = open(log, encoding='utf-8', errors='replace').read()
            tail = [l for l in out.splitlines() if l.strip()][-1:] or ['']
            print(f'{"ok  " if rc == 0 else "FAIL"} {name}  {dt:5.0f} s   {tail[0][:110]}', flush=True)
            if rc:
                bad.append(name)
                fails = [l for l in out.splitlines() if l.startswith('FAIL') or 'Error' in l][:20]
                print('\n'.join('     ' + l[:300] for l in fails) or out[-2000:]); print(f'     (full output: {log})')
    print(f'{"all checks passed" if not bad else "FAILED: " + ", ".join(bad)} in {time.time() - t0:.0f} s' + (' (browser tests skipped: --fast)' if fast else ''))
    sys.exit(1 if bad else 0)

if __name__ == '__main__': main(sys.argv[1:])
