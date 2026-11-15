"""Compares a Sūkta's text.txt with its independent witnesses (tools/works/*-suktam/source/check.py), shared by the six
Sūktas because their texts and witnesses are alike: Vedic recitation texts in Devanagari, the base with svaras and the
Taittirīya reciters' spellings, the witnesses with or without svaras.

A witness file (source/witness/<site>.txt, made from the raw download by the work's source/witnesses.py) is runs of
text, each headed by a line "# <first id> <last id>": the run must spell the same words as our verses from the first id
to the last, in order. Spacing, line division, daṇḍas and numbers are not compared, so a witness may join or divide the
verses otherwise. What the spellings below write alike is no difference (key):
  - the svaras (compared on their own by svaras(), only where a witness has them);
  - ॐ / ओं, a visarga typed as a colon, a hyphen joining words, a word divided after its final consonant (सवितर् आधिपत्यैः, the pada-like
    division of Wikisource's unaccented Saṃhitā), the avagraha ऽ (-ऽ and -ऽऽ where a long vowel is joined, or none);
  - the anusvāra: a class nasal before a consonant, a word-final म्, ꣳ and the typed ग्ं, and ं all read alike
    (tools/text/standard.py → fold, applied to the joined letters); the ँ the Taittirīya texts write on य व ल after an
    anusvāra (तं-यँ॒ज्ञं), and ँ for ं;
  - an anusvāra before य व ल written as that letter doubled (देव॒व्विँ॒श्वाक्ष॑, शँय्योः: the accented Wikisource pages),
    and their ऱ for र before ष;
  - a visarga before a sibilant written as the sibilant (-स्स, -श्श: त्रि-स्स॒प्त, त्रिःसप्त), थ्स for त्स, न्त्स for न्स,
    the reciters' doubled द्ध्य द्ध्व for ध्य ध्व and त्त्व / त्व, the doubled final न्न् at a pause.
Where a witness has svaras, the svaras of each word it spells as we do, at the same place, are compared too (svaras()).
Every other difference is printed with the verse of ours it falls in, unless the work's check.py lists it (EXPECTED:
{witness file: [(witness, ours) or (witness, ours, verse id)]}, each pair in key form or as written, for every run of
the file or for the run holding that verse only; each recorded in the work's reconciliation.md),
and every expected pair must still be found, so a list never outlives its difference.
"""
import difflib, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); import textfile
sys.path.insert(0, os.path.join(HERE, '..', 'text')); from standard import fold

SVARA = '॒॑॓॔᳐-᳨᳚'
CONS = 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ'

def letters(s):
    """The text as one run of letters (no spaces, svaras, daṇḍas, numbers), each convention above folded."""
    s = unicodedata.normalize('NFC', s).replace('‍', '').replace('‌', '').replace('ॐ', 'ओं')
    s = re.sub('[%s]' % SVARA, '', s)
    s = re.sub('(?<=[ऀ-ॿ]):', 'ः', s)                          # a visarga typed as a colon
    s = re.sub(r'[\s\-–—.,;:!?।॥|/()\[\]{}`\'"0-9०-९]', ' ', s)
    s = re.sub('न्न्(?= |$)', 'न्', s)                     # व्य॑कल्पयन्न् at a pause
    s = re.sub('([%s])् +([अआइईउऊऋएऐओऔ])' % CONS, lambda m: m.group(1) + dict(zip('अआइईउऊऋएऐओऔ', ['', *'ािीुूृेैोौ']))[m.group(2)], s)   # सवितर् आधिपत्यैः
    s = s.replace(' ', '').replace('ऽ', '')
    s = s.replace('ग्ं', 'ꣳ')
    s = re.sub('(?<=[ािीुूेैोौ])ग्(?=[शषसह])', 'ꣳ', s)      # ज्यायाग्॑श्च: the typed ग्ं with its ं dropped
    s = re.sub('([यवल])्(?=\\1[^ ]{0,3}?ँ)', 'ं', s)          # देव॒व्विँ॒श्वाक्ष॑, सर्व॒व्व्याँ॒प्य: ं before य व ल as the letter doubled
    s = re.sub('([यवल][ािीुूेैोौ]?)ँ', r'\1', s)              # तं-यँ॒ज्ञ, शंयोँः, लोँ॒क
    s = s.replace('ँ', 'ं')
    s = re.sub('ं([यवल])्(?=\\1)', 'ं', s).replace('ऱ', 'र')        # शँय्योः; ऱ्ष, the Taittirīya r before ष
    s = re.sub('ः(?=[शषस])', lambda m: '', s)                 # ः स / -स्स: the sibilant doubled below
    s = re.sub('([शषस])्(?=\\1)', '', s)
    s = s.replace('थ्स', 'त्स').replace('न्त्स', 'न्स')            # तस्मिन्त्सर्वं, the t Pāṇini allows between न् and स
    s = re.sub('द्ध्(?=[यव])', 'ध्', s).replace('त्त्व', 'त्व')    # म॒द्ध्ये, ऊ॒र्द्ध्व, तत्त्व: the reciters' doubling
    s = re.sub('[ङञणनम]्(?=[%s])' % CONS, 'ं', s)
    s = re.sub('म्$', 'ं', s)
    return fold(s)

