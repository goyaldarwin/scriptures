"""Muṇḍaka Upaniṣad: the web witnesses' raw downloads (scriptures-data) → witness/*.txt, in check.py's format.

  IIT Kanpur Heritage: the reader API's JSON, <work path>/printouts/iitk/batch-*.json; the mantra is the verse's primary
      मूलम्; the khaṇḍa's closing words inside the last mantra (इति मुण्डकोपनिषदि …) are their own block. → witness/iitk.txt
  upanishads.org.in: one page per mantra, <work path>/printouts/upanishads-org/<m.k.n>.html; the mantra is the page's
      <p class="sloka" lang="sa">. It prints no śānti and no closing words. → witness/upanishads-org.txt
  Sanskrit Wikisource: the page's wikitext, <work path>/printouts/wikisource/mundakopanishad.wiki, the text inside
      <poem>. → witness/wikisource.txt
  Vedic Heritage Portal: the page's HTML, <work path>/printouts/vedicheritage/mundakopanishad.html, the lines of
      <div id="videotext">. → witness/vedicheritage.txt

The last two print the śānti, a heading before each khaṇḍa (॥ प्रथममुण्डके प्रथमः खण्डः ॥), the khaṇḍas' closing
words, and after 3.2 the Upaniṣad's colophon and the śānti again: the headings, the invocations (श्रीः, ॐ ब्रह्मणे नमः)
and everything after the last khaṇḍa's closing words are left out (reconciliation.md). Every witness numbers the
mantras muṇḍaka.khaṇḍa.mantra, as the text does.
Usage: python3 witnesses.py <the folder printouts/ of the work in a scriptures-data clone>
"""
import glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))
ORD = {'प्रथम': '1', 'द्वितीय': '2', 'तृतीय': '3'}
HEADING = re.compile(r'^॥\s*(प्रथम|द्वितीय|तृतीय)\s*मुण्डके\s+(प्रथम|द्वितीय)ः\s+खण्डः\s*॥$')
ITI = re.compile(r'^(॥\s*)?इति मुण्डकोपनिषदि')
SKIP = re.compile(r'^॥\s*(श्रीः|मुण्डकोपनिषत्|ॐ ब्रह्मणे नमः)\s*॥$')
END = re.compile(r'॥\s*(?:[०-९]+\.[०-९]+\.)?([०-९]+)\s*॥$')
COLOPHON = 'इत्यथर्ववेदीय'

def key(ref): return tuple(int(x) for x in ref.split('.'))

def write(name, blocks):
    """blocks: (id, text) with id shanti.1, m.k.n or m.k.iti, in order."""
    out, sec = [], None
    for vid, text in blocks:
        text = text.strip()
        if vid != 'shanti.1':
            m, k, n = vid.split('.')
            if m + '.' + k != sec: sec = m + '.' + k; out.append('# ' + sec)
            if n != 'iti': text = END.sub('', text).strip() + ' ॥ %s॥' % DEV(n)
        out.append(text)
    open(os.path.join(HERE, 'witness', name), 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print(name + ':', sum(v.split('.')[-1].isdigit() and v != 'shanti.1' for v, _ in blocks), 'mantras,', len(blocks), 'blocks')

def from_lines(lines):
    """The lines of a page that prints the whole text (Wikisource, Vedic Heritage) → blocks."""
    blocks, cur, sec = [], [], None
    for l in (x.strip() for x in lines):
        if not l or SKIP.match(l): continue
        if COLOPHON in l: break
        h = HEADING.match(l)
        if h: sec = ORD[h.group(1)] + '.' + ORD[h.group(2)]; continue
        if ITI.match(l): blocks.append((sec + '.iti', l)); continue
        cur.append(l)
        if sec is None and 'शान्तिः शान्तिः' in l: blocks.append(('shanti.1', '\n'.join(cur))); cur = []; continue
        e = END.search(l)
        if e: blocks.append(('%s.%d' % (sec, int(e.group(1).translate(str.maketrans('०१२३४५६७८९', '0123456789')))), '\n'.join(cur))); cur = []
    assert not cur, cur
    return blocks

def main(printouts):
    ik = {}
    for p in sorted(glob.glob(os.path.join(printouts, 'iitk', 'batch-[0-9][0-9][0-9].json'))):
        for v in json.load(open(p, encoding='utf-8'))['verses']:
            (m,) = [x for x in v['moolams'] if x['is_primary']]
            ik[v['ref']] = [l.strip() for l in m['text'].split('\n') if l.strip()]
    blocks = []
    for ref in sorted(ik, key=key):
        lines = ik[ref]
        blocks.append((ref, '\n'.join(l for l in lines if not ITI.match(l))))
        blocks += [(ref.rsplit('.', 1)[0] + '.iti', l) for l in lines if ITI.match(l)]
    write('iitk.txt', blocks)

    uo = []
    for p in glob.glob(os.path.join(printouts, 'upanishads-org', '*.*.*.html')):
        ref = os.path.basename(p)[:-5]
        (m,) = re.findall(r'<p class="sloka" lang="sa">(.*?)</p>', open(p, encoding='utf-8').read(), re.S)
        lines = html.unescape(re.sub(r'<br\s*/?>', '\n', m)).split('\n')       # 2.2.7 has an empty line inside
        uo.append((ref, '\n'.join(l.strip() for l in lines if l.strip())))
    write('upanishads-org.txt', sorted(uo, key=lambda x: key(x[0])))

    ws = open(os.path.join(printouts, 'wikisource', 'mundakopanishad.wiki'), encoding='utf-8').read()
    (poem,) = re.findall(r'<poem>(.*?)</poem>', ws, re.S)
    write('wikisource.txt', from_lines(re.sub(r'<[^>]+>', '', poem).split('\n')))

    vh = open(os.path.join(printouts, 'vedicheritage', 'mundakopanishad.html'), encoding='utf-8').read()
    (div,) = re.findall(r'<div id="videotext"[^>]*>(.*?)</div>', vh, re.S)
    # U+E001, a private-use glyph of the page's font, stands for ꣳ (its Kaṭha writes तꣳ ह कुमारꣳ with it)
    text = html.unescape(re.sub(r'<br\s*/?>|</?p[^>]*>', '\n', div.replace('&#8211;', ''))).replace('\ue001', 'ꣳ')
    write('vedicheritage.txt', from_lines(re.sub(r'<[^>]+>', '', text).split('\n')))

if __name__ == '__main__':
    main(sys.argv[1])
