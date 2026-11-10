"""The six volumes read by epub.py (v1.json … v6.json in the working folder) → text.txt, meanings/hi/gitapress.json and
check.md (every adhyāya checked against the book's own numbers and counts). See README.md, "How it is made".

    python3 make_text.py <this work's folder>        (run in the folder that holds v1.json … v6.json)

Items, in the book's order, per adhyāya (section <parva>.<adhyāya>):
  <p>.<a>.<n>        a numbered verse or prose passage (shloka, gadya); n as printed (॥ १६½ ॥ → 16½)
  <p>.<a>.<n>d<k>    the k-th dākṣiṇātya (southern) verse after verse n (0: before the first), unnumbered (dshloka, dgadya)
  <p>.<a>.0          the opening verse of a parva (नारायणं नमस्कृत्य …), unnumbered (mangalacharan)
  <p>.<a>.iti        the closing words (iti)
A closing piece of a parva with no adhyāya number (श्रवण-महिमा, the Bhārata-śravaṇa-vidhi, the Mahābhārata-māhātmya)
is a section of its own, <p>.<name>.
The Hindi: each paragraph sits under the last verse its mark names (॥ ९—११ ॥ under 11), else under the last verse before
it; a paragraph printed before its verse has ended (the verse runs on: ॥ ८½ ॥) joins the next one, every mark kept as
printed. The notes (१. … *, …) go under the meaning that carries their mark, or under the meaning of the verse whose
line carries it.
"""
import json, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..'))
import textfile, jsonio

DEV = str.maketrans('०१२३४५६७८९', '0123456789')
def asc(n): return n.translate(DEV)
PARVAS = ['आदिपर्व', 'सभापर्व', 'वनपर्व', 'विराटपर्व', 'उद्योगपर्व', 'भीष्मपर्व', 'द्रोणपर्व', 'कर्णपर्व', 'शल्यपर्व',
          'सौप्तिकपर्व', 'स्त्रीपर्व', 'शान्तिपर्व', 'अनुशासनपर्व', 'आश्वमेधिकपर्व', 'आश्रमवासिकपर्व', 'मौसलपर्व',
          'महाप्रस्थानिकपर्व', 'स्वर्गारोहणपर्व']
END = re.compile(r'\s*॥\s*([०-९]+½?)\s*॥\s*$')
MARK = re.compile(r'॥\s*([^॥]*?)\s*॥\s*$')
COR = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'corrections.json')) else {}
UPA_EN = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'upaparva_en.tsv'), encoding='utf-8') if l.strip())

V = '\u093e-\u094c\u0962\u0963'
def syllables(l):
    """Akṣaras in a line: each vowel, written or inherent (a consonant not followed by a virāma)."""
    return len(re.findall(r'[\u0905-\u0914]|[\u0915-\u0939\u0958-\u095f]\u093c?(?!\u094d)', l))

def slokas(lines):
    """How many ślokas the book counts in these lines: an anuṣṭubh half-verse (about 16 akṣaras) is ½, a longer metre's
    pāda (11–12) ¼; a speaker's line counts nothing."""
    n = 0
    for l in lines:
        if re.search(r'(उवाच|ऊचुः|ऊचतुः)$', l.strip()): continue
        a = syllables(re.sub(r'॥.*$|[।॥]', '', l)); n += 0.5 if a >= 14 else 0.25
    return n

def fmt(line):
    return END.sub(lambda m: ' ॥' + m.group(1) + '॥', line)

def marknums(t):
    """The verse numbers a Hindi paragraph's closing mark names: ॥ ९—११ ॥ → [9, 10, 11]; ॥ ८½ ॥ → [8]; ॥ ॥ → []."""
    m = MARK.search(t)
    if not m: return None, []
    nums = [int(x) for x in re.findall(r'\d+', asc(m.group(1)))]
    if len(nums) == 2 and re.search(r'[-—–]', m.group(1)) and nums[0] < nums[1] < nums[0] + 60: nums = list(range(nums[0], nums[1] + 1))
    return m.group(1), nums

