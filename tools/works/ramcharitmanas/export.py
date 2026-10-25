"""Śrī Rāmacaritamānasa: book data (book/app_data.json) → library/tulsidas/ramcharitmanas/.

Writes   work.json                  the text (verse + number), kāṇḍas, topics, plans, vidhi
         meanings/hi-gitapress.json Hindi meaning source (Gita Press bhāvārtha)
         meanings/en-gitapress.json English meaning source (Gita Press translation)
         meanings/hi-scriptures.json, en-scriptures.json  our own meanings (meanings/hi.json, en.json;
                                    tools/meanings/style.md), with the verse numbers added; stops on any overlap
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
# ---- one caupāī per item (owner, 2026-10-20) ----
# In 16 places Gita Press prints two or three caupāīs as one (e.g. ।।३-५।।) because its translation renders them jointly.
# Here each becomes its own item — bal.6.cau3-5 → bal.6.cau3, cau4, cau5 — split where the transliteration numbers each
# caupāī. The joint Gita Press meaning goes under the last of the group (where Gita Press prints its number), and the
# earlier ones point to it. work.json "renamed" maps each old id to its first part, so readers' bookmarks, notes and
# places follow (tools/site/app.js), and tools/audio/make_timings.py reads old ids in its caches the same way.
JOINT = {}   # old id → [new ids]
def split_joint(o):
    a, b = map(int, o['n'].split('-'))
    groups, st = [], 0
    for k, t in enumerate(o['t']):
        m = re.search(r'॥(\d+)॥\s*$', t)
        if m: groups.append((m.group(1), st, k + 1)); st = k + 1
    assert [int(g[0]) for g in groups] == list(range(a, b + 1)) and st == len(o['v']), f"cannot split {o['id']}"
    base = o['id'].rsplit('.cau', 1)[0]
    return [dict(o, id=f'{base}.cau{n}', n=n, v=o['v'][s0:s1], t=o['t'][s0:s1]) for n, s0, s1 in groups]
items = []
for x in IT:
    o = {'id': x['id'], 'p': x['k'], 's': x['s'], 'y': x['y'], 'n': x['n'], 'v': x['v']}
    if x.get('t'): o['t'] = x['t']
    if verse_lang(x) != 'awa': o['l'] = verse_lang(x)
    if o['y'] == 'cau' and re.fullmatch(r'\d+-\d+', o['n']):
        parts = split_joint(o); JOINT[o['id']] = [q['id'] for q in parts]; items += parts
    else: items.append(o)
assert len({x['id'] for x in items}) == len(items), 'duplicate ids after splitting'
FIRST = {k: v[0] for k, v in JOINT.items()}; LAST = {k: v[-1] for k, v in JOINT.items()}
ids = [x['id'] for x in IT]
plans = {k: {'n': len(v), 'end': [LAST.get(ids[v[str(n)]], ids[v[str(n)]]) for n in range(1, len(v) + 1)]} for k, v in d['P'].items()}   # a day ends after the whole group
work = {
    'id': 'manas',
    'lang': 'awa',
    'title': {'hi': 'श्रीरामचरितमानस', 'en': 'Śrī Rāmacaritamānasa'},
    'by': {'hi': 'गोस्वामी तुलसीदास', 'en': 'Gosvāmī Tulasīdāsa'},
    'edition': {'hi': 'गीताप्रेस, गोरखपुर', 'en': 'Gita Press, Gorakhpur'},
    'colophon': {'hi': '।। इति श्रीरामचरितमानस समाप्त ।। सियावर रामचन्द्रकी जय', 'en': '।। इति श्रीरामचरितमानस समाप्त ।। Glory to Śrī Rāma'},
    'parts': {'name': {'hi': 'काण्ड', 'en': 'Kāṇḍa'}, 'list': d['kands']},
    'plans': [
        {'id': 'M', 'name': {'hi': 'मासपारायण', 'en': '30-day'}, 'long': {'hi': 'मासपारायण (३० दिन)', 'en': 'Māsa-pārāyaṇa (30 days)'}, 'unit': {'hi': 'विश्राम', 'en': 'Vishram'}, 'before': ['vidhi'], 'after': ['aarti', 'visarjan'], **plans['M']},
        {'id': 'N', 'name': {'hi': 'नवाह्नपारायण', 'en': '9-day'}, 'long': {'hi': 'नवाह्नपारायण (९ दिन)', 'en': 'Navāhna-pārāyaṇa (9 days)'}, 'unit': {'hi': 'विश्राम', 'en': 'Vishram'}, 'before': ['vidhi'], 'after': ['aarti', 'visarjan'], **plans['N']},
    ],
    'items': items,
    'topics': [{'id': FIRST.get(ids[t['i']], ids[t['i']]), 'hi': t['hi'], 'en': t.get('en') or t['hi']} for t in d['topics']],
    'renamed': FIRST,
    # a reader's place saved before 2026-10-19 is an item position, without its id: [old position, items added there]
    'split': [[k, len(JOINT[x['id']]) - 1] for k, x in enumerate(IT) if x['id'] in JOINT],
    'vidhi': {**d['vidhi'], 'visarjan': {k: v for k, v in json.load(open(os.path.join(HERE, 'visarjan.json'))).items() if k != 'source'}},   # kathā-visarjana: see visarjan.md
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
# a joint meaning (the split caupāīs above): under the last part; the earlier parts say where it is
def spread(m, lg):
    for old, new in JOINT.items():
        if old not in m: continue
        e = m.pop(old); last = items_by[new[-1]]['n']
        for q in new[:-1]: m[q] = ['(इस चौपाईका अर्थ नीचे, चौपाई ' + last.translate(DEVA) + ' के साथ दिया गया है।)' if lg == 'hi' else f'(The meaning of this caupāī is given below, with caupāī {last}.)']
        m[new[-1]] = e
    return {x['id']: m[x['id']] for x in items if x['id'] in m}   # in text order
DEVA = str.maketrans('0123456789', '०१२३४५६७८९'); items_by = {x['id']: x for x in items}
hi = spread(hi, 'hi')
sizes['hi'] = dump(WP + '/meanings/hi-gitapress.json', {'id': 'hi-gitapress', 'lang': 'hi', 'order': 1, 'title': {'hi': 'गीताप्रेस — भावार्थ (हनुमानप्रसाद पोद्दार)', 'en': 'Gita Press — Hindi bhāvārtha (Hanumānprasād Poddār)'}, 'm': hi})

# ---- English meaning source (one entry per verse; footnotes attached) ----
en = {}
for x in IT:
    g = EG.get(str(x['g'])) if x.get('g') is not None else None
    if not g: continue
    e = [g['x']]
    if g.get('f'): e.append(g['f'])
    en[x['id']] = e
en = spread(en, 'en')
sizes['en'] = dump(WP + '/meanings/en-gitapress.json', {'id': 'en-gitapress', 'lang': 'en', 'order': 1, 'title': {'hi': 'गीताप्रेस — अंग्रेज़ी अनुवाद', 'en': 'Gita Press — English translation'}, 'm': en})

# ---- our own meaning sources (meanings/hi.json, en.json; tools/meanings/style.md) ----
# Written from the verse for this library, to replace the copyrighted ones (docs/handoff/2026-10-19-own-meanings.md).
# They cover the verses written so far; a reader who chooses them sees Gita Press's for the rest. Every verse has both
# languages; the verse number is added here from the verse (tools/meanings/versenum.py); and no meaning may share a run
# of 10+ words with Gita Press's (tools/meanings/overlap.py), or the export stops; runs of 6–9 are listed to be read.
sys.path.insert(0, os.path.join(HERE, '..', '..', 'meanings')); import versenum as vnum, overlap
OWN = {lg: json.load(open(os.path.join(HERE, 'meanings', lg + '.json'), encoding='utf-8')) for lg in ('hi', 'en')}
BYID = {x['id']: x for x in items}
assert set(OWN['hi']) == set(OWN['en']), f"hi and en differ: {sorted(set(OWN['hi']) ^ set(OWN['en']))[:10]}"
assert all(k in BYID for k in OWN['hi']), f"unknown ids: {[k for k in OWN['hi'] if k not in BYID][:10]}"
assert all(vnum.joined(v).strip() for D in OWN.values() for v in D.values()), 'empty meaning'
for lg, G in (('hi', hi), ('en', en)):
    res = overlap.check({k: vnum.joined(v) for k, v in OWN[lg].items()}, {k: v[0] for k, v in G.items()})
    bad = [r for r in res if len(r[1]) >= 10]
    assert not bad, f'{lg}: {len(bad)} meanings share 10+ words with Gita Press, e.g. {bad[0][0]}: {" ".join(bad[0][1])}'
    note = [r for r in res if len(r[1]) >= 6]
    if note: print(f'{lg}: {len(note)} meanings share 6–9 words with Gita Press (read them: tools/meanings/overlap.py --report)')
TITLES = {'hi': {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'},
          'en': {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'}}
order_ids = [x['id'] for x in items]
for lg in ('hi', 'en'):
    TP = {i: vnum.text_and_pieces(OWN[lg][i], BYID[i], lg) for i in order_ids if i in OWN[lg]}   # a list = line by line
    m = {i: [t[0]] for i, t in TP.items()}; pcs = {i: t[1] for i, t in TP.items() if t[1]}
    sizes[lg + '-ours'] = dump(f'{WP}/meanings/{lg}-scriptures.json', {'id': lg + '-scriptures', 'lang': lg, 'order': 2, 'title': TITLES[lg], 'm': m, **({'p': pcs} if pcs else {})})
print(f"our own meanings: {len(OWN['hi'])} verses in Hindi and English")
print(f"{len(JOINT)} joint caupāīs split into {sum(len(v) for v in JOINT.values())} items")

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
