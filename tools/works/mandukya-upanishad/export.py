"""Māṇḍūkya Upaniṣad (Atharvaveda): this folder → library/hinduism/veda/atharvaveda/upanishad/mandukya-upanishad/.

Source of truth for the text: the owner's printout of sanskritdocuments.org/doc_upanishhat/maandu.html, settled in
text.txt; the śānti mantra as SMVedroad chants it and as the owner's second printout (freepressjournal.in, NJ Reddy)
gives it. Every change is in reconciliation.md. The meanings are written for this library (the owner's instruction
for the Sanskrit texts): concise, faithful, following Śaṅkara's reading, with other context in footnotes.

Writes   work.json                     the text: śānti mantra, mantras 1–12, the closing words
         meanings/hi-scriptures.json   Hindi meaning (meanings/hi.json)
         meanings/en-scriptures.json   English meaning (meanings/en.json)
         glossary.json                 the work's own senses of words whose shared sense doesn't fit here (WORK_SENSES)
Merges   glossary_sa.json into library/glossary/sa.json (adds new words; never overwrites existing ones).
Checks   every item has both meanings and every word a meaning; it stops otherwise.
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(HERE, '..', '..')); import jsonio

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/veda/atharvaveda/upanishad/mandukya-upanishad'

def dump(path, obj):
    return jsonio.dump_library(OUT, path, obj)

items = []
for raw in open(os.path.join(HERE, 'text.txt'), encoding='utf-8'):
    line = raw.strip()
    if not line or line.startswith('#'): continue
    m = re.fullmatch(r'\[(\S+) (\w+)(?: (\d+))?\]', line)
    if m:
        items.append({'id': m.group(1), 'p': 0, 's': m.group(1), 'y': m.group(2), 'n': m.group(3) or '', 'v': []}); continue
    items[-1]['v'].append(line)
assert [x['id'] for x in items] == ['shanti.1'] + ['m%02d' % n for n in range(1, 13)] + ['iti']
for x in items:   # each mantra ends with its own number
    if x['y'] == 'mantra': assert re.search(r'॥%s॥$' % ''.join('०१२३४५६७८९'[int(c)] for c in x['n']), x['v'][-1]), x['id']

work = {
    'id': 'mandukya-upanishad',
    'lang': 'sa',
    'title': {'hi': 'माण्डूक्योपनिषद्', 'en': 'Māṇḍūkya Upaniṣad'},
    'by': {'hi': 'अथर्ववेद', 'en': 'Atharvaveda'},
    'edition': {'hi': 'sanskritdocuments.org', 'en': 'sanskritdocuments.org'},
    'parts': {'name': {'hi': 'उपनिषद्', 'en': 'Upaniṣad'}, 'list': [{'hi': 'माण्डूक्योपनिषद्', 'en': 'Māṇḍūkya Upaniṣad'}]},
    'types': {
        'shanti': {'name': {'hi': 'शान्तिमन्त्र', 'en': 'Śānti Mantra'}, 'short': {'hi': 'शा॰', 'en': 'Śā.'}},
        'mantra': {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},
        'iti': {'name': {'hi': 'समापन (पुष्पिका)', 'en': 'Closing words (iti)'}, 'short': {'hi': 'इति', 'en': 'Iti'}},
    },
    'items': items,
    'topics': [{'id': 'shanti.1', 'hi': 'शान्तिपाठ', 'en': 'Śānti Pāṭha'},
               {'id': 'm01', 'hi': 'ओंकार ही सब कुछ; आत्मा ही ब्रह्म', 'en': 'Om is all; the Self is Brahman'},
               {'id': 'm03', 'hi': 'आत्माके चार पाद', 'en': 'The four quarters of the Self'},
               {'id': 'm08', 'hi': 'ओंकारकी मात्राएँ और पाद', 'en': 'The sounds of Om and the quarters'},
               {'id': 'm12', 'hi': 'मात्रारहित चौथा (तुरीय)', 'en': 'The soundless Fourth'}],
    # the four topics are the four khaṇḍas SMVedroad's recording announces (अथ प्रथमः खण्डः … इति चतुर्थः खण्डः)
}
old = os.path.join(OUT, WP, 'work.json')   # keep the sources list that build.py registered
if os.path.exists(old): work['sources'] = json.load(open(old)).get('sources', {})
dump(WP + '/work.json', work)

ids = {x['id'] for x in items}
def meanings(lang, title):
    M = json.load(open(os.path.join(HERE, 'meanings', lang + '.json'), encoding='utf-8'))
    m = {k: v for k, v in M.items() if not k.startswith('_')}
    assert set(m) == ids, (lang, ids ^ set(m))
    m = {k: (v if v[1] else v[:1]) for k, v in m.items()}   # no empty footnote list
    dump(WP + '/meanings/%s-scriptures.json' % lang, {'id': lang + '-scriptures', 'lang': lang, 'order': 1, 'title': title, 'm': m})
    return m
hi = meanings('hi', {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'})
en = meanings('en', {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'})

# ---- word meanings: every word of the verses must have a meaning ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")
SVARA = re.compile('[॑-॔᳐-᳿꣠-꣱]')   # as in tools/site/app.js cleanWord
words = {SVARA.sub('', PUNCT.sub('', t)) for x in items for l in x['v'] for t in l.split()} - {''}
WORK_SENSES = {   # words already in sa.json whose shared sense doesn't fit this text
    'न': {'hi': 'नहीं; शान्तिपाठमें (स्वस्ति न इन्द्रो): हमारे लिये (नः)', 'en': 'not; in the śānti pāṭha (svasti na indro): for us (naḥ)', 'g': 'अव्यय / सर्वनाम (नः, संधिमें)'},
    'देवा': {'hi': 'हे देवो!', 'en': 'O gods!', 'r': 'देव', 'g': 'सम्बोधन बहुवचन (देवाः, संधिमें)'},
    'य': {'hi': 'जो', 'en': 'whoever', 'r': 'यद्', 'g': 'सर्वनाम, प्रथमा एकवचन (यः, संधिमें)'},
}
dump(WP + '/glossary.json', {'sa': WORK_SENSES})
gp = os.path.join(OUT, 'glossary', 'sa.json'); G = json.load(open(gp))
NEW = json.load(open(os.path.join(HERE, 'glossary_sa.json'), encoding='utf-8'))
assert not [k for k in NEW if SVARA.search(k)], 'glossary keys must not carry svaras'
for k, v in NEW.items(): assert v.get('hi') and v.get('en'), f'{k} needs hi and en'
add_ = {k: v for k, v in NEW.items() if k not in G}
G.update(add_); jsonio.dump_glossary(gp, G)
missing = sorted(w for w in words if w not in G and w not in WORK_SENSES)
unused = sorted(k for k in NEW if k not in words)
print(len(items), 'items;', len(words), 'distinct words;', len(add_), 'new words')
assert not missing and not unused, f'words without a meaning: {missing}; unused glossary entries: {unused}'
