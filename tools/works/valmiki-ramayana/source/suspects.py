"""Gita Press readings to check against the page: where both witnesses agree against Gita Press and either
(a) the metre: the GP half-verse has a syllable count the metre forbids and the witness reading fixes it, or
(b) the word: the GP word (normalised) occurs nowhere else in GP nor in IITK, while the witness form does.
"""
import json, sys, re, collections
sys.path.insert(0, sys.argv[1]); import align, metre
B = {k['kanda']: k for k in json.load(open(sys.argv[2]))}
both = json.load(open(sys.argv[3]))
I = json.load(open(sys.argv[4]))

def words_norm(text):
    """normalised words of a text, each normalised with the next word's first letter as context"""
    ws = [w for w in re.split(r'\s+', text.replace('।', ' ').replace('॥', ' ').replace('|', ' ')) if w and not re.fullmatch(r'[\d०-९.\-]+', w)]
    out = []
    for k, w in enumerate(ws):
        nxt = ws[k + 1][:1] if k + 1 < len(ws) else ''
        n = align.norm_line(w + nxt)
        if nxt:
            n2 = align.norm_line(nxt)
            n = n[:len(n) - len(n2)] if n2 and n.endswith(n2) else n
        out.append((w, n))
    return out

gp_count = collections.Counter(); ik_count = collections.Counter()
for k in B.values():
    for s in k['sargas']:
        for v in s['verses']:
            for w, n in words_norm(' '.join(v['lines'])): gp_count[n] += 1
for k in I['kandas']:
    for s in k['sargas']:
        for v in s['verses']:
            for w, n in words_norm(' '.join(v['text']['dv'])): ik_count[n] += 1

res = []
for d in both:
    s = B[d['kanda']]['sargas'][d['sarga'] - 1]
    # rebuild the sarga's normalised string word by word to find the GP word(s) at the difference
    pos = 0; hit = []; halfpos = 0; half = None
    for v in s['verses']:
        for h in align.halves(' '.join(v['lines'])):
            hn = align.norm_line(h)
            if half is None and halfpos <= d['i'] <= halfpos + len(hn) and (d['i'] < halfpos + len(hn) or not d['gp']):
                half = (v['n'], h, hn, d['i'] - halfpos)
            halfpos += len(hn)
            for w, n in words_norm(h):
                if pos <= d['i'] + len(d['gp']) and d['i'] <= pos + len(n):
                    hit.append((w, n, pos))
                pos += len(n)
    if not half:
        continue
    n_, h, hn, off = half
    h2 = hn[:off] + d['wit'] + hn[off + len(d['gp']):]
    a, b = metre.syllables(hn), metre.syllables(h2)
    metre_flag = (a not in (16, 22, 24, 23, 25) and b in (16, 22, 24)) or (a in (15, 17) and b == 16)
    word_flag = False; wit_word = None
    if len(hit) == 1:
        w, n, p0 = hit[0]
        o = d['i'] - p0
        wn = n[:o] + d['wit'] + n[o + len(d['gp']):]
        wit_word = wn
        word_flag = gp_count[n] == 1 and ik_count[n] == 0 and (ik_count[wn] + gp_count[wn]) >= 1
    if metre_flag or word_flag:
        res.append({'kanda': d['kanda'], 'sarga': d['sarga'], 'n': n_, 'gp': d['gp'], 'wit': d['wit'],
                    'half': h, 'syl': [a, b], 'metre': metre_flag, 'word': word_flag,
                    'gp_word': hit[0][0] if len(hit) == 1 else None, 'wit_word_norm': wit_word})
json.dump(res, open(sys.argv[5], 'w'), ensure_ascii=False, indent=0)
print(len(res), 'to check: metre', sum(r['metre'] for r in res), 'word', sum(r['word'] for r in res))
