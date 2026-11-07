"""The Hindi of a scan's OCR (ocr/<book>/p<NNNN>.json, by ocr.py), merged and checked, per verse, with every doubtful word
flagged for reading by eye on the page image (hindi/README.md).

    python3 merge.py <book> <first adhyāya section> [<pages>]      e.g.  merge.py shiv-1 m.1 13-199

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
    for li, line in enumerate(unicodedata.normalize('NFC', text).replace('।।', '॥').splitlines()):
        line = re.sub(r'^[|;:`„)\]\s]+(?=\S)', '', line)                  # the column rule's marks at a line's start
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

MARK = re.compile(r'॥\s*([०-९]+(?:\s*[-–—]\s*[०-९]+)?)\s*॥')
DEV = str.maketrans('०१२३४५६७८९', '0123456789')

def main(book, first, pages=None):
    files = sorted(glob.glob(os.path.join(HERE, 'ocr', book, 'p*.json')))
    if pages:
        a, b = map(int, pages.split('-')); files = [f for f in files if a <= int(os.path.basename(f)[1:5]) <= b]
    T = textfile.read(os.path.join(HERE, '..', '..', 'text.txt'))
    order = list(dict.fromkeys(x['section'] for x in T))
    nums = collections.defaultdict(set)
    for x in T:
        if x['n']: nums[x['section']].add(int(x['n']))
    secs = order[order.index(first):]
    # the stream of words, column by column, page by page
    stream = []
    for f in files:
        P = json.load(open(f, encoding='utf-8'))
        for c in P['cols']:
            for t, li, sp, fl, alt in merge(c['hin'], c['deva']):
                stream.append({'t': t, 'page': P['page'], 'side': c['side'], 'line': li, 'sp': sp, 'flag': fl, 'alt': alt})
    # paragraphs end at a verse mark; a mark that restarts at 1 begins the next adhyāya
    out, flags, chosen = {}, [], []
    si, cur, last, ended = 0, [], 0, 0
    text = lambda ws: ''.join((' ' if w['sp'] else '') + ('⟦' + w['t'] + '⟧' if w['flag'] and w['flag'] != 'chose' else w['t']) for w in ws if w['t']).strip()
    ordinal = lambda sec: int(sec.split('.')[-1])
    for k, w in enumerate(stream):
        cur.append(w)
        m = MARK.search(''.join(x['t'] for x in cur[-8:])) if w['t'] == '॥' else None
        if not m: continue
        rng = [int(x) for x in re.split(r'\s*[-–—]\s*', m.group(1).translate(DEV))]
        lo, hi = rng[0], rng[-1]
        sec = secs[si]; top = max(nums[sec] or {1})
        if lo == hi == ordinal(sec) and last >= 0.6 * top and lo < last and ended < 2:   # the adhyāya's two closing lines
            ended += 1; cur = []; continue                                  # (इति … and इस प्रकार … पूर्ण हुआ ॥ N ॥)
        if ended:
            if lo != 1: cur = []; continue
            si += 1; ended = 0; last = 0
            if si >= len(secs): break
            sec = secs[si]
        vid = f'{sec}.{hi}' if hi in nums[sec] else f'{sec}.?{hi}'          # a mark that is no verse of this adhyāya: flagged
        out.setdefault(sec, {})[vid] = {'t': text(cur), 'page': cur[0]['page'], 'mark': m.group(1), 'covers': list(range(lo, hi + 1))}
        for x in cur:
            if x['flag']: (chosen if x['flag'] == 'chose' else flags).append({'id': vid, 'page': x['page'], 'side': x['side'], 'line': x['line'], 'word': x['t'], 'why': x['flag'], 'alt': x['alt']})
        if vid.split('.')[-1].startswith('?'): flags.append({'id': vid, 'page': cur[0]['page'], 'side': cur[0]['side'], 'line': cur[0]['line'], 'word': m.group(0), 'why': 'mark', 'alt': []})
        last, cur = hi, []
    json.dump(out, open(os.path.join(HERE, f'{book}.merged.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    with open(os.path.join(HERE, f'{book}.flags.jsonl'), 'w', encoding='utf-8') as f:
        for x in flags: f.write(json.dumps(x, ensure_ascii=False) + '\n')
    with open(os.path.join(HERE, f'{book}.chosen.jsonl'), 'w', encoding='utf-8') as f:     # accepted by the one-real-word rule, for audit
        for x in chosen: f.write(json.dumps(x, ensure_ascii=False) + '\n')
    words = sum(1 for w in stream if re.match(r'[ऀ-ॿ]', w['t'] or 'x'))
    missing = [(s, sorted(nums[s] - {n for v in out.get(s, {}).values() for n in v['covers']})) for s in secs[:si + 1]]
    print(f'{book}: {len(files)} pages, {words} words, {len(flags)} flagged ({100 * len(flags) / max(words, 1):.1f}%), adhyāyas reached: {secs[0]} … {secs[min(si, len(secs) - 1)]}')
    for s, mv in missing:
        if mv: print('  ', s, 'verses without a Hindi paragraph mark:', mv[:12], '…' if len(mv) > 12 else '')

if __name__ == '__main__':
    main(*sys.argv[1:])
