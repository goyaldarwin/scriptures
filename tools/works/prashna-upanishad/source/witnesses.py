"""Praśna Upaniṣad: the web witnesses' raw downloads (scriptures-data) → witness/*.txt, in check.py's format.

Raw files are in scriptures-data at <work path>/printouts/<site>/:
  upanishads.org.in: one page per mantra, upanishads-org/p-<praśna.mantra>.html; the mantra is the page's
      <p class="sloka" lang="sa">. No śānti. → witness/upanishads-org.txt
  IIT Kanpur Heritage: the reader API's JSON, iitk/batch-*.json; the mantra is the verse's primary मूलम्. Its refs are
      <praśna>.1.<mantra>, but some of its verses are copies of others: its 4.1.12 is a second copy of 3.12 (it ends
      इति तृतीयः प्रश्नः) and its 5.1.8–5.1.11 a second copy of 4.8–4.11 (the last ends इति चतुर्थः प्रश्नः), which makes
      its 72 (16, 13, 12, 12, 11, 8) of the others' 67; and its 1.1.5 and 1.1.7 hold 1.6 and 1.8 again, so it lacks 1.5
      and 1.7 (check.py → ABSENT). The copies are left out (REPEATS); the first copy of each verse is compared. Its closing words are left out; the śānti it prints after 6.8 goes after "# end". → witness/iitk.txt
  Sanskrit Wikisource, प्रश्न उपनिषद् (action=raw): the <pre> blocks; its "== n ==" headings do not fall at the praśnas'
      boundaries, so a praśna ends at its closing words (इति प्रश्नोपनिषदि … प्रश्नः). → witness/wikisource.txt
  Vedic Heritage Portal, prashnopanishad.html: the page's #videotext, divided like Wikisource. → witness/vedicheritage.txt
  GRETIL, sa_praznopaniSad-comm.xml (IAST, with Śaṅkara's bhāṣya): the mūla of each "START PrUp p.m" block, converted
      to Devanagari by settle.py's tr2deva_word (the conversion this work uses for the base page's transliteration);
      GRETIL writes a word's final consonant apart from the next word (śaibyaś ca, pippalādam upasannāḥ), so a final
      consonant is joined to the word after it. → witness/gretil.txt
Every witness numbers the mantras praśna.mantra (16, 13, 12, 11, 7, 8), as the text does.
Usage: python3 witnesses.py <the folder printouts/ of the work in a scriptures-data clone>
"""
import glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from settle import tr2deva_word, IV, V
DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))
NUM = re.compile(r'\s*॥\s*(?:[०-९0-9]+\.)?([०-९0-9]+)\s*॥\s*$')
CLOSE = re.compile(r'^\s*इति प्रश्नोपनिषदि \S+ प्रश्नः\s*॥?\s*$')
REPEATS = {'1.1.5': '1.6', '1.1.7': '1.8', '4.1.12': '3.12', '5.1.8': '4.8', '5.1.9': '4.9', '5.1.10': '4.10', '5.1.11': '4.11'}

