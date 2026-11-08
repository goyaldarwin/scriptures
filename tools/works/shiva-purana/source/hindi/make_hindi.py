"""The Hindi meanings → meanings/hi/gitapress.json, from the merged OCR of both scans (merge.py), every flagged word
as read by eye (review.py apply → <book>.read.json), the words the readers' whole lines set right (review.py lines →
<book>.lines.json), the book's typography (curly quotes, one em dash) and the fixes in hindi/corrections.json.

    python3 make_hindi.py [--draft]

Each printed paragraph sits under the last verse its mark names (॥ १३-१४ ॥ under 14), its mark kept as printed.
A paragraph with a word still in doubt (⟦…⟧: not yet read, or read as "⟨?⟩") is left out and listed; --draft keeps
it, for checking only (never committed).
"""
import json, os, re, sys, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..'))
BOOKS = ['shiv-1', 'kalyan-2018']
ABOUT = ("Gita Press's Hindi: the Māhātmya to the Rudra Saṃhitā's Yuddha Khaṇḍa from the Śrī Śivamahāpurāṇa with Hindi "
         "translation (code 2223), the rest from Kalyan's 2018 Śivamahāpurāṇāṅka; both scans read by OCR, every word "
         "the two passes did not read alike, or the word list lacks, read by eye on the page (source/hindi/README.md). "
         "Each paragraph sits under the last verse its mark names, its mark kept as printed")

