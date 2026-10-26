"""Śrī Rudram: source/<part>_raw.json (the printout's blocks) → ../text.txt (the settled text, one verse per mantra,
with the parts, the sections and our topic headings).

The Devanagari is the page's own, with the PDF text layer's breaks mended (rudram_text.norm_deva) and the
corrections below, each checked against the page image and the page's own transliteration
(see ../reconciliation.md). The transliteration is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py shri-rudram)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
from rudram_text import norm_deva, tr2deva, key, SV

# ---- corrections: (block, wrong, right); each must occur exactly once in that block's text ----
# Most restore a reph (र्) that the text layer drops but the page image and the transliteration show,
# or letters lost where the text layer breaks a line inside a word.
FIX = {'namakam': [
    (12, 'प्रमुंच धन्वनस्त्वमुभयोरार\nनियोज्याम् ।\nयाश्च ते हस्त इषवः परा ता भगवो वप ।',
         'प्रमु॑ञ्च॒ धन्व॑न॒स्त्वमु॒भयो॒रार्त्नि॑यो॒र्ज्याम् ।\nयाश्च॑ ते॒ हस्त॒ इष॑वः॒ परा॒ ता भ॑गवो वप ॥'),
    (19, 'नमो॑ म॒न्त\nणे॑ वाणि॒जाय॒', 'नमो॑ म॒न्त्रिणे॑ वाणि॒जाय॒'),
    (21, 'क॒मारे᳚भ्यश्च', 'क॒र्मारे᳚भ्यश्च'),
    (22, 'नमः॑ श॒वाय॑', 'नमः॑ श॒र्वाय॑'),
    (26, 'पणश॒द्या॑य', 'पर्णश॒द्या॑य'),
    (27, 'मा भेमा-ऽरो॒', 'मा भेर्मा-ऽरो॒'),
    (29, 'अ॒स\nन्नना॑तुरम्', 'अ॒स्मिन्नना॑तुरम्'),
    (31, 'म्प्रि\nया मा', 'म्प्रि॒या मा'),
    (40, 'अ॒स\nन्म॑ह॒त्य॑र्ण॒वें᳚', 'अ॒स्मिन्म॑ह॒त्य॑र्ण॒वें᳚'),
    (40, 'श्श॒वा अ॒धः', 'श्श॒र्वा अ॒धः'),
    (42, 'ती॒थानि॑', 'ती॒र्थानि॑'),
    (42, 'वाँतो॑ व॒र्\nष॒मिष॑व॒स्तेभ्यो॒ दश॒ प्राची॒दश॑ दक्षि॒णा दश॑ प्र॒तीची॒-दशो-दी॑ची॒-\nदशो॒ध्वास्तेभ्यो॒ नम॒स्ते',
         'वाँतो॑\nव॒र्ष॒मिष॑व॒स्तेभ्यो॒ दश॒ प्राची॒र्दश॑ दक्षि॒णा दश॑ प्र॒तीची॒-र्दशो-दी॑ची॒-र्दशो॒र्ध्वास्तेभ्यो॒\nनम॒स्ते'),
    (42, 'जम्भे॑\nदधामि॥ ११॥', 'जम्भे॑ दधामि ॥ ११॥'),
    (43, 'मृत्यो॑मुक्षीय', 'मृत्यो॑र्मुक्षीय'),
    (44, 'यो रु॒द्रो अ॒ग्नौ यो अ॒प्सु य ओष॑धीषु॒ यो रु॒द्रो विश्वा॒ भुव॑ना वि॒वेश॒ तस्म\nरु॒द्राय॒ नमो॑ अस्तु ।',
         'यो रु॒द्रो अ॒ग्नौ यो अ॒प्सु य ओष॑धीषु॒\nयो रु॒द्रो विश्वा॒ भुव॑ना वि॒वेश॒ तस्मै॑ रु॒द्राय॒ नमो॑ अस्तु ।'),
], 'chamakam': [
    (0, 'स॒जोष॑से॒माव॑धन्तु', 'स॒जोष॑से॒माव॑र्धन्तु'),
    (0, 'द्यु॒म्नैवाजे॑भि॒राग॑तम्', 'द्यु॒म्नैर्वाजे॑भि॒राग॑तम्'),
    (2, 'ध॒ता च॑', 'ध॒र्ता च॑'),
    (2, 'दीघायु॒त्व', 'दीर्घायु॒त्व'),
    (3, 'पू॒ण-ञ्च॑ मे पू॒णत॑र', 'पू॒र्ण-ञ्च॑ मे पू॒र्णत॑र'),
    (5, 'मू॒धा च॑', 'मू॒र्धा च॑'),
    (5, 'त्वष्ठा॑', 'त्वष्टा॑'),
    (7, 'हवि॒धान॑', 'हवि॒र्धान॑'),
    (8, 'घ॒मश्च॑ मे॒-ऽकश्च॑', 'घ॒र्मश्च॑ मे॒-ऽर्कश्च॑'),
    (9, 'त्र्य॒वीच॑ मे', 'त्र्य॒वी च॑ मे'),
    (10, 'त्रय॑स\nग्ंशच्च', 'त्रय॑स्त्रिग्ंशच्च'),
    (10, 'मू॒धा च॒', 'मू॒र्धा च॒'),
    (11, 'देव॒हू-मनु॑यज्ञ॒नी-बृह॒स्पति॑', 'देव॒हू-र्मनु॑र्यज्ञ॒नी-र्बृह॒स्पति॑'),
    (11, 'पृथि॑विमात॒मा', 'पृथि॑विमात॒र्मा'),
    (11, 'हिग्ंसी॒मधु॑', 'हिग्ंसी॒र्मधु॑'),
]}

def blocks(part):
    B = json.load(open(os.path.join(HERE, part + '_raw.json'), encoding='utf-8'))
    out = ['\n'.join(norm_deva(v) for v in b['v']) for b in B]
    for bi, a, b in FIX[part]:
        assert out[bi].count(a) == 1, (part, bi, a, out[bi])
        out[bi] = out[bi].replace(a, b)
    return [x.split('\n') for x in out], B

def house(l):
    """The page's daṇḍas as the library writes them: ॥, the number inside without spaces (॥११॥)."""
    l = re.sub(r'\s*॥\s*([०-९]+)\s*॥', r' ॥\1॥', l)
    l = re.sub(r'\s*॥(?![०-९])(?<![०-९]॥)', ' ॥', l)
    return l.strip()

