"""Chāndogya Upaniṣad: source/chandogya_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text, one
verse per mantra, with the parts, the sections and our topic headings).

The Devanagari is the page's own. Each block is split into mantras at the page's ॥ a.k.m ॥ marks (four blocks hold
two or three mantras); the page's adhyāya headings (॥ प्रथमोऽध्यायः ॥) and its closing lines (॥ इति प्रथमः खण्डः ॥,
॥ इति प्रथमोऽध्यायः ॥) are left out, and a mantra ends with its own number (॥१॥). The page's transliteration is read
back into Devanagari and compared with the Devanagari, block by block, as a second witness of it; the corrections
below are each recorded in ../reconciliation.md. The transliteration of the text is made by the exporter.
Run: python3 settle.py   (then python3 tools/works/export.py chandogya-upanishad)
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile

DIG = '०१२३४५६७८९'
def num(s): return int(s.translate(str.maketrans(DIG, '0123456789')))
def deva(n): return str(n).translate(str.maketrans('0123456789', DIG))

# ---- the page's transliteration as a witness of its own Devanagari ----
V = [('ai', 'ऐ', 'ै'), ('au', 'औ', 'ौ'), ('ā', 'आ', 'ा'), ('ī', 'ई', 'ी'), ('ū', 'ऊ', 'ू'), ('ṝ', 'ॠ', 'ॄ'), ('ṛ', 'ऋ', 'ृ'),
     ('ḷ', 'ऌ', 'ॢ'), ('e', 'ए', 'े'), ('o', 'ओ', 'ो'), ('a', 'अ', ''), ('i', 'इ', 'ि'), ('u', 'उ', 'ु')]
C = [('kh', 'ख'), ('k', 'क'), ('gh', 'घ'), ('g', 'ग'), ('ṅ', 'ङ'), ('ch', 'छ'), ('c', 'च'), ('jh', 'झ'), ('j', 'ज'), ('ñ', 'ञ'),
     ('ṭh', 'ठ'), ('ṭ', 'ट'), ('ḍh', 'ढ'), ('ḍ', 'ड'), ('ṇ', 'ण'), ('th', 'थ'), ('t', 'त'), ('dh', 'ध'), ('d', 'द'), ('n', 'न'),
     ('ph', 'फ'), ('p', 'प'), ('bh', 'भ'), ('b', 'ब'), ('m', 'म'), ('y', 'य'), ('r', 'र'), ('l', 'ल'), ('v', 'व'), ('ś', 'श'),
     ('ṣ', 'ष'), ('s', 'स'), ('h', 'ह')]
SIGN = {'ṃ': 'ं', 'ḥ': 'ः', "'": 'ऽ'}

def tr2deva(s):
    s = unicodedata.normalize('NFC', s).lower().replace('m̐', 'ँ')   # the page writes the candrabindu of अस्मिँल्लोके as m̐
    out, i, prev_c = [], 0, False
    while i < len(s):
        lat = next((x for x in C if s.startswith(x[0], i)), None)
        if lat:
            out.append(('्' if prev_c else '') + lat[1]); i += len(lat[0]); prev_c = True; continue
        vow = next((x for x in V if s.startswith(x[0], i)), None)
        if vow:
            out.append(vow[2] if prev_c else vow[1]); i += len(vow[0]); prev_c = False; continue
        out.append(('्' if prev_c else '') + SIGN.get(s[i], s[i])); i += 1; prev_c = False
    if prev_c: out.append('्')
    return unicodedata.normalize('NFC', ''.join(out))

def key(s):
    """For comparison: no spaces, daṇḍas, digits or the page's stray ; (3.17.7, in both)."""
    return re.sub(r'[\s|.,;।॥0-9०-९]', '', s.replace('ॐ', 'ओं'))

# a difference between the page's Devanagari and its transliteration: (block, Devanagari, transliteration read back)
WITNESS_DIFF = {'8.5.2': ('मनुतेऽ', 'मनुते')}

