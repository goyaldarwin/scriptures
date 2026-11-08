"""The books' footnotes, found so the merge leaves them out of the paragraphs.

    python3 notes.py <book>   → <book>.notes.json: {page: {"side": [first note line, …], "text": the notes as the
                                 whole-page pass read them (one pass, not read by eye: not published)}}

A page's notes stand at its foot under their mark (* † ‡): the whole-page pass reads them whole, line by line, from
the first line that opens with a mark to the end. A column's last lines are notes when most of their words are words
of those notes (in Gita Press code 2223 a note runs under both columns, so the Hindi column holds the end of each of
its lines); the walk up from the column's foot stops at the first line that is not.
"""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = re.compile(r'^\s*[*†‡]')
WORD = re.compile(r'[ऀ-ॣ०-ॿ‌‍]{2,}')

def page_notes(P):
    full = [l for l in P['full'].splitlines() if l.strip()]
    start = next((i for i in range(max(0, len(full) - 8), len(full)) if MARK.match(full[i])), None)   # notes are short
    if start is None: return None
    note = full[start:]; words = set(w for l in note for w in WORD.findall(l))
    out = {}
    for c in P['cols']:
        lines = c['deva'].splitlines(); cut = None
        for i in range(len(lines) - 1, -1, -1):
            ws = WORD.findall(lines[i])
            if not lines[i].strip(): continue
            if ws and sum(w in words for w in ws) >= max(1, .6 * len(ws)): cut = i
            else: break
        if cut is not None and len(lines) - cut <= 6: out[c['side']] = cut
    return {'cols': out, 'text': '\n'.join(note)} if out else None

def main(book):
    R = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'ocr', book, 'p*.json'))):
        P = json.load(open(f, encoding='utf-8')); n = page_notes(P)
        if n: R[str(P['page'])] = n
    json.dump(R, open(os.path.join(HERE, f'{book}.notes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print(f'{book}: notes on {len(R)} pages, {sum(len(v["cols"]) for v in R.values())} columns cut')

if __name__ == '__main__':
    main(sys.argv[1])
