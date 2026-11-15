"""Checks text.txt (the Bṛhadāraṇyaka Upaniṣad) against the Devanagari witnesses in source/witness/.

A witness file has a "# a.b.n" line before each mantra's lines (witness_upanishads_org.py). upanishads.org.in writes
the words apart (सूर्यश् चक्षुर्), breaks the prose into sentences and writes the word before each break in pausa
(आसीत् । मृत्युना, where the printout runs on: आसीन्मृत्युना), and writes ं, म् and ꣳ as it likes. So:
1. at each of the witness's sentence breaks, the two words around it are joined with the sandhi the printout uses
   when it runs on (join), wherever the printout has those letters there and not the pausa form (fit);
2. both texts are reduced to the letters that carry the reading (skeleton): no spaces, daṇḍas, numbers or avagraha, a
   consonant's virāma before a vowel joined to it, every nasal before a consonant and a word-final म् as ं, ꣳ as ं;
3. each mantra's skeletons are compared letter by letter. Every difference must be listed, with its decision, in the
   witness's decisions file (witness/<name>.decisions.json; the readings are also in reconciliation.md): a difference
   not listed, or a listed one no longer found, fails the check.
Usage: python3 tools/works/brihadaranyaka-upanishad/source/check.py
"""
import difflib, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
ITEMS = textfile.read(os.path.join(HERE, '..', 'text.txt'))
BY = {x['id']: x for x in ITEMS}

MATRA = {'अ': '', 'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'}
VOWEL = ''.join(MATRA)
CONS = 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह'
VOICED = 'गघजझडढदधबभङञणनमयरलवह'


def skeleton(s):
    s = unicodedata.normalize('NFC', s).replace('‍', '').replace('‌', '').replace('ꣳ', 'ं')
    s = re.sub(r'[।॥|0-9०-९.,:\-–ऽ’\'"]', ' ', s)
    s = re.sub(r'ं(?=\s*[%s])' % VOWEL, 'म्', s)                                 # समं एतद् = समम् एतद्
    s = re.sub(r'्\s*([%s])' % VOWEL, lambda m: MATRA[m.group(1)], s)        # सूर्यश् चक्षुर् … पर्वाण्य् अहो
    s = re.sub(r'\s', '', s)
    s = re.sub(r'[ङञणनम]्(?=[%s])' % CONS, 'ं', s)                           # a nasal before a consonant → ं
    return re.sub(r'म्$', 'ं', s)


def join(w1, w2):
    """Two words across one of the witness's sentence breaks, written with the sandhi the printout uses when it runs on
    (आसीत् + मृत्युना → आसीन्मृत्युना, भवति + अथ → भवत्यथ, जघनार्धः + यद् → जघनार्धो यद्)."""
    if not w1 or not w2: return w1 + w2
    v = w2[0]; last = w1[-1]
    if last == 'ः':
        base = w1[:-1]; p = base[-1:]
        if p and p in CONS:                                     # -aḥ
            if v == 'अ': return base + 'ो' + w2[1:]
            if v in VOWEL: return base + ' ' + w2
            if v in VOICED: return base + 'ो' + w2
        elif p == 'ा':                                          # -āḥ
            if v in VOWEL or v in VOICED: return base + ' ' + w2
        elif v in VOWEL or v in VOICED:                         # -iḥ, -uḥ …
            return base + 'र्' + w2
        if v in 'चछ': return base + 'श्' + w2
        if v in 'टठ': return base + 'ष्' + w2
        if v in 'तथ': return base + 'स्' + w2
        return w1 + w2
    if last == '्':
        c = w1[-2:-1]; base = w1[:-2]
        if c == 'त':
            if v in 'नम': return base + 'न्' + w2
            if v in 'चछ': return base + 'च्' + w2
            if v in 'जझ': return base + 'ज्' + w2
            if v == 'ल': return base + 'ल्' + w2
            if v == 'श': return base + 'च्छ' + w2[1:]
            if v == 'ह': return base + 'द्ध' + w2[1:]
            if v in VOWEL or v in VOICED: return base + 'द्' + w2
        if c in ('क', 'ट', 'प') and (v in VOWEL or v in VOICED):
            return base + {'क': 'ग', 'ट': 'ड', 'प': 'ब'}[c] + '्' + w2
        if c == 'न':
            if v in 'चछ': return base + 'ंश्' + w2
            if v in 'तथ': return base + 'ंस्' + w2
            if v in 'जझश': return base + 'ञ्' + w2
            if v == 'ल': return base + 'ल्' + w2
            if v in VOWEL and base[-1:] and base[-1] in CONS + 'िु': return base + 'न्न्' + w2
        return w1 + w2
    if v in VOWEL:
        rest = w2[1:]
        if last in CONS or last == 'ा':                         # -a, -ā
            base = w1 if last in CONS else w1[:-1]
            m = {'अ': 'ा', 'आ': 'ा', 'इ': 'े', 'ई': 'े', 'उ': 'ो', 'ऊ': 'ो', 'ए': 'ै', 'ऐ': 'ै', 'ओ': 'ौ', 'औ': 'ौ'}.get(v)
            if m: return base + m + rest
            if v == 'ऋ': return base + 'र्' + rest
        if last in 'िी': return w1[:-1] + ('ी' + rest if v in 'इई' else '्य' + MATRA[v] + rest)
        if last in 'ुू': return w1[:-1] + ('ू' + rest if v in 'उऊ' else '्व' + MATRA[v] + rest)
        if last in 'ेो' and v == 'अ': return w1 + rest
        if last == 'े': return w1[:-1] + ' ' + w2
        if last == 'ै': return w1[:-1] + 'ा ' + w2
    return w1 + w2


