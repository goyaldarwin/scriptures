"""The hard words of our meanings: list the candidates, and check the entries (docs/LIBRARY.md §5, "hard": true).

  python3 tools/meanings/hard_words.py candidates OUT_DIR [--batch N]
      Every word of our own Hindi and English meanings (tools/works/*/meanings/{hi,en}/scriptures.json), grouped under its
      plain form the way the app finds it (a joined Hindi ending, an English plural or tense: tools/site/app.js hardForms),
      with how often it is used, the works it is in and two places it is used. Words that already have a hard entry
      (library/glossary/hi.json, en.json, or the work's own glossary/<lang>.json) are left out. Writes
      OUT_DIR/<lang>-NN.json, N words a file, most-used first, for a writer to choose the hard ones from.
  python3 tools/meanings/hard_words.py apply BATCH.out.json [...]
      Puts written entries into the dictionaries, each marked "hard": true: a new word into library/glossary/<lang>.json,
      a sense only one work gives ("work") into tools/works/<work>/glossary/<lang>.json; "keep" marks an existing Hindi entry
      hard; "skip" is left out. A reviewer's BATCH.review.json beside it ({"w", "fix": {...}} or {"w", "drop": why}) is
      applied first. An existing shared entry is never overwritten.
  python3 tools/meanings/hard_words.py report [--reach]
      For each hard entry, how many places in our meanings the app would underline; entries it would never underline
      (a key that no form of any word in the meanings reaches) are listed. --reach lists every word each key underlines.
"""
import glob, json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORD = {'hi': re.compile(r'[ऀ-ॣ०-ॿ‌‍]+'), 'en': re.compile(r"[A-Za-zÀ-ɏḀ-ỿ]+(?:[’'][A-Za-zÀ-ɏḀ-ỿ]+)*")}
HI_POST = ['वाला', 'वाली', 'वाले', 'में', 'से', 'को', 'का', 'की', 'के', 'ने', 'पर', 'तक']

def _base(w):
    w = re.sub('[\u200c\u200d]', '', w)   # a joiner (जाम्बवान्‌ने) is not part of the word
    base = [w] + [w[:-len(p)] for p in HI_POST if len(w) > len(p) + 1 and w.endswith(p)]
    return base + [x[:-2] for x in base if len(x) > 3 and x.endswith('जी')]   # विभीषणजीने → विभीषण

def _plural(x):
    """A plural's guessed singulars, in the app's order (an ī-noun's देवियों → देवी before an i-noun's शक्तियों → शक्ति)."""
    v = [re.sub('ियों$', 'ी', x), re.sub('ियों$', 'ि', x), re.sub('ियाँ$', 'ी', x), re.sub('ियाँ$', 'ि', x), re.sub('एँ$', '', x), re.sub('ओं$', '', x), re.sub('ों$', '', x), re.sub('ों$', 'ा', x), re.sub('ें$', '', x), re.sub('ें$', 'ा', x), re.sub('े$', 'ा', x)]
    return [y for y in v if y != x]

def forms(w, lang):
    """The forms the app tries for a word of a meaning, in its order (tools/site/app.js hardForms): the word, without its
    postposition or जी, then a plural's guessed singulars."""
    if lang == 'en':
        x = re.sub(r"[’']s$", '', w.lower())
        return [x, re.sub(r'ies$', 'y', x), re.sub(r'es$', '', x), re.sub(r's$', '', x), re.sub(r'ed$', '', x), re.sub(r'ed$', 'e', x), re.sub(r'ing$', '', x), re.sub(r'ing$', 'e', x), re.sub(r'ly$', '', x)]
    base = _base(w)
    return base + [y for x in base for y in _plural(x)]

def hard_key(w, lang, ent):
    """The hard entry the app underlines a word with (tools/site/app.js hardKey), or None. ent(k): the entry for key k (the
    work's own glossary first, then the shared one), or None. In Hindi the word itself, or without its postposition or जी,
    decides when it has an entry (a plain one makes it a plain word: परे is never taken for परा); only a word with no
    entry of its own is looked through as a plural, the first form found deciding."""
    if lang == 'en':
        for k in forms(w, lang):
            e = ent(k)
            if e is not None: return k if e.get('hard') else None
        return None
    base = _base(w)
    for k in base:
        e = ent(k)
        if e is not None and e.get('hard'): return k
    if any(ent(k) is not None for k in base): return None
    for x in base:
        for k in _plural(x):
            e = ent(k)
            if e is not None: return k if e.get('hard') else None
    return None

def meanings():
    """(work, lang, item id, text) for every one of our meanings, each text once (the Sundarakāṇḍa repeats the Mānas)."""
    seen = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'tools/works/*/meanings/*/scriptures.json'))):
        work, lang = f.split('/')[-4], f.split('/')[-2]
        if lang not in WORD: continue
        for iid, v in json.load(open(f, encoding='utf-8')).get('m', {}).items():
            t = v[0] if isinstance(v, list) else v
            if isinstance(t, str) and (lang, t) not in seen: seen.add((lang, t)); yield work, lang, iid, t

def hard_keys():
    """lang → set of keys with a hard entry: the shared dictionaries and every work's own glossary."""
    H = defaultdict(set)
    for lang in WORD:
        p = os.path.join(ROOT, 'library/glossary', lang + '.json')
        if os.path.exists(p): H[lang] |= {k for k, v in json.load(open(p, encoding='utf-8')).items() if v.get('hard')}
        for f in glob.glob(os.path.join(ROOT, 'tools/works/*/glossary', lang + '.json')):
            H[lang] |= {k for k, v in json.load(open(f, encoding='utf-8')).items() if v.get('hard')}
    return H

