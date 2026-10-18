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
