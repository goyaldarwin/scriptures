"""The Hindi of a scan's OCR (ocr/<book>/p<NNNN>.json, by ocr.py), merged and checked, per verse, with every doubtful word
flagged for reading by eye on the page image (hindi/README.md).

    python3 merge.py <book> <first adhyāya> [<last adhyāya> [<pages>]]      e.g.  merge.py shiv-1 m.1 2.5.59

It writes hindi/<book>.merged.json: {section: {verse id: {"t": text with ⟦…⟧ around each flag, "page": n, "mark": "८-९"}}},
and hindi/<book>.flags.jsonl: one line per flagged word, {id, page, side, line, word, why, alt}.
A word is accepted unflagged only when both passes read it alike and it occurs in the exact Gita Press Hindi of the
Bhāgavata, Vālmīki and Mānas (library/), or is two such words joined; every other word is flagged.
"""
import json, os, re, sys, glob, difflib, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'works'))
import jsonio, textfile

def plain(w): return unicodedata.normalize('NFC', w).replace('‌', '').replace('‍', '')

def vocab():
    V = collections.Counter()
    for p in ['library/hinduism/purana/mahapurana/bhagavata/meanings/hi-gitapress.json',
              'library/hinduism/granth/valmiki/ramayana/meanings/hi-gitapress.json',
              'library/hinduism/granth/tulsidas/ramcharitmanas/meanings/hi-gitapress.json']:
        for v in jsonio.read_meanings(os.path.join(ROOT, p))['m'].values():
            t = v[0] if isinstance(v, list) else v
            t = ' '.join(t) if isinstance(t, list) else t
            for w in re.findall(r'[ऀ-ॣॱ-ॿ‌‍]+', t): V[plain(w)] += 1
    return set(V)
V = vocab()
ENDS = ['का', 'की', 'के', 'को', 'से', 'में', 'ने', 'पर', 'तक', 'वाले', 'वाला', 'वाली', 'ों', 'ोंके', 'ोंको', 'ोंसे', 'ोंमें', 'ोंका', 'ोंकी', 'ोंने']
TOK = re.compile(r'[ऀ-ॣॱ-ॿ‌‍]+|[०-९]+|\S')
NUM = re.compile(r'^[०-९]+$')
QUOTES = set('\'"‘’“”`')

CONFIRMED = os.path.join(HERE, 'confirmed.txt')     # words read by eye on the page and found right: one per line
if os.path.exists(CONFIRMED): V |= {plain(l.strip()) for l in open(CONFIRMED, encoding='utf-8') if l.strip()}

def known(w):
    w = plain(w)
    return w in V or bool(NUM.match(w)) or not re.match('[\u0900-\u0963\u0966-\u097F]', w)     # the daṇḍas are punctuation

def compound(w):
    w = plain(w)
    for i in range(2, len(w) - 1):
        a, b = w[:i], w[i:]
        if a in V and (b in V or any(b.endswith(e) and b[:-len(e)] in V for e in ENDS)): return True
    return False

def toks(text):
    out = []
    lines = unicodedata.normalize('NFC', text).replace('।।', '॥').splitlines()
    if lines and len(lines[0].split()) <= 8 and re.search(r'[०-९]{1,4}\s*$|^[०-९]|संहिता|महापुराण|अ०|माहात्म्य', lines[0]):
        lines[0] = ''                                                     # the running header (… संहिता ४९, [अ० १)
    for li, line in enumerate(lines):
        line = re.sub(r'^[|;:`„)\]\s]+(?=\S)', '', line)                  # the column rule's marks at a line's start
        line = re.sub(r'^[०-९]{1,3}\s*[|।]?\s+', '', line)                 # the Sanskrit column's verse number beside the gutter
        line = re.sub(r'(?<=[\u0900-\u0963])\s?:', 'ः', line)            # a visarga read as a colon (अत : → अतः)
        line = re.sub(r'-\s?-', '—', line)                                  # an em dash read as two hyphens
        line = re.sub(r'(?<=[\u0900-\u097F])\s*\|(?=\s|$)', ' ।', line)       # a daṇḍa read as |
        line = re.sub(r'(?<![A-Za-z])[A-Za-z\\]{1,3}(?![A-Za-z])', ' ', line)   # stray Latin letters from the pictures
        for m in TOK.finditer(line):
            out.append((m.group(), li, m.start() > 0 and line[m.start() - 1] == ' '))
    return out

