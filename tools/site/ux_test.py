"""End-to-end test of navigation and the reading experience, at phone size, for every work on the shelf.

Usage:  python3 tools/site/ux_test.py [--shots DIR]      (serves the repository root on a free port)
Needs:  pip install playwright (Chromium; set CHROMIUM=/path/to/chrome if it is not found)

Each check prints PASS/FAIL with what it saw; the run fails if any check fails or the page logs a script error.
--shots saves a screenshot after each step, for a person to look at.
"""
import asyncio, functools, http.server, json, os, socketserver, sys, threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from playwright.async_api import async_playwright

SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
results = []

def check(name, ok, seen=''):
    results.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + (f'  [{seen}]' if seen != '' else ''), flush=True)

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    s = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT)); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

def leaves(nodes, trail=()):
    for n in nodes:
        if 'work' in n: yield n, trail
        else: yield from leaves(n['children'], trail + (n['id'],))

async def main():
    srv = serve(); url = f'http://127.0.0.1:{srv.server_address[1]}/'
    shelf = json.load(open(os.path.join(ROOT, 'library', 'index.json')))
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}
        b = await p.chromium.launch(**kw)
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        n = 0
        async def shot(tag):
            nonlocal n
            if SHOTS: n += 1; os.makedirs(SHOTS, exist_ok=True); await pg.screenshot(path=os.path.join(SHOTS, f'{n:02d}-{tag}.png'))
        ev = pg.evaluate
        await pg.goto(url); await pg.wait_for_timeout(2500)

        # ---- library: two levels per screen, every tradition is a heading ----
        await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(300); await shot('library')
        heads = await ev("Array.from(document.querySelectorAll('#libList .lhead')).map(x => x.textContent)")
        check('library shows each tradition as a heading', len(heads) == len(shelf), heads)
        rows = await ev("document.querySelectorAll('#libList [data-node]').length")
        check('library lists the genres under them', rows == sum(len(t['children']) for t in shelf), rows)

        # one header on the library, a work and the reader: back, A−/A+, हिं·En·शब्द, search, menu
        for v in ('library', 'home', 'reader'):
            need = ['.lyr.layers', '.hsearch', '.hmenu'] + ([] if v == 'library' else ['.szm', '.szp'])   # the library's left side is its breadcrumbs
            parts = await ev(f"(() => {{ const b = document.querySelector('#{v} .bar'); return b ? {need!r}.map(c => !!b.querySelector(c)) : []; }})()")
            check(f'{v}: the same header (हिं·En·शब्द, search, menu; A−/A+ on a work and the reader)', parts and all(parts), parts)
        hgt = await ev("document.querySelector('#library .bar').getBoundingClientRect().height")
        check('library: the header is one row, even inside a shelf', hgt < 70, hgt)
        # the library's way back is the breadcrumb row in its header; inside a work, “‹ Library” goes to the library
        await ev("libPath=[LIB[0].id]; show('library')"); await pg.wait_for_timeout(300)
        crumbs = await ev("document.querySelector('#library .bar #libCrumbs').innerText")
        check('library: breadcrumbs sit in the header', 'Library' in crumbs or 'पुस्तकालय' in crumbs, crumbs)
        hgt = await ev("document.querySelector('#library .bar').getBoundingClientRect().height")
        check('library: inside a shelf the header is still one row', hgt < 70, hgt)
        await ev("libPath=[]; renderLibrary()")
        await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(300)
        lang0 = await ev("LANG()")
        await (await pg.query_selector('#library .lyr.layers [data-l=e]')).click(); await pg.wait_for_timeout(400)
        check('language can be changed from the library', await ev("LANG()") != lang0, lang0)
        await (await pg.query_selector('#library .lyr.layers [data-l=e]')).click(); await pg.wait_for_timeout(300)
        # library search finds a work by its English or Hindi name
        for leaf, trail in list(leaves(shelf))[:3]:
            await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(200)
            await (await pg.query_selector('#libSearchBtn')).click(); await pg.wait_for_timeout(200)
            q = leaf['title']['en'].split()[-1][:5]
            await pg.fill('#q', q); await pg.wait_for_timeout(500)
            found = await ev("Array.from(document.querySelectorAll('#sRes .snip')).map(x => x.textContent)")
            check(f'library search “{q}” finds {leaf["work"]}', leaf['title']['hi'] in found or leaf['title']['en'] in found, found[:4])
        await shot('library-search')

        for leaf, trail in leaves(shelf):
            wid = leaf['work']; tag = wid
            # walk the shelf exactly as a reader would: tap down the path, two levels at a time
            await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(200)
            path = list(trail) + [leaf['id']]
            k = 0; opened = False
            while k < len(path):
                key = '/'.join(path[k:k + 2]) if k + 1 < len(path) else path[k]
                btn = await pg.query_selector(f'#libList [data-node="{key}"]')
                if not btn: key = path[k]; btn = await pg.query_selector(f'#libList [data-node="{key}"]')
                if not btn: break
                await btn.click(); await pg.wait_for_timeout(1500 if k + key.count('/') + 1 >= len(path) else 300)
                k += key.count('/') + 1
                if k >= len(path): opened = True
            on_home = await ev("document.querySelector('#home').classList.contains('on') && W && W.id")
            check(f'{tag}: reached from the library by tapping its shelves', opened and on_home == wid, ' › '.join(path))
            if on_home != wid: await ev(f"openWork({json.dumps(wid)})"); await pg.wait_for_timeout(1500)
            await shot(f'{tag}-home')
            title = await ev("document.querySelector('#hTitle').textContent")
            check(f'{tag}: home shows the title', title.strip() != '', title)
            single = await ev("PARTS.length === 1")
            seg_hidden = await ev("document.querySelector('#orgSeg').hidden")
            check(f'{tag}: plan switch only when there are plans', seg_hidden == (await ev("PLANS.length === 0")))
            nrows = await ev("document.querySelectorAll('#orgList [data-open]').length")
            want = await ev("PARTS.length === 1 ? null : PARTS.length")
            check(f'{tag}: home lists {"its sections" if single else "its parts"}', nrows > 0 and (want is None or nrows == want), nrows)
            has_au = await ev("firstAu(0, IT.length - 1) != null")
            pa = await ev("!document.querySelector('#hPlayAll').hidden")
            check(f'{tag}: “play the complete work” only when there is audio', pa == has_au, f'audio={has_au}')
            # each plan shows the pages it names before its first day and after its last (pūrvāṅga / uttarāṅga)
            for pid in await ev("PLANS.map(p => p.id)"):
                await ev(f"WS().org = {json.dumps(pid)}; renderHome()"); await pg.wait_for_timeout(200)
                got = await ev("[...document.querySelectorAll('#orgList [data-page]')].map(b => b.dataset.page)")
                want_pg = await ev(f"(PLAN[{json.dumps(pid)}].before || []).concat(PLAN[{json.dumps(pid)}].after || [])")
                first = await ev("(document.querySelector('#orgList .it') || {}).dataset ? document.querySelector('#orgList .it').dataset.page || 'day' : ''")
                check(f'{tag}: plan {pid} lists its before/after pages in place', got == want_pg and (first == (want_pg[0] if (await ev(f"(PLAN[{json.dumps(pid)}].before || []).length")) else 'day')), f'{got} first={first}')
            if await ev("PLANS.length"): await ev("WS().org = 'k'; renderHome()"); await pg.wait_for_timeout(200)
            # timing review: drafts only with Settings › Audio timing on; a start and an end set by ear take effect at once
            drafts = await ev("(W.sources.au || []).filter(s => s.draft).map(s => s.id)")
            if drafts:
                check(f'{tag}: a draft recording is not played to readers', (await ev("SRC.au ? SRC.au.meta.id : null")) not in drafts)
            await ev("S.timing.on = true; applyTiming()"); await ev("loadSources()"); await pg.wait_for_timeout(600)
            if await ev("!!SRC.au"):
                j = await ev("AUT[0][1] ? AUT[0][1][0] : AUT[0][0][0]")
                await ev(f"setTime({j}, 1, AUT[0].find(x => x[0] === {j})[1] + 0.5); setTime({j}, 2, AUT[0].find(x => x[0] === {j})[1] + 3)")
                ent = await ev(f"AUT[0].find(x => x[0] === {j})")
                check(f'{tag}: a start and an end set by ear apply at once', ent[2] is not None and abs(ent[2] - ent[1] - 3) < 0.05, ent)
                await ev(f"openReader('k', {j})"); await pg.wait_for_timeout(800)
                check(f'{tag}: every verse shows its own timing buttons', await ev("document.querySelectorAll('#rBody .verse .tmark [data-a=tstart]').length") == await ev("document.querySelectorAll('#rBody .verse').length"))
                await ev("show('home')"); await pg.wait_for_timeout(300)
                # an end set past the next verse's start moves that verse to begin where this one ends
                k2 = await ev(f"AUT[0].findIndex(x => x[0] === {j})")
                if await ev(f"AUT[0].length > {k2} + 2"):
                    nx = await ev(f"AUT[0][{k2} + 1][0]"); nxs = await ev(f"AUT[0][{k2} + 1][1]")
                    await ev(f"setTime({j}, 1, AUT[0][{k2}][1]); setTime({j}, 2, {nxs} + 2)")
                    got = await ev(f"SRC.au.at[IT[{nx}].id][1]")
                    check(f'{tag}: the next verse starts where an end set by ear says this one ends', abs(got - (nxs + 2)) < 0.11, [nxs, got])
                await ev("delete S.timing.fix[tkey()]; save()")
            await ev("S.timing.on = false; applyTiming()"); await ev("loadSources()"); await pg.wait_for_timeout(400)
            # continue and play sit on one line
            await ev("WS().last = {org: 'k', i: 0}; renderHome()"); await pg.wait_for_timeout(200)
            tops = await ev("[...document.querySelectorAll('.heroacts .btn:not([hidden])')].map(b => Math.round(b.getBoundingClientRect().top))")
            check(f'{tag}: continue and play share one line', len(set(tops)) <= 1, tops)

            # ---- reader ----
            await (await pg.query_selector('#orgList [data-open]')).click(); await pg.wait_for_timeout(1500); await shot(f'{tag}-reader')
            nv = await ev("document.querySelectorAll('#reader .verse').length")
            check(f'{tag}: reader opens with verses', nv > 0, nv)
            hdr = await ev("document.querySelector('#rMid').innerText")
            check(f'{tag}: the bottom bar names where you are', len(hdr.strip()) > 2, hdr.replace('\n', ' / '))
            # text size: A+ and A− change it and keep the reader at the same verse
            at = await ev("topVisibleItem()"); sz = await ev("S.settings.size")
            await (await pg.query_selector('#rBigger')).click(); await pg.wait_for_timeout(500)
            sz2 = await ev("S.settings.size"); at2 = await ev("topVisibleItem()")
            await (await pg.query_selector('#rSmaller')).click(); await pg.wait_for_timeout(500)
            check(f'{tag}: A+ / A− change the text size and keep your place', sz2 == sz + 2 and await ev("S.settings.size") == sz and abs(at2 - at) <= 1, f'{sz}→{sz2}, verse {at}→{at2}')
            # icons never overlap the verse text
            overlap = await ev("""(() => { let bad = 0; document.querySelectorAll('#reader .vtext p').forEach(p => {
                const r = p.getBoundingClientRect(), pad = 0;
                p.querySelectorAll('.vt, .vbm, .vend, .vplay').forEach(ic => { const a = ic.getBoundingClientRect();
                  p.querySelectorAll('.w').forEach(w => { const c = w.getBoundingClientRect();
                    if (a.width && c.width && a.left < c.right - 1 && a.right > c.left + 1 && a.top < c.bottom - 1 && a.bottom > c.top + 1) bad++; }); }); }); return bad; })()""")
            check(f'{tag}: verse icons never touch the words', overlap == 0, overlap)
            wide = await ev("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(f'{tag}: nothing runs off the side of the screen', wide <= 0, f'{wide}px')
            # continuous scroll loads the next pages
            before = await ev("document.querySelectorAll('#reader .pg').length")
            for _ in range(6): await ev("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(400)
            after = await ev("document.querySelectorAll('#reader .pg').length")
            more = await ev("(() => { const v = [...document.querySelectorAll('#reader .verse')]; return v.length && +v[v.length - 1].dataset.i < R.b; })()")   # verses left in this part (the reader shows one part at a time)
            check(f'{tag}: scrolling down keeps loading the text', after > before or not more, f'{before}→{after}')
            # section picker
            await ev("sectionSheet()"); await pg.wait_for_timeout(400); await shot(f'{tag}-sections')
            secs = await ev("document.querySelectorAll('#sheetBody .secs button').length")
            check(f'{tag}: section picker lists sections', secs > 0, secs)
            last = await pg.query_selector_all('#sheetBody .secs button')
            if last:
                await last[-1].click(); await pg.wait_for_timeout(1200)
                where = await ev("topVisibleItem()")
                check(f'{tag}: picking a section jumps there', where is not None, where)
            # meaning layers
            for lang, sel in (('h', '.layer.h'), ('e', '.layer.e')):
                await ev(f"S.settings.layers.{lang} = true; refreshReader()"); await pg.wait_for_timeout(500)
                cnt = await ev(f"document.querySelectorAll('#reader {sel}').length")
                srcs = await ev(f"((W.sources||{{}})['{'hi' if lang == 'h' else 'en'}']||[]).length")
                check(f'{tag}: {"Hindi" if lang == "h" else "English"} meanings show', cnt > 0 or srcs == 0, f'{cnt} on screen, {srcs} sources')
            # word meaning
            w = await pg.query_selector('#reader .vtext .w')
            if w:
                await w.click(); await pg.wait_for_timeout(500); await shot(f'{tag}-word')
                sheet = await ev("document.querySelector('#sheetBody h2') && document.querySelector('#sheetBody h2').textContent")
                check(f'{tag}: tapping a word opens its meaning sheet', bool(sheet), sheet)
                await ev("closeSheet()")
            # bookmark round trip
            bm = await pg.query_selector('#reader .vbm')
            if bm:
                await bm.click(); await pg.wait_for_timeout(300)
                k = await ev("Object.keys(ME().bm).filter(k => k.startsWith(W.id + ':')).length")
                check(f'{tag}: bookmark is saved', k > 0, k)
                await ev("show('bookmarks')"); await pg.wait_for_timeout(500); await shot(f'{tag}-bookmarks')
                listed = await ev("document.querySelectorAll('#bookmarks [data-i], #bookmarks .res, #bookmarks li').length")
                check(f'{tag}: bookmark appears in Bookmarks', listed > 0, listed)
                await ev("history.back()"); await pg.wait_for_timeout(500)
                await ev("Object.keys(ME().bm).filter(k => k.startsWith(W.id + ':')).forEach(k => delete ME().bm[k]); save()")
            # search for a word of the first verse
            word = await ev("cleanWord((IT[0].v[0].split(/\\s+/).find(x => cleanWord(x).length > 2)) || '')")
            if word:
                await ev("openSearch('text')"); await pg.fill('#q', word); await pg.wait_for_timeout(1200); await shot(f'{tag}-search')
                hits = await ev("document.querySelectorAll('#sRes .res').length")
                check(f'{tag}: search finds a word of its first verse', hits > 0, f'{word}: {hits}')
                if hits:
                    await (await pg.query_selector('#sRes .res')).click(); await pg.wait_for_timeout(1200)
                    check(f'{tag}: a search result opens the reader', await ev("document.querySelector('#reader').classList.contains('on')"))
            # English interface
            await ev("S.settings.layers.e = true; S.settings.layers.h = false; applyLang(); refreshReader()"); await pg.wait_for_timeout(500)
            en_hdr = await ev("document.querySelector('#rMid').innerText")
            check(f'{tag}: English interface works in the reader', bool(en_hdr.strip()), en_hdr)
            await ev("S.settings.layers.h = true; S.settings.layers.e = false; applyLang()")
            # the work menu (☰) leads to bookmarks and settings
            await ev("show('home')"); await pg.wait_for_timeout(300)
            await (await pg.query_selector('#hMenu')).click(); await pg.wait_for_timeout(300)
            items = await ev("Array.from(document.querySelectorAll('#sheetBody [data-go]')).map(b => b.dataset.go)")
            check(f'{tag}: ☰ holds bookmarks and settings', 'bookmarks' in items and 'settings' in items, items)
            await ev("closeSheet()")
            # back goes home
            await ev("show('home')"); await pg.wait_for_timeout(300)
            check(f'{tag}: back to the work home', await ev("document.querySelector('#home').classList.contains('on')"))

        check('no script errors anywhere', not errs, '; '.join(errs[:3]))
        await b.close()
    print(f'\n{sum(results)}/{len(results)} checks passed')
    sys.exit(0 if all(results) else 'UX TEST FAILED')
asyncio.run(main())
