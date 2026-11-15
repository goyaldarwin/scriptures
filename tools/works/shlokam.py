"""Helpers for works whose text is a shlokam.org page saved as HTML (the six Sūktas: tools/works/*-suktam/source/).

page(): the page's verse blocks (div.verse-section), each with the page's verse number (data-verse), its Devanagari
lines (div.detail-sanskrit) and its transliteration lines (the div.detail-text after it), split at <br>, with zero-width
spaces removed and empty lines dropped. The page's English (its colloquial spelling, translation and word meanings) is
the publisher's and is never read here.
tr2deva(): the page's transliteration (ISO-like: ē ō, Ch छ, ch च, gͫ ꣳ, ḻ ळ, ṃ anusvāra, the svaras as ◌̍ ◌̠ ◌̎) back to
Devanagari, the second witness of every line (the Śrī Rudram's method, tools/works/shri-rudram/source/rudram_text.py).
key(): a line reduced to what both scripts must share, for comparing them.
"""
import html.parser, re, unicodedata

class _Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.field, self.want, self.depth, self.buf = [], None, None, 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = (a.get('class') or '').split()
        if tag == 'div' and 'verse-section' in cls:
            self.blocks.append({'verse': a.get('data-verse', ''), 'v': None, 't': None}); self.want = None
        if tag == 'div' and a.get('data-field') in ('sanskrit', 'roman'):
            self.want = a['data-field']
        if tag == 'div' and 'detail-text' in cls and self.field is None and self.want:
            self.field, self.depth, self.buf = self.want, 1, []; return
        if self.field:
            if tag == 'div': self.depth += 1
            if tag == 'br': self.buf.append('\n')

    def handle_endtag(self, tag):
        if self.field and tag == 'div':
            self.depth -= 1
            if self.depth == 0:
                text = unicodedata.normalize('NFC', ''.join(self.buf).replace('​', ''))
                lines = [re.sub(r'\s+', ' ', l).strip() for l in text.split('\n')]
                self.blocks[-1]['v' if self.field == 'sanskrit' else 't'] = [l for l in lines if l]
                self.field = self.want = None

    def handle_data(self, data):
        if self.field: self.buf.append(data)

def page(path):
    p = _Page(); p.feed(open(path, encoding='utf-8').read())
    assert p.blocks and all(b['v'] and b['t'] for b in p.blocks), path
    return p.blocks

SV = '॒॑᳚'
V = [('ai', 'ऐ', 'ै'), ('au', 'औ', 'ौ'), ('ā', 'आ', 'ा'), ('ī', 'ई', 'ी'), ('ū', 'ऊ', 'ू'), ('ṝ', 'ॠ', 'ॄ'), ('r̥', 'ऋ', 'ृ'),
     ('ṛ', 'ऋ', 'ृ'), ('ḷ', 'ऌ', 'ॢ'), ('ē', 'ए', 'े'), ('e', 'ए', 'े'), ('ō', 'ओ', 'ो'), ('o', 'ओ', 'ो'), ('a', 'अ', ''),
     ('i', 'इ', 'ि'), ('u', 'उ', 'ु')]
C = [('kh', 'ख'), ('k', 'क'), ('gh', 'घ'), ('g', 'ग'), ('ṅ', 'ङ'), ('chh', 'छ'), ('ch', 'च'), ('c', 'च'), ('jh', 'झ'),
     ('j', 'ज'), ('ñ', 'ञ'), ('ṭh', 'ठ'), ('ṭ', 'ट'), ('ḍh', 'ढ'), ('ḍ', 'ड'), ('ṇ', 'ण'), ('th', 'थ'), ('t', 'त'), ('dh', 'ध'),
     ('d', 'द'), ('n', 'न'), ('ph', 'फ'), ('p', 'प'), ('bh', 'भ'), ('b', 'ब'), ('m', 'म'), ('y', 'य'), ('r', 'र'), ('ḻ', 'ळ'),
     ('l', 'ल'), ('v', 'व'), ('ś', 'श'), ('ṣ', 'ष'), ('s', 'स'), ('h', 'ह')]
ACC = {'̍': '॑', '̠': '॒', '̱': '॒', '̎': '᳚'}

