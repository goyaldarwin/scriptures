"""upanishads.org.in's Bṛhadāraṇyaka (one page per mantra, /u/brihadaranyaka/p/<a.b.n>) → source/witness/upanishads-org-in.txt.

Usage: python3 witness_upanishads_org.py <folder of the saved pages, <a.b.n>.html>
The pages are private (scriptures-data: <work path>/printouts/upanishads-org-in/brihadaranyaka-pages.tar.gz, unpacked). Only each page's Devanagari
(p.sloka, its lines split at <br>) is written, a "# a.b.n" line before each mantra; the page's English
(Max Müller's translation) and its transliteration are not kept.
"""
import html, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

def key(ref): return tuple(int(x) for x in ref.split('.'))

def sloka(path):
    h = open(path, encoding='utf-8').read()
    m = re.search(r'<p class="sloka" lang="sa">(.*?)</p>', h, re.S)
    if not m: raise SystemExit('no p.sloka in ' + path)
    lines = [html.unescape(re.sub(r'<[^>]+>', '', l)) for l in re.split(r'<br\s*/?>', m.group(1))]
    return [unicodedata.normalize('NFC', re.sub(r'\s+', ' ', l.replace('​', '')).strip()) for l in lines if l.strip()]

if __name__ == '__main__':
    folder = sys.argv[1]
    refs = sorted((f[:-5] for f in os.listdir(folder) if re.fullmatch(r'\d+\.\d+\.\d+\.html', f)), key=key)
    out = ['# upanishads.org.in, Bṛhadāraṇyaka Upaniṣad: the Devanagari of each mantra page (made by witness_upanishads_org.py)']
    for r in refs: out += ['', '# ' + r] + sloka(os.path.join(folder, r + '.html'))
    os.makedirs(os.path.join(HERE, 'witness'), exist_ok=True)
    open(os.path.join(HERE, 'witness', 'upanishads-org-in.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(len(refs), 'mantras')
