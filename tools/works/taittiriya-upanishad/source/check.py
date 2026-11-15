"""Checks text.txt (the Taittirīya Upaniṣad) against the witnesses in source/witness/ (made by witnesses.py).

A witness file: paragraphs separated by blank lines; a line "# 1.3" names the anuvāka the following paragraphs belong
to, "# shanti.2" the śānti pāṭha opening vallī 2, "# end.2" the one after it (our shanti.2.end). The witnesses divide
some anuvākas into paragraphs differently, so each anuvāka is compared as one run of letters, and every difference is
printed with the paragraph of ours it falls in. Not compared: the closing words of an anuvāka (इति … ऽनुवाकः, the last
line of our last paragraph) and of a vallī (our `iti` items), which the witnesses word differently; spaces, daṇḍas,
bars, numbers, hyphens; ॐ is read as ओं; spellings the library's standard makes one (a class nasal or ं, a final म्
or ं, ꣳ) and candrabindu for anusvāra are read alike; a consonant with virama before a space and a vowel is the
consonant with that vowel. At a space a witness's words written apart (in pausa, or with their vowels unjoined) are
read joined where our text has them joined (resolve() below). The only differences allowed are those listed in
reconciliation.md (source/witness-readings.tsv, per witness).
Usage: python3 tools/works/taittiriya-upanishad/source/check.py [-v]
       … check.py --write   appends every difference left to witness-readings.tsv (only once each is reviewed)
"""
import difflib, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'text')); import standard
ITEMS = [x for x in textfile.read(os.path.join(HERE, '..', 'text.txt')) if x['y'] != 'iti']
ANUVAKA_CLOSE = re.compile(r'^इत(?:ि |्य)\S*ऽनुवाकः ॥$')

