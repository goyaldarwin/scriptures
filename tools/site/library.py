"""Register sources and check the library before every build (called by build.py).

For each work on the shelf (library/index.json) this:
  1. lists the meaning sources in <work>/meanings/*.json and the audio sources in <work>/audio/*.json
     and writes them into work.json → "sources" (the website reads that list; it cannot scan folders),
     and marks "glossary": true when the work has its own <work>/glossary.json;
  2. checks that every work has its folder in tools/works with the files every work has (check_folders), and that
     everything refers to things that exist (sources, plans, topics in reading order, verse languages, a meaning for
     every word of every verse (check_words, with the app's own word rule),
     dictionaries in glossary/, fallbacks, each store app's shelves in library/apps.json), and stops the build with
     a clear message if not.
A source's file name must equal its "id". The source with the lowest "order" (then id) is the default.
"""
import glob, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'text')); import standard

class LibraryError(Exception): pass

def _need(ok, msg):
    if not ok: raise LibraryError(msg)

def _bi(x):  # bilingual label
    return isinstance(x, dict) and isinstance(x.get('hi'), str) and isinstance(x.get('en'), str)

def leaves(shelf, trail=()):
    seen = set()
    for n in shelf:
        _need(isinstance(n.get('id'), str) and re.fullmatch(r'[a-z0-9-]+', n['id']), f"shelf: bad id {n.get('id')!r} under {'/'.join(trail) or 'top'} (use lowercase letters, digits, -)")
        _need(n['id'] not in seen, f"shelf: id {n['id']!r} appears twice under {'/'.join(trail) or 'top'}")
        seen.add(n['id']); _need(_bi(n.get('title')), f"shelf: {n['id']} needs title {{hi, en}}")
        if 'work' in n:
            _need('children' not in n, f"shelf: {n['id']} has both work and children")
            want = '/'.join(trail + (n['id'],))
            _need(n.get('path') == want, f"shelf: {n['id']} path must be {want!r} (the shelf ids above it, then its own id), not {n.get('path')!r}")
            _need(len(trail) >= 2, f"shelf: {want} is too shallow; a work sits at least at tradition/genre/work (e.g. hinduism/stotra/…)")
            yield n
        else:
            _need(isinstance(n.get('children'), list) and n['children'], f"shelf: {n['id']} needs children (a shelf) or work (a book)")
            yield from leaves(n['children'], trail + (n['id'],))

def word_rule():
    """The app's own rule for turning a verse token into a dictionary key (tools/site/app.js cleanWord: PUNCT, SVARA,
    NFC), read from app.js itself so the build and the app can never disagree."""
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.js'), encoding='utf-8').read()
    P = re.search(r"const PUNCT = /(\[[^\n]*?\])/g;", js); S = re.search(r"const SVARA = /(\[[^\n]*?\])/g;", js)
    _need(P and S, "library.py: could not read PUNCT / SVARA from tools/site/app.js")
    P, S = re.compile(P.group(1)), re.compile(S.group(1))
    return lambda t: unicodedata.normalize('NFC', S.sub('', P.sub('', t)))

_FOLDED = {}
def _folded(D, lang):
    """The lookup forms (standard.fold) of a dictionary's words."""
    key = (id(D), lang)
    if key not in _FOLDED or _FOLDED[key][0] is not D: _FOLDED[key] = (D, {standard.fold(k) for k in D.get(lang, {})})
    return _FOLDED[key][1]

def check_words(lib, name, w, LANGS, G, clean):
    """Every word of every verse has a meaning in its language or a fallback (the work's own glossary.json first)."""
    wg = os.path.join(lib, name, 'glossary.json'); WG = json.load(open(wg, encoding='utf-8')) if os.path.exists(wg) else {}
    miss = {}
    for x in w['items']:
        lg = x.get('l', w['lang']); chain = [lg] + LANGS[lg].get('fallback', [])
        for line in x['v']:
            for t in line.split():
                k = clean(t)
                if k and not any(k in WG.get(c, {}) or k in G.get(c, {}) or standard.fold(k) in _folded(WG, c) or standard.fold(k) in _folded(G, c) for c in chain): miss.setdefault(lg, set()).add(k)
    _need(not miss, f"{name}: words without a meaning: " + '; '.join(f"{lg}: {' '.join(sorted(ws)[:12])}{' …' if len(ws) > 12 else ''} ({len(ws)})" for lg, ws in miss.items()))

