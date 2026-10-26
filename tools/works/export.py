"""One exporter for every work: tools/works/<work>/ → library/<path>/. The folder's format is in tools/works/README.md.

    python3 tools/works/export.py                 every work, each after the works it takes verses from
    python3 tools/works/export.py manas sundarkand
    python3 tools/works/export.py --out DIR …     write into DIR (a copy of library/) instead of library/

Writes   library/<path>/work.json                 the manifest's fields, the verses (text.txt) and the topics
         library/<path>/meanings/<lang>-<src>.json one per meaning source (meanings/<lang>/<src>.json)
         library/<path>/glossary.json             the work's own senses of words (glossary/<lang>.json), if any
The recordings' timings (library/<path>/audio/<src>.json) are made by tools/audio/make_timings.py.
Every file goes through the writing standard (tools/jsonio.py → tools/text/standard.py). It stops on anything wrong:
an unknown verse, type, part or work; a verse without lines; a meaning for a verse the work does not have; our own
meanings missing a verse (unless the source is `partial`) or sharing a run of 10+ words with a copied source.
`sources` (and `glossary` in work.json) are added by tools/site/build.py.
"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'tools')); import jsonio
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'tools', 'meanings')); import versenum, overlap
sys.path.insert(0, os.path.join(REPO, 'tools', 'text')); import standard

# the title of our own meanings (source "scriptures") in each language, when its file gives none
OUR_TITLE = {'hi': {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'},
             'en': {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'},
             'pa': {'hi': 'पंजाबी अर्थ — शास्त्र', 'en': 'Punjabi meaning — Scriptures'}}
BUILD_ONLY = {'path', 'include', 'topics'}   # manifest keys that steer the export and are not copied into work.json

class WorkError(Exception): pass
def need(ok, msg):
    if not ok: raise WorkError(msg)

def folders():
    return sorted(d for d in os.listdir(HERE) if os.path.isfile(os.path.join(HERE, d, 'work.json')))

def manifest(wid):
    m = json.load(open(os.path.join(HERE, wid, 'work.json'), encoding='utf-8'))
    need(m.get('id') == wid, f'{wid}/work.json: id {m.get("id")!r} must equal the folder name')
    for f in m.get('include', []):
        extra = json.load(open(os.path.join(HERE, wid, f), encoding='utf-8'))
        need(not set(extra) & set(m), f'{wid}/{f}: its keys {sorted(set(extra) & set(m))} are in work.json too')
        m.update(extra)
    return m

# ---- text.txt ----
from textfile import HEAD, TAKE   # the format of text.txt

def takes(wid):
    """The works whose verses this work's text takes."""
    return sorted({m.group('w') for l in open(os.path.join(HERE, wid, 'text.txt'), encoding='utf-8') for m in [TAKE.fullmatch(l.strip())] if m})

def order(wids):
    """Each work after the works it takes from."""
    out, seen = [], set()
    def visit(w, path=()):
        need(w not in path, f'works take from each other in a circle: {" → ".join(path + (w,))}')
        if w in seen: return
        for t in takes(w): visit(t, path + (w,))
        seen.add(w); out.append(w)
    for w in wids: visit(w)
    return out

