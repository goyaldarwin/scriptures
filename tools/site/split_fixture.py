"""A work loaded by part, for the tests (smoke_test.py, ux_test.py).

The Kaṭha Upaniṣad (two adhyāyas, its own word senses in both) is exported again by the real exporter with
`"load": "parts"` and its own section labels (`"sections"`: Vallī 1 …), into a temporary folder, and checked by
library.py as the build checks a work. `serve(tmp)` then serves the repository with that work in place of the published
one, so the app is tested on a split work without one on the shelf.

    lib, path = make(tmp)       # tmp: an empty folder
    srv = serve(lib, path)      # srv.server_address[1]: the port
"""
import functools, glob, http.server, json, os, shutil, socketserver, subprocess, sys, threading
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
WORK = 'katha-upanishad'
# the labels of its sections, in the form a big work gives them (सर्ग १ / Sarga 1): Devanagari digits, shown as 1 2 3
SECTIONS = {'shanti': {'hi': 'शान्तिपाठ', 'en': 'Śānti Pāṭha'},
            **{f'v{a}.{v}': {'hi': f'वल्ली {"०१२३"[a]}.{"०१२३"[v]}', 'en': f'Vallī {a}.{v}'} for a in (1, 2) for v in (1, 2, 3)}}

def make(tmp):
    """Export the split fixture into tmp/library; returns (that library folder, the work's path)."""
    src = os.path.join(ROOT, 'tools', 'works', WORK)
    works = os.path.join(tmp, 'tools', 'works'); os.makedirs(works)
    for name in ('jsonio.py', 'meanings', 'text'): os.symlink(os.path.join(ROOT, 'tools', name), os.path.join(tmp, 'tools', name))
    for name in ('export.py', 'textfile.py'): shutil.copy(os.path.join(ROOT, 'tools', 'works', name), works)
    shutil.copytree(src, os.path.join(works, WORK), ignore=shutil.ignore_patterns('source', 'audio'))
    mp = os.path.join(works, WORK, 'work.json'); M = json.load(open(mp, encoding='utf-8'))
    M['load'] = 'parts'; M['sections'] = SECTIONS
    json.dump(M, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    lib = os.path.join(tmp, 'library'); os.makedirs(lib)
    r = subprocess.run([sys.executable, os.path.join(works, 'export.py'), '--out', lib, WORK], capture_output=True, text=True)
    if r.returncode: raise SystemExit('split fixture: export failed\n' + r.stdout + r.stderr)
    path = M['path']
    for f in glob.glob(os.path.join(ROOT, 'library', path, 'audio', '*.json')):   # its recordings, as published
        os.makedirs(os.path.join(lib, path, 'audio'), exist_ok=True); shutil.copy(f, os.path.join(lib, path, 'audio'))
    sys.path.insert(0, HERE); import library   # registers the sources and checks it, as the build does
    real = os.path.join(ROOT, 'library'); LANGS = json.load(open(os.path.join(real, 'glossary', 'languages.json')))
    leaf = {'id': WORK, 'work': WORK, 'path': path}
    library.check_work(lib, leaf, LANGS)
    G = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(real, 'glossary', '*.json')) if not f.endswith('languages.json')}
    library.check_words(lib, path, json.load(open(os.path.join(lib, path, 'work.json'), encoding='utf-8')), LANGS, G, library.word_rule())
    return lib, path

def serve(lib, path):
    """The repository root, with library/<path>/ served from the fixture."""
    pre = '/library/' + path + '/'
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def translate_path(self, p):
            q = p.split('?', 1)[0].split('#', 1)[0]
            if q.startswith(pre): return os.path.join(lib, path, *q[len(pre):].split('/'))
            return super().translate_path(p)
    s = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=ROOT)); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

if __name__ == '__main__':   # make it once and list what it wrote
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        lib, path = make(t)
        for f in sorted(glob.glob(os.path.join(lib, path, '**', '*.json'), recursive=True)): print(os.path.relpath(f, lib), os.path.getsize(f))