def check_work(lib, leaf, LANGS):
    path = leaf.get('path'); wp = os.path.join(lib, path or '', 'work.json')
    _need(path and os.path.exists(wp), f"shelf: {leaf['id']} → path {path!r} has no work.json")
    w = json.load(open(wp)); name = path
    _need(w.get('id') == leaf['work'], f"{name}: work.json id {w.get('id')!r} ≠ shelf work {leaf['work']!r}")
    items = w['items']; ids = [x['id'] for x in items]; ID = set(ids)
    _need(w.get('lang') in LANGS, f"{name}: work.json lang {w.get('lang')!r} is not in glossary/languages.json")
    bad = sorted({x['l'] for x in items if 'l' in x} - set(LANGS)); _need(not bad, f"{name}: verse languages {bad} are not in glossary/languages.json")
    wg = os.path.join(lib, path, 'glossary.json')
    if os.path.exists(wg):
        for lg, words in json.load(open(wg)).items():
            _need(lg in LANGS, f"{name}/glossary.json: unknown language {lg!r}")
            for k, v in words.items(): _need(isinstance(v, dict) and ('hi' in v or 'en' in v), f"{name}/glossary.json: {lg}:{k} needs hi/en")
    _need(len(ID) == len(ids), f"{name}: item ids are not unique")
    # the writing standard (tools/text/standard.py, PLAYBOOK §3): every verse and transliteration is what it makes
    std = standard.apply(json.loads(json.dumps(items)), w['lang'], standard.yajur(path))
    bad = [a['id'] for a, b in zip(items, std) if a['v'] != b['v'] or a.get('t') != b.get('t')]
    _need(not bad, f"{name}: {len(bad)} items are not written by the standard (export through jsonio.dump_library): {bad[:5]}")
    for f in [wp] + glob.glob(os.path.join(lib, path, 'meanings', '*.json')):
        _need('।।' not in open(f, encoding='utf-8').read(), f"{os.path.relpath(f, lib)}: two daṇḍas ।। where the standard writes ॥")
    for x in items:
        _need(isinstance(x.get('v'), list) and x['v'], f"{name}: item {x['id']} has no verse lines")
        _need(0 <= x['p'] < len(w['parts']['list']), f"{name}: item {x['id']} part {x['p']} out of range")
    for k, t in (w.get('types') or {}).items():
        _need(re.fullmatch(r'[a-z0-9_]+', k) and _bi(t.get('name')) and (_bi(t['short']) if 'short' in t else True), f"{name}: type {k!r} needs name {{hi, en}} (and a bilingual short if given)")
    for t in w.get('topics', []): _need(t['id'] in ID and _bi({'hi': t['hi'], 'en': t['en']}), f"{name}: topic {t} is invalid")
    tp = [ids.index(t['id']) for t in w.get('topics', []) if t['id'] in ID]
    _need(tp == sorted(set(tp)), f"{name}: topics must be in reading order, one per verse at most")
    for p in w.get('plans', []):
        _need(len(p['end']) == p['n'], f"{name}: plan {p['id']} has {len(p['end'])} ends for {p['n']} days")
        pos = [ids.index(e) if e in ID else -1 for e in p['end']]
        _need(min(pos) >= 0 and pos == sorted(pos), f"{name}: plan {p['id']} ends are missing or out of order")
        # before / after: pages read before the first day and after the reading (pūrvāṅga / uttarāṅga)
        pages = ({'vidhi'} if (w.get('vidhi') or {}).get('hi') else set()) | ({'aarti'} if (w.get('vidhi') or {}).get('aarti') else set()) | ({'visarjan'} if (w.get('vidhi') or {}).get('visarjan') else set())
        vs = (w.get('vidhi') or {}).get('visarjan')
        if vs: _need(_bi(vs.get('title')) and _bi(vs.get('when')) and all(len(x.get('v', [])) >= 1 and x.get('hi') and x.get('en') for x in vs.get('verses', [])) and vs.get('verses'), f"{name}: vidhi.visarjan needs title, when and verses [{{v, hi, en}}]")
        if vs:   # every word of the visarjan has its own meaning in context (vidhi.visarjan.g)
            ws = {x for v in vs['verses'] for l in v['v'] for x in re.findall(r'[\u0900-\u0963\u0971-\u097f]+', l)}
            _need(not (ws - set(vs.get('g') or {})), f"{name}: vidhi.visarjan.g lacks {sorted(ws - set(vs.get('g') or {}))[:8]}")
        for k in ('before', 'after'):
            _need(all(x in pages for x in p.get(k, [])), f"{name}: plan {p['id']} {k} {p.get(k)} names a page the work lacks (has {sorted(pages)})")
    # sources
    # meaning languages: those with a "meaning" block in glossary/languages.json (hi, en, pa);
    # hi, en and au are always listed, another only when the work has one
    ML = sorted((k for k, L in LANGS.items() if L.get('meaning')), key=lambda k: (LANGS[k]['meaning'].get('order', 100), k))
    src = {k: [] for k in ML}; src.setdefault('hi', []); src.setdefault('en', []); src['au'] = []
    for f in sorted(glob.glob(os.path.join(lib, path, 'meanings', '*.json'))):
        s = json.load(open(f)); sid = os.path.basename(f)[:-5]; where = f"{name}/meanings/{sid}.json"
        _need(s.get('id') == sid, f"{where}: id {s.get('id')!r} must equal the file name")
        _need(s.get('lang') in ML, f"{where}: lang must be a meaning language of glossary/languages.json ({', '.join(ML)})")
        _need(_bi(s.get('title')), f"{where}: needs title {{hi, en}}")
        bad = [k for k in s['m'] if k not in ID]; _need(not bad, f"{where}: {len(bad)} unknown item ids, e.g. {bad[:3]}")
        for k, e in s['m'].items(): _need(isinstance(e, list) and e and isinstance(e[0], str), f"{where}: {k} must be [text, footnotes?]")
        # line by line: "p" gives a verse's meaning one piece per verse line, shown under its line;
        # "" where a line has no meaning of its own. The joined text in "m" stays (search, copy, a reader's correction).
        NL = {x['id']: len(x['v']) for x in items}
        for k, ps in (s.get('p') or {}).items():
            _need(k in s['m'], f"{where}: p.{k} has no meaning in m")
            _need(isinstance(ps, list) and len(ps) == NL.get(k, -1) and all(isinstance(x, str) for x in ps) and any(x.strip() for x in ps),
                  f"{where}: p.{k} must give one piece (or \"\") per verse line ({NL.get(k, '?')} lines)")
        src[s['lang']].append({'id': sid, 'file': 'meanings/' + sid, 'title': s['title'], 'order': s.get('order', 100)})
    for f in sorted(glob.glob(os.path.join(lib, path, 'audio', '*.json'))):
        s = json.load(open(f)); sid = os.path.basename(f)[:-5]; where = f"{name}/audio/{sid}.json"
        _need(s.get('id') == sid, f"{where}: id {s.get('id')!r} must equal the file name")
        _need(s.get('type') == 'youtube', f"{where}: type must be youtube")
        _need(_bi(s.get('title')), f"{where}: needs title {{hi, en}}")
        T = s['tracks']
        for t in T: _need(re.fullmatch(r'[\w-]{11}', t['yt']) and t['first'] in ID and t['last'] in ID and t['dur'] > 0, f"{where}: bad track {t}")
        for k, v in s['at'].items(): _need(k in ID and len(v) in (2, 3) and 0 <= v[0] < len(T) and 0 <= v[1] <= T[v[0]]['dur'] and (len(v) == 2 or v[1] < v[2] <= T[v[0]]['dur'] + 1), f"{where}: bad timing {k}: {v}")   # [track, start, end?]
        POS = {x: k for k, x in enumerate(ids)}
        out = [k for k, v in s['at'].items() if k in POS and not POS[T[v[0]]['first']] <= POS[k] <= POS[T[v[0]]['last']]]
        _need(not out, f"{where}: verses timed outside their recording's first..last (the player would loop on them): {out[:5]}")
        _need(all(k in s['at'] for k in s.get('check', [])), f"{where}: check lists verses without a time")
        _need(all(k in s['at'] for k in s.get('guess', [])), f"{where}: guess lists verses without a time")
        src['au'].append({'id': sid, 'file': 'audio/' + sid, 'title': s['title'], 'order': s.get('order', 100), **({'draft': True} if s.get('draft') else {})})
    for k in src:
        src[k].sort(key=lambda x: (x['order'], x['id']))
        for x in src[k]: del x['order']
    src = {k: v for k, v in src.items() if v or k in ('hi', 'en', 'au')}
    has_g = os.path.exists(wg)   # the app fetches <work>/glossary.json only when the work says it has one
    if w.get('sources') != src or bool(w.get('glossary')) != has_g:
        w['sources'] = src
        if has_g: w['glossary'] = True
        else: w.pop('glossary', None)
        json.dump(w, open(wp, 'w'), ensure_ascii=False, separators=(',', ':'))
    return w['id'], {k: [x['id'] for x in v] for k, v in src.items()}

