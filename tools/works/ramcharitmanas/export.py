"""Śrī Rāmacaritamānasa: book data (book/app_data.json) → library/tulsidas/ramcharitmanas/.

Writes   work.json                  the text (verse + number), kāṇḍas, topics, plans, vidhi
         meanings/hi-gitapress.json Hindi meaning source (Gita Press bhāvārtha)
         meanings/en-gitapress.json English meaning source (Gita Press translation)
Merges   its word meanings into library/gloss.json (adds new words; never overwrites existing ones).
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py, which registers the sources and checks everything.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ROOT = os.path.join(HERE, 'book')   # where app_data.json is built
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'tulsidas/ramcharitmanas'
d = json.load(open(os.path.join(ROOT, 'app_data.json')))
IT = d['it']; EG = d['eg']

def dump(path, obj):
    path = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(path)

# ---- the text: verse + number only (transliteration belongs to the text) ----
items = []
for x in IT:
    o = {'id': x['id'], 'p': x['k'], 's': x['s'], 'y': x['y'], 'n': x['n'], 'v': x['v']}
    if x.get('t'): o['t'] = x['t']
    items.append(o)
ids = [x['id'] for x in IT]
plans = {k: {'n': len(v), 'end': [ids[v[str(n)]] for n in range(1, len(v) + 1)]} for k, v in d['P'].items()}
work = {
    'id': 'manas',
    'title': {'hi': 'श्रीरामचरितमानस', 'en': 'Śrī Rāmacaritamānasa'},
    'by': {'hi': 'गोस्वामी तुलसीदास', 'en': 'Gosvāmī Tulasīdāsa'},
    'edition': {'hi': 'गीताप्रेस, गोरखपुर', 'en': 'Gita Press, Gorakhpur'},
    'colophon': {'hi': '।। इति श्रीरामचरितमानस समाप्त ।। सियावर रामचन्द्रकी जय', 'en': '।। इति श्रीरामचरितमानस समाप्त ।। Glory to Śrī Rāma'},
    'parts': {'name': {'hi': 'काण्ड', 'en': 'Kāṇḍa'}, 'list': d['kands']},
    'plans': [
        {'id': 'M', 'name': {'hi': 'मासपारायण', 'en': '30-day'}, 'long': {'hi': 'मासपारायण (३० दिन)', 'en': 'Māsa-pārāyaṇa (30 days)'}, 'unit': {'hi': 'विश्राम', 'en': 'Vishram'}, **plans['M']},
        {'id': 'N', 'name': {'hi': 'नवाह्नपारायण', 'en': '9-day'}, 'long': {'hi': 'नवाह्नपारायण (९ दिन)', 'en': 'Navāhna-pārāyaṇa (9 days)'}, 'unit': {'hi': 'विश्राम', 'en': 'Vishram'}, **plans['N']},
    ],
    'items': items,
    'topics': [{'id': ids[t['i']], 'hi': t['hi'], 'en': t.get('en') or t['hi']} for t in d['topics']],
    'vidhi': d['vidhi'],
    'vg': d['vg'],
}
sizes = {}
sizes['work'] = dump(WP + '/work.json', work)

# ---- Hindi meaning source ----
hi = {}
for x in IT:
    e = [x['h']]
    if x.get('f'): e.append(x['f'])
    hi[x['id']] = e
sizes['hi'] = dump(WP + '/meanings/hi-gitapress.json', {'id': 'hi-gitapress', 'lang': 'hi', 'order': 1, 'title': {'hi': 'गीताप्रेस — भावार्थ (हनुमानप्रसाद पोद्दार)', 'en': 'Gita Press — Hindi bhāvārtha (Hanumānprasād Poddār)'}, 'm': hi})

# ---- English meaning source (one entry per verse; footnotes attached) ----
en = {}
for x in IT:
    g = EG.get(str(x['g'])) if x.get('g') is not None else None
    if not g: continue
    e = [g['x']]
    if g.get('f'): e.append(g['f'])
    en[x['id']] = e
sizes['en'] = dump(WP + '/meanings/en-gitapress.json', {'id': 'en-gitapress', 'lang': 'en', 'order': 1, 'title': {'hi': 'गीताप्रेस — अंग्रेज़ी अनुवाद', 'en': 'Gita Press — English translation'}, 'm': en})

# ---- shared word meanings: add new words, keep existing ones ----
gp = os.path.join(OUT, 'gloss.json')
G = json.load(open(gp)) if os.path.exists(gp) else {}
new = {k: v for k, v in d['gloss'].items() if k not in G}
G.update(new); sizes['gloss'] = dump('gloss.json', G)
print({k: round(v / 1e6, 2) for k, v in sizes.items()}, 'MB;', len(new), 'new words')
