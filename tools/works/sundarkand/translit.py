"""Devanagari → the Roman transliteration used by the Mānas items (IAST with ṁ for anusvara, ̐ for candrabindu, r̥).

Every inherent a is written (the Mānas does not drop it: bacana, hanumaṁta). In a verse line, a mid-line । becomes
",", a final ।। becomes "." (or "," for the first line of a dohā), and a number ।।N।। becomes " ॥N॥".
Checked against the Mānas's own transliterations: `python3 tools/works/sundarkand/translit.py --check`.
"""
import re, sys
V = {'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 'ऋ': 'r̥', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au'}
M = {'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū', 'ृ': 'r̥', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au'}
C = {'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ', 'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
     'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ', 'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
     'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
     'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h', 'ड़': 'ṛ', 'ढ़': 'ṛh'}
NASAL_LONG = set('ीईेोौऔ')   # anusvara after these at the end of a word is written ̐ (also inside a word after े ौ)
def word(w):
    w = w.replace('\u095c', 'ड़').replace('\u095d', 'ढ़')
    out, i = [], 0
    while i < len(w):
        ch = w[i]
        if ch in 'डढ' and w[i + 1:i + 2] == '़': ch = ch + '़'; w = w[:i] + ch + w[i + 2:]
        if ch in C:
            out.append(C[ch]); i += len(ch); nx = w[i] if i < len(w) else ''
            if nx == '्': i += 1; continue
            if nx in M: out.append(M[nx]); i += 1; continue
            out.append('a'); continue
        if ch in V: out.append(V[ch])
        elif ch == 'ं':
            prev = w[i - 1] if i else ''
            out.append('̐' if prev in NASAL_LONG and (not re.match(r'[\u0900-\u0963]', w[i + 1:i + 2]) or prev in 'ेौ') else 'ṁ')
        elif ch == 'ँ': out.append('̐')
        elif ch == 'ः': out.append('ḥ')
        elif ch == 'ऽ': out.append('’')
        else: out.append(ch)
        i += 1
    return ''.join(out)
DIG = str.maketrans('०१२३४५६७८९', '0123456789')
def line(l, n=None):
    """One verse line; n = the verse number to print at its end when the Devanagari line ends in a bare ।।"""
    l = l.strip()
    m = re.search(r'\s*।।([०-९]+)।।$', l); num = m.group(1).translate(DIG) if m else None
    if not m and n and l.endswith('।।'): l, num = l[:-2].rstrip() + ' ।।' + n + '।।', n; m = re.search(r'\s*।।(\d+)।।$', l)
    if m: l = l[:m.start()]
    end = ''
    if not m:
        if l.endswith('।।'): l, end = l[:-2].rstrip(), '.'
        elif l.endswith('।'): l, end = l[:-1].rstrip(), ','
    l = re.sub(r'\s*।\s*', ', ', l)
    t = ' '.join(word(w) for w in l.split())
    return t + (' ॥' + num + '॥' if num else end)
def verse(lines, n=None):
    """A verse's lines; a caupāī's number (n) goes after its last line, as in the Mānas."""
    return [line(l, n if k == len(lines) - 1 else None) for k, l in enumerate(lines)]
if __name__ == '__main__' and '--check' in sys.argv:
    import json, os, collections
    R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
    w = json.load(open(os.path.join(R, 'library/hindu/granth/tulsidas/ramcharitmanas/work.json')))
    ok = n = 0; bad = collections.Counter(); ex = []
    for x in w['items']:
        if x.get('l') == 'sa' or 't' not in x: continue
        for a, b in zip(verse(x['v'], x['n'] if x['y'] == 'cau' else None), x['t']):
            n += 1
            if a == b: ok += 1
            else:
                aw, bw = a.split(), b.split()
                if len(aw) == len(bw):
                    for p, q in zip(aw, bw):
                        if p != q: bad[(p, q)] += 1
                if len(ex) < 8: ex.append((a, b))
    print(f'{ok}/{n} lines identical'); print(bad.most_common(25)); [print(' mine', a, '\n book', b) for a, b in ex]