def read_text(wid, M, lib):
    """text.txt → (items, topics, taken {item id: source work})"""
    keys = [p.get('key') for p in M['parts']['list']]
    part, sec, lang, topic = 0, None, M['lang'], None
    items, topics, taken = [], [], {}
    def add_topic(iid):
        nonlocal topic
        if topic: topics.append({'id': iid, **topic}); topic = None
    for no, raw in enumerate(open(os.path.join(HERE, wid, 'text.txt'), encoding='utf-8'), 1):
        line = raw.strip(); where = f'{wid}/text.txt:{no}'
        if not line or line.startswith('#'): continue
        if line.startswith('@'):
            cmd, _, arg = line[1:].partition(' '); arg = arg.strip()
            if cmd == 'part': need(arg in keys, f'{where}: unknown part {arg!r} (work.json → parts.list[].key)'); part = keys.index(arg)
            elif cmd == 'section': sec = arg
            elif cmd == 'lang': lang = arg
            elif cmd == 'topic':
                f = [x.strip() for x in arg.split('|')]; need(len(f) == 2, f'{where}: @topic hi | en'); topic = {'hi': f[0], 'en': f[1]}
            else: need(False, f'{where}: unknown line {line!r}')
            continue
        m = TAKE.fullmatch(line)
        if m:
            S = lib.work(m.group('w')); sid = [x['id'] for x in S['items']]
            need(m.group('a') in sid and (not m.group('b') or m.group('b') in sid), f'{where}: {m.group("w")} has no verse {m.group("a")} / {m.group("b")}')
            a = sid.index(m.group('a')); b = sid.index(m.group('b')) if m.group('b') else a
            run = S['items'][a:b + 1]
            for x in run:
                it = {k: v for k, v in x.items() if k not in ('p', 'l', 't')}
                it['p'] = part
                if not m.group('b') and sec: it['s'] = sec   # a single verse joins this text's section; a run keeps its own
                if x.get('l', S['lang']) != M['lang']: it['l'] = x.get('l', S['lang'])
                items.append(it); taken[it['id']] = m.group('w')
            own_first = topic is not None; add_topic(run[0]['id'])
            if m.group('b'):   # a run brings the source work's topics, named by this work's choice (work.json → topics)
                names = lib.headings(m.group('w'), M.get('topics'))
                inside = [t for t in S['topics'] if sid.index(t['id']) in range(a, b + 1)]
                if not inside or inside[0]['id'] != run[0]['id']:   # the run starts inside a topic: it opens with that topic's name
                    cover = [t for t in S['topics'] if sid.index(t['id']) <= a]
                    if cover and not (topics and topics[-1]['id'] == run[0]['id']): inside.insert(0, dict(cover[-1], id=run[0]['id']))
                if own_first: inside = [t for t in inside if t['id'] != run[0]['id']]   # this text's own topic names the run's start
                for t in inside:
                    nm = names.get(t['id'], t) if names is not None else t
                    need(names is None or t['id'] in names or t is inside[0], f'{where}: no heading for topic {t["id"]} in {m.group("w")}/topics.json')
                    topics.append({'id': t['id'], 'hi': nm['hi'], 'en': nm['en']})
            continue
        m = HEAD.fullmatch(line)
        if m:
            need(sec, f'{where}: a verse before the first @section')
            it = {'id': m.group('id'), 'p': part, 's': sec, 'y': m.group('y'), 'n': m.group('n') or '', 'v': []}
            if lang != M['lang']: it['l'] = lang
            items.append(it); add_topic(it['id']); continue
        need(items and items[-1]['id'] not in taken, f'{where}: a line outside a verse: {line[:40]!r}')
        items[-1]['v'].append(line)
    ids = [x['id'] for x in items]
    need(len(set(ids)) == len(ids), f'{wid}: verse ids repeat: {sorted({i for i in ids if ids.count(i) > 1})[:5]}')
    need(all(x['v'] for x in items), f'{wid}: verses without lines: {[x["id"] for x in items if not x["v"]][:5]}')
    known = set(M.get('types') or {}) | {'cau', 'do', 'so', 'cha', 'shloka'}
    need({x['y'] for x in items} <= known, f'{wid}: unknown verse types {sorted({x["y"] for x in items} - known)} (work.json → types)')
    return items, topics, taken

# ---- the library being written ----
class Lib:
    def __init__(self, out): self.out, self.cache = out, {}
    def path(self, wid): return manifest(wid)['path']
    def work(self, wid):
        p = os.path.join(self.out, self.path(wid), 'work.json'); need(os.path.exists(p), f'{wid} is not exported yet')
        return json.load(open(p, encoding='utf-8'))
    def meanings(self, wid):
        d = os.path.join(self.out, self.path(wid), 'meanings')
        return {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(d, '*.json'))}
    def headings(self, wid, choice):
        """A work's topic headings by first verse id when a taking work shows "ours" (the work's topics.json), else None."""
        if choice != 'ours': return None
        return json.load(open(os.path.join(HERE, wid, 'topics.json'), encoding='utf-8'))
    def dump(self, rel, obj): return jsonio.dump_library(self.out, rel, obj)

