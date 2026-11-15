"""Chāndogya Upaniṣad: the witnesses' raw downloads (scriptures-data, <work path>/printouts/) → witness/*.txt, in check.py's format.

  upanishads.org.in: one page per mantra, upanishads-org/p-<a>-<k>-<m>.html; the mantra is the page's
      <p class="sloka" lang="sa">. No śānti. → witness/upanishads-org.txt
  IIT Kanpur Heritage: the reader API's JSON, iitk/batch-*.json; the mantra is the verse's primary मूलम्, its closing
      words (इति … खण्डः ।।, इति … अध्यायः ।।) left out; a ref with no मूलम् (4.3.1–8, 6.13.4–6) is left out, and so is
      a ref holding the same text as the next one (the reader's misfiled mantras). No śānti.
      → witness/iitk.txt
  Sanskrit Wikisource: wikitext, wikisource/chandogya-<0…8>.wiki (the index page, then one page per adhyāya; the
      first holds the opening śānti, the last the closing one, which is not compared); links, tags and the closing words are left out, and the khaṇḍas are numbered in their order on the page.
      → witness/wikisource.txt
  GRETIL: TEI XML with Śaṅkara's bhāṣya, gretil/sa_chAndogyopaniSad-comm.xml; the mantra is the bold text (<hi> or <l>) ending
      || ChUp_a,k.m ||, its IAST read into Devanagari word by word (GRETIL separates the words, often undoing the
      sandhi of vowels: check.py joins them). The śānti is the paragraph before the text. → witness/gretil.txt

Usage: python3 witnesses.py <the folder printouts/ of the work in a scriptures-data clone>
"""
import difflib, glob, html, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DIG = '०१२३४५६७८९'
DEV = lambda n: str(n).translate(str.maketrans('0123456789', DIG))
def num(s): return int(s.translate(str.maketrans(DIG, '0123456789')))
def key(ref): return tuple(int(x) for x in ref.split('.'))

