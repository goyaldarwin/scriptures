"""Check that the standalone Sundarakāṇḍa's first part is exactly the Mānas's Sundara-kāṇḍa.

Compares every item (all fields except the part index `p`), the order of the items, the topics, and the Gita Press
Hindi and English meanings (the same entry for every item, and the same source id, language, order and title).
Usage: python3 tools/works/sundarkand/check.py        (exits non-zero on any difference)
"""
import json, os, sys
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
L = lambda rel: json.load(open(os.path.join(REPO, 'library', rel), encoding='utf-8'))
MP, SP = 'hinduism/granth/tulsidas/ramcharitmanas', 'hinduism/granth/tulsidas/sundarkand'
M, S = L(MP + '/work.json'), L(SP + '/work.json')
K = next(k for k, p in enumerate(M['parts']['list']) if p['en'].startswith('Sundara'))
mi = [x for x in M['items'] if x['p'] == K]
si = [x for x in S['items'] if x['p'] == 0]
bad = []
strip = lambda x: {k: v for k, v in x.items() if k != 'p'}
if [x['id'] for x in mi] != [x['id'] for x in si]: bad.append('item ids or order differ')
bad += [f"item {a['id']} differs" for a, b in zip(mi, si) if strip(a) != strip(b)]
if S['items'][:len(si)] != si: bad.append('the Sundarakāṇḍa is not the first part')
ids = {x['id'] for x in mi}
if [t for t in M['topics'] if t['id'] in ids] != [t for t in S['topics'] if t['id'] in ids]: bad.append('topics differ')
for sid in ('hi-gitapress', 'en-gitapress'):
    a, b = L(f'{MP}/meanings/{sid}.json'), L(f'{SP}/meanings/{sid}.json')
    if {k: v for k, v in a.items() if k != 'm'} != {k: v for k, v in b.items() if k != 'm'}: bad.append(f'{sid}: header differs')
    if {i: a['m'][i] for i in ids if i in a['m']} != b['m']: bad.append(f'{sid}: meanings differ')
print(f'{len(mi)} items, {sum(1 for t in S["topics"] if t["id"] in ids)} topics, 2 meaning sources compared:', 'identical' if not bad else 'DIFFERENT')
for x in bad[:20]: print(' ', x)
sys.exit(1 if bad else 0)
