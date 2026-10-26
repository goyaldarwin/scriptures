"""Readers keep bookmarks, notes, progress and saved places by work id and verse id, and audio times point at verse ids:
an id that disappears silently loses them. This check compares library/ with an earlier commit (the base of a pull
request, or the previous main) and fails when

  - a work on the shelf (library/index.json) is gone, unless library/removed.json lists it under `works`;
  - a verse id of a work is gone, unless the work's work.json maps it in `renamed` (old id → new id) or lists it in
    `removed` (a verse taken out on purpose; its id is never used again).

    python3 tools/site/history_check.py <git ref or commit>      (default: origin/main)
"""
import json, os, subprocess, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def git_json(ref, path):
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], cwd=REPO, capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None

def works(shelf):
    for n in shelf:
        if 'work' in n: yield n
        else: yield from works(n.get('children', []))

def main():
    ref = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'origin/main'
    old_idx = git_json(ref, 'library/index.json')
    if old_idx is None: print(f'history check: {ref} has no library/index.json; nothing to compare'); return
    new_idx = json.load(open(os.path.join(REPO, 'library', 'index.json'), encoding='utf-8'))
    old_w = {n['work']: n.get('path') for n in works(old_idx)}; new_w = {n['work']: n.get('path') for n in works(new_idx)}
    rp = os.path.join(REPO, 'library', 'removed.json'); retired = set(json.load(open(rp, encoding='utf-8')).get('works', {})) if os.path.exists(rp) else set()
    bad = [f'work {w} is gone from the shelf (list it in library/removed.json → works if that is meant)' for w in old_w if w not in new_w and w not in retired]
    n = 0
    for wid, path in old_w.items():
        if wid not in new_w: continue
        a = git_json(ref, f'library/{old_w[wid]}/work.json'); p = os.path.join(REPO, 'library', new_w[wid], 'work.json')
        if a is None or not os.path.exists(p): continue
        b = json.load(open(p, encoding='utf-8'))
        keep = {x['id'] for x in b['items']} | set(b.get('renamed') or {}) | set(b.get('removed') or [])
        lost = [x['id'] for x in a['items'] if x['id'] not in keep]; n += len(a['items'])
        if lost: bad.append(f"{wid}: {len(lost)} verse ids are gone, e.g. {lost[:5]} (map them in work.json → renamed, or list them in removed)")
    if bad:
        print('FAIL: ids that readers\' bookmarks, notes, places and audio times point at would be lost:'); [print('  ' + b) for b in bad]; sys.exit(1)
    print(f'history check: every work and all {n} verse ids of {ref} are still here (or renamed / removed on purpose)')

if __name__ == '__main__': main()