# ---- items ----
def item(part, sec, key_, y, n, lines, p):
    v = [house(l) for l in lines if l.strip()]
    return {'id': '%s.%s.%s' % (part, sec, key_), 'p': p, 's': '%s-%s' % (part[:3], sec), 'y': y, 'n': n,
            'v': v}

def namakam():
    L, B = blocks('namakam'); I = []; P = 0
    I.append(item('namakam', 'purva', 'guru', 'mangala', '1', L[0][:1], P))
    I.append(item('namakam', 'purva', 'ganapati', 'mangala', '2', L[0][1:], P))
    I.append(item('namakam', 'purva', 'samhita', 'shirsha', '', L[1], P))
    I.append(item('namakam', 'purva', 'rudraya', 'mangala', '3', L[2], P))
    for k, bi in enumerate(range(3, 18), 1): I.append(item('namakam', 'a01', 'm%02d' % k, 'mantra', '1.%d' % k, L[bi], P))
    # "श्री शम्भवे नमः" (L[18][:1]) is printed in the source but not recited: left out, as the owner asked
    I.append(item('namakam', 'bhagavan', 'namaste', 'mangala', '4', L[18][1:], P))
    for a, bi in zip(range(2, 10), range(19, 27)):
        for k, l in enumerate(L[bi], 1): I.append(item('namakam', 'a%02d' % a, 'm%02d' % k, 'mantra', '%d.%d' % (a, k), [l], P))
    for k, bi in enumerate(range(27, 39), 1): I.append(item('namakam', 'a10', 'm%02d' % k, 'mantra', '10.%d' % k, L[bi], P))
    g = [L[39], L[40], L[41]] + [[l] for l in L[42][:6]] + [L[42][6:]]
    for k, ls in enumerate(g, 1): I.append(item('namakam', 'a11', 'm%02d' % k, 'mantra', '11.%d' % k, ls, P))
    b = L[44]; g = [L[43], b[0:2], b[2:3], b[3:4], b[4:6], b[6:8], b[8:9], b[9:13]]
    for k, ls in enumerate(g, 1): I.append(item('namakam', 'uttara', 'u%d' % k, 'uttara', str(k), ls, P))
    I.append(item('namakam', 'uttara', 'shanti', 'shanti', '', L[45], P))
    return I, B

