"""आरति श्रीरामायनजी की (the āratī of the Śrī Rāmacaritamānasa): the Mānas's Gita Press āratī → ../text.txt.

Source of truth for the text: the āratī printed at the end of the owner's Gita Press Mānas (scriptures-data:
hinduism/granth/tulsidas/ramcharitmanas/books/gitapress/hindi.pdf), as the Mānas's own generator reads it
(tools/works/manas/source/make_appdata.py → tools/works/manas/book.json, vidhi.aarti: the āratī page of its plans).
Taken from there line by line, never retyped, so the two can never differ.

Its 18 printed lines are the refrain (टेक, lines 1–2) and four stanzas of four lines each (पद, lines 3–18). Each line
ends in । (the first half) or ॥ (the second); the stanzas are not numbered in the book, so no number is printed here
(each still has its n, 1–4).

Writes   ../text.txt
Run it after a change to the Mānas's book.json; then python3 tools/works/export.py ramayan-aarti.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(WORK)); import textfile

lines = json.load(open(os.path.join(WORK, '..', 'manas', 'book.json'), encoding='utf-8'))['vidhi']['aarti']
assert len(lines) == 18, f'the Gita Press āratī has 18 lines, book.json has {len(lines)}'
lines = [re.sub(r'\s*।\s*।\s*$', ' ॥', re.sub(r'\s*॥\s*$', ' ॥', l)).strip() for l in lines]   # ।। is one ॥ (docs/PLAYBOOK.md §3)
assert all(re.search(r' (।|॥)$', l) for l in lines), 'every line ends in । or ॥'

items = [{'id': 'aarti.tek', 'p': 0, 's': 'aarti', 'y': 'tek', 'v': lines[:2]}]
items += [{'id': f'aarti.pad{k}', 'p': 0, 's': 'aarti', 'y': 'pad', 'n': str(k), 'v': lines[2 + 4 * (k - 1):2 + 4 * k]} for k in range(1, 5)]
textfile.write(os.path.join(WORK, 'text.txt'), items, [{'id': 'aarti.tek', 'hi': 'आरति श्रीरामायनजी की', 'en': 'Aarti Shri Ramayanji Ki'}],
               ['aarti'], 'awa', ['आरति श्रीरामायनजी की (Ārati Śrīrāmāyanajī Kī): the verse text, made by source/make.py from the Mānas\'s Gita Press āratī.',
                                  'The source and every choice: reconciliation.md.'])
print('text.txt:', len(items), 'verses')