def joined(a, b):
    """a's last word and b's first word joined with sandhi, with the rest of both."""
    a = a.rstrip(' ।॥-,'); b = b.lstrip(' ।॥-,')
    i = a.rfind(' ') + 1; j = (b + ' ').find(' ')
    return a[:i] + join(a[i:], b[:j]) + b[j:]


def fit(ours, wlines):
    """The witness's text with each word break (a sentence break, a speaker's --, or a space) kept where the printout
    pauses or writes the words apart too, and joined with sandhi where the printout runs the words together."""
    sk = skeleton(ours)
    segs = [x for x in re.split(r'(?<=[।॥,])\s*|\s*--\s*|(?<=[-])|\s+', ' '.join(wlines)) if x and x.strip(' -,')]
    out = segs[0] if segs else ''
    for seg in segs[1:]:
        cand = joined(out, seg)
        k = len(skeleton(out)); left = skeleton(out)[-8:]; right = skeleton(seg)[:-2][:8]
        sc = skeleton(cand)
        # the joined letters around the junction (the token's last two left out: a final nasal is written by what follows)
        if (left + right) not in sk and sc[max(0, k - 8):max(k + 1, len(sc) - 2)] in sk: out = cand
        else: out = out + ' ' + seg
    return out


def decisions(path):
    """witness/<name>.decisions.json: the reviewed differences of that witness, {item id: [[ours, witness, decision]]}."""
    p = path[:-len('.txt')] + '.decisions.json'
    if not os.path.exists(p): return {}
    return {k: [(a, b) for a, b, _ in v] for k, v in json.load(open(p, encoding='utf-8'))['decisions'].items()}


def witness(path):
    W, cur = {}, None
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('#'):
            m = re.fullmatch(r'# (\d+\.\d+\.\d+)', line)
            cur = m.group(1) if m else None
            if cur: W[cur] = []
            continue
        if cur and line.strip(): W[cur].append(line)
    return W


def diffs(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(a[i1:i2], b[j1:j2], a[max(0, i1 - 12):i2 + 12]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']


if __name__ == '__main__':
    bad = 0
    for path in sorted(f for f in os.listdir(os.path.join(HERE, 'witness')) if f.endswith('.txt')):
        W = witness(os.path.join(HERE, 'witness', path))
        EXPECTED = decisions(os.path.join(HERE, 'witness', path))
        for vid, lines in W.items():
            if vid not in BY: print(path, 'has', vid, 'which is not in text.txt'); bad += 1; continue
            ours = ' '.join(BY[vid]['v'])
            exp = list(EXPECTED.get(vid, []))
            for a, b, ctx in diffs(skeleton(ours), skeleton(fit(ours, lines))):
                if (a, b) in exp: exp.remove((a, b)); continue
                bad += 1; print('≠', vid, 'ours %r witness %r  …%s…' % (a, b, ctx))
            for a, b in exp: bad += 1; print('expected but not found', vid, a, b)
        missing = [x['id'] for x in ITEMS if x['y'] == 'mantra' and x['id'] not in W]
        if missing: bad += len(missing); print(path, 'lacks', ' '.join(missing))
        print(path + ':', len(W), 'mantras compared')
    print(bad, 'differences not settled')
    sys.exit(1 if bad else 0)
