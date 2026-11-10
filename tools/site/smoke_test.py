"""Smoke test before every push: the site starts, every work opens, the reader shows verses, no script errors, and the
app looks words up by the same rule as tools/text/standard.py. A work loaded by part (tools/site/split_fixture.py) opens
in this release, with its verses' lines and its meanings in its second part, and in the previous release (origin/main's app.js, as a phone
with it cached runs it) without a script error.

Usage:  python3 tools/site/smoke_test.py            (serves the repository root on a free port)
Needs:  pip install playwright (Chromium; set CHROMIUM=/path/to/chrome if it is not found)
"""
import asyncio, functools, glob, http.server, json, os, shutil, socketserver, subprocess, sys, tempfile, threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'site')); import split_fixture
sys.path.insert(0, os.path.join(ROOT, 'tools', 'text')); import standard
sys.path.insert(0, os.path.join(ROOT, 'tools')); import jsonio
from playwright.async_api import async_playwright

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=ROOT)
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), h); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

def works(nodes):
    for n in nodes:
        if 'work' in n: yield n['work']
        else: yield from works(n['children'])

async def main():
    srv = serve(); url = f'http://127.0.0.1:{srv.server_address[1]}/'
    ids = list(works(json.load(open(os.path.join(ROOT, 'library', 'index.json')))))
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}
        b = await p.chromium.launch(**kw)
        pg = await (await b.new_context(viewport={'width': 390, 'height': 844})).new_page()
        await pg.add_init_script('window.__SALUTE_MS = 0')
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e) + ' @ ' + ' ‹ '.join(l.strip() for l in (getattr(e, 'stack', '') or '').splitlines()[1:4])))   # where in app.js
        await pg.goto(url); await pg.wait_for_timeout(2500)
        await pg.evaluate("typeof closeTour === 'function' && closeTour()")
        ok = True
        # the app's word lookup form is the same rule as tools/text/standard.py fold(), on every word of the library
        words = sorted({t for f in glob.glob(os.path.join(ROOT, 'library', '**', 'work.json'), recursive=True) for x in jsonio.read_work(f)['items'] for l in x['v'] for t in l.split()} | {'गङ्गा', 'इदम्', 'अग्ंशुश्च', 'सꣳहिता'})
        js = await pg.evaluate("ws => ws.map(fold)", words)
        bad = [(w, a, standard.fold(w)) for w, a in zip(words, js) if a != standard.fold(w)]
        print(f'word lookup form: app and standard.py agree on {len(words) - len(bad)} of {len(words)} words'); ok &= not bad
        for b_ in bad[:5]: print('  differs:', *b_)
        for wid in ids:
            # waits for what it needs to see, never a fixed time (a slow phone or runner only takes longer)
            await pg.evaluate(f"openWork({json.dumps(wid)})")
            await pg.wait_for_function(f"W && W.id === {json.dumps(wid)} && document.querySelector('#home').classList.contains('on') && !!document.querySelector('#orgList [data-open]')", timeout=30000)
            await pg.click('#orgList [data-open]')
            try: await pg.wait_for_function("document.querySelector('#reader').classList.contains('on') && document.querySelectorAll('#reader .verse').length > 0", timeout=20000)
            except Exception: pass
            n = await pg.evaluate("document.querySelectorAll('#reader .verse').length")
            print(f'{wid}: {n} verses in the reader'); ok &= n > 0
            await pg.evaluate("history.back()"); await pg.wait_for_function("!document.querySelector('#reader').classList.contains('on')", timeout=10000)
        # a work loaded by part, in this release and in the previous one
        tmp = tempfile.mkdtemp(); lib, path = split_fixture.make(tmp); srv2 = split_fixture.serve(lib, path); url2 = f'http://127.0.0.1:{srv2.server_address[1]}/'
        old = subprocess.run(['git', 'show', 'origin/main:tools/site/app.js'], cwd=ROOT, capture_output=True, text=True)
        for label, js in (('this release', None), ('the previous release', old.stdout if old.returncode == 0 else None)):
            if label != 'this release' and js is None: print('split work, previous release: origin/main is not here; skipped'); continue
            cx = await b.new_context(viewport={'width': 390, 'height': 844}); sp = await cx.new_page(); e2 = []
            sp.on('pageerror', lambda e: e2.append(str(e))); await sp.add_init_script('window.__SALUTE_MS = 0')
            if js is not None:
                def serve_js(body):   # Playwright passes the request too when the handler takes two arguments
                    async def h(route): await route.fulfill(status=200, content_type='application/javascript', body=body)
                    return h
                await sp.route('**/app/app.js*', serve_js(js))
            await sp.goto(url2); await sp.wait_for_timeout(2000)
            await sp.evaluate("(() => { S.settings.tour = 1; typeof closeTour === 'function' && closeTour(); S.settings.layers.h = true; S.settings.layers.e = true; save(); })()")
            await sp.evaluate(f"openWork({json.dumps(split_fixture.WORK)})"); await sp.wait_for_timeout(1500)
            await sp.evaluate("openReader('k', PARTS[1].a)"); await sp.wait_for_timeout(1500)
            n, m, tx = await sp.evaluate("[document.querySelectorAll('#reader .verse').length, document.querySelectorAll('#reader .layer').length, [...document.querySelectorAll('#reader .verse .vtext')].filter(x => x.textContent.trim()).length]")
            # the previous release draws the verses without failing (their lines and meanings, loaded by part, need this release)
            good = n > 0 and not e2 and (js is not None or (m > 0 and tx == n))
            print(f'split work, {label}: {n} verses ({tx} with their lines) and {m} meanings in its second part' + (f'; errors: {e2[:2]}' if e2 else '')); ok &= good
            await cx.close()
        srv2.shutdown(); srv2.server_close(); shutil.rmtree(tmp, ignore_errors=True)
        await b.close()
    if errs: print('SCRIPT ERRORS:', *errs, sep='\n  ')
    sys.exit(0 if ok and not errs else 'SMOKE TEST FAILED')
asyncio.run(main())