def compare(B):
    bad = 0
    for b in B:
        at = '%d.%d.%d' % (b['ch'], b['sec'], b['n'])
        a, t = key(' '.join(b['v'])), key(tr2deva(' '.join(b['t'])))
        if at in WITNESS_DIFF:
            d, r = WITNESS_DIFF[at]; assert a.count(d) == 1 and t.count(r) == 1, at; a = a.replace(d, r)
        if a != t: bad += 1; print('page Devanagari ≠ its transliteration', at, '\n ', a, '\n ', t)
    assert not bad, bad

# ---- the page's blocks → mantras ----
HEAD = re.compile(r'^॥ (प्रथम|द्वितीय|तृतीय|चतुर्थ|पञ्चम|षष्ठ|सप्तम|अष्टम)ोऽध्यायः ॥ ')
MARK = re.compile(r'॥\s*([०-९]+)\.([०-९]+)\.([०-९]+)\s*॥')
CLOSE = re.compile(r'^(?:॥\s*॥\s*इति [^॥]*॥\s*|॥\s*इति [^॥]*॥\s*)*$')
# the page numbers the last mantra of 6.6 "६.६.६"; it is the fifth (the page has no 6.6.5: the khaṇḍa is the four
# likenesses, curd, food, water and fire, 6.6.1–4, and this mantra that sums them up, closing the khaṇḍa)
RENUMBER = {(6, 6, 6): 5}
# the page's block 3.17.7–8: after आदित्प्रत्नस्य रेतसः it adds the rest of that ṛc (ज्योतिः पश्यन्ति वासरम्; परो यदिध्यते
# दिवि), which no witness has, and numbers the next ṛc's words 3.17.8; every witness has one mantra, 3.17.7
BLOCK_FIX = {(3, 17, 7): ('रेतसः ज्योतिः पश्यन्ति वासरम्; परो यदिध्यते दिवि ॥ ३.१७.७ ॥ उद्वयं', 'रेतसः । उद्वयं', '॥ ३.१७.८ ॥', '॥ ३.१७.७ ॥')}

def mantras(B):
    out = []
    for b in B[1:]:
        text = ' '.join(b['v'])
        text = HEAD.sub('', text) if b['n'] == 1 and b['sec'] == 1 else text
        if (b['ch'], b['sec'], b['n']) in BLOCK_FIX:
            f = BLOCK_FIX[(b['ch'], b['sec'], b['n'])]
            for a, c in zip(f[::2], f[1::2]): assert text.count(a) == 1, a; text = text.replace(a, c)
        parts = MARK.split(text)
        assert CLOSE.match(parts[-1].strip()), (b['id'], parts[-1])
        for k in range(0, len(parts) - 1, 4):
            a, s, m = num(parts[k + 1]), num(parts[k + 2]), num(parts[k + 3])
            m = RENUMBER.get((a, s, m), m)
            if k == 0: assert (a, s) == (b['ch'], b['sec']), b['id']
            out.append({'a': a, 'k': s, 'm': m, 'text': ' '.join(parts[k].split())})
    return out

