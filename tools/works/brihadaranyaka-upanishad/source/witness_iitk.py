"""IIT Kanpur Heritage's Bṛhadāraṇyaka (reader API batches, BRU) → source/witness/iitk.txt.

Usage: python3 witness_iitk.py <folder with batch-*.json>
The JSON is private (scriptures-data: <work path>/printouts/iitk/BRU.tar.gz, unpacked). Only each mantra's primary mūla
(moolams[is_primary]) is written, a "# a.b.n" line before it, its lines split where the site breaks them; the
brāhmaṇa's closing words that the site runs into its last mantra (इति प्रथमो ब्राह्मणम्।।) are left out, and the
site's translations and commentaries are not kept.
"""
import glob, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
CLOSE = re.compile(r'\s*(?:इति\s+\S+|इत्य\S+)\s+ब्राह्मणम्[^\n]*$')   # … इति षष्ठं ब्राह्मणम् ।। इति प्रथमोऽध्यायः ।।

def key(ref): return tuple(int(x) for x in ref.split('.'))

if __name__ == '__main__':
    V = {}
    for f in sorted(glob.glob(os.path.join(sys.argv[1], 'batch-*.json'))):
        for v in json.load(open(f, encoding='utf-8'))['verses']:
            m = [x for x in v['moolams'] if x.get('is_primary')]
            if m: V[v['ref']] = m[0]['text']
    out = ['# IIT Kanpur Heritage (heritage.iitk.ac.in), BRU: the primary mūla of each mantra (made by witness_iitk.py)']
    for r in sorted(V, key=key):
        t = unicodedata.normalize('NFC', V[r].replace('​', ''))
        t = CLOSE.sub('', t)
        out += ['', '# ' + r] + [re.sub(r'\s+', ' ', l).strip() for l in t.split('\n') if l.strip()]
    open(os.path.join(HERE, 'witness', 'iitk.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(len(V), 'mantras')
