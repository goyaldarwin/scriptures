"""Register sources and check the library before every build (called by build.py).

For each work on the shelf (library/index.json) this:
  1. lists the meaning sources in <work>/meanings/*.json and the audio sources in <work>/audio/*.json
     and writes them into work.json → "sources" (the website reads that list; it cannot scan folders),
     and marks "glossary": true when the work has its own <work>/glossary.json;
  2. checks that everything refers to things that exist (sources, plans, topics, verse languages,
     dictionaries in glossary/, fallbacks), and stops the build with a clear message if not.
A source's file name must equal its "id". The source with the lowest "order" (then id) is the default.
"""
import glob, json, os, re

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
    for x in items:
        _need(isinstance(x.get('v'), list) and x['v'], f"{name}: item {x['id']} has no verse lines")
        _need(0 <= x['p'] < len(w['parts']['list']), f"{name}: item {x['id']} part {x['p']} out of range")
    for k, t in (w.get('types') or {}).items():
        _need(re.fullmatch(r'[a-z0-9_]+', k) and _bi(t.get('name')) and (_bi(t['short']) if 'short' in t else True), f"{name}: type {k!r} needs name {{hi, en}} (and a bilingual short if given)")
    for t in w.get('topics', []): _need(t['id'] in ID and _bi({'hi': t['hi'], 'en': t['en']}), f"{name}: topic {t} is invalid")
    for p in w.get('plans', []):
        _need(len(p['end']) == p['n'], f"{name}: plan {p['id']} has {len(p['end'])} ends for {p['n']} days")
        pos = [ids.index(e) if e in ID else -1 for e in p['end']]
        _need(min(pos) >= 0 and pos == sorted(pos), f"{name}: plan {p['id']} ends are missing or out of order")
        # before / after: pages read before the first day and after the reading (pūrvāṅga / uttarāṅga)
        pages = ({'vidhi'} if (w.get('vidhi') or {}).get('hi') else set()) | ({'aarti'} if (w.get('vidhi') or {}).get('aarti') else set()) | ({'visarjan'} if (w.get('vidhi') or {}).get('visarjan') else set())
        vs = (w.get('vidhi') or {}).get('visarjan')
        if vs: _need(_bi(vs.get('title')) and _bi(vs.get('when')) and all(len(x.get('v', [])) >= 1 and x.get('hi') and x.get('en') for x in vs.get('verses', [])) and vs.get('verses'), f"{name}: vidhi.visarjan needs title, when and verses [{{v, hi, en}}]")
        for k in ('before', 'after'):
            _need(all(x in pages for x in p.get(k, [])), f"{name}: plan {p['id']} {k} {p.get(k)} names a page the work lacks (has {sorted(pages)})")
    # sources
    src = {'hi': [], 'en': [], 'au': []}
    for f in sorted(glob.glob(os.path.join(lib, path, 'meanings', '*.json'))):
        s = json.load(open(f)); sid = os.path.basename(f)[:-5]; where = f"{name}/meanings/{sid}.json"
        _need(s.get('id') == sid, f"{where}: id {s.get('id')!r} must equal the file name")
        _need(s.get('lang') in ('hi', 'en'), f"{where}: lang must be hi or en")
        _need(_bi(s.get('title')), f"{where}: needs title {{hi, en}}")
        bad = [k for k in s['m'] if k not in ID]; _need(not bad, f"{where}: {len(bad)} unknown item ids, e.g. {bad[:3]}")
        for k, e in s['m'].items(): _need(isinstance(e, list) and e and isinstance(e[0], str), f"{where}: {k} must be [text, footnotes?]")
        src[s['lang']].append({'id': sid, 'file': 'meanings/' + sid, 'title': s['title'], 'order': s.get('order', 100)})
    for f in sorted(glob.glob(os.path.join(lib, path, 'audio', '*.json'))):
        s = json.load(open(f)); sid = os.path.basename(f)[:-5]; where = f"{name}/audio/{sid}.json"
        _need(s.get('id') == sid, f"{where}: id {s.get('id')!r} must equal the file name")
        _need(s.get('type') == 'youtube', f"{where}: type must be youtube")
        _need(_bi(s.get('title')), f"{where}: needs title {{hi, en}}")
        T = s['tracks']
        for t in T: _need(re.fullmatch(r'[\w-]{11}', t['yt']) and t['first'] in ID and t['last'] in ID and t['dur'] > 0, f"{where}: bad track {t}")
        for k, (ti, sec) in s['at'].items(): _need(k in ID and 0 <= ti < len(T) and 0 <= sec <= T[ti]['dur'], f"{where}: bad timing {k}: {[ti, sec]}")
        src['au'].append({'id': sid, 'file': 'audio/' + sid, 'title': s['title'], 'order': s.get('order', 100)})
    for k in src:
        src[k].sort(key=lambda x: (x['order'], x['id']))
        for x in src[k]: del x['order']
    has_g = os.path.exists(wg)   # the app fetches <work>/glossary.json only when the work says it has one
    if w.get('sources') != src or bool(w.get('glossary')) != has_g:
        w['sources'] = src
        if has_g: w['glossary'] = True
        else: w.pop('glossary', None)
        json.dump(w, open(wp, 'w'), ensure_ascii=False, separators=(',', ':'))
    return w['id'], {k: [x['id'] for x in v] for k, v in src.items()}

def prepare(lib):
    LANGS = json.load(open(os.path.join(lib, 'glossary', 'languages.json')))
    for code, L in LANGS.items():
        _need(re.fullmatch(r'[a-z]{2,3}', code), f"languages.json: {code!r} must be an ISO 639 code (2–3 lowercase letters)")
        _need(_bi(L.get('name')) and isinstance(L.get('script'), str), f"languages.json: {code} needs name {{hi, en}} and script")
        bad = [f for f in L.get('fallback', []) if f not in LANGS or f == code]; _need(not bad, f"languages.json: {code} has bad fallback {bad}")
    for f in glob.glob(os.path.join(lib, 'glossary', '*.json')):
        code = os.path.basename(f)[:-5]
        if code == 'languages': continue
        _need(code in LANGS, f"glossary/{code}.json: {code!r} is not in languages.json")
        for k, v in json.load(open(f)).items(): _need(isinstance(v, dict) and ('hi' in v or 'en' in v), f"glossary/{code}.json: {k!r} needs hi/en")
    shelf = json.load(open(os.path.join(lib, 'index.json')))
    works = {}
    for leaf in leaves(shelf):
        _need(leaf['work'] not in works, f"shelf: work id {leaf['work']!r} is used twice")
        wid, src = check_work(lib, leaf, LANGS); works[wid] = src
    return works
