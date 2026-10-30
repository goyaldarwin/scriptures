"""Prepare batches of verses for writing our own meanings (tools/meanings/style.md).

    python3 tools/meanings/prepare.py OUT_DIR FIRST_ID LAST_ID [--size 50] [--context 6]
            [--work manas]   (a work's id: its folder in tools/works)

Splits the verses FIRST_ID..LAST_ID (reading order, inclusive) into batches that end on a section (dohā) boundary,
about --size verses each, and writes OUT_DIR/batch-NN.md for each: the topic headings, the verses just before the batch
(for context), then every verse of the batch with its transliteration and the meaning of each of its words from our
dictionaries (language of the verse, then its fallbacks, then the suffix rules, as the app looks words up). Verses that
already have both our meanings are marked so the writer keeps them unless they are wrong. Also writes
OUT_DIR/batch-NN.ids (one id per line), which is what the writer must cover exactly.

It reads only; it never writes into library/ or the meaning files.
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९੦-੯0-9]")   # the app's rule (tools/site/app.js): Devanagari and Gurmukhi digits are verse numbers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('first'); ap.add_argument('last')
    ap.add_argument('--size', type=int, default=50); ap.add_argument('--context', type=int, default=6)
    ap.add_argument('--work', default='manas')
    a = ap.parse_args()
    import sanskrit_dict   # Monier-Williams and Apte check the hard words (style.md); no batch is made without them
    missing = [d for d in sanskrit_dict.DICTS if not os.path.exists(os.path.join(sanskrit_dict.CACHE, d + '.txt'))]
    if missing:
        raise SystemExit(f'The Sanskrit dictionaries are not downloaded ({", ".join(missing)}): run python3 tools/meanings/sanskrit_dict.py fetch first')
    lib = os.path.join(REPO, 'library'); folder = os.path.join(REPO, 'tools', 'works', a.work)
    path = json.load(open(os.path.join(folder, 'work.json'), encoding='utf-8'))['path']
    W = json.load(open(os.path.join(lib, path, 'work.json'), encoding='utf-8'))
    LANGS = json.load(open(os.path.join(lib, 'glossary', 'languages.json'), encoding='utf-8'))
    G = {}
    def gloss(lg):
        if lg not in G: G[lg] = json.load(open(os.path.join(lib, 'glossary', lg + '.json'), encoding='utf-8'))
        return G[lg]
    own = os.path.join(lib, path, 'glossary.json')
    OWN = json.load(open(own, encoding='utf-8')) if os.path.exists(own) else {}
    mine = lambda lg: os.path.join(folder, 'meanings', lg, 'scriptures.json')   # our own meanings (tools/works/README.md)
    ours = {lg: json.load(open(mine(lg), encoding='utf-8')).get('m', {}) if os.path.exists(mine(lg)) else {} for lg in ('hi', 'en')}

    def lookup(w, lg):
        chain = [lg] + LANGS[lg].get('fallback', [])
        for c in chain:
            for D in (OWN.get(c, {}), gloss(c)):
                if w in D: return c, w, D[w]
        for c in chain:
            for suf in LANGS[c].get('suffixes', []):
                if w.endswith(suf) and len(w) > len(suf):
                    for st in LANGS[c].get('stems', ['']):
                        r = w[:-len(suf)] + st
                        for D in (OWN.get(c, {}), gloss(c)):
                            if r in D: return c, r, D[r]
        return None

    items = W['items']; ids = [x['id'] for x in items]
    i0, i1 = ids.index(a.first), ids.index(a.last)
    topics = {t['id']: t for t in W.get('topics', [])}
    parts = W['parts']['list']
    # batches end where the section changes
    batches, cur = [], []
    for i in range(i0, i1 + 1):
        cur.append(i)
        nxt = items[i + 1]['s'] if i + 1 < len(items) else None
        if len(cur) >= a.size and (i == i1 or nxt != items[i]['s']): batches.append(cur); cur = []
    if cur: batches.append(cur)
    os.makedirs(a.out, exist_ok=True)
    for n, b in enumerate(batches, 1):
        L = [f'# Batch {n:02d}: {ids[b[0]]} … {ids[b[-1]]} ({len(b)} verses)', '',
             f'Work: {W["title"]["en"]} · part: {parts[items[b[0]]["p"]]["en"]}', '']
        ctx = range(max(0, b[0] - a.context), b[0])
        if ctx:
            L += ['## Just before this batch (context only; do not write these)', '']
            for i in ctx: L.append(f'- `{ids[i]}` ' + ' / '.join(items[i]['v']))
            L.append('')
        L += ['## Verses to write', '']
        for i in b:
            x = items[i]; lg = x.get('l', W['lang'])
            if x['id'] in topics: L += [f'### ▸ Topic: {topics[x["id"]]["hi"]} — {topics[x["id"]]["en"]}', '']
            done = x['id'] in ours['hi'] and x['id'] in ours['en']
            L.append(f'#### `{x["id"]}` · {x["y"]} {x["n"]} · language {lg}' + (' · ALREADY WRITTEN (keep unless wrong)' if done else ''))
            L += ['', *[f'> {l}' for l in x['v']], '']
            if x.get('t'): L += [f'*{" / ".join(x["t"])}*', '']
            seen = set()
            for l in x['v']:
                for t in l.split():
                    w = PUNCT.sub('', t)
                    if not w or w in seen: continue
                    seen.add(w); f = lookup(w, lg)
                    if not f: L.append(f'- {w}: (no entry)')
                    else:
                        c, r, e = f
                        extra = ', '.join(x_ for x_ in (e.get('g'), e.get('r') and f'root {e["r"]}') if x_)
                        L.append(f'- {w}{"" if r == w else " → " + r}{"" if c == lg else " [" + c + "]"}: {e.get("hi", "")} | {e.get("en", "")}' + (f' ({extra})' if extra else ''))
            if done: L += ['', f'Our Hindi: {ours["hi"][x["id"]]}', f'Our English: {ours["en"][x["id"]]}']
            L.append('')
        open(os.path.join(a.out, f'batch-{n:02d}.md'), 'w', encoding='utf-8').write('\n'.join(L))
        open(os.path.join(a.out, f'batch-{n:02d}.ids'), 'w').write('\n'.join(ids[i] for i in b) + '\n')
        print(f'batch-{n:02d}: {ids[b[0]]} … {ids[b[-1]]} ({len(b)} verses)')

if __name__ == '__main__':
    main()