def renumber(blocks, sec, report, stats):
    """The book's slips in verse numbers, put right where its own sequence and Hindi settle them (reconciliation.md):
    a number that breaks the run while its neighbours keep it (… १२, ५३, १४ … → 13); a verse printed without its
    number (a bare ॥ between n and n+2) whose Hindi names n+1. Every change is reported."""
    num = [(i, int(asc(b['n']).replace('½', ''))) for i, b in enumerate(blocks) if b.get('end') == 'n']
    for j, (i, n) in enumerate(num):
        prev = num[j - 1][1] if j else 0
        nxt = num[j + 1][1] if j + 1 < len(num) else None
        if n != prev + 1 and nxt == prev + 2:
            b = blocks[i]; new = str(prev + 1)
            report.append(f'- {sec}.{new}: printed ॥ {b["n"]} ॥, between {prev} and {nxt}: corrected to {new}')
            b['n'] = new; b['lines'][-1] = END.sub(' ॥' + new.translate(str.maketrans('0123456789', '०१२३४५६७८९')) + '॥', b['lines'][-1])
            num[j] = (i, prev + 1); stats['number_fixed'] += 1
    for (i, a), (k, b2) in zip(num, num[1:]):
        if b2 <= a + 1: continue
        mid = [x for x in range(i + 1, k) if blocks[x].get('kind') in ('v', 'g')]
        if len(mid) >= 1 and len(mid) == b2 - a - 1 and all(blocks[x].get('end') == 'bare' and not blocks[x].get('paren') for x in mid):
            for j, x in enumerate(mid):   # a run printed without numbers that fills the gap exactly (a list of names)
                b = blocks[x]; new = str(a + 1 + j)
                report.append(f'- {sec}.{new}: printed without its number, in a run of {len(mid)} between {a} and {b2}: numbered {new}')
                b['end'] = 'n'; b['n'] = new; b['dak'] = False
                b['lines'][-1] = re.sub(r'\s*॥\s*$', '', b['lines'][-1]) + ' ॥' + new.translate(str.maketrans('0123456789', '०१२३४५६७८९')) + '॥'
                stats['number_restored'] += 1
            continue
        if b2 != a + 2 or len(mid) != 1 or blocks[mid[0]].get('end') != 'bare': continue
        para = next((blocks[x] for x in range(mid[0] + 1, len(blocks)) if blocks[x].get('kind') == 'para' and not blocks[x]['open']), None)
        nums = marknums(para['t'])[1] if para else []
        if nums and nums[-1] == a + 1:
            b = blocks[mid[0]]; new = str(a + 1)
            report.append(f'- {sec}.{new}: printed without its number (its Hindi ends ॥ {marknums(para["t"])[0]} ॥): numbered {new}')
            b['end'] = 'n'; b['n'] = new; b['dak'] = False
            b['lines'][-1] = re.sub(r'\s*॥\s*$', '', b['lines'][-1]) + ' ॥' + new.translate(str.maketrans('0123456789', '०१२३४५६७८९')) + '॥'
            stats['number_restored'] += 1

