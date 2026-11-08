"""The work's own word meanings (glossary/sa.json) from the owner's word-by-word English glosses.

    python3 tools/works/shiva-purana/source/words.py <shiva-purana-drafts.json>

<shiva-purana-drafts.json> is in scriptures-data at hinduism/purana/mahapurana/shiva/meaning-records/en-scriptures/: the
owner's drafts, each verse of the copy with its English meaning and its words glossed one by one, in their split,
pausal forms (कथासारम् = "the essence of the stories"). The verse prints them joined by sandhi (कथासारं, ह्यब्रुवन्वचनं),
and a reader taps the word as printed, so:
  1. each verse's glosses are lined up with its printed words, the whole verse at once (a printed word takes 0–5
     glosses, the pairing that matches the sounds best wins); only a pairing whose sounds agree is used;
  2. a printed word made of several glossed words gets their glosses joined with "; ", in order;
  3. a word's senses across the work are gathered: the same gloss in another case is one sense (the form used most
     is kept), a gloss met once where the word has a sense met many times is left out (an alignment slip), and the
     senses that remain are joined with " / ", the most used first, as every dictionary of the library lists senses;
  4. a word the shared dictionary (library/glossary/sa.json) already has is left to it.
The entries are English only (`work.json` → "words": "partial"; Hindi, root and grammar are not written yet).
"""
import json, re, sys, os, difflib, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'works')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'text'))
import jsonio, textfile, standard

SP = re.compile(r'(वाच|ऊचुः|ऊचतुः|उचुः|ूचतुः|ूचुः|वाच्)$')

def skel(s):
    """A sound skeleton that survives sandhi at word ends."""
    s = unicodedata.normalize('NFC', s).replace('‍', '').replace('‌', '')
    s = re.sub(r'[ंःँ्ऽ]', '', s); s = re.sub(r'[ङञणनम](?=[क-ह])', '', s)
    return re.sub(r'[^ऀ-ॿ]', '', s)

def tokens(lines):
    out = []
    for l in lines:
        if SP.search(l) and len(l.split()) <= 3: continue          # a speaker's line
        out += [t.replace('-', '').replace('—', '') for t in re.split(r'[\s।॥०-९()]+', l) if re.search(r'[ऀ-ॿ]', t)]   # the app looks a word up without its hyphens
    return out

def align(toks, gl):
    """Pair each printed word with 0–5 consecutive glosses, best over the whole verse: [(word, [gloss…], ok)]."""
    n, m = len(toks), len(gl); INF = 1e9
    S = [skel(t) for t in toks]; G = [skel(g['word']) for g in gl]
    def cost(i, j1, j2):
        b = ''.join(G[j1:j2]); a = S[i]
        r = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a and b else 0
        return (1 - r) + 0.05 * (j2 - j1 - 1)
    D = [[INF] * (m + 1) for _ in range(n + 1)]; B = [[None] * (m + 1) for _ in range(n + 1)]; D[0][0] = 0
    for i in range(n):
        for j in range(m + 1):
            if D[i][j] >= INF: continue
            for k in range(0, 6):
                if j + k > m: break
                c = D[i][j] + (1.0 if k == 0 else cost(i, j, j + k))
                if c < D[i + 1][j + k]: D[i + 1][j + k] = c; B[i + 1][j + k] = (j, k)
        for j in range(m):
            if D[i + 1][j] + 1.0 < D[i + 1][j + 1]: D[i + 1][j + 1] = D[i + 1][j] + 1.0; B[i + 1][j + 1] = ('skip', j)
    out, i, j = [], n, m
    while i > 0:
        b = B[i][j]
        if b and b[0] == 'skip': j = b[1]; continue
        j0, k = b
        out.append((toks[i - 1], gl[j0:j0 + k], k > 0 and cost(i - 1, j0, j0 + k) < 0.35)); i -= 1; j = j0
    return out[::-1]

def main(drafts):
    E = json.load(open(drafts, encoding='utf-8'))
    W = {f"{c['ref']}#{v['seq']}": v['word_meanings'] for f in E['files'] for c in f['chapters'] for v in c['verses']}
    keys = json.load(open(os.path.join(HERE, 'keys.json'), encoding='utf-8'))
    T = {x['id']: x for x in textfile.read(os.path.join(HERE, '..', 'text.txt'))}
    senses = collections.defaultdict(collections.Counter); stat = collections.Counter()
    for vid, ks in keys.items():
        x = T[vid]
        if x['y'] == 'iti': continue
        for t, parts, ok in align(tokens(x['v']), [g for k in ks for g in W.get(k, [])]):
            stat['ok' if ok else 'not used'] += 1
            if ok: senses[t]['; '.join(re.sub(r'\s+', ' ', p['meaning']).strip().rstrip('.') for p in parts)] += 1
    shared = {standard.fold(k) for k in json.load(open(os.path.join(ROOT, 'library', 'glossary', 'sa.json'), encoding='utf-8'))}
    G = {}
    for w, C in senses.items():
        if standard.fold(w) in shared: stat['left to the shared dictionary'] += 1; continue
        one = collections.defaultdict(collections.Counter)            # one sense in any case: the form used most
        for g, n in C.items(): one[g.lower()][g] += n
        S = sorted(((sum(c.values()), c.most_common(1)[0][0]) for c in one.values()), reverse=True)
        top = S[0][0]
        S = [g for n, g in S if not (n == 1 and top >= 5)][:4]          # a lone gloss beside a common one: a slip
        G[w] = {'en': ' / '.join(S)}
    os.makedirs(os.path.join(HERE, '..', 'glossary'), exist_ok=True)
    jsonio.dump_glossary(os.path.join(HERE, '..', 'glossary', 'sa.json'), G)
    print(f"{len(G)} words; {dict(stat)}")

if __name__ == '__main__':
    main(sys.argv[1])
