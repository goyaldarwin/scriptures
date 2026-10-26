"""Sukhmani Sahib (Guru Arjan Dev Ji) → library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/.

Inputs (all in this folder; see README.md):
  source/lines.json        the PDF's printed lines (extract.py): legacy Gurmukhi, transliteration, English
  gurmukhi.py              legacy font encoding → Unicode Gurmukhi;  structure.py: lines → items
  meanings/hi.json, en.json, pa.json   our Hindi, English and Punjabi meaning of every item, written for this library
  glossary/pa.json         Gurmukhi word meanings
Writes
  work.json                         the text (Gurmukhi verse lines + the PDF's transliteration), 24 Ashtapadis as
                                    parts, two topics per Ashtapadi, the work's verse types
  meanings/en-sant-singh-khalsa.json  the PDF's English (Dr. Sant Singh Khalsa), the lines of an item joined (order 2)
  meanings/hi-scriptures.json       the Hindi meaning (written for this library; the PDF has none)
  meanings/en-scriptures.json       our English meaning (meanings/en.json, written for this library from the Gurmukhi,
                                    tools/meanings/style.md §12), the default; the PDF's English stays selectable
  meanings/pa-scriptures.json       our Punjabi meaning (meanings/pa.json, line by line), shown in the ਪੰ layer
  Our meanings end with the stanza's number (tools/meanings/versenum.py).
Merges glossary/pa.json into library/glossary/pa.json (adds new words, never overwrites) and reports how many of
the work's words have a meaning. Does not touch library/index.json. Then run tools/site/build.py.
Before exporting it runs the conversion check (check.py) and the structure check, and stops on any failure.
"""
import json, os, re, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(REPO, 'tools'))
import jsonio
from structure import build, check

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'sikhism/gurbani/guru-arjan-dev/sukhmani-sahib'
WORK = 'sukhmani-sahib'
LANG = 'pa'

subprocess.run([sys.executable, os.path.join(HERE, 'check.py')], check=True, stdout=subprocess.DEVNULL)
items = build(); check(items)
ids = [x['id'] for x in items]

DEVD = '०१२३४५६७८९'


def num_hi(n): return ''.join(DEVD[int(d)] for d in str(n))


def gur2dev(s):
    """Gurmukhi → Devanagari, letter for letter (for topic names shown in the Hindi interface)."""
    s = re.sub(r'ੱ(.)', lambda m: chr(ord(m.group(1)) - 0x100) + '्' + m.group(1), s)   # addak doubles the next letter
    out = []
    for c in s:
        o = ord(c)
        if c == 'ੰ': out.append('ं')
        elif c == 'ੵ': out.append('्य')
        elif c == 'ੑ': out.append('्ह')
        elif c == 'ੜ': out.append('ड़')
        elif 0x0A00 <= o <= 0x0A7F: out.append(chr(o - 0x100))
        else: out.append(c)
    return ''.join(out)


# ---- types, parts, topics ----
TYPES = {
    'heading': {'name': {'hi': 'शीर्षक', 'en': 'Heading'}},
    'salok':   {'name': {'hi': 'सलोक', 'en': 'Salok'}, 'short': {'hi': 'सलोक', 'en': 'Salok'}},
    'pauri':   {'name': {'hi': 'पउड़ी', 'en': 'Pauri'}, 'short': {'hi': 'पउड़ी', 'en': 'Pauri'}},
    'rahao':   {'name': {'hi': 'रहाउ', 'en': 'Rahao'}, 'short': {'hi': 'रहाउ', 'en': 'Rahao'}},
}
assert {x['y'] for x in items} <= set(TYPES)

parts = {'name': {'hi': 'अष्टपदी', 'en': 'Ashtapadi'},
         'list': [{'hi': 'अष्टपदी ' + num_hi(k), 'en': f'Ashtapadi {k}'} for k in range(1, 25)]}

