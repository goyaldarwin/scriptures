"""Word packets for writing the Sanskrit word meanings of a kāṇḍa: for every distinct word of the kāṇḍa (by the
app's lookup key, folded) not yet in the work's glossary, up to three verses it occurs in and the word-by-word
glosses the two witnesses give for those verses (IIT Kanpur in Devanagari; valmikiramayan.net converted from
ITRANS). The glosses are aids to check against, never copied: the entry is written from them, Monier-Williams and
Apte (style.md §11).

    python3 packets.py <kāṇḍa> <iitk scrape> <valmikiramayan.net scrape> <out dir> [--size 250]
"""
import json, os, re, sys, collections, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'works')); sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, os.path.join(HERE, '..'))
import textfile, align
from text import standard
from rapidfuzz import fuzz, process
from indic_transliteration import sanscript

KANDAS = ['bala', 'ayodhya', 'aranya', 'kishkindha', 'sundara', 'yuddha', 'uttara']
PUNCT = re.compile(r'[।॥|,;:!?.()\[\]{}"“”‘’\'\-–—*०-९0-9]')

def key(t):
    return unicodedata.normalize('NFC', PUNCT.sub('', t))

def deva(itrans):
    return sanscript.transliterate(itrans, sanscript.ITRANS, sanscript.DEVANAGARI)

def witness_verses(W, kind, kd):
    k = W['kandas'][KANDAS.index(kd)]
    out = []
    for s in k['sargas']:
        for v in s['verses']:
            text = ' '.join(v['text']['dv'] if kind == 'iitk' else v['sanskrit'])
            gl = []
            for w in v.get('word_meanings') or []:
                if kind == 'iitk':
                    sa = (w.get('word') or {}).get('dv', '')
                else:
                    sa = deva(w.get('sanskrit', ''))
                if sa and w.get('meaning'):
                    gl.append([sa.strip(), w['meaning'].strip()])
            out.append({'text': text, 'norm': align.norm_line(text), 'gl': gl})
    return out

def match_verses(items, WV):
    """each verse id → indices of the witness verses whose text it shares (a sliding window, in order)"""
    norms = [w['norm'] for w in WV]
    res, pos = {}, 0
    for it in items:
        q = align.norm_line(' '.join(it['v']))
        lo, hi = max(0, pos - 30), min(len(norms), pos + 60)
        m = process.extractOne(q, norms[lo:hi], scorer=fuzz.partial_ratio)
        if m and m[1] >= 70:
            j = lo + m[2]; res[it['id']] = [j] + ([j + 1] if j + 1 < len(norms) and fuzz.partial_ratio(q, norms[j + 1]) >= 70 else [])
            pos = j
        else:
            res[it['id']] = []
    return res

def candidates(word, glosses):
    """the glosses whose Sanskrit shares a stretch with the word (sandhi changes only a word's edges, spellings
    differ by a letter: कर्शन / कर्षण); when none does, every gloss of the verse, for the checker to choose from"""
    wn = align.norm_line(word)
    out = []
    for sa, en in glosses:
        for tok in sa.split():
            tn = re.sub('[ंःािीुूृेैोौ्]+$', '', align.norm_line(tok))
            if len(tn) >= 2 and (tn in wn or (len(tn) >= 3 and fuzz.partial_ratio(tn, wn) >= 85)):
                out.append([sa, en]); break
    return out or [[sa, en] for sa, en in glosses]

def main():
    kd, iitk, vr, out = sys.argv[1:5]
    size = int(sys.argv[sys.argv.index('--size') + 1]) if '--size' in sys.argv else 250
    items = [i for i in textfile.read(os.path.join(HERE, '..', '..', 'text.txt')) if i['id'].startswith(kd + '.')]
    gloss_path = os.path.join(HERE, '..', '..', 'glossary', 'sa.json')
    have = set(json.load(open(gloss_path))) if os.path.exists(gloss_path) else set()
    have |= set(json.load(open(os.path.join(ROOT, 'library', 'glossary', 'sa.json'))))
    have_f = {standard.fold(k) for k in have}
    I = witness_verses(json.load(open(iitk)), 'iitk', kd) if kd != 'uttara' else []
    V = witness_verses(json.load(open(vr)), 'vr', kd) if kd != 'uttara' else []
    mi = match_verses(items, I) if I else {}
    mv = match_verses(items, V) if V else {}
    words = collections.OrderedDict()
    for it in items:
        std = [standard.sanskrit(l) for l in it['v']]
        gl = [g for j in mi.get(it['id'], []) for g in I[j]['gl']] + [g for j in mv.get(it['id'], []) for g in V[j]['gl']]
        for line in std:
            for t in line.split():
                k = key(t)
                if not k or standard.fold(k) in have_f:
                    continue
                f = standard.fold(k)
                e = words.setdefault(f, {'word': k, 'count': 0, 'contexts': []})
                e['count'] += 1
                if len(e['contexts']) < 3:
                    e['contexts'].append({'id': it['id'], 'verse': ' / '.join(std), 'glosses': candidates(k, gl)})
    os.makedirs(out, exist_ok=True)
    W = list(words.values())
    for b in range(0, len(W), size):
        json.dump(W[b:b + size], open(os.path.join(out, f'{kd}-{b // size + 1:03d}.json'), 'w'), ensure_ascii=False, indent=0)
    print(kd, len(W), 'words;', (len(W) + size - 1) // size, 'batches;',
          sum(1 for w in W if any(c['glosses'] for c in w['contexts'])), 'with at least one gloss')

if __name__ == '__main__':
    main()
