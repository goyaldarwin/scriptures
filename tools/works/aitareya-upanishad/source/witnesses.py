"""Aitareya Upaniṣad: the web witnesses' raw downloads (scriptures-data) → witness/*.txt, in check.py's format.

  upanishads.org.in: one page per mantra, <work path>/printouts/upanishads-org/aitareya/p-<a.k.m>.html; the mantra
      is the page's <p class="sloka" lang="sa"> (Sri Aurobindo's text, CWSA 18). → witness/upanishads-org.txt
  IIT Kanpur Heritage: the reader API's JSON, <work path>/printouts/iitk/AIU/batch-*.json; the mantra is the
      verse's primary मूलम्, its khaṇḍa's closing words (इत्यैतरेयोपनिषदि …) left out. → witness/iitk.txt

Neither prints the śānti mantra. Their own numbering (adhyāya.khaṇḍa.mantra) is ours.
Usage: python3 witnesses.py <the folder printouts/ of the work in a scriptures-data clone>
"""
import glob, html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = lambda n: ''.join('०१२३४५६७८९'[int(c)] for c in str(n))

def write(name, verses):
    out, sec = [], None
    for ref, text in verses:
        a, k, m = ref.split('.')
        if a + '.' + k != sec: sec = a + '.' + k; out.append('# ' + sec)
        text = re.sub(r'\s*॥\s*[०-९]+\s*॥\s*$', '', text.strip())
        out.append(text + ' ॥ %s॥' % DEV(m))
    open(os.path.join(HERE, 'witness', name), 'w', encoding='utf-8').write('\n\n'.join(out) + '\n')
    print(name + ':', len(verses), 'mantras')

def key(ref): return tuple(int(x) for x in ref.split('.'))

def main(printouts):
    pages = glob.glob(os.path.join(printouts, 'upanishads-org', 'aitareya', 'p-*.html'))
    uo = []
    for p in pages:
        ref = re.search(r'p-([\d.]+)\.html$', p).group(1)
        s = open(p, encoding='utf-8').read()
        (m,) = re.findall(r'<p class="sloka" lang="sa">(.*?)</p>', s, re.S)
        uo.append((ref, html.unescape(re.sub(r'<br\s*/?>', '\n', m))))
    write('upanishads-org.txt', sorted(uo, key=lambda x: key(x[0])))
    ik = {}
    for p in sorted(glob.glob(os.path.join(printouts, 'iitk', 'AIU', 'batch-*.json'))):
        for v in json.load(open(p, encoding='utf-8'))['verses']:
            (m,) = [x for x in v['moolams'] if x['is_primary']]
            lines = [l.strip() for l in m['text'].split('\n') if l.strip() and not l.strip().startswith('इत्यैतरेय')]
            assert ik.get(v['ref'], lines) == lines, v['ref']     # the batches overlap; a repeated verse is the same
            ik[v['ref']] = lines
    write('iitk.txt', sorted(((r, '\n'.join(l)) for r, l in ik.items()), key=lambda x: key(x[0])))

if __name__ == '__main__':
    main(sys.argv[1])
