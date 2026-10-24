"""The Hindu āratīs (one work each) → library/hinduism/aarti/<deity>/<work>/.

  shri-ramchandra-kripalu  Tulasīdāsa's stuti "श्रीरामचन्द्र कृपालु", with the Mānas's chhand and sorathā Bāla 236 that close it
  ramlala-aarti  "आरती कीजे श्रीरामलला की"
  ramchandra-aarti  "आरती कीजै रामचन्द्र जी की"
                 (the three Rāma āratīs come from one page but are separate works: owner, 2026-10-24)
  hanuman-aarti  "आरती कीजै हनुमान लला की": TAKEN from the Sundarakāṇḍa work, never edited here (same ids, lines,
                 meanings and recordings' timings), so a correction there reaches this work the next time this script runs
  jagdish-aarti  "ॐ जय जगदीश हरे"
  shiv-aarti     "ॐ जय शिव ओंकारा"
  ganga-aarti    "ॐ जय गंगे माता"

Each folder holds text.txt (the verse text; format in shri-ramchandra-kripalu/text.txt), meanings/hi.json and en.json (our own
meanings, one per verse: the owner gave no meanings for these) and reconciliation.md (the source and every change).
A verse written [manas <id>] is the Mānas's own verse, with its Gita Press meanings (selectable) and our own meanings.

Writes   library/<path>/work.json, meanings/hi-scriptures.json, en-scriptures.json (+ hi-gitapress, en-gitapress for
         the Mānas verses), and glossary.json from <work>/senses.json: the work's own senses of words whose shared
         sense doesn't fit there (`docs/LIBRARY.md` §5)
Merges   glossary/<lang>.json (this folder) into library/glossary/<lang>.json: adds new words, never overwrites.
Checks   every verse has both meanings, the taken verses equal their originals, and every word of every verse has a
         meaning in its language or a fallback. It stops if anything is wrong.
Run it after tools/works/ramcharitmanas/export.py and tools/works/sundarkand/export.py. Does not touch
library/index.json (the shelf is edited by hand). Then run tools/site/build.py.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(HERE, '..', '..')); import jsonio
sys.path.insert(0, os.path.join(HERE, '..', 'sundarkand')); import translit
sys.path.insert(0, os.path.join(HERE, '..', '..', 'meanings')); import versenum

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
MANAS = 'hinduism/granth/tulsidas/ramcharitmanas'
SUNDAR = 'hinduism/granth/tulsidas/sundarkand'

def load(rel): return json.load(open(os.path.join(OUT, rel), encoding='utf-8'))
def dump(rel, obj):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

TYPES = {   # verse types the app doesn't know; cau, cha, do and so are the Mānas's own
    'tek': {'name': {'hi': 'टेक', 'en': 'Refrain (ṭeka)'}, 'short': {'hi': 'टेक', 'en': 'Ref.'}},
    'pad': {'name': {'hi': 'पद', 'en': 'Stanza'}, 'short': {'hi': 'पद', 'en': 'St.'}},
}
WORKS = {
    'shri-ramchandra-kripalu': {
        'path': 'hinduism/aarti/rama/shri-ramchandra-kripalu', 'lang': 'bra',
        'title': {'hi': 'श्रीरामचन्द्र कृपालु', 'en': 'Śrī Rāmacandra Kṛpālu'},
        'by': {'hi': 'गोस्वामी तुलसीदास', 'en': 'Gosvāmī Tulasīdāsa'},
        'from': {'hi': 'विनय-पत्रिका', 'en': 'Vinaya-patrikā'}},
    'ramlala-aarti': {
        'path': 'hinduism/aarti/rama/ramlala-aarti', 'lang': 'awa',
        'title': {'hi': 'आरती कीजे श्रीरामलला की', 'en': 'Āratī Kīje Śrī Rāmalalā Kī'},
        'by': {'hi': 'भगवान श्रीराम', 'en': 'Bhagavān Śrī Rāma'}},
    'ramchandra-aarti': {
        'path': 'hinduism/aarti/rama/ramchandra-aarti', 'lang': 'hi',
        'title': {'hi': 'आरती कीजै रामचन्द्र जी की', 'en': 'Āratī Kījai Rāmacandra Jī Kī'},
        'by': {'hi': 'भगवान श्रीराम', 'en': 'Bhagavān Śrī Rāma'},
        'from': {'hi': 'संत नामदेव', 'en': 'Saint Nāmadeva'}},
    'hanuman-aarti': {
        'path': 'hinduism/aarti/hanuman/hanuman-aarti', 'lang': 'hi', 'take': SUNDAR, 'prefix': 'aarti.',
        'title': {'hi': 'श्रीहनुमानजीकी आरती', 'en': 'Śrī Hanumānjī kī Āratī'},
        'by': {'hi': 'श्रीहनुमानजी', 'en': 'Śrī Hanumān'},
        'from': {'hi': 'आरती कीजै हनुमान लला की', 'en': 'Āratī kījai Hanumāna lalā kī'}},
    'jagdish-aarti': {
        'path': 'hinduism/aarti/vishnu/jagdish-aarti', 'lang': 'hi',
        'title': {'hi': 'ॐ जय जगदीश हरे', 'en': 'Om Jaya Jagadīśa Hare'},
        'by': {'hi': 'भगवान विष्णु (जगदीश)', 'en': 'Bhagavān Viṣṇu (Jagadīśa)'}},
    'shiv-aarti': {
        'path': 'hinduism/aarti/shiva/shiv-aarti', 'lang': 'hi',
        'title': {'hi': 'ॐ जय शिव ओंकारा', 'en': 'Om Jaya Śiva Oṅkārā'},
        'by': {'hi': 'भगवान शिव', 'en': 'Bhagavān Śiva'}},
    'ganga-aarti': {
        'path': 'hinduism/aarti/ganga/ganga-aarti', 'lang': 'hi',
        'title': {'hi': 'श्रीगंगाजीकी आरती', 'en': 'Śrī Gaṅgājī kī Āratī'},
        'by': {'hi': 'माँ गंगा', 'en': 'Mother Gaṅgā'},
        'from': {'hi': 'ॐ जय गंगे माता', 'en': 'Om Jaya Gaṅge Mātā'}},
}
TITLES = {'hi': {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'},
          'en': {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'}}
M = load(MANAS + '/work.json'); MID = {x['id']: x for x in M['items']}

def read_text(wid, lang):
    """text.txt → (sections, items, pulled Mānas ids)"""
    sections, items, pulled, sec = [], [], [], None
    for raw in open(os.path.join(HERE, wid, 'text.txt'), encoding='utf-8'):
        line = raw.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('=='):
            sid, l, thi, ten = [f.strip() for f in line[2:].split('|')]
            sec = {'id': sid, 'lang': l, 'hi': thi, 'en': ten, 'first': None}; sections.append(sec); continue
        m = re.fullmatch(r'\[manas (\S+)\]', line)
        if m:
            it = dict(MID[m.group(1)], p=0, s=sec['id'])
            if it.get('l', M['lang']) != lang: it['l'] = it.get('l', M['lang'])
            elif 'l' in it: del it['l']
            items.append(it); pulled.append(it['id']); sec['first'] = sec['first'] or it['id']; continue
        m = re.fullmatch(r'\[(\w+)(?: (\d+))?\]', line)
        if m:
            y, n = m.group(1), m.group(2) or ''
            it = {'id': f"{sec['id']}.{y}{n}", 'p': 0, 's': sec['id'], 'y': y, 'n': n, 'v': []}
            if sec['lang'] != lang: it['l'] = sec['lang']
            items.append(it); sec['first'] = sec['first'] or it['id']; continue
        items[-1]['v'].append(line)
    for it in items:
        if it['id'] not in pulled: it['t'] = translit.verse(it['v'], it['n'] if it['y'] == 'cau' else None)
    return sections, items, pulled

PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")   # the app's own rule (tools/site/app.js)
words = {}   # language → words used, over all the works
covered = []   # (work, its words by language, its own senses)
for wid, cfg in WORKS.items():
    WP, lang = cfg['path'], cfg['lang']
    if 'take' in cfg:   # taken unchanged from another work
        S = load(cfg['take'] + '/work.json')
        items = [dict(x, p=0) for x in S['items'] if x['id'].startswith(cfg['prefix'])]
        for it in items:
            if it.get('l') == lang: del it['l']
        sections = [{'id': items[0]['s'], 'hi': cfg['title']['hi'], 'en': cfg['title']['en'], 'first': items[0]['id']}]
        pulled = []; own = []
        types = {k: v for k, v in S['types'].items() if k in {x['y'] for x in items}}
    else:
        sections, items, pulled = read_text(wid, lang)
        own = [x['id'] for x in items if x['id'] not in pulled]
        types = {k: v for k, v in TYPES.items() if k in {x['y'] for x in items}}
    ids = [x['id'] for x in items]
    assert len(set(ids)) == len(ids), f'{wid}: duplicate item ids'
    assert all(x['v'] for x in items), f'{wid}: item without lines'
    assert {x['y'] for x in items} <= set(types) | {'cau', 'cha', 'do', 'so'}, f'{wid}: unknown verse type'
    work = {'id': wid, 'lang': lang, 'title': cfg['title'], 'by': cfg['by']}
    if cfg.get('from'): work['from'] = cfg['from']   # under the title on the work's page (by · from)
    work.update({
        'parts': {'name': {'hi': 'आरती', 'en': 'Āratī'}, 'list': [cfg['title']]},
        'types': types, 'items': items,
        'topics': [{'id': s['first'], 'hi': s['hi'], 'en': s['en']} for s in sections]})
    old = os.path.join(OUT, WP, 'work.json')   # keep the sources list that build.py registered
    if os.path.exists(old): work['sources'] = json.load(open(old)).get('sources', {})
    dump(WP + '/work.json', work)

    # ---- meanings ----
    if 'take' in cfg:   # the other work's own, for these verses
        for lg in ('hi', 'en'):
            S = load(f"{cfg['take']}/meanings/{lg}-scriptures.json")
            m = {i: S['m'][i] for i in ids}
            dump(f'{WP}/meanings/{lg}-scriptures.json', {'id': lg + '-scriptures', 'lang': lg, 'order': 1, 'title': TITLES[lg], 'm': m})
    else:
        BYID = {x['id']: x for x in items}
        for lg in ('hi', 'en'):
            D = json.load(open(os.path.join(HERE, wid, 'meanings', lg + '.json'), encoding='utf-8'))
            miss = [i for i in own if not D.get(i)]; extra = [k for k in D if k not in own]
            assert not miss and not extra, f'{wid} {lg} meanings: missing {miss[:5]}, unknown {extra[:5]}'
            m = {i: [versenum.with_number(D[i], BYID[i], lg)] for i in own}
            if pulled:   # the Mānas verses: the Mānas's own meanings, ours where written (the default) and Gita Press
                # (selectable; the app shows it where ours is not written yet)
                MS = load(f'{MANAS}/meanings/{lg}-scriptures.json'); m.update({i: MS['m'][i] for i in pulled if i in MS['m']})
                G = load(f'{MANAS}/meanings/{lg}-gitapress.json')
                dump(f'{WP}/meanings/{lg}-gitapress.json', {**{k: v for k, v in G.items() if k != 'm'}, 'order': 2, 'm': {i: G['m'][i] for i in pulled if i in G['m']}})
            m = {i: m[i] for i in ids if i in m}
            dump(f'{WP}/meanings/{lg}-scriptures.json', {'id': lg + '-scriptures', 'lang': lg, 'order': 1, 'title': TITLES[lg], 'm': m})
    if 'take' in cfg:   # the other work's recordings, for these verses only (their timings are made there)
        ad = os.path.join(OUT, cfg['take'], 'audio')
        for f in sorted(os.listdir(ad)) if os.path.isdir(ad) else []:
            A = json.load(open(os.path.join(ad, f), encoding='utf-8'))
            at = {i: t for i, t in A['at'].items() if i in ids}
            if not at: continue
            used = sorted({t[0] for t in at.values()})
            tracks = [dict(A['tracks'][k], first=min((i for i in at if at[i][0] == k), key=ids.index), last=max((i for i in at if at[i][0] == k), key=ids.index)) for k in used]
            at = {i: [used.index(t[0])] + t[1:] for i, t in at.items()}
            out = {k: v for k, v in A.items() if k not in ('tracks', 'at', 'check', 'guess', 'moved', 'raw')}
            out.update(tracks=tracks, at=at)
            for k in ('check', 'guess'):
                if [i for i in A.get(k, []) if i in ids]: out[k] = [i for i in A[k] if i in ids]
            dump(f'{WP}/audio/{f}', out)
    # the taken verses must equal their originals
    W2 = load(WP + '/work.json'); B = {x['id']: x for x in W2['items']}
    for i in pulled: assert {k: v for k, v in MID[i].items() if k not in ('p', 's', 'l')} == {k: v for k, v in B[i].items() if k not in ('p', 's', 'l')}, i
    mine = {}
    for x in items:
        for l in x['v']:
            for t in l.split():
                t = PUNCT.sub('', t)
                if t: mine.setdefault(x.get('l', lang), set()).add(t)
    for lg, ws in mine.items(): words.setdefault(lg, set()).update(ws)
    # the work's own senses of words whose shared sense doesn't fit here (<work>/senses.json → glossary.json)
    sp = os.path.join(HERE, wid, 'senses.json')
    senses = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else {}
    for lg, D in senses.items():
        bad = [k for k, v in D.items() if k not in mine.get(lg, ()) or not (v.get('hi') and v.get('en'))]
        assert not bad, f'{wid}: senses not in any verse of {lg}, or without hi and en: {bad}'
    gl = os.path.join(OUT, WP, 'glossary.json')
    if senses: dump(WP + '/glossary.json', senses)
    elif os.path.exists(gl): os.remove(gl)
    covered.append((wid, mine, senses))
    print(f"{wid}: {len(items)} verses in {len(sections)} section(s){f', {len(pulled)} from the Mānas' if pulled else ''}")

# ---- word meanings, filed by the language of the verses each word occurs in ----
LANGS = load('glossary/languages.json')
added = {}
for f in sorted(os.listdir(os.path.join(HERE, 'glossary'))):
    lg = f[:-5]; gp = os.path.join(OUT, 'glossary', f)
    G = json.load(open(gp, encoding='utf-8')) if os.path.exists(gp) else {}
    mine = json.load(open(os.path.join(HERE, 'glossary', f), encoding='utf-8'))
    for k, v in mine.items(): assert v.get('hi') and v.get('en'), f'{lg}:{k} needs hi and en'
    unused = [k for k in mine if k not in words.get(lg, ())]; assert not unused, f'{lg}: words not in any verse {unused}'
    new = {k: v for k, v in mine.items() if k not in G}
    G.update(new); added[lg] = len(new); jsonio.dump_glossary(gp, G)
missing = []
for wid, mine, senses in covered:
    for lg, ws in mine.items():
        chain = [lg] + LANGS[lg].get('fallback', [])
        D = [senses.get(c, {}) for c in chain] + [load(f'glossary/{c}.json') for c in chain if os.path.exists(os.path.join(OUT, 'glossary', c + '.json'))]
        missing += [f'{wid} {lg}:{w}' for w in sorted(ws) if not any(w in d for d in D)]
assert not missing, f'{len(missing)} words have no meaning: {missing}'
print(f'new words {added}')