WORKS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'works')
FOLDER_FILES = ['work.json', 'text.txt', 'README.md', 'reconciliation.md']   # every work's folder (tools/works/README.md)

def check_folders():
    """Every work folder in tools/works has the files every work has, and its manifest names it. Returns {id: path}."""
    out = {}
    for d in sorted(os.listdir(WORKS)):
        f = os.path.join(WORKS, d)
        if not os.path.isfile(os.path.join(f, 'work.json')): continue
        miss = [x for x in FOLDER_FILES if not os.path.isfile(os.path.join(f, x))]
        _need(not miss, f"tools/works/{d}/: missing {miss}")
        m = json.load(open(os.path.join(f, 'work.json'), encoding='utf-8'))
        _need(m.get('id') == d and m.get('path'), f"tools/works/{d}/work.json: needs id {d!r} and the work's path")
        out[d] = m['path']
    return out

def prepare(lib):
    bad = standard.selftest()
    _need(not bad, 'tools/text/standard.py fails its own cases: ' + '; '.join(f'{c}: wants {w!r}, makes {g!r}' for c, w, g in bad))
    LANGS = json.load(open(os.path.join(lib, 'glossary', 'languages.json')))
    for code, L in LANGS.items():
        _need(re.fullmatch(r'[a-z]{2,3}', code), f"languages.json: {code!r} must be an ISO 639 code (2–3 lowercase letters)")
        _need(_bi(L.get('name')) and isinstance(L.get('script'), str), f"languages.json: {code} needs name {{hi, en}} and script")
        bad = [f for f in L.get('fallback', []) if f not in LANGS or f == code]; _need(not bad, f"languages.json: {code} has bad fallback {bad}")
        M = L.get('meaning')
        if M: _need(isinstance(M.get('short'), str) and M['short'] and _bi(M.get('name')), f"languages.json: {code}.meaning needs short and name {{hi, en}}")
    for f in glob.glob(os.path.join(lib, 'glossary', '*.json')):
        code = os.path.basename(f)[:-5]
        if code == 'languages': continue
        _need(code in LANGS, f"glossary/{code}.json: {code!r} is not in languages.json")
        for k, v in json.load(open(f)).items(): _need(isinstance(v, dict) and ('hi' in v or 'en' in v), f"glossary/{code}.json: {k!r} needs hi/en")
    G = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(lib, 'glossary', '*.json')) if not f.endswith('languages.json')}
    clean = word_rule()
    shelf = json.load(open(os.path.join(lib, 'index.json')))
    folders = check_folders()
    works = {}
    for leaf in leaves(shelf):
        _need(leaf['work'] not in works, f"shelf: work id {leaf['work']!r} is used twice")
        _need(folders.get(leaf['work']) == leaf['path'], f"shelf: work {leaf['work']!r} needs its folder tools/works/{leaf['work']}/ with path {leaf['path']!r} in work.json")
        wid, src = check_work(lib, leaf, LANGS); works[wid] = src
        check_words(lib, leaf['path'], json.load(open(os.path.join(lib, leaf['path'], 'work.json'), encoding='utf-8')), LANGS, G, clean)
    # store apps (library/apps.json): each app's shelves must exist on the shelf
    ap = os.path.join(lib, 'apps.json')
    if os.path.exists(ap):
        paths = set()
        def walk(ns, at):
            for n in ns:
                p = at + [n['id']]; paths.add('/'.join(p)); walk(n.get('children', []), p)
        walk(shelf, [])
        for aid, a in json.load(open(ap)).items():
            if aid.startswith('_'): continue
            _need(a.get('shelves') and all(x in paths for x in a['shelves']), f"apps.json: {aid}: every shelf must be a path on the shelf ({a.get('shelves')})")
    return works