VOW = 'अआइईउऊऋएऐओऔ'
MATRA = dict(zip(VOW, ['', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ']))
SIGNS = 'ािीुूृेैोौ'
CONS = '[क-हळ]'

def letters(s, spaces=False):
    """The letters compared; '|' marks a daṇḍa (a word before it may stand in pausa), and, with
    spaces, '_' a space (a witness's words may be left apart, in pausa or with their vowels unjoined)."""
    s = s.replace('ॐ', 'ओं').replace('ऽ', '').replace('र्ऋ', 'रृ').replace(':', 'ः').replace('ॢ', '्लृ')
    s = s.replace('\u200d', '').replace('\u200c', '').replace('ꣳ', 'ं').replace('ग्ं', 'ं').replace('ँ', 'ं')
    s = re.sub(r'[ञन]्(\s*)श', r'ञ्\1छ', s).replace('च्श', 'च्छ')            # n + ś: ñś, ñch (Pāṇini 8.4.63)
    s = re.sub(r'[0-9०-९\-—()]', ' ', s)
    s = re.sub(r'\s*[।॥|,;/.]+[\s।॥|,;/.]*', '|', s.strip())
    s = re.sub('(' + CONS + ')्\\s+([' + VOW + '])', lambda m: m.group(1) + MATRA[m.group(2)], s)
    s = re.sub('ं\\s+([' + VOW + '])', lambda m: 'म' + MATRA[m.group(1)], s)   # a final m before a vowel, as ं
    s = re.sub('[ङञणनम]्\\s+(?=[' + ''.join(standard.STOPS) + '])', 'ं', s)    # a class nasal at a word's end
    if spaces: s = re.sub(r'\s+', '_', s)
    s = re.sub(r'\s+', '', s).strip('|')
    s = standard._FOLD_NASAL.sub('ं', s)
    return re.sub('म्(?=[क-हळ_|]|$)', 'ं', s)

def joins(tail, nxt):
    """(how many letters of tail, how many of nxt, the joined form) for a word ending in tail before nxt, when the
    first is written in pausa or the two vowels are left apart."""
    out = []
    v = nxt[:1]
    vm = MATRA.get(v)
    last = tail[-1:]
    if last == 'ः':
        for r in ['', 'ो', 'स्', 'श्', 'ष्', 'र्']: out.append((1, 0, r))
        if v == 'अ': out.append((1, 1, 'ोऽ')); out.append((1, 1, 'ो'))
        if vm is not None: out.append((1, 1, 'र' + vm))
    elif last == '्':
        c = tail[-2:-1]
        for r in {'त': 'दनचजलड', 'क': 'गङ', 'ट': 'डण', 'प': 'बम', 'न': 'ञण'}.get(c, ''): out.append((2, 0, r + '्'))
        if c == 'न': out += [(2, 0, 'ंश्'), (2, 0, 'ंस्'), (2, 0, 'ं')]
        if c == 'त' and v == 'ह': out.append((2, 1, 'द्ध'))
        if c == 'त' and v == 'श': out.append((2, 1, 'च्छ'))
        if c in 'तकटप' and vm is not None: out.append((2, 1, {'त': 'द', 'क': 'ग', 'ट': 'ड', 'प': 'ब'}[c] + vm))
    elif last == 'ं' and vm is not None: out.append((1, 1, 'म' + vm))
    elif vm is not None:
        left = last if last in SIGNS else ''
        if left or re.match(CONS, last):
            out += [(len(left), 1, m) for m in merged(left, v)]
            if left == 'े': out.append((1, 0, ''))
            if left and left in 'ैौ': out.append((1, 0, {'ै': 'ा', 'ौ': 'ाव'}[left]))     # ai, au before a vowel
    return out

def merged(left, v):
    """The joined forms of a word ending in `left` (a vowel sign, or '' for a consonant's a) before the vowel v."""
    if left in ('', 'ा'):
        return {'अ': ['ा'], 'आ': ['ा'], 'इ': ['े'], 'ई': ['े'], 'उ': ['ो'], 'ऊ': ['ो'], 'ए': ['ै'], 'ऐ': ['ै'], 'ओ': ['ौ'],
                'औ': ['ौ'], 'ऋ': ['र्']}.get(v, []) + (['ो'] if v == 'ओ' else [])     # a + om is om
    if left in 'िी': return ['ी'] if v in 'इई' else ['्य' + MATRA[v]]
    if left in 'ुू': return ['ू'] if v in 'उऊ' else ['्व' + MATRA[v]]
    if left == 'ृ': return ['्र' + MATRA[v]]
    if left in 'ेो' and v == 'अ': return [left + 'ऽ', left]
    return []

def resolve(w, o):
    """w with its marks ('|', '_') taken out: at each, the joined form where o has it (near the same place), else the
    two words as w writes them. '#' in w (our breaks between verses) is kept."""
    T = re.split('[|_]', w)
    at0, n = [], 0
    for t in T[:-1]: n += len(t.replace('#', '')); at0.append(n)
    sm = difflib.SequenceMatcher(None, plain(w), o, autojunk=False)
    blocks = sm.get_matching_blocks()
    def at(p):
        for a, b, m in blocks:
            if a <= p <= a + m: return b + p - a
        return min(len(o), p)
    for i in range(len(T) - 2, -1, -1):
        left, right = T[i], T[i + 1]
        lo, hi = left.replace('#', '')[-7:], right.replace('#', '')[:7]
        if len(lo) == len(left.replace('#', '')) and lo[:1] in VOW: lo = lo[1:]     # it may still join the word before
        q = at(at0[i]); win = o[max(0, q - 40):q + 40]
        join = left + right
        if lo + hi not in win and lo and hi:
            for nl, nr, r in joins(lo[-3:], hi[:3]):
                if lo[:len(lo) - nl] + r + hi[nr:] in win:
                    join = left[:len(left) - nl] + r + right[nr:]; break
        T[i:i + 2] = [join]
    return T[0]

def section(i):
    """Our item id → the witness files' section: 1.3.2 → 1.3, shanti.2 → shanti.2, shanti.2.end → end.2."""
    if i.startswith('shanti.'): return 'end.' + i.split('.')[1] if i.endswith('.end') else i
    return i.rsplit('.', 1)[0]

def ours():
    """{section: [(item id, letters)]}"""
    out = {}
    for x in ITEMS:
        v = [l for l in x['v'] if not ANUVAKA_CLOSE.match(l.strip())]
        out.setdefault(section(x['id']), []).append((x['id'], letters('\n'.join(v))))
    return out

NORM = {   # a witness's own way of typing a letter, read as the letter (reconciliation.md, "The witnesses")
    'iitk.txt': [('ध्द', 'द्ध'), ('ड्ग', 'ङ्ग'), ('ड्क', 'ङ्क'), ('ड्घ', 'ङ्घ')],
}

def witness(path):
    W, k = {}, '0'
    norm = NORM.get(os.path.basename(path), [])
    for blk in re.split(r'\n\s*\n', open(path, encoding='utf-8').read().strip()):
        blk = blk.strip()
        if blk.startswith('# '): k = blk[2:].strip(); continue
        for a, b in norm: blk = blk.replace(a, b)
        W.setdefault(k, []).append(letters(blk, True))
    return {k: '|'.join(v) for k, v in W.items()}

def plain(s): return re.sub('[|_#]', '', s)

# The witnesses' own readings, one per line of witness-readings.tsv (witness file, our item, the witness's letters, ours,
# kind; letters as letters() and resolve() leave them), applied in order, each to its first place in the khaṇḍa
# (reconciliation.md, "The witnesses' own readings").
READINGS = os.path.join(HERE, 'witness-readings.tsv')
READING = {}
if os.path.exists(READINGS):
    for line in open(READINGS, encoding='utf-8').read().split('\n')[1:]:
        if line.strip():
            f = line.split('\t'); READING.setdefault(f[0], []).append((f[1], f[2], f[3]))

LACKS = {   # witness file: our paragraphs whose text it does not have (witnesses.py)
    'iitk.txt': ['1.5.2'],
}

def compare(name, k, w, items, verbose):
    """The differences of witness w (marked letters) from our section k: [(item id, witness, ours, context)]."""
    items = [x for x in items if x[0] not in LACKS.get(name, ())]
    if not items: return []
    o = '#'.join(t for _, t in items)
    w = resolve(w, plain(o)).replace('ऽ', '')
    o = resolve(o, w).replace('ऽ', '')
    parts = o.split('#'); starts, n = [], 0
    for (i, _), t in zip(items, parts): starts.append((n, i)); n += len(t)
    o = ''.join(parts)
    ids = {i for i, _ in items}
    for n, (vid, a, b) in enumerate(READING.get(name, [])):
        if vid in ids and a in w: w = w.replace(a, b, 1); USED.add((name, n))
    if '--write' in sys.argv: return list(readings(name, w, o, starts))
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, w, o, autojunk=False).get_opcodes():
        if op == 'equal': continue
        s0, vid = [x for x in starts if x[0] <= j1][-1]
        out.append((vid, w[max(0, i1 - 4):i2 + 4], o[max(0, j1 - 4):j2 + 4], o[max(0, j1 - 15):j2 + 15], j1 - s0, j2 - s0, w[i1:i2], o[j1:j2]))
    return out

def readings(name, w, o, starts):
    """The differences left, as lines for witness-readings.tsv: each a place that is unique in w, with its kind."""
    while w != o:
        ops = [x for x in difflib.SequenceMatcher(None, w, o, autojunk=False).get_opcodes() if x[0] != 'equal']
        op, i1, i2, j1, j2 = ops[0]
        for x in ops[1:]:                                   # differences close together are one reading
            if x[1] - i2 > 6: break
            i2, j2 = x[2], x[4]
        c = 3
        while True:
            a, b = w[max(0, i1 - c):i2 + c], o[max(0, j1 - c):j2 + c]
            if a and w.count(a) == 1: break
            c += 1
        vid = [x for x in starts if x[0] <= j1][-1][1]
        kind = 'omits' if not w[i1:i2] and j2 - j1 > 12 else 'adds' if not o[j1:j2] and i2 - i1 > 12 else 'own'
        yield '\t'.join([name, vid, a, b, kind])
        w = w.replace(a, b, 1)

USED = set()

def main():
    O, bad, verbose = ours(), 0, '-v' in sys.argv
    for path in sorted(glob.glob(os.path.join(HERE, 'witness', '*.txt'))):
        name = os.path.basename(path)
        W = witness(path)
        n = 0
        for k, items in O.items():
            if k not in W: continue
            if '--write' in sys.argv: WRITE.extend(compare(name, k, W[k], items, verbose)); continue
            for vid, a, b, ctx, *_ in compare(name, k, W[k], items, verbose):
                n += 1
                print('≠ %s %s [%s → %s]' % (name, vid, a, b) + ('   …%s…' % ctx if verbose else ''))
        missing = [k for k in O if k not in W]
        print('%s: %d sections compared, %d differences%s' % (name, len(O) - len(missing), n,
              ('; not in it: ' + ', '.join(missing)) if missing else ''))
        bad += n
    if '--write' in sys.argv:
        old = open(READINGS, encoding='utf-8').read().split('\n')[1:] if os.path.exists(READINGS) else []
        open(READINGS, 'w', encoding='utf-8').write('\n'.join(['witness\titem\twitness reads\tours\tkind'] +
                                                            [l for l in old if l.strip()] + WRITE) + '\n')
        print(len(WRITE), 'readings added to', READINGS); return
    for name, R in READING.items():
        for n, (vid, a, b) in enumerate(R):
            if (name, n) not in USED: print('listed but not found:', name, vid, a); bad += 1
    sys.exit(1 if bad else 0)

WRITE = []

if __name__ == '__main__':
    main()
