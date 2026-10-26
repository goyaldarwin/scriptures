"""Sukhmani Sahib (Guru Arjan Dev Ji): the owner's PDF data → the work's files.

Inputs   lines.json             the PDF's printed lines (extract.py): legacy Gurmukhi, transliteration, English
         gurmukhi.py            legacy font encoding → Unicode Gurmukhi;  structure.py: lines → verses
Writes   ../text.txt                              the Gurmukhi verse lines, 24 Ashtapadis as parts, two topics in each
         ../meanings/en/sant-singh-khalsa.json    the PDF's English (Dr. Sant Singh Khalsa), line by line where the PDF
                                                  prints one English line under each Gurmukhi line
It runs the conversion check (check.py) and the structure check first, and stops on any failure.
Run it after a change to lines.json or the scripts; then python3 tools/works/export.py sukhmani-sahib.
"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(WORK)); import textfile
sys.path.insert(0, os.path.join(WORK, '..', '..')); import jsonio
sys.path.insert(0, os.path.join(WORK, '..', '..', 'text')); import standard
from structure import build, check

subprocess.run([sys.executable, os.path.join(HERE, 'check.py')], check=True, stdout=subprocess.DEVNULL)
items = build(); check(items)


def gur2dev(s):
    """Gurmukhi → Devanagari, letter for letter (for topic names shown in the Hindi interface)."""
    s = re.sub(r'ੱ(.)', lambda m: chr(ord(m.group(1)) - 0x100) + '्' + m.group(1), s)   # addak doubles the next letter
    out = []
    for c in s:
        o = ord(c)
        if c == 'ੰ': out.append('ं')
        elif c == 'ੵ': out.append('्य')
        elif c == 'ੑ': out.append('्ह')
        elif c == 'ੜ': out.append('ड़')
        elif 0x0A00 <= o <= 0x0A7F: out.append(chr(o - 0x100))
        else: out.append(c)
    return ''.join(out)


# Two topics in each Ashtapadi: its Salok and its eight pauris, each named by its first line — the way a passage
# of Gurbani is cited ("ਸਿਮਰਉ ਸਿਮਰਿ ਸਿਮਰਿ ਸੁਖੁ ਪਾਵਉ"). The Hindi name is the line in Devanagari letters, the English
# name its ISO 15919 transliteration (tools/text/standard.py).
def pratik(x, skip):
    j = next(i for i, l in enumerate(x['v']) if not l.startswith(skip))
    first = re.sub(r'\s*॥.*$', '', x['v'][j])
    tr = standard.iso_line(standard.gurmukhi(first))
    return {'hi': gur2dev(first), 'en': tr[:1].upper() + tr[1:]}


topics = []
for k in range(24):
    sal = next(x for x in items if x['p'] == k and x['y'] == 'salok')
    p1 = next(x for x in items if x['p'] == k and x['y'] == 'pauri')
    topics.append({'id': sal['id'], **pratik(sal, ('ਸਲੋਕੁ', 'ੴ'))})   # Ashtapadi 1: after the title line
    topics.append({'id': p1['id'], **pratik(p1, ('ਅਸਟਪਦੀ',))})
textfile.write(os.path.join(WORK, 'text.txt'), items, topics, [str(k) for k in range(1, 25)], 'pa', [
    'Sukhmani Sahib, Sri Guru Granth Sahib, Ang 262–296. Made by source/make.py from the owner\'s PDF; do not edit',
    'here. Every choice: reconciliation.md; source/check.py checks the Gurmukhi conversion.'])

# ---- the PDF's English, copied; only extraction breaks are fixed ----
EN_FIXES = [('obtai n', 'obtain')]   # a word split in the PDF's text layer (see reconciliation.md)
def en_line(l):
    for a, b in EN_FIXES: l = l.replace(a, b)
    return re.sub(r'\s+', ' ', l).strip()
en = {x['id']: [en_line(l) for l in x['e']] if len(x['e']) == len(x['v']) and any(l.strip() for l in x['e'])
      else en_line(' '.join(x['e'])) for x in items}
jsonio.dump_meanings(os.path.join(WORK, 'meanings', 'en', 'sant-singh-khalsa.json'), {
    'about': "The English of the owner's PDF (Dr. Sant Singh Khalsa), copied; only breaks of the PDF's text layer are mended. A list gives it line by line.",
    'title': {'hi': 'अंग्रेज़ी अनुवाद — डॉ. संत सिंह खालसा', 'en': 'English translation — Dr. Sant Singh Khalsa'},
    'order': 2, 'copied': True, 'm': en})
print(f'{len(items)} verses in 24 Ashtapadis; English line by line for {sum(isinstance(v, list) for v in en.values())}')
