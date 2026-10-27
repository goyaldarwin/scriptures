"""Build the website and the single-file versions.

python3 tools/site/build.py
  1. registers each work's meaning/audio sources and checks the library (library.py), re-writes the shared glossary and
     shelf files one entry per line (tools/jsonio.py) and checks that app.js parses; stops on any problem
  2. writes the website at the repository root: index.html, app/ (app.js, style.css, fonts.css, fonts, icons), manifest.json, sw.js,
     privacy.html, get/ (the shared link), CNAME, .nojekyll and .well-known/assetlinks.json
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
         ('Literata', F + '/noto-serif-gurmukhi-gurmukhi-400-normal.woff2', 400, 'normal', GURR), ('Literata', F + '/noto-serif-gurmukhi-gurmukhi-700-normal.woff2', 600, 'normal', GURR),
         # Vedic text (svara marks): Tiro Devanagari Sanskrit draws the svarita ॑ as a clear stroke; Noto's looks like an anusvāra at bold
         ('Vedic', F + '/tiro-devanagari-sanskrit-devanagari-400-normal.woff2', 400, 'normal', None)]
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
# the card a chat app (WhatsApp …) shows under a shared link to the site: title, description and icon (Open Graph)
HOST = json.load(open(os.path.join(ROOT, 'apps', 'app.json')))['host']
SHARE_DESC = 'श्रीरामचरितमानस, सुन्दरकाण्ड, हनुमान चालीसा, उपनिषद्, आरती — मूल पाठ, अर्थ, शब्दार्थ और ऑडियो। निःशुल्क। · Śrī Rāmacaritamānasa, Sundarakāṇḍa, Hanumān Chālīsā, Upaniṣads, āratīs: the text, Hindi and English meanings, the meaning of every word, recitation audio. Free, no ads.'
OG = ('<meta property="og:type" content="website"><meta property="og:site_name" content="शास्त्र · Scriptures"><meta property="og:title" content="शास्त्र · Scriptures">'
      '<meta property="og:description" content="' + SHARE_DESC + '"><meta property="og:image" content="https://' + HOST + '/app/share-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
      '<meta property="og:url" content="https://' + HOST + '/"><meta name="description" content="' + SHARE_DESC + '">\n')
head = OG + '<link rel="manifest" href="manifest.json"><link rel="icon" href="app/icon.svg"><link rel="apple-touch-icon" href="app/apple-touch-icon.png"><link rel="stylesheet" href="' + VF + '"><link rel="stylesheet" href="' + VCSS + '">\n'
html = tpl.replace(m.group(0), head).replace('/*BUNDLE*/\n', '').replace('<script>\n/*APP*/\n</script>', '<script src="' + VJS + '"></script>')
open(os.path.join(SITE, 'index.html'), 'w').write(html)
# installable app (web, Android, iPhone): PNG icons made by tools/store/make_icons.py; one shortcut per work (?w=<work id>)
ICONS = os.path.join(ROOT, 'tools', 'store', 'icons')
for n in ('icon-192.png', 'icon-512.png', 'maskable-512.png', 'apple-touch-icon.png', 'share-card.png'): shutil.copy(os.path.join(ICONS, n), os.path.join(APPD, n))   # share-card: the picture under a shared link (og:image)
_works = []
def _walk(ns):
    for n in ns:
        if 'work' in n: _works.append(n)
        else: _walk(n.get('children', []))
_walk(json.load(open(os.path.join(SITE, 'library', 'index.json'))))
json.dump({'id': './', 'name': 'शास्त्र · Scriptures', 'short_name': 'Scriptures', 'description': 'Read and listen to the scriptures: Rāmacaritamānasa, Sundarakāṇḍa, Śrī Rudram and more, with Hindi and English meanings and word-by-word meanings.',
           'lang': 'hi', 'start_url': './', 'scope': './', 'display': 'standalone', 'orientation': 'portrait', 'background_color': '#F6F6F2', 'theme_color': '#2B3A8C', 'categories': ['books', 'education', 'lifestyle'],
           'icons': [{'src': 'app/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'app/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
                     {'src': 'app/maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}, {'src': 'app/icon.svg', 'sizes': 'any', 'type': 'image/svg+xml'}],
           'shortcuts': [{'name': w['title']['en'], 'short_name': w['title']['en'][:12], 'url': './?w=' + w['work'], 'icons': [{'src': 'app/icon-192.png', 'sizes': '192x192'}]} for w in _works[:4]]},
          open(os.path.join(SITE, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(APPD, 'icon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2B3A8C"/><text x="32" y="44" text-anchor="middle" font-size="34" fill="#F2A653" font-family="serif">ॐ</text></svg>')
files = list(dict.fromkeys(['./', 'index.html', 'manifest.json', 'app/icon.svg', 'app/icon-192.png', 'app/icon-512.png', 'app/apple-touch-icon.png', VJS, VCSS, VF] + ['app/fonts/' + os.path.basename(p[1]) for p in FONTS]))   # each file once: cache.addAll refuses a duplicate, and the worker would never install
ver = hashlib.sha1((VJS + VCSS + VF).encode()).hexdigest()[:10]
# The service worker (offline reading). Two caches: V holds the app shell (CORE) and is renewed on every
# build; LIB holds the library's files (texts, meanings, word lists, audio times) and survives every deploy, so a work opened
# once stays readable offline. Library files are network-first with a short wait — fresh text whenever the phone is online
# (accuracy first; a published correction is seen at the next open) — and from the cache when offline or the network is slow.
open(os.path.join(SITE, 'sw.js'), 'w').write("""const V='s-%s';const LIB='lib-v1';const CORE=%s;
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V&&k!==LIB).map(k=>caches.delete(k)))));self.clients.claim();});
function netFirst(req,name,ms){
 const net=fetch(req,{cache:'no-cache'}).then(r=>{if(r.ok){const c=r.clone();caches.open(name).then(x=>x.put(req,c));}return r;});
 const timed=ms?Promise.race([net,new Promise((_,rej)=>setTimeout(()=>rej('slow'),ms))]):net;
 return timed.catch(()=>caches.match(req,{ignoreSearch:req.mode==='navigate'}).then(c=>c||(req.mode==='navigate'?caches.match('index.html'):undefined)).then(c=>c||net));
}
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin!==location.origin||e.request.method!=='GET')return;
 e.respondWith(u.pathname.includes('/library/')?netFirst(e.request,LIB,2500):netFirst(e.request,V,0));});
