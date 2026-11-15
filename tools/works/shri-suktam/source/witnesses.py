"""Śrī Sūkta: the raw witness downloads → source/witness/<site>.txt (Devanagari runs for check.py).

Usage: python3 witnesses.py <dir>
<dir> holds the raw downloads as stored in scriptures-data at hinduism/veda/rigveda/samhita/shri-suktam/printouts/:
  wikisource/श्रीसूक्तम्.wiki.txt   Sanskrit Wikisource, raw wikitext of https://sa.wikisource.org/wiki/श्रीसूक्तम्. The page
      holds two texts: the first, 27 verses (→ wikisource-1.txt; its verse 19, पद्मानने पद्मविपत्रे…, is our 24 in
      another wording, and it lacks our 23, 25–31 and 36), and the second, headed "अन्यः पाठः", 36 verses in our order
      (→ wikisource-2.txt). The page names no edition; the two are compared separately, as they differ.
  gretil/sa_RgvedakhilAni.xml       GRETIL's Ṛgveda khilāni (TEI, IAST, words and compound members joined with "."),
      https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_RgvedakhilAni.xml, from Scheftelowitz's edition (Breslau
      1906) of a Kashmir manuscript: khila 2.6 has our ṛks 1–15 (2.6.1–15) and, in its own order, our 20–22 and 32–36,
      the verses after them given as variants ("alt" lines: our 16–19, 23–26, 29–31). It lacks our 27–28 and 37.
      Its IAST is made Devanagari with the Kaṭha Upaniṣad's converter (tools/works/katha-upanishad/source/settle.py →
      iast2deva_word), after the vowels its "." keeps apart are joined by the rules of sandhi (join below, with the
      places of hiatus our text keeps); its page and verse marks (|.(.p.72.)., //6) are dropped.
"""
import importlib.util, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..'))
from sukta_witness import write_witness
spec = importlib.util.spec_from_file_location('katha', os.path.join(HERE, '..', '..', 'katha-upanishad', 'source', 'settle.py'))
katha = importlib.util.module_from_spec(spec); spec.loader.exec_module(katha)

V = 'aāiīuūṛeo'
# where the text keeps two vowels apart (a visarga or an e dropped before a vowel), as ours does
HIATUS = {('ma', 'āvaha'), ('mama', 'āvaha'), ('bāhyā', 'alakṣmīḥ'), ('mātā', 'āyuṣmantam'), ('divo', 'abhrasya')}

def join(a, b):
    """Two IAST words the khila's "." keeps apart, joined (vowel sandhi only; consonants it has already joined)."""
    if not a or not b or a[-1] not in V + 'i' or b[0] not in V:
        if a.endswith('ai') and b[:1] in V: return a[:-2] + 'ā' + b
        if a.endswith('au') and b[:1] in V: return a[:-2] + 'āv' + b
        return a + b
    x, y = a[-1], b[0]; y2 = b[:2] if b[:2] in ('ai', 'au') else y
    if x in 'aā':
        r = {'a': 'ā', 'ā': 'ā', 'i': 'e', 'ī': 'e', 'u': 'o', 'ū': 'o', 'ṛ': 'ar', 'e': 'ai', 'o': 'au', 'ai': 'ai', 'au': 'au'}[y2]
        return a[:-1] + r + b[len(y2):]
    if x in 'iī': return a[:-1] + ('ī' + b[1:] if y in 'iī' else 'y' + b)
    if x in 'uū': return a[:-1] + ('ū' + b[1:] if y in 'uū' else 'v' + b)
    if x in 'eo': return a + ("'" + b[1:] if y == 'a' else ' ' + b)
    return a + b

def gretil(line):
    line = re.sub(r'\|\.\(\.?p\.\d+\.?\)\.|//\d*|/', ' ', line)
    out = []
    for chunk in line.split():
        ws = [w for w in chunk.split('.') if w]
        s, prev = '', None
        for w in ws: s, prev = (s + ' ' + w if (prev, w) in HIATUS else join(s, w)), w
        out.append(' '.join(katha.iast2deva_word(w) for w in s.split()))
    return ' '.join(out)

KHILA = {'m%02d' % k: ['2.6.%d' % k] for k in range(1, 16)}
KHILA.update({'m16': ['2.6.alt16'], 'm17': ['2.6.alt17'], 'm18': ['2.6.alt18'], 'm19': ['2.6.alt19'], 'm20': ['2.6.20'],
              'm21': ['2.6.21'], 'm22': ['2.6.22'], 'm23': ['2.6.alt24'], 'm24': ['2.6.alt25'], 'm25': ['2.6.alt26'],
              'm26': ['2.6.alt27'], 'm29': ['2.6.alt28'], 'm30': ['2.6.alt29'], 'm31': ['2.6.alt30'], 'm32': ['2.6.23'],
              'm33': ['2.6.25'], 'm34': ['2.6.26'], 'm35': ['2.6.24'], 'm36': ['2.6.29']})
WS1 = {k: 'm%02d' % k for k in range(1, 19)}
WS1.update({19: 'm24', 20: 'm19', 21: 'm20', 22: 'm21', 23: 'm22', 24: 'm32', 25: 'm33', 26: 'm34', 27: 'm35'})

def verses(t):
    """Wikisource's verses by their number: {n: text}"""
    out = {}
    for m in re.finditer(r'(.*?)॥\s*([०-९]+)\s*॥', t, re.S):
        n = int(''.join(str('०१२३४५६७८९'.index(c)) for c in m.group(2)))
        out[n] = re.sub(r'<br>|<poem>|\{\{.*?\}\}', ' ', m.group(1), flags=re.S)
    return out

if __name__ == '__main__':
    w = open(os.path.join(sys.argv[1], 'wikisource', 'श्रीसूक्तम्.wiki.txt'), encoding='utf-8').read()
    one, two = w.split('==अन्यः पाठः==')
    one = one[one.index('<poem>') + 6:one.index('</poem>')]
    V1, V2 = verses(one), verses(two)
    assert sorted(V1) == list(range(1, 28)) and sorted(V2) == list(range(1, 37)), (sorted(V1), sorted(V2))
    write_witness(os.path.join(HERE, 'witness', 'wikisource-1.txt'), [(WS1[n], WS1[n], V1[n]) for n in sorted(V1, key=lambda n: WS1[n])])
    write_witness(os.path.join(HERE, 'witness', 'wikisource-2.txt'), [('m%02d' % n, 'm%02d' % n, V2[n]) for n in sorted(V2)])
    x = open(os.path.join(sys.argv[1], 'gretil', 'sa_RgvedakhilAni.xml'), encoding='utf-8').read()
    L = {}
    for m in re.finditer(r'<l xml:id="RvKh_(2\.6\.(?:alt)?\d+)[a-z]">(.*?)</l>', x): L.setdefault(m.group(1), []).append(m.group(2))
    write_witness(os.path.join(HERE, 'witness', 'gretil-khila.txt'),
                  [(i, i, ' '.join(gretil(l) for r in KHILA[i] for l in L[r])) for i in sorted(KHILA)])