# ---- corrections: (item, the page, the text); each must occur exactly once in that item (reconciliation.md) ----
FIX = [
    ('shanti.1', 'निराकरणंं', 'निराकरणं'),
    ('1.2.1', 'संयेतिरे उभये', 'संयेतिर उभये'),
    ('1.2.6', 'संकल्पनीयंच चासंकल्पनीयं', 'संकल्पनीयं चासंकल्पनीयं'),
    ('1.6.1', 'च्यध्यूढ़ं साम', 'च्यध्यूढं साम'),
    ('1.6.4', 'नक्षत्रान्येवर्क्', 'नक्षत्राण्येवर्क्'),
    ('1.6.6', 'आप्रणस्वात्', 'आप्रणखात्'),
    ('1.7.7', 'स एष चामुष्मात्', 'स एष ये चामुष्मात्'),
    ('1.8.2', 'प्रावहणो', 'प्रवाहणो'),
    ('1.9.1', 'ज्यायानकाशः', 'ज्यायानाकाशः'),
    ('1.11.9', 'भूतन्यन्नमेव', 'भूतान्यन्नमेव'),
    ('1.12.5', 'प्रजपतिः', 'प्रजापतिः'),
    ('1.13.1', 'हाउकारः वायु', 'हाउकारो वायु'),
    ('1.13.2', 'प्रजपतिर्', 'प्रजापतिर्'),
    ('2.1.2', 'साधुनैनमुपगादित्येव', 'साधुनैनमुपागादित्येव'),
    ('2.5.1', 'हिंकारः ग्रीष्मः', 'हिंकारो ग्रीष्मः'),
    ('2.8.1', 'सप्तविध्ं', 'सप्तविधं'),
    ('2.10.6', 'आप्नोती हादित्यस्य', 'आप्नोति हादित्यस्य'),
    ('2.15.2', 'सुरूपंश्च', 'सुरूपांश्च'),
    ('2.19.1', 'द्गीथोस्थि', 'द्गीथोऽस्थि'),
    ('2.21.3', 'त्रीणी त्रीणि', 'त्रीणि त्रीणि'),
    ('2.23.2', 'सम्प्रास्र्वन्त', 'सम्प्रास्रवन्त'),
    ('2.24.3', 'गार्हपत्यस्योदाङ्मुख', 'गार्हपत्यस्योदङ्मुख'),
    ('3.2.1', 'ता अमृत आपः', 'ता अमृता आपः'),
    ('3.2.2', 'रसोजायत', 'रसोऽजायत'),
    ('3.4.2', 'तिहासपूराण', 'तिहासपुराण'),
    ('3.4.2', 'भ्यतपं स्तस्या', 'भ्यतपंस्तस्या'),
    ('3.4.2', 'तेज इन्द्रियां', 'तेज इन्द्रियं'),
    ('3.5.2', 'भ्यतपं स्तस्या', 'भ्यतपंस्तस्या'),
    ('3.6.3', 'स य एतदेव रूपमभि', 'स एतदेव रूपमभि'),
    ('3.9.4', 'धिपत्य्ं', 'धिपत्यं'),
    ('3.12.1', 'वा ईदं', 'वा इदं'),
    ('3.12.7', 'तद्योयं', 'तद्योऽयं'),
    ('3.12.8', 'पुरुष अकाशो', 'पुरुष आकाशो'),
    ('3.13.8', 'यत्रितदस्मिञ्', 'यत्रैतदस्मिञ्'),
    ('3.14.2', 'मभ्यत्तोऽवाक्य', 'मभ्यात्तोऽवाक्य'),
    ('3.16.6', 'प्राणा अदित्या', 'प्राणा आदित्या'),
    ('3.17.6', 'घोर् आङ्गिरसः', 'घोर आङ्गिरसः'),
    ('3.18.2', 'पादा अदित्यः', 'पाद आदित्यः'),
    ('3.18.4', 'तपति च् भाति', 'तपति च भाति'),
    ('3.19.2', 'समेघो', 'स मेघो'),
    ('4.1.2', 'हं सोहं समभ्युवाद', 'हंसो हंसमभ्युवाद'),
    ('4.1.2', 'प्रसाङ्क्षी स्तत्त्वा', 'प्रसाङ्क्षीस्तत्त्वा'),
    ('4.3.8', 'तस्म उ ह', 'तस्मा उ ह'),
    ('4.4.4', 'परिचरिणी', 'परिचारिणी'),
    ('4.6.1', 'ग आभिप्रस्थापयांचकार', 'गा अभिप्रस्थापयांचकार'),
    ('4.8.4', 'स यै एतमेवं', 'स य एतमेवं'),
    ('4.9.1', 'हाचर्यकुलं', 'हाचार्यकुलं'),
    ('4.9.1', 'तमाचर्योऽभ्युवाद', 'तमाचार्योऽभ्युवाद'),
    ('4.10.1', 'ब्रह्मचार्यमुवास', 'ब्रह्मचर्यमुवास'),
    ('4.10.1', 'वार्षाण्य', 'वर्षाण्य'),
    ('4.10.3', 'व्याधीभिः', 'व्याधिभिः'),
    ('4.13.2', 'सर्वमयुरेति', 'सर्वमायुरेति'),
    ('4.16.1', 'पवते एष', 'पवत एष'),
    ('4.16.2', 'यत्रौपाकृते', 'यत्रोपाकृते'),
    ('4.17.1', 'न्तरिक्षातादित्यं', 'न्तरिक्षादादित्यं'),
    ('5.3.4', 'किमनुशिष्ठोऽवोचथा', 'किमनुशिष्टोऽवोचथा'),
    ('5.4.1', 'इति तृतीयः खण्डः ॥ असौ', 'असौ'),
    ('5.4.2', 'तस्या अहुतेः', 'तस्या आहुतेः'),
    ('5.12.2', 'मूधा त्वेष', 'मूर्धा त्वेष'),
    ('5.15.1', 'त्वमात्मानमुपस्से', 'त्वमात्मानमुपास्से'),
    ('5.17.1', 'त्वमात्मानमुपस्स इति', 'त्वमात्मानमुपास्स इति'),
    ('5.23.2', 'ब्रह्मवर्चसेन ॥', 'ब्रह्मवर्चसेनेति ॥'),
    ('5.24.1', 'इदमविद्वाग्निहोत्रं', 'इदमविद्वानग्निहोत्रं'),
    ('6.1.3', 'प्राक्ष्यः येनाश्रुतं', 'प्राक्ष्यो येनाश्रुतं'),
    ('6.1.6', 'सोम्यिकेन', 'सोम्यैकेन'),
    ('6.4.3', 'यच्छन्द्रमसो', 'यच्चन्द्रमसो'),
    ('6.5.4', 'सोम्य मनः आपोमयः', 'सोम्य मन आपोमयः'),
    ('6.6.1', 'स उर्ध्वः', 'स ऊर्ध्वः'),
    ('6.6.2', 'स उर्ध्वः', 'स ऊर्ध्वः'),
    ('6.6.3', 'स उर्ध्वः', 'स ऊर्ध्वः'),
    ('6.6.3', 'सा प्राणो भवति', 'स प्राणो भवति'),
    ('6.6.4', 'स उर्ध्वः', 'स ऊर्ध्वः'),
    ('6.7.2', 'पञ्चदशाहानि नशाथ', 'पञ्चदशाहानि नाशाथ'),
    ('6.7.3', 'महतोऽभ्या हितस्यैको', 'महतोऽभ्याहितस्यैको'),
    ('6.7.4', 'स हशाथ', 'स हाशाथ'),
    ('6.8.3', 'तत्रितच्छुङ्गमु', 'तत्रैतच्छुङ्गमु'),
    ('6.8.6', 'न्यत्राद्भ्य्ऽद्भिः', 'न्यत्राद्भ्योऽद्भिः'),
    ('6.9.3', 'त इह व्यघ्रो', 'त इह व्याघ्रो'),
    ('6.11.3', 'म्रियते इति', 'म्रियत इति'),
    ('6.12.3', 'दद्ं सर्वं', 'दं सर्वं'),
    ('6.16.2', 'भवति ततेव', 'भवति तत एव'),
    ('6.16.2', 'प्रतिगृह्णाति सन दह्यते', 'प्रतिगृह्णाति स न दह्यते'),
    ('7.2.1', 'क्षत्रविद्यां सर्पदेवजनविद्यां', 'क्षत्रविद्यां नक्षत्रविद्यां सर्पदेवजनविद्यां'),
    ('7.12.2', 'भूय इति आकाशाद्वाव', 'भूय इत्याकाशाद्वाव'),
    ('7.24.1', 'तन्मर्त्य्ं', 'तन्मर्त्यं'),
    ('8.1.3', 'न्तर्हृदय अकाश', 'न्तर्हृदय आकाश'),
    ('8.1.5', 'स ब्रूयात्नास्य', 'स ब्रूयान्नास्य'),
    ('8.1.5', 'ब्रह्मपुरमस्मिकामाः', 'ब्रह्मपुरमस्मिन्कामाः'),
    ('8.1.6', 'तद्य इहात्मानमनुविद्य', 'तद्य इहात्मानमननुविद्य'),
    ('8.1.6', 'मनिवुद्य', 'मनुविद्य'),
    ('8.1.6', 'व्रजन्त्येतंश्च', 'व्रजन्त्येतांश्च'),
    ('8.5.2', 'तब्ब्रह्मचर्येण', 'तद्ब्रह्मचर्येण'),
    ('8.5.2', 'मनुते ऽ ॥', 'मनुते ॥'),
    ('8.5.4', 'एवैतवरं', 'एवैतावरं'),
    ('8.6.3', 'समस्त्ः', 'समस्तः'),
    ('8.12.5', 'सात्मा मनोऽस्य', 'स आत्मा मनोऽस्य'),
    ('8.12.6', 'प्र्जापतिरुवाच', 'प्रजापतिरुवाच'),
    ('8.15.1', 'तधैतद्ब्रह्मा प्रजापतयै उवाच', 'तद्धैतद्ब्रह्मा प्रजापतय उवाच'),
    ('8.15.1', 'प्रजाभ्यः आचार्यकुलाद्', 'प्रजाभ्य आचार्यकुलाद्'),
    ('8.15.1', 'धर्मिकान्विदधदा', 'धार्मिकान्विदधदा'),
    ('8.15.1', 'सर्वैन्द्रियाणि', 'सर्वेन्द्रियाणि'),
]