# Two topics in each Ashtapadi: its Salok and its eight pauris, each named by its first line — the way a passage
# of Gurbani is cited ("ਸਿਮਰਉ ਸਿਮਰਿ ਸਿਮਰਿ ਸੁਖੁ ਪਾਵਉ"). The Hindi name is the line in Devanagari letters, the English
# name the PDF's transliteration of it.
def pratik(x, skip):
    j = next(i for i, l in enumerate(x['v']) if not l.startswith(skip))
    first = re.sub(r'\s*॥.*$', '', x['v'][j])
    tr = re.sub(r'[.\s]+$', '', re.sub(r'\|\|.*$', '', x['t'][j]))
    return {'hi': gur2dev(first), 'en': tr[:1].upper() + tr[1:]}


topics = []
for k in range(24):
    sal = next(x for x in items if x['p'] == k and x['y'] == 'salok')
    p1 = next(x for x in items if x['p'] == k and x['y'] == 'pauri')
    topics.append({'id': sal['id'], **pratik(sal, ('ਸਲੋਕੁ', 'ੴ'))})   # Ashtapadi 1: after the title line
    topics.append({'id': p1['id'], **pratik(p1, ('ਅਸਟਪਦੀ',))})

work = {
    'id': WORK, 'lang': LANG,
    'title': {'hi': 'सुखमनी साहिब', 'en': 'Sukhmani Sahib'},
    'by': {'hi': 'गुरु अर्जन देव जी', 'en': 'Guru Arjan Dev Ji'},
    'edition': {'hi': 'श्री गुरु ग्रन्थ साहिब, अंग २६२–२९६', 'en': 'Sri Guru Granth Sahib, Ang 262–296'},
    'from': {'hi': 'श्री गुरु ग्रन्थ साहिब, अंग २६२–२९६', 'en': 'Sri Guru Granth Sahib, Ang 262–296'},   # under the title on the work's page (by · from)
    'parts': parts,
    'types': TYPES,
    'items': [{k: x[k] for k in ('id', 'p', 's', 'y', 'n', 'v', 't')} for x in items],
    'topics': topics,
}


def dump(rel, obj):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


old = os.path.join(OUT, WP, 'work.json')
if os.path.exists(old): work['sources'] = json.load(open(old)).get('sources', {})
dump(WP + '/work.json', work)

# ---- English: the PDF's translation, copied; only extraction breaks are fixed ----
EN_FIXES = [('obtai n', 'obtain')]   # a word split in the PDF's text layer (see reconciliation.md)
en = {}
for x in items:
    s = ' '.join(x['e'])
    for a, b in EN_FIXES: s = s.replace(a, b)
    en[x['id']] = [re.sub(r'\s+', ' ', s).strip()]
def en_line(l):
    for a_, b_ in EN_FIXES: l = l.replace(a_, b_)
    return re.sub(r'\s+', ' ', l).strip()
# line by line: the PDF prints one English line under each Gurmukhi line, so its pieces are those lines
enp = {x['id']: [en_line(l) for l in x['e']] for x in items if len(x['e']) == len(x['v']) and any(l.strip() for l in x['e'])}
dump(f'{WP}/meanings/en-sant-singh-khalsa.json', {
    'id': 'en-sant-singh-khalsa', 'lang': 'en', 'order': 2,   # ours is the default; this stays selectable
    'title': {'hi': 'अंग्रेज़ी अनुवाद — डॉ. संत सिंह खालसा', 'en': 'English translation — Dr. Sant Singh Khalsa'},
    'm': en, 'p': enp})
print(f'en-sant-singh-khalsa: {len(enp)} of {len(items)} items line by line')

sys.path.insert(0, os.path.join(REPO, 'tools', 'meanings')); import versenum, overlap
BYID = {x['id']: x for x in items}

