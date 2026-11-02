"""Merge the written word batches (source/words/out/*.json) into the work's own dictionary, glossary/sa.json.

Every entry must have en, hi, r and g (p for joined words); `src` (iitk, vr, iitk+vr, ours) goes to source/words/src.json; a word already in the dictionary keeps its entry
(a later batch never overwrites an earlier, checked one). The English of entries written before the owner's rule (the
witnesses' glosses copied as they are) is rewritten by that rule in out-en/*.json ({word: {en, src}}), applied last. The result is written one word per line, sorted
(tools/jsonio.py), so additions from different branches merge.

    python3 merge.py
"""
import json, os, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import jsonio
G = os.path.join(HERE, '..', '..', 'glossary', 'sa.json')
gl = json.load(open(G)) if os.path.exists(G) else {}
bad, added = [], 0
SRC = os.path.join(HERE, 'src.json')
src = json.load(open(SRC)) if os.path.exists(SRC) else {}
for f in sorted(glob.glob(os.path.join(HERE, 'out', '*.json'))):
    for w, e in json.load(open(f)).items():
        if not all(isinstance(e.get(k), str) and e[k].strip() for k in ('en', 'hi', 'r', 'g')):
            bad.append((os.path.basename(f), w)); continue
        if 'p' in e and not (isinstance(e['p'], list) and all(isinstance(x, list) and len(x) == 2 for x in e['p'])):
            bad.append((os.path.basename(f), w)); continue
        if w not in gl:
            gl[w] = {k: e[k] for k in ('hi', 'en', 'r', 'g', 'p') if k in e}; added += 1
        src[w] = e.get('src', 'ours-reworded')      # where en comes from; batches written before the owner's rule
                                                     # (glosses copied as they are) say ours-reworded: to redo
redone = 0
for f in sorted(glob.glob(os.path.join(HERE, 'out-en', '*.json'))):
    for w, e in json.load(open(f)).items():
        if w not in gl or not (isinstance(e.get('en'), str) and e['en'].strip()) or e.get('src') not in ('iitk', 'vr', 'iitk+vr', 'ours'):
            bad.append((os.path.basename(f), w)); continue
        gl[w]['en'] = e['en'].strip(); src[w] = e['src']; redone += 1
jsonio.dump_glossary(G, gl)
jsonio.dump_glossary(SRC, src)
print(added, 'added;', redone, 'English rewritten;', len(gl), 'words in glossary/sa.json;', len(bad), 'incomplete entries skipped', bad[:10])