def merge(a, b):
    """[(word, line, space before, flag, alternatives)] from the hin pass a and the Devanagari pass b (b's lines)."""
    A, B = toks(a), toks(b); out = []
    sm = difflib.SequenceMatcher(None, [t for t, _, _ in A], [t for t, _, _ in B], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for t, li, sp in B[j1:j2]:
                out.append((t, li, sp, None if known(t) or compound(t) else 'unknown', []))
        elif op == 'replace' and i2 - i1 == j2 - j1:
            for (ta, _, _), (tb, li, sp) in zip(A[i1:i2], B[j1:j2]):
                if plain(ta) == plain(tb) or (ta in QUOTES and tb in QUOTES):     # the same word, or only the quote's style
                    out.append((plain(tb), li, sp, None if known(tb) or compound(tb) else 'unknown', [])); continue
                pick = tb if known(tb) or not known(ta) else ta
                if not known(ta) and not known(tb) and compound(ta) and not compound(tb): pick = ta
                # one pass reads a real word and the other a non-word: the real word, unflagged (logged as 'chose');
                # both real words (शिवकी / शिवको) or neither: flagged, read by eye
                out.append((pick, li, sp, 'chose' if known(ta) != known(tb) else 'differ', [ta, tb]))
        else:
            sa = ' '.join(t for t, _, _ in A[i1:i2])
            for k, (tb, li, sp) in enumerate(B[j1:j2]): out.append((tb, li, sp, 'differ', [sa] if k == 0 else []))
            if j1 == j2 and sa.strip() and not re.fullmatch(r'[|;:,.\-—`\'"]+', sa.replace(' ', '')):
                li = out[-1][1] if out else 0; out.append(('', li, True, 'only in one pass', [sa]))
    return out

MARK = re.compile(r'॥\s*([०-९]+(?:\s*(?:½|[१1]\s*/\s*[२2]))?(?:\s*[-–—]\s*[०-९]+(?:\s*(?:½|[१1]\s*/\s*[२2]))?)?)\s*॥')   # ॥ ३½ ॥, ॥ १-३½ ॥
DEV = str.maketrans('०१२३४५६७८९', '0123456789')

HEAD = re.compile(r'(शतरुद्र|कोटिरुद्र|उमा|उम्रा|कैलास|वायवीय)\s*संहिता\s*-?\s*(पू|उ)?[^अआ]{0,8}[अआ]\s*[०o]?\s*([०-९]+)')
SAMHITA = {'शतरुद्र': '3', 'कोटिरुद्र': '4', 'उमा': '5', 'उम्रा': '5', 'कैलास': '6', 'वायवीय': '7'}

def running_heads(files, order):
    """{page: adhyāya} from the Kalyan running heads (‘उमासंहिता-अ० १२ ]’), which name the adhyāya the page ends in.
    A head read wrong (not a section, or out of order with its neighbours) is dropped."""
    H = {}
    for f in files:
        P = json.load(open(f, encoding='utf-8'))
        m = HEAD.search(' '.join(c['hin'] for c in P['cols'] if c['side'].endswith('0')).replace('\n', ' '))
        if not m: continue
        s = SAMHITA[m.group(1)] + ('.' + ('1' if m.group(2) == 'पू' else '2') if m.group(1) == 'वायवीय' else '')
        sec = f"{s}.{int(m.group(3).translate(DEV))}"
        if sec in order: H[P['page']] = sec
    pages = sorted(H)
    ok = lambda i, j: order.index(H[pages[i]]) <= order.index(H[pages[j]])
    return {p: H[p] for i, p in enumerate(pages) if (i == 0 or ok(i - 1, i)) and (i == len(pages) - 1 or ok(i, i + 1))}

def digits(m): return re.sub(r'\D', '', m.translate(DEV))

def closings(P, page):
    """A Kalyan adhyāya's closing line (‘॥ इस प्रकार … अध्याय पूर्ण हुआ ॥ १ ॥’) spans both columns, between the column bands,
    so the column passes never read it. Its mark is taken from the whole-page pass and put into the stream after the
    verse mark that stands before it there; the line's words wait for the closing lines' own Hindi (not yet read).
    Returns the closings whose place was not found."""
    full, lost = re.sub(r'\s+', ' ', P['full']), []
    for m in re.finditer(r'पूर्ण\s*हुआ\s*॥\s*([०-९]+)\s*॥', full):
        before = [x for x in MARK.finditer(full[:m.start()]) if 'पूर्ण' not in full[max(0, x.start() - 25):x.start()]]
        want = digits(before[-1].group(1)) if before else None
        at = None
        for i, w in enumerate(page):
            if w['t'] == '॥' and want:
                mk = MARK.search(''.join(x['t'] for x in page[max(0, i - 7):i + 1]))
                if mk and digits(mk.group(1)) == want: at = i
        if at is None and not before: at = -1                       # the page opens with the closing line
        if at is None: lost.append((P['page'], m.group(1))); continue
        w = page[at] if at >= 0 else page[0]
        mark = [dict(w, t=x, sp=True, flag=None, alt=[], closing=True) for x in ('॥', m.group(1), '॥')]
        page[at + 1:at + 1] = mark
    return lost

def main(book, first, upto=None, pages=None):
    files = sorted(glob.glob(os.path.join(HERE, 'ocr', book, 'p*.json')))
    if pages:
        a, b = map(int, pages.split('-')); files = [f for f in files if a <= int(os.path.basename(f)[1:5]) <= b]
    T = textfile.read(os.path.join(HERE, '..', '..', 'text.txt'))
    order = list(dict.fromkeys(x['section'] for x in T))
    ids = {x['id'] for x in T}
    nums = collections.defaultdict(set)
    for x in T:
        if x['n']: nums[x['section']].add(int(x['n']))
    secs = order[order.index(first):(order.index(upto) + 1 if upto else None)]
    # the stream of words, column by column, page by page
    stream, lost, hhpages = [], [], set()
    notes = json.load(open(os.path.join(HERE, f'{book}.notes.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, f'{book}.notes.json')) else {}
    for f in files:
        P = json.load(open(f, encoding='utf-8'))
        page = []; cut = notes.get(str(P['page']), {}).get('cols', {})   # the page's footnotes (notes.py) are no paragraph's
        for c in P['cols']:
            for t, li, sp, fl, alt in merge(c['hin'], c['deva']):
                if c['side'] in cut and li >= cut[c['side']]: continue
                page.append({'t': t, 'page': P['page'], 'side': c['side'], 'line': li, 'sp': sp, 'flag': fl, 'alt': alt})
        if P['layout'] == 'hh': lost += closings(P, page); hhpages.add(P['page'])
        stream += page
    # paragraphs end at a verse mark; a mark that restarts at 1 begins the next adhyāya
    out, flags, chosen = {}, [], []
    si, cur, last, ended, peak = 0, [], 0, 0, 0
    resync = []
    def text(ws):
        out, prev = [], None
        for w in ws:
            if not w['t'] or w.get('closing'): continue
            brk = prev is not None and (w['page'], w['side'], w['line']) != (prev['page'], prev['side'], prev['line'])
            sp = w['sp'] or (brk and not prev['t'].endswith('-'))
            if brk and prev['t'].endswith('-') and out and out[-1].endswith('-') and re.search(r'[\u0900-\u097F]-$', out[-1]): pass
            out.append((' ' if sp else '') + ('⟦' + w['t'] + '⟧' if w['flag'] and w['flag'] != 'chose' else w['t'])); prev = w
        return ''.join(out).strip()
    ordinal = lambda sec: int(sec.split('.')[-1])
    heads = running_heads(files, order)
    def behind(page, sec):          # a running head on this page or the next two names a later adhyāya: the walk missed an end
        h = next((heads[p] for p in (page, page + 1, page + 2) if p in heads), None)
        return h is not None and order.index(h) > order.index(sec)
    for k, w in enumerate(stream):
        cur.append(w)
        m = MARK.search(''.join(x['t'] for x in cur[-8:])) if w['t'] == '॥' else None
        if not m: continue
        rng = [int(re.sub(r'(½|1\s*/\s*2)$', '', x.strip()) or 0) for x in re.split(r'\s*[-–—]\s*', m.group(1).translate(DEV))]
        lo, hi = rng[0], rng[-1]
        sec = secs[si]; top = max(nums[sec] or {1})
        if os.environ.get('WALK'): print('walk', w['page'], m.group(1), sec, top, ended, peak, file=sys.stderr)
        if lo == hi and hi > top + 2 and not ended:                    # a range whose dash was lost (९-१३ read ९१३)
            d = str(hi); nx = str(last + 1)
            if d.startswith(nx) and d[len(nx):] and last + 1 < int(d[len(nx):]) <= top: lo, hi = last + 1, int(d[len(nx):])
        if w.get('closing') and lo == hi and lo != ordinal(sec):        # a printed closing line names its adhyāya: the walk follows it
            pre = sec.rsplit('.', 1)[0] + '.'
            ahead = [j for j in range(si + 1, min(si + 4, len(secs))) if secs[j] == pre + str(lo)]
            behind_ = [j for j in range(max(0, si - 3), si) if secs[j] == pre + str(lo)]
            if ahead or behind_:
                resync.append((w['page'], sec, secs[(ahead or behind_)[0]]))
                if ahead: si = ahead[0]; sec = secs[si]; top = max(nums[sec] or {1}); peak = max(peak, top)
                else: ended = 2; cur = []; continue                       # already past it (a closing read twice)
            elif not ended and peak >= 0.6 * top:                          # its number misread (२१ read २९): it still closes this adhyāya
                resync.append((w['page'], sec, 'closing ' + m.group(1))); ended = 2; cur = []; continue
        if lo == hi == ordinal(sec) and peak >= 0.6 * top and (lo > top or lo <= peak) and ended < 2:   # the adhyāya's two closing lines
            if ended and not w.get('closing') and w['page'] in hhpages:     # Kalyan: the column's own copy of a closing line already
                if cur: cur.pop()                                           # the mark's closing ॥
                for _ in range(4):                                          # … back to its opening ॥
                    if not cur or cur.pop()['t'].startswith('॥'): break
                ended += 1; continue                                        # placed: the words after it (the next heading, the first
                                                                            # words of the next adhyāya in the other column) stay
            ended += 1; cur = []; continue                                  # (इति … and इस प्रकार … पूर्ण हुआ ॥ N ॥)
        if not ended and lo == 1 and (peak >= 0.8 * top or (peak >= 0.3 * top and behind(w['page'], sec))): ended = 1   # a closing line misread: the marks restart anyway
        if not ended and lo != 1 and (hi < last - 3 or hi > top + 2) and not (lo == hi == ordinal(sec)):   # a mark far behind, or beyond the last verse: misread, flagged
            flags.append({'k': None, 'id': f'{sec}.?{hi}', 'page': w['page'], 'side': w['side'], 'line': w['line'], 'word': m.group(0), 'why': 'mark', 'alt': []})
            continue
        if ended:
            if lo > 5: cur = []; continue                                  # the other closing line (a first mark misread: ≤ 5)
            si += 1; ended = 0; last = 0; peak = 0
            if si >= len(secs): break
            sec = secs[si]
        if last == 0 and peak == 0:          # an adhyāya's first paragraph: its title runs across both columns above it; the paragraph
            at = next(((x['page'], x['line']) for x in cur if x['t'] and x['t'].startswith('बोल')), None)   # begins with the speaker
            if at:
                head = [x for x in cur if (x['page'], x['line']) < at]
                cur = [x for x in cur if (x['page'], x['line']) >= at]
                if f'{sec}.0' in ids and head:        # an unnumbered opening (1.1.0): its Hindi stands before the speaker,
                    for x in head: x['flag'] = x['flag'] or 'opening'                  # below the title: every word read by eye
                    out.setdefault(sec, {})[f'{sec}.0'] = {'t': text(head), 'page': head[0]['page'], 'mark': '', 'covers': []}
        vid = f'{sec}.{hi}' if hi in nums[sec] else f'{sec}.?{hi}'          # a mark that is no verse of this adhyāya: flagged
        out.setdefault(sec, {})[vid] = {'t': text(cur), 'page': cur[0]['page'], 'mark': m.group(1), 'covers': list(range(lo, hi + 1))}
        k = 0
        for x in cur:
            if x['flag'] and x['flag'] != 'chose' and x['t']: x['k'] = k; k += 1        # its place among the paragraph's ⟦…⟧
        for x in cur:
            if x['flag']: (chosen if x['flag'] == 'chose' else flags).append({'k': x.get('k'), 'id': vid, 'page': x['page'], 'side': x['side'], 'line': x['line'], 'word': x['t'], 'why': x['flag'], 'alt': x['alt']})
        if vid.split('.')[-1].startswith('?'): flags.append({'id': vid, 'page': cur[0]['page'], 'side': cur[0]['side'], 'line': cur[0]['line'], 'word': m.group(0), 'why': 'mark', 'alt': []})
        last, cur = hi, []; peak = max(peak, hi)
    json.dump(out, open(os.path.join(HERE, f'{book}.merged.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    with open(os.path.join(HERE, f'{book}.flags.jsonl'), 'w', encoding='utf-8') as f:
        for x in flags: f.write(json.dumps(x, ensure_ascii=False) + '\n')
    with open(os.path.join(HERE, f'{book}.chosen.jsonl'), 'w', encoding='utf-8') as f:     # accepted by the one-real-word rule, for audit
        for x in chosen: f.write(json.dumps(x, ensure_ascii=False) + '\n')
    if lost: print('closing lines not placed:', lost)
    if resync: print('the walk set right by a closing line (page, walk, closing):', resync)
    words = sum(1 for w in stream if re.match(r'[ऀ-ॿ]', w['t'] or 'x'))
    missing = [(s, sorted(nums[s] - {n for v in out.get(s, {}).values() for n in v['covers']})) for s in secs[:si + 1]]
    print(f'{book}: {len(files)} pages, {words} words, {len(flags)} flagged ({100 * len(flags) / max(words, 1):.1f}%), adhyāyas reached: {secs[0]} … {secs[min(si, len(secs) - 1)]}')
    for s, mv in missing:
        if mv: print('  ', s, 'verses without a Hindi paragraph mark:', mv[:12], '…' if len(mv) > 12 else '')

if __name__ == '__main__':
    main(*sys.argv[1:])
