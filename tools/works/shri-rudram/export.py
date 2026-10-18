"""Śrī Rudram (Namakam and Chamakam): tools/works/shri-rudram/ → library/hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/.

Source of truth for the text: the owner's printouts (PDF) of shlokam.org's two pages (rudram-namakam.htm,
rudram-chamakam.htm), settled in text.json by source/extract.py + source/settle.py (see reconciliation.md).
The meanings are our own, written for this library (meanings/namakam.json, chamakam.json).

Writes   work.json                     the text: opening, Namakam anuvākas 1–11, closing; Chamakam anuvākas 1–11, śānti
         meanings/en-scriptures.json   English meaning, one per mantra (with footnotes)
         meanings/hi-scriptures.json   Hindi meaning, one per mantra (with footnotes)
         glossary.json                 this work's own senses (glossary/work_sa.json)
Merges   glossary/g*.json into library/glossary/sa.json (adds new words; never overwrites existing ones).
Does not touch library/index.json (the shelf is edited by hand) or audio/ (see tools/audio).
Then run tools/site/build.py.
"""
import glob, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); import jsonio

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'library')
WP = 'hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram'

def dump(path, obj):
    path = os.path.join(OUT, path); os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))

items = json.load(open(os.path.join(HERE, 'text.json'), encoding='utf-8'))

ORD = ['प्रथम', 'द्वितीय', 'तृतीय', 'चतुर्थ', 'पञ्चम', 'षष्ठ', 'सप्तम', 'अष्टम', 'नवम', 'दशम', 'एकादश']
types = {
    'mangala': {'name': {'hi': 'मङ्गल मन्त्र', 'en': 'Maṅgala mantra'}, 'short': {'hi': 'मङ्ग॰', 'en': 'Maṅg.'}},
    'shirsha': {'name': {'hi': 'शीर्षक', 'en': 'Heading'}, 'short': {'hi': 'शी॰', 'en': 'Hd.'}},
    'mantra':  {'name': {'hi': 'मन्त्र', 'en': 'Mantra'}, 'short': {'hi': 'मं॰', 'en': 'Man.'}},
    'uttara':  {'name': {'hi': 'उत्तर मन्त्र', 'en': 'Closing mantra'}, 'short': {'hi': 'उ॰', 'en': 'Cl.'}},
    'shanti':  {'name': {'hi': 'शान्ति मन्त्र', 'en': 'Śānti mantra'}, 'short': {'hi': 'शा॰', 'en': 'Śā.'}},
}
# one topic per anuvāka (with its theme), plus the opening and closing
THEME_N = [('धनुष-बाण शान्त हों', 'Rudra’s bow and arrows made gracious'),
           ('सबके स्वामी', 'Lord of all: armies, trees, paths, fields'),
           ('चोरों-डाकुओंमें भी वही', 'Present even in thieves and robbers'),
           ('गण, शिल्पी और शिकारी', 'Hosts, craftsmen and hunters'),
           ('रुद्रके नाम और रूप', 'Rudra’s own names and forms'),
           ('ज्येष्ठ-कनिष्ठ, सर्वत्र', 'Eldest and youngest, everywhere'),
           ('जल, मेघ और घरमें', 'In waters, clouds and dwellings'),
           ('नमः शिवाय', 'Namaḥ Śivāya'),
           ('भूमि, घर और देवहृदय', 'In the earth, the home and the gods’ hearts'),
           ('रक्षा और कृपाकी प्रार्थना', 'Prayer for protection and grace'),
           ('सब रुद्रोंके धनुष दूर', 'The bows of all the Rudras laid away')]
THEME_C = [('प्राण, इन्द्रियाँ और शरीर', 'Life, senses and body'),
           ('प्रतिष्ठा, सत्य और समृद्धि', 'Standing, truth and growth'),
           ('सुख, कल्याण और अभय', 'Happiness, welfare and fearlessness'),
           ('अन्न और धान्य', 'Food and grains'),
           ('पृथ्वीकी सम्पदा', 'The wealth of the earth'),
           ('इन्द्रके साथ देवता', 'The gods together with Indra'),
           ('सोमयागके ग्रह', 'The soma cups'),
           ('यज्ञकी सामग्री', 'The things of the sacrifice'),
           ('महायज्ञ और वेद', 'The great rites and the Vedas'),
           ('पशुधन और प्राण यज्ञमें', 'Cattle, and life offered in the yajña'),
           ('संख्याएँ और लोकोंके स्वामी', 'The numbers, and the lords of the worlds')]
