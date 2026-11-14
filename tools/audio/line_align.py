"""Every singing of every line, from MMS's emissions (tools/audio/METHOD.md, "Line by line: kirtan").

A sung shabad repeats its lines: the rahao (refrain) opens it and returns after every pada, and lines are sung twice. A
forced aligner, which takes the text once and in order, cannot place that. Here the verse's lines are the units of a small
grammar of how a shabad is sung, and a Viterbi search over MMS's frame-by-frame letter probabilities finds the best path
through it:

  - a pada (the lines up to a ॥n॥) is sung line by line; a line may be sung again, the pada may start again from any of
    its earlier lines, and a line may be left out at a cost (a heading — ਮਹਲਾ, ਸਲੋਕੁ, ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ … — at none);
  - the rahao (the lines up to ॥੧॥ ਰਹਾਉ ॥) may open the song and follows each pada, and is sung as often as liked;
  - after a pada and its rahao comes the next pada, or a later one at a cost; so do opening on a later pada and ending
    before the last (a stanza sung on its own);
  - between any two lines, and before and after, a filler takes what the text does not hold: the alaap, music, a
    manglacharan or dhaarna, lines of another shabad. A frame costs the filler its best letter's probability less a
    penalty (small where MMS hears no letter, larger where it hears one), so a line wins only where its own letters are
    heard about as well as anything else could be, and the frames between a line's letters cost a little more than the
    filler's quiet ones, so a line does not stretch over the music around it.

`inorder=True` is the plain forced alignment of METHOD.md step 2 instead: every line once, in the text's order (headings
optional), with a filler between lines; its starts are each line's first singing in the text's order.

Results are line occurrences [line index, start s, end s, score], score the mean probability of the line's letters over
their frames (as torchaudio's MMS_FA scores a word). `read()` gives the letters MMS hears (its most likely letter at each
frame, repeats and blanks dropped), to check that a recording sings the verse its title names.
"""
import re, unicodedata
import numpy as np

END = re.compile(r'॥\s*[੦-੯0-9]+\s*॥')
HEAD = ('ਮਹਲਾ', 'ਮਃ', 'ੴ', 'ਸਲੋਕੁ', 'ਸਲੋਕ', 'ਪਉੜੀ', 'ਪਵੜੀ', 'ਛੰਤੁ', 'ਛੰਤ', 'ਘਰੁ', 'ਬਾਣੀ', 'ਅਸਟਪਦੀ', 'ਡਖਣਾ', 'ਦੁਪਦੇ', 'ਤਿਪਦੇ', 'ਚਉਪਦੇ', 'ਪੰਚਪਦੇ', 'ਵਾਰ')
NEG = -1e30
# the search's costs, in log-probability: tuned on the pilot's recordings (aligned.md of the source that uses them)
P = {'filler': 2.0,     # per frame of filler where MMS hears a letter, below that letter (sung words the text does not hold)
     'quiet': 0.1,      # per frame of filler where MMS hears no letter (alaap, music, a pause)
     'blank': 0.11,     # per frame between a line's letters, below the blank: more than 'quiet', so a line does not
                        # stretch over the music around it
     'sub': 1.5,        # the most a frame costs a line, below the frame's best letter (a letter sung otherwise than written)
     'enter': 1.0,      # per line sung (a line must earn its place)
     'skip': 6.0,       # per line of a pada left out
     'pada': 8.0}       # per pada passed over, opened after or ended before (a stanza sung on its own)       # per pada passed over, opened after or ended before (a stanza sung on its own)       # per pada passed over (a stanza sung on its own)

def rom(s):
    """A line's transliteration in plain letters a–z as MMS spells what it hears (a long ā, ī, ū doubled: aa, ii, uu), its
    numbers and the word rahāu dropped (they are not sung)."""
    t = unicodedata.normalize('NFD', s.lower())
    for a, b in (('a\u0304', 'aa'), ('i\u0304', 'ii'), ('u\u0304', 'uu')): t = t.replace(a, b)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    w = re.sub(r'[^a-z\s]', ' ', t).split()
    while w and w[-1] in ('rahau', 'duja', 'duji'): w.pop()
    return ''.join(w)

