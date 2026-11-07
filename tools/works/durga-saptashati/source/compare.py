"""Compare the text's 700 mantras with the Gita Press witness (witness/gitapress.json, made by gitapress.py).

    python3 tools/works/durga-saptashati/source/compare.py

Both are read with spacing, punctuation, numbers, the avagraha, footnote marks, the closing bījas and the nasal spelling
(standard.fold) set aside, so only a difference of words or letters is left. Writes witness/differences.json, every
mantra that differs: the text's reading, the witness's, and the decision (reconciliation.md: the text's reading stays
unless corrections.json corrects it).
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'works')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'text'))
import textfile, standard

def norm(s):
    s = unicodedata.normalize('NFC', s).replace('ड्.ग', 'ङ्ग').replace('ड् .', 'ङ्').replace('ड्.', 'ङ्')
    s = re.sub(r'॥\s*(?:ऐं\s*ॐ|ह्रीं\s*ॐ|क्लीं\s*ॐ|ॐ)\s*॥', '॥', s)
    s = re.sub(r'॥\s*[०-९]+\s*॥', '', s)
    s = re.sub(r'[‘’\'"*\-.ऽ।॥|,\s]', '', s)
    return standard.fold(s)

def main():
    G = json.load(open(os.path.join(HERE, 'witness', 'gitapress.json'), encoding='utf-8'))
    C = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8'))['lines']
    T = {x['id']: x for x in textfile.read(os.path.join(HERE, '..', 'text.txt'))}
    out = []
    for c in range(1, 14):
        for n, gl in G[str(c)].items():
            x = T[f'{c}.{n}']; a, b = ' '.join(x['v']), ' '.join(gl)
            if norm(a) != norm(b):
                out.append({'id': x['id'], 'text': a, 'gitapress': b, 'decision': 'corrected (corrections.json)' if x['id'] in C else 'the text stays'})
    json.dump(out, open(os.path.join(HERE, 'witness', 'differences.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(out), 'mantras differ;', sum(d['decision'] != 'the text stays' for d in out), 'of them corrected where the copy is wrong')

if __name__ == '__main__':
    main()