def main(out):
    vols = [json.load(open(f'v{k}.json', encoding='utf-8')) for k in range(1, 7)]
    parvas = [p for v in vols for p in v['parvas']]
    assert [p['name'] for p in parvas] == PARVAS, [p['name'] for p in parvas]
    items, topics, mean, notes = [], [], {}, {}
    report, stats = [], Counter()
    for pi, P in enumerate(parvas):
        pk = str(pi + 1)
        for ai, A in enumerate(P['adh']):
            ex = A.get('extra')
            if ex:   # a closing piece that only repeats verses printed before it (Drona's श्रवण-महिमा) is left out
                done = {re.sub(r'\s*॥.*', '', l).strip(' ।') for B2 in P['adh'] if not B2.get('extra') for b in B2['blocks'] if b.get('kind') in ('v', 'g') for l in b['lines']}
                mine = [re.sub(r'\s*॥.*', '', l).strip(' ।') for b in A['blocks'] if b.get('kind') in ('v', 'g') for l in b['lines']]
                if mine and all(l in done for l in mine):
                    report.append(f'- {pk}.{ex}: "{A["title"]}" repeats verses printed before it: left out'); stats['repeat_left_out'] += 1; continue
                sec = f'{pk}.{ex}'
            else:
                if A['n'] != ai + 1: report.append(f'- {pk}.{ai + 1}: the closing words number it {A["n"]}')
                sec = f'{pk}.{ai + 1}'
            renumber(A['blocks'], sec, report, stats)
            sec_items = []; last_n = '0'; dk = 0; cover = []; pend = None; target_of = {}; seen = set(); last_tid = None; ahead = []
            def add(it):
                nonlocal dk
                if it['id'] in seen:   # a number the book prints twice in one adhyāya
                    report.append(f'- {it["id"]}: the book prints this number twice'); stats['dup_number'] += 1
                    k2 = 2
                    while f'{it["id"]}.{k2}' in seen: k2 += 1
                    it['id'] = f'{it["id"]}.{k2}'
                seen.add(it['id'])
                it.update(p=pi, s=sec); items.append(it); sec_items.append(it); cover.append(it)
            def place(para):
                """A Hindi paragraph (with any held before it) under its verse."""
                nonlocal cover, pend, last_tid, ahead
                text = para['t']; nts = list(para['notes'])
                if pend: text = pend['t'] + ' ' + text; nts = pend['notes'] + nts; pend = None
                raw, nums = marknums(text)
                if not cover:
                    if last_tid:   # a second paragraph on the same verses
                        mean[last_tid] += ' ' + text; notes.setdefault(last_tid, []).extend(' '.join(n['note']) for n in nts if n['note'])
                        stats['para_joined_prev'] += 1; return
                    report.append(f'- {sec}: a Hindi paragraph before any verse: {text[:80]}'); return
                num = [c for c in cover if c.get('n') and int(re.sub(r'½', '', c['n'])) == nums[-1]] if nums else []
                tgt = num[-1] if num else cover[-1]
                if nums and not num: stats['mark_not_in_cover'] += 1; report.append(f'- {tgt["id"]}: its Hindi ends ॥ {raw} ॥')
                tid = tgt['id']
                if tid in mean: mean[tid] += ' ' + text
                else: mean[tid] = text
                for c in cover: target_of[c['id']] = tid
                for c in cover:   # the notes of the verse lines this meaning covers
                    for n in c.pop('_notes', []):
                        if n['note']: notes.setdefault(tid, []).append(' '.join(n['note']))
                for n in nts:
                    if n['note']: notes.setdefault(tid, []).append(' '.join(n['note']))
                if ahead: notes.setdefault(tid, []).extend(ahead); ahead = []
                cover = []; last_tid = tid
            first = True
            for b in A['blocks']:
                k = b['kind']
                if k == 'head': stats['heads'] += 1; continue
                if k == 'para' and re.match(r'सम्बन्ध\s*—', b['t']):   # the Gītā's link to the verse that follows: a note on it
                    ahead.append(b['t']); stats['sambandha'] += 1; continue
                if k == 'para':
                    if b['open']: pend = {'t': (pend['t'] + ' ' if pend else '') + b['t'], 'notes': (pend['notes'] if pend else []) + b['notes']}; stats['para_runs_on'] += 1
                    else: place(b)
                    continue
                lines = [re.sub(r'\s+', ' ', l).strip() for l in b['lines'] if l.strip()]
                if b.get('end') == 'n':
                    n = asc(b['n']); y = 'gadya' if k == 'g' else 'shloka'
                    vid = f'{sec}.{n.replace("½", "h")}'; last_n = n.replace('½', 'h'); dk = 0
                    it = dict(id=vid, y=y, n=n, v=[fmt(l) for l in lines])
                elif b.get('end') == 'invocation':
                    it = dict(id=f'{sec}.om', y='mangalacharan', n='', v=lines); stats['mangala'] += 1
                elif first and not sec_items and lines and lines[0].startswith('नारायणं नमस्कृत्य'):
                    it = dict(id=f'{sec}.0', y='mangalacharan', n='', v=lines); stats['mangala'] += 1
                elif ex:   # the closing pieces' unnumbered verses: numbered by place
                    dk += 1; it = dict(id=f'{sec}.u{dk}', y='shloka', n='', v=lines); stats['extra_unnumbered'] += 1
                else:
                    dk += 1; it = dict(id=f'{sec}.{last_n}d{dk}', y='dgadya' if k == 'g' else 'dshloka', n='', v=lines)
                    stats['dak_' + b['end']] += 1
                if any(re.search(r'[\u0900-\u097f]:', l) for l in it['v']):   # an ASCII colon typed for the visarga
                    report.append(f'- {it["id"]}: “:” for the visarga ः'); stats['visarga_colon'] += 1
                    it['v'] = [re.sub(r'(?<=[\u0900-\u097f]):', 'ः', l) for l in it['v']]
                it['_notes'] = b.get('notes', [])
                for old, new, why in COR.get(it['id'], []):
                    assert any(old in l for l in it['v']), (it['id'], old)
                    it['v'] = [l.replace(old, new) for l in it['v']]
                add(it); first = False
                if first is False and len(sec_items) == 1:
                    title = A['title'] or ''
                    if A.get('sub'): title = f'({A["sub"]}) {title}'
                    en = UPA_EN[A['upaparva'] or P['name']]
                    en = f'{en} · Adhyay {ai + 1}' if not ex else {'mahima': 'The merit of hearing', 'vidhi': 'How to hear the Mahabharat', 'mahatmya': 'The glory of the Mahabharat'}[ex]
                    topics.append(dict(id=it['id'], hi=re.sub(r'\s+', ' ', title).strip(), en=en))
            if pend:   # a paragraph that runs on, with no paragraph after it in the adhyāya: under the verses before it
                report.append(f'- {sec}: a Hindi paragraph runs on to the end: {pend["t"][-60:]}'); place(dict(t='', notes=[]))
            if cover:
                stats['verses_without_meaning'] += len(cover)
                for c in cover: report.append(f'- {c["id"]}: no Hindi after it')
            for c in sec_items: c.pop('_notes', None)
            if A['iti']:
                col = fmt(A['iti']['t']); iid = f'{sec}.iti'
                it = dict(id=iid, y='iti', n='', v=[col]); add(it); it.pop('_notes', None)
                if A['iti_hi']: mean[iid] = A['iti_hi']['t']
            elif not ex: report.append(f'- {sec}: no closing words')
            # the dākṣiṇātya count the book prints under the adhyāya
            nd = 2 * sum(slokas(c['v']) for c in sec_items if c['y'] in ('dshloka', 'dgadya'))
            if A['daknote']:
                W = {'आधा': 0.5, 'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4, 'पाँच': 5}
                m = re.search(r'पा[ठव](?:के|का|क)\s*([०-९]*|आधा|एक|दो|तीन|चार|पाँच)\s*(½?)\s*श्लोक', A['daknote'])
                want = ((W.get(m.group(1)) or (int(asc(m.group(1))) if m.group(1) else 0)) + (0.5 if m.group(2) else 0)) if m else None
                stats['daknotes'] += 1
                if want is None or abs(nd / 2 - want) > max(1, want * 0.15): report.append(f'- {sec}: the book counts {want} dākṣiṇātya ślokas ({A["daknote"]}); the text has {nd} lines ({nd / 2:g} ślokas)'); stats['daknote_off'] += 1
                else: stats['daknote_ok'] += 1
            elif nd: report.append(f'- {sec}: {nd} dākṣiṇātya lines, and the book prints no count'); stats['dak_no_note'] += 1
            nums = [int(c['n'].replace('½', '')) for c in sec_items if c.get('n')]
            if nums and nums != list(range(1, len(nums) + 1)):
                gaps = [(x, y) for x, y in zip([0] + nums, nums) if y != x + 1]
                report.append(f'- {sec}: the verse numbers jump {gaps[:6]}'); stats['number_jumps'] += 1
    ids = [x['id'] for x in items]
    assert len(ids) == len(set(ids))
    assert not [k for k in notes if k not in mean]
    part_keys = [str(i + 1) for i in range(18)]
    textfile.write(os.path.join(out, 'text.txt'), items, topics, part_keys, 'sa', [
        'Mahābhārata: made by source/make_text.py from the owner\'s Gita Press e-books (codes 32–37, read by source/epub.py);',
        'change it there, not here. Every correction and choice: reconciliation.md.'])
    M = {"about": "Gita Press, Mahābhārata with simple Hindi translation (codes 32–37), read from the e-books' Unicode text (source/epub.py); each paragraph sits under the last verse its mark names, a paragraph printed before its verse has ended (॥ ८½ ॥) joined to the next, every mark kept as printed; the book's notes under the meaning that carries their mark",
         "title": {"hi": "गीताप्रेस — हिंदी अर्थ", "en": "Gita Press — Hindi meaning"}, "order": 1, "copied": True,
         "m": {k: mean[k] for k in ids if k in mean}, "notes": {k: notes[k] for k in ids if k in notes}}
    os.makedirs(os.path.join(out, 'meanings', 'hi'), exist_ok=True)
    jsonio.dump_meanings(os.path.join(out, 'meanings', 'hi', 'gitapress.json'), M)
    ty = Counter(x['y'] for x in items)
    head = [f'# What the checks found', '', f'{len(items):,} items: ' + ', '.join(f'{k} {v:,}' for k, v in ty.most_common()),
            f'{len(M["m"]):,} meanings, {sum(len(v) for v in M["notes"].values()):,} notes, {len(topics):,} topics.', '',
            'Counts: ' + ', '.join(f'{k} {v:,}' for k, v in sorted(stats.items())), '', '## Places to read', '']
    open(os.path.join(out, 'source', 'check.md'), 'w', encoding='utf-8').write('\n'.join(head + report) + '\n')
    print(len(items), 'items', dict(ty), len(M['m']), 'meanings', len(topics), 'topics'); print(dict(stats)); print(len(report), 'report lines')

if __name__ == '__main__':
    main(sys.argv[1])
