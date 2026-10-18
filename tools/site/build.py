"""Build the website and the single-file versions.

python3 tools/site/build.py
  1. registers each work's meaning/audio sources and checks the library (library.py); stops on any problem
  2. writes the website at the repository root: index.html, app/ (app.js, style.css, fonts.css, fonts, icon), manifest.json, sw.js
  3. writes dist/Scriptures-offline.html (everything in one file) and dist/Scriptures-artifact.html (for a claude.ai artifact)
Sources of the app: tools/site/app.js and tools/site/index_template.html. Never edit the generated files.
"""
import base64, json, os, glob, shutil, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))   # repository root
SITE = ROOT   # the website lives at the repository root (GitHub Pages)
F = os.environ.get('FONTS') or os.path.join(ROOT, 'tools', 'fonts')
nd = F + '/_fontsource_noto-serif-devanagari/package/files/'; lt = F + '/_fontsource_literata/package/files/'
if not os.path.isdir(nd): nd = lt = F + '/'
DEVR = 'U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+25CC,U+A830-A839,U+A8E0-A8FF'
GURR = 'U+0A00-0A7F,U+200C-200D,U+25CC'   # Gurmukhi (Gurbani)
LX = 'U+0100-024F,U+1E00-1EFF,U+0300-036F'
FONTS = [('NSDev', nd + 'noto-serif-devanagari-devanagari-400-normal.woff2', 400, 'normal', DEVR), ('NSDev', nd + 'noto-serif-devanagari-devanagari-700-normal.woff2', 700, 'normal', DEVR),
         ('NSDev', lt + 'literata-latin-400-normal.woff2', 400, 'normal', 'U+0000-00FF,U+2000-206F'), ('NSDev', lt + 'literata-latin-600-normal.woff2', 700, 'normal', 'U+0000-00FF,U+2000-206F'),
         ('Literata', lt + 'literata-latin-400-normal.woff2', 400, 'normal', None), ('Literata', lt + 'literata-latin-ext-400-normal.woff2', 400, 'normal', LX),
         ('Literata', lt + 'literata-latin-400-italic.woff2', 400, 'italic', None), ('Literata', lt + 'literata-latin-ext-400-italic.woff2', 400, 'italic', LX),
         ('TrLat', F + '/gentium-tr-italic.woff2', 400, 'italic', None), ('TrLat', F + '/gentium-tr-regular.woff2', 400, 'normal', None),
         ('Literata', lt + 'literata-latin-600-normal.woff2', 600, 'normal', None), ('Literata', lt + 'literata-latin-ext-600-normal.woff2', 600, 'normal', LX),
         ('NSDev', F + '/noto-serif-gurmukhi-gurmukhi-400-normal.woff2', 400, 'normal', GURR), ('NSDev', F + '/noto-serif-gurmukhi-gurmukhi-700-normal.woff2', 700, 'normal', GURR),
         ('Literata', F + '/noto-serif-gurmukhi-gurmukhi-400-normal.woff2', 400, 'normal', GURR), ('Literata', F + '/noto-serif-gurmukhi-gurmukhi-700-normal.woff2', 600, 'normal', GURR)]
def face(fam, url, w, st, ur): return f"@font-face{{font-family:'{fam}';src:url({url}) format('woff2');font-weight:{w};font-style:{st};font-display:swap;{('unicode-range:' + ur + ';') if ur else ''}}}"
tpl = open(os.path.join(HERE, 'index_template.html')).read()
app = open(os.path.join(HERE, 'app.js')).read()
# ---------- library: register sources + check ----------
import sys; sys.path.insert(0, HERE)
from library import prepare, LibraryError
try: WORKS = prepare(os.path.join(ROOT, 'library'))
except LibraryError as e: sys.exit('LIBRARY PROBLEM: ' + str(e))
print('works', WORKS)
# keep shared files one entry per line (tools/jsonio.py) so parallel branches merge cleanly
sys.path.insert(0, os.path.dirname(HERE)); import jsonio
for f in glob.glob(os.path.join(ROOT, 'library', 'glossary', '*.json')):
    if os.path.basename(f) != 'languages.json': jsonio.dump_glossary(f, json.load(open(f)))