def is_head(line):
    return not END.search(line) and (any(k in line for k in HEAD) and len(line.split()) <= 11 or len([w for w in line.split() if w != '॥']) <= 2)

def units(item):
    """The verse's lines as sung units: [{"k", "rom", "head", "rahao", "group"}] and the groups: padas and rahao blocks,
    in the text's order ({"kind": "pada"|"rahao", "lines": [k, …]})."""
    v, t = item['v'], item.get('t') or item['v']
    U, groups, cur = [], [], []
    for k, (g, tr) in enumerate(zip(v, t)):
        u = {'k': k, 'rom': rom(tr), 'head': is_head(g), 'rahao': False}
        U.append(u); cur.append(k)
        if END.search(g):
            kind = 'rahao' if 'ਰਹਾਉ' in g else 'pada'
            groups.append({'kind': kind, 'lines': cur}); cur = []
    if cur: groups.append({'kind': 'pada', 'lines': cur})
    for gi, g in enumerate(groups):
        for k in g['lines']: U[k]['group'] = gi; U[k]['rahao'] = g['kind'] == 'rahao'
    return U, groups

class Graph:
    """Line instances (a line in its pada, or in one of the rahao's copies), each a CTC chain of states, and the moves
    between their ends and starts."""
    def __init__(self, item, D, inorder=False, p=P):
        U, groups = units(item)
        self.U = U
        inst = []                      # (line k, copy tag)
        def add(k, tag): inst.append((k, tag)); return len(inst) - 1
        padas = [g for g in groups if g['kind'] == 'pada']
        rah = [g for g in groups if g['kind'] == 'rahao']
        sung = lambda ks: [k for k in ks if U[k]['rom']]
        M = {}
        if inorder:
            order = [k for g in groups for k in sung(g['lines'])]
            for k in order: M[('t', k)] = add(k, 't')
        else:
            for pi, g in enumerate(padas):
                for k in sung(g['lines']): M[('p', pi, k)] = add(k, ('p', pi))
            # the rahao that follows pada pi: the last rahao block before the next pada in the text (else the first)
            pos = {id(g): n for n, g in enumerate(groups)}
            def rahao_after(pi):
                nxt = pos[id(padas[pi + 1])] if pi + 1 < len(padas) else len(groups)
                before = [g for g in rah if pos[id(g)] < nxt]
                return before[-1] if before else (rah[0] if rah else None)
            self.rcopies = []
            if rah:
                for pi in range(-1, len(padas)):         # -1: the opening (sthai), before the first pada
                    rb = rah[0] if pi < 0 else rahao_after(pi)
                    rks = [k for k in sung(rb['lines']) if not U[k]['head']]   # a heading before the rahao is not sung with it
                    for k in rks: M[('r', pi, k)] = add(k, ('r', pi))
                    self.rcopies.append((pi, rks))
        n = len(inst); self.inst = inst
        pen = np.full((n, n), NEG); start = np.full(n, NEG); final = np.zeros(n)
        def edge(a, b, c=0.0):
            if a in M and b in M: pen[M[a], M[b]] = max(pen[M[a], M[b]], -(p['enter'] + c))
        if inorder:
            order = [k for g in groups for k in sung(g['lines'])]
            for i, k in enumerate(order):
                skipped = 0.0
                for j in range(i + 1, len(order)):
                    edge(('t', k), ('t', order[j]), skipped)
                    if not U[order[j]]['head']: break
                    skipped += 0.0
                if all(U[x]['head'] for x in order[:i]): start[M[('t', k)]] = -p['enter']
            final[:] = NEG
            last = max(i for i, k in enumerate(order) if not U[k]['head'])
            for k in order[last:]: final[M[('t', k)]] = 0.0
        else:
            def firsts(ks):     # where a group may be entered: its first line, or a later one when the lines before are headings
                out = []
                for k in ks:
                    out.append(k)
                    if not U[k]['head']: break
                return out
            for pi, g in enumerate(padas):
                ks = sung(g['lines'])
                for i, k in enumerate(ks):
                    for j in range(i + 1):                                  # again: this line or an earlier one of the pada (not a heading)
                        if not U[ks[j]]['head']: edge(('p', pi, k), ('p', pi, ks[j]))
                    cost = 0.0                                              # on: the next line, or a later one at a cost
                    for j in range(i + 1, len(ks)):
                        edge(('p', pi, k), ('p', pi, ks[j]), cost)
                        cost += 0.0 if U[ks[j]]['head'] else p['skip']
                    tail = sum(0.0 if U[x]['head'] else p['skip'] for x in ks[i + 1:])   # lines of the pada left unsung
                    for (ri, rks) in self.rcopies:
                        if ri == pi and rks: edge(('p', pi, k), ('r', pi, rks[0]), tail)
                    for qi in range(pi + 1, len(padas)):                   # the next pada, or a later one at a cost
                        for f in firsts(sung(padas[qi]['lines'])): edge(('p', pi, k), ('p', qi, f), tail + p['pada'] * (qi - pi - 1))
                for f in firsts(ks): start[M[('p', pi, f)]] = -(p['enter'] + p['pada'] * pi)   # a song that opens on a later pada: those before cost
                for k in ks: final[M[('p', pi, k)]] = -p['pada'] * (len(padas) - 1 - pi)              # and so do those it ends before
            for (ri, rks) in self.rcopies:
                for i, k in enumerate(rks):
                    for j in range(i + 1): edge(('r', ri, k), ('r', ri, rks[j]))
                    if i + 1 < len(rks): edge(('r', ri, k), ('r', ri, rks[i + 1]))
                    for qi in range(ri + 1, len(padas)):
                        for f in firsts(sung(padas[qi]['lines'])): edge(('r', ri, k), ('p', qi, f), p['pada'] * (qi - ri - 1))
                    if ri >= 0:                                            # back to the pada just sung (a ragi often sings it again)
                        for f in firsts(sung(padas[ri]['lines'])): edge(('r', ri, k), ('p', ri, f))
                if rks: start[M[('r', ri, rks[0])]] = -(p['enter'] + p['pada'] * max(0, ri))
                for k in rks: final[M[('r', ri, k)]] = -p['pada'] * (len(padas) - 1 - max(ri, 0))
        self.pen, self.start, self.final = pen, start, final
        # the states: per instance [blank, c1, blank, c2, …, cn, blank]
        tok, off, skip, own = [], [], [], []
        for x, (k, _) in enumerate(inst):
            off.append(len(tok)); cs = [D[c] for c in U[k]['rom']]
            for j, c in enumerate(cs):
                tok += [0, c]; skip += [False, j > 0 and cs[j - 1] != c]; own += [x, x]
            tok.append(0); skip.append(False); own.append(x)
        off.append(len(tok))
        self.tok, self.off, self.skip, self.own = np.array(tok), np.array(off), np.array(skip), np.array(own)
        self.first = self.off[:-1]                     # the leading blank
        self.last = self.off[1:] - 1                   # the trailing blank (the last letter is last - 1)

