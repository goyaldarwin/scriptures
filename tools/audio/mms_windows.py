"""Windows for Meta's MMS forced aligner (tools/audio/METHOD.md, step 2), from a recording's rough starts (step 1).

    python3 tools/audio/mms_windows.py tools/works/<work>/audio/<source>     → <source>/mms/windows.json

Each recording's verses (its tracks' first … last in library/<work>/audio/<source>.json) are cut into windows of about
WIN seconds of the rough starts (Whisper's, matched to the text). A window also holds the verse before and the verse after,
so windows overlap by a verse; "keep" names the verses it answers for. Its audio runs from PAD seconds before the
verse before's rough start to PAD seconds after the verse after's. A verse with no rough start is placed between its
neighbours by its length, only to cut the windows: the aligner times it. The text given to the aligner is each verse's
transliteration in plain letters (a–z), its numbers dropped.
Window: {"yt", "a", "b" (seconds), "keep": [ids], "lines": [{"id", "rom", "rough"}]}.
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
WIN, PAD = 90.0, 6.0

def rom(lines):
    t = unicodedata.normalize('NFD', ' '.join(lines).lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'[^a-z\s]', ' ', t)
    return ' '.join(t.split())

def main(src):
    meta = json.load(open(os.path.join(src, 'source.json')))
    lib = os.path.join(REPO, 'library', meta['work'])
    sys.path.insert(0, os.path.dirname(HERE)); import jsonio
    work = jsonio.read_work(os.path.join(lib, 'work.json'))   # its verses joined when loaded by part
    au = json.load(open(os.path.join(lib, 'audio', meta['id'] + '.json'), encoding='utf-8'))
    IT = work['items']; ID = {x['id']: k for k, x in enumerate(IT)}
    L = lambda i: max(8, len(''.join(IT[i]['v'])))
    out = []
    for ti, tr in enumerate(au['tracks']):
        idx = list(range(ID[tr['first']], ID[tr['last']] + 1))
        rough = {i: au['at'][IT[i]['id']][1] for i in idx if IT[i]['id'] in au['at'] and au['at'][IT[i]['id']][0] == ti}
        # a verse without a rough start: between its neighbours by length (or at the pace of the recording at its ends)
        known = sorted(rough)
        pace = (rough[known[-1]] - rough[known[0]]) / max(1, sum(L(i) for i in range(known[0], known[-1])))
        T = {}
        for i in idx:
            if i in rough: T[i] = rough[i]; continue
            lo = max((k for k in known if k < i), default=None); hi = min((k for k in known if k > i), default=None)
            if lo is not None and hi is not None:
                T[i] = rough[lo] + (rough[hi] - rough[lo]) * sum(L(k) for k in range(lo, i)) / max(1, sum(L(k) for k in range(lo, hi)))
            elif lo is not None: T[i] = rough[lo] + pace * sum(L(k) for k in range(lo, i))
            else: T[i] = max(0.0, rough[hi] - pace * sum(L(k) for k in range(i, hi)))
        k = 0
        while k < len(idx):
            j = k
            while j + 1 < len(idx) and T[idx[j + 1]] - T[idx[k]] < WIN: j += 1
            lo, hi = max(0, k - 1), min(len(idx) - 1, j + 1)
            a = max(0.0, T[idx[lo]] - PAD)
            b = min(tr['dur'], (T[idx[hi + 1]] if hi + 1 < len(idx) else tr['dur'] - PAD) + PAD)
            out.append({'yt': tr['yt'], 'a': round(a, 2), 'b': round(b, 2), 'keep': [IT[i]['id'] for i in idx[k:j + 1]],
                        'lines': [{'id': IT[i]['id'], 'rom': rom(IT[i].get('t') or []), 'rough': round(T[i], 2) if i in rough else None} for i in idx[lo:hi + 1]]})
            k = j + 1
    os.makedirs(os.path.join(src, 'mms'), exist_ok=True)
    with open(os.path.join(src, 'mms', 'windows.json'), 'w', encoding='utf-8') as f:
        f.write('[\n' + ',\n'.join(json.dumps(w, ensure_ascii=False, separators=(',', ':')) for w in out) + '\n]\n')
    bad = [l['id'] for w in out for l in w['lines'] if not l['rom']]
    print(len(out), 'windows,', sum(len(w['keep']) for w in out), 'verses', '(no letters:', bad[:5], ')' if bad else '')

if __name__ == '__main__': main(os.path.abspath(sys.argv[1]))