# ---- making the witness files (each work's source/witnesses.py) ----
# Sanskrit Wikisource's accented pages write some signs with private-use characters of their font, read here by their
# places: U+E001 and U+F156 are ꣳ (त्रि\ue001॑शत्, य॒ज्ञ\uf156 स्वा), U+F131 the visarga before प (शान्ति॒\uf131 पुरु॑षः),
# U+F176, U+F184 and U+F185 the svarita ᳚ (देवाना\uf176म्, ते\uf184ऽस्मद्); U+E007 and U+F1AB (a mark beside a daṇḍa,
# one stray) are dropped.
PUA = {0xE001: 'ꣳ', 0xF156: 'ꣳ', 0xF131: 'ः', 0xF176: '᳚', 0xF184: '᳚', 0xF185: '᳚', 0xE007: None, 0xF1AB: None}

def read_raw(path):
    return open(path, encoding='utf-8').read().translate(PUA)

def between(t, a, b):
    """From the text a to the end of the first match of the pattern b after it."""
    i = t.index(a); return t[i:re.compile(b).search(t, i).end()]

def clean(s):
    """A witness's words only: its <ref> notes, verse and section numbers, labels (6.11.1) and ", इति" dropped."""
    s = re.sub(r'<ref>.*?</ref>', '', s)
    s = re.sub(r'\(\s*[0-9०-९]+\s*\)', ' ', s)
    s = re.sub(r'॥\s*[०-९0-9]+\s*[कख]?\s*॥', '॥', s)
    s = re.sub(r'\[\d+\]', ' ', s)
    s = re.sub(r'^\d+(\.\d+)+\s*$', '', s, flags=re.M)
    s = re.sub(r',\s*इति', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def write_witness(path, runs):
    """runs: [(first id, last id, raw text)] → the witness file."""
    out = []
    for a, b, t in runs: out += ['# %s %s' % (a, b), clean(t), '']
    open(path, 'w', encoding='utf-8').write('\n'.join(out))

def ours(text_path):
    return [(x['id'], '\n'.join(x['v'])) for x in textfile.read(text_path)]

def runs(witness_path):
    """[(first id, last id, text)]"""
    out = []
    for blk in re.split(r'^# ', open(witness_path, encoding='utf-8').read(), flags=re.M)[1:]:
        head, _, body = blk.partition('\n')
        a, b = head.split()[:2]
        out.append((a, b, body))
    return out

def compare(text_path, witness_dir, expected):
    """Prints every difference not in `expected` ({file: [(witness, ours)]}); returns their number. Each expected pair
    is put in place in the witness's letters before comparing (it must be found there), so a pair names the witness's
    reading and ours in full words, in key form or as written."""
    O = ours(text_path); idx = {i: k for k, (i, _) in enumerate(O)}
    bad = 0
    for name in sorted(os.listdir(witness_dir)):
        if not name.endswith('.txt'): continue
        # a pair written with svaras names a svara difference (svaras()), the others a difference of letters
        acc = lambda x: re.search('[%s]' % SVARA, x)
        raw = [tuple(e[:2]) for e in expected.get(name, [])]
        only = [e[2] if len(e) > 2 else None for e in expected.get(name, [])]   # a pair for one verse only
        exp = [(None, None) if acc(a) or acc(b) else (letters(a), letters(b)) for a, b in raw]
        used, n = set(), 0
        for a, b, body in runs(os.path.join(witness_dir, name)):
            seq = O[idx[a]:idx[b] + 1]
            ol = letters('\n'.join(t for _, t in seq)); where = []
            for i, t in seq: where += [i] * len(letters(t))      # each verse's place, near enough for naming it
            wl = letters(body)
            here = {i for i, _ in seq}
            for k, (x, y) in enumerate(exp):
                if y is None or only[k] and only[k] not in here: continue
                if x and x in wl: wl = wl.replace(x, y); used.add(k)
                elif not x and y in ol and (k not in used): used.add(k)    # a word the witness lacks: matched below
            ops = [o for o in difflib.SequenceMatcher(None, wl, ol, autojunk=False).get_opcodes() if o[0] != 'equal']
            groups = []
            for o in ops:   # differences a few letters apart are one
                if groups and o[1] - groups[-1][2] <= 3: groups[-1] = (groups[-1][0], groups[-1][1], o[2], groups[-1][3], o[4])
                else: groups.append(o)
            for _, i1, i2, j1, j2 in groups:
                w, o = wl[i1:i2], ol[j1:j2]
                if not w and any(y is not None and not x and y == o for x, y in exp): continue
                n += 1
                print('≠ %s %s\n  witness: %s[%s]%s\n  ours:    %s[%s]%s' % (name, where[min(j1, len(where) - 1)], wl[max(0, i1 - 8):i1], w, wl[i2:i2 + 8],
                                                                       ol[max(0, j1 - 8):j1], o, ol[j2:j2 + 8]))
        for i, w, o in svaras(text_path, os.path.join(witness_dir, name)):
            if (w, o) in raw: used.add(raw.index((w, o))); continue
            n += 1; print('≠ %s %s (svaras)\n  witness: %s\n  ours:    %s' % (name, i, w, o))
        for k, (x, y) in enumerate(exp):
            if k not in used: print('  %s: expected difference not found: %s → %s' % (name, raw[k][0], raw[k][1])); n += 1
        print('%s: %d differences' % (name, n)); bad += n
    return bad

VOWEL_SIGN = 'ािीुूृॄेैोौ'
VOWEL = 'अआइईउऊऋॠएऐओऔ'

def vowels(s):
    """The text's vowels in order, each with the svaras written after it (on it, or after its ं ः ꣳ): [(vowel, svaras)]."""
    s = unicodedata.normalize('NFC', s).replace('ॐ', 'ओं')
    out = []
    for k, c in enumerate(s):
        if c in CONS:
            nxt = s[k + 1] if k + 1 < len(s) else ''
            if not nxt or (nxt != '्' and nxt not in VOWEL_SIGN): out.append(['a', ''])
        elif c in VOWEL_SIGN or c in VOWEL: out.append([c, ''])
        elif re.match('[%s]' % SVARA, c) and out: out[-1][1] += c
    return [(v, ''.join(sorted(a))) for v, a in out]

def svaras(text_path, witness_path):
    """Where the witness has svaras: the vowels whose svaras differ from ours, in runs of vowels where the two agree
    (the letters are compared by compare()): [(id, witness, ours)], each shown as the word around it."""
    O = ours(text_path); idx = {i: k for k, (i, _) in enumerate(O)}
    out = []
    for a, b, body in runs(witness_path):
        if not re.search('[%s]' % SVARA, body): continue
        seq = O[idx[a]:idx[b] + 1]
        W = vowels(body); V, where, words = [], [], []
        for i, t in seq:
            for w in t.split():
                for v in vowels(w): V.append(v); where.append((i, w))
        wwords = [w for w in body.split() for _ in vowels(w)]
        A, B = [v for v, _ in W], [v for v, _ in V]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
            if op != 'equal' or i2 - i1 < 4: continue      # only inside a stretch long enough to be the same words
            for k in range(i2 - i1):
                if W[i1 + k][1] != V[j1 + k][1]:
                    i, ow = where[j1 + k]
                    if not out or out[-1][1:] != (wwords[i1 + k], ow): out.append((i, wwords[i1 + k], ow))
    return out