def tr2deva(s):
    s = unicodedata.normalize('NFC', s).replace('​', '')
    s = s.replace('Ch', 'chh').lower().replace('gͫ', 'ꣳ')
    out, i, prevC = [], 0, False
    def acc(j):
        a = ''
        while j < len(s) and s[j] in ACC: a += ACC[s[j]]; j += 1
        return a, j
    while i < len(s):
        ch = s[i]
        for lat, dv in C:
            if s.startswith(lat, i):
                if prevC: out.append('्')
                out.append(dv); i += len(lat); prevC = True
                break
        else:
            for lat, ind, mat in V:
                if s.startswith(lat, i):
                    out.append(mat if prevC else ind); i += len(lat); prevC = False
                    a, i = acc(i); out.append(a); break
            else:
                if ch == 'ṃ':          # gṃ after a consonant is the Vedic ग्ं (anusvāra after a half g)
                    out.append('्ं' if prevC else 'ं'); a, i = acc(i + 1); out.append(a); prevC = False; continue
                if prevC: out.append('्'); prevC = False
                if ch == 'ḥ': out.append('ः')
                elif ch in "'’": out.append('ऽ')
                elif ch in ACC: out.append(ACC[ch])
                else: out.append(ch)
                i += 1
    if prevC: out.append('्')
    r = unicodedata.normalize('NFC', ''.join(out))
    return re.sub('([%s]+)([ःं])' % SV, r'\2\1', r)        # नम॑ः → नमः॑ (the page puts the svara after ः and ं)

NASAL = 'ङञणनम'
def key(s):
    """Letters and svaras only, with the two scripts' conventions folded: ॐ / ōṃ, the ँ the Devanagari writes before
    य व ल (the transliteration has none), and a nasal before a consonant written as its class letter or as ṃ."""
    s = unicodedata.normalize('NFC', s).replace('ॐ', 'ओं').replace('ँ', '')
    s = re.sub(r'[\s\-–.,।॥|`0-9०-९]', '', s)
    s = re.sub('[%s]्(?=[क-ह])' % NASAL, 'ं', s)
    return s

def house(l):
    """The page's daṇḍas as the library writes them: spaced, and the verse number compact (॥१२॥)."""
    l = re.sub(r'\s*॥\s*([०-९]+)\s*॥', r' ॥\1॥', l)
    l = l.replace('।', ' । ')
    l = re.sub(r'\s*॥(?![०-९])(?<![०-९]॥)', ' ॥', l)
    l = re.sub(r'(?<![०-९])॥(?=[^\s०-९])', '॥ ', l)
    return re.sub(r'\s+', ' ', l).strip()

def compare(blocks, allowed):
    """The page's Devanagari against its own transliteration, line by line: {(verse, line index)} that differ, which
    must be exactly `allowed` (settle.py names each and says why)."""
    differ = set()
    for b in blocks:
        assert len(b['v']) == len(b['t']), (b['verse'], b['v'], b['t'])
        for i, (v, t) in enumerate(zip(b['v'], b['t'])):
            if key(v) != key(tr2deva(t)): differ.add((b['verse'], i))
    assert differ == set(allowed), sorted(differ ^ set(allowed))

def settled(raw, heading, witness, fix):
    """The page's blocks (raw: source/<name>_raw.json) → {page verse: [lines]}: the Devanagari checked against the
    transliteration (`witness`: the lines allowed to differ), the page's own headings dropped (`heading`: {verse:
    first line}, an editor's title, not recited; our topics replace them), the corrections made (`fix`: [(verse,
    wrong, right)], each found exactly once in that verse), and the daṇḍas written as the library writes them."""
    import json
    B = json.load(open(raw, encoding='utf-8'))
    compare(B, witness)
    L = {}
    for b in B:
        v = list(b['v'])
        if b['verse'] in heading: assert v[0] == heading[b['verse']], (b['verse'], v[0]); v = v[1:]
        L[b['verse']] = '\n'.join(v)
    assert set(heading) <= set(L)
    for verse, a, b in fix:
        assert L[verse].count(a) == 1, (verse, a, L[verse])
        L[verse] = L[verse].replace(a, b)
    return {k: [house(l) for l in t.split('\n')] for k, t in L.items()}
