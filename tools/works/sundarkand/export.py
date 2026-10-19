"""Sundarakāṇḍa (standalone work) → library/hinduism/granth/tulsidas/sundarkand/.

Part 0, the maṅgalācaraṇa, is what Pt. Ashwin Kumar Pathak's recording sings before the text: "ॐ श्री परमात्मने नमः",
the two Gaṇeśa ślokas (वक्रतुण्ड…, विघ्नेश्वराय…), "ॐ श्री परमात्मने नमः" again, and the Mānas's sorathā "प्रनवउँ पवनकुमार"
(Bāla-kāṇḍa 17). It comes from text.txt; the sorathā is pulled from the Mānas (`[manas bal.17.so17]`), never copied.
Part 1 is the lead-in recited before the Sundarakāṇḍa: the close of the Kiṣkindhā-kāṇḍa from dohā 29 (Jāmbavān reminds
Hanumān of his strength), as Pt. Ashwin Kumar Pathak recites it. Like part 2 it is taken from the Mānas unchanged.
Part 2, the Sundarakāṇḍa, is GENERATED from the Rāmacaritamānasa and never edited here: every item of the Mānas's
Sundara-kāṇḍa part (same ids, sections `s` = dohā numbers, types, numbers, verse lines, transliteration and
language `l`), its topics, and its Gita Press Hindi and English meanings (same source ids and titles). So a correction
made to the Mānas reaches this work the next time this script runs. Run it after tools/works/ramcharitmanas/export.py.

Parts 3 and 4, the Śrī Hanumān Chālīsā and the āratī "आरती कीजै हनुमान लला की", come from text.txt (settled in
reconciliation.md). Their meanings, and those of the maṅgalācaraṇa's own lines, are our own (meanings/hi.json, en.json → sources hi-scriptures, en-scriptures,
order 2); the app shows them to a reader who has chosen Gita Press, because Gita Press does not cover these verses.

Writes   work.json, meanings/hi-gitapress.json, en-gitapress.json, hi-scriptures.json, en-scriptures.json
Merges   glossary/awa.json, hi.json and sa.json (this folder) into library/glossary/<lang>.json: adds new words, never overwrites.
Checks   the Sundarakāṇḍa items equal the Mānas ones, every new verse has both meanings, and every word of every verse
         has a meaning in its language or a fallback. It stops if anything is wrong.
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio). Then run tools/site/build.py.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(HERE, '..', '..')); import jsonio
sys.path.insert(0, HERE); import translit

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
MANAS = 'hinduism/granth/tulsidas/ramcharitmanas'
WP = 'hinduism/granth/tulsidas/sundarkand'
LANG = 'awa'

def load(rel): return json.load(open(os.path.join(OUT, rel), encoding='utf-8'))
def dump(rel, obj):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# ---- parts 1 and 2: the close of the Kiṣkindhā-kāṇḍa and the Sundarakāṇḍa, taken from the Mānas ----
M = load(MANAS + '/work.json')
assert M['lang'] == LANG
K = next(k for k, p in enumerate(M['parts']['list']) if p['en'].startswith('Sundara'))
sk = [x for x in M['items'] if x['p'] == K]
assert sk and sk[0]['id'].startswith('sundar.') and len(sk) == sum(1 for x in M['items'] if x['id'].startswith('sundar.'))
LEAD_FROM = 'kishkindha.29.do29'                       # part 1: the end of the Kiṣkindhā-kāṇḍa, from this verse
mids = [x['id'] for x in M['items']]; a = mids.index(LEAD_FROM); b = mids.index(sk[0]['id'])
lead = M['items'][a:b]
assert lead and all(x['p'] == M['items'][a]['p'] for x in lead) and M['items'][a]['p'] == K - 1, 'the lead-in must be the end of the Kiṣkindhā-kāṇḍa'
items = [dict(x, p=1) for x in lead] + [dict(x, p=2) for x in sk]   # identical apart from the part index
sk_ids = {x['id'] for x in lead + sk}
topics = [t for t in M['topics'] if t['id'] in sk_ids]
if lead[0]['id'] not in {t['id'] for t in topics}:     # the lead-in starts inside a Mānas topic: it opens with that topic's name
    cover = [t for t in M['topics'] if mids.index(t['id']) <= a][-1]
    topics.insert(0, dict(cover, id=lead[0]['id']))

# ---- parts 0, 3 and 4: text.txt ----
PARTS = {'mangal': (0, {'hi': 'प्रारम्भिक वन्दना', 'en': 'Opening prayers'}),
         'chalisa': (3, {'hi': 'श्रीहनुमानचालीसा', 'en': 'Śrī Hanumān Chālīsā'}),
         'aarti': (4, {'hi': 'आरती', 'en': 'Āratī'})}
TYPES = {   # verse types the app doesn't know; cau and do are the Mānas's own
    'tek': {'name': {'hi': 'टेक', 'en': 'Refrain (ṭeka)'}, 'short': {'hi': 'टेक', 'en': 'Ref.'}},
    'pad': {'name': {'hi': 'पद', 'en': 'Stanza'}, 'short': {'hi': 'पद', 'en': 'St.'}},
    'mantra': {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},   # as in the Rāma Rakṣā
}
MID = {x['id']: x for x in M['items']}
pulled = []   # Mānas items placed in a text.txt section with [manas <id>]: the same item, only its part and section change
new, sec, count, new_topic = [], None, {}, None
for raw in open(os.path.join(HERE, 'text.txt'), encoding='utf-8'):
    line = raw.strip()
    if not line or line.startswith('#'): continue
    if line.startswith('=='):
        part, sid, lang, thi, ten = [f.strip() for f in line[2:].split('|')]
        sec = {'part': part, 'id': sid, 'lang': lang}
        new_topic = {'hi': thi, 'en': ten}; continue
    m = re.fullmatch(r'\[manas (\S+)\]', line)
    if m:
        it = dict(MID[m.group(1)], p=PARTS[sec['part']][0], s=sec['id']); new.append(it); pulled.append(it['id'])
        if new_topic: topics.append(dict(id=it['id'], **new_topic)); new_topic = None
        continue
    m = re.fullmatch(r'\[(\w+)(?: (\d+))?\]', line)
    if m:
        y, n = m.group(1), m.group(2) or ''
        key = (sec['part'], y); count[key] = count.get(key, 0) + 1
        iid = f"{sec['part']}.{y}{n or (count[key] if y != 'tek' else '')}"
        it = {'id': iid, 'p': PARTS[sec['part']][0], 's': sec['id'], 'y': y, 'n': n, 'v': []}
        if sec['lang'] != LANG: it['l'] = sec['lang']
        new.append(it)
        if new_topic: topics.append(dict(id=iid, **new_topic)); new_topic = None
        continue
    new[-1]['v'].append(line)
for it in new:
    if it['id'] not in pulled: it['t'] = translit.verse(it['v'], it['n'] if it['y'] == 'cau' else None)
items = [x for x in new if x['p'] == 0] + items + [x for x in new if x['p'] > 2]
assert [x['p'] for x in items] == sorted(x['p'] for x in items), 'items out of part order'
ids = [x['id'] for x in items]; new_ids = [x['id'] for x in new if x['id'] not in pulled]   # new_ids: the verses with our own meanings
assert len(set(ids)) == len(ids), 'duplicate item ids'
assert all(x['v'] for x in items), 'item without lines'
assert [x['n'] for x in new if x['y'] == 'cau'] == [str(i) for i in range(1, 41)], 'the Chālīsā needs caupāīs 1–40'
assert {x['y'] for x in new} <= set(TYPES) | {'cau', 'do', 'so', 'shloka'}, 'unknown verse type'

work = {
    'id': 'sundarkand', 'lang': LANG,
    'title': {'hi': 'सुन्दरकाण्ड', 'en': 'Sundarakāṇḍa'},
    'by': M['by'],
    'edition': {'hi': 'श्रीरामचरितमानस, गीताप्रेस', 'en': 'Śrī Rāmacaritamānasa, Gita Press'},
    'colophon': {'hi': '।। सियावर रामचन्द्रकी जय ।। पवनसुत हनुमानकी जय ।।', 'en': '।। Glory to Śrī Rāma ।। Glory to Hanumān, son of the Wind ।।'},
    'parts': {'name': {'hi': 'भाग', 'en': 'Part'},
              'list': [PARTS['mangal'][1], {'hi': 'किष्किन्धाकाण्ड (अन्तिम अंश)', 'en': 'Kiṣkindhā-kāṇḍa (closing verses)'}, {'hi': 'सुन्दरकाण्ड', 'en': 'Sundarakāṇḍa'}] + [v[1] for v in sorted(PARTS.values(), key=lambda v: v[0]) if v[0] > 2]},
    'types': TYPES,
    'items': items,
    'topics': topics,
    # the maṅgalācaraṇa (part 0) was put before the text on 2026-10-19, after readers had saved their places as item
    # positions: the app moves a place saved without an item id (only those older ones) forward by this many items
    'prepended': sum(1 for x in new if x['p'] == 0),
}
old = os.path.join(OUT, WP, 'work.json')   # keep the sources list that build.py registered
if os.path.exists(old): work['sources'] = json.load(open(old)).get('sources', {})
dump(WP + '/work.json', work)

# ---- check: the Sundarakāṇḍa is exactly the Mānas's ----
W2 = load(WP + '/work.json'); B = {x['id']: x for x in W2['items']}
for a_ in lead + sk:
    assert {k: v for k, v in a_.items() if k != 'p'} == {k: v for k, v in B[a_['id']].items() if k != 'p'}, a_['id']
for i in pulled:   # a Mānas verse in the maṅgalācaraṇa: the Mānas's own, apart from its part and section
    assert {k: v for k, v in MID[i].items() if k not in ('p', 's')} == {k: v for k, v in B[i].items() if k not in ('p', 's')}, i

# ---- meanings: Gita Press (the Mānas's, Sundarakāṇḍa only) ----
for sid in ('hi-gitapress', 'en-gitapress'):
    S = load(f'{MANAS}/meanings/{sid}.json')
    m = {x['id']: S['m'][x['id']] for x in items if (x['id'] in sk_ids or x['id'] in pulled) and x['id'] in S['m']}
    dump(f'{WP}/meanings/{sid}.json', {**{k: v for k, v in S.items() if k != 'm'}, 'm': m})
    print(f"{sid}: {sum(1 for x in sk if x['id'] in S['m'])} of {len(sk)} Sundarakāṇḍa verses")

# ---- meanings: our own, for the maṅgalācaraṇa's own lines, the Chālīsā and the āratī ----
TITLES = {'hi': {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'},
          'en': {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'}}
for lg in ('hi', 'en'):
    D = json.load(open(os.path.join(HERE, 'meanings', lg + '.json'), encoding='utf-8'))
    miss = [i for i in new_ids if not D.get(i)]; extra = [k for k in D if k not in new_ids]
    assert not miss and not extra, f'{lg} meanings: missing {miss[:5]}, unknown {extra[:5]}'
    dump(f'{WP}/meanings/{lg}-scriptures.json', {'id': lg + '-scriptures', 'lang': lg, 'order': 2, 'title': TITLES[lg], 'm': {i: [D[i]] for i in new_ids}})

# ---- word meanings, filed by the language of the verses each word occurs in ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")   # the app's own rule (tools/site/app.js)
LANGS = load('glossary/languages.json')
words = {}
for x in items:
    for l in x['v']:
        for t in l.split():
            t = PUNCT.sub('', t)
            if t: words.setdefault(x.get('l', LANG), set()).add(t)
added = {}
for lg in ('awa', 'hi', 'sa'):
    gp = os.path.join(OUT, 'glossary', lg + '.json'); G = json.load(open(gp, encoding='utf-8'))
    mine = json.load(open(os.path.join(HERE, 'glossary', lg + '.json'), encoding='utf-8'))
    for k, v in mine.items(): assert v.get('hi') and v.get('en'), f'{lg}:{k} needs hi and en'
    unused = [k for k in mine if k not in words.get(lg, ())]; assert not unused, f'{lg}: words not in any verse {unused}'
    new_words = {k: v for k, v in mine.items() if k not in G}
    G.update(new_words); added[lg] = len(new_words); jsonio.dump_glossary(gp, G)
missing = []
for lg, ws in words.items():
    chain = [lg] + LANGS[lg].get('fallback', [])
    D = [load(f'glossary/{c}.json') for c in chain]
    missing += [f'{lg}:{w}' for w in sorted(ws) if not any(w in d for d in D)]
assert not missing, f'{len(missing)} words have no meaning: {missing[:20]}'
print(f'{len(items)} verses ({len(sk)} Sundarakāṇḍa and {len(lead) + len(pulled)} more from the Mānas, {len(new_ids)} maṅgalācaraṇa + Chālīsā + āratī), {len(topics)} topics; new words {added}')