def write(name, verses, shanti=None):
    """verses: [(a.k.m, text)]; written in khaṇḍa order, each ending ॥ m॥, after the śānti block (no number)."""
    out, sec = [], None
    if shanti: out.append(shanti.strip())
    for ref, text in sorted(verses, key=lambda x: key(x[0])):
        a, k, m = ref.split('.')
        if a + '.' + k != sec: sec = a + '.' + k; out.append('# ' + sec)
        text = re.sub(r'\s*॥\s*[०-९]+\s*॥\s*$', '', '\n'.join(l.strip() for l in text.strip().split('\n') if l.strip()))
        out.append(text + ' ॥ %s॥' % DEV(m))
    open(os.path.join(HERE, 'witness', name), 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print(name + ':', len(verses), 'mantras' + (' and the śānti' if shanti else ''))

def upanishads_org(P):
    out = []
    for p in glob.glob(os.path.join(P, 'upanishads-org', 'p-*.html')):
        ref = re.search(r'p-([\d-]+)\.html$', p).group(1).replace('-', '.')
        (m,) = re.findall(r'<p class="sloka" lang="sa">(.*?)</p>', open(p, encoding='utf-8').read(), re.S)
        out.append((ref, html.unescape(re.sub(r'<br\s*/?>', '\n', m))))
    write('upanishads-org.txt', out)

CLOSE = re.compile(r'\s*\bइत(?:ि |्य)\S*\s*\S*\s*(?:खण्डः|ध्यायः)\s*(?:।।|॥)?\s*$')

def iitk(P):
    out = {}
    for p in sorted(glob.glob(os.path.join(P, 'iitk', 'batch-[0-9][0-9][0-9].json'))):
        for v in json.load(open(p, encoding='utf-8'))['verses']:
            prim = [x for x in v['moolams'] if x['is_primary']]
            if not prim: continue
            lines = [CLOSE.sub('', l).strip() for l in prim[0]['text'].split('\n')]
            lines = [l for l in lines if l]
            out[v['ref']] = '\n'.join(lines)
    # the reader files some mantras under the number before their own, so two refs hold the same text and the
    # mantra of the first is missing (1.4.2 holds 1.4.3): the earlier copy is left out (check.py → LACKS)
    flat = {r: re.sub(r'\s|%u2022', '', t) for r, t in out.items()}
    refs = sorted(out, key=key)
    for r, nxt in zip(refs, refs[1:]):
        if difflib.SequenceMatcher(None, flat[r], flat[nxt], autojunk=False).ratio() > 0.95:
            del out[r]; print('iitk: %s holds the text of %s; left out' % (r, nxt))
    write('iitk.txt', list(out.items()))

KHANDAS = [13, 24, 19, 17, 24, 16, 26, 15]

def wiki_plain(s):
    s = re.sub(r'<ref>.*?</ref>|\[\[File:[^\]]*\]\]', '', s, flags=re.S)
    s = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\[https?://\S+ ([^\]]*)\]', r'\1', s)
    return re.sub(r'<[^>]*>', '', s)

def wikisource(P):
    first = wiki_plain(open(os.path.join(P, 'wikisource', 'chandogya-1.wiki'), encoding='utf-8').read())
    shanti = re.search(r'(ॐ आप्यायन्तु.*?शान्तिः शान्तिः शान्तिः ॥)', first, re.S).group(1)
    out = []
    for a in range(1, 9):
        s = wiki_plain(open(os.path.join(P, 'wikisource', 'chandogya-%d.wiki' % a), encoding='utf-8').read())
        s = re.split(r'\n==[^=]', s.split('॥ इति छान्दोग्यो')[0])[0]          # the page's links section
        if a == 8: s = s.split('ॐ आप्यायन्तु')[0]                          # the closing śānti after 8.15
        heads = list(re.finditer(r'॥\s*(?:[\d.]+\s*)?(\S+) खण्डः\s*॥', s))
        assert len(heads) == KHANDAS[a - 1], (a, len(heads))      # counted in order (the page spells one द्वितियः)
        for k, h in enumerate(heads, 1):
            body = s[h.end(): heads[k].start() if k < len(heads) else len(s)]
            body = re.split(r'॥\s*इति ', body)[0]
            parts = re.split(r'॥\s*([०-९]+)\s*॥', body)
            if re.search('[क-ह]', parts[-1]): print('wikisource: text after the last mantra of', a, k, repr(parts[-1][:200]))
            for i in range(0, len(parts) - 1, 2):
                out.append(('%d.%d.%d' % (a, k, num(parts[i + 1])), ' '.join(parts[i].split())))
    write('wikisource.txt', out, ' '.join(shanti.split()))

# IAST → Devanagari, one word at a time (a word-final consonant keeps its virama)
V = [('ai', 'ऐ', 'ै'), ('au', 'औ', 'ौ'), ('ā', 'आ', 'ा'), ('ī', 'ई', 'ी'), ('ū', 'ऊ', 'ू'), ('ṝ', 'ॠ', 'ॄ'), ('ṛ', 'ऋ', 'ृ'),
     ('ḷ', 'ऌ', 'ॢ'), ('e', 'ए', 'े'), ('o', 'ओ', 'ो'), ('a', 'अ', ''), ('i', 'इ', 'ि'), ('u', 'उ', 'ु')]
C = [('kh', 'ख'), ('k', 'क'), ('gh', 'घ'), ('g', 'ग'), ('ṅ', 'ङ'), ('ch', 'छ'), ('c', 'च'), ('jh', 'झ'), ('j', 'ज'), ('ñ', 'ञ'),
     ('ṭh', 'ठ'), ('ṭ', 'ट'), ('ḍh', 'ढ'), ('ḍ', 'ड'), ('ṇ', 'ण'), ('th', 'थ'), ('t', 'त'), ('dh', 'ध'), ('d', 'द'), ('n', 'न'),
     ('ph', 'फ'), ('p', 'प'), ('bh', 'भ'), ('b', 'ब'), ('m', 'म'), ('y', 'य'), ('r', 'र'), ('l', 'ल'), ('v', 'व'), ('ś', 'श'),
     ('ṣ', 'ष'), ('s', 'स'), ('h', 'ह')]
SIGN = {'ṃ': 'ं', 'ṁ': 'ं', 'ḥ': 'ः', "'": 'ऽ', '’': 'ऽ', '|': '।', '/': '।'}

def deva_word(s):
    out, i, prev_c = [], 0, False
    while i < len(s):
        lat = next((x for x in C if s.startswith(x[0], i)), None)
        if lat: out.append(('्' if prev_c else '') + lat[1]); i += len(lat[0]); prev_c = True; continue
        vow = next((x for x in V if s.startswith(x[0], i)), None)
        if vow: out.append(vow[2] if prev_c else vow[1]); i += len(vow[0]); prev_c = False; continue
        out.append(('्' if prev_c else '') + SIGN.get(s[i], s[i])); i += 1; prev_c = False
    if prev_c: out.append('्')
    return ''.join(out)

def deva(s):
    s = unicodedata.normalize('NFC', s).lower()
    s = re.sub(r"\s+'", " '", s)
    return unicodedata.normalize('NFC', ' '.join(deva_word(w) for w in s.split()))

def gretil(P):
    x = open(os.path.join(P, 'gretil', 'sa_chAndogyopaniSad-comm.xml'), encoding='utf-8').read()
    body = x[x.index('<body>'):]
    sh = re.search(r'(āpyāyantu.*?santu) //</p>\s*<p>(oṃ śāntiḥ śāntiḥ śāntiḥ)', body, re.S)
    out = []
    for _, b in re.findall(r'<(hi|l) rend="bold">(.*?)</\1>', body, re.S):
        parts = re.split(r'\|\|\s*ChUp_(\d+),(\d+)\.(\d+)\s*\|\|', b)
        if len(parts) == 1: continue
        assert not parts[-1].strip(), b[:200]
        for i in range(0, len(parts) - 1, 4):
            out.append(('%s.%s.%s' % tuple(parts[i + 1:i + 4]), deva(parts[i].replace('\n', ' '))))
    assert len(out) == len(set(re.findall(r'ChUp_(\d+),(\d+)\.(\d+) \|\|', body))), len(out)
    write('gretil.txt', out, deva(sh.group(1).replace(',', ' |') + ' || ' + sh.group(2)) + ' ॥')

if __name__ == '__main__':
    P = sys.argv[1]
    os.makedirs(os.path.join(HERE, 'witness'), exist_ok=True)
    upanishads_org(P); iitk(P); wikisource(P); gretil(P)
