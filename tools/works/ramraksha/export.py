"""Śrī Rāma Rakṣā Stotram (Budha Kauśika): source/ → library/hinduism/stotra/rama/ramraksha/.

Source of truth for the text: the Vande Guru Paramparaam video (YouTube ZIDdE4SZAuw), whose
on-screen lines (Devanagari · transliteration · English) were transcribed from the owner's
screenshots into source/video_text.tsv (frame number, Devanagari, transliteration, English).
Repeated screenshots of the same line are left out of the file.

Writes   work.json                              the text: invocation, viniyoga, dhyāna, ślokas 1–38, colophon
         meanings/en-vande-guru-paramparaam.json English meaning (the video's on-screen meaning, joined per verse)
         meanings/hi-stuti-chalisa-sangrah.json  Hindi meaning (source/hi_meanings.json, from the owner's PDF of that web page)
Merges   glossary_sa.json into library/glossary/sa.json (adds new words; never overwrites existing ones).
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); import jsonio

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/stotra/rama/ramraksha'

def dump(path, obj):
    path = os.path.join(OUT, path); os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))

# ---- the video's lines ----
rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'source', 'video_text.tsv'), encoding='utf-8') if l.strip()]
DIG = '०१२३४५६७८९'
def deva(s):   # house style shared with the Mānas: ।। (two daṇḍas) and the number inside ।।N।।
    s = s.replace('॥', '।।'); return re.sub(r'\s+', ' ', s).strip()
def tr(s):     # transliteration in the Mānas convention: ṁ for anusvāra, e/o without macron, ',' for the half-line daṇḍa
    s = s.replace('ṃ', 'ṁ').replace('ē', 'e').replace('ō', 'o').replace("'", '’')
    s = re.sub(r'\s*।\s*$', ',', s.strip()); return re.sub(r'\s+', ' ', s).strip()

# ---- group lines into verses ----
# frame 001 the invocation · 002–008 viniyoga · 009 the heading "ध्यानम्" (a topic, not a verse)
# 010–013 the dhyāna verse · 014–108 ślokas 1–38 (a śloka ends with its number) · 109–110 colophon
items, en = [], {}
def add(id, y, n, rs, s=None):
    items.append({'id': id, 'p': 0, 's': s or id, 'y': y, 'n': n, 'v': [deva(r[1]) for r in rs], 't': [tr(r[2]) for r in rs]})
    en[id] = [' '.join(r[3].strip() for r in rs)]
F = {int(r[0]): r for r in rows}
add('mangal', 'mantra', '', [F[1]])
add('viniyoga', 'viniyoga', '', [F[k] for k in range(2, 9)])
add('dhyana', 'dhyana', '', [F[k] for k in range(10, 14)])
buf, num = [], 0
for k in sorted(F):
    if not 14 <= k <= 108: continue
    buf.append(F[k]); m = re.search(r'॥\s*([०-९]+)\s*॥\s*$', F[k][1])
    if m:
        n = int(''.join(str(DIG.index(c)) for c in m.group(1))); num += 1
        assert n == num, ('śloka numbers out of order', k, n, num)
        add('sh%d' % n, 'shloka', str(n), buf); buf = []
assert not buf and num == 38, (num, buf)
add('iti', 'iti', '', [F[109], F[110]])

types = {
    'mantra':   {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},
    'viniyoga': {'name': {'hi': 'विनियोग', 'en': 'Viniyoga'}, 'short': {'hi': 'विनि॰', 'en': 'Vin.'}},
    'dhyana':   {'name': {'hi': 'ध्यान', 'en': 'Dhyāna'}, 'short': {'hi': 'ध्या॰', 'en': 'Dhy.'}},
    'shloka':   {'name': {'hi': 'श्लोक', 'en': 'Śloka'}, 'short': {'hi': 'श्लो॰', 'en': 'Śl.'}},
    'iti':      {'name': {'hi': 'पुष्पिका', 'en': 'Colophon'}, 'short': {'hi': 'इति', 'en': 'Iti'}},
}
work = {
    'id': 'ramraksha',
    'lang': 'sa',
    'title': {'hi': 'श्रीरामरक्षास्तोत्रम्', 'en': 'Śrī Rāma Rakṣā Stotram'},
    'by': {'hi': 'बुधकौशिक ऋषि', 'en': 'Budha Kauśika Ṛṣi'},
    'edition': {'hi': 'वन्दे गुरु परम्पराम्', 'en': 'Vande Guru Paramparaam'},
    'parts': {'name': {'hi': 'पाठ', 'en': 'Pāṭha'}, 'list': [{'hi': 'श्रीरामरक्षास्तोत्रम्', 'en': 'Śrī Rāma Rakṣā Stotram'}]},
    'types': types,
    'items': items,
    'topics': [{'id': 'viniyoga', 'hi': 'विनियोग', 'en': 'Viniyoga'}, {'id': 'dhyana', 'hi': 'ध्यानम्', 'en': 'Dhyānam'},
               {'id': 'sh1', 'hi': 'स्तोत्र', 'en': 'Stotra'}],
}
dump(WP + '/work.json', work)

dump(WP + '/meanings/en-vande-guru-paramparaam.json', {'id': 'en-vande-guru-paramparaam', 'lang': 'en', 'order': 1,
     'title': {'hi': 'वन्दे गुरु परम्पराम् — अंग्रेज़ी अर्थ', 'en': 'Vande Guru Paramparaam — English meaning'}, 'm': en})
H = json.load(open(os.path.join(HERE, 'source', 'hi_meanings.json'), encoding='utf-8'))
hi = {k: [v] for k, v in H.items() if not k.startswith('_')}
assert set(hi) <= {x['id'] for x in items}, set(hi) - {x['id'] for x in items}
dump(WP + '/meanings/hi-stuti-chalisa-sangrah.json', {'id': 'hi-stuti-chalisa-sangrah', 'lang': 'hi', 'order': 1,
     'title': {'hi': 'स्तुति चालीसा संग्रह — हिंदी अर्थ', 'en': 'Stuti Chalisa Sangrah — Hindi meaning'}, 'm': hi})

# ---- word meanings: every word of the verses must be in sa.json ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")
words = {PUNCT.sub('', t) for x in items for l in x['v'] for t in l.split()} - {''}
gp = os.path.join(OUT, 'glossary', 'sa.json'); G = json.load(open(gp))
gf = os.path.join(HERE, 'glossary_sa.json'); NEW = json.load(open(gf)) if os.path.exists(gf) else {}
add_ = {k: v for k, v in NEW.items() if k not in G}
G.update(add_); jsonio.dump_glossary(gp, G)
missing = sorted(w for w in words if w not in G)
print(len(items), 'items;', len(en), 'en;', len(hi), 'hi;', len(add_), 'new words;', len(missing), 'words still without a meaning')
if missing: print(' '.join(missing))