def viterbi(em, G, p=P):
    """The best path through G over the emissions em [frames, letters] (log-probabilities, blank = 0).
    Returns [(instance, first frame, last frame, [(state, first frame, last frame), …])] in time order."""
    T, N, n = em.shape[0], len(G.tok), len(G.inst)
    top = em.max(1); fill = top - np.where(em.argmax(1) == 0, p['quiet'], p['filler']); floor = top - p['sub']
    blank = G.tok == 0
    isfirst = np.zeros(N, bool); isfirst[G.first] = True
    isc1 = np.zeros(N, bool); isc1[G.first + 1] = True
    m1 = np.ones(N, bool); m1[G.first] = False
    m2 = G.skip.copy()
    V = np.full(N, NEG); F = np.full(n, NEG); F0 = 0.0
    bp = np.zeros((T, N), np.uint8)                    # 0 stay, 1 from the state before, 2 from two before, 3 entered
    ent = np.zeros((T, n), np.int32)                   # where an entry came from: x*3 + (0 last letter, 1 last blank, 2 filler); -1 the opening filler
    fbp = np.zeros((T, n), np.uint8)                   # filler: 0 stay, 1 from the last letter, 2 from the last blank
    for t in range(T):
        e = np.maximum(em[t, G.tok] - np.where(blank, p['blank'], 0.0), floor[t])
        a0 = V
        a1 = np.where(m1, np.concatenate(([NEG], V[:-1])), NEG)
        a2 = np.where(m2, np.concatenate(([NEG, NEG], V[:-2])), NEG)
        best = np.maximum(a0, np.maximum(a1, a2)); code = np.where(best == a0, 0, np.where(best == a1, 1, 2)).astype(np.uint8)
        # the ends of the instances at the frame before: the last letter, the last blank, the filler after it
        el, eb = V[G.last - 1], V[G.last]
        X = np.stack([el, eb, F]); xk = X.argmax(0); xv = X.max(0)
        cand = xv[:, None] + G.pen                       # [from, to]
        src = cand.argmax(0); val = cand.max(0)
        enc = src * 3 + xk[src]
        s0 = F0 + G.start
        use0 = s0 > val; val = np.where(use0, s0, val); enc = np.where(use0, -1, enc)
        for tgt in (G.first, G.first + 1):
            better = val > best[tgt]
            best[tgt] = np.where(better, val, best[tgt]); code[tgt] = np.where(better, 3, code[tgt])
        ent[t] = enc
        Vn = best + e
        fk = np.stack([F, el, eb]); fb = fk.argmax(0)
        F = fk.max(0) + fill[t]; fbp[t] = fb
        F0 = F0 + fill[t]
        V = Vn; bp[t] = code
    # the end: any state, the filler after any instance (and the final rule of an in-order alignment)
    endv = np.concatenate([V + G.final[G.own], F + G.final])   # ending before the last pada costs (G.final)
    k = int(endv.argmax())
    if endv[k] <= NEG / 2: return []
    occ, cur = [], None
    def close():
        if cur: occ.append(cur)
    s, inF = (k, False) if k < N else (k - N, True)
    t = T - 1
    while t >= 0:
        if inF:
            b = fbp[t, s]
            if b == 0: t -= 1; continue
            s = G.last[s] - 1 if b == 1 else G.last[s]; inF = False; t -= 1; continue
        x = G.own[s]
        if cur is None or cur[0] != x or cur[1] != t + 1:
            close(); cur = [x, t, t, []]
        cur[1] = t
        if G.tok[s] != 0:
            if cur[3] and cur[3][-1][0] == s and cur[3][-1][1] == t + 1: cur[3][-1][1] = t
            else: cur[3].append([s, t, t])
        c = bp[t, s]
        if c == 0: t -= 1
        elif c == 1: s -= 1; t -= 1
        elif c == 2: s -= 2; t -= 1
        else:
            e = ent[t, x]
            close(); cur = None
            if e < 0:
                t -= 1
                while t >= 0: t -= 1          # the opening filler to the start
                break
            fx, kind = divmod(int(e), 3)
            t -= 1
            if kind == 0: s = G.last[fx] - 1
            elif kind == 1: s = G.last[fx]
            else: s, inF = fx, True
    close()
    occ.reverse()
    return [(x, a, b, sorted(toks, key=lambda q: q[1])) for x, a, b, toks in occ]

