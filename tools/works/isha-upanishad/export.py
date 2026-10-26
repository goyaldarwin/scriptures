"""Īśāvāsya Upaniṣad (Śukla Yajurveda, Kāṇva Saṃhitā 40): this folder → library/hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/.

Source of truth for the text: the owner's printout of shlokam.org/text/isha-upanishad.htm (scriptures-data:
<path>/printouts/shlokam/isha-upanishad.pdf), settled in text.json; its corrections are in reconciliation.md
and check.py verifies text.json against the printout. The meanings are written for this library (the owner's
instruction for the Sanskrit texts): concise, faithful, following Śaṅkara's reading, with other readings in footnotes.

Writes   work.json                     the text: śānti mantra and mantras 1–18
         meanings/hi-scriptures.json   Hindi meaning (meanings/hi.json)
         meanings/en-scriptures.json   English meaning (meanings/en.json)
         glossary.json                 the work's own senses of words whose shared sense doesn't fit here (WORK_SENSES)
Merges   glossary_sa.json into library/glossary/sa.json (adds new words; never overwrites existing ones).
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); import jsonio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'meanings')); import versenum as vnum

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad'

def dump(path, obj):
    path = os.path.join(OUT, path); os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))

T = json.load(open(os.path.join(HERE, 'text.json'), encoding='utf-8'))['items']
items = [{'id': x['id'], 'p': 0, 's': x['id'], 'y': x['y'], 'n': x['n'], 'v': x['v'], 't': x['t']} for x in T]
assert [x['id'] for x in items] == ['shanti.1'] + ['m%02d' % n for n in range(1, 19)]
for x in items[1:]:   # each mantra ends with its own number
    assert re.search(r'।।%s।।$' % ''.join('०१२३४५६७८९'[int(c)] for c in x['n']), x['v'][-1]), x['id']

work = {
    'id': 'isha-upanishad',
    'lang': 'sa',
    'title': {'hi': 'ईशावास्योपनिषद्', 'en': 'Īśāvāsya Upaniṣad'},
    'by': {'hi': 'शुक्ल यजुर्वेद, काण्व संहिता — अध्याय ४०', 'en': 'Śukla Yajurveda, Kāṇva Saṃhitā — chapter 40'},
    'edition': {'hi': 'shlokam.org', 'en': 'shlokam.org'},
    'parts': {'name': {'hi': 'उपनिषद्', 'en': 'Upaniṣad'}, 'list': [{'hi': 'ईशावास्योपनिषद्', 'en': 'Īśāvāsya Upaniṣad'}]},
    'types': {
        'shanti': {'name': {'hi': 'शान्तिमन्त्र', 'en': 'Śānti Mantra'}, 'short': {'hi': 'शा॰', 'en': 'Śā.'}},
        'mantra': {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},
    },
    'items': items,
    # the printout's sections (Verses 1-2, 3-8, 9-14, 15-18), with the śānti mantra before them
    'topics': [{'id': 'shanti.1', 'hi': 'शान्तिपाठ', 'en': 'Śānti Pāṭha'},
               {'id': 'm01', 'hi': 'ईश्वरसे व्याप्त जगत् और त्याग', 'en': 'The Lord-pervaded world and renunciation'},
               {'id': 'm03', 'hi': 'आत्माका स्वरूप', 'en': 'The nature of the Self'},
               {'id': 'm09', 'hi': 'विद्या और अविद्या, सम्भूति और असम्भूति', 'en': 'Vidyā and avidyā, sambhūti and asambhūti'},
               {'id': 'm15', 'hi': 'अन्तकालकी प्रार्थनाएँ', 'en': 'Prayers at life’s end'}],
}
dump(WP + '/work.json', work)

ids = {x['id'] for x in items}
def meanings(lang, title):
    M = json.load(open(os.path.join(HERE, 'meanings', lang + '.json'), encoding='utf-8'))
    m = {k: v for k, v in M.items() if not k.startswith('_')}
    assert set(m) == ids, (lang, ids ^ set(m))
    I = {x['id']: x for x in items}   # the verse's number at the end of its meaning, as in the other works
    m = {k: [vnum.with_number(v[0], I[k], lang)] + v[1:] for k, v in m.items()}
    dump(WP + '/meanings/%s-scriptures.json' % lang, {'id': lang + '-scriptures', 'lang': lang, 'order': 1, 'title': title, 'm': m})
    return m
hi = meanings('hi', {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'})
en = meanings('en', {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'})

# ---- word meanings: every word of the verses must have a meaning ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")
SVARA = re.compile('[॑-॔᳐-᳿꣠-꣱]')   # as in tools/site/app.js cleanWord
words = {SVARA.sub('', PUNCT.sub('', t)) for x in items for l in x['v'] for t in l.split()} - {''}
WORK_SENSES = {   # words already in sa.json whose shared sense doesn't fit this text
    'कृतं': {'hi': 'जो किया गया, किये हुए कर्म', 'en': 'what has been done, one’s deeds', 'r': 'कृत', 'g': 'द्वितीया एकवचन'},
    'देव': {'hi': 'हे देव', 'en': 'O god', 'r': 'देव', 'g': 'सम्बोधन एकवचन'},
}
dump(WP + '/glossary.json', {'sa': WORK_SENSES})
gp = os.path.join(OUT, 'glossary', 'sa.json'); G = json.load(open(gp))
NEW = json.load(open(os.path.join(HERE, 'glossary_sa.json'), encoding='utf-8'))
assert not [k for k in NEW if SVARA.search(k)], 'glossary keys must not carry svaras'
add_ = {k: v for k, v in NEW.items() if k not in G}
G.update(add_); jsonio.dump_glossary(gp, G)
missing = sorted(w for w in words if w not in G and w not in WORK_SENSES)
unused = sorted(k for k in NEW if k not in words)
print(len(items), 'items;', len(hi), 'hi;', len(en), 'en;', len(words), 'distinct words;', len(add_), 'new words;',
      len(missing), 'words without a meaning;', len(unused), 'unused glossary entries')
if missing: print('missing:', ' '.join(missing))
if unused: print('unused:', ' '.join(unused))
