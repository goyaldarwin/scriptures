"""The work's own word meanings (glossary/sa.json) from the owner's word-by-word glosses.

    python3 tools/works/durga-saptashati/source/words.py <durga-saptashati.json>

<durga-saptashati.json> is in scriptures-data at hinduism/stotra/durga/durga-saptashati/printouts/sanskritdocuments/:
each item of the owner's copy with its words glossed one by one in Hindi and English, in their split, pausal forms
(तम् "उससे / to him", आविष्टम् "घिरे हुए / overcome"). The verse prints them joined by sandhi (कृपयाविष्टमश्रुपूर्णाकुलेक्षणम्),
and a reader taps the word as printed, so:
  1. each verse's glosses are lined up with its printed words, the whole verse at once (a printed word takes 0–9
     glosses; the pairing whose sounds match best wins, by the letters or by the consonants alone, which vowel sandhi
     leaves: च + एव → चैव); only a pairing whose sounds agree is used;
  2. a printed word made of several glossed words gets their glosses joined with "; " in order, and its parts (`p`):
     each glossed word with its Hindi;
  3. a word's senses across the work are gathered: one sense per English gloss (the Hindi used most with it), the
     most used first, at most four, a gloss met once beside a sense met five times or more left out (an alignment
     slip); the senses are joined with " / ", as every dictionary of the library lists them;
  4. a word the shared dictionary (library/glossary/sa.json) already has is left to it;
  5. the glosses are put in the style of our dictionaries: square brackets round, the Devī for the Goddess, pronouns
     in lower case (me, you), and in Hindi the rules of our meanings (meanings.py → hi: postpositions joined, लिये, गये …);
  6. words_ours.json, beside this script, has the words the copy does not gloss (the colophons, the bījas):
     ours, written from Monier-Williams and Apte, which win over the gathered senses; and under "force" the long
     compounds whose pairing is right though its sounds score low (checked by eye).
Root and grammar are not written yet (README.md). It prints the words of the verses still without a meaning.
"""
import json, re, sys, os, difflib, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'works')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'text'))
import jsonio, textfile, standard
sys.path.insert(0, HERE); import meanings

SPEAKER = set()
PUNCT = re.compile(r'[\s।॥|,.;:!?\-—‘’“”\'"()\[\]०-९0-9]')

def clean(t):
    return unicodedata.normalize('NFC', PUNCT.sub('', t))

def skel(s):
    """A sound skeleton that survives sandhi at word ends."""
    s = unicodedata.normalize('NFC', s).replace('\u200d', '').replace('\u200c', '')
    s = re.sub(r'[ंःँ्ऽ]', '', s); s = re.sub(r'[ङञणनम](?=[क-ह])', '', s)
    return re.sub(r'[^\u0900-\u097F]', '', s)

def cons(s):
    """Consonants only: what is left of a word through vowel sandhi (च + एव → चैव, तु + एव + अहम् → त्वेवाहं)."""
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'(?<=[क-ह])्[यव]', '', s)                        # ह्य, त्व: the y, v of a vowel before another (हि, तु)
    s = re.sub(r'[मन]्$|[ंः]$', '', s).replace('ं', 'न').replace('ः', '')
    s = re.sub(r'[^क-ह]', '', s)
    return s.translate(str.maketrans('दचजलधङञणम', 'ततततथनननन'))   # a final t, n, m as sandhi writes it (यच्च, तल्लोक, सम्प)

def tokens(lines):
    return [k for l in lines if l not in SPEAKER for k in (clean(t) for t in l.split()) if k]

def align(toks, gl):
    """Pair each printed word with 0–9 consecutive glosses, best over the whole verse: [(word, [gloss…], ok)]."""
    n, m = len(toks), len(gl); INF = 1e9
    S = [skel(t) for t in toks]; G = [skel(g['word']) for g in gl]
    SC = [cons(t) for t in toks]; GC = [cons(g['word']) for g in gl]
    memo = {}
    def cost(i, j1, j2):
        if (i, j1, j2) not in memo:
            b = ''.join(G[j1:j2]); a = S[i]
            r = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a and b else 0
            ac, bc = SC[i], ''.join(GC[j1:j2])
            if len(ac) >= 2 and ac and bc: r = max(r, difflib.SequenceMatcher(None, ac, bc, autojunk=False).ratio() - 0.05)
            memo[i, j1, j2] = (1 - r) + 0.03 * (j2 - j1 - 1)
        return memo[i, j1, j2]
    D = [[INF] * (m + 1) for _ in range(n + 1)]; B = [[None] * (m + 1) for _ in range(n + 1)]; D[0][0] = 0
    for i in range(n):
        for j in range(m + 1):
            if D[i][j] >= INF: continue
            for k in range(0, 10):
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
        out.append((toks[i - 1], gl[j0:j0 + k], k > 0 and cost(i - 1, j0, j0 + k) < 0.34)); i -= 1; j = j0
    return out[::-1]