def lines(em, sec, item, D, inorder=False, p=P):
    """[[line index, start s, end s, score]] for every singing found (in time order). A line's start and end are its first
    and last letter's."""
    G = Graph(item, D, inorder, p)
    if not len(G.inst): return []
    out = []
    for x, a, b, toks in viterbi(em, G, p):
        if not toks: continue
        sc = float(np.mean([np.exp(em[t0:t1 + 1, G.tok[s]]).mean() for s, t0, t1 in toks]))
        out.append([G.inst[x][0], round(toks[0][1] * sec, 2), round((toks[-1][2] + 1) * sec, 2), round(sc, 3)])
    return out

def read(em, labels):
    """The letters MMS hears: its most likely letter at each frame, repeats joined, blanks dropped."""
    a = em.argmax(1); keep = np.concatenate(([True], a[1:] != a[:-1])) & (a != 0)
    return ''.join(labels[i] for i in a[keep] if labels[i] not in ('-', '*', "'"))

def read_at(em, labels, sec, every=10.0):
    """read() in stretches: [[start s, letters], …], one per `every` seconds."""
    a = em.argmax(1); keep = np.concatenate(([True], a[1:] != a[:-1])) & (a != 0); out = []
    for t in np.nonzero(keep)[0]:
        c = labels[a[t]]
        if c in ('-', '*', "'"): continue
        if not out or t * sec >= out[-1][0] + every: out.append([round(float(t * sec), 1), ''])
        out[-1][1] += c
    return out

