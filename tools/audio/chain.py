"""The whole audio chain for one recording source, in one command (tools/audio/METHOD.md, docs/HOW-TO.md "Add a new audio source").

    python3 tools/audio/chain.py tools/works/<work>/audio/<source> [--branch B] [--data-ref R] [--per-job N] [--lean S]
                                 [--whole] [--skip id,id] [--realign] [--no-pr] [--trailer LINE]... [--dry-run]

Before it: source.json and recordings.json written, each recording's speech-quality copy in scriptures-data (its "data"
path), as docs/HOW-TO.md says. Then, in order, each step skipped when it is already done, so a stopped run is started
again with the same command:
  1. a branch: --branch, else the branch checked out if it is not main, else audio-<source id> made from main;
     tools/works/export.py <work>, so the library has the work's current text;
  2. transcribe (not for a source timed line by line, "lines": true): the recordings with no finished transcript
     (transcripts/<id>.jsonl.done) go to the `transcribe` workflow, which commits their transcripts to the branch; it waits
     for the runs and pulls;
  3. make_timings.py (the rough starts: the transcript's, or spread by length for "lines");
  4. mms_windows.py (--whole for "lines", or when asked, with --skip); where a recording's windows changed (a text changed),
     its old MMS result (mms/<id>.json) is removed, because the align workflow keeps a result it finds; a source with MMS
     starts made another way (aligned.json without mms/windows.json: the Mānas) is aligned again only with --realign;
  5. MMS: the recordings with no result go to the `align` workflow (--per-job for many short recordings); it waits and pulls;
  6. mms_merge.py --lean (--lean, else the lean the source's check.json names, else 0.6), make_timings.py, aligned_md.py;
  7. tools/site/build.py, so docs/PENDING.md and docs/WORKS.md follow;
  8. commit, push, and a pull request to main (unless --no-pr, or one is open for the branch). CI runs the full check there.
The owner's starts (owner.json) and the hand fixes (fixes.json) are never touched: make_timings.py lets them win.
--trailer adds a line to the end of each commit message (a session's attribution). --dry-run prints the plan only.
Workflows are started and read with the GitHub REST API (`gh api`); GraphQL is not used.
"""
import glob, hashlib, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
GH = 'repos/goyaldarwin/scriptures'
POLL, WAIT_MAX = 60, 6 * 3600

def arg(name, default=None, many=False):
    A = sys.argv[1:]; got = [A[k + 1] for k, a in enumerate(A) if a == name and k + 1 < len(A)]
    return got if many else (got[-1] if got else default)

def flag(name): return name in sys.argv[1:]

def sh(cmd, check=True, quiet=False):
    if not quiet: print('  $', ' '.join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if check and r.returncode: sys.exit(f'failed ({r.returncode}): {" ".join(cmd)}\n{r.stdout[-2000:]}{r.stderr[-2000:]}')
    return r.stdout

def py(script, *a): return sh([sys.executable, os.path.join(REPO, script), *a])

def gh(path, *a, check=True): return sh(['gh', 'api', path, *a], check=check, quiet=True)

def git_commit(msg, paths, trailers):
    sh(['git', 'add', '-A', '--', *paths])
    if not sh(['git', 'diff', '--cached', '--name-only'], quiet=True).strip(): return False
    sh(['git', 'commit', '-q', '-m', msg + ('\n\n' + '\n'.join(trailers) if trailers else '')])
    return True

def git_push(branch):
    sh(['git', 'pull', '-q', '--rebase', 'origin', branch], check=False)
    sh(['git', '-c', 'push.negotiate=true', 'push', '-q', '-u', 'origin', branch])

def dispatch_and_wait(workflow, inputs, title):
    """Start a workflow_dispatch run and wait until it ends; the run is the one whose title names this source and branch
    (the workflows' run-name), else the newest of this workflow started after the dispatch."""
    t0 = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 5))
    gh(f'{GH}/actions/workflows/{workflow}/dispatches', '-X', 'POST', '-f', 'ref=main', *[x for k, v in inputs.items() for x in ('-f', f'inputs[{k}]={v}')])
    print(f'  started {workflow}: {title}', flush=True)
    run, start = None, time.time()
    while time.time() - start < WAIT_MAX:
        time.sleep(POLL if run else 10)
        if run is None:
            runs = json.loads(gh(f'{GH}/actions/workflows/{workflow}/runs?event=workflow_dispatch&per_page=30&created=%3E%3D{t0}'))['workflow_runs']
            mine = [r for r in runs if r.get('display_title') == title] or [r for r in runs if r.get('display_title', '') == workflow.split('.')[0]]
            if mine: run = min(mine, key=lambda r: r['created_at'])['id']; print(f'  run {run}', flush=True)
            continue
        r = json.loads(gh(f'{GH}/actions/runs/{run}'))
        if r['status'] == 'completed':
            print(f'  run {run}: {r["conclusion"]}', flush=True); return r['conclusion']
    sys.exit(f'{workflow} run {run} still not finished after {WAIT_MAX // 3600} h: start this command again later; it goes on from there')

