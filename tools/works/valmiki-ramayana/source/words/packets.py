"""Word packets for writing the Sanskrit word meanings of a kāṇḍa: for every distinct word of the kāṇḍa (by the
app's lookup key, folded) not yet in the work's glossary, up to three verses it occurs in and the word-by-word
glosses the two witnesses give for those verses (IIT Kanpur in Devanagari; valmikiramayan.net converted from
ITRANS), pre-selected to the glosses that look like the word. Every gloss of each verse, by witness, goes to
<out dir>/verse_glosses.json, printed by glosses.py when the pre-selection misses. An entry's English is the
witnesses' gloss as they give it (BRIEF.md; docs/PLAYBOOK.md §4).

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
    """each verse id → the witness verse it shares most text with (searched across the whole kāṇḍa), with the
    verses either side (the witnesses divide verses differently)"""
    norms = [w['norm'] for w in WV]
    res = {}
    for it in items:
        q = align.norm_line(' '.join(it['v']))
        m = process.extractOne(q, norms, scorer=fuzz.partial_ratio)
        if m and m[1] >= 65:
            j = m[2]; res[it['id']] = [x for x in (j - 1, j, j + 1) if 0 <= x < len(norms)]
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

def refresh(kd, iitk, vr, files):
    """rebuild the contexts' glosses of existing batch files (their words unchanged)"""
    items = [i for i in textfile.read(os.path.join(HERE, '..', '..', 'text.txt')) if i['id'].startswith(kd + '.')]
    byid = {i['id']: i for i in items}
    I = witness_verses(json.load(open(iitk)), 'iitk', kd); V = witness_verses(json.load(open(vr)), 'vr', kd)
    mi = match_verses(items, I); mv = match_verses(items, V)
    for f in files:
        W = json.load(open(f))
        for w in W:
            for c in w['contexts']:
                gl = [g for j in mi.get(c['id'], []) for g in I[j]['gl']] + [g for j in mv.get(c['id'], []) for g in V[j]['gl']]
                c['glosses'] = candidates(w['word'], gl)
        json.dump(W, open(f, 'w'), ensure_ascii=False, indent=0)
        print(f, sum(1 for w in W if any(c['glosses'] for c in w['contexts'])), 'of', len(W), 'with glosses')

def main():
    if sys.argv[1] == '--refresh':
        return refresh(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
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
    json.dump({it['id']: {'iitk': [g for j in mi.get(it['id'], []) for g in I[j]['gl']],
                          'vr': [g for j in mv.get(it['id'], []) for g in V[j]['gl']]} for it in items},
              open(os.path.join(out, 'verse_glosses.json'), 'w'), ensure_ascii=False)
    W = list(words.values())
    for b in range(0, len(W), size):
        json.dump(W[b:b + size], open(os.path.join(out, f'{kd}-{b // size + 1:03d}.json'), 'w'), ensure_ascii=False, indent=0)
    print(kd, len(W), 'words;', (len(W) + size - 1) // size, 'batches;',
          sum(1 for w in W if any(c['glosses'] for c in w['contexts'])), 'with at least one gloss')

if __name__ == '__main__':
    main()