# ---- Hindi: written for this library ----
hp = os.path.join(HERE, 'meanings', 'hi.json')
HI = json.load(open(hp, encoding='utf-8')) if os.path.exists(hp) else {}
extra = [k for k in HI if k not in ids]; assert not extra, f'hi meanings for unknown items: {extra}'
miss = [i for i in ids if not HI.get(i)]
dump(f'{WP}/meanings/hi-scriptures.json', {
    'id': 'hi-scriptures', 'lang': 'hi', 'order': 1,
    'title': {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'},
    'm': {i: [versenum.text_and_pieces(HI[i], BYID[i], 'hi')[0]] for i in ids if HI.get(i)},
    'p': {i: versenum.text_and_pieces(HI[i], BYID[i], 'hi')[1] for i in ids if HI.get(i) and not isinstance(HI[i], str)}})

# ---- English: ours, written for this library (every item; no overlap with the PDF's; the default) ----
EN = json.load(open(os.path.join(HERE, 'meanings', 'en.json'), encoding='utf-8'))
miss = [i for i in ids if not EN.get(i)]; extra = [k for k in EN if k not in ids]
assert not miss and not extra, f'en meanings: missing {miss[:5]}, unknown {extra[:5]}'
bad = [r for r in overlap.check({k: versenum.joined(v) for k, v in EN.items()}, {k: v[0] for k, v in en.items()}) if len(r[1]) >= 10]
assert not bad, f'en: {bad[0][0]} shares 10+ words with the PDF\'s English: {" ".join(bad[0][1])}'
dump(f'{WP}/meanings/en-scriptures.json', {
    'id': 'en-scriptures', 'lang': 'en', 'order': 1,
    'title': {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'},
    'm': {i: [versenum.text_and_pieces(EN[i], BYID[i], 'en')[0]] for i in ids},
    'p': {i: versenum.text_and_pieces(EN[i], BYID[i], 'en')[1] for i in ids if not isinstance(EN[i], str)}})

# ---- Punjabi: ours, written for this library line by line, shown in the ਪੰ layer ----
# (checked against Prof. Sahib Singh's Darpan and the Faridkot Teeka with tools/meanings/overlap.py while writing; those
# books are private, so the check is not repeated here: style.md §13)
pp = os.path.join(HERE, 'meanings', 'pa.json')
if os.path.exists(pp):
    PA = json.load(open(pp, encoding='utf-8'))
    pmiss = [i for i in ids if not PA.get(i)]; pextra = [k for k in PA if k not in ids]
    assert not pmiss and not pextra, f'pa meanings: missing {pmiss[:5]}, unknown {pextra[:5]}'
    dump(f'{WP}/meanings/pa-scriptures.json', {
        'id': 'pa-scriptures', 'lang': 'pa', 'order': 1,
        'title': {'hi': 'पंजाबी अर्थ — शास्त्र', 'en': 'Punjabi meaning — Scriptures'},
        'm': {i: [versenum.text_and_pieces(PA[i], BYID[i], 'pa')[0]] for i in ids},
        'p': {i: versenum.text_and_pieces(PA[i], BYID[i], 'pa')[1] for i in ids if not isinstance(PA[i], str)}})

# ---- word meanings (Gurmukhi → library/glossary/pa.json, add-only) ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९੦-੯0-9]")   # the app's own rule (tools/site/app.js)
words = {}
for x in items:
    for l in x['v']:
        for t in l.split():
            t = PUNCT.sub('', t)
            if t: words[t] = words.get(t, 0) + 1
gp = os.path.join(OUT, 'glossary', 'pa.json')
G = json.load(open(gp, encoding='utf-8')) if os.path.exists(gp) else {}
mp = os.path.join(HERE, 'glossary', 'pa.json')
mine = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else {}
for k, v in mine.items(): assert v.get('hi') and v.get('en'), f'pa:{k} needs hi and en'
new = {k: v for k, v in mine.items() if k not in G}
G.update(new)
if G: jsonio.dump_glossary(gp, G)
have = [w for w in words if w in G]
print(f'{len(items)} items in 24 Ashtapadis; English {len(en)}/{len(ids)}; Hindi {len(ids) - len(miss)}/{len(ids)}'
      + (f' (missing {miss[:5]}…)' if miss else ''))
print(f'words: {len(have)} of {len(words)} distinct ({sum(words[w] for w in have)} of {sum(words.values())} in the text) '
      f'have a meaning; {len(new)} new in glossary/pa.json')