def load(name, default):
    p = os.path.join(HERE, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default

def texts(book):
    """{verse id: paragraph} with every flagged word as read (a word not yet read stays ⟦…⟧)."""
    M, RD = load(f'{book}.merged.json', {}), load(f'{book}.read.json', {'at': {}, 'unknown': {}})
    R, at = {}, collections.Counter()               # each flag's reading by its printed place
    for l in open(os.path.join(HERE, f'{book}.flags.jsonl'), encoding='utf-8'):
        f = json.loads(l); key = f"{f['page']}|{f['side']}|{f['line']}"; p = f"{key}|{at[key]}"; at[key] += 1
        if f['k'] is None: continue
        w = RD['at'].get(p, RD['unknown'].get(f['word']) if f['why'] == 'unknown' else None)
        if w is not None: R.setdefault(f['id'], {})[str(f['k'])] = w
    out = {}
    for sec, V in M.items():
        for vid, v in V.items():
            k = iter(range(10 ** 6)); r = R.get(vid, {})
            def word(mo):
                w = r.get(str(next(k)))
                return w if w is not None else '⟦' + mo.group(1) + '⟧'
            t = re.sub(r'⟦(.*?)⟧', word, v['t'])
            out[vid] = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', t)).strip()
    return out

CORE = re.compile(r"^([‘’'\"“”(\[—-]*)(.*?)([‘’'\"“”)\],;!?।॥—-]*)$")

def set_right(t, fixes):
    """The readers' whole lines: a word between the same neighbours becomes the word as printed."""
    ws = t.split(' ')
    cores = [CORE.match(w).group(2) for w in ws]
    for before, a, after, b in fixes:
        for i, c in enumerate(cores):
            if c == a and (not before or (i and cores[i - 1] == before)) and (not after or (i + 1 < len(cores) and cores[i + 1] == after)):
                m = CORE.match(ws[i]); ws[i] = m.group(1) + b + m.group(3); cores[i] = b
    return ' '.join(ws)

VERB = r'(?:बोले|बोलीं|बोला|कहते हैं|कहने लगे|उवाच|रुवाच)'
SPEAKER = re.compile(r'(?:^|(?<=॥ )|(?<=॥))\s*((?:[^\s॥]+ ){0,3}?[^\s॥]+ (?:बोले|बोलीं|बोला)|[^\s॥]+ने (?:कहा|पूछा))(?:\s*[-—–]\s*|\s+)(?=\S)')
HEADING = re.compile(r'अध्याय|संहिता|खण्ड|श्रीगणेशाय|श्रीशिवमहापुराण|वाँ\b|^[\s—_-]')

PAIRS = collections.Counter()                       # ‘<a> और <b> बोले’ across the work (main fills it)

def speaker_at(t):
    """Where the speaker's words begin (‘सूतजी बोले’, ‘ब्रह्मा और विष्णु बोले’, ‘ऋषियोंने पूछा’), or None."""
    for m in re.finditer(r'(?<=\s)' + VERB + r'(?=[\s—-])|ने (?:कहा|पूछा)(?=[\s—-])', ' ' + t):
        ws = t[:m.start() - 1].rstrip().split(' ') if not m.group().startswith('ने') else t[:m.start() - 1].split(' ')
        n = 1 if not m.group().startswith('ने') else 0           # ‘ऋषियोंने’ is one word with its ने
        if m.group().startswith('ने'): ws, n = ws, 1
        if len(ws) >= 3 and ws[-2] == 'और' and PAIRS[' '.join(ws[-3:])] >= 2: n = 3   # ‘ब्रह्मा और विष्णु बोले’, a pair seen elsewhere too
        start = ' '.join(ws[:-n]) if len(ws) > n else ''
        return len(start) + (1 if start else 0)
    return None

def headings(vid, t, first):
    """An adhyāya's first paragraph: the previous closing line, the heading and the subtitle, which the column
    passes run into it, go, up to the speaker's words (‘सूतजी बोले—’); with no speaker there, it is listed."""
    if not first or vid.endswith('.0'): return t, False, ''
    if not HEADING.search(' '.join(t.split()[:40])): return t, False, ''
    at = speaker_at(t)
    if at is not None and len(t[:at].split()) <= 40: return t[at:], False, t[:at]
    return t, True, ''

def kalyan_heads():
    """{page: [heading words]}: each adhyāya's heading and subtitle in Kalyan as the whole-page pass reads them (after
    the closing line, up to the speaker). Kalyan sets them inside a column band, so the column passes can run their
    halves into the paragraphs around."""
    import glob
    spk = re.compile(r'बोले|बोलीं|बोला|कहते हैं|ने कहा|ने पूछा|उवाच|॥\s*[०-९]')
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'ocr', 'kalyan-2018', 'p*.json'))):
        P = json.load(open(f, encoding='utf-8')); L = [l.strip() for l in P['full'].splitlines() if l.strip()]
        for i, l in enumerate(L):
            if re.search(r'पूर्ण\s*हुआ\s*॥\s*[०-९]+\s*॥', l) or (i < 4 and re.search(r'^(पहला|दूसरा|तीसरा|चौथा|छठा|\S+वाँ)\s*अध्याय', l)):
                j = i + 1 if 'पूर्ण' in l else i; blk = []
                while j < len(L) and len(blk) < 4 and not spk.search(L[j]) and not re.search(r'[।॥]', L[j]): blk.append(L[j]); j += 1
                ws = re.findall(r'[\u0900-\u0963\u0970-\u097F]+(?:-[\u0900-\u0963\u0970-\u097F]+)*', ' '.join(blk).replace('\u200c', ''))
                if 'अध्याय' in ws: out.setdefault(P['page'], []).append(ws[max(0, ws.index('अध्याय') - 1):])
    return out

HEADWORD = r'(?:पहला|दूसरा|तीसरा|चौथा|छठा|\S+वाँ)'

