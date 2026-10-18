"""Smoke test before every push: the site starts, every work opens, the reader shows verses, no script errors.

Usage:  python3 tools/site/smoke_test.py            (serves the repository root on a free port)
Needs:  pip install playwright (Chromium; set CHROMIUM=/path/to/chrome if it is not found)
"""
import asyncio, functools, http.server, json, os, socketserver, sys, threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.async_api import async_playwright

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=ROOT)
    s = socketserver.TCPServer(('127.0.0.1', 0), h); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

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
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url); await pg.wait_for_timeout(2500)
        await pg.evaluate("typeof closeTour === 'function' && closeTour()")
        ok = True
        for wid in ids:
            await pg.evaluate(f"openWork({json.dumps(wid)})"); await pg.wait_for_timeout(1500)
            await pg.click('[data-open]'); await pg.wait_for_timeout(1500)
            n = await pg.evaluate("document.querySelectorAll('#reader .verse').length")
            print(f'{wid}: {n} verses in the reader'); ok &= n > 0
            await pg.evaluate("history.back()"); await pg.wait_for_timeout(500)
        await b.close()
    if errs: print('SCRIPT ERRORS:', *errs, sep='\n  ')
    sys.exit(0 if ok and not errs else 'SMOKE TEST FAILED')
asyncio.run(main())