def export(wid, lib):
    M = manifest(wid); WP = M['path']
    items, topics, taken = read_text(wid, M, lib)
    ids = [x['id'] for x in items]; BYID = {x['id']: x for x in items}; own = [i for i in ids if i not in taken]
    work = {k: v for k, v in M.items() if k not in BYID and k not in BUILD_ONLY}
    work['parts'] = {**M['parts'], 'list': [{k: v for k, v in p.items() if k != 'key'} for p in M['parts']['list']]}
    work['items'] = items; work['topics'] = topics
    old = os.path.join(lib.out, WP, 'work.json')   # keep the sources list that build.py registered
    if os.path.exists(old): work['sources'] = json.load(open(old, encoding='utf-8')).get('sources', {})
    lib.dump(WP + '/work.json', work)

    # ---- meanings: meanings/<lang>/<src>.json ----
    have = set()
    srcs = {}
    for f in sorted(glob.glob(os.path.join(HERE, wid, 'meanings', '*', '*.json'))):
        lg = os.path.basename(os.path.dirname(f)); src = os.path.basename(f)[:-5]
        srcs[(lg, src)] = json.load(open(f, encoding='utf-8'))
    copied = {k: v for k, v in srcs.items() if v.get('copied')}
    taken_from = {}   # source work → its meaning files in the library
    for w in set(taken.values()): taken_from[w] = lib.meanings(w)
    for (lg, src), D in srcs.items():
        sid = f'{lg}-{src}'; mine = D.get('m', {})
        unknown = [k for k in mine if k not in BYID or k in taken]
        need(not unknown, f'{wid}/meanings/{lg}/{src}.json: meanings for verses this work does not write itself: {unknown[:5]}')
        if mine and not D.get('partial') and not D.get('copied'):
            miss = [i for i in own if not mine.get(i)]
            need(not miss, f'{wid}/meanings/{lg}/{src}.json: no meaning for {miss[:5]} (or mark the source "partial")')
        for (clg, csrc), C in copied.items():   # our own meanings never copy a copied source
            if clg != lg or csrc == src or D.get('copied'): continue
            res = overlap.check({k: versenum.joined(v) for k, v in mine.items()}, {k: versenum.joined(v) for k, v in C.get('m', {}).items()})
            bad = [r for r in res if len(r[1]) >= 10]
            need(not bad, f'{wid}/meanings/{lg}/{src}.json: {len(bad)} meanings share 10+ words with {csrc}, e.g. {bad[0][0] if bad else ""}: {" ".join(bad[0][1]) if bad else ""}')
            note = [r for r in res if len(r[1]) >= 6]
            if note: print(f'{wid} {sid}: {len(note)} meanings share 6–9 words with {csrc} (read them: tools/meanings/overlap.py --report)')
        m, p = {}, {}
        for i in ids:
            if i in taken:   # a taken verse: the same source of the work it comes from
                S = taken_from[taken[i]].get(sid)
                if S and i in S['m']:
                    m[i] = S['m'][i]
                    if i in S.get('p', {}): p[i] = S['p'][i]
                continue
            if i not in mine: continue
            v = mine[i]
            if D.get('numbers'):
                t, pcs = versenum.text_and_pieces(v, BYID[i], lg, by_n=D['numbers'] == 'n')
            else:
                t, pcs = (v, None) if isinstance(v, str) else (versenum.joined(v), [x.strip() for x in v])
            m[i] = [t] + ([D['notes'][i]] if i in D.get('notes', {}) else [])
            if pcs: p[i] = pcs
        title = D.get('title') or (OUR_TITLE.get(lg) if src == 'scriptures' else None)
        if not title:   # a source with no entries of its own: the same source of the work its verses come from
            title = next((tf[sid]['title'] for tf in taken_from.values() if sid in tf), None)
        need(title, f'{wid}/meanings/{lg}/{src}.json: needs a title')
        need(m, f'{wid}/meanings/{lg}/{src}.json: no meaning for any verse')
        out = {'id': sid, 'lang': lg, 'order': D['order'], 'title': title, 'm': m}
        if p: out['p'] = p
        lib.dump(f'{WP}/meanings/{sid}.json', out); have.add(sid + '.json')
    for f in glob.glob(os.path.join(lib.out, WP, 'meanings', '*.json')):   # a source removed from the folder leaves the library too
        if os.path.basename(f) not in have: os.remove(f)

    # ---- the work's own senses of words: glossary/<lang>.json ----
    senses = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(HERE, wid, 'glossary', '*.json')))}
    words = {}
    for x in items:
        for l in x['v']:
            for t in l.split(): words.setdefault(x.get('l', M['lang']), set()).add(standard.fold(standard.SVARA.sub('', re.sub(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९੦-੯0-9]", '', t))))
    for lg, D in senses.items():   # a word as the app looks it up (standard.fold: गङ्गा and गंगा are one word)
        bad = [k for k, v in D.items() if standard.fold(k) not in words.get(lg, ()) or not (v.get('hi') and v.get('en'))]
        need(not bad, f'{wid}/glossary/{lg}.json: senses of words not in any {lg} verse, or without hi and en: {bad[:5]}')
    gl = os.path.join(lib.out, WP, 'glossary.json')
    if senses: lib.dump(WP + '/glossary.json', senses)
    elif os.path.exists(gl): os.remove(gl)

    print(f'{wid}: {len(items)} verses ({len(taken)} taken), {len(topics)} topics, {len(srcs)} meaning sources')

def main(argv):
    out = os.path.join(REPO, 'library')
    if '--out' in argv: k = argv.index('--out'); out = argv[k + 1]; argv = argv[:k] + argv[k + 2:]
    wids = argv or folders()
    unknown = [w for w in wids if w not in folders()]
    if unknown: sys.exit(f'no work folder {unknown} in tools/works')
    lib = Lib(out)
    try:
        for w in order(wids): export(w, lib)
    except WorkError as e: sys.exit(f'EXPORT STOPPED: {e}')

if __name__ == '__main__': main(sys.argv[1:])