def unhead(t, heads):
    """Take out of a paragraph the runs of a nearby heading's words (two or more in the heading's order), and a
    lone ‘अध्याय’ or ordinal beside them. Returns the paragraph and what was taken out."""
    from difflib import SequenceMatcher as SM
    same = lambda a, b: a == b or (len(a) > 3 and SM(None, a, b).ratio() >= .85)
    ws = t.split(' '); drop = set()
    core = [CORE.match(w).group(2) for w in ws]
    for H in heads:
        i = 0
        while i < len(ws):
            best = 0
            for h0 in range(len(H)):
                n = 0
                while i + n < len(ws) and h0 + n < len(H) and same(core[i + n], H[h0 + n]): n += 1
                best = max(best, n)
            run = range(i, i + best)
            anchored = any(core[x] == 'अध्याय' or re.fullmatch(HEADWORD, core[x]) for x in range(max(0, i - 1), min(len(ws), i + best + 1)))
            if best >= 2 and (anchored or (best >= 4 and any(len(core[x]) >= 8 for x in run))):
                drop |= set(run); i += best              # beside ‘अध्याय’, or four of its words in order
            else: i += 1
    for i, c in enumerate(core):                     # ‘अध्याय’ or an ordinal standing alone, out of any sentence
        if i not in drop and (c == 'अध्याय' or (re.fullmatch(HEADWORD, c) and (i - 1 in drop or i + 1 in drop))) and not re.match(r'(में|का|के|की|को|से|तक|है|हैं|था|थे)$', core[i + 1] if i + 1 < len(core) else ''):
            drop.add(i)
    if not drop: return t, ''
    return ' '.join(w for i, w in enumerate(ws) if i not in drop), ' '.join(ws[i] for i in sorted(drop))