def by_track(p):
    if not os.path.exists(p): return {}
    out = {}
    for w in json.load(open(p, encoding='utf-8')): out.setdefault(w['yt'], []).append(w)
    return {k: hashlib.sha1(json.dumps(v, sort_keys=True, ensure_ascii=False).encode()).hexdigest() for k, v in out.items()}

def windows_stale(src, meta, wpath):
    """No windows yet, a recording with none, or a verse whose text (as the aligner is given it) is no longer the work's."""
    if not os.path.exists(wpath): return True
    sys.path.insert(0, HERE); from mms_windows import rom
    work = json.load(open(os.path.join(REPO, 'library', meta['work'], 'work.json'), encoding='utf-8'))
    T = {x['id']: rom(x.get('t') or []) for x in work['items']}
    W = json.load(open(wpath, encoding='utf-8'))
    recs = {r['yt'] for r in json.load(open(os.path.join(src, 'recordings.json'), encoding='utf-8'))}
    if recs - {w['yt'] for w in W}: return True
    return any(l['id'] not in T or l['rom'] != T[l['id']] for w in W for l in w['lines'])

def batches(ids, n): return [ids[k:k + n] for k in range(0, len(ids), n)]

def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith('-'): sys.exit(__doc__)
    src = os.path.abspath(sys.argv[1]); rel = os.path.relpath(src, REPO)
    meta = json.load(open(os.path.join(src, 'source.json'), encoding='utf-8'))
    recs = json.load(open(os.path.join(src, 'recordings.json'), encoding='utf-8'))
    wid = os.path.relpath(src, os.path.join(REPO, 'tools', 'works')).split(os.sep)[0]
    lines = bool(meta.get('lines')); trailers = arg('--trailer', many=True); dry = flag('--dry-run')
    ids = [r['yt'] for r in recs]
    nodata = [r['yt'] for r in recs if not r.get('data')]
    if nodata: sys.exit(f'no "data" path in recordings.json for {", ".join(nodata)}: put its copy in scriptures-data first (docs/HOW-TO.md)')

    cur = sh(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], quiet=True).strip()
    branch = arg('--branch') or (cur if cur != 'main' else f'audio-{meta["id"]}')
    tdir = os.path.join(src, 'transcripts')
    todo_t = [] if lines else [i for i in ids if not os.path.exists(os.path.join(tdir, i + '.jsonl.done'))]
    print(f'{rel}: {len(ids)} recording(s), work {wid}, branch {branch}' + (', timed line by line' if lines else f', {len(todo_t)} to transcribe'))
    if dry:
        print('plan: export → ' + ('' if lines else 'transcribe → ') + 'make_timings → mms_windows → align → mms_merge, make_timings, aligned_md → build → commit, push, PR'); return

    # 1. the branch, and the work's current text in the library
    if sh(['git', 'status', '--porcelain', '--untracked-files=no'], quiet=True).strip(): sys.exit('the working tree has uncommitted changes: commit or stash them first')
    if cur != branch:
        if sh(['git', 'rev-parse', '--verify', '-q', branch], check=False, quiet=True).strip(): sh(['git', 'checkout', '-q', branch])
        else: sh(['git', 'checkout', '-q', 'main']); sh(['git', 'pull', '-q', '--ff-only']); sh(['git', 'checkout', '-q', '-b', branch])
    git_commit(f'{meta["id"]}: the recording source ({rel})', [rel], trailers)
    py('tools/works/export.py', wid)
    git_commit(f'{wid}: exported before timing {meta["id"]}', ['library', 'tools/works/' + wid], trailers)
    git_push(branch)

    # 2. transcripts (the transcribe workflow commits them to the branch)
    if todo_t:
        for b in batches(todo_t, 256):
            dispatch_and_wait('transcribe.yml', {'source': rel, 'ids': ','.join(b), 'ref': branch, 'data_ref': arg('--data-ref', '')}, f'transcribe {rel} ({branch})')
        sh(['git', 'pull', '-q', '--rebase', 'origin', branch])
        left = [i for i in todo_t if not os.path.exists(os.path.join(tdir, i + '.jsonl.done'))]
        if left: sys.exit(f'not transcribed yet: {", ".join(left)} (a job ran out of time or failed): start this command again; it goes on from there')

    # 3–4. rough starts and MMS windows, cut only when there are none yet or the text they hold is no longer the work's;
    # then from the rough starts alone (the transcript's, the owner's and the hand fixes), MMS's earlier result set aside,
    # because windows cut from MMS's own starts would move on every run. A recording whose windows changed loses its old result.
    wpath = os.path.join(src, 'mms', 'windows.json')
    if os.path.exists(os.path.join(src, 'aligned.json')) and not os.path.exists(wpath) and not flag('--realign'):
        sys.exit('this source has MMS starts (aligned.json) made another way, without mms/windows.json: aligning it again costs a '
                 'run on every recording; ask with --realign if that is meant')
    if not windows_stale(src, meta, wpath):
        print('  MMS windows hold the current text: kept')
        before = after = None
    else:
      al = os.path.join(src, 'aligned.json'); hold = al + '.hold'
      if os.path.exists(al): os.replace(al, hold)
      try:
        py('tools/audio/make_timings.py', rel)
        before = by_track(wpath)
        a = [rel] + (['--whole'] if lines or flag('--whole') else []) + (['--skip', arg('--skip')] if arg('--skip') else [])
        py('tools/audio/mms_windows.py', *a)
        after = by_track(wpath)
      finally:
        if os.path.exists(hold): os.replace(hold, al)
      for i in ids:
        res = os.path.join(src, 'mms', i + '.json')
        if os.path.exists(res) and before.get(i) != after.get(i):
            os.remove(res); print(f'  {i}: windows changed, its old MMS result removed')
      git_commit(f'{meta["id"]}: rough starts and MMS windows ({rel})', [rel, 'library'], trailers)
      git_push(branch)

    # 5. MMS (the align workflow commits mms/<id>.json to the branch)
    todo_a = [i for i in ids if not os.path.exists(os.path.join(src, 'mms', i + '.json'))]
    if todo_a:
        per = int(arg('--per-job', '1'))
        for b in batches(todo_a, 256 * per):
            dispatch_and_wait('align.yml', {'source': rel, 'ids': ','.join(b), 'ref': branch, 'data_ref': arg('--data-ref', ''), 'per_job': str(per)}, f'align {rel} ({branch})')
        sh(['git', 'pull', '-q', '--rebase', 'origin', branch])
        left = [i for i in todo_a if not os.path.exists(os.path.join(src, 'mms', i + '.json'))]
        if left: sys.exit(f'not aligned yet: {", ".join(left)}: start this command again; it goes on from there')

    # 6. MMS's starts into the timings
    lean = arg('--lean')
    if not lean and os.path.exists(os.path.join(src, 'check.json')):
        m = re.search(r'lean ([\d.]+) s', json.load(open(os.path.join(src, 'check.json'), encoding='utf-8')).get('why', ''))
        lean = m.group(1) if m else None
    py('tools/audio/mms_merge.py', rel, '--lean', lean or '0.6')
    py('tools/audio/make_timings.py', rel)
    py('tools/audio/aligned_md.py', rel)

    # 7. the generated docs
    py('tools/site/build.py')

    # 8. commit, push, pull request
    git_commit(f'{meta["id"]}: timed with MMS ({rel})', [rel, 'library', 'docs', 'app'], trailers)
    git_push(branch)
    if flag('--no-pr'): return
    if json.loads(gh(f'{GH}/pulls?head=goyaldarwin:{branch}&state=open')): print(f'  a pull request for {branch} is open: pushed to it'); return
    body = (f'The audio chain (`tools/audio/chain.py`) for `{rel}`: ' + ('' if lines else 'transcripts, ') +
            'rough starts, MMS windows and starts, the merge (`aligned.json`, `check.json`), the timings and `aligned.md`, then the build. '
            'Read `aligned.md` and the first and last verse each recording found before merging.')
    pr = json.loads(gh(f'{GH}/pulls', '-X', 'POST', '-f', f'title=Audio: {meta["title"]["en"]} ({wid})', '-f', f'head={branch}', '-f', 'base=main', '-f', f'body={body}'))
    print(f'  pull request #{pr["number"]}: {pr["html_url"]}')

if __name__ == '__main__': main()
