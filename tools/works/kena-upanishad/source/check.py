"""Checks text.txt (the Kena Upaniṣad) against the Devanagari witnesses in source/witness/.

A witness file (plain text: verses separated by blank lines, each ending in ॥ N॥; a line "# 2" names the khaṇḍa the
following verses belong to; the block before the first "# 1" is the śānti mantra; "# end" starts what is after the
text, the closing śānti, which is not compared; a block naming a khaṇḍa's end, "इति … खण्डः", is not compared, as the
witnesses word it differently) must spell the same words as text.txt. The witnesses number and divide the mantras in
more than one way (khaṇḍa 1 in eight mantras or nine; the boundaries of 3.1/3.2 and 3.11/3.12), so each khaṇḍa is
compared as one run of words, and every difference is printed with the mantra of ours it falls in (a khaṇḍa whose
mantras a witness counts otherwise is named). Daṇḍas, bars, numbers and hyphens at line breaks are ignored; ॐ is read
as ओं too; spacing, a nasal the library's standard folds (tools/text/standard.py → fold) and candrabindu for anusvāra
count as the same. The only differences allowed are those listed in reconciliation.md (LINE and READING below).
Usage: python3 tools/works/kena-upanishad/source/check.py
"""
import difflib, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'text')); from standard import fold
ITEMS = [x for x in textfile.read(os.path.join(HERE, '..', 'text.txt')) if x['y'] != 'iti']

def words(s):
    s = re.sub(r'-\s*\n\s*', '', s)                 # a word broken over two lines (विदाञ्-/चकार)
    s = s.replace('ॐ', 'ओं').replace('‍', '')
    return re.sub(r'[।॥|,0-9०-९\-]', ' ', s).split()

def norm(s):
    """Spacing, a nasal the standard folds (a class nasal before its stop, a final म्, ꣳ) and candrabindu for anusvāra are
    conventions, not readings."""
    return fold(s.replace(' ', '').replace('ँ', 'ं'))

def ours():
    """{khaṇḍa ('0' the śānti): [(word, item id)]}"""
    out = {}
    for x in ITEMS:
        k = '0' if x['id'] == 'shanti.1' else x['id'].split('.')[0]
        out.setdefault(k, []).extend((w, x['id']) for w in words('\n'.join(x['v'])))
    return out

LINE = [   # (witness, ours): the book ends a line inside a sandhi, in pausa form (reconciliation.md, "Line division")
    ('श्रोत्रमथो', 'श्रोत्रम् अथो'), ('निराकरोदनिराकरणमस्त्वनिराकरणं', 'निराकरोद् अनिराकरणमस्त्वनिराकरणं'), ('धर्मास्ते', 'धर्माः ते'),
    ('चक्षुषश्चक्षुः अतिमुच्य', 'चक्षुषश्चक्षुरतिमुच्य'),      # here the witness ends its line inside the sandhi
    ('ऐक्षन्तास्माकमेवायं', 'ऐक्षन्त अस्माकमेवायं'), ('कोऽसीत्यग्निर्वा', 'कोऽसीति अग्निर्वा'),
    ('वीर्यमित्यपीदं', 'वीर्यमितिअपीदं'), ('वायवेतद्विजानीहि', 'वायव्एतद्विजानीहि'), ('पस्पर्शुस्ते', 'पस्पर्शुः ते'),
    ('पाप्मानमनन्ते', 'पाप्मानम् अनन्ते')]
READING = {   # witness: [(witness, ours)]: readings recorded in reconciliation.md
    'upanishads-org.txt': [('', 'ओं'), ('यद्वाचानभ्युदितं', 'यद्वाचाऽनभ्युदितं'), ('दभ्रमेवापि', 'दहरमेवापि'), ('किमेतद्यक्षमिति', 'किमिदंयक्षमिति'),
                           ('प्रतितिष्ठति', 'प्रतितिष्ठतीति')],
    'wikisource.txt': [('मीमाँस्येमेव', 'मीमाँस्यमेव'), ('शशाकादतुम्', 'शशाकादातुं'), ('यद्देतद्गच्छतीव', 'यदेतद्गच्छतीव'), ('तसै', 'तस्यै'),
                       ('प्रतितिष्ठति', 'प्रतितिष्ठतीति')],
    'iitk.txt': [('', 'ओं'), ('ड्ग', 'ङ्ग'), ('वाक्प्राणचक्षुः', 'वाक्प्राणश्चक्षुः'), ('माहं', 'माऽहं'), ('मेस्तु', 'मेऽस्तु'), ('मनो', 'मनः'), ('विदमो', 'विद्मो'), ('विध्दि', 'विद्धि'), ('श्रृणोति', 'शृणोति'), ('ब्रहम्न', 'ब्रह्म'), ('विघ्दि', 'विद्धि'),
                 ('दभ्रमेवापि', 'दहरमेवापि'), ('च', ''), ('तध्दैषां', 'तद्धैषां'), ('किमेतद्यक्षमिति', 'किमिदंयक्षमिति'), ('तस्मिँस्त्वाम', 'तस्मिँस्त्वयि'),
                 ('संकल्पःतध्द', 'सङ्कल्पःतद्ध'), ('वेदाऽभि', 'वेदाभि'), ('प्रतितिष्ठति', 'प्रतितिष्ठतीति')]}
EXPECTED = {name: [(norm(a), norm(b)) for a, b in LINE + R] for name, R in READING.items()}

def expected(name, wit, our):
    """A difference made only of expected ones: the witness's words, each expected reading put in ours' place, are ours."""
    w, o = norm(wit), norm(our)
    if (w, o) in EXPECTED[name]: return True
    for a, b in EXPECTED[name]:
        if len(a) > 2 and a in w: w = w.replace(a, b)      # a short one (च) only as the whole difference
        elif not a and b and o.startswith(b) and not w.startswith(b): w = b + w
    return w == o

def witness(path):
    """{khaṇḍa: [words]}, {khaṇḍa: the number of verses}"""
    txt = open(path, encoding='utf-8').read()
    k, W, count = '0', {}, {}
    for blk in re.split(r'\n\s*\n', txt.strip()):
        blk = '\n'.join(l for l in blk.split('\n') if not l.startswith('# ') or re.fullmatch(r'# (\d|end)', l)).strip()
        if not blk: continue
        if blk.startswith('# '):
            k = blk[2:].strip()
            if k == 'end': break
            continue
        if re.search(r'इति [^\n]*खण्डः', blk) and len(words(blk)) <= 5: continue
        w = words(blk)
        W.setdefault(k, []).extend(w); count[k] = count.get(k, 0) + 1
    return W, count

O = ours()
bad = 0
for path in sorted(glob.glob(os.path.join(HERE, 'witness', '*.txt'))):
    name = os.path.basename(path); W, count = witness(path); n = 0
    for k, ow in O.items():
        a, b = W.get(k, []), [w for w, _ in ow]
        if not a: continue
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == 'equal': continue
            wit, our = ' '.join(a[i1:i2]), ' '.join(b[j1:j2])
            if norm(wit) == norm(our): continue
            if expected(name, wit, our): continue
            n += 1; where = ow[min(j1, len(ow) - 1)][1]
            print('≠ %s %s\n  witness: %s\n  ours:    %s' % (name, where, wit or '—', our or '—'))
        mine = len({i for _, i in ow})
        if k != '0' and count[k] != mine: print('  %s khaṇḍa %s: %d mantras, ours %d' % (name, k, count[k], mine))
    print(name + ':', n, 'differences')
    bad += n
sys.exit(1 if bad else 0)
