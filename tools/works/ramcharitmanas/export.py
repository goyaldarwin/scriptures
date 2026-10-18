"""Śrī Rāmacaritamānasa: book data (book/app_data.json) → library/tulsidas/ramcharitmanas/.

Writes   work.json                  the text (verse + number), kāṇḍas, topics, plans, vidhi
         meanings/hi-gitapress.json Hindi meaning source (Gita Press bhāvārtha)
         meanings/en-gitapress.json English meaning source (Gita Press translation)
Merges   its word meanings into library/glossary/sa.json and awa.json by the language of the verses
         they occur in (adds new words; never overwrites existing ones).
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py, which registers the sources and checks everything.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); import jsonio

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ROOT = os.path.join(HERE, 'book')   # where app_data.json is built
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/granth/tulsidas/ramcharitmanas'
d = json.load(open(os.path.join(ROOT, 'app_data.json')))
IT = d['it']; EG = d['eg']

def dump(path, obj):
    path = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(path)

# ---- language of each verse ----
# The Mānas is in Awadhi (awa). Its Sanskrit (sa) passages: every śloka, Atri's stuti
# (Araṇya 4, "namāmi bhakta vatsalaṁ"), Sutīkṣṇa's stuti (Araṇya 11, "śyāma tāmarasa dāma śarīraṁ")
# and the Rudrāṣṭaka (Uttara 108, "namāmīśamīśāna"). The other stutis (e.g. Laṅkā 111, Uttara 14)
# are Sanskritised Awadhi in Awadhi spelling, so they stay awa; awa falls back to sa for tatsama words.
import re
def verse_lang(x):
    if x['y'] == 'shloka' or x['id'].startswith('aranya.4.cha') or re.fullmatch(r'aranya\.11\.cau[2-8]|uttar\.108\.cau[1-8]', x['id']): return 'sa'
    return 'awa'

# ---- the text: verse + number only (transliteration belongs to the text) ----
items = []
for x in IT:
    o = {'id': x['id'], 'p': x['k'], 's': x['s'], 'y': x['y'], 'n': x['n'], 'v': x['v']}
    if x.get('t'): o['t'] = x['t']
    if verse_lang(x) != 'awa': o['l'] = verse_lang(x)
    items.append(o)
ids = [x['id'] for x in IT]
plans = {k: {'n': len(v), 'end': [ids[v[str(n)]] for n in range(1, len(v) + 1)]} for k, v in d['P'].items()}
work = {
    'id': 'manas',
    'lang': 'awa',
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

# ---- word meanings, filed by the language of the verses each word occurs in ----
# A word found in both Sanskrit and Awadhi verses goes into both dictionaries (its sense may differ).
# Words reached only through suffix rules (not written as such in any verse) belong to Awadhi.
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")
seen = {}
for x in items:
    for l in x['v']:
        for t in l.split():
            t = PUNCT.sub('', t)
            if t: seen.setdefault(t, set()).add(x.get('l', 'awa'))
added = {}
for lang in ('sa', 'awa'):
    rel = 'glossary/' + lang + '.json'; gp = os.path.join(OUT, rel)
    G = json.load(open(gp)) if os.path.exists(gp) else {}
    new = {k: v for k, v in d['gloss'].items() if k not in G and lang in seen.get(k, {'awa'})}
    G.update(new); added[lang] = len(new); jsonio.dump_glossary(gp, G); sizes['gloss-' + lang] = os.path.getsize(gp)
print({k: round(v / 1e6, 2) for k, v in sizes.items()}, 'MB; new words', added)