def merge(every, inorder, lens, thr=0.35):
    """The singings to keep: [line, start, end, score, how]. The search for every singing where it scores thr or more
    ("every"), and for a line it left out, the in-order alignment's singing ("inorder") where the kept singings of the
    lines before and after it in the text (the nearest each side) start before and after it: the in-order alignment is
    right where the song goes through the verse in order, and this keeps it only there. A singing's end is cut to the next
    singing's start and to 2.5 times the line's length at the song's pace (a line's last letter can be matched far off,
    over music). lens: letters per line. Returns (kept, those from in-order)."""
    def trim(occ):
        occ = sorted(occ, key=lambda o: o[1])
        pace = sorted((o[2] - o[1]) / max(1, lens[o[0]]) for o in occ) or [0.25]
        m = pace[len(pace) // 2]
        for n, o in enumerate(occ):
            o[2] = round(min(o[2], o[1] + 2.5 * m * max(1, lens[o[0]]), occ[n + 1][1] if n + 1 < len(occ) else o[2]), 2)
        return occ
    good = trim([o[:4] + ['every'] for o in every if o[3] >= thr])
    inorder = trim([list(o) for o in inorder])
    first = {}
    for o in good: first.setdefault(o[0], o[1])
    fill = []
    for o in inorder:
        k = o[0]
        if k in first: continue
        before = [first[j] for j in first if j < k]; after = [first[j] for j in first if j > k]
        if before and after and max(before) < o[1] < min(after) and not any(g[1] < o[2] and o[1] < g[2] for g in good):
            fill.append(o[:4] + ['inorder'])
    return sorted(good + fill, key=lambda o: o[1]), fill

class Titles:
    """Which verse of a work a recording sounds most like: the letters MMS hears against each verse's text, as letter
    trigrams weighted by how rare they are in the work (cosine)."""
    def __init__(self, texts):
        import collections, math
        self.math = math
        g = {k: collections.Counter(v[i:i + 3] for i in range(len(v) - 2)) for k, v in texts.items()}
        df = collections.Counter(x for c in g.values() for x in c); self.N = len(g)
        self.idf = {x: math.log(self.N / n) for x, n in df.items()}
        self.V = {k: self.vec(c) for k, c in g.items()}
    def vec(self, c):
        v = {x: n * self.idf.get(x, self.math.log(self.N)) for x, n in c.items()}
        z = self.math.sqrt(sum(y * y for y in v.values())) or 1
        return {x: y / z for x, y in v.items()}
    def like(self, heard, iid):
        import collections
        h = self.vec(collections.Counter(heard[i:i + 3] for i in range(len(heard) - 2)))
        cos = lambda v: sum(y * v.get(x, 0) for x, y in h.items())
        return cos(self.V[iid]), max((cos(v), k) for k, v in self.V.items())