topics = [{'id': 'namakam.purva.guru', 'hi': 'अथ श्रीरुद्रप्रश्नः — मङ्गलाचरण', 'en': 'Śrī Rudra Praśna — the opening'}]
for a, (h, e) in enumerate(THEME_N, 1):
    topics.append({'id': 'namakam.a%02d.m01' % a, 'hi': '%s अनुवाक — %s' % (ORD[a - 1], h), 'en': 'Anuvāka %d — %s' % (a, e)})
    if a == 1: topics.append({'id': 'namakam.bhagavan.namaste', 'hi': 'नमस्ते अस्तु भगवन्', 'en': 'Namaste astu bhagavan'})
topics.append({'id': 'namakam.uttara.u1', 'hi': 'उत्तर मन्त्र और शान्ति', 'en': 'Closing mantras and śānti'})
for a, (h, e) in enumerate(THEME_C, 1):
    topics.append({'id': 'chamakam.a%02d.m01' % a, 'hi': '%s अनुवाक — %s' % (ORD[a - 1], h), 'en': 'Anuvāka %d — %s' % (a, e)})
topics.append({'id': 'chamakam.shanti.shanti', 'hi': 'शान्ति मन्त्र', 'en': 'Śānti mantra'})
ids = {x['id'] for x in items}; assert all(t['id'] in ids for t in topics)

work = {
    'id': 'shri-rudram',
    'lang': 'sa',
    'title': {'hi': 'श्रीरुद्रम्', 'en': 'Śrī Rudram'},
    'by': {'hi': 'कृष्ण यजुर्वेद, तैत्तिरीय संहिता ४.५ और ४.७', 'en': 'Kṛṣṇa Yajurveda, Taittirīya Saṃhitā 4.5 and 4.7'},
    'edition': {'hi': 'श्लोकम् (shlokam.org)', 'en': 'Shlokam (shlokam.org)'},
    'parts': {'name': {'hi': 'भाग', 'en': 'Part'}, 'list': [{'hi': 'नमकम्', 'en': 'Namakam'}, {'hi': 'चमकम्', 'en': 'Chamakam'}]},
    'types': types,
    'items': [{k: x[k] for k in ('id', 'p', 's', 'y', 'n', 'v', 't')} for x in items],
    'topics': topics,
}
dump(WP + '/work.json', work)

# ---- meanings: our own, one per item ----
M = {}
for f in ('namakam', 'chamakam'):
    d = json.load(open(os.path.join(HERE, 'meanings', f + '.json'), encoding='utf-8')); d.pop('_', None); M.update(d)
assert set(M) == ids, (ids - set(M), set(M) - ids)
def layer(lang):
    out = {}
    for x in items:
        e = M[x['id']]; f = e.get('f' + lang)
        out[x['id']] = [e[lang], f] if f else [e[lang]]
    return out
dump(WP + '/meanings/en-scriptures.json', {'id': 'en-scriptures', 'lang': 'en', 'order': 1,
     'title': {'hi': 'शास्त्र — अंग्रेज़ी अर्थ', 'en': 'Scriptures — English meaning'}, 'm': layer('en')})
dump(WP + '/meanings/hi-scriptures.json', {'id': 'hi-scriptures', 'lang': 'hi', 'order': 1,
     'title': {'hi': 'शास्त्र — हिंदी अर्थ', 'en': 'Scriptures — Hindi meaning'}, 'm': layer('hi')})

# ---- word meanings ----
W = json.load(open(os.path.join(HERE, 'glossary', 'work_sa.json'), encoding='utf-8')); W.pop('_', None)
dump(WP + '/glossary.json', {'sa': W})
PUNCT = re.compile(r"[।॥|,.;:!?\-—‘’“”'\"()\[\]०-९0-9]")
SVARA = re.compile('[॑-॔᳐-᳿꣠-꣱]')     # the app ignores these when looking a word up
clean = lambda w: unicodedata.normalize('NFC', SVARA.sub('', PUNCT.sub('', w)))
words = {clean(t) for x in items for l in x['v'] for t in l.split()} - {''}
gp = os.path.join(OUT, 'glossary', 'sa.json'); G = json.load(open(gp))
NEW = {}
for f in sorted(glob.glob(os.path.join(HERE, 'glossary', 'g*.json'))): NEW.update(json.load(open(f, encoding='utf-8')))
assert all(k == clean(k) for k in NEW), [k for k in NEW if k != clean(k)]
add = {k: v for k, v in NEW.items() if k not in G}
G.update(add); jsonio.dump_glossary(gp, G)
missing = sorted(w for w in words if w not in G and w not in W)
print(len(items), 'items;', len(M), 'meanings (en + hi);', len(add), 'new words;', len(missing), 'words still without a meaning')
if missing: print(' '.join(missing))
