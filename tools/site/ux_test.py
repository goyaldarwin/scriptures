"""End-to-end test of navigation and the reading experience, at phone size, for every work on the shelf.

Usage:  python3 tools/site/ux_test.py [--shots DIR]      (serves the repository root on a free port)
Needs:  pip install playwright (Chromium; set CHROMIUM=/path/to/chrome if it is not found)

Each check prints PASS/FAIL with what it saw; the run fails if any check fails or the page logs a script error.
--shots saves a screenshot after each step, for a person to look at.
"""
import asyncio, functools, http.server, json, os, random, shutil, socketserver, subprocess, sys, tempfile, threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'audio')); import order as ORDER   # the order rule, shared with make_timings.py
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
        await pg.add_init_script('window.__SALUTE_MS = 0')   # the 1.5 s greeting is tested on its own
        pg.on('pageerror', lambda e: errs.append(str(e)))
        n = 0
        async def shot(tag):
            nonlocal n
            if SHOTS: n += 1; os.makedirs(SHOTS, exist_ok=True); await pg.screenshot(path=os.path.join(SHOTS, f'{n:02d}-{tag}.png'))
        ev = pg.evaluate
        await pg.goto(url); await pg.wait_for_timeout(2500)
        # first run: an interactive tour inside the Sundarakāṇḍa — each step moves on only when the reader has done it
        check('first run: the tour shows', await ev("!document.querySelector('#tour').hidden"))
        check('the page asks browsers never to offer translating it', await ev("document.documentElement.getAttribute('translate') === 'no' && !!document.querySelector('meta[name=google][content=notranslate]')"))
        await (await pg.query_selector('#tourNext')).click(); await pg.wait_for_timeout(2500)
        check('tour: opens the Sundarakāṇḍa and lights the first step', await ev("W && W.id") == 'sundarkand' and await ev("!document.querySelector('#coach').hidden && TOUR && TOUR.k === 0"))
        check('tour: the first step points at the Sundarakāṇḍa itself, not the opening prayers', await ev("IT[+tourSteps()[0].t().dataset.open].id") == 'sundar.0.shloka1', await ev("IT[+tourSteps()[0].t().dataset.open].id"))
        await ev("tourSteps()[0].t().click()"); await pg.wait_for_timeout(1800)
        check('tour: opening the text moves to the word step', await ev("TOUR && TOUR.k") == 1, await ev("TOUR && TOUR.k"))
        check('tour: the text opens at the Sundarakāṇḍa', await ev("IT[R.a].id") == 'sundar.0.shloka1', await ev("IT[R.a].id"))
        await ev("tourSteps()[1].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: tapping a word opens its meaning and moves on', await ev("TOUR && TOUR.k") == 2 and await ev("document.querySelector('#sheet').classList.contains('on')"))
        await ev("document.querySelector('#cbBack').click()"); await pg.wait_for_timeout(1200)
        check('tour: ‹ Back from “close the drawer” closes it and waits on “tap a word”', await ev("TOUR && TOUR.k") == 1 and not await ev("document.querySelector('#sheet').classList.contains('on')"), await ev("TOUR && TOUR.k"))
        await ev("tourSteps()[1].t().click()"); await pg.wait_for_timeout(1200)
        sz0 = await ev("S.settings.size"); await ev("S.settings.size = 34; applyTheme()")   # already at the largest when the A+ step comes
        await ev("closeSheet()"); await pg.wait_for_timeout(1200)
        check('tour: closing the drawer moves on', await ev("TOUR && TOUR.k") == 3)
        await pg.wait_for_timeout(600); stay = await ev("TOUR && TOUR.k")
        await ev("tourSteps()[3].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: A+ at the largest size waits for the tap, then moves on', stay == 3 and await ev("TOUR && TOUR.k") == 4, [stay, await ev("TOUR && TOUR.k")])
        await ev(f"S.settings.size = {sz0}; applyTheme()"); await ev("document.querySelector('#cbBack').click()"); await pg.wait_for_timeout(1200)
        blocked = await ev("(() => { const b = document.querySelector('#rLayers [data-l=w]'); const w0 = S.settings.layers.w; b.click(); return S.settings.layers.w === w0; })()")
        check('tour: taps outside the current step do nothing', blocked)
        check('tour: the first steps have ‹ Back, the first does not', await ev("!document.querySelector('#cbBack').hidden"))
        await ev("tourSteps()[3].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: A+ moves on to A−', await ev("TOUR && TOUR.k") == 4 and await ev("tourSteps()[4].t() === document.querySelector('#reader .szm')"))
        await ev("document.querySelector('#cbBack').click()"); await pg.wait_for_timeout(1200)
        check('tour: ‹ Back returns to the step before (A+)', await ev("TOUR && TOUR.k") == 3, await ev("TOUR && TOUR.k"))
        await ev("tourSteps()[3].t().click()"); await pg.wait_for_timeout(1200)
        await ev("tourSteps()[4].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: A− makes the text smaller and moves on', await ev("TOUR && TOUR.k") == 5)
        await ev("tourSteps()[5].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: switching a meaning moves on', await ev("TOUR && TOUR.k") == 6)
        await ev("tourSteps()[6].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: recitation mode moves on', await ev("TOUR && TOUR.k") == 7 and await ev("S.settings.recite"))
        await ev("document.querySelector('#cbBack').click()"); await pg.wait_for_timeout(1200)
        check('tour: ‹ Back to recitation mode turns it off so it can be tried again', await ev("TOUR && TOUR.k") == 6 and not await ev("S.settings.recite"))
        await ev("tourSteps()[6].t().click()"); await pg.wait_for_timeout(1200)
        await ev("(() => { const b = tourSteps()[7].t(); const i = +b.closest('.verse').dataset.i; ME().bm[KEY(IT[i].id)] = 1; save(); rerenderItem(i); })()"); await pg.wait_for_timeout(300)   # already bookmarked
        await ev("tourSteps()[7].t().click()"); await pg.wait_for_timeout(700)
        k_off = await ev("TOUR && TOUR.k")
        await ev("tourSteps()[7].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: a verse already bookmarked — taken off and put back — still moves the tour on', k_off == 7 and await ev("TOUR && TOUR.k") == 8, [k_off, await ev("TOUR && TOUR.k")])
        await ev("for (const k in ME().bm) delete ME().bm[k]; save()")
        await ev("tourSteps()[8].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: while the verse plays, the tour waits in the reader', await ev("TOUR && TOUR.waiting && CURVIEW === 'reader' && document.querySelector('#coach').hidden"))
        await pg.wait_for_timeout(5600)   # the verse plays for 5 seconds
        check('tour: after 5 s the library, with the parting message in the light card, the meanings back', await ev("!TOUR && !PL.on && CURVIEW === 'library' && libPath.length === 0 && !S.settings.recite && /Tour complete|परिचय पूरा/.test(document.querySelector('#toast').textContent) && document.querySelector('#toast').classList.contains('act')"))
        await ev("setSize(-2)")
        check('the tour is remembered', await ev("S.settings.tour === 1"))
        await ev("S.work = null; save()")
        await pg.reload(); await pg.wait_for_timeout(2000)
        check('the tour is not shown again', await ev("document.querySelector('#tour').hidden"))
        # the drawer closes when dragged down from its handle
        await ev("openSheet('<p>test</p>')"); await pg.wait_for_timeout(300)
        await ev("""(() => { const sh = document.querySelector('#sheet'), g = sh.querySelector('.grab'), r = g.getBoundingClientRect(), x = r.left + 5, y = r.top + 2;
          const t = (yy) => new Touch({identifier: 1, target: g, clientX: x, clientY: yy});
          g.dispatchEvent(new TouchEvent('touchstart', {bubbles: true, touches: [t(y)]}));
          g.dispatchEvent(new TouchEvent('touchmove', {bubbles: true, touches: [t(y + 150)]}));
          g.dispatchEvent(new TouchEvent('touchend', {bubbles: true, touches: []})); })()"""); await pg.wait_for_timeout(300)
        check('the drawer closes when dragged down', not await ev("document.querySelector('#sheet').classList.contains('on')"))
        # the opening screen greets each work with its own salutation (library/index.json "salute"; default ॐ श्री परमात्मने नमः)
        for wid, want in (('manas', '॥ जय श्रीराम ॥'), ('sukhmani-sahib', 'ੴ'), ('ramraksha', '॥ ॐ श्री परमात्मने नमः ॥')):
            got = await ev(f"(async () => {{ const p = openWork({json.dumps(wid)}); await new Promise(r => setTimeout(r, 0)); const t = document.querySelector('#loading').textContent; await p; return [saluteOf({json.dumps(wid)}), t]; }})()")
            check(f'opening {wid} from the library greets it', got == [want, want], got)
        # no greeting when the app starts, on a refresh, or on a quiet open
        pg2 = await ctx.new_page(); await pg2.add_init_script("window.__SALUTE_MS = undefined")
        await pg2.goto(url + '?w=sukhmani-sahib'); await pg2.wait_for_timeout(200)
        t1 = await pg2.evaluate("document.querySelector('#loading').textContent")
        await pg2.wait_for_function("document.querySelector('#loading').hidden", timeout=10000); await pg2.reload(); await pg2.wait_for_timeout(200)
        t2 = await pg2.evaluate("document.querySelector('#loading').textContent")
        check('no greeting when the app starts or is refreshed', t1 == '' and t2 == '', [t1, t2])
        # stepping into a work from the library: the greeting stays 1.5 s even when loading is quicker
        await pg2.wait_for_function("document.querySelector('#loading').hidden", timeout=10000)
        shown = await pg2.evaluate("(async () => { W = null; const t0 = performance.now(); await openWork('ramraksha'); return performance.now() - t0; })()")
        check('the greeting stays about 1.5 s', shown >= 1450, round(shown)); await pg2.close()
        # a store app shows only its shelves (?app=<id>, library/apps.json)
        apps = json.load(open(os.path.join(ROOT, 'library', 'apps.json')))
        for aid, a in apps.items():
            if aid.startswith('_'): continue
            await pg.goto(url + '?app=' + aid); await pg.wait_for_timeout(2000)
            got = await ev("(() => { const r = []; (function w(ns, at){ ns.forEach(n => n.work ? r.push(at.concat(n.id).join('/')) : w(n.children || [], at.concat(n.id))); })(LIB, []); return r; })()")
            ok = got and all(any(g == s_ or g.startswith(s_ + '/') for s_ in a['shelves']) for g in got)
            check(f'app {aid}: only its shelves', ok, got)
        await pg.goto(url); await pg.wait_for_timeout(2000)

        # ---- library: two levels per screen, every tradition is a heading ----
        await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(300); await shot('library')
        heads = await ev("Array.from(document.querySelectorAll('#libList .lhead')).map(x => x.textContent)")
        check('library shows each tradition as a heading', len(heads) == len(shelf), heads)
        rows = await ev("document.querySelectorAll('#libList button.it[data-node]').length")   # not the '+N' chip of a shelf with more works
        check('library lists the genres under them', rows == sum(len(t['children']) for t in shelf), rows)
        # each shelf names its works; tapping one opens it straight away
        chip = await ev("(() => { const b = document.querySelector('#libList [data-open-work]'); return b ? b.dataset.openWork : null; })()")
        check('library: a shelf lists its works by name', bool(chip), chip)
        if chip:
            await (await pg.query_selector('#libList [data-open-work]')).click(); await pg.wait_for_timeout(1500)
            check('library: tapping a work on a shelf opens it', await ev("document.querySelector('#home').classList.contains('on') && W && W.id") == chip)
            await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(300)

        # one header on the library, a work and the reader: back, A−/A+, हिं·En·शब्द, search, menu
        for v in ('library', 'home', 'reader'):
            need = ['.lyr.layers' if v == 'reader' else '.lyr.uilang', '.hsearch', '.hmenu'] + ([] if v == 'library' else ['.szm', '.szp'])   # the library's left side is its breadcrumbs
            parts = await ev(f"(() => {{ const b = document.querySelector('#{v} .bar'); return b ? {need!r}.map(c => !!b.querySelector(c)) : []; }})()")
            check(f'{v}: the same header (हिं·En — with शब्द in the reader —, search, menu; A−/A+ on a work and the reader)', parts and all(parts), parts)
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
        other = 'hi' if lang0 == 'en' else 'en'
        await (await pg.query_selector(f'#library .lyr.uilang [data-u={other}]')).click(); await pg.wait_for_timeout(400)
        check('language can be changed from the library (हिं · En, one choice)', await ev("LANG()") == other and await ev("document.querySelector('#libTitle').textContent") in ('पुस्तकालय', 'Library') and not await ev("!!document.querySelector('#library .lyr [data-l=w]')"), lang0)
        check('हिं · En on the library also chooses the meaning', await ev("[S.settings.layers.h, S.settings.layers.e]") == [other == 'hi', other == 'en'])
        await (await pg.query_selector(f'#library .lyr.uilang [data-u={lang0}]')).click(); await pg.wait_for_timeout(300)
        await ev("S.settings.layers.h = false; save()")
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
            # timing review: drafts only with ☰ › More settings › Audio timing on; a start and an end set by ear take effect at once
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
                # after "Ends now", the next verse is lit at once (review mode), so its start can be marked; the bar moves
                a0 = await ev("AUT[0][1] ? AUT[0][1] : AUT[0][0]")
                if await ev("AUT[0].length > 3"):
                    v1, s1 = await ev("[AUT[0][1][0], AUT[0][1][1]]"); v2 = await ev("AUT[0][2][0]"); s2 = await ev("AUT[0][2][1]")
                    if s2 - s1 > 2:
                        await ev(f"PL.on = true; PL.t = 0; PL.end = null; ytOK = true; ytInfo.t = {s1} + 1; setTime({v1}, 2, {s1} + 0.5); setTime({v2}, 1, {s2})")   # the end gives v2 its start; put v2 back at its own, later start
                        check(f'{tag}: after an end is set, the next verse is lit at once', await ev("PL.cur") == v2, [await ev("PL.cur"), v2])
                        check(f'{tag}: the progress bar moves while playing', (await ev("document.querySelector('#pProg').style.width")) not in ('', '0%'))
                        await ev("S.timing.on = false; PL.cur = -1; tick()")
                        check(f'{tag}: outside review mode too, a verse whose end has passed hands the light to the next verse', await ev("PL.cur") == v2, [await ev("PL.cur"), v2])
                        await ev(f"ytInfo.t = {s1} + 0.2; PL.cur = -1; tick()")
                        check(f'{tag}: outside review mode, before the end the verse itself is lit', await ev("PL.cur") == v1, [await ev("PL.cur"), v1])
                        await ev("S.timing.on = true; PL.on = false; ytOK = false")
                # guessed starts after a verse you place later than guessed move with it (in order, after its end)
                g = await ev("""(() => { const a = AUT[0]; for (let k = 0; k + 3 < a.length; k++){ const ids = [0,1,2,3].map(d => IT[a[k + d][0]].id); if (ids.every(x => SRC.au.guessSet.has(x))) return k; } return -1; })()""")
                if g >= 0:
                    await ev("S.timing.fix[tkey()] = {}; save(); buildAudio()")
                    vi, s0, s2 = await ev(f"[AUT[0][{g}][0], AUT[0][{g}][1], AUT[0][{g} + 2][1]]")
                    await ev(f"setTime({vi}, 1, {s0}); setTime({vi}, 2, {s2} + 5)")
                    nxt = await ev(f"[1, 2, 3].map(d => AUT[0][{g} + d][1])")
                    check(f'{tag}: guessed starts after your end follow it, in order', nxt[0] >= s2 + 5 - 0.05 and nxt[0] < nxt[1] < nxt[2], [s2 + 5, nxt])
                    # the light waits for you: it stays on the verse you marked while the next start is only a guess
                    await ev("S.timing.fix[tkey()] = {}; save(); buildAudio()")
                    va, sa = await ev(f"[AUT[0][{g}][0], AUT[0][{g}][1]]"); vb, sb = await ev(f"[AUT[0][{g} + 1][0], AUT[0][{g} + 1][1]]")
                    await ev(f"PL.on = true; PL.t = 0; PL.end = null; ytOK = true; ytInfo.t = {sa} + 0.2; setTime({va}, 1, {sa})")
                    await ev(f"ytInfo.t = {sb} + 1; tick()")
                    held = await ev("PL.cur")
                    await ev(f"setTime({vb}, 1, {sb} + 0.8)")
                    check(f'{tag}: the light waits on your verse past a guessed start, and moves when you mark the next', held == va and await ev("PL.cur") == vb, [held, va, await ev("PL.cur"), vb])
                    await ev("PL.on = false; ytOK = false")
                    await ev("delete S.timing.fix[tkey()]; save(); buildAudio()")
                # a helper's file: saved from the marks, opened by the owner as marks "from <helper>" that are not sent until checked
                await ev("S.timing.fix[tkey()] = {}; S.timing.from = {}; save(); buildAudio()")
                await ev(f"setTime({j}, 1, AUT[0].find(x => x[0] === {j})[1] + 0.7)")
                doc = await ev("timingDoc('Asha')")
                await ev("delete S.timing.fix[tkey()]; delete S.timing.sent[tkey()]; save(); buildAudio()")
                await ev("importTiming(JSON.parse(JSON.stringify(Object.assign({}, " + json.dumps(doc) + ", {path: 'nowhere'}))))"); await pg.wait_for_timeout(300)
                check(f'{tag}: a helper file for another work is refused', not await ev("Object.keys(myStarts()).length"))
                await ev("importTiming(" + json.dumps(doc) + ")"); await pg.wait_for_timeout(500)
                await (await pg.query_selector('#tiAll')).click(); await pg.wait_for_timeout(300)
                jid = await ev(f"IT[{j}].id")
                check(f'{tag}: a helper file loads as marks to check, not sent', await ev(f"fromOf({json.dumps(jid)})") == 'Asha' and not await ev("Object.keys(pendingStarts()).length") and 'data-a="tok"' in await ev(f"markBar({j})"), await ev("pendingStarts()"))
                await ev(f"unfrom({json.dumps(jid)}); save()")
                check(f'{tag}: a checked helper mark is sent with yours', jid in await ev("pendingStarts()"))
                await ev("delete S.timing.fix[tkey()]; S.timing.from = {}; save()")
                # a single verse that has ended offers “Continue ▶”, which goes on from the next verse, like “Play all”
                if await ev("AUT[0].length > 3"):
                    v1 = await ev("AUT[0][1][0]"); v2 = await ev("firstAu(AUT[0][1][0] + 1, IT.length - 1)")
                    await ev(f"S.timing.on = false; PL.on = true; PL.t = 0; PL.end = {v1}; PL.whole = false; PL.endMsg = ''; ytOK = true; ytInfo.t = AUT[0][2][1] + 0.5; tick()")
                    shown = await ev("!!document.querySelector('#toast .tact')")
                    check(f'{tag}: a played verse that ends offers Continue', shown and not await ev("PL.on"))
                    if shown:
                        await ev("document.querySelector('#toast .tact').click()"); await pg.wait_for_timeout(300)
                        check(f'{tag}: Continue plays on from the next verse to the end', await ev("PL.on && PL.end == null") and await ev("PL.cur") == v2, [await ev("PL.cur"), v2])
                    await ev("stopAudio(); ytOK = false; S.timing.on = true; show('home')"); await pg.wait_for_timeout(300)
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
            # the verse type is a heading shown only where the type changes (never twice in a row for the same type)
            dup = await ev("""(() => { const els = [...document.querySelectorAll('#reader .pg > .vtype, #reader .pg > .verse')]; let bad = 0, last = null, prevHead = false;
              els.forEach(e => { if (e.classList.contains('vtype')){ if (prevHead) bad++; prevHead = true; } else { const y = IT[+e.dataset.i].y; if (!prevHead && last != null && y !== last && TYPEN[y]) bad++; last = y; prevHead = false; } }); return bad; })()""")
            check(f'{tag}: the verse type heads each run of one type, once', dup == 0, dup)
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
                # a work with a third meaning language shows a chosen pair: choose one with this language
                await ev(f"S.settings.layers.{lang} = true; {{ const k = '{'hi' if lang == 'h' else 'en'}', o = pairOptions().find(p => p.includes(k)); if (workKinds().length > 2 && o) S.settings.pair = o.join(','); }} syncLayers(); refreshReader()"); await pg.wait_for_timeout(500)
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
            await ev("S.settings.ui = 'en'; S.settings.layers.e = true; S.settings.layers.h = false; applyLang(); refreshReader()"); await pg.wait_for_timeout(500)
            en_hdr = await ev("document.querySelector('#rMid').innerText")
            check(f'{tag}: English interface works in the reader', bool(en_hdr.strip()), en_hdr)
            # recitation mode is the fourth button of the reader's capsule: it hides the meanings; a meaning turned on ends it
            await ev("S.settings.recite = false; S.settings.layers.h = true; S.settings.layers.e = true; if (workKinds().length > 2) S.settings.pair = 'pa,hi'; save(); applyRecite(); syncLayers(); refreshReader()")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(400)
            ok1 = await ev("S.settings.recite && !S.settings.layers.h && !S.settings.layers.e && !S.settings.layers.w && document.body.classList.contains('recite') && document.querySelector('#rLayers [data-l=r]').classList.contains('on')")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(400)
            ok2 = await ev("!S.settings.recite && S.settings.layers.h && S.settings.layers.e")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(300)
            await (await pg.query_selector('#rLayers [data-l=h]')).click(); await pg.wait_for_timeout(300)
            ok3 = await ev("!S.settings.recite && S.settings.layers.h && !document.body.classList.contains('recite')")
            check(f'{tag}: recitation mode from the capsule hides meanings and restores them; a meaning ends it', ok1 and ok2 and ok3, [ok1, ok2, ok3])
            await ev("delete S.settings.pair; save(); syncLayers()")
            wide2 = await ev("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(f'{tag}: the reader header still fits', wide2 <= 0, wide2)
            # English app, Hindi meaning only inside the work: the reader's words are Hindi; back on the work page, English
            await ev("S.settings.ui = 'en'; S.settings.layers.e = false; S.settings.layers.h = true; applyLang(); refreshReader()"); await pg.wait_for_timeout(400)
            check(f'{tag}: inside the work the words follow the Hindi meaning', await ev("LANG()") == 'hi')
            await ev("(document.querySelector('#rLayers [data-l=e]') || {click(){ S.settings.layers.e = true; S.settings.ui = 'en'; }}).click()"); await pg.wait_for_timeout(300)   # English meaning on → the app is English, in the work page too
            await ev("show('home')"); await pg.wait_for_timeout(200)
            check(f'{tag}: a meaning chosen inside the work sets the app language (both on → English)', await ev("[S.settings.ui, LANG()]") == ['en', 'en'])
            await ev("document.querySelector('#home .lyr.uilang [data-u=hi]').click()"); await pg.wait_for_timeout(300)
            check(f'{tag}: हिं on the work page → Hindi meaning only', await ev("[S.settings.ui, S.settings.layers.h, S.settings.layers.e]") == ['hi', True, False])
            await ev("S.settings.ui = 'en'; S.settings.layers.e = true; S.settings.layers.h = false; applyLang(); syncLayers()")
            await ev("show('reader')"); await pg.wait_for_timeout(200)
            await ev("S.settings.ui = 'hi'; S.settings.layers.h = true; S.settings.layers.e = false; applyLang()")
            # the work menu (☰) leads to bookmarks and settings
            await ev("show('home')"); await pg.wait_for_timeout(300)
            await (await pg.query_selector('#hMenu')).click(); await pg.wait_for_timeout(300)
            items = await ev("Array.from(document.querySelectorAll('#sheetBody [data-m], #sheetBody [data-tour], #sheetBody #mth, #sheetBody #mtm')).map(b => b.dataset.m || (b.dataset.tour != null ? 'tour' : b.id === 'mtm' ? 'timing' : 'dark-theme'))")
            check(f'{tag}: ☰ holds Bookmarks, Dark theme, Share the app, Take the tour and More settings — nothing else', items == ['bm', 'dark-theme', 'share', 'tour', 'set'] and not await ev("!!document.querySelector('#sheetBody [data-rate], #sheetBody [data-m=sec], #sheetBody #mtr')"), items)
            await ev("closeSheet()")
            # back goes home
            await ev("show('home')"); await pg.wait_for_timeout(300)
            check(f'{tag}: back to the work home', await ev("document.querySelector('#home').classList.contains('on')"))

        # a place saved before the Sundarakāṇḍa's opening prayers were added (an item position, no id) still opens the same verse
        old = await ev("""(async () => { await openWork('sundarkand', true); const old = W.items.findIndex(x => x.id === 'sundar.12.cau3') - W.prepended;
            S.w.sundarkand.last = {org: 'k', i: old}; S.w.sundarkand.pos = {k: old}; W = null; await openWork('sundarkand', true); return [W.prepended, S.w.sundarkand.last.id, IT[S.w.sundarkand.last.i].id, S.w.sundarkand.pos.k === S.w.sundarkand.last.i]; })()""")
        check('an old saved place moves forward past the opening prayers, once, and keeps its verse id', old[0] == 5 and old[1] == old[2] == 'sundar.12.cau3' and old[3], old)
        again = await ev("(async () => { W = null; await openWork('sundarkand', true); return IT[S.w.sundarkand.last.i].id; })()")
        check('reopening does not move it again', again == 'sundar.12.cau3', again)
        # one reader per device: several readers (from an older phone or file) are joined, nothing dropped
        joined = await ev("""(() => { const a = newProfile('A'), b = newProfile('B'); a.notes['x:1'] = [{t: 'one', ts: 1}]; b.notes['x:1'] = [{t: 'two', ts: 2}]; b.bm['x:2'] = 5;
            const keep = S; S = {profiles: [a, b], active: b.id, show: [a.id], settings: {}, v: 3}; oneReader(); const r = [S.profiles.length, S.profiles[0].notes['x:1'].length, !!S.profiles[0].bm['x:2'], S.show.length]; S = keep; return r; })()""")
        check('several readers are joined into one, keeping every note and bookmark', joined == [1, 2, True, 1], joined)
        await ev("show('settings')"); await pg.wait_for_timeout(500)
        st = await ev("document.querySelector('#setBody').innerText")
        bmf = await ev("(async () => { show('bookmarks'); await new Promise(r => setTimeout(r, 300)); return [!!document.querySelector('#bmBody #exp'), !!document.querySelector('#bmBody #imp')]; })()")
        check('Bookmarks & notes: Save my file / Open a file live there', bmf == [True, True], bmf)
        await ev("show('settings')"); await pg.wait_for_timeout(300); st = await ev("document.querySelector('#setBody').innerText")
        check('More settings: only transliteration, sources, audio timing and privacy — no my file, meanings, text size, language, speed or screen switch', ('Sources' in st or 'स्रोत' in st) and ('Audio timing' in st or 'ऑडियोका समय' in st) and not ('My file' in st or 'मेरी फ़ाइल' in st) and not await ev("!!document.querySelector('#setBody #exp')") and ('Transliteration' in st or 'लिप्यन्तरण' in st) and not await ev("!!document.querySelector('#setBody #sh, #setBody #ssz, #setBody #sui, #setBody #sth, #setBody [data-rate], #setBody #swk')") and 'Speed' not in st, st[:80])
        await ev("show('library')"); await pg.wait_for_timeout(500)
        s0 = await ev("S.settings.size"); await ev("document.querySelector('#library .szp').click()"); s1 = await ev("S.settings.size")
        check('library: A+ in its header changes the text size', s1 == s0 + 2, [s0, s1])
        await ev("document.querySelector('#library .szm').click()")
        fits = await ev("(() => { const b = document.querySelector('#library .bar .wrap'); return b.scrollWidth <= b.clientWidth + 1; })()")
        check('library: the header still fits a phone', fits)
        # ▶ after a seek: an old time reported by the player does not light the previous verse
        guard = await ev("(() => { PL.seekT = null; seekGuard(100); ytInfo.t = 40; const a = playTime(); ytInfo.t = 100.2; const b = playTime(); ytInfo.t = 99; const c = playTime(); return [a, b, c]; })()")
        check('a stale time right after a seek is held at the asked-for start', guard == [100, 100.2, 99], guard)
        # a refresh keeps you on the same page
        await ev("show('library'); libPath = [LIB[0].id]; renderLibrary()"); await pg.reload(); await pg.wait_for_timeout(2500)
        r1 = await ev("[CURVIEW, libPath.join('/')]")
        check('refresh on a library shelf stays on that shelf', r1[0] == 'library' and r1[1] != '', r1)
        await ev("show('settings')"); await pg.reload(); await pg.wait_for_timeout(2500)
        r2 = await ev("CURVIEW"); await pg.go_back(); await pg.wait_for_timeout(1200); r2b = await ev("CURVIEW")
        check('refresh on Settings stays on Settings, and Back still works', r2 == 'settings' and r2b == 'library', [r2, r2b])
        await ev("(async () => { await openWork('sundarkand', true); show('home'); openReader('k', ID['sundar.12.cau3']); savePos(ID['sundar.12.cau3']); })()"); await pg.wait_for_timeout(1500); await pg.reload(); await pg.wait_for_timeout(3000)
        r3 = await ev("[CURVIEW, W && W.id, document.getElementById('v' + ID['sundar.12.cau3']) ? 1 : 0]")
        check('refresh in the reader reopens the same work and verse', r3 == ['reader', 'sundarkand', 1], r3)
        # Back retraces exactly: library › shelf › shelf › work, then back to the shelf, not another work
        await ev("libPath = []; show('library')"); await pg.wait_for_timeout(400)
        trail = await ev("""(() => { let out = null; (function walk(ns, t){ ns.forEach(n => { if (n.work === 'shri-rudram') out = t; else if (n.children) walk(n.children, t.concat([n.id])); }); })(LIB, []); return out; })()""")
        for k in range(1, len(trail) + 1):   # the way a reader goes down the shelves: each step is a history entry
            await ev(f"libPath = {json.dumps(trail[:k])}; history.pushState(snap('library'), ''); renderLibrary()")
        await ev("openWork('shri-rudram')"); await pg.wait_for_timeout(2000)
        await pg.go_back(); await pg.wait_for_timeout(1500)
        back1 = await ev("[CURVIEW, libPath.join('/')]")
        check('Back from a work opened on a shelf returns to that shelf', back1 == ['library', '/'.join(trail)], [trail, back1])
        await pg.go_back(); await pg.wait_for_timeout(800)
        back2 = await ev("[CURVIEW, libPath.join('/')]")
        check('Back again goes up one shelf', back2 == ['library', '/'.join(trail[:-1])], back2)
        await ev("(async () => { await openWork('shirdi-sai-dhoop-aarti'); })()"); await pg.wait_for_timeout(1500)
        await ev("document.querySelector('#hLib').click()"); await pg.wait_for_timeout(600)
        lib = await ev("[CURVIEW, libPath.length]")
        check('“‹ Library” on a work opens the library itself', lib == ['library', 0], lib)
        gap = await ev("(async () => { await openWork('manas', true); show('bookmarks'); await new Promise(r => setTimeout(r, 300)); const b = [...document.querySelectorAll('#bmBody .acts .btn')].slice(0, 2).map(x => x.getBoundingClientRect()); return b.length == 2 ? Math.round(b[1].left - b[0].right) : -1; })()")
        check('the file buttons stand apart', gap >= 8, gap)
        foot = await ev("(async () => { await openWork('sundarkand', true); show('home'); openReader('k', ID['kishkindha.29.do29']); await new Promise(r => setTimeout(r, 600)); return document.querySelector('#rMid small').textContent; })()")
        check('the reader footer names only the part, not the topic', foot == await ev("KNAME(R.n)"), foot)
        subs = await ev("""(async () => { const r = {}; for (const id of ['manas', 'sundarkand', 'ramraksha']){ await openWork(id, true); S.settings.ui = 'en'; applyLang(); show('home'); r[id] = document.querySelector('#hSub').textContent; } return r; })()""")
        check('under the title: the author and parent text, no publisher', subs == {'manas': 'Gosvāmī Tulasīdāsa', 'sundarkand': 'Gosvāmī Tulasīdāsa · Śrī Rāmacaritamānasa', 'ramraksha': 'Budha Kauśika Ṛṣi'}, subs)
        pk = await ev("""(async () => { await openWork('manas', true); show('home'); openReader('k', 0); await new Promise(r => setTimeout(r, 500)); sectionSheet();
            const a0 = R.a; document.querySelector('#sheetBody [data-pick="1"]').click(); await new Promise(r => setTimeout(r, 300));
            const stillOpen = document.querySelector('#sheet').classList.contains('on'), same = R.a === a0, first = +document.querySelector('#sheetBody .secs [data-to]').dataset.to;
            document.querySelector('#sheetBody .secs [data-to]').click(); await new Promise(r => setTimeout(r, 600));
            return [stillOpen, same, first === PARTS[1].a, R.n === 1, document.querySelector('#sheet').classList.contains('on')]; })()""")
        check('section picker: a kāṇḍa only shows its sections; a section opens it', pk == [True, True, True, True, False], pk)
        # The timing tests practise on the Śrī Rudram's recording as if nothing had been set by ear yet (every verse estimated,
        # none the owner's), so they do not depend on how far the owner has marked it: each first clears, in memory only, the
        # published marks, ends and checks, and rebuilds the times (inlined: the page reloads between tests).
        # timing: "Ends now" on a verse whose estimated start lies after now takes the previous verse's set end as its start
        te = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); }
            const a = AUT[0]; let j = a.findIndex((x, n) => n > 0 && toCheck(x[0]) && !toCheck(a[n - 1][0]) && x[1] - a[n - 1][1] > 3); if (j < 0) j = 5;
            const i = a[j][0], p = a[j - 1][0], ps = a[j - 1][1], keep = JSON.stringify(S.timing.fix[tkey()] || {});
            openReader('k', i); await new Promise(r => setTimeout(r, 500));
            setTime(p, 2, ps + 1); const end = ps + 2; setTime(i, 2, end);
            const got = SRC.au.at[IT[i].id]; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources();
            return [Math.round(got[1] * 10) / 10 === Math.round((ps + 1) * 10) / 10, Math.round(got[2] * 10) / 10 === Math.round(end * 10) / 10]; })()""")
        check('timing: Ends now on a late estimate starts it at the previous verse\'s end', te == [True, True], te)
        # …but a start set by ear and already sent (published "own") is never moved by that rule: the end is refused instead
        so = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shirdi-sai-dhoop-aarti', true); await loadSources(); show('home');
            const A = SRC.au, ids = [...A.ownSet]; let i = -1, p = -1;
            for (const id of ids){ const q = ID[id], a = AUT[A.at[id][0]], j = a.findIndex(x => x[0] === q); if (j > 0 && a[j - 1][2] != null && a[j][1] - a[j - 1][2] > 1){ i = q; p = a[j - 1][0]; break; } }
            if (i < 0){ const id = ids[5], q = ID[id], a = AUT[A.at[id][0]], j = a.findIndex(x => x[0] === q); i = q; p = a[j - 1][0]; const keep0 = JSON.stringify(S.timing.fix[tkey()] || {}); setTime(p, 2, A.at[IT[p].id][1] + 0.5); }
            openReader('k', i); await new Promise(r => setTimeout(r, 500));
            const s0 = A.at[IT[i].id][1], pe = A.at[IT[p].id][2], r = setTime(i, 2, Math.min(s0 - 0.2, (pe != null ? pe : s0 - 1) + 0.3)), s1 = A.at[IT[i].id][1];
            S.timing.fix[tkey()] = {}; S.timing.on = false; save(); applyTiming(); await loadSources(); return [r === false, s1 === s0]; })()""")
        check('timing: a sent start is never moved by a late "Ends now"', so == [True, True], so)
        # a timing mark never scrolls the page while the lit verse is on screen
        ns = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); }
            const a = AUT[0], i = a[8][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); PL.on = true; PL.t = 0; setCur(i); await new Promise(r => setTimeout(r, 900));
            const y0 = scrollY; ytInfo.t = a[8][1] + 1; setTime(i, 2, a[8][1] + 1); await new Promise(r => setTimeout(r, 900)); const y1 = scrollY;
            PL.on = false; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [y0, y1]; })()""")
        check('timing: marking a verse does not move the page', abs(ns[0] - ns[1]) < 2, ns)
        nu = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); }
            const a = AUT[0], i = a[10][0], o = a[12][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); setTime(i, 1, a[10][1]); const s0 = SRC.au.at[IT[i].id][1]; setTime(i, 2, s0 + 3); rerenderItem(i);
            const v = document.getElementById('v' + i), has = !!v.querySelector('.tgrp .tn'), two = v.querySelectorAll('.tgrp .tn').length, other = !!document.getElementById('v' + o)?.querySelector('.tgrp .tn'), dup = !!document.querySelector('#rBody [data-a=tplay]');
            S.timing.step = 0.5; v.querySelector('.tgrp [data-k="1"][data-d="1"]').click(); const s1 = SRC.au.at[IT[i].id][1];
            document.getElementById('v' + i).querySelector('.tgrp [data-k="2"][data-d="-1"]').click(); const e1 = SRC.au.at[IT[i].id][2];
            const snipSet = PL.on && PL.snip != null && Math.abs(PL.snip - SRC.au.at[IT[i].id][2]) < 0.01;   // the end's preview plays up to the new end
            stopAudio(); S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources();
            if (!snipSet) return 'no preview';
            return [has, two, other, dup, Math.round((s1 - s0) * 10) / 10, Math.round((e1 - s0) * 10) / 10]; })()""")
        check('timing: a marked verse has ±0.5 s for its start and end; others do not; no second ▶', nu == [True, 4, False, False, 0.5, 2.5], nu)
        row = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); }
            const a = AUT[0], i = a[10][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); setTime(i, 1, a[10][1]); setTime(i, 2, SRC.au.at[IT[i].id][1] + 3); rerenderItem(i);
            const bs = [...document.getElementById('v' + i).querySelectorAll('.tmark .tgrp button')].map(b => Math.round(b.getBoundingClientRect().top));
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return bs; })()""")
        check('timing: − Starts now + and − Ends now + sit on one line at phone width', len(row) == 6 and max(row) - min(row) < 4, row)
        link = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); }
            const a = AUT[0], i = a[10][0], n = a[11][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); setTime(i, 1, a[10][1]); const s0 = SRC.au.at[IT[i].id][1]; setTime(n, 1, s0 + 4); setTime(n, 2, s0 + 7); setTime(i, 2, s0 + 4);
            setTime(i, 2, s0 + 4.5); const ns = SRC.au.at[IT[n].id][1] - s0, ie = SRC.au.at[IT[i].id][2] - s0;
            setTime(n, 1, s0 + 4.2); const ie2 = SRC.au.at[IT[i].id][2] - s0;
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [ie, ns, ie2].map(x => Math.round(x * 10) / 10); })()""")
        check('timing: an end pushed past the next start moves that start along; a start pulled back moves the previous end', link == [4.5, 4.5, 4.2], link)
        # a send bigger than one GitHub issue: the button names its parts, and "publish" goes with the last part only
        sp = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}), keepSent = JSON.stringify(S.timing.sent[tkey()] || {}), keepPub = JSON.stringify(S.timing.publish || {});
            const a = AUT[0].concat(AUT[1] || []), fx = {}; a.slice(0, SEND_MAX + 10).forEach(([i, s0], k) => { fx[IT[i].id] = [SRC.au.at[IT[i].id][0], Math.round((s0 + 0.3) * 10) / 10, null]; });
            S.timing.fix[tkey()] = fx; S.timing.sent[tkey()] = {}; (S.timing.publish = S.timing.publish || {})[tkey()] = true; save(); buildAudio();
            const urls = [], open0 = window.open; window.open = u => { urls.push(u); return null; };
            const label1 = (timingHTML().match(/id="tSend"[^>]*>(.*?)<\/button>/) || [])[1] || '';
            sendStarts(); const label2 = (timingHTML().match(/id="tSend"[^>]*>(.*?)<\/button>/) || [])[1] || ''; sendStarts();
            window.open = open0; const pub = urls.map(u => decodeURIComponent(u).includes('"publish":true'));
            const left = Object.keys(pendingStarts()).length, still = !!(S.timing.publish || {})[tkey()];
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.sent[tkey()] = JSON.parse(keepSent); S.timing.publish = JSON.parse(keepPub); S.timing.on = false; save(); applyTiming(); await loadSources();
            return [urls.length, pub, /part 1 of 2|भाग १, कुल २/.test(label1), /part/.test(label2), left, still]; })()""")
        check('timing: a send of two parts names them on the button; "publish" goes with the last part only', sp == [2, [False, True], True, False, 0, False], sp)
        # ---- audio timing: the order rule in the app and in the
        # generator give the same figures for the same marks; every write path keeps the order of the text ----
        T0 = "S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); } const keep = JSON.stringify(S.timing.fix[tkey()] || {}); PL.on = false; stopAudio();"
        T1 = "S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources();"
        # the same marks give the same times in the app (buildAudio) and in the library (tools/audio/order.py, used by make_timings.py)
        random.seed(20261020); bad = []
        for leaf, trail in leaves(shelf):
            wid = leaf['work']
            await ev(f"(async () => {{ S.timing.on = true; applyTiming(); await openWork({json.dumps(wid)}, true); await loadSources(); }})()")
            for sid in await ev("srcList('au').map(s => s.id)"):
                await ev(f"(async () => {{ (S.src[W.id] = S.src[W.id] || {{}}).au = {json.dumps(sid)}; await loadSources(); }})()")
                A = await ev("({at: SRC.au.at0, tracks: SRC.au.tracks, guess: SRC.au.guess || [], own: SRC.au.own || [], raw: SRC.au.raw || {}})")
                items = await ev("IT.map(x => [x.id, x.v.join('').length])"); IDX = {x[0]: i for i, x in enumerate(items)}; guess = set(A['guess'])
                pub = await ev("(() => { delete S.timing.fix[tkey()]; buildAudio(); return SRC.au.at; })()")
                if pub != A['at']: bad.append((wid, sid, 'published', [(k, A['at'][k], pub.get(k)) for k in A['at'] if A['at'][k] != pub.get(k)][:3]))
                for trial in range(8):   # marks near and far from the published times, with and without ends, out of order too
                    fix = {}
                    for ti, tr in enumerate(A['tracks']):
                        ids = [k for k, v in A['at'].items() if v[0] == ti and k in IDX]
                        for k in random.sample(ids, min(len(ids), random.choice([1, 3, 6]))):
                            st = max(0, round(A['at'][k][1] + random.uniform(-25, 25), 1)); fix[k] = [ti, st, round(st + random.uniform(0.5, 30), 1) if random.random() < 0.5 else None]
                    got = await ev(f"(() => {{ S.timing.fix[tkey()] = {json.dumps(fix)}; buildAudio(); return {{at: SRC.au.at, moved: [...SRC.au.moved]}}; }})()")
                    base = {k: ([v[0], A['raw'][k]] + v[2:]) if k in A['raw'] else v for k, v in A['at'].items()}; base.update(fix); exp = {}; moved = []; ownset = set(A['own']) | set(fix)
                    for ti, tr in enumerate(A['tracks']):
                        rows, mv = ORDER.keep_order(sorted([[IDX[k], v[1], v[2] if len(v) > 2 and v[2] is not None else None] for k, v in base.items() if v[0] == ti and k in IDX]), lambda i: items[i][0] in ownset, lambda i: items[i][0] not in guess, lambda i: max(8, items[i][1]), tr['dur'])
                        for i, st, en in rows: exp[items[i][0]] = [ti, st, en] if en is not None else [ti, st]
                        moved += [items[i][0] for i in mv]
                    diff = [(k, got['at'].get(k), exp.get(k)) for k in set(exp) | set(got['at']) if got['at'].get(k) != exp.get(k)]
                    if diff or set(moved) != set(got['moved']): bad.append((wid, sid, trial, diff[:3], sorted(set(moved) ^ set(got['moved']))[:3]))
                await ev("delete S.timing.fix[tkey()]; delete S.src[W.id].au; buildAudio()")
        await ev("(async () => { S.timing.on = false; applyTiming(); await loadSources(); })()")
        check('timing: the app and the library place the same times for the same marks (every recording, 8 random sets each)', not bad, bad[:2])
        # Undo (↶, the verse's bottom-left corner) redraws the verse (no more − / +, not "yours") and the neighbours it had moved
        un = await ev("""(async () => { """ + T0 + """
            const a = AUT[0], i = a[10][0], n = a[11][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            setTime(i, 1, a[10][1]); setTime(i, 2, a[11][1] + 2); clearStart(n); const nMoved = SRC.au.at[IT[n].id][1];   // the end gave n a start; Undo on n leaves it an estimate placed after the end
            const b = document.getElementById('v' + i).querySelector('.vundo [data-a=tundo]'); if (!b) return 'no undo';   // ↶, the verse's bottom-left corner
            b.click(); await new Promise(r => setTimeout(r, 200));
            const v = document.getElementById('v' + i), r = [!!myStarts()[IT[i].id], v.querySelectorAll('.tgrp .tn').length, /yours|आपका/.test(v.querySelector('.tinfo').textContent), document.getElementById('v' + n).querySelector('.tinfo').textContent.includes(fmtT(SRC.au.at[IT[n].id][1])), nMoved !== SRC.au.at[IT[n].id][1]];
            """ + T1 + """ return r; })()""")
        check('timing: ↶ under the verse redraws it and the neighbour it had moved', un == [False, 0, False, True, True], un)
        # "Until next" on a verse that has no end does nothing (the estimated start does not become "yours")
        unx = await ev("""(async () => { """ + T0 + """ const i = AUT[0][10][0]; const r = [setTime(i, 2, null), !!myStarts()[IT[i].id]]; """ + T1 + """ return r; })()""")
        check('timing: Until next on a verse without an end changes nothing', unx == [False, False], unx)
        # order between verses set by ear: a start cannot go before the previous set start, or at or past the next set start
        ordr = await ev("""(async () => { """ + T0 + """ const a = AUT[0], p = a[10][0], i = a[11][0], n = a[12][0], s0 = Math.round(a[10][1] * 10) / 10;
            setTime(p, 1, s0); setTime(n, 1, s0 + 20); setTime(i, 1, s0 + 10); const s = SRC.au.at[IT[i].id][1];
            const r = [setTime(i, 1, s0 - 1), setTime(i, 1, s0 + 20.5), SRC.au.at[IT[i].id][1] === s, setTime(i, 1, s0 + 19)];
            """ + T1 + """ return r; })()""")
        check('timing: a start cannot go before the previous set start or past the next set start', ordr == [False, False, True, None], ordr)
        # an end carried into the next verse is refused when it would squeeze that verse against the verse after it
        chain = await ev("""(async () => { """ + T0 + """ const a = AUT[0], i = a[10][0], n = a[11][0], nn = a[12][0], s = Math.round(a[10][1] * 10) / 10;
            setTime(i, 1, s); setTime(n, 1, s + 10); setTime(nn, 1, s + 14);
            const r = [setTime(i, 2, s + 15), Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10, setTime(i, 2, s + 12), Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10];
            """ + T1 + """ return r; })()""")
        check('timing: an end pushed past the next start carries it, but not into the verse after next', chain == [False, 10, None, 12], chain)
        # the link skips estimates in between: a start pulled back pulls the previous *set* end back, even with a guess between them
        skip = await ev("""(async () => { """ + T0 + """ const a = AUT[0], p = a[10][0], x = a[12][0], s = Math.round(a[10][1] * 10) / 10;
            setTime(p, 1, s); setTime(p, 2, s + 10); clearStart(a[11][0]); setTime(x, 1, s + 12); setTime(x, 1, s + 8);   // the end gave a[11] a start; Undo makes it an estimate again
            const r = [Math.round((SRC.au.at[IT[p].id][2] - s) * 10) / 10, SRC.au.at[IT[a[11][0]].id][1] >= s + 8 - 0.01 && SRC.au.at[IT[a[11][0]].id][1] <= s + 8.01];
            """ + T1 + """ return r; })()""")
        check('timing: a start pulled back pulls the previous set end back across an estimate, which sits between them', skip == [8, True], skip)
        # a verse of another recording: marking it while this one plays is refused (the time would belong to the wrong recording)
        trk = await ev("""(async () => { """ + T0 + """ if (AUT.length < 2) return 'one track'; const i = AUT[0][5][0]; PL.on = true; PL.t = 1; ytOK = true;
            const r = [setTime(i, 1, 50), !!myStarts()[IT[i].id]]; PL.on = false; ytOK = false; """ + T1 + """ return r; })()""")
        check('timing: a verse of another recording cannot be marked while this one plays', trk == [False, False], trk)
        # after a short seek back (− on an end), the player's first report is still the old time: it is not taken as arrived
        stale = await ev("(() => { PL.seekT = null; ytInfo.t = 100; seekGuard(97.5); ytInfo.t = 100; const a = playTime(); ytInfo.t = 97.6; const b = playTime(); return [a, b]; })()")
        check('timing: the old time reported after a short seek back is held until the player really moves', stale == [97.5, 97.6], stale)
        # the moment of a tap right after a seek is taken from the asked-for time, not the player's stale report
        tap = await ev("(() => { PL.seekT = null; ytInfo.t = 40; ytInfo.at = performance.now() - 2000; ytInfo.st = 1; seekGuard(300); ytInfo.t = 40; const t = nowAt(); ytInfo.st = -1; PL.seekT = null; return t; })()")
        check('timing: Starts now right after ▶ uses the asked-for time, not the stale one', 299.6 <= tap <= 300.0, tap)
        # a time already in the library counts as set by ear: it shows − / +, and a neighbour's end pushed past it carries it along
        pubown = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shirdi-sai-dhoop-aarti', true); (S.src[W.id] = S.src[W.id] || {}).au = 'pramod-medhi-times'; await loadSources(); show('home');
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); delete S.timing.fix[tkey()]; buildAudio(); const own = SRC.au.own || []; if (own.length < 3) return 'no own';
            const i = ID[own[1]], n = ID[own[2]]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const bar = markBar(i), ns = SRC.au.at[own[2]][1]; setTime(i, 2, ns + 1);
            const r = [bar.includes('data-a="tn"'), /sent|भेजा/.test(bar), Math.round(SRC.au.at[own[2]][1] * 10) / 10 === Math.round((ns + 1) * 10) / 10, !!myStarts()[own[2]]];
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return r; })()""")
        check('timing: a time already in the library shows − / + and is carried along like one set here', pubown == [True, True, True, True], pubown)
        # the light never moves on to a start placed again by the order rule (it is only a guess now), even for a heard verse
        mv = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('manas', true); await loadSources(); show('home');
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); delete S.timing.fix[tkey()]; buildAudio(); const a = AUT[0]; let k = a.findIndex((x, q) => q > 5 && [0, 1, 2].every(d => !toCheck(a[q + d][0]) && !ownAt(IT[a[q + d][0]].id)) && a[q + 2][1] - a[q][1] > 8);   // three heard verses, none set by ear (the owner's sent times would be kept, not placed again) if (k < 0) return 'no run';
            const x = a[k][0], y = a[k + 1][0], z = a[k + 2][0], ys = a[k + 1][1], zs = a[k + 2][1]; setTime(x, 1, ys + 1);   // x starts after y's heard start: y is placed again
            const moved = toCheck(y) && SRC.au.at[IT[y].id][1] > ys; PL.on = true; PL.t = 0; PL.end = null; ytOK = true; PL.seekT = null; PL.cur = x; ytInfo.t = SRC.au.at[IT[y].id][1] + 0.3; tick(); const lit = PL.cur;
            ytInfo.t = zs + 0.3; tick(); const lit2 = PL.cur; PL.on = false; ytOK = false; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [moved, lit === x, lit2 === z]; })()""")
        check('timing: the light waits on your verse past a start that was placed again, and follows the next heard one', mv == [True, True, True], mv)
        # the library's workflow (tools/audio/apply_owner_timing.py): a second send that gives a moved verse its own start back is applied
        # (on a recording timed only from its transcript: the fixture tools/site/fixtures/shirdi-transcribed, placed in a temporary library)
        tmp = tempfile.mkdtemp(); wp = 'hinduism/aarti/shirdi-sai/dhoop-aarti'; sp = 'tools/works/shirdi-sai-dhoop-aarti/audio/pramod-medhi'
        os.makedirs(os.path.join(tmp, 'library', wp, 'audio')); shutil.copy(os.path.join(ROOT, 'library', wp, 'work.json'), os.path.join(tmp, 'library', wp)); shutil.copytree(os.path.join(ROOT, 'tools/site/fixtures/shirdi-transcribed'), os.path.join(tmp, sp))
        env = dict(os.environ, SCRIPTURES_REPO=tmp); out = []
        r0 = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/audio/make_timings.py'), os.path.join(tmp, sp)], env=env, capture_output=True, text=True)
        raw = json.load(open(os.path.join(tmp, 'library', wp, 'audio', 'pramod-medhi.json')))['at']
        for end in (100, 60):   # the first send pushes the heard verses after pad1 to 100; the second lets pad3 (heard at 65.6) return to its own start
            body = os.path.join(tmp, 'body.txt'); open(body, 'w').write('```json\n' + json.dumps({'path': wp, 'source': 'pramod-medhi', 'starts': {'QKf_JPbN6Lw': {'aarti.pad1': [30.6, end]}}}) + '\n```\n')
            r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/audio/apply_owner_timing.py'), body], env=env, capture_output=True, text=True); out.append((r.returncode, r.stdout.strip().split('\n')[-1]))
        after = json.load(open(os.path.join(tmp, 'library', wp, 'audio', 'pramod-medhi.json')))['at']; shutil.rmtree(tmp)
        check('timing: a second send that lets a moved verse go back to its own start is applied by the workflow', r0.returncode == 0 and out[0][0] == 0 and out[1][0] == 0 and after['aarti.pad3'] == raw['aarti.pad3'] and 60 < raw['aarti.pad3'][1] < 100, (r0.stderr[-200:], out, raw.get('aarti.pad3'), after.get('aarti.pad3')))
        # ---- flow and navigation ----
        # a saved place at a verse no longer in the text: the reader is not broken after a refresh; the place is dropped
        await ev("(async () => { await openWork('ramraksha', true); show('home'); openReader('k', 0); })()"); await pg.wait_for_timeout(600)
        await ev("WS().last = {org: 'k', i: 999, id: 'gone.1'}; WS().pos = {k: 999}; save()")
        n_err = len(errs); await pg.reload(); await pg.wait_for_timeout(3000)
        st = await ev("[CURVIEW, document.querySelector('#loading').hidden, S.w.ramraksha.last, Object.keys(S.w.ramraksha.pos).length]")
        check('a saved place at a removed verse is dropped; the work page opens instead of an empty reader', st == ['home', True, None, 0] and len(errs) == n_err, (st, errs[n_err:]))
        # "Play all" across two recordings keeps "the whole work" and the finishing message
        wh = await ev("""(async () => { await openWork('manas', true); show('home'); playRange('k', 0, IT.length - 1); const w0 = PL.whole; PL.on = true; ytOK = true; onEnded(); const r = [w0, PL.whole, PL.t];
            const P = PLANS[0]; let d = 1; for (; d <= P.n; d++){ const [a, b] = dayRange(P.id, d); const t = SRC.au.at[IT[firstAu(a, b)].id][0]; if (SRC.au.tracks[t].li < b) break; } if (d > P.n) return r.concat(['no day spans two recordings']);
            const [a, b] = dayRange(P.id, d); playRange(P.id, a, b); const m0 = PL.endMsg; onEnded(); r.push(m0 !== '' && PL.endMsg === m0 && PL.end === b); stopAudio(); ytOK = false; return r; })()""")
        check('a reading that goes on in the next recording keeps what was asked for (whole work, the day and its message)', wh == [True, True, 1, True], wh)
        # the search page: clearing the box adds no history entry; Back to a library search keeps its kind and query
        await ev("libPath = []; show('library'); window.__pushes = 0; if (!history.__wrapped){ const o = history.pushState.bind(history); history.pushState = (...a) => { window.__pushes++; o(...a); }; history.__wrapped = 1; }")   # the browser caps history.length, so the pushes are counted
        await ev("openSearch('lib')"); await pg.fill('#q', 'ram'); await pg.wait_for_timeout(400); await pg.fill('#q', ''); await pg.wait_for_timeout(400); await pg.fill('#q', 'rudram'); await pg.wait_for_timeout(400); await pg.fill('#q', ''); await pg.wait_for_timeout(400)
        check('clearing the search box adds no history entry', await ev("window.__pushes") == 1, await ev("window.__pushes"))
        await pg.fill('#q', 'rudram'); await pg.wait_for_timeout(500)
        await (await pg.query_selector('#sRes [data-hit]')).click(); await pg.wait_for_timeout(1800)
        await pg.go_back(); await pg.wait_for_timeout(900)
        bs = await ev("[CURVIEW, SCOPE, document.querySelector('#q').value, document.querySelector('#scope').hidden, document.querySelectorAll('#sRes [data-hit]').length > 0]")
        check('Back from a work found by a library search returns to that search, its query and results kept', bs == ['search', 'lib', 'rudram', True, True], bs)
        # transliteration is a switch on the More settings page (rarely used), seen in the reader afterwards
        await ev("(async () => { await openWork('ramraksha', true); show('home'); S.settings.tr = false; save(); show('settings'); })()"); await pg.wait_for_timeout(400)
        await ev("document.querySelector('#str').click()"); await pg.wait_for_timeout(200); await ev("openReader('k', 0)"); await pg.wait_for_timeout(500)
        cap = await ev("[S.settings.tr, document.querySelectorAll('#reader .tr').length > 0, document.querySelectorAll('#rLayers button').length]")
        await ev("S.settings.tr = false; save(); refreshReader()")
        check('More settings › Transliteration turns the Roman text on under the verses; the capsule keeps its four buttons', cap == [True, True, 4], cap)
        pin = await ev("""(async () => { S.timing.on = false; applyTiming(); await openWork('manas', true); show('home'); openReader('k', 30); await new Promise(r => setTimeout(r, 700));
            stopAudio(); ytOK = false; PL.seekT = null; PL.on = true; PL.cur = -1; let err = ''; try { setCur(34); } catch (e) { err = String(e); } await new Promise(r => setTimeout(r, 1200));   // a quiet player: the tick must not move the light meanwhile (it did on CI)
            const bar = document.querySelector('#reader .bar').getBoundingClientRect().bottom, v = document.getElementById('v34'); if (!v){ PL.on = false; return ['no v34', err, CURVIEW, R.a, R.b, document.querySelectorAll('#rBody .verse').length, PL.cur, !!SRC.au, W && W.id]; } const pv = v.previousElementSibling;
            const t = (pv && pv.classList.contains('vtype') ? pv : v).getBoundingClientRect().top, nx = document.getElementById('v35').getBoundingClientRect().top;
            PL.on = false; return [Math.round(t - bar), nx < innerHeight]; })()""")
        check('playing: the verse being recited is kept at the top, the next verse in view below it', pin[0] != 'no v34' and 0 <= pin[0] <= 12 and pin[1], pin)
        # one caupāī per item: Gita Press's joint caupāīs are split; old ids, places and notes follow
        sp = await ev("""(async () => { W = null; await openWork('manas', true); const hi = SRC.hi, m = id => ((hi && hi.m[id]) || [''])[0];
            return [ID['bal.6.cau3-5'] == null, ['bal.6.cau3', 'bal.6.cau4', 'bal.6.cau5'].every(id => ID[id] != null), /चौपाई ५/.test(m('bal.6.cau3')), /३-५/.test(m('bal.6.cau5')), IT[ID['bal.6.cau5']].v.length]; })()""")
        check('Mānas: joint caupāīs are separate verses; the joint meaning sits under the last', sp == [True, True, True, True, 1], sp)
        mv = await ev("""(async () => { const me = ME(); me.notes['manas:bal.6.cau3-5'] = [{t: 'n', ts: 1}]; me.bm['manas:bal.6.cau3-5'] = 2; me.fix['manas:hi-gitapress:bal.6.cau3-5'] = {m: 'x'};
            const old = ID['bal.6.do6'] - 3; S.w.manas.last = {org: 'k', i: old}; S.w.manas.pos = {k: old}; save(); W = null; await openWork('manas', true);
            const r = [!!me.notes['manas:bal.6.cau3'], !!me.bm['manas:bal.6.cau3'], !!me.fix['manas:hi-gitapress:bal.6.cau5'], !me.notes['manas:bal.6.cau3-5'], S.w.manas.last.id];
            delete me.notes['manas:bal.6.cau3']; delete me.bm['manas:bal.6.cau3']; delete me.fix['manas:hi-gitapress:bal.6.cau5']; save(); return r; })()""")
        check('Mānas: notes, bookmarks, corrections and an old place follow the split', mv == [True, True, True, True, 'bal.6.do6'], mv)
        for v in ('vidhi', 'bookmarks', 'settings'):
            hz = await ev(f"""(async () => {{ await openWork('manas', true); show('{v}'); await new Promise(r => setTimeout(r, 300));
                const sec = document.getElementById('{v}'), b = sec.querySelector('.bar .wrap'), s0 = S.settings.size; sec.querySelector('.szp').click(); const s1 = S.settings.size; sec.querySelector('.szm').click();
                return [!!sec.querySelector('.bar .lyr'), s1 === s0 + 2, b.scrollWidth <= b.clientWidth + 1]; }})()""")
            check(f'{v}: text size and हिं · En in the header, and it fits', hz == [True, True, True], hz)
        tm = await ev("""(async () => { show('library'); document.querySelector('#libMenu').click(); await new Promise(r => setTimeout(r, 300));
            const b = document.querySelector('#sheetBody [data-tour]'); if (!b) return 'no button'; b.click(); await new Promise(r => setTimeout(r, 300));
            const on = !document.querySelector('#tour').hidden; closeTour(); const inSet = (show('settings'), /Show the tour|परिचय फिरसे/.test(document.querySelector('#setBody').innerText)); return [on, inSet]; })()""")
        check('☰ › Take the tour starts the tour; More settings does not have it', tm == [True, False], tm)
        # ☰ › Share the app (on every page): the phone's share sheet gets a short description, the store app and the website
        await ev("show('library'); window.__shared = null; Object.defineProperty(navigator, 'share', {configurable: true, value: async d => { window.__shared = d; }})")
        await (await pg.query_selector('#libMenu')).click(); await pg.wait_for_timeout(300)
        await (await pg.query_selector('#sheetBody [data-m=share]')).click(); await pg.wait_for_timeout(600)
        sh = await ev("(() => { const t = (window.__shared || {}).text || ''; return [t.trim().endsWith(location.origin + '/get'), (t.match(/https?:\\/\\//g) || []).length, /Free, no ads|निःशुल्क, बिना विज्ञापन/.test(t)]; })()")
        await ev("delete navigator.share")
        check('☰ › Share the app shares a description and one link, <site>/get', sh == [True, 1, True], sh)
        # <site>/get: a chat app's card (title, description, icon); an Android phone goes on to the Play Store, anything else to the site
        card = await ev("fetch('get/').then(r => r.text()).then(h => ['og:title', 'og:description', 'og:image'].every(k => h.includes('property=\"' + k + '\"')))")
        dest = {}
        for ua, tag in (('Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36', 'android'), ('Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148', 'iphone')):
            cx = await b.new_context(user_agent=ua); gp = await cx.new_page(); seen = []
            async def to_store(r): seen.append(r.request.url); await r.abort()   # the store itself is never opened
            await gp.route('https://play.google.com/**', to_store)
            try: await gp.goto(url + 'get/', wait_until='domcontentloaded'); await gp.wait_for_timeout(800)
            except Exception: pass
            dest[tag] = 'play' if seen and 'org.craadle.scriptures.hinduism' in seen[0] else 'site' if gp.url == url else gp.url
            await cx.close()
        check('<site>/get: a link card for chat apps; Android goes to the Play Store, an iPhone to the website', [card, dest.get('android'), dest.get('iphone')] == [True, 'play', 'site'], [card, dest])
        ft = await ev("""(async () => { await openWork('manas', true); show('home'); openReader('k', 30); await new Promise(r => setTimeout(r, 500));
            document.querySelector('#rMid').click(); await new Promise(r => setTimeout(r, 300)); const ok = document.querySelector('#sheet').classList.contains('on') && !!document.querySelector('#sheetBody .secs [data-to]'); closeSheet(); return ok; })()""")
        check('reader: tapping the footer opens the section picker', ft)
        # the footer has broken before (a tap passed the click event on as the part): tap it the way a finger does
        # (Playwright refuses to tap what is hidden or covered), in every work, and pick the last section listed: the
        # reader must move there. (While reciting, the player bar takes the footer's place, by design.)
        for leaf, trail in leaves(shelf):
            wid = leaf['work']
            for with_player in (False,):
                await ev(f"""(async () => {{ closeSheet(); await openWork({json.dumps(wid)}, true); show('home'); openReader('k', 0); await new Promise(r => setTimeout(r, 400));
                    if ({'true' if with_player else 'false'}) {{ $('#player').hidden = false; document.body.classList.add('playing'); }} }})()""")
                try:
                    await pg.click('#rMid', timeout=3000); await pg.wait_for_timeout(400)
                    opened = await ev("document.querySelector('#sheet').classList.contains('on') && document.querySelectorAll('#sheetBody .secs [data-to]').length")
                    to = await ev("(() => { const b = [...document.querySelectorAll('#sheetBody .secs [data-to]')]; return b.length ? +b[b.length - 1].dataset.to : null; })()")
                    if to is not None: await pg.click('#sheetBody .secs [data-to="%d"]' % to, timeout=3000); await pg.wait_for_timeout(700)
                    got = await ev(f"[!document.querySelector('#sheet').classList.contains('on'), (() => {{ const el = document.getElementById('v{to}'); if (!el) return false; const r = el.getBoundingClientRect(); return r.top >= 0 && r.top < innerHeight - 80; }})()]")
                    res = [bool(opened), got]
                except Exception as e:
                    res = repr(e)[:120]
                await ev("(() => { closeSheet(); $('#player').hidden = true; document.body.classList.remove('playing'); })()")
                check(f'{wid}: a tap on the reader footer opens the sections and a tap on the last one goes there' + (' (player open)' if with_player else ''), res == [True, [True, True]], res)
        bd = await ev("""(async () => { const me = ME(); me.bm[KEY(IT[40].id)] = 1; me.bm[KEY(IT[41].id)] = 2; save(); show('bookmarks'); await new Promise(r => setTimeout(r, 300));
            const n0 = document.querySelectorAll('#bmBody [data-del]').length; document.querySelector('#bmBody [data-del="40"]').click(); await new Promise(r => setTimeout(r, 300));
            const r = [n0, document.querySelectorAll('#bmBody [data-del]').length, !me.bm[KEY(IT[40].id)], !!me.bm[KEY(IT[41].id)]]; delete me.bm[KEY(IT[41].id)]; save(); return r; })()""")
        check('bookmarks: each bookmark can be removed on its own', bd == [2, 1, True, True], bd)
        th = await ev("""(async () => { await openWork('manas', true); show('home'); openReader('k', 30); await new Promise(r => setTimeout(r, 400)); const t0 = S.settings.theme;
            document.querySelector('#rMore').click(); await new Promise(r => setTimeout(r, 300)); S.settings.theme = 'light'; applyTheme(); document.querySelector('#mth').checked = false; document.querySelector('#mth').click();
            const r = [S.settings.theme, document.documentElement.getAttribute('data-theme'), document.querySelector('#sheet').classList.contains('on'), document.querySelector('#mth').checked];
            document.querySelector('#mth').click(); r.push(S.settings.theme); S.settings.theme = t0; applyTheme(); save(); closeSheet(); return r; })()""")
        check('☰ › Dark theme is one switch: on = dark, off = light, at once, the sheet stays open', th == ['dark', 'dark', True, True, 'light'], th)
        # ---- "Ends now" also starts the next verse; the preview only when nothing plays live ----
        en = await ev("""(async () => { """ + T0 + """ const a = AUT[0], i = a[10][0], n = a[11][0], m = a[12][0], s = Math.round(a[10][1] * 10) / 10;
            setTime(i, 1, s); setTime(i, 2, s + 6); const r = [Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10, !!myStarts()[IT[n].id], !!myStarts()[IT[m].id]];   // the next verse starts at the end and is yours; the one after is untouched
            setTime(i, 2, s + 5.5); r.push(Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10);   // − on the end: the start follows it back
            setTime(i, 2, s + 7); r.push(Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10);     // + on the end: carried along
            setTime(n, 1, s + 8); setTime(i, 2, s + 6.5); r.push(Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10);   // a start you set yourself no longer follows the end back
            setTime(m, 1, s + 9); clearStart(n); r.push(setTime(i, 2, s + 9.5), Math.round((SRC.au.at[IT[n].id][1] - s) * 10) / 10);   // the next verse unset again, a set verse after it: an end reaching that start is refused
            """ + T1 + """ return r; })()""")
        check('timing: Ends now gives the next unmarked verse that end as its start; the start follows the end while they are equal; refused past a set verse', en == [6, True, False, 5.5, 7, 8, False, 6.5], en)
        pv = await ev("""(async () => { """ + T0 + """ const a = AUT[0], i = a[10][0], s = Math.round(a[10][1] * 10) / 10; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            setTime(i, 1, s); setTime(i, 2, s + 4); rerenderItem(i); S.timing.step = 0.5;
            PL.on = true; PL.t = 0; PL.end = null; PL.snip = null; ytOK = true; ytInfo.st = 1; ytInfo.t = s + 20; ytInfo.at = performance.now(); PL.seekT = null;   // playing live, further on
            document.getElementById('v' + i).querySelector('.tgrp [data-k="2"][data-d="-1"]').click();
            const live = [PL.snip == null, Math.round((SRC.au.at[IT[i].id][2] - s) * 10) / 10, PL.seekT == null];   // the end moved, no preview, no seek
            ytInfo.st = 2;   // paused
            document.getElementById('v' + i).querySelector('.tgrp [data-k="2"][data-d="-1"]').click();
            const paused = [PL.snip != null && Math.abs(PL.snip - SRC.au.at[IT[i].id][2]) < 0.01, Math.round((SRC.au.at[IT[i].id][2] - s) * 10) / 10];   // now the preview plays up to the new end
            stopAudio(); ytOK = false; ytInfo.st = -1; """ + T1 + """ return live.concat(paused); })()""")
        check('timing: − / + while the recitation plays on only move the time; the 2-second preview plays when nothing is playing', pv == [True, 3.5, True, True, 3], pv)
        # the player's timing wins: a touch (a bookmark, say) or a scroll does not pause the following; the page
        # moves to the next verse the moment it starts
        fl = await ev("""(async () => { await openWork('ramraksha', true); show('home'); S.timing.on = false; openReader('k', 0); await new Promise(r => setTimeout(r, 500));
            const a = AUT[0], v1 = a[3][0], v2 = a[4][0]; PL.on = true; PL.t = 0; PL.end = null; PL.cur = -1; ytOK = true; PL.seekT = null; ytInfo.t = a[3][1] + 0.2; tick(); await new Promise(r => setTimeout(r, 900));
            const el = document.getElementById('v' + v1); el.dispatchEvent(new TouchEvent('touchstart', {bubbles: true}));   // a finger on the page
            el.querySelector('.vbm').click();   // bookmark the lit verse
            window.scrollBy(0, 600); await new Promise(r => setTimeout(r, 300));   // and scroll away
            ytInfo.t = a[4][1] + 0.2; tick(); await new Promise(r => setTimeout(r, 1200));   // the next verse starts
            const r = document.getElementById('v' + v2).getBoundingClientRect(), top = document.querySelector('#reader .bar').getBoundingClientRect().bottom;
            const ok = PL.cur === v2 && r.top >= top - 2 && r.bottom <= innerHeight;
            stopAudio(); ytOK = false; Object.keys(ME().bm).filter(k => k.startsWith(W.id + ':')).forEach(k => delete ME().bm[k]); save(); return [ok, PL.cur === v2, Math.round(r.top), Math.round(top)]; })()""")
        check('playing: after a touch, a bookmark and a scroll, the page still follows the next verse the moment it starts', fl[0], fl)
        # “↓ now playing” pill: only while the lit verse is off the screen; a tap brings it back; gone at the next verse
        jp = await ev("""(async () => { await openWork('ramraksha', true); show('home'); S.timing.on = false; openReader('k', 0); await new Promise(r => setTimeout(r, 500));
            const a = AUT[0], v1 = a[3][0], v2 = a[4][0], pill = document.querySelector('#pJump'); PL.on = true; document.querySelector('#player').hidden = false; document.body.classList.add('playing'); PL.t = 0; PL.end = null; PL.cur = -1; ytOK = true; PL.seekT = null; ytInfo.t = a[3][1] + 0.2; tick(); await new Promise(r => setTimeout(r, 900));
            const r = []; jumpPill(); r.push(pill.hidden);                                   // on screen: no pill
            window.scrollBy(0, 1200); await new Promise(r => setTimeout(r, 400)); jumpPill(); r.push(!pill.hidden, pill.textContent.startsWith('↑') && (pill.textContent.includes('Go to') || pill.textContent.includes('पर जाएँ')) && pill.textContent.includes(posLabel(v1)));   // scrolled past it: the pill, pointing up
            pill.click(); await new Promise(r => setTimeout(r, 900)); jumpPill(); r.push(pill.hidden, inView(document.getElementById('v' + v1)));   // a tap: back to the verse, pill gone
            window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)); jumpPill(); r.push(!pill.hidden && pill.textContent.startsWith('↓'));   // scrolled before it: pointing down
            ytInfo.t = a[4][1] + 0.2; tick(); await new Promise(r => setTimeout(r, 1200)); jumpPill(); r.push(pill.hidden, PL.cur === v2);   // the next verse starts: the page follows, no pill
            stopAudio(); ytOK = false; r.push(pill.hidden); return r; })()""")
        check('playing: the “now playing” pill shows only while the lit verse is off screen, points the way, and brings it back on a tap', jp == [True, True, True, True, True, True, True, True, True], jp)
        # offline reading: a work opened once is readable with no network at all; a work never opened says so
        srv2 = serve(); url2 = f'http://127.0.0.1:{srv2.server_address[1]}/'
        ctx2 = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); pg3 = await ctx2.new_page(); errs3 = []
        pg3.on('pageerror', lambda e: errs3.append(str(e))); await pg3.add_init_script('window.__SALUTE_MS = 0; window.__SW_TEST = 1')
        await pg3.goto(url2); await pg3.wait_for_timeout(2500)
        sw = await pg3.evaluate("navigator.serviceWorker.getRegistration().then(r => r ? (r.active ? 'active' : 'installing') : 'none')")
        check('offline: the service worker installs (every file in its list once — a duplicate makes it fail silently)', sw == 'active', sw)
        await pg3.reload(); await pg3.wait_for_timeout(2000)   # now every file goes through the worker
        await pg3.evaluate("(async () => { S.settings.tour = 1; closeTour(); await openWork('ramraksha'); S.settings.layers.h = true; S.settings.layers.e = true; save(); })()"); await pg3.wait_for_timeout(1500)
        kept = await pg3.evaluate("caches.keys().then(async ks => { const c = await caches.open('lib-v1'); const es = await c.keys(); return [ks.includes('lib-v1'), es.filter(r => r.url.includes('/library/')).length]; })")
        srv2.shutdown(); srv2.server_close()   # the network is gone
        await pg3.reload(); await pg3.wait_for_timeout(3000)
        off = await pg3.evaluate("(async () => { if (!W || W.id !== 'ramraksha') await openWork('ramraksha', true); show('home'); openReader('k', 0); await new Promise(r => setTimeout(r, 600)); return [W && W.id, document.querySelectorAll('#reader .verse').length, document.querySelectorAll('#reader .layer.h').length, document.querySelectorAll('#reader .layer.e').length, document.querySelector('#loading').hidden]; })()")
        never = await pg3.evaluate("(async () => { await openWork('manas'); return [W && W.id, document.querySelector('#toast').textContent]; })()")
        check('offline: a work opened once is readable without any network, with its meanings', kept[0] and kept[1] >= 4 and off[0] == 'ramraksha' and off[1] > 0 and off[2] > 0 and off[3] > 0 and off[4], (kept, off, errs3[:2]))
        check('offline: a work never opened on this phone says so', never[0] == 'ramraksha' and ('No internet' in never[1] or 'इंटरनेट' in never[1]), never)
        await ctx2.close()
        # the speed button in the player bar cycles the speeds; ☰ has no speed and no reading timer
        sp = await ev("""(async () => { await openWork('ramraksha', true); show('home'); openReader('k', 0); S.settings.rate = 1; applyRate(); playFrom(0, null); await new Promise(r => setTimeout(r, 300));
            const b = document.querySelector('#pRate'), r = [b.textContent, !!b.offsetParent]; b.click(); r.push(b.textContent, S.settings.rate); for (let k = 0; k < 5; k++) b.click(); r.push(S.settings.rate);
            document.querySelector('#rMore').click(); await new Promise(r => setTimeout(r, 200)); r.push(!document.querySelector('#sheetBody [data-rate]'), !!document.querySelector('#sheetBody [data-m=timer]'), !!document.querySelector('#timerPill'));   // six taps: round the six speeds, back to 1×; the speed is only in the bar
            closeSheet(); S.settings.rate = 1; applyRate(); stopAudio(); return r; })()""")
        check('player: a speed button in the bar steps through the speeds; speed is nowhere else; no reading timer', sp == ['1×', True, '1.25×', 1.25, 1, True, False, False], sp)
        # Bookmarks & notes: each list folds under its heading, and a fold is remembered
        fd = await ev("""(async () => { await openWork('manas', true); show('home'); const me = ME(); me.bm[KEY(IT[3].id)] = 1; save(); show('bookmarks'); await new Promise(r => setTimeout(r, 300));
            const d = document.querySelector('#bmBody .bmsec[data-fold=bm]'), r = [d.open, d.querySelectorAll('.res').length]; d.querySelector('summary').click(); await new Promise(r => setTimeout(r, 200)); r.push(d.open, !!(S.settings.bmFold || {}).bm);
            show('home'); show('bookmarks'); await new Promise(r => setTimeout(r, 300)); r.push(document.querySelector('#bmBody .bmsec[data-fold=bm]').open, document.querySelector('#bmBody .bmsec[data-fold=notes]').open);
            document.querySelector('#bmBody .bmsec[data-fold=bm] summary').click(); await new Promise(r => setTimeout(r, 200)); delete me.bm[KEY(IT[3].id)]; delete S.settings.bmFold; save(); return r; })()""")
        check('bookmarks & notes: the lists fold under their headings and a fold is remembered', fd == [True, 1, False, True, False, True], fd)
        # the timing controls sit under the verse and in the player bar: ↶ is the verse's fourth corner, the saffron
        # ±step chip beside ✕ cycles (timing mode only), Until next removes the end, ⋮ holds nothing about timing
        tc = await ev("""(async () => { """ + T0 + """ const a = AUT[0], i = a[10][0], s0 = Math.round(a[10][1] * 10) / 10; openReader('k', i); await new Promise(r => setTimeout(r, 500));
            setTime(i, 1, s0); setTime(i, 2, s0 + 6); rerenderItem(i); const v = () => document.getElementById('v' + i); S.timing.step = 0.5; syncStep(); const st = document.querySelector('#pStep');
            const r = [!st.hidden, st.textContent, getComputedStyle(st).color === getComputedStyle(v().querySelector('.tmark button')).color]; st.click(); r.push(S.timing.step, st.textContent);
            v().querySelector('[data-a=tnone]').click(); r.push(SRC.au.at[IT[i].id][2] == null, !v().querySelector('[data-a=tnone]'), !!v().querySelector('.vundo'), !!v().querySelector('.vplay'));
            itemMenu(i); await new Promise(r => setTimeout(r, 200)); r.push(!document.querySelector('#sheetBody .tbox')); closeSheet(); S.timing.step = 0.5; """ + T1 + """ syncStep(); r.push(document.querySelector('#pStep').hidden); return r; })()""")
        check('timing: the ±step chip in the player bar (saffron, timing mode only) cycles; Until next removes the end; ↶ is the fourth corner; ⋮ holds nothing about timing', tc == [True, '±0.5 s', True, 1, '±1 s', True, True, True, True, True, True], tc)
        # Next ▸ (saffron, player bar, timing mode only): a finger's tap goes to the next verse still to check after the one
        # playing and plays it, round to the first; the count drops when one is set by ear; hidden when none is left
        await ev("(async () => { " + T0 + """ window.__keep = keep; const a = AUT[0], ids = [a[20][0], a[40][0], a[5][0]]; SRC.au.checkSet = new Set(ids.map(i => IT[i].id)); window.__nx = ids; window.__got = []; openReader('k', a[10][0]); await new Promise(r => setTimeout(r, 400)); PL.on = true; PL.cur = a[10][0]; $('#player').hidden = false; syncStep();
            // on a runner with YouTube, the real player moves the lit verse between taps: each tap starts from the verse the last
            // one reached (pinned as the tap begins, capture phase) and records where it went (right after the app's handler)
            window.__at = a[10][0]; window.__h = [['#pCheck', () => { PL.cur = window.__at; }, true], ['#pCheck', () => { window.__got.push(PL.cur); window.__at = PL.cur; }, false],
              ['#pNext', () => { PL.t = SRC.au.at[IT[window.__nx[2]].id][0]; PL.cur = window.__nx[2]; window.__t0 = SRC.au.at[IT[PL.cur].id][1]; }, true], ['#pNext', () => { window.__t1 = ytInfo.t; }, false]];
            window.__h.forEach(([s, f, c]) => $(s).addEventListener('click', f, c)); })()""")
        nx = [await ev("[!$('#pCheck').hidden, $('#pCheck').textContent === T('अगला ▸ ', 'Next ▸ ') + DEV(3), getComputedStyle($('#pCheck')).backgroundColor === getComputedStyle($('#pStep')).color]")]
        for _ in range(3): await pg.click('#pCheck'); await pg.wait_for_timeout(250)
        nx.append(await ev("window.__got.map(i => window.__nx.indexOf(i))"))
        nx.append(await ev("(() => { const i = window.__nx[0]; setTime(i, 1, SRC.au.at[IT[i].id][1]); refreshMarks({}, i); return $('#pCheck').textContent === T('अगला ▸ ', 'Next ▸ ') + DEV(2); })()"))
        lay = await ev("(() => { const r = s => document.querySelector(s).getBoundingClientRect(), v = r('.ytw'), c = r('#pCheck'), t = r('#pStep'), x = r('#pClose'); return [c.left >= v.right, t.left >= v.right, x.bottom <= Math.min(c.top, t.top) + 1, Math.abs(c.top - t.top) < 2]; })()")
        check('timing: in the player bar ✕ sits on its own line above Next ▸ and ±step, which stay clear of the video', lay == [True, True, True, True], lay)
        RT = "(() => { const r = s => document.querySelector(s).getBoundingClientRect(), t = r('#pRate'), x = r('#pClose'), p = r('#pPlay'); return [t.right <= innerWidth, t.top < p.top ? 'top' : 'controls', Math.abs((t.top + t.bottom) / 2 - (x.top + x.bottom) / 2) < 4]; })()"
        rw = [await ev(RT)]; await pg.set_viewport_size({'width': 360, 'height': 844}); await pg.wait_for_timeout(300); rw.append(await ev(RT)); await pg.set_viewport_size({'width': 390, 'height': 844}); await pg.wait_for_timeout(300)
        check('player bar: 1× stays after ⏭ on a 390-px phone, and moves up beside ✕ on a 360-px one, never cut off', rw == [[True, 'controls', False], [True, 'top', True]], rw)
        await pg.click('#pNext'); await pg.wait_for_timeout(300); nx.append(await ev("window.__t1 > window.__t0"))   # ⏭ still goes on to the next verse
        nx.append(await ev("(() => { const ids = [...document.querySelectorAll('[id]')].map(e => e.id); return ids.length === new Set(ids).size; })()"))   # an id used twice took ⏭'s tap away once
        nx.append(await ev("(async () => { window.__h.forEach(([s, f, c]) => $(s).removeEventListener('click', f, c)); stopAudio(); ytOK = false; $('#player').hidden = true; const keep = window.__keep; " + T1 + " syncStep(); return $('#pCheck').hidden; })()"))
        check('timing: Next ▸ in the player bar (saffron) goes to the next verse to check and plays it, round to the first; the count drops when one is set; hidden when timing is off; no id is used twice; ⏭ still works', nx == [[True, True, True], [0, 1, 2], True, True, True, True], nx)
        # while Audio timing is on, ☰ shows its switch and Clear adjustments at the top level
        tm2 = await ev("""(async () => { """ + T0 + """ const i = AUT[0][10][0]; openReader('k', i); await new Promise(r => setTimeout(r, 400)); setTime(i, 1, AUT[0][10][1]);
            document.querySelector('#rMore').click(); await new Promise(r => setTimeout(r, 300)); const r = [!!document.querySelector('#mtm'), !!document.querySelector('#sheetBody [data-m=tclear]')];
            document.querySelector('#mtm').click(); await new Promise(r => setTimeout(r, 700)); r.push(S.timing.on, !document.querySelector('#sheet').classList.contains('on'), !document.getElementById('v' + i).querySelector('.tmark'));
            document.querySelector('#rMore').click(); await new Promise(r => setTimeout(r, 300)); r.push(!document.querySelector('#mtm')); closeSheet(); S.timing.on = true; applyTiming(); await loadSources(); """ + T1 + """ return r; })()""")
        check('☰ while timing is on: the switch turns it off at once and Clear adjustments is there; off, neither shows', tm2 == [True, True, False, True, True, True], tm2)
        # headings follow the text size; the ⋮ menu's ▶ is blue
        hs = await ev("""(async () => { await openWork('manas', true); show('home'); S.settings.tr = true; S.settings.size = 21; applyTheme(); openReader('k', 0); await new Promise(r => setTimeout(r, 400));
            const px = q => parseFloat(getComputedStyle(document.querySelector('#rBody ' + q)).fontSize); const a = ['.part-h b', '.topic-h b', '.vtype', '.tr'].map(px);
            S.settings.size = 34; applyTheme(); await new Promise(r => setTimeout(r, 100)); const b = ['.part-h b', '.topic-h b', '.vtype', '.tr'].map(px);
            itemMenu(0); await new Promise(r => setTimeout(r, 200)); const play = getComputedStyle(document.querySelector('#sheetBody [data-x=play] svg')).color, copy = getComputedStyle(document.querySelector('#sheetBody [data-x=copy] svg')).stroke; closeSheet();
            S.settings.size = 21; S.settings.tr = false; applyTheme(); save(); return [a.every((v, k) => b[k] > v * 1.4), play === copy, a.map(Math.round)]; })()""")
        check('reader: the part and topic headings and the transliteration grow with the text size; the ⋮ menu’s ▶ is blue like its other icons', hs[0] and hs[1], hs)
        # a shelf shows two works, the most recently used first, then +N
        sh2 = await ev("""(async () => { const keep = JSON.stringify(Object.fromEntries(Object.entries(S.w).map(([k, v]) => [k, v.at]))); Object.values(S.w).forEach(v => delete v.at);
            await openWork('isha-upanishad', true); libPath = []; show('library'); await new Promise(r => setTimeout(r, 200));
            const row = [...document.querySelectorAll('#libList li')].find(li => li.querySelector('[data-node="hinduism/veda"], [data-node="veda"]')); const chips = [...row.querySelectorAll('[data-open-work]')].map(b => b.dataset.openWork), more = row.querySelector('.more');
            const g = [...document.querySelectorAll('#libList li')].find(li => li.querySelector('[data-node="hinduism/granth"], [data-node="granth"]')); const gchips = g.querySelectorAll('[data-open-work]').length;
            JSON.parse(keep); Object.entries(JSON.parse(keep)).forEach(([k, v]) => { if (S.w[k]) { if (v) S.w[k].at = v; else delete S.w[k].at; } }); save(); return [chips[0], chips.length, !!more, gchips]; })()""")
        check('library: a shelf shows two works, the one used most recently first', sh2[0] == 'isha-upanishad' and sh2[1] <= 2 and sh2[3] <= 2, sh2)
        # one word for one thing: no "text" for a verse, no "listen/hear" for play, no "translation", no "Adjust audio timing"
        words = await ev("""(() => { const src = [...document.querySelectorAll('[data-en]')].map(e => e.dataset.en).join(' | '); return src; })()""")
        bad = [w for w in ('Listen', 'translation', 'Adjust audio timing', 'the text') if w in words]
        check('labels: the template uses the app\'s vocabulary', not bad, bad)
        # ⋮ order: Play from here · Write a note · Copy verse and meaning · Correct …
        order = await ev("(async () => { await openWork('manas', true); show('home'); openReader('k', 0); await new Promise(r => setTimeout(r, 300)); itemMenu(0); await new Promise(r => setTimeout(r, 200)); const r = [...document.querySelectorAll('#sheetBody [data-x]')].map(b => b.dataset.x); closeSheet(); return r; })()")
        check('⋮: Write a note comes before Copy verse and meaning', order[:4] == ['play', 'note', 'copy', 'edit'], order)
        # line by line: a source with a piece per verse line shows each piece under its line; a source
        # without pieces, and a verse with no pieces at all, show the meaning whole after the verse
        lbl = await ev("""(async () => { await openWork('sukhmani-sahib', true); S.settings.layers = {h: true, e: true, w: false}; S.settings.pair = 'hi,en'; S.settings.recite = false; await loadSources();
            const i = IT.findIndex(x => x.id === 'a01.p3'), it = IT[i], n = it.v.length;
            const keep = {h: SRC.hi.p, e: SRC.en.p}; SRC.hi.p = {}; SRC.en.p = {};
            SRC.en.p[it.id] = it.v.map((_, k) => k === 1 ? '' : 'EN' + k); SRC.hi.p[it.id] = it.v.map((_, k) => 'HI' + k);
            const d = document.createElement('div'); d.innerHTML = verseHTML(i); const v = d.firstElementChild;
            const kids = [...v.children].map(c => c.classList.contains('vline') ? 'V' : c.classList.contains('h') ? 'h' : c.classList.contains('e') ? 'e' : '');
            const r1 = [v.querySelectorAll('.vline').length === n, v.querySelectorAll('.layer.h').length === n, v.querySelectorAll('.layer.e').length === n - 1, kids.slice(0, 6).join('') === 'VheVhV'];
            delete SRC.en.p[it.id]; d.innerHTML = verseHTML(i); const w = d.firstElementChild;
            const r2 = [w.querySelectorAll('.layer.e').length === 1, w.lastElementChild.classList.contains('e'), w.querySelectorAll('.layer.h').length === n];
            SRC.hi.p = {}; d.innerHTML = verseHTML(i); const u = d.firstElementChild;
            const r3 = [u.querySelectorAll('.vline').length === 0, u.querySelectorAll('.vtext').length === 1];
            SRC.hi.p = keep.h; SRC.en.p = keep.e; delete S.settings.pair; return [...r1, ...r2, ...r3]; })()""")
        check('meanings line by line: each piece under its line; a source without pieces shows whole after the verse; none at all keeps the verse whole', all(lbl), lbl)
        # a third meaning language: with a Punjabi source the capsule shows ਪੰ · En (English app) or ਪੰ · हिं
        # (Hindi app), always four places; Punjabi pieces sit under their lines; Sources lists it and "Meanings in the bar";
        # search finds it; recitation mode turns it off too
        pa = await ev("""(async () => { await openWork('sukhmani-sahib', true); show('home'); const S0 = JSON.stringify(S.settings);
            S.settings.ui = 'en'; S.settings.layers = {h: false, e: true, w: false, pa: true}; S.settings.recite = false; delete S.settings.pair;
            const i = IT.findIndex(x => x.id === 'a01.p3'), it = IT[i], n = it.v.length;
            W.sources.pa = [{id: 'pa-test', file: 'meanings/pa-test', title: {hi: 'परीक्षा', en: 'Test'}}];
            SRC.pa = {meta: W.sources.pa[0], id: 'pa-test', m: {[it.id]: ['ਪਰਖ ਅਰਥ ਸਾਰਾ']}, p: {[it.id]: it.v.map((_, k) => 'ਪਰਖ' + k)}}; IDX = null;
            syncLayers(); openReader('k', i); await new Promise(r => setTimeout(r, 400));
            const cap = () => [...document.querySelectorAll('#rLayers button')].map(b => b.textContent.trim() || b.dataset.l).join('·');
            const c1 = cap();
            const d = document.createElement('div'); d.innerHTML = verseHTML(i); const v = d.firstElementChild;
            const lay = [v.querySelectorAll('.layer.pa').length === n, v.querySelector('.vline + .layer.pa') != null, v.querySelectorAll('.layer.e').length > 0];
            S.settings.ui = 'hi'; syncLayers(); const c2 = cap();
            S.settings.pair = 'hi,en'; syncLayers(); const c3 = cap(); delete S.settings.pair; S.settings.ui = 'en'; syncLayers();
            show('settings'); await new Promise(r => setTimeout(r, 200));
            const srcs = [!!document.querySelector('#setBody [data-src="pa"]'), [...document.querySelectorAll('#sPair option')].map(o => o.textContent).join('|')];
            openSearch('text'); document.querySelector('#q').value = 'ਪਰਖ ਅਰਥ'; runSearch(); const found = document.querySelectorAll('#sRes .res').length > 0 && !document.querySelector('#scope [data-s="pa"]').hidden;
            toggleRecite(); const off = !S.settings.layers.pa; toggleRecite(); const back = !!S.settings.layers.pa;
            delete W.sources.pa; SRC.pa = null; IDX = null; S.settings = JSON.parse(S0); syncLayers(); save(); show('home');
            return {c1, c2, c3, lay, srcs, found, off, back}; })()""")
        check('a third meaning language: ਪੰ · En in an English app, ਪੰ · हिं in a Hindi one, हिं · En when chosen; four places', pa['c1'].split('·')[:2] == ['ਪੰ', 'En'] and pa['c2'].split('·')[:2] == ['ਪੰ', 'हिं'] and pa['c3'].split('·')[:2] == ['हिं', 'En'] and len(pa['c1'].split('·')) == 4, pa)
        check('a third meaning language: its pieces under their lines, listed in Sources with "Meanings in the bar", searchable, off in recitation mode',
              all(pa['lay']) and pa['srcs'][0] and pa['srcs'][1].split('|') == ['ਪੰ · En', 'ਪੰ · हिं', 'हिं · En'] and pa['found'] and pa['off'] and pa['back'], pa)
        # a Roman-letter search shows the verse itself; Play from here ends with the open section
        rs = await ev("(async () => { await openWork('manas', true); show('home'); openSearch('text'); document.querySelector('#q').value = 'asur chal chonip'; runSearch(); await new Promise(r => setTimeout(r, 300)); const r = document.querySelector('#sRes .res'); return r ? [r.querySelector('.where').textContent, r.querySelector('.snip').textContent.slice(0, 12)] : 'none'; })()")
        check('search: a verse found by Roman letters is shown as the verse', rs != 'none' and ('Verses' in rs[0] or 'मूल पाठ' in rs[0]) and 'रहे' in rs[1], rs)
        pf = await ev("(async () => { const P = PLANS[0]; const [a, b] = dayRange(P.id, 2); openReader(P.id, a + 3); await new Promise(r => setTimeout(r, 300)); itemMenu(a + 3); await new Promise(r => setTimeout(r, 200)); document.querySelector('#sheetBody [data-x=play]').click(); const r = [PL.end === b, PL.endMsg]; stopAudio(); return r; })()")
        check('Play from here ends with the open vishram, with its message', pf[0] and 'finished' in pf[1], pf)
        check('no script errors anywhere', not errs, '; '.join(errs[:3]))
        await b.close()
    print(f'\n{sum(results)}/{len(results)} checks passed')
    sys.exit(0 if all(results) else 'UX TEST FAILED')
asyncio.run(main())
