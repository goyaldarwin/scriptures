"""Check that the English of written word batches is the witnesses' gloss as they give it (BRIEF.md): for an entry
whose `src` names only witnesses (iitk, vr, iitk+vr), every "; "-part of `en` must be a whole gloss of one of the
word's verses or the three either side (the witnesses divide verses differently; verse_glosses.json, beside the
batch). Prints the entries that fail, to be written again.

    python3 check_en.py <batch>.json …          (each with its <batch>.json.out.json)
"""
import json, os, sys

def near(i):
    k, s, n = i.rsplit('.', 2)
    return [f'{k}.{s}.{m}' for m in range(int(n) - 3, int(n) + 4)] if n.isdigit() else [i]

def clean(t):
    return ' '.join(t.split()).rstrip('.').strip()

fails, total = [], 0
for f in sys.argv[1:]:
    G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(f)), 'verse_glosses.json')))
    O = json.load(open(f + '.out.json'))
    for w in json.load(open(f)):
        e = O.get(w['word']); total += 1
        if not e:
            fails.append((f, w['word'], 'missing')); continue
        if 'ours' in e.get('src', 'ours').split('+'):
            continue
        have = {clean(en) for c in w['contexts'] for i in near(c['id']) for k in ('iitk', 'vr') for _, en in G.get(i, {}).get(k, [])}
        bad = [p for p in e['en'].split('; ') if clean(p) not in have]
        if bad:
            fails.append((f, w['word'], e['en']))
for x in fails:
    print(*x, sep='\t')
print(len(fails), 'of', total, 'entries fail', file=sys.stderr)
