"""Śrī Rāmacaritamānasa: the Gita Press book data (app_data.json, made by make_appdata.py; README.md) → the work's files.

Writes   ../text.txt                   every verse, with its kāṇḍa, dohā section, language and Gita Press's topic headings
         ../book.json                  the 30-day and 9-day plans, the pārāyaṇa vidhi (with visarjan.json), and
                                       `renamed` / `split` for the joint caupāīs (below); work.json includes it
         ../meanings/hi/gitapress.json Gita Press's Hindi bhāvārtha (Hanumānprasād Poddār), with its footnotes
         ../meanings/en/gitapress.json Gita Press's English translation, with its footnotes
Run it after a change to the book data; then python3 tools/works/export.py manas sundarkand shri-ramchandra-kripalu.

The language of each verse: the Mānas is in Awadhi (awa). Its Sanskrit (sa) passages: every śloka, Atri's stuti
(Araṇya 4, "namāmi bhakta vatsalaṁ"), Sutīkṣṇa's stuti (Araṇya 11, "śyāma tāmarasa dāma śarīraṁ") and the Rudrāṣṭaka
(Uttara 108, "namāmīśamīśāna"). The other stutis (e.g. Laṅkā 111, Uttara 14) are Sanskritised Awadhi in Awadhi
spelling, so they stay awa; awa falls back to sa for tatsama words.

One caupāī per verse (the owner's rule): in 16 places Gita Press prints two or three caupāīs as one (e.g. ॥३-५॥)
because its translation renders them jointly. Each becomes its own verse — bal.6.cau3-5 → bal.6.cau3, cau4, cau5 —
split where the book's transliteration numbers each caupāī. The joint Gita Press meaning goes under the last of the
group (where Gita Press prints its number), and the earlier ones point to it. `renamed` maps each joint id to its first
part, so readers' bookmarks, notes and places saved on a joint id follow (tools/site/app.js), and
tools/audio/make_timings.py reads joint ids in its caches the same way; `split` moves a place saved as a bare position.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(WORK)); import textfile
sys.path.insert(0, os.path.join(WORK, '..', '..')); import jsonio

d = json.load(open(os.path.join(HERE, 'app_data.json'), encoding='utf-8'))
IT, EG = d['it'], d['eg']
PART_KEYS = ['bal', 'ayodhya', 'aranya', 'kishkindha', 'sundar', 'lanka', 'uttar']
assert len(d['kands']) == len(PART_KEYS)

def verse_lang(x):
    if x['y'] == 'shloka' or x['id'].startswith('aranya.4.cha') or re.fullmatch(r'aranya\.11\.cau[2-8]|uttar\.108\.cau[1-8]', x['id']): return 'sa'
    return 'awa'

JOINT = {}   # joint id → [ids of its parts]
def split_joint(o):
    a, b = map(int, o['n'].split('-'))
    groups, st = [], 0
    for k, t in enumerate(o['t']):
        m = re.search(r'॥(\d+)॥\s*$', t)
        if m: groups.append((m.group(1), st, k + 1)); st = k + 1
    assert [int(g[0]) for g in groups] == list(range(a, b + 1)) and st == len(o['v']), f"cannot split {o['id']}"
    base = o['id'].rsplit('.cau', 1)[0]
    return [dict(o, id=f'{base}.cau{n}', n=n, v=o['v'][s0:s1], t=o['t'][s0:s1]) for n, s0, s1 in groups]

items = []
for x in IT:
    o = {'id': x['id'], 'p': x['k'], 's': x['s'], 'y': x['y'], 'n': x['n'], 'v': x['v'], 't': x.get('t') or []}
    if verse_lang(x) != 'awa': o['l'] = verse_lang(x)
    if o['y'] == 'cau' and re.fullmatch(r'\d+-\d+', o['n']):
        parts = split_joint(o); JOINT[o['id']] = [q['id'] for q in parts]; items += parts
    else: items.append(o)
for o in items: o.pop('t')
assert len({x['id'] for x in items}) == len(items), 'duplicate ids after splitting'
FIRST = {k: v[0] for k, v in JOINT.items()}; LAST = {k: v[-1] for k, v in JOINT.items()}
ids = [x['id'] for x in IT]
topics = [{'id': FIRST.get(ids[t['i']], ids[t['i']]), 'hi': t['hi'], 'en': t.get('en') or t['hi']} for t in d['topics']]
textfile.write(os.path.join(WORK, 'text.txt'), items, topics, PART_KEYS, 'awa', [
    'Śrī Rāmacaritamānasa, Gita Press (Gorakhpur): every verse. Made by source/make.py from the book data; do not edit',
    'here (a fix goes in source/text_fixes.json, source/README.md). Topic headings are Gita Press\'s; ours are topics.json.'])

plans = {k: {'n': len(v), 'end': [LAST.get(ids[v[str(n)]], ids[v[str(n)]]) for n in range(1, len(v) + 1)]} for k, v in d['P'].items()}   # a day ends after the whole group
book = {
    'plans': [
        {'id': 'M', 'name': {'hi': 'मासपारायण', 'en': '30-day'}, 'long': {'hi': 'मासपारायण (३० दिन)', 'en': 'Māsa-pārāyaṇa (30 days)'}, 'unit': {'hi': 'विश्राम', 'en': 'Vishram'}, 'before': ['vidhi'], 'after': ['aarti', 'visarjan'], **plans['M']},
        {'id': 'N', 'name': {'hi': 'नवाह्नपारायण', 'en': '9-day'}, 'long': {'hi': 'नवाह्नपारायण (९ दिन)', 'en': 'Navāhna-pārāyaṇa (9 days)'}, 'unit': {'hi': 'विश्राम', 'en': 'Vishram'}, 'before': ['vidhi'], 'after': ['aarti', 'visarjan'], **plans['N']},
    ],
    'renamed': FIRST,
    # a reader's place saved as a bare item position (no id) counts the joint caupāīs as one: [position, items added there]
    'split': [[k, len(JOINT[x['id']]) - 1] for k, x in enumerate(IT) if x['id'] in JOINT],
    'vidhi': {**d['vidhi'], 'visarjan': {k: v for k, v in json.load(open(os.path.join(HERE, 'visarjan.json'), encoding='utf-8')).items() if k != 'source'}},   # kathā-visarjana: visarjan.md
    'vg': d['vg'],
}
json.dump(book, open(os.path.join(WORK, 'book.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# ---- Gita Press's meanings ----
DEVA = str.maketrans('0123456789', '०१२३४५६७८९'); BY = {x['id']: x for x in items}
def spread(m, notes, lg):
    """A joint meaning goes under the last part of its group; the earlier parts say where it is."""
    for old, new in JOINT.items():
        if old not in m: continue
        e = m.pop(old); f = notes.pop(old, None); last = BY[new[-1]]['n']
        for q in new[:-1]: m[q] = '(इस चौपाईका अर्थ नीचे, चौपाई ' + last.translate(DEVA) + ' के साथ दिया गया है।)' if lg == 'hi' else f'(The meaning of this caupāī is given below, with caupāī {last}.)'
        m[new[-1]] = e
        if f is not None: notes[new[-1]] = f
    order = [x['id'] for x in items]
    return {i: m[i] for i in order if i in m}, {i: notes[i] for i in order if i in notes}
# A footnote comes from the book one printed line per entry; the lines of one note are joined, so the app shows each note
# as one paragraph. A note starts with its mark (*, †, ‡, §, # or "2."); any other line continues the one before. A line
# that ends in a hyphen keeps it (forty-eight, mind-born), except where the printer split a word (WORD_SPLIT).
MARK = re.compile(r'^\s*(?:[*†‡§¶#]|\d+\.\s)')
WORD_SPLIT = {'expand-ing', 'consti-tute', 'circumambu-lation'}
COMPOUND = {'wind-god', 'forty-eight', 'monkey-god', 'ill-will', 'non-Brāhmaṇa', 'mind-born', 'sixty-four'}
def note_lines(lines):
    out = []
    for l in lines:
        l = l.strip()
        if not out or MARK.match(l): out.append(l); continue
        if out[-1].endswith('-'):
            pair = re.sub(r'^\W+|\W+$', '', out[-1].split()[-1] + l.split()[0])   # the two halves, without brackets or commas
            assert pair in WORD_SPLIT | COMPOUND, f'a line ends in a hyphen: is "{pair}" one split word (WORD_SPLIT) or a hyphenated word (COMPOUND)?'
            out[-1] = (out[-1][:-1] if pair in WORD_SPLIT else out[-1]) + l
        else: out[-1] += ' ' + l
    return out
hi, hin = {}, {}
for x in IT:
    hi[x['id']] = x['h']
    if x.get('f'): hin[x['id']] = note_lines(x['f'])
en, enn = {}, {}
for x in IT:
    g = EG.get(str(x['g'])) if x.get('g') is not None else None
    if not g: continue
    en[x['id']] = g['x']
    if g.get('f'): enn[x['id']] = note_lines(g['f'])
for lg, m, notes, title in (('hi', hi, hin, {'hi': 'गीताप्रेस — भावार्थ (हनुमानप्रसाद पोद्दार)', 'en': 'Gita Press — Hindi bhāvārtha (Hanumānprasād Poddār)'}),
                            ('en', en, enn, {'hi': 'गीताप्रेस — अंग्रेज़ी अनुवाद', 'en': 'Gita Press — English translation'})):
    m, notes = spread(m, notes, lg)
    jsonio.dump_meanings(os.path.join(WORK, 'meanings', lg, 'gitapress.json'), {'title': title, 'order': 1, 'copied': True, 'm': m, 'notes': notes})
print(f'{len(items)} verses ({len(JOINT)} joint caupāīs split into {sum(len(v) for v in JOINT.values())}); meanings hi {len(hi)}, en {len(en)}')