""" % (ver, json.dumps(files)))
open(os.path.join(SITE, '.nojekyll'), 'w').write('')
shutil.copy(os.path.join(ROOT, 'tools', 'site', 'privacy.html'), os.path.join(SITE, 'privacy.html'))   # the privacy policy the app stores link to
# /get: the one link ☰ › Share the app sends. An Android phone goes on to the store app's page (library/apps.json → "store";
# ?app=<id> picks the app, else the first that has one), anything else to the website; a chat app shows the same card as the site's
_stores = {k: v['store'] for k, v in json.load(open(os.path.join(SITE, 'library', 'apps.json'))).items() if isinstance(v, dict) and v.get('store')}
os.makedirs(os.path.join(SITE, 'get'), exist_ok=True)
open(os.path.join(SITE, 'get', 'index.html'), 'w').write('<!doctype html>\n<html lang="hi" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="google" content="notranslate"><title>शास्त्र · Scriptures</title>' + OG.replace('content="https://' + HOST + '/"', 'content="https://' + HOST + '/get"') +
    '<script>const S=' + json.dumps(_stores) + ',a=new URLSearchParams(location.search).get("app"),s=S[a]||Object.values(S)[0];'
    'location.replace(/Android/i.test(navigator.userAgent)&&s?s:"/");</script></head>'
    '<body style="font-family:serif;text-align:center;padding:40px 16px"><p><a href="/">शास्त्र · Scriptures</a></p>' +
    ''.join('<p><a href="' + u + '">Android</a></p>' for u in list(_stores.values())[:1]) + '</body></html>\n')
# the site's own address (GitHub Pages custom domain): apps/app.json host; DNS CNAME <host> → goyaldarwin.github.io (Cloudflare, DNS only)
open(os.path.join(SITE, 'CNAME'), 'w').write(json.load(open(os.path.join(ROOT, 'apps', 'app.json')))['host'] + '\n')
# Android: the apps that may open this site full screen (Digital Asset Links), from apps/app.json
_apps = json.load(open(os.path.join(ROOT, 'apps', 'app.json')))['apps']
os.makedirs(os.path.join(SITE, '.well-known'), exist_ok=True)
json.dump([{'relation': ['delegate_permission/common.handle_all_urls'], 'target': {'namespace': 'android_app', 'package_name': a['packageId'], 'sha256_cert_fingerprints': a['sha256']}}
           for a in _apps.values() if a.get('sha256')], open(os.path.join(SITE, '.well-known', 'assetlinks.json'), 'w'), indent=1)
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
