"""Śrī Sāī Bābā (Shirdi) — Dhūpa āratī: text.txt + meanings/ + glossary/ → library/hinduism/aarti/shirdi-sai/dhoop-aarti/.

Writes   work.json                     the text (verse + number + language), sections as topics, verse types
         meanings/hi-scriptures.json   Hindi bhāvārtha (written for this library; the default)
         meanings/en-scriptures.json   English meaning (written for this library; every verse; the default)
         meanings/en-shirdisaibabakripa.json   English meaning copied from the shirdisaibabakripa.org printout
                                       (second choice; it has no meaning for prarthana.jay2 and jay3)
Merges   glossary/<lang>.json (mr, sa, hi) into library/glossary/<lang>.json: adds new words, never overwrites.
Checks   every verse has a meaning in both written sources, and every word of every verse has a meaning in its
         language or a fallback (Marathi and Hindi fall back to Sanskrit). It stops if anything is missing.
Does not touch library/index.json (the shelf is edited by hand). Then run tools/site/build.py.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); import jsonio

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/aarti/shirdi-sai/dhoop-aarti'
WORK = 'shirdi-sai-dhoop-aarti'
LANG = 'mr'

# ---- the text ----
sections, items = [], []
sec = None
for raw in open(os.path.join(HERE, 'text.txt'), encoding='utf-8'):
    line = raw.strip()
    if not line or line.startswith('#'): continue
    if line.startswith('=='):
        f = [x.strip() for x in line[2:].split('|')]
        sec = {'id': f[0], 'lang': f[1], 'hi': f[2], 'en': f[3], 'by': {'hi': f[4], 'en': f[5]} if len(f) > 5 and f[4] else None}
        sections.append(sec); continue
    m = re.fullmatch(r'\[(\w+)(?: (\d+))?(?: ([a-z]{2,3}))?\]', line)
    if m:
        y, n, l = m.group(1), m.group(2) or '', m.group(3) or sec['lang']
        it = {'id': f"{sec['id']}.{y}{n}", 'p': 0, 's': sec['id'], 'y': y, 'n': n, 'v': []}
        if l != LANG: it['l'] = l
        items.append(it); continue
    items[-1]['v'].append(line)
ids = [x['id'] for x in items]
assert len(set(ids)) == len(ids), 'duplicate item ids'
assert all(x['v'] for x in items), 'item without lines'

TYPES = {
    'dhru':   {'name': {'hi': 'ध्रुवपद', 'en': 'Dhruvapada'}, 'short': {'hi': 'ध्रु॰', 'en': 'Dhru.'}},
    'pad':    {'name': {'hi': 'पद', 'en': 'Pada'}, 'short': {'hi': 'पद', 'en': 'Pada'}},
    'abhang': {'name': {'hi': 'अभंग', 'en': 'Abhaṅga'}, 'short': {'hi': 'अभं॰', 'en': 'Abh.'}},
    'shloka': {'name': {'hi': 'श्लोक', 'en': 'Śloka'}, 'short': {'hi': 'श्लो॰', 'en': 'Śl.'}},
    'mantra': {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},
    'jay':    {'name': {'hi': 'जयघोष', 'en': 'Jayaghoṣa'}, 'short': {'hi': 'जय', 'en': 'Jaya'}},
}
assert {x['y'] for x in items} <= set(TYPES), 'unknown verse type'

work = {
    'id': WORK, 'lang': LANG,
    'title': {'hi': 'धूप आरती', 'en': 'Dhūpa Āratī'},
    'by': {'hi': 'श्री साईबाबा, शिरडी', 'en': 'Śrī Sāī Bābā of Shirdi'},
    'edition': {'hi': 'शिरडीकी सायंकालीन आरती', 'en': 'The evening āratī of Shirdi'},
    'from': {'hi': 'शिरडीकी सायंकालीन आरती', 'en': 'The evening āratī of Shirdi'},   # under the title on the work's page (by · from)
    'parts': {'name': {'hi': 'आरती', 'en': 'Āratī'}, 'list': [{'hi': 'धूप आरती', 'en': 'Dhūpa Āratī'}]},
    'types': TYPES,
    'items': items,
    'topics': [{'id': next(x['id'] for x in items if x['s'] == s['id']), 'hi': s['hi'], 'en': s['en']} for s in sections],
}

def dump(rel, obj):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# keep the sources list that build.py registered, so an export alone does not change it
old = os.path.join(OUT, WP, 'work.json')
if os.path.exists(old): work['sources'] = json.load(open(old)).get('sources', {})
dump(WP + '/work.json', work)

# ---- meanings (one per verse, both languages) ----
TITLES = {'hi': {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'},
          'en': {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'}}
for lg in ('hi', 'en'):
    M = json.load(open(os.path.join(HERE, 'meanings', lg + '.json'), encoding='utf-8'))
    miss = [i for i in ids if not M.get(i)]; extra = [k for k in M if k not in ids]
    assert not miss and not extra, f'{lg} meanings: missing {miss[:5]}, unknown {extra[:5]}'
    # our own meanings are the default in both languages (the owner's rule: our own meanings in place of others'
    # copyrighted ones); the printout's English stays selectable in ☰ › More › Sources
    dump(f'{WP}/meanings/{lg}-scriptures.json', {'id': lg + '-scriptures', 'lang': lg, 'order': 1, 'title': TITLES[lg], 'm': {i: [M[i]] for i in ids}})

# ---- meanings copied from the owner's printouts (only the verses they cover) ----
COPIED = {'en-shirdisaibabakripa': {'lang': 'en', 'order': 2,
          'title': {'hi': 'shirdisaibabakripa.org — अंग्रेज़ी अर्थ', 'en': 'shirdisaibabakripa.org — English meaning'}}}
for sid, meta in COPIED.items():
    M = json.load(open(os.path.join(HERE, 'meanings', sid + '.json'), encoding='utf-8'))
    extra = [k for k in M if k not in ids]; assert not extra, f'{sid}: unknown {extra}'
    m = {i: ([M[i]] if isinstance(M[i], str) else M[i]) for i in ids if i in M}
    assert all(v[0] for v in m.values()), f'{sid}: empty meaning'
    dump(f'{WP}/meanings/{sid}.json', {'id': sid, 'lang': meta['lang'], 'order': meta['order'], 'title': meta['title'], 'm': m})
    print(f'{sid}: {len(m)} of {len(ids)} verses; not covered: {[i for i in ids if i not in M]}')

# ---- word meanings, filed by the language of the verses each word occurs in ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")   # the app's own rule (tools/site/app.js)
LANGS = json.load(open(os.path.join(OUT, 'glossary', 'languages.json')))
words = {}
for x in items:
    for l in x['v']:
        for t in l.split():
            t = PUNCT.sub('', t)
            if t: words.setdefault(x.get('l', LANG), set()).add(t)
added = {}
for lg in sorted(words):
    rel = f'glossary/{lg}.json'; gp = os.path.join(OUT, rel)
    G = json.load(open(gp, encoding='utf-8')) if os.path.exists(gp) else {}
    mine = json.load(open(os.path.join(HERE, 'glossary', lg + '.json'), encoding='utf-8'))
    for k, v in mine.items(): assert v.get('hi') and v.get('en'), f'{lg}:{k} needs hi and en'
    new = {k: v for k, v in mine.items() if k not in G}
    G.update(new); added[lg] = len(new); jsonio.dump_glossary(gp, G)
missing = []
for lg, ws in words.items():
    chain = [lg] + LANGS[lg].get('fallback', [])
    D = [json.load(open(os.path.join(OUT, 'glossary', c + '.json'), encoding='utf-8')) for c in chain if os.path.exists(os.path.join(OUT, 'glossary', c + '.json'))]
    missing += [f'{lg}:{w}' for w in sorted(ws) if not any(w in d for d in D)]
assert not missing, f'{len(missing)} words have no meaning: {missing[:20]}'
print(f'{len(items)} verses in {len(sections)} sections; new words {added}')
