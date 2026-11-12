"""Prepare batches of Sri Guru Granth Sahib for writing our own Punjabi and English meanings (docs/HOW-TO.md, "Write our
own meanings for Sri Guru Granth Sahib"; tools/meanings/style.md §12, §13; the briefs tools/meanings/briefs/gurbani-*.md).

    python3 tools/meanings/gurbani_prepare.py OUT_DIR FIRST_ID LAST_ID --db DATABASE [--lines 150] [--context 2]

DATABASE is the Shabad OS database (build/database.sqlite of @shabados/database 4.8.7, whose npm package is in the
private scriptures-data: sikhism/gurbani/guru-granth-sahib/printouts/shabados/). OUT_DIR is a scratch folder outside
this repository: what it gets quotes copyrighted translations and is never committed here (its records, if kept, go to
scriptures-data, under the work's meaning-records/).

Splits the Granth's own verses FIRST_ID..LAST_ID (reading order, inclusive; the taken Japji and Sukhmani are skipped,
they have their own meanings) into batches of about --lines verse lines, never cutting a verse, and writes for each:
  batch-NN.md        the part, the verses just before (context), then each verse: its id, type, writer, its lines
                     numbered from 0 with their transliteration, and our Punjabi word meanings where we have them;
  batch-NN.ids       one id per line: what the writer covers, exactly;
  batch-NN.refs.md   for every line, the line-by-line translations of the Shabad OS database (Prof. Sahib Singh,
                     Bhai Manmohan Singh, the Faridkot Teeka, in Punjabi; Dr. Sant Singh Khalsa, Bhai Manmohan Singh,
                     in English): read only to check a reading, after the draft, never copied;
  copied-<source>.json  {"m": {id: [one piece per line]}} for each of those sources over the batches, for overlap.py.
It reads only; it never writes into the repository.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
GGS = os.path.join(REPO, 'tools', 'works', 'guru-granth-sahib')
sys.path.insert(0, os.path.join(GGS, 'source')); import shabados, make
sys.path.insert(0, os.path.join(REPO, 'tools', 'works')); import textfile

# Shabad OS translation sources: id → (file name, label). Line-by-line for every Granth line unless noted.
# (The database's Jaggi, Kohli and Bhai Vir Singh translations are of the Dasam Granth and the Vaaran, not of this Granth.)
SOURCES = {6: ('pa-sahib-singh', 'Prof. Sahib Singh (pa, ©)'), 3: ('pa-manmohan-singh', 'Bhai Manmohan Singh (pa, ©)'),
           5: ('pa-faridkot', 'Faridkot Teeka (pa, public domain)'),
           1: ('en-sant-singh-khalsa', 'Dr. Sant Singh Khalsa (en, ©)'), 2: ('en-manmohan-singh', 'Bhai Manmohan Singh (en, ©)')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('first'); ap.add_argument('last'); ap.add_argument('--db', required=True)
    ap.add_argument('--lines', type=int, default=150); ap.add_argument('--context', type=int, default=2)
    a = ap.parse_args()
    if os.path.abspath(a.out).startswith(REPO + os.sep): sys.exit('OUT_DIR must be outside the repository')
    sys.path.insert(0, HERE); import sanskrit_dict
    if sanskrit_dict.missing(): sys.exit('run python3 tools/meanings/sanskrit_dict.py fetch first (style.md §10)')
    W = json.load(open(os.path.join(REPO, 'library', 'sikhism', 'gurbani', 'guru-granth-sahib', 'work.json'), encoding='utf-8'))
    items = W['items']; ids = [x['id'] for x in items]; parts = W['parts']['list']
    writer = {}
    for v in W['views']:
        if v['id'] != 'writer': continue
        for g in v['groups']:
            for w in g['list']:
                for i in w['items']: writer.setdefault(i, w['en'])
    PA = json.load(open(os.path.join(REPO, 'library', 'glossary', 'pa.json'), encoding='utf-8'))

    # each own verse's lines → the database's line ids (as source/faridkot.py does)
    U = shabados.units(shabados.EXTRACT); V = [x for x in make.verses(U) if 'take' not in x]
    T = textfile.read(os.path.join(GGS, 'text.txt'))
    assert [x['v'] for x in T] == [[l['v'] for l in x['lines']] for x in V], 'text.txt is stale: run make.py'
    LID = {t['id']: [l['id'] for l in x['lines']] for t, x in zip(T, V)}
    TR = {sid: shabados.translations(a.db, sid) for sid in SOURCES}

    i0, i1 = ids.index(a.first), ids.index(a.last)
    sel = [i for i in range(i0, i1 + 1) if ids[i] in LID]
    batches, cur, n = [], [], 0
    for i in sel:
        cur.append(i); n += len(items[i]['v'])
        nxt = sel[sel.index(i) + 1] if i != sel[-1] else None
        if n >= a.lines or nxt is None or items[nxt]['p'] != items[i]['p']: batches.append(cur); cur, n = [], 0
    if cur: batches.append(cur)
    os.makedirs(a.out, exist_ok=True)
    copied = {f: {} for f, _ in SOURCES.values()}
    for k, b in enumerate(batches, 1):
        L = [f'# Batch {k:02d}: {ids[b[0]]} … {ids[b[-1]]} ({len(b)} verses, {sum(len(items[i]["v"]) for i in b)} lines)', '',
             f'Work: Sri Guru Granth Sahib · part: {parts[items[b[0]]["p"]]["en"]}', '']
        ctx = [j for j in range(max(0, b[0] - a.context), b[0])]
        if ctx:
            L += ['## Just before this batch (context only; do not write these)', '']
            for j in ctx: L.append(f'- `{ids[j]}` ' + ' / '.join(items[j]['v']))
            L.append('')
        R = [f'# References for batch {k:02d}: read only after your draft, to check a reading; never copy their wording', '']
        for i in b:
            x = items[i]; vid = x['id']
            L += [f'## `{vid}` · {x["y"]} · {writer.get(vid, "")} · Ang {x["s"]} · {len(x["v"])} lines', '']
            R += [f'## `{vid}`', '']
            for j, (g, t) in enumerate(zip(x['v'], x.get('t') or [''] * len(x['v']))):
                L.append(f'{j}. {g}  \n   _{t}_')
                words = [w.strip('॥।,.') for w in g.split()]
                known = [f'{w}: {PA[w].get("pa") or PA[w].get("en")}' for w in dict.fromkeys(words) if w in PA and isinstance(PA[w], dict)]
                if known: L.append('   words: ' + '; '.join(known))
                R.append(f'{j}. {g}')
                lid = LID[vid][j]
                for sid, (f, label) in SOURCES.items():
                    tr = (TR[sid].get(lid) or ('', ''))[0] or ''
                    tr = tr.replace('☬', ' ').strip()
                    copied[f].setdefault(vid, []).append(tr)
                    if tr: R.append(f'   - {label}: {tr}')
            L.append(''); R.append('')
        open(os.path.join(a.out, f'batch-{k:02d}.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        open(os.path.join(a.out, f'batch-{k:02d}.refs.md'), 'w', encoding='utf-8').write('\n'.join(R) + '\n')
        open(os.path.join(a.out, f'batch-{k:02d}.ids'), 'w').write('\n'.join(ids[i] for i in b) + '\n')
    for f, m in copied.items():
        json.dump({'m': m}, open(os.path.join(a.out, f'copied-{f}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{len(batches)} batches, {sum(len(b) for b in batches)} verses, '
          f'{sum(len(items[i]["v"]) for b in batches for i in b)} lines → {a.out}')


if __name__ == '__main__':
    main()