def write(name, shanti, verses, end=''):
    """verses: [(praśna, mantra, text)] in order."""
    out, sec = ([shanti.strip()] if shanti else []), None
    for p, m, text in verses:
        if p != sec: sec = p; out.append('# %d' % p)
        out.append(NUM.sub('', text.strip()) + ' ॥ %s॥' % DEV(m))
    if end: out += ['# end', end.strip()]
    open(os.path.join(HERE, 'witness', name), 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print(name + ':', len(verses), 'mantras')

def by_closing(lines):
    """Lines of a whole text (śānti, six praśnas each ending with its closing words, the closing śānti) →
    (śānti, [(praśna, mantra, text)], what follows the sixth praśna). A mantra ends at its ॥ N॥; where a mantra's number
    is missing (Wikisource's 3.4), the blank line after it ends it."""
    shanti, verses, cur, p, before = [], [], [], 1, True
    for l in lines:
        l = l.strip()
        if not l:
            if cur and cur[-1] is not None: cur.append(None)
            continue
        if CLOSE.match(l):
            assert not cur, (p, cur); p += 1
            if p == 7: break
            continue
        if before:
            if l.startswith('ॐ शान्तिः'): shanti.append(l); before = False; continue
            if 'सुकेशा' in l: before = False
            else: shanti.append(l); continue
        cur.append(l)
        n = NUM.search(l)
        if n:
            n = int(n.group(1).translate(str.maketrans('०१२३४५६७८९', '0123456789')))
            last = verses[-1][1] if verses and verses[-1][0] == p else 0
            if n == last + 2 and None in cur:
                b = cur.index(None); verses.append((p, last + 1, '\n'.join(cur[:b]))); cur = cur[b + 1:]
            assert n == len([v for v in verses if v[0] == p]) + 1, (p, n)
            verses.append((p, n, '\n'.join(x for x in cur if x is not None))); cur = []
    i = lines.index(next(l for l in lines if CLOSE.match(l.strip()) and 'षष्ठः' in l))
    return '\n'.join(shanti), verses, '\n'.join(l.strip() for l in lines[i + 1:] if l.strip())

def join_iast(text):
    """GRETIL's IAST → Devanagari words, a final consonant joined to the next word (pippalādam upasannāḥ → one word)."""
    out = []
    for w in text.replace('-', ' ').split():
        d = tr2deva_word(w)
        if out and out[-1].endswith('्'):
            first = next((k for k, v in IV.items() if d.startswith(v)), None)
            out[-1] = out[-1][:-1] + V[first] + d[len(IV[first]):] if first else out[-1] + d
        else: out.append(d)
    return ' '.join(out)

def upanishads_org(printouts):
    uo = []
    for f in glob.glob(os.path.join(printouts, 'upanishads-org', 'p-*.html')):
        p, m = map(int, re.search(r'p-(\d+)\.(\d+)\.html$', f).groups())
        (t,) = re.findall(r'<p class="sloka" lang="sa">(.*?)</p>', open(f, encoding='utf-8').read(), re.S)
        uo.append((p, m, html.unescape(re.sub(r'<br\s*/?>', '\n', t))))
    write('upanishads-org.txt', '', sorted(uo))

def iitk(printouts):
    ik = {}
    for f in sorted(glob.glob(os.path.join(printouts, 'iitk', 'batch-[0-9][0-9][0-9].json'))):
        for v in json.load(open(f, encoding='utf-8'))['verses']:
            (m,) = [x for x in v['moolams'] if x['is_primary']]
            ik[v['ref']] = m['text']
    assert len(ik) == 72, len(ik)
    verses, end = [], ''
    for ref, t in ik.items():
        if ref in REPEATS: continue
        p, _, m = map(int, ref.split('.'))
        t = re.sub(r'[ \t]+\n', '\n', t)
        c = re.search(r'[।\s]*इति (?:प्रश्नोपनिषदि )?\S+ प्रश्नः\s*।*', t)
        if c:
            if p == 6: end = t[c.end():]
            t = t[:c.start()]
        verses.append((p, m, t))
    write('iitk.txt', '', sorted(verses), end)

def wikisource(printouts):
    s = open(os.path.join(printouts, 'wikisource', 'prashnopanishad.wiki'), encoding='utf-8').read()
    lines = '\n'.join(re.findall(r'<pre>(.*?)</pre>', s, re.S)).split('\n')
    write('wikisource.txt', *by_closing(lines))

def vedicheritage(printouts):
    s = open(os.path.join(printouts, 'vedicheritage', 'prashnopanishad.html'), encoding='utf-8').read()
    (t,) = re.findall(r'<div id="videotext"[^>]*>(.*?)</div>', s, re.S)
    t = html.unescape(re.sub(r'<br\s*/?>|</p>', '\n', t)).replace('¬', '').replace('\ue001', 'ं')
    lines = [re.sub(r'<[^>]+>', '', l) for l in t.split('\n')]
    lines = [l for l in lines if l.strip() and 'प्रश्नोपनिषद् ॥' not in l]
    write('vedicheritage.txt', *by_closing(lines))

def gretil(printouts):
    s = open(os.path.join(printouts, 'gretil', 'sa_praznopaniSad-comm.xml'), encoding='utf-8').read()
    verses = []
    for m in re.finditer(r'<p>START PrUp (\d+)\.(\d+)\s*(.*?)</div>', s, re.S):
        t = re.sub(r'<[^>]+>', '', m.group(3))
        t = re.sub(r'[|\s]*PrUp_[\d.]+[|\s]*', '', t)
        lines = [join_iast(re.sub(r'[|/,;:!?"]', ' ', l)) for l in t.split('\n') if l.strip()]
        verses.append((int(m.group(1)), int(m.group(2)), '\n'.join(lines)))
    body = s[s.index('<body>'):s.index('START PrUp 1.1')]
    sh = [join_iast(re.sub(r'[|/!]', ' ', re.sub(r'<[^>]+>', '', l))) for l in re.findall(r'<l>(.*?)</l>', body)]
    write('gretil.txt', '\n'.join(sh), verses)

def main(printouts):
    os.makedirs(os.path.join(HERE, 'witness'), exist_ok=True)
    upanishads_org(printouts); iitk(printouts); wikisource(printouts); vedicheritage(printouts); gretil(printouts)

if __name__ == '__main__':
    main(sys.argv[1])
