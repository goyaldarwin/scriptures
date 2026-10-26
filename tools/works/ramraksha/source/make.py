"""Śrī Rāma Rakṣā Stotram (Budha Kauśika): the owner's sources → the work's files.

Source of truth for the text: the Vande Guru Paramparaam video (YouTube ZIDdE4SZAuw), whose on-screen lines
(Devanagari · transliteration · English) are transcribed from the owner's screenshots into video_text.tsv
(frame number, Devanagari, transliteration, English). Repeated screenshots of the same line are left out of the file.

Writes   ../text.txt                                     the text: invocation, viniyoga, dhyāna, ślokas 1–38, colophon
         ../meanings/en/vande-guru-paramparaam.json      the video's on-screen English meaning, joined per verse
Run it after a change to video_text.tsv; then python3 tools/works/export.py ramraksha.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(WORK)); import textfile
sys.path.insert(0, os.path.join(WORK, '..', '..')); import jsonio

rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'video_text.tsv'), encoding='utf-8') if l.strip()]
DIG = '०१२३४५६७८९'
def deva(s): return re.sub(r'\s+', ' ', s).strip()   # the transliteration is made from it (tools/text/standard.py)

# frame 001 the invocation · 002–008 viniyoga · 009 the heading "ध्यानम्" (a topic, not a verse)
# 010–013 the dhyāna verse · 014–108 ślokas 1–38 (a śloka ends with its number) · 109–110 colophon
items, en = [], {}
def add(id, y, n, rs):
    items.append({'id': id, 'p': 0, 's': id, 'y': y, 'n': n, 'v': [deva(r[1]) for r in rs]})
    en[id] = ' '.join(r[3].strip() for r in rs)
F = {int(r[0]): r for r in rows}
add('mangal', 'mantra', '', [F[1]])
add('viniyoga', 'viniyoga', '', [F[k] for k in range(2, 9)])
add('dhyana', 'dhyana', '', [F[k] for k in range(10, 14)])
buf, num = [], 0
for k in sorted(F):
    if not 14 <= k <= 108: continue
    buf.append(F[k]); m = re.search(r'॥\s*([०-९]+)\s*॥\s*$', F[k][1])
    if m:
        n = int(''.join(str(DIG.index(c)) for c in m.group(1))); num += 1
        assert n == num, ('śloka numbers out of order', k, n, num)
        add('sh%d' % n, 'shloka', str(n), buf); buf = []
assert not buf and num == 38, (num, buf)
add('iti', 'iti', '', [F[109], F[110]])

TOPICS = [{'id': 'viniyoga', 'hi': 'विनियोग', 'en': 'Viniyoga'}, {'id': 'dhyana', 'hi': 'ध्यानम्', 'en': 'Dhyānam'},
          {'id': 'sh1', 'hi': 'स्तोत्र', 'en': 'Stotra'}]
textfile.write(os.path.join(WORK, 'text.txt'), items, TOPICS, ['ramraksha'], 'sa', [
    'Śrī Rāma Rakṣā Stotram, as the Vande Guru Paramparaam video shows it. Made by source/make.py from video_text.tsv;',
    'do not edit here. Every choice: reconciliation.md.'])

jsonio.dump_meanings(os.path.join(WORK, 'meanings', 'en', 'vande-guru-paramparaam.json'), {
    'about': "The English meaning the Vande Guru Paramparaam video (YouTube ZIDdE4SZAuw) shows on screen, joined per verse.",
    'title': {'hi': 'वन्दे गुरु परम्पराम् — अंग्रेज़ी अर्थ', 'en': 'Vande Guru Paramparaam — English meaning'},
    'order': 2, 'copied': True, 'm': en})
print(len(items), 'verses;', len(en), 'English meanings')
