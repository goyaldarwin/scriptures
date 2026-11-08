"""Checks text.txt against the witnesses of the Japji Sahib — run it after make.py.

1. Always: every line is Gurmukhi (no unknown character, no bare vowel bearer), the structure is the bani's
   (Mool Mantar, ॥ ਜਪੁ ॥, the opening salok, pauris 1–38, the closing salok; make.py → check).
2. Optional witnesses (scratch copies, never committed; see reconciliation.md):
     --shabados <database.sqlite>   the Shabad OS database (@shabados/database on npm): its Jap Ji Sahib bani,
                                    compared word by word with text.txt (vishraam marks ; . , removed), and the
                                    division into lines (where each ॥ falls)
     --gurmukhi-utils <package dir> an independent ASCII→Unicode converter (gurmukhi-utils on npm, run with node),
                                    compared with ours on every printed line of source/pdf.txt
     --md <file>                    the owner's line-by-line study sheet (a Markdown table, Gurmukhi | meaning):
                                    its Gurmukhi compared word by word
Usage: python3 tools/works/japji-sahib/source/check.py [--shabados DB] [--gurmukhi-utils DIR] [--md FILE]
"""
import difflib, json, os, re, subprocess, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(WORK)); import textfile
sys.path.append(os.path.join(WORK, '..', 'sukhmani-sahib', 'source')); from gurmukhi import to_unicode
from make import build, check, read_pdf, GDIG   # this folder's make.py (HERE is first on the path)


def words(s):
    s = unicodedata.normalize('NFC', s.translate(GDIG))
    s = re.sub(r'॥\s*([੦-੯]+)\s*॥', r' ॥\1॥ ', s)
    return re.sub(r'(?<![੦-੯])॥(?![੦-੯])', ' ॥ ', s).split()


def compare(name, A, B):
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    d = [(op, ' '.join(A[i1:i2]), ' '.join(B[j1:j2]), ' '.join(A[max(0, i1 - 4):i1]))
         for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
    print(f'{name}: {len(A)} words in text.txt, {len(B)} in the witness; {len(d)} differences')
    for x in d: print(f'    {x[0]:8} text {x[1]!r:24} witness {x[2]!r:24} after “{x[3]}”')
    return d


def main(argv):
    items = build(); check(items)
    T = textfile.read(os.path.join(WORK, 'text.txt'))
    assert [(x['id'], x['v']) for x in T] == [(x['id'], x['v']) for x in items], 'text.txt is stale: run make.py'
    print(f'1. structure: {len(T)} items, {sum(len(x["v"]) for x in T)} lines; conversion clean')
    A = [w for x in T for l in x['v'] for w in words(l)]

    if '--shabados' in argv:
        import sqlite3
        db = sqlite3.connect(argv[argv.index('--shabados') + 1])
        bid = db.execute("select id from banis where name_english='Jap Ji Sahib'").fetchone()[0]
        ref = [r[0] for r in db.execute('select l.gurmukhi from bani_lines bl join lines l on l.id=bl.line_id '
                                        'where bl.bani_id=? order by bl.line_group, l.order_id', (bid,))]
        ref = [to_unicode(re.sub(r'\s+', ' ', re.sub(r'[;.,]', '', r)).strip()) for r in ref]
        compare('2a. Shabad OS', A, [w for r in ref for w in words(r)])
        ends = lambda L: [i for i, w in enumerate(L) if '॥' in w]
        mine = ' '.join(l for x in T for l in x['v']).count('॥')
        print(f'    ॥ marks: {mine} in text.txt, {" ".join(ref).count("॥")} in Shabad OS')
    if '--gurmukhi-utils' in argv:
        pkg = os.path.abspath(argv[argv.index('--gurmukhi-utils') + 1])
        L = read_pdf()
        js = "const g=require(process.argv[1]);const L=JSON.parse(require('fs').readFileSync(0,'utf8'));" \
             "process.stdout.write(JSON.stringify(L.map(s=>g.toUnicode(s))))"
        theirs = json.loads(subprocess.run(['node', '-e', js, pkg], input=json.dumps(L),
                                           capture_output=True, text=True, check=True).stdout)
        n = 0
        for g, t in zip(L, theirs):
            a = words(to_unicode(g)); b = words(t)
            if a != b: n += 1; print(f'    ours {" ".join(a)}  | gurmukhi-utils {" ".join(b)}  | {g}')
        print(f'2b. gurmukhi-utils: {len(L) - n} of {len(L)} printed lines identical, {n} differ')
    if '--md' in argv:
        md = open(argv[argv.index('--md') + 1], encoding='utf-8').read()
        cells = re.findall(r'^\| ([^|]*[਀-੿][^|]*?) \|', md, re.M)
        compare('2c. the owner\'s study sheet', A, [w for c in cells for w in words(c)])


if __name__ == '__main__':
    main(sys.argv[1:])