jsonio.dump_shelf(os.path.join(ROOT, 'library', 'index.json'), json.load(open(os.path.join(ROOT, 'library', 'index.json'))))
# the app must at least parse: a syntax error would leave every reader with a blank page
import subprocess
r = subprocess.run(['node', '--check', os.path.join(HERE, 'app.js')], capture_output=True, text=True)
if r.returncode: sys.exit('APP PROBLEM: tools/site/app.js does not parse\n' + r.stderr)
# ---------- website ----------
if os.path.isdir(os.path.join(SITE, 'app')): shutil.rmtree(os.path.join(SITE, 'app'))
APPD = os.path.join(SITE, 'app'); os.makedirs(os.path.join(APPD, 'fonts'), exist_ok=True)
css = ''
for fam, path, w, st, ur in FONTS:
    name = os.path.basename(path); shutil.copy(path, os.path.join(APPD, 'fonts', name)); css += face(fam, 'fonts/' + name, w, st, ur) + '\n'
open(os.path.join(APPD, 'fonts.css'), 'w').write(css)
m = re.search(r'<style>\n/\*FONTS\*/\n(.*?)</style>', tpl, re.S)
open(os.path.join(APPD, 'style.css'), 'w').write(m.group(1))
open(os.path.join(APPD, 'app.js'), 'w').write(app)
# version every asset by its content, so a page never runs a cached app.js from an older release
import hashlib
hv = lambda name: hashlib.sha1(open(os.path.join(APPD, name), 'rb').read()).hexdigest()[:10]
VJS, VCSS, VF = 'app/app.js?v=' + hv('app.js'), 'app/style.css?v=' + hv('style.css'), 'app/fonts.css?v=' + hv('fonts.css')
head = '<link rel="manifest" href="manifest.json"><link rel="icon" href="app/icon.svg"><link rel="stylesheet" href="' + VF + '"><link rel="stylesheet" href="' + VCSS + '">\n'
html = tpl.replace(m.group(0), head).replace('/*BUNDLE*/\n', '').replace('<script>\n/*APP*/\n</script>', '<script src="' + VJS + '"></script>')
open(os.path.join(SITE, 'index.html'), 'w').write(html)
json.dump({'name': 'शास्त्र · Scriptures', 'short_name': 'Scriptures', 'start_url': './', 'display': 'standalone', 'background_color': '#F6F6F2', 'theme_color': '#2B3A8C', 'icons': [{'src': 'app/icon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]}, open(os.path.join(SITE, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(APPD, 'icon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2B3A8C"/><text x="32" y="44" text-anchor="middle" font-size="34" fill="#F2A653" font-family="serif">ॐ</text></svg>')
files = ['./', 'index.html', 'manifest.json', 'app/icon.svg', VJS, VCSS, VF] + ['app/fonts/' + os.path.basename(p[1]) for p in FONTS]
ver = hashlib.sha1((VJS + VCSS + VF).encode()).hexdigest()[:10]
open(os.path.join(SITE, 'sw.js'), 'w').write("""const V='s-%s';const CORE=%s;
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))));self.clients.claim();});
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin!==location.origin)return;
 e.respondWith(fetch(e.request, {cache: 'no-cache'}).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r;}).catch(()=>caches.match(e.request)));});
""" % (ver, json.dumps(files)))
open(os.path.join(SITE, '.nojekyll'), 'w').write('')
# ---------- single-file bundle ----------
LIBD = os.path.join(SITE, 'library')
bundle = {'files': {}}
for f in glob.glob(LIBD + '/**/*.json', recursive=True): bundle['files'][os.path.relpath(f, LIBD)[:-5]] = json.load(open(f))
css64 = ''.join(face(fam, 'data:font/woff2;base64,' + base64.b64encode(open(path, 'rb').read()).decode(), w, st, ur) for fam, path, w, st, ur in FONTS)
js = 'window.__BUNDLE=' + json.dumps(bundle, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
one = tpl.replace('/*FONTS*/', css64).replace('/*BUNDLE*/\n', '<script>' + js + '</script>\n').replace('/*APP*/', app)
out = os.path.join(ROOT, 'dist'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'Scriptures-offline.html'), 'w').write(one)
a = re.sub(r'^<!doctype html>\s*<html[^>]*>\s*<head>\s*', '', one, flags=re.I)
a = a.replace('<meta charset="utf-8">\n', '').replace('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n', '')
a = a.replace('</head>\n<body>', '', 1).replace('</body>\n</html>', '')
m = re.search(r'<title>.*?</title>\n', a); art = m.group(0) + '<meta name="claude:viewport-fit-sides" content="cover">\n' + a.replace(m.group(0), '', 1)
open(os.path.join(out, 'Scriptures-artifact.html'), 'w').write(art)
print('site', round(sum(os.path.getsize(p) for p in glob.glob(SITE + '/**', recursive=True) if os.path.isfile(p)) / 1e6, 2), 'MB; bundle', round(len(one.encode()) / 1e6, 2), 'MB')