# ---- corrections the witnesses show (reconciliation.md, "Corrections from the witnesses"); applied after FIX ----
WITNESS_FIX = [
    ('1.1.2', 'पृथिव्या अपो रसः', 'पृथिव्या आपो रसः'),
    ('1.2.6', 'तेनोभयंसंकल्पते', 'तेनोभयंसंकल्पयते'),
    ('1.2.9', 'ऽवित्त्वोत्क्रमति', 'ऽवित्त्वोत्क्रामति'),
    ('1.8.5', 'लोकमिति नयेदिति', 'लोकमतिनयेदिति'),
    ('1.8.7', 'लोकमिति नयेदिति', 'लोकमतिनयेदिति'),
    ('2.1.4', 'विद्वानसाधु', 'विद्वान्साधु'),
    ('2.11.2', 'स एवमेतद्गायत्रं', 'स य एवमेतद्गायत्रं'),
    ('2.20.2', 'सलोकतांसर्ष्टितांसायुज्यं', 'सलोकतांसार्ष्टितांसायुज्यं'),
    ('2.21.4', 'सर्वमस्मीत्युपासित', 'सर्वमस्मीत्युपासीत'),
    ('4.4.2', 'जाबालो ब्रवीथा', 'जाबालो ब्रुवीथा'),
    ('4.16.2', 'ब्रह्मा व्यवदति', 'ब्रह्मा व्यववदति'),
    ('4.16.4', 'ब्रह्मा व्यवदत्युभे', 'ब्रह्मा व्यववदत्युभे'),
    ('5.11.5', 'न कर्दर्यो', 'न कदर्यो'),
    ('5.13.2', 'चक्षुषेतदात्मन', 'चक्षुष्ट्वेतदात्मन'),
    ('5.10.5', 'तस्मिन्यवात्सम्पात', 'तस्मिन्यावत्सम्पात'),
    ('7.6.1', 'ध्यायन्तीव पर्वता देवमनुष्या', 'ध्यायन्तीव पर्वता ध्यायन्तीव देवमनुष्या'),
    ('7.15.1', 'प्राणो वा आशाया', 'प्राणो वाव आशाया'),
    ('7.26.2', 'विंशतिराहारशुद्धौ सत्त्वशुद्धौ', 'विंशतिराहारशुद्धौ सत्त्वशुद्धिः सत्त्वशुद्धौ'),
    ('8.5.3', 'ब्रह्मचर्यमेव तदरश्च', 'ब्रह्मचर्यमेव तत्तदरश्च'),
    ('8.7.3', 'किमिच्छन्तावास्तमिति', 'किमिच्छन्ताववास्तमिति'),
]