def chamakam():
    L, B = blocks('chamakam'); I = []; P = 1
    for a in range(1, 12):
        ls = L[a - 1]; g = [ls[:2]] + [[l] for l in ls[2:]] if a == 1 else [[l] for l in ls]
        for k, x in enumerate(g, 1): I.append(item('chamakam', 'a%02d' % a, 'm%02d' % k, 'mantra', '%d.%d' % (a, k), x, P))
    I.append(item('chamakam', 'shanti', 'shanti', 'shanti', '', L[11], P))
    return I, B

if __name__ == '__main__':
    N, BN = namakam(); C, BC = chamakam()
    items = N + C
    ids = [x['id'] for x in items]; assert len(ids) == len(set(ids))
    # misprints in the printout itself (its own transliteration has them too), corrected by item (reconciliation.md)
    ITEM_FIX = {'namakam.a03.m12': [('नमो-ऽस्स॑द्भ्यो॒ विद्य॑द्भ्यश्च', 'नमो-ऽस्य॑द्भ्यो॒ विध्य॑द्भ्यश्च')],
                'chamakam.a08.m02': [('दिष्णि॑याश्च', 'धिष्णि॑याश्च')]}
    for x in items:
        for a_, b_ in ITEM_FIX.get(x['id'], []):
            assert sum(l.count(a_) for l in x['v']) == 1, (x['id'], a_)
            x['v'] = [l.replace(a_, b_) for l in x['v']]
    # a line the recording does not recite, left out at the owner's word (reconciliation.md): u8 begins at प्राणानां
    DROP_LINE = {'namakam.uttara.u8': 'ओ-न्नमो भगवते रुद्राय विष्णवे मृत्यु॑र्मे पा॒हि ॥'}
    for x in items:
        if x['id'] in DROP_LINE:
            assert x['v'].count(DROP_LINE[x['id']]) == 1, (x['id'], x['v'])
            x['v'].remove(DROP_LINE[x['id']])
    # the closing mantras of the Namakam in the order the recording sings them (the owner: "the ending verses
    # are jumbled up and don't match the order in the recording"): Shlokam's recording sings u1 u2 u6 u7 u8 and then
    # u3 u4 u5 (तमु ष्टुहि, यक्ष्वामहे, अयं मे हस्तो) before the śānti; the printout lists u3–u5 after u2. The ids stay; the
    # printed numbers follow the recording's order. Recorded in reconciliation.md.
    ORDER_FIX = {'namakam.uttara.u8': ['namakam.uttara.u3', 'namakam.uttara.u4', 'namakam.uttara.u5']}
    for after, moved in ORDER_FIX.items():
        mv = [next(x for x in items if x['id'] == m) for m in moved]
        items = [x for x in items if x['id'] not in moved]
        k = next(i for i, x in enumerate(items) if x['id'] == after) + 1
        items[k:k] = mv
    ut = [x for x in items if x['id'].startswith('namakam.uttara.u')]
    for k, x in enumerate(ut, 1): x['n'] = str(k)
    assert [x['id'][-2:] for x in ut] == ['u1', 'u2', 'u6', 'u7', 'u8', 'u3', 'u4', 'u5']
    ORD = ['प्रथम', 'द्वितीय', 'तृतीय', 'चतुर्थ', 'पञ्चम', 'षष्ठ', 'सप्तम', 'अष्टम', 'नवम', 'दशम', 'एकादश']
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
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, topics, ['namakam', 'chamakam'], 'sa', [
        'Śrī Rudram (Namakam and Chamakam), shlokam.org. Made by source/settle.py from the owner\'s printouts; do not edit',
        'here. Every correction and choice: reconciliation.md.'])
    print(len(N), 'Namakam items,', len(C), 'Chamakam items')