def typography(t):
    t = t.replace('\u200c', '').replace('\u200d', '')                 # plain Unicode, as the Bhāgavata's Hindi
    t = ' '.join(w for w in t.split(' ') if not re.fullmatch(r"[0-9A-Za-z_?!.:;,'\"/()\[\]-]*[0-9A-Za-z_][0-9A-Za-z_?!.:;,'\"/()\[\]-]*", w))   # printer's marks, page numbers
    half = lambda n: re.sub(r'(?<=[०-९])(?:१?\s*/\s*२|½)+$', '½', n.strip())     # ६४१/२ (the passes' ½) → ६४½
    t = re.sub(r'\s*॥\s*([०-९][०-९\-–—½/ ]*?)\s*॥', lambda x: ' ॥ ' + '-'.join(half(n) for n in re.split(r'\s*[-–—]+\s*', x.group(1).strip())) + ' ॥', t)
    t = re.sub(r'[—-]*—[—-]*', '—', t)
    t = SPEAKER.sub(lambda x: ' ' + x.group(1) + '—', t).strip()       # the speaker's dash, which the passes drop                                 # one em dash (an OCR pass doubles it)
    t = re.sub(r"(^|[\s(\[—])'", r'\1‘', t); t = t.replace("'", '’')     # the book's curly quotes
    t = re.sub(r'(^|[\s(\[—])"', r'\1“', t); t = t.replace('"', '”')
    t = re.sub(r'\s+([,।?!;])', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip()

def main(draft=False):
    fix = load('corrections.json', {})                  # {verse id: [{"from": …, "to": …} or {"set": the paragraph}, …]}
    m, doubt, seen, split = {}, [], set(), []
    heads, cuts, unheads = [], [], []
    KH = kalyan_heads()
    for book in BOOKS:
        for t in texts(book).values():
            for x in re.finditer(r'(\S+ और \S+) (?:बोले|बोलीं|कहते हैं)', t): PAIRS[x.group(1)] += 1
    for book in BOOKS:
        lines = load(f'{book}.lines.json', {})
        proof = load(f'{book}.proof.json', {})          # paragraphs proofread whole against the page (null: no such paragraph)
        firsts = set(); pages = {vid: v['page'] for V in load(f'{book}.merged.json', {}).values() for vid, v in V.items()}
        for sec, V in load(f'{book}.merged.json', {}).items():
            if V: firsts.add(min(V, key=lambda k: int(k.rsplit('.', 1)[1]) if k.rsplit('.', 1)[1].isdigit() else -1))
        for vid, t in texts(book).items():
            if vid in seen: continue
            seen.add(vid)
            t, left, cut = headings(vid, set_right(t, lines.get(vid, [])), vid in firsts)
            if book == 'kalyan-2018':
                pg = pages[vid]; near = [h for p in (pg - 1, pg, pg + 1) for h in KH.get(p, [])]
                t, gone = unhead(t, near)
                if gone: unheads.append((vid, gone))
            if left: heads.append(vid)
            if cut.strip(): cuts.append((vid, cut))
            if vid in proof:
                if proof[vid] is None: continue
                t = proof[vid]
            t = typography(t)
            for f in fix.get(vid, []):
                if 'set' in f: t = f['set']; continue           # a paragraph read whole on the page
                if 'start' in f: assert f['start'] in t, (vid, f['start']); t = t[t.index(f['start']):]; continue
                assert f['from'] in t, (vid, f['from']); t = t.replace(f['from'], f['to'])
            if '⟦' in t or '⟨?⟩' in t:
                doubt.append(vid)
                if not draft: continue
            m[vid] = t
    for vid in list(m):                                 # a mark inside a paragraph (the walk passed it by): the
        sec = vid.rsplit('.', 1)[0]                     # paragraph splits there, each part under its own last verse
        parts = re.split(r'(?<=॥ )([०-९½/-]+)( ॥)\s+(?=\S)', m[vid])
        if len(parts) == 1: continue
        pieces, cur = [], ''
        for i in range(0, len(parts) - 1, 3):
            cur += parts[i] + parts[i + 1] + parts[i + 2]; pieces.append((parts[i + 1], cur)); cur = ''
        rest = parts[-1]
        moved = []
        for mark, piece in pieces:
            if '½' in mark or '/' in mark: rest = None; break   # a half verse joins the next verse's paragraph, as it is
            n = int(mark.split('-')[-1].translate(str.maketrans('०१२३४५६७८९', '0123456789')))
            if f'{sec}.{n}' in m or f'{sec}.{n}' in moved: rest = None; break
            moved.append((f'{sec}.{n}', piece))
        if rest is None: continue
        for k, piece in moved: m[k] = piece.strip(); split.append(k)
        m[vid] = rest.strip()
    failed = []                                         # the full proofreading against the page (<book>.full.json)
    for book in BOOKS:
        F = load(f'{book}.full.json', {'edits': {}, 'set': {}, 'add': {}})
        for vid, t in F['set'].items():
            if vid in m or vid in F['add']: m[vid] = typography(t)
        for vid, t in F['add'].items():
            if vid not in m: m[vid] = typography(t)
        for vid, E in F['edits'].items():
            if vid not in m: failed.append((vid, 'no paragraph')); continue
            for a, b in E:
                if a in m[vid]: m[vid] = m[vid].replace(a, b, 1)
                else: failed.append((vid, a))
            m[vid] = typography(m[vid])
    if failed: print(f'{len(failed)} proofreading edits not found:', failed[:20])
    for vid in [v for v, t in m.items() if '⟨?⟩' in t or '⟦' in t]:
        doubt.append(vid)
        if not draft: del m[vid]
    m = dict(sorted(m.items(), key=lambda kv: [int(x) if x.isdigit() else -1 for x in kv[0].replace('m.', '0.').split('.')]))
    out = {'about': ABOUT, 'title': {'hi': 'गीताप्रेस — हिन्दी अनुवाद', 'en': 'Gita Press — Hindi translation'},
           'order': 2, 'copied': True, 'm': m}
    path = os.path.join(WORK, 'meanings', 'hi', 'gitapress.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(f'{len(split)} paragraphs split off at a mark inside another')
    print(f'{len(cuts)} first paragraphs cut to the speaker; {len(unheads)} paragraphs with heading words taken out')
    print(f'{len(heads)} first paragraphs with a heading and no speaker:', ' '.join(heads))
    doubt = [d for d in doubt if d not in m]
    print(f'{len(m)} paragraphs written; {len(doubt)} with a word still in doubt' + (' (kept: --draft)' if draft else ' (left out)'))
    for d in doubt:
        if d not in m: print('  ', d)

if __name__ == '__main__':
    main('--draft' in sys.argv)
