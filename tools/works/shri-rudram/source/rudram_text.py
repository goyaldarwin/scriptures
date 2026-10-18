"""Helpers for settling the Devanagari of the shlokam.org printout (see settle.py).

norm_deva(): mends the PDF text layer's known breaks (identical svaras or vowel signs repeated, ःः, the Dravidian
short ऒ/ॊ/ॆ of the invocation lines, the श्ड़्ण्व cluster).  tr2deva(): the page's own transliteration back to
Devanagari, used as the second witness for every line."""
import re, unicodedata

SV = '॒॑᳚'                              # ॑ ॒ ᳚ as used on the page
MATRA = 'ािीुूृेैोौॢ'

def norm_deva(s):
    s = unicodedata.normalize('NFC', s)
    s = s.replace('​', '')
    s = re.sub('([%s])\\1+' % SV, r'\1', s)                              # शि॒॒ → शि॒
    for _ in range(2):
        s = re.sub('([%s])([%sं]?)\\1\\2' % (MATRA, SV), r'\1\2', s)      # व्या॒ा॒ → व्या॒, ज्ञाा → ज्ञा, व्यांां → व्यां
    s = s.replace('ःः', 'ः').replace('ॊ', 'ो').replace('ॆ', 'े').replace('ऒ', 'ओ')
    s = s.replace('श्ड़्ण्व', 'शृण्व')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

V = [('ai', 'ऐ', 'ै'), ('au', 'औ', 'ौ'), ('ā', 'आ', 'ा'), ('ī', 'ई', 'ी'), ('ū', 'ऊ', 'ू'), ('ṝ', 'ॠ', 'ॄ'), ('ṛ', 'ऋ', 'ृ'),
     ('ḷ', 'ऌ', 'ॢ'), ('ē', 'ए', 'े'), ('e', 'ए', 'े'), ('ō', 'ओ', 'ो'), ('o', 'ओ', 'ो'), ('a', 'अ', ''), ('i', 'इ', 'ि'), ('u', 'उ', 'ु')]
C = [('kh', 'ख'), ('k', 'क'), ('gh', 'घ'), ('g', 'ग'), ('ṅ', 'ङ'), ('chh', 'छ'), ('ch', 'च'), ('c', 'च'), ('jh', 'झ'), ('j', 'ज'),
     ('ñ', 'ञ'), ('ṭh', 'ठ'), ('ṭ', 'ट'), ('ḍh', 'ढ'), ('ḍ', 'ड'), ('ṇ', 'ण'), ('th', 'थ'), ('t', 'त'), ('dh', 'ध'), ('d', 'द'),
     ('n', 'न'), ('ph', 'फ'), ('p', 'प'), ('bh', 'भ'), ('b', 'ब'), ('m', 'म'), ('y', 'य'), ('r', 'र'), ('l', 'ल'), ('v', 'व'),
     ('ś', 'श'), ('ṣ', 'ष'), ('s', 'स'), ('h', 'ह')]
ACC = {'̍': '॑', '̠': '॒', '̱': '॒', '̎': '᳚'}

def tr2deva(s):
    s = unicodedata.normalize('NFC', s).replace('​', '').lower()
    out, i, prevC = [], 0, False
    def acc(j):
        a = ''
        while j < len(s) and s[j] in ACC: a += ACC[s[j]]; j += 1
        return a, j
    while i < len(s):
        ch = s[i]
        if s.startswith('gͫ', i): out.append('ꣳ'); prevC = False; i += 2; continue
        for lat, dv in C:
            if s.startswith(lat, i):
                if prevC: out.append('्')
                out.append(dv); i += len(lat); prevC = True
                # g + (accent) + ṃ = the Vedic ग्ं (anusvāra after a half g)
                if lat == 'g':
                    a, j = acc(i)
                    if j < len(s) and s[j] == 'ṃ': out.append('्ं' + a); i = j + 1; prevC = False
                break
        else:
            for lat, ind, mat in V:
                if s.startswith(lat, i):
                    out.append(mat if prevC else ind); i += len(lat); prevC = False
                    a, i = acc(i); out.append(a); break
            else:
                if prevC and ch not in "ṃḥ'’-": pass
                if ch == 'ṃ': out.append('ं'); a, i = acc(i + 1); out.append(a); prevC = False; continue
                if ch == 'ḥ': out.append('ः'); i += 1; prevC = False; continue
                if prevC: out.append('्'); prevC = False
                if ch in "'’": out.append('ऽ')
                elif ch in ACC: out.append(ACC[ch])
                else: out.append(ch)
                i += 1
    if prevC: out.append('्')
    r = unicodedata.normalize('NFC', ''.join(out))
    return re.sub('([%s]+)([ःं])' % SV, r'\2\1', r)        # नम॑ः → नमः॑ (the page puts the svara after ः/ं)

def key(s, svara=True):
    """For comparison: no spaces, hyphens, dandas or digits; optionally no svaras."""
    s = re.sub(r'[\s\-–.,।॥0-9०-९|]', '', s)
    if not svara: s = re.sub('[%s]' % SV, '', s)
    return s
