"""Settle the Vālmīki Rāmāyaṇa text from the decoded Gita Press book and write text.txt and the copied English.

Inputs: book.json (parse.py), the decided corrections (corrections.final.json). Every change is listed in
reconciliation.md; this script is the only place they are applied.
"""
import json, re, sys, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import english

KANDA = ['bala', 'ayodhya', 'aranya', 'kishkindha', 'sundara', 'yuddha', 'uttara']
KANDA_NAME = {'bala': ('बालकाण्ड', 'Bal Kand'), 'ayodhya': ('अयोध्याकाण्ड', 'Ayodhya Kand'),   # English in plain spelling (docs/PLAYBOOK.md §6)
              'aranya': ('अरण्यकाण्ड', 'Aranya Kand'), 'kishkindha': ('किष्किन्धाकाण्ड', 'Kishkindha Kand'),
              'sundara': ('सुन्दरकाण्ड', 'Sundar Kand'), 'yuddha': ('युद्धकाण्ड', 'Yuddh Kand'),
              'uttara': ('उत्तरकाण्ड', 'Uttar Kand')}
DEV = str.maketrans('0123456789', '०१२३४५६७८९')

# The book misnumbers three verses (the sequence and, in two, the English marks settle them).
NUMBER_FIX = {('yuddha', 17, 63, 2): 64, ('yuddha', 61, 25, 2): 26, ('uttara', 20, 22, 2): 23}
# The book prints no Sanskrit for Sundara 1.154 (its English is printed); IIT Kanpur's 5.1.155 is the verse
# (its रामशासनात् is the English's "At the command of Śrī Rāma"; valmikiramayan.net has रामकारणात्).
INSERT = {('sundara', 1, 153): ['तस्याः सकाशं दूतोऽहं गमिष्ये रामशासनात्।', 'कर्तुमर्हसि रामस्य साह्यं विषयवासिनि॥ १५४॥']}
# Printing slips found by the decoder's well-formedness check, confirmed on the page image.
PRINT_FIX = [('bala', 'मुक्तपुष्पावकीेर्णेन', 'मुक्तपुष्पावकीर्णेन'), ('bala', 'जगााम', 'जगाम'),
             ('yuddha', 'भु्ङ्क्ते', 'भुङ्क्ते')]

def sarga_key(kanda, i, s):
    """the sarga's id: its number, or p1/p2 for the later additions (प्रक्षिप्त), counted in the kāṇḍa"""
    return s['_key']

def number_sargas(k):
    n = 0; p = 0
    for s in k['sargas']:
        if 'प्रक्षिप्त' in s['heading']:
            p += 1; s['_key'] = f'p{p}'; s['_label'] = (f'प्रक्षिप्त सर्ग {p}', f'Interpolated sarga {p}')   # as work.json → sections
        else:
            n += 1; s['_key'] = str(n); s['_label'] = None

def clean_last(line, n):
    """the verse's last line ends with its number, written ॥N॥ (the book's slips ॥॥४०, ॥ 4॥, विना९॥, ॥ ६८ mended)"""
    t = re.sub(r'[\s॥।]*[०-९0-9]+[\s॥]*$', '', line).rstrip()
    t = re.sub(r'[॥।\s]+$', '', t)
    return t + '॥ ' + str(n).translate(DEV) + '॥'

def settle(book, corrections):
    items, log = [], []
    corr = collections.defaultdict(list)
    for c in corrections:
        corr[c['id']].append(c)
    for k in book:
        kd = k['kanda']; number_sargas(k)
        part = KANDA.index(kd)
        for pos, s in enumerate(k['sargas'], 1):
            seen = collections.Counter()
            verses = []
            for v in s['verses']:
                seen[v['n']] += 1
                n = NUMBER_FIX.get((kd, int(s['_key']) if s['_key'].isdigit() else s['_key'], v['n'], seen[v['n']]), v['n'])
                if n != v['n']:
                    log.append(f"{kd}.{s['_key']}: the book's second verse numbered {v['n']} is {n}")
                verses.append({'n': n, 'lines': list(v['lines']), 'page': v['page']})
                ins = INSERT.get((kd, int(s['_key']) if s['_key'].isdigit() else -1, n))
                if ins:
                    verses.append({'n': n + 1, 'lines': ins, 'page': v['page'], 'filled': True})
                    log.append(f"{kd}.{s['_key']}.{n + 1}: filled from IIT Kanpur (not printed in the book)")
            for v in verses:
                vid = f"{kd}.{s['_key']}.{v['n']}"
                lines = v['lines'][:-1] + [clean_last(v['lines'][-1], v['n'])]
                text = '\n'.join(lines)
                for kk, a, b in PRINT_FIX:
                    if kk == kd and a in text:
                        text = text.replace(a, b); log.append(f'{vid}: {a} → {b} (print slip)')
                for c in corr.get(f"{kd}.{pos}.{v['n']}", []):   # review ids count sargas by position (a later addition included)
                    c['real_id'] = vid
                    if c['from'] not in text and c['to'] in text:
                        continue          # already mended above (PRINT_FIX)
                    if text.count(c['from']) != 1:
                        raise SystemExit(f"{vid}: correction anchor {c['from']!r} found {text.count(c['from'])} times")
                    text = text.replace(c['from'], c['to'])
                lines = text.split('\n')
                items.append({'id': vid, 'p': part, 's': f"{kd}.{s['_key']}", 'y': 'shloka', 'n': str(v['n']),
                              'v': lines, 'page': v['page']})
    return items, log

def english_meanings(book, items):
    """{verse id: text}: Gita Press's English under the last verse of its range, the printed mark kept."""
    ids = {i['id'] for i in items}
    texts = [e['text'] for k in book for s in k['sargas'] for e in s['en']]
    fix = english.hyphen_rule([english.convert(t) for t in texts])
    m = {}
    for k in book:
        for s in k['sargas']:
            for e in s['en']:
                if e['to'] is None:
                    continue          # a stray word after the last mark
                t = fix(english.convert(e['text']))
                t = ' '.join(t.split())
                mark = english.convert(e['printed']) or (f'({e["from"]}-{e["to"]})' if e['from'] != e['to'] else f'({e["to"]})')
                vid = f"{k['kanda']}.{s['_key']}.{e['to']}"
                if vid not in ids:
                    raise SystemExit(f'English for {vid}: no such verse')
                m[vid] = (t + ' ' + mark).strip()
    return m

if __name__ == '__main__':
    book = json.load(open(sys.argv[1]))
    corrections = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else []
    items, log = settle(book, corrections)
    en = english_meanings(book, items)
    json.dump({'items': items, 'log': log}, open(sys.argv[3], 'w'), ensure_ascii=False)
    missing = [c['id'] for c in corrections if 'real_id' not in c]
    if missing:
        raise SystemExit(f'corrections not applied: {missing}')
    json.dump(corrections, open(sys.argv[2].replace('.json', '.applied.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(en, open(sys.argv[4], 'w'), ensure_ascii=False)
    print(len(items), 'verses;', len(en), 'English meanings;', len(log), 'logged changes')
    print('\n'.join(log[:20]))
