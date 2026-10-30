"""Look up Sanskrit words in Monier-Williams (1899) and Apte (1890), from the Cologne Digital Sanskrit Lexicon.

    python3 tools/meanings/sanskrit_dict.py fetch                 # download the two dictionaries (~62 MB)
    python3 tools/meanings/sanskrit_dict.py check                 # exit 1 unless both are downloaded
    python3 tools/meanings/sanskrit_dict.py look शान्त निर्भर …     # print their entries for each word (Devanagari)

The download lives outside the repository (CACHE below), so every new machine or cloud session starts without it:
run `fetch` (or `check`) before any meaning is written, reviewed or applied. `look` downloads them itself when missing;
`prepare.py` and `apply_batches.py` refuse to run without them.

Used to check our word meanings (library/glossary/sa.json, and Sanskrit-derived Awadhi words) and our meanings of
Sanskrit verses: tools/meanings/style.md §11. The data comes from the lexicon's own repository on GitHub
(github.com/sanskrit-lexicon/csl-orig) and is kept outside the repository (CACHE below); take the facts from it
(sense, grammar), never its sentences.
"""
import os, re, sys, urllib.request

CACHE = os.environ.get('SANSKRIT_DICT_DIR', os.path.expanduser('~/.cache/scriptures-dict'))
DICTS = {'mw': 'Monier-Williams 1899', 'ap90': 'Apte 1890'}
URL = 'https://raw.githubusercontent.com/sanskrit-lexicon/csl-orig/master/v02/{0}/{0}.txt'

# Devanagari → SLP1 (the lexicon's key spelling)
V = {'अ': 'a', 'आ': 'A', 'इ': 'i', 'ई': 'I', 'उ': 'u', 'ऊ': 'U', 'ऋ': 'f', 'ॠ': 'F', 'ऌ': 'x', 'ए': 'e', 'ऐ': 'E', 'ओ': 'o', 'औ': 'O'}
M = {'ा': 'A', 'ि': 'i', 'ी': 'I', 'ु': 'u', 'ू': 'U', 'ृ': 'f', 'ॄ': 'F', 'ॢ': 'x', 'े': 'e', 'ै': 'E', 'ो': 'o', 'ौ': 'O'}
C = dict(zip('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह',
             'k K g G N c C j J Y w W q Q R t T d D n p P b B m y r l v S z s h'.split()))
def slp1(w):
    out, i = [], 0
    w = w.replace('‌', '').replace('‍', '').replace('ऽ', '')
    while i < len(w):
        ch = w[i]
        if ch in V: out.append(V[ch])
        elif ch in C:
            out.append(C[ch]); nx = w[i + 1] if i + 1 < len(w) else ''
            if nx == '्': i += 1
            elif nx in M: out.append(M[nx]); i += 1
            else: out.append('a')
        elif ch == 'ं': out.append('M')
        elif ch == 'ः': out.append('H')
        elif ch == 'ँ': out.append('~')
        i += 1
    return ''.join(out)

def missing():
    return [d for d in DICTS if not os.path.exists(os.path.join(CACHE, d + '.txt'))]

def fetch():
    os.makedirs(CACHE, exist_ok=True)
    for d in DICTS:
        p = os.path.join(CACHE, d + '.txt')
        if not os.path.exists(p): urllib.request.urlretrieve(URL.format(d), p); print('fetched', d)

_IDX = {}
def index(d):
    if d not in _IDX:
        if missing(): fetch()
        idx = {}
        txt = open(os.path.join(CACHE, d + '.txt'), encoding='utf-8').read()
        for m in re.finditer(r'<L>[^\n]*?<k1>([^<\n]+)[^\n]*\n(.*?)<LEND>', txt, re.S):
            idx.setdefault(m.group(1), []).append(m.group(2).strip())
        _IDX[d] = idx
    return _IDX[d]

def clean(e): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', e.replace('¦', ':'))).strip()

def look(word, limit=6):
    k = slp1(word); out = []
    for d, name in DICTS.items():
        es = index(d).get(k) or index(d).get(k.rstrip('M').rstrip('H')) or []
        for e in es[:limit]: out.append(f'{name}: {clean(e)[:400]}')
    return k, out

if __name__ == '__main__':
    if sys.argv[1:2] == ['fetch']: fetch()
    elif sys.argv[1:2] == ['check']:
        m = missing()
        if m: sys.exit(f'The Sanskrit dictionaries are not downloaded ({", ".join(m)}): run python3 tools/meanings/sanskrit_dict.py fetch')
        print('Monier-Williams and Apte are downloaded:', CACHE)
    elif sys.argv[1:2] == ['look']:
        for w in sys.argv[2:]:
            k, out = look(w); print(f'== {w} ({k})'); print('\n'.join(out) or '   (not found as a headword; try the stem)')
    else: print(__doc__)
