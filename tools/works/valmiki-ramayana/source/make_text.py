"""Write ../text.txt: the settled verses (settle.py, from the owner's Gita Press Sanskrit–English book, read from its text
layer) under their kāṇḍas and sargas, each sarga with its titles from the two Gita Press editions:
  - Hindi: topics_hi.json, the Hindi edition's (code 77) sarga titles as decoded by hindi/decode.py;
  - English: the Sanskrit–English edition's heading of the sarga as parse.py reads it, the printed running heads and
    "Canto N" marks taken off, in plain Indian English (plain_en.plain).
Needs the book read by the first steps (README, "How it is made"):

    python3 make_text.py <book.json>
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import english, settle, plain_en

HEAD = ['# Śrīmad Vālmīki Rāmāyaṇa: 23,701 verses. Made by source/make_text.py from the owner\'s Gita Press book (read from its',
        '# text layer, no OCR); change it there, not here. Every correction and choice: reconciliation.md. Topics: the sarga',
        '# titles of the Gita Press Hindi (code 77) and English (codes 452–453) editions.']

# The English heading of a sarga that parse.py does not find on its page: the book's heading, in plain spelling.
EN_TITLE = {'ayodhya.72': "Entering his father’s apartments and not finding him there, Bharat moves to his mother’s apartments and, having communicated to her the welfare of his maternal grandfather and others on being questioned by her, inquires of her the whereabouts of his father. Kaikeyi then breaks to him the news of his father’s death, attributing it to Shri Ram’s exile and holding herself responsible for the latter, and after comforting him calls upon him to get himself installed on the throne after finishing his father’s obsequies"}

# What prints above a heading on the page and is not part of it: the running head, the kāṇḍa's name, "Canto N".
NOISE = re.compile(r'^\s*(?:Śrīmad V(?:ālmīki-Rāmāyaṇa)?|lmīki-Rāmāyaṇa|\[Book \w+\]|\(\w+kāṇḍa\)|(?:Interpolated )?Canto\s*'
                   r'(?:[IVXLCDM]+?|\d+)?(?=Canto|\s|$))\s*')

def english_title(sarga):
    t = ' '.join(english.convert(' '.join(sarga['title_en'])).split())
    while True:
        t2 = NOISE.sub('', t, count=1)
        if t2 == t: return t.strip()
        t = t2

def main():
    book = json.load(open(sys.argv[1], encoding='utf-8'))
    corrections = json.load(open(os.path.join(HERE, 'review', 'corrections.final.json'), encoding='utf-8'))
    items, _ = settle.settle(book, corrections)
    hi = json.load(open(os.path.join(HERE, 'topics_hi.json'), encoding='utf-8'))
    en = {}
    for k in book:
        for s in k['sargas']:
            sec = f"{k['kanda']}.{s['_key']}"
            en[sec] = EN_TITLE.get(sec) or plain_en.plain(english_title(s))
    assert set(hi) == set(en), set(hi) ^ set(en)
    out, part, sec = list(HEAD) + [''], None, None
    for it in items:
        p = it['s'].split('.')[0]
        if p != part:
            if part: out.append('')
            out.append('@part ' + p); part = p
        if it['s'] != sec:
            sec = it['s']; out += ['@section ' + sec, f'@topic {hi[sec]} | {en[sec]}']
        out.append(f"[{it['id']} {it['y']} {it['n']}]")
        out += it['v']
    bad = [l for l in out if l.startswith('@topic') and plain_en.MARK.search(l.split('|', 1)[1])]
    assert not bad, bad[:3]
    open(os.path.join(HERE, '..', 'text.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(len(items), 'verses,', len(hi), 'sargas')

if __name__ == '__main__':
    main()
