"""Kaṭha Upaniṣad (Kṛṣṇa Yajurveda, Kaṭha śākhā): this folder → library/hinduism/veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad/.

The text (text.json) is settled by source/settle.py from the owner's PDF (see README.md and reconciliation.md); check.py
compares it with the Devanagari witnesses. The meanings are written for this library (the owner's instruction for the
Sanskrit texts): concise, faithful, following Śaṅkara's reading, with other readings in footnotes.

Writes   work.json                     the text: śānti mantra, mantras 1.1.1 … 2.3.18, closing śānti
         meanings/hi-scriptures.json   Hindi meaning (meanings/hi.json)
         meanings/en-scriptures.json   English meaning (meanings/en.json)
         glossary.json                 the work's own senses of words whose shared sense doesn't fit here (WORK_SENSES)
Merges   glossary/*.json into library/glossary/sa.json (adds new words; never overwrites existing ones).
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); import jsonio
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'meanings')); import versenum as vnum

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad'

def dump(path, obj):
    path = os.path.join(OUT, path); os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))

items = json.load(open(os.path.join(HERE, 'text.json'), encoding='utf-8'))['items']
VALLI = [('1', '1', 29), ('1', '2', 25), ('1', '3', 17), ('2', '1', 15), ('2', '2', 15), ('2', '3', 18)]
want = ['shanti.1'] + ['%s.%s.%d' % (a, v, m) for a, v, n in VALLI for m in range(1, n + 1)] + ['shanti.2']
assert [x['id'] for x in items] == want, 'text.json is not in the expected order'
for x in items:
    if x['y'] == 'mantra':   # each mantra ends with its number within the vallī
        assert re.search(r'।।%s।।$' % ''.join('०१२३४५६७८९'[int(c)] for c in x['n'].split('.')[-1]), x['v'][-1]), x['id']

ORD = ['प्रथमा', 'द्वितीया', 'तृतीया']
work = {
    'id': 'katha-upanishad',
    'lang': 'sa',
    'title': {'hi': 'कठोपनिषद्', 'en': 'Kaṭha Upaniṣad'},
    'by': {'hi': 'कृष्ण यजुर्वेद, कठ शाखा', 'en': 'Kṛṣṇa Yajurveda, Kaṭha śākhā'},
    'edition': {'hi': 'स्वामी गुरुभक्तानन्द (सन्दीपनी) की पुस्तक; shlokam.org, sanskritdocuments.org', 'en': 'Swami Gurubhaktananda (Sandeepany); shlokam.org, sanskritdocuments.org'},
    'parts': {'name': {'hi': 'अध्याय', 'en': 'Adhyāya'}, 'list': [{'hi': 'प्रथम अध्याय', 'en': 'Adhyāya 1'}, {'hi': 'द्वितीय अध्याय', 'en': 'Adhyāya 2'}]},
    'types': {
        'shanti': {'name': {'hi': 'शान्तिमन्त्र', 'en': 'Śānti Mantra'}, 'short': {'hi': 'शा॰', 'en': 'Śā.'}},
        'mantra': {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},
    },
    'items': items,
    'topics': [
        {'id': 'shanti.1', 'hi': 'शान्तिपाठ', 'en': 'Śānti Pāṭha'},
        {'id': '1.1.1', 'hi': 'प्रथम अध्याय, प्रथमा वल्ली — नचिकेताकी कथा और तीन वर', 'en': 'Adhyāya 1, Vallī 1 — The story of Naciketā and the three boons'},
        {'id': '1.2.1', 'hi': 'प्रथम अध्याय, द्वितीया वल्ली — श्रेय और प्रेय; ॐ; अजर-अमर आत्मा', 'en': 'Adhyāya 1, Vallī 2 — The good and the pleasant; Om; the deathless Self'},
        {'id': '1.3.1', 'hi': 'प्रथम अध्याय, तृतीया वल्ली — रथका रूपक; उठो, जागो', 'en': 'Adhyāya 1, Vallī 3 — The chariot; arise, awake'},
        {'id': '2.1.1', 'hi': 'द्वितीय अध्याय, प्रथमा वल्ली — भीतर देखो; यही वह है', 'en': 'Adhyāya 2, Vallī 1 — Look within; this indeed is that'},
        {'id': '2.2.1', 'hi': 'द्वितीय अध्याय, द्वितीया वल्ली — ग्यारह द्वारोंका नगर; सबका अन्तरात्मा', 'en': 'Adhyāya 2, Vallī 2 — The city of eleven gates; the inner Self of all'},
        {'id': '2.3.1', 'hi': 'द्वितीय अध्याय, तृतीया वल्ली — ऊर्ध्वमूल अश्वत्थ; योग; अमरता', 'en': 'Adhyāya 2, Vallī 3 — The inverted tree; yoga; immortality'},
        {'id': 'shanti.2', 'hi': 'शान्तिपाठ', 'en': 'Śānti Pāṭha'},
    ],
}
dump(WP + '/work.json', work)

ids = {x['id'] for x in items}
def meanings(lang, title):
    M = json.load(open(os.path.join(HERE, 'meanings', lang + '.json'), encoding='utf-8'))
    m = {k: v for k, v in M.items() if not k.startswith('_')}
    assert set(m) == ids, (lang, ids ^ set(m))
    I = {x['id']: x for x in items}   # the verse's number (adhyāya.vallī.mantra) at the end of its meaning, as in the other works
    m = {k: [vnum.with_number(v[0], I[k], lang, by_n=True)] + v[1:] for k, v in m.items()}
    dump(WP + '/meanings/%s-scriptures.json' % lang, {'id': lang + '-scriptures', 'lang': lang, 'order': 1, 'title': title, 'm': m})
    return m
hi = meanings('hi', {'hi': 'भावार्थ — शास्त्र', 'en': 'Hindi meaning — Scriptures'})
en = meanings('en', {'hi': 'अंग्रेज़ी अर्थ — शास्त्र', 'en': 'English meaning — Scriptures'})

# ---- word meanings: every word of the verses must have a meaning ----
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")
SVARA = re.compile('[॑-॔᳐-᳿꣠-꣱]')   # as in tools/site/app.js cleanWord
words = {SVARA.sub('', PUNCT.sub('', t)) for x in items for l in x['v'] for t in l.split()} - {''}
WORK_SENSES = {   # words already in sa.json whose shared sense doesn't fit this text
    'हर': {'hi': 'लाओ (जल ले आओ)', 'en': 'fetch, bring (water)', 'r': 'हृ', 'g': 'लोट् मध्यम पुरुष एकवचन'},
    'परा': {'hi': 'परे, श्रेष्ठ, ऊँची', 'en': 'higher, beyond', 'r': 'परा', 'g': 'प्रथमा एकवचन (स्त्रीलिंग) / प्रथमा बहुवचन (परे, पुल्लिंग)'},
    'प्रथमो': {'hi': 'पहला', 'en': 'the first', 'r': 'प्रथम', 'g': 'प्रथमा एकवचन (प्रथमः)'},
    'विश्वे': {'hi': 'सब', 'en': 'all', 'r': 'विश्व', 'g': 'प्रथमा बहुवचन'},
    'देवा': {'hi': 'देवता (इन्द्रियाँ)', 'en': 'the gods (the senses)', 'r': 'देव', 'g': 'प्रथमा बहुवचन (देवाः)'},
}
dump(WP + '/glossary.json', {'sa': WORK_SENSES})
gp = os.path.join(OUT, 'glossary', 'sa.json'); G = json.load(open(gp))
NEW = {}
for f in sorted(glob.glob(os.path.join(HERE, 'glossary', '*.json'))):
    for k, v in json.load(open(f, encoding='utf-8')).items():
        assert k not in NEW, ('twice in the glossary files:', k)
        NEW[k] = v
assert not [k for k in NEW if SVARA.search(k)], 'glossary keys must not carry svaras'
add_ = {k: v for k, v in NEW.items() if k not in G}
G.update(add_); jsonio.dump_glossary(gp, G)
missing = sorted(w for w in words if w not in G and w not in WORK_SENSES)
unused = sorted(k for k in NEW if k not in words)
print(len(items), 'items;', len(hi), 'hi;', len(en), 'en;', len(words), 'distinct words;', len(add_), 'new words;',
      len(missing), 'words without a meaning;', len(unused), 'unused glossary entries')
if missing: print('missing:', ' '.join(missing))
if unused: print('unused:', ' '.join(unused))
assert not missing
