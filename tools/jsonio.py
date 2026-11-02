"""How shared library files are written, so that sessions working in parallel merge cleanly.

A file that many works add to (library/glossary/<lang>.json, library/index.json) must not be one long line:
two branches that each add a word would always conflict. These helpers write one entry per line, sorted,
so additions from different branches land on different lines. tools/site/build.py re-writes those files
with these helpers on every build, so the format never drifts. Per-work files stay compact.
"""
import json

def dumps_lines(d):
    """A dict as one "key": value entry per line, keys sorted."""
    items = sorted(d.items())
    return '{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False, separators=(',', ':')) for k, v in items) + '\n}\n'

def dump_glossary(path, d):
    open(path, 'w').write(dumps_lines(d))

def dump_shelf(path, tree):
    open(path, 'w').write(json.dumps(tree, ensure_ascii=False, indent=1) + '\n')

def dump_library(out, rel, obj):
    """Write one of a work's files, library/<rel> under `out`, compact, after the writing standard
    (tools/text/standard.py): a work.json's verses and transliteration, a meaning file's daṇḍas. Every exporter writes
    through this, so no work can differ from the standard. Returns the file's size."""
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'text')); import standard
    obj = standard.finish(rel, obj)
    p = os.path.join(out, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f: json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(p)

def dump_meanings(path, obj):
    """A meaning source in a work's folder (tools/works/<work>/meanings/<lang>/<source>.json): its settings first, then
    `m` and `notes` one verse per line in the text's order, so a change to one meaning is a one-line diff."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    head = {k: v for k, v in obj.items() if k not in ('m', 'notes')}
    lines = ['{'] + [json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) + ',' for k, v in head.items()]
    blocks = [k for k in ('m', 'notes') if k in obj]
    for b, k in enumerate(blocks):
        rows = [json.dumps(i, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for i, v in obj[k].items()]
        lines.append(json.dumps(k) + ': {'); lines.append(',\n'.join(rows)); lines.append('}' + (',' if b < len(blocks) - 1 else ''))
    if not blocks: lines[-1] = lines[-1].rstrip(',')
    open(path, 'w', encoding='utf-8').write('\n'.join(lines) + '\n}\n')

# ---- a work loaded by part (work.json "load": "parts", docs/LIBRARY.md §3 and §5) ----
# Its meaning sources are each a header (library/<work>/meanings/<id>.json: the source's fields, "load": "parts" and an
# empty "m") and one file per part (meanings/<id>/<part index>.json: the same fields, "part" and only that part's "m"
# and "p"); its own word senses are one file per part (glossary/<part index>.json). These read them whole.

def read_meanings(path):
    """A meaning source of the library (library/<work>/meanings/<id>.json), whole: the parts of a source loaded by part
    are joined (its header's "load" and "m" give way to them)."""
    import os
    with open(path, encoding='utf-8') as f: s = json.load(f)
    if s.get('load') != 'parts': return s
    d = path[:-5]; s = {k: v for k, v in s.items() if k != 'load'}; s['m'] = {}; p = {}
    for k in sorted((int(f[:-5]) for f in os.listdir(d) if f.endswith('.json')) if os.path.isdir(d) else []):
        with open(os.path.join(d, f'{k}.json'), encoding='utf-8') as f: x = json.load(f)
        s['m'].update(x.get('m', {})); p.update(x.get('p', {}))
    if p: s['p'] = p
    return s

def read_work_glossary(workdir):
    """A work's own senses of words (library/<work>/glossary.json, or glossary/<part>.json for a work loaded by part),
    whole: {lang: {word: entry}}; {} when it has none."""
    import os
    one = os.path.join(workdir, 'glossary.json'); d = os.path.join(workdir, 'glossary')
    files = [one] if os.path.exists(one) else sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.json')) if os.path.isdir(d) else []
    out = {}
    for fn in files:
        with open(fn, encoding='utf-8') as f:
            for lg, words in json.load(f).items(): out.setdefault(lg, {}).update(words)
    return out