def candidates(out, batch):
    H = hard_keys(); count = Counter(); where = defaultdict(set); ex = defaultdict(list); surface = defaultdict(set)
    for work, lang, iid, t in meanings():
        for m in WORD[lang].finditer(t):
            w = m.group(0); count[(lang, w)] += 1; where[(lang, w)].add(work)
            if len(ex[(lang, w)]) < 2: ex[(lang, w)].append(f"{work}:{iid}: …{t[max(0, m.start() - 60):m.end() + 60]}…")
            surface[lang].add(w if lang == 'hi' else w.lower())
    groups = defaultdict(lambda: {'n': 0, 'forms': set(), 'works': set(), 'ex': []})
    for (lang, w), n in count.items():
        fs = forms(w, lang)
        if any(f in H[lang] for f in fs): continue   # already has a hard entry
        known = [f for f in fs if f in surface[lang]]
        lemma = min(known or fs, key=len)   # the shortest form: भौंहके, भौंहें, भौंहोंकी are one word
        if (lang == 'hi' and len(lemma) < 3) or (lang == 'en' and len(lemma) < 4): continue
        g = groups[(lang, lemma)]; g['n'] += n; g['forms'].add(w); g['works'] |= where[(lang, w)]
        g['ex'] = (g['ex'] + ex[(lang, w)])[:2]
    os.makedirs(out, exist_ok=True)
    for lang in WORD:
        L = sorted(((k[1], g) for k, g in groups.items() if k[0] == lang), key=lambda x: (-x[1]['n'], x[0]))
        rows = [{'w': w, 'n': g['n'], 'forms': sorted(g['forms']), 'works': sorted(g['works']), 'ex': g['ex']} for w, g in L]
        for k in range(0, len(rows), batch):
            json.dump(rows[k:k + batch], open(os.path.join(out, f'{lang}-{k // batch + 1:03d}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        print(f'{lang}: {len(rows)} words → {(len(rows) + batch - 1) // batch} files of {batch}')

def apply(files):
    sys.path.insert(0, os.path.join(ROOT, 'tools')); import jsonio
    shared = {l: json.load(open(os.path.join(ROOT, 'library/glossary', l + '.json'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'library/glossary', l + '.json')) else {} for l in WORD}
    own = {}; n = Counter()
    for f in files:
        lang = os.path.basename(f)[:2]; rows = json.load(open(f, encoding='utf-8'))
        rv = f.replace('.out.json', '.review.json'); R = {r['w']: r for r in json.load(open(rv, encoding='utf-8'))} if os.path.exists(rv) else {}
        for e in rows:
            r = R.get(e['w'], {})
            if 'drop' in r or 'skip' in e: n['left out'] += 1; continue
            e = dict(e, **r.get('fix', {})); k = e['w']
            if e.get('keep'):
                if k in shared[lang] and shared[lang][k].get('hi') and shared[lang][k].get('en'): shared[lang][k]['hard'] = True; n['kept'] += 1
                continue
            entry = {x: e[x] for x in ('hi', 'en', 'g') if e.get(x)}; entry['hard'] = True
            if e.get('work'):
                p = os.path.join(ROOT, 'tools/works', e['work'], 'glossary', lang + '.json')
                D = own.setdefault(p, json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {})
                if k not in D: D[k] = entry; n['work'] += 1
            elif k in shared[lang]: n['already there'] += 1
            else: shared[lang][k] = entry; n['new'] += 1
    for l, D in shared.items(): jsonio.dump_glossary(os.path.join(ROOT, 'library/glossary', l + '.json'), D)
    for p, D in own.items(): os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(D, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')
    print(dict(n))

def report(reach=False):
    H = hard_keys(); hit = Counter(); via = defaultdict(Counter); D = {}
    def ent(work, lang):   # the work's own glossary first, then the shared dictionary, as the app looks a word up
        if (work, lang) not in D:
            wp = os.path.join(ROOT, 'tools/works', work, 'glossary', lang + '.json'); sp = os.path.join(ROOT, 'library/glossary', lang + '.json')
            if lang not in D: D[lang] = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else {}
            W = json.load(open(wp, encoding='utf-8')) if os.path.exists(wp) else {}
            D[(work, lang)] = lambda k, W=W, S=D[lang]: W.get(k, S.get(k))
        return D[(work, lang)]
    for work, lang, iid, t in meanings():
        for m in WORD[lang].finditer(t):
            k = hard_key(m.group(0), lang, ent(work, lang))
            if k: hit[(lang, k)] += 1; via[(lang, k)][m.group(0)] += 1
    if reach:   # every word each hard key underlines, to catch a wrong catch (साम in सामने)
        for (lang, k), ws in sorted(via.items()): print(lang, k, '←', ' '.join(f'{w}×{n}' for w, n in ws.most_common()))
    for lang in WORD:
        dead = sorted(k for k in H[lang] if not hit[(lang, k)])
        print(f'{lang}: {len(H[lang])} hard entries, {sum(n for (l, _), n in hit.items() if l == lang)} places underlined; never reached: {len(dead)} {dead[:30]}')

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['candidates']: candidates(a[1], int(a[a.index('--batch') + 1]) if '--batch' in a else 400)
    elif a[:1] == ['apply']: apply(a[1:])
    elif a[:1] == ['report']: report('--reach' in a)
    else: sys.exit(__doc__)
