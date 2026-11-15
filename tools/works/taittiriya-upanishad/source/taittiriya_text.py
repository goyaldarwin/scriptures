"""Helpers for settling the Devanagari of the shlokam.org page (see settle.py).

tr2deva(): the page's own transliteration (IAST: c च, ch छ, gͫ ꣳ, ṃ anusvāra, m̐ candrabindu, ' avagraha, 3 pluta)
back to Devanagari, the second witness of every line. key(): a line reduced to its letters, for comparing the two."""
import re, unicodedata

V = [('ai', 'ऐ', 'ै'), ('au', 'औ', 'ौ'), ('ā', 'आ', 'ा'), ('ī', 'ई', 'ी'), ('ū', 'ऊ', 'ू'), ('ṝ', 'ॠ', 'ॄ'), ('ṛ', 'ऋ', 'ृ'),
     ('ḷ', 'ऌ', 'ॢ'), ('e', 'ए', 'े'), ('o', 'ओ', 'ो'), ('a', 'अ', ''), ('i', 'इ', 'ि'), ('u', 'उ', 'ु')]
C = [('kh', 'ख'), ('k', 'क'), ('gh', 'घ'), ('g', 'ग'), ('ṅ', 'ङ'), ('ch', 'छ'), ('c', 'च'), ('jh', 'झ'), ('j', 'ज'),
     ('ñ', 'ञ'), ('ṭh', 'ठ'), ('ṭ', 'ट'), ('ḍh', 'ढ'), ('ḍ', 'ड'), ('ṇ', 'ण'), ('th', 'थ'), ('t', 'त'), ('dh', 'ध'), ('d', 'द'),
     ('n', 'न'), ('ph', 'फ'), ('p', 'प'), ('bh', 'भ'), ('b', 'ब'), ('m', 'म'), ('y', 'य'), ('r', 'र'), ('l', 'ल'), ('v', 'व'),
     ('ś', 'श'), ('ṣ', 'ष'), ('s', 'स'), ('h', 'ह')]

def tr2deva(s):
    s = unicodedata.normalize('NFC', s).replace('​', '').lower()
    s = s.replace('gͫ', 'ꣳ').replace('m̐', 'ँ').replace('oṃ', 'ॐ')
    out, i, prevC = [], 0, False
    while i < len(s):
        for lat, dv in C:
            if s.startswith(lat, i):
                if prevC: out.append('्')
                out.append(dv); i += len(lat); prevC = True
                break
        else:
            for lat, ind, mat in V:
                if s.startswith(lat, i):
                    out.append(mat if prevC else ind); i += len(lat); prevC = False
                    break
            else:
                ch = s[i]; i += 1
                if prevC and ch != 'ँ': out.append('्')
                prevC = False
                out.append({'ṃ': 'ं', 'ḥ': 'ः', "'": 'ऽ', '’': 'ऽ', '.': '।'}.get(ch, ch))
    if prevC: out.append('्')
    return unicodedata.normalize('NFC', ''.join(out))

def key(s):
    """For comparison: letters only (no spaces, daṇḍas, digits or the page's stray `)."""
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'[\s\-–.,।॥|`0-9०-९]', '', s)
