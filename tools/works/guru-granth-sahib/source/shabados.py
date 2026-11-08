"""Read Sri Guru Granth Sahib from the Shabad OS database (@shabados/database on npm, its build/database.sqlite).

    import shabados; units = shabados.units(DB)

The database keeps the Gurbani in the common legacy ASCII Gurmukhi encoding (GurbaniAkhar), with vishraam (pause)
marks ; . , that the Granth does not print, a spacer Ø under a nasal before a bihari (ˆØI = ਂ + ੀ) and, in some
headings, the small numerals the Granth prints under a word (ਪੰਚਪਦੇ₂, the count of the shabads that follow). Each
line becomes Unicode with the Sukhmani Sahib's converter (tools/works/sukhmani-sahib/source/gurmukhi.py) and the
writing standard (tools/text/standard.py); the vishraams, the spacer and the small numerals are left out
(reconciliation.md §2).

A unit is one of the database's shabads (source 1, the Granth), in the Granth's order:
    {'sid', 'section' (1–51), 'writer', 'lines': [{'id', 'ang', 'line', 'type', 'v'}]}
type: 1 Manglacharan (ੴ …), 2 Sirlekh (a heading), 3 Rahao, 4 Pankti (a line of the shabad).
"""
import os, re, sqlite3, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); WORKS = os.path.dirname(os.path.dirname(HERE))
sys.path.append(os.path.join(WORKS, 'sukhmani-sahib', 'source')); import gurmukhi
sys.path.append(os.path.join(WORKS, '..', 'text')); import standard

DEFAULT = os.path.join(os.path.expanduser('~'), 'npm-sgdb', 'node_modules', '@shabados', 'database', 'build', 'database.sqlite')
SUBSCRIPT = re.compile('[₀-₉]')


def db_path(argv):
    """The database: --db PATH, else $SHABADOS_DB, else ~/npm-sgdb/… (npm install @shabados/database@4.8.7 there)."""
    p = argv[argv.index('--db') + 1] if '--db' in argv else os.environ.get('SHABADOS_DB', DEFAULT)
    if not os.path.exists(p): sys.exit(f'no database at {p}: npm install @shabados/database@4.8.7, then --db <its build/database.sqlite>')
    return p


def line(ascii_text):
    """One database line → the Granth's Unicode line (no vishraams, no spacer, no small numerals)."""
    s = SUBSCRIPT.sub('', ascii_text.replace('Ø', ''))
    s = re.sub(r'\s+', ' ', re.sub(r'[;.,]', '', s)).strip()
    u = gurmukhi.to_unicode(s)
    u = re.sub(r'(?<=॥)\s*([੦-੯]+)\s*(?=॥)', r'\1', u)   # a number mark is compact: ॥੮॥੨੪॥
    return standard.dandas(unicodedata.normalize('NFC', u))


def units(path):
    db = sqlite3.connect(path)
    out, cur = [], None
    for sid, sec, wr, lid, ang, ln, ty, g in db.execute(
            'select s.id, s.section_id, s.writer_id, l.id, l.source_page, l.source_line, l.type_id, l.gurmukhi '
            'from shabads s join lines l on l.shabad_id = s.id where s.source_id = 1 order by s.order_id, l.order_id'):
        if cur is None or cur['sid'] != sid:
            cur = {'sid': sid, 'section': sec, 'writer': wr, 'lines': []}; out.append(cur)
        cur['lines'].append({'id': lid, 'ang': ang, 'line': ln, 'type': ty, 'v': line(g), 'raw': g})
    return out


def sections(path):
    db = sqlite3.connect(path)
    return {r[0]: {'en': r[1], 'gu': gurmukhi.to_unicode(r[2]), 'start': r[3], 'end': r[4]} for r in db.execute(
        'select id, name_english, name_gurmukhi, start_page, end_page from sections where source_id = 1')}


def translations(path, source_id):
    """{line id: (translation, additional_information)} of one translation source."""
    db = sqlite3.connect(path)
    return {r[0]: (r[1], r[2]) for r in db.execute(
        'select t.line_id, t.translation, t.additional_information from translations t join lines l on l.id = t.line_id '
        'join shabads s on s.id = l.shabad_id where s.source_id = 1 and t.translation_source_id = ?', (source_id,))}