def settle():
    B = json.load(open(os.path.join(HERE, 'chandogya_raw.json'), encoding='utf-8'))
    compare(B)
    sh = B[0]; assert sh['n'] == 0 and sh['ref'] == '1.1.0'
    shanti = [l for l in sh['v']]
    shanti[-1] = re.sub(r'^॥\s*', '', shanti[-1])          # "॥ ॐ शान्तिः शान्तिः शान्तिः ॥": the opening ॥ of a line is not ours
    items = [{'id': 'shanti.1', 'p': 0, 's': 'shanti', 'y': 'shanti', 'n': '', 'v': shanti}]
    M = mantras(B)
    for x in M:
        items.append({'id': '%d.%d.%d' % (x['a'], x['k'], x['m']), 'p': x['a'] - 1, 's': 'k%d.%d' % (x['a'], x['k']),
                      'y': 'mantra', 'n': str(x['m']), 'v': [x['text'] + ' ॥%s॥' % deva(x['m'])]})
    byid = {x['id']: x for x in items}
    assert len(byid) == len(items)
    for at, a, b in FIX + WITNESS_FIX:
        v = byid[at]['v']
        assert sum(l.count(a) for l in v) == 1, (at, a)
        byid[at]['v'] = [l.replace(a, b) for l in v]
    # every khaṇḍa's mantras run 1 … N without a gap, and the adhyāyas run 1 … 8
    run = {}
    for x in M: run.setdefault((x['a'], x['k']), []).append(x['m'])
    for (a, k), ms in run.items(): assert ms == list(range(1, len(ms) + 1)), (a, k, ms)
    assert sorted({a for a, _ in run}) == list(range(1, 9))
    for a in range(1, 9):
        ks = sorted(k for a2, k in run if a2 == a); assert ks == list(range(1, len(ks) + 1)), (a, ks)
    return items, run