def tidy(s, lang):
    """A gloss in the style of our dictionaries: square brackets round; Hindi postpositions joined, as in our meanings."""
    s = re.sub(r'\s+', ' ', s).strip().rstrip('.;,').replace('[', '(').replace(']', ')')
    if lang == 'hi':
        s = meanings.hi(s, None)
        return s + '!' if s.startswith('हे ') and not s.endswith('!') and ';' not in s else s
    s = re.sub(r'\bGoddess\b', 'Devī', s)
    return re.sub(r'\b(Me|My|Mine|Myself|You|Your|Yours|Yourself|He|His|Him|Himself|She|Her|Hers|Herself)\b', lambda m: m.group(0).lower(), s)   # pronouns in lower case

def main(src):
    J = json.load(open(src, encoding='utf-8'))
    # a gloss of several words (मा स्म गमः, यत् यत्) is one gloss per word, each with the phrase's meaning
    T = textfile.read(os.path.join(HERE, '..', 'text.txt'))
    import make_text
    C = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8'))
    made = [m for m in make_text.items_of(J, C) if not m['id'].endswith('.iti')]
    its = [it for sec in J['sections'] for it in sec['items'] for _ in range(3 if '-' in (it['number'] or '') else 1)]
    W = {x['id']: [dict(g, word=w) for g in it['word_meanings'] for w in g['word'].split()] for x, it in zip(made, its)}
    for x, it in zip(made, its):          # adhyāya 5's triple namaskāras: the second and third mantras are नमस्तस्यै (नमो नमः)
        if '-' in (it['number'] or '') and x['id'] != f"5.{it['number'].split('-')[0]}":
            W[x['id']] = [g for g in W[x['id']] if g['word'] in ('नमः', 'तस्यै')][-4 if x['id'].endswith(it['number'].split('-')[1]) else -2:]
        elif '-' in (it['number'] or ''):  # the first: the stanza's line and one नमस्तस्यै
            gl = W[x['id']]; k = [i for i, g in enumerate(gl) if g['word'] == 'तस्यै'][0]; W[x['id']] = gl[:k + 1]
    O = json.load(open(os.path.join(HERE, 'words_ours.json'), encoding='utf-8')); force = O.get('force', {})
    senses = collections.defaultdict(collections.Counter); parts = collections.defaultdict(collections.Counter)
    stat = collections.Counter(); weak = []
    for x in T:
        if x['id'].endswith('.iti'): continue
        for t, gs, ok in align(tokens(x['v']), W[x['id']]):
            ok = ok or t in force.get(x['id'], [])
            if not ok: stat['not used'] += 1; weak.append((x['id'], t, [g['word'] for g in gs])); continue
            stat['ok'] += 1
            senses[t][('; '.join(tidy(g['hi'], 'hi') for g in gs), '; '.join(tidy(g['en'], 'en') for g in gs))] += 1
            if len(gs) > 1:
                parts[t][json.dumps([[g['word'], tidy(g['hi'], 'hi')] for g in gs], ensure_ascii=False)] += 1
    shared = {standard.fold(k) for k in json.load(open(os.path.join(ROOT, 'library', 'glossary', 'sa.json'), encoding='utf-8'))}
    ours = O['words']
    G = {}
    for w, C in senses.items():
        if standard.fold(w) in shared and w not in ours: stat['left to the shared dictionary'] += 1; continue
        by_en = collections.defaultdict(collections.Counter)
        for (h, e), n in C.items(): by_en[e.lower()][(h, e)] += n
        S = sorted(((sum(c.values()), c.most_common(1)[0][0]) for c in by_en.values()), key=lambda z: -z[0])
        top = S[0][0]
        S = [he for n, he in S if not (n == 1 and top >= 5)][:4]
        hs = list(dict.fromkeys(h for h, e in S)); es = [e for h, e in S]
        G[w] = {'hi': ' / '.join(hs), 'en': ' / '.join(es)}
        if parts[w] and len(S) == 1: G[w]['p'] = json.loads(parts[w].most_common(1)[0][0])
    for w, e in ours.items(): G[w] = e
    os.makedirs(os.path.join(HERE, '..', 'glossary'), exist_ok=True)
    jsonio.dump_glossary(os.path.join(HERE, '..', 'glossary', 'sa.json'), dict(sorted(G.items())))
    have = set(G) | shared
    miss = collections.Counter(k for x in T for l in x['v'] for k in (clean(t) for t in l.split()) if k and k not in G and standard.fold(k) not in shared and standard.fold(k) not in {standard.fold(g) for g in G})
    json.dump({'missing': sorted(miss), 'weak': weak}, open(os.path.join('/tmp', 'durga-words-report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(f"{len(G)} words; {dict(stat)}; {len(miss)} printed words still without a meaning (/tmp/durga-words-report.json)")

if __name__ == '__main__':
    main(sys.argv[1])
