"""The Faridkot Teeka, as the Shabad OS database gives it (translation source 5, "Fareedkot Teeka", one entry per line of
the Granth) → commentary/pa/faridkot.json of this work, and of the Japji Sahib and the Sukhmani Sahib, whose verses this
work takes (a taken verse's commentary comes from its own work).

    python3 tools/works/guru-granth-sahib/source/faridkot.py [--db <database.sqlite>]

Copied as given, line by line: a verse's commentary is one piece per verse line (a heading line, or a line the Teeka
leaves without a word, has an empty piece); a line's piece keeps the Teeka's own paragraphs (☬ in the database, a line
break here). Its footnotes (the database's "reference", marked _¹_ … for the ⁽¹⁾ in the text) are the verse's notes.
The only changes are the typing breaks the database carries from its legacy font (reconciliation.md §5): a private-use
code for a hora (U+F02B → ੋ), for a bindi (U+F02E → ਂ), a stray one (U+F02C) and a zero-width non-joiner dropped, the
addak typed as ~ before its letter (~ → ੱ) and one word left in the legacy encoding (qMU → ਤੂੰ).
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE); WORKS = os.path.dirname(WORK)
sys.path.insert(0, HERE); import shabados, make
sys.path.insert(0, WORKS); import textfile
sys.path.insert(0, os.path.join(WORKS, '..')); import jsonio

FIX = [('', 'ੋ'), ('', 'ਂ'), ('', ''), ('‌', ''), ('~', 'ੱ'), ('qMU', 'ਤੂੰ')]
TITLE = {'hi': 'फरीदकोट वाला टीका (पंजाबी)', 'en': 'Faridkot Teeka (Punjabi)', 'pa': 'ਫਰੀਦਕੋਟ ਵਾਲਾ ਟੀਕਾ'}
ABOUT = ('The Faridkot Teeka (made at the Faridkot court by Nirmala scholars, 1883–1905; public domain), as typed line by '
         'line in the Shabad OS database (@shabados/database 4.8.7, translation source "Fareedkot Teeka", CC BY-SA 4.0); '
         'made by tools/works/guru-granth-sahib/source/faridkot.py; copied as given.')


def clean(s):
    for a, b in FIX: s = s.replace(a, b)
    s = re.sub(r'[ \t]*☬[ \t]*', '\n', s)
    return re.sub(r'[ \t]+', ' ', s).strip()


def notes_of(ref):
    """The database's reference: _¹_ note … _²_ note → ['¹ note', '² note']."""
    ref = clean(ref or '')
    if not ref: return []
    parts = re.split(r'_([¹²³⁴⁵⁶⁷⁸⁹⁰]+)_', ref)
    out = [parts[0].strip()] if parts[0].strip() else []
    out += [f'{parts[k]} {parts[k + 1].strip()}' for k in range(1, len(parts) - 1, 2)]
    return [x for x in out if x]


def source(entries):
    """entries: [(verse id, [(line text, (translation, additional_information) or None)])] → the commentary file."""
    m, notes = {}, {}
    for vid, lines in entries:
        pieces = [clean(t[0]) if t else '' for _, t in lines]
        if not any(pieces): continue
        m[vid] = pieces if len(pieces) > 1 else pieces[0]
        ns = [n for _, t in lines if t for n in notes_of(json.loads(t[1] or '{}').get('reference'))]
        if ns: notes[vid] = ns
    return {'about': ABOUT, 'title': TITLE, 'order': 1, 'copied': True, 'm': m, 'notes': notes}


def write(work, obj):
    d = os.path.join(WORKS, work, 'commentary', 'pa'); os.makedirs(d, exist_ok=True)
    jsonio.dump_meanings(os.path.join(d, 'faridkot.json'), obj)
    print(f'{work}: {len(obj["m"])} verses, {len(obj["notes"])} with footnotes')


def main(argv):
    db = shabados.db_path(argv)
    U = shabados.units(shabados.EXTRACT); F = shabados.translations(db, 5)
    V = make.verses(U)
    T = textfile.read(os.path.join(WORK, 'text.txt'))
    own = [x for x in V if 'take' not in x]
    assert [x['v'] for x in T] == [[l['v'] for l in x['lines']] for x in own], 'text.txt is stale: run make.py'
    write('guru-granth-sahib', source([(t['id'], [(l['v'], F.get(l['id'])) for l in x['lines']]) for t, x in zip(T, own)]))
    JAP, SUKH = make.takes(U)
    for work, ks in (('japji-sahib', JAP), ('sukhmani-sahib', SUKH)):
        db_lines = [l for k in sorted(ks) for l in U[k]['lines']]
        items = textfile.read(os.path.join(WORKS, work, 'text.txt')); entries, n = [], 0
        for it in items:
            got = []
            for v in it['v']:
                if work == 'japji-sahib' and it['id'] == 'mool':   # the Japji prints the Mool Mantar on four lines, the database on one
                    got.append((v, F.get(db_lines[0]['id']) if v == it['v'][-1] else None)); continue
                assert db_lines[n]['v'] == v, (work, it['id'], v, db_lines[n]['v']); got.append((v, F.get(db_lines[n]['id']))); n += 1
            if it['id'] == 'mool': n = 1
            entries.append((it['id'], got))
        assert n == len(db_lines), (work, n, len(db_lines))
        write(work, source(entries))


if __name__ == '__main__':
    main(sys.argv[1:])
