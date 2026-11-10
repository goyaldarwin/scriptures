"""Sweep inventory: every work on the shelf and in tools/works, with its sources, and what is missing where.
Usage: python3 -I inventory.py <scriptures repo> <scriptures-data repo> <out.md> <findings.json>"""
import json, os, sys, glob, re

REPO, DATA, OUT, FIND = sys.argv[1:5]
W = os.path.join(REPO, 'tools/works')

def walk(nodes, trail=()):
    for n in nodes:
        if 'work' in n:
            yield n, trail
        for x in walk(n.get('children', []), trail + (n['id'],)):
            yield x

idx = json.load(open(os.path.join(REPO, 'library/index.json')))
shelf = {n['work']: (n, t) for n, t in walk(idx)}
folders = sorted(d for d in os.listdir(W) if os.path.isdir(os.path.join(W, d)))
findings = []

def F(kind, work, msg):
    findings.append({'kind': kind, 'work': work, 'msg': msg})

for w in folders:
    if w not in shelf and os.path.exists(os.path.join(W, w, 'work.json')):
        F('A1', w, 'folder in tools/works but not on the shelf (index.json)')
for w in shelf:
    if w not in folders:
        F('A1', w, 'on the shelf but no tools/works folder')

rows = []
for w in folders:
    wj = os.path.join(W, w, 'work.json')
    if not os.path.exists(wj):
        continue
    man = json.load(open(wj))
    path = man.get('path')
    node, trail = shelf.get(w, ({}, ()))
    if node and node.get('path') != path:
        F('A1', w, f'index.json path {node.get("path")} != work.json path {path}')
    lib = os.path.join(REPO, 'library', path or '', 'work.json')
    nitems = None; langs = {}
    if os.path.exists(lib):
        L = json.load(open(lib))
        items = L.get('items', [])
        nitems = len(items)
        for it in items:
            l = it.get('l', L.get('lang'))
            langs[l] = langs.get(l, 0) + 1
        nparts = len(L.get('parts', {}).get('list', []))
    else:
        F('A8', w, f'no library/{path}/work.json'); nparts = None
    # meanings
    ms = sorted(os.path.relpath(p, os.path.join(W, w, 'meanings')) for p in glob.glob(os.path.join(W, w, 'meanings/*/*.json')))
    cms = sorted(os.path.relpath(p, os.path.join(W, w, 'commentary')) for p in glob.glob(os.path.join(W, w, 'commentary/*/*.json')))
    gl = sorted(os.path.basename(p) for p in glob.glob(os.path.join(W, w, 'glossary/*.json')))
    for req in ('README.md', 'reconciliation.md', 'text.txt'):
        if not os.path.exists(os.path.join(W, w, req)):
            F('A8', w, f'missing {req}')
    # audio
    auds = []
    for ad in sorted(glob.glob(os.path.join(W, w, 'audio/*/'))):
        aid = os.path.basename(ad.rstrip('/'))
        src = json.load(open(os.path.join(ad, 'source.json'))) if os.path.exists(os.path.join(ad, 'source.json')) else None
        if src is None:
            F('A8', w, f'audio/{aid}: no source.json'); continue
        recs = json.load(open(os.path.join(ad, 'recordings.json'))) if os.path.exists(os.path.join(ad, 'recordings.json')) else []
        take = src.get('take')
        if not recs and not take:
            F('A7', w, f'audio/{aid}: no recordings.json and no take')
        missing = 0; nodata = 0
        for r in recs:
            d = r.get('data')
            if not d:
                nodata += 1
            elif not os.path.exists(os.path.join(DATA, d)):
                missing += 1
        if nodata:
            F('A7', w, f'audio/{aid}: {nodata} of {len(recs)} recordings name no file in scriptures-data ("data")')
        if missing:
            F('A7', w, f'audio/{aid}: {missing} of {len(recs)} recordings\' "data" files are not in scriptures-data')
        jb = sum(1 for r in recs if 'start' in r or 'end' in r)
        files = sorted(os.listdir(ad))
        flags = [f for f in ('fixes.json', 'fixes.md', 'aligned.json', 'aligned.md', 'check.json', 'owner.json') if f in files]
        if 'fixes.json' in files and 'fixes.md' not in files:
            F('A7', w, f'audio/{aid}: fixes.json without fixes.md')
        auds.append(f'{aid} ({len(recs)} rec{", take " + take if take else ""}{", " + str(jb) + " stretch" if jb else ""}; {" ".join(flags) or "—"}{"; draft" if src.get("draft") else ""}{"; review" if src.get("review") else ""})')
    # scriptures-data folder
    dpath = os.path.join(DATA, path or '')
    dk = sorted(os.listdir(dpath)) if os.path.isdir(dpath) else []
    if not dk:
        F('A1', w, f'no folder in scriptures-data at {path}')
    rows.append((path, w, man.get('lang'), nparts, nitems, langs, ms, cms, gl, auds, dk))

rows.sort()
with open(OUT, 'w') as f:
    f.write('# Inventory\n\nMade by the sweep from `library/index.json`, `tools/works/*` and `scriptures-data` (`python3 tools/sweep/inventory.py . <clone of scriptures-data> docs/reviews/sweep/inventory.md <findings.json>`; re-run to refresh). Columns: shelf path · work id · language(s) of verses · parts · verses · meaning sources (lang/source) · commentaries · own glossary files · recordings (count; inputs present) · kinds of source in scriptures-data.\n\n')
    f.write(f'{len(rows)} works in `tools/works`, {len(shelf)} on the shelf.\n\n')
    f.write('| Path | Id | Verses: languages | Parts | Verses | Meanings | Commentary | Own glossary | Recordings | scriptures-data |\n|---|---|---|---|---|---|---|---|---|---|\n')
    for path, w, lang, np, ni, langs, ms, cms, gl, auds, dk in rows:
        lg = ', '.join(f'{k} {v}' for k, v in sorted(langs.items(), key=lambda x: -x[1]))
        f.write(f'| `{path}` | `{w}` | {lg} | {np} | {ni} | {", ".join(m[:-5] for m in ms) or "—"} | {", ".join(c[:-5] for c in cms) or "—"} | {", ".join(gl) or "—"} | {"; ".join(auds) or "—"} | {", ".join(dk) or "**none**"} |\n')
json.dump(findings, open(FIND, 'w'), ensure_ascii=False, indent=1)
print(len(rows), 'works;', len(findings), 'findings')
from collections import Counter
print(Counter(x['kind'] for x in findings))