# ---- our topic headings: one at each teaching ----
TOPICS = [
    ('shanti.1', 'शान्तिपाठ', 'Shanti Paath'),
    ('1.1.1', 'उद्गीथ — ॐ अक्षरकी उपासना', 'The Udgitha: meditation on the syllable Om'),
    ('1.2.1', 'देवता और असुर — मुख्य प्राण', 'Gods and demons: the chief breath'),
    ('1.3.1', 'सूर्य और श्वासमें उद्गीथ', 'The Udgitha in the sun and in the breath'),
    ('1.8.1', 'तीन उद्गीथ-ज्ञाता — सामका आधार', 'Three masters of the Udgitha: what the saman rests on'),
    ('1.10.1', 'उषस्ति चाक्रायण', 'Ushasti Chakrayana'),
    ('1.12.1', 'कुत्तोंका उद्गीथ', 'The Udgitha of the dogs'),
    ('1.13.1', 'स्तोभ अक्षर', 'The stobha syllables'),
    ('2.1.1', 'सम्पूर्ण सामकी उपासना', 'Meditation on the whole saman'),
    ('2.2.1', 'पाँच भागोंवाला साम', 'The saman of five parts'),
    ('2.8.1', 'सात भागोंवाला साम', 'The saman of seven parts'),
    ('2.11.1', 'गायत्र आदि साम — किसमें पिरोये हैं', 'The named samans and what each is woven into'),
    ('2.22.1', 'गानके स्वर; धर्मके तीन स्कन्ध; ॐ', 'How to sing; the three branches of dharma; Om'),
    ('2.24.1', 'यज्ञके तीन सवन', 'The three pressings of the sacrifice'),
    ('3.1.1', 'मधुविद्या — सूर्य देवताओंका मधु', 'The honey teaching: the sun as the honey of the gods'),
    ('3.12.1', 'गायत्री और हृदयका आकाश', 'The Gayatri and the space within the heart'),
    ('3.13.1', 'हृदयके पाँच द्वार', 'The five openings of the heart'),
    ('3.14.1', 'शाण्डिल्यविद्या — यह सब ब्रह्म है', 'Shandilya’s teaching: all this is Brahman'),
    ('3.15.1', 'अक्षय कोश', 'The undecaying chest'),
    ('3.16.1', 'पुरुष ही यज्ञ है', 'A man’s life as the sacrifice'),
    ('3.18.1', 'मन और आकाश ब्रह्मरूपमें', 'Mind and space as Brahman'),
    ('3.19.1', 'आदित्य ब्रह्म है — ब्रह्माण्ड', 'The sun as Brahman: the cosmic egg'),
    ('4.1.1', 'जानश्रुति और रैक्व — संवर्गविद्या', 'Janashruti and Raikva: the gatherer'),
    ('4.4.1', 'सत्यकाम जाबाल', 'Satyakama Jabala'),
    ('4.10.1', 'उपकोसल और अग्नियोंका उपदेश', 'Upakosala and the teaching of the fires'),
    ('4.16.1', 'यज्ञ और ब्रह्मा ऋत्विक्', 'The sacrifice and the Brahma priest'),
    ('5.1.1', 'प्राणकी श्रेष्ठता', 'Breath, the eldest and best'),
    ('5.3.1', 'प्रवाहण जैवलि — पञ्चाग्निविद्या', 'Pravahana Jaivali: the five fires'),
    ('5.11.1', 'वैश्वानर आत्मा', 'The universal Self, Vaishvanara'),
    ('6.1.1', 'उद्दालक और श्वेतकेतु — एकको जाननेसे सब जाना', 'Uddalaka and Shvetaketu: knowing the one, all is known'),
    ('6.2.1', 'सत् से सृष्टि — तेज, जल और अन्न', 'Creation from Being: heat, water and food'),
    ('6.8.1', 'नींद, भूख और प्यास — तत्त्वमसि', 'Sleep, hunger and thirst: that you are'),
    ('6.9.1', 'दृष्टान्तोंमें तत्त्वमसि', 'That you are, shown by examples'),
    ('7.1.1', 'नारद और सनत्कुमार — नामसे ऊपर', 'Narada and Sanatkumara: beyond name, step by step'),
    ('7.23.1', 'भूमा ही सुख है', 'The infinite alone is joy'),
    ('8.1.1', 'दहरविद्या — हृदयका छोटा आकाश', 'The small space within the heart'),
    ('8.7.1', 'इन्द्र, विरोचन और प्रजापति', 'Indra, Virochana and Prajapati'),
    ('8.13.1', 'अन्तिम मन्त्र', 'The closing mantras'),
]

if __name__ == '__main__':
    items, run = settle()
    T = [{'id': i, 'hi': h, 'en': e} for i, h, e in TOPICS]
    ids = {x['id'] for x in items}
    for t in T: assert t['id'] in ids, t
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, T, [str(a) for a in range(1, 9)], 'sa', [
        'Chāndogya Upaniṣad: the śānti mantra and the eight adhyāyas, mantras 1.1.1 … 8.15.1, from shlokam.org. Made by',
        'source/settle.py from the page; do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(items), 'items:', len(items) - 1, 'mantras in', len(run), 'khaṇḍas;',
          ', '.join('%d: %d' % (a, sum(len(v) for (a2, _), v in run.items() if a2 == a)) for a in range(1, 9)))
