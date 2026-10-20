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
        bm0 = await ev("Object.keys(ME().bm).length")
        await ev("tourSteps()[7].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: tapping the bookmark sign saves the verse and moves on', await ev("TOUR && TOUR.k") == 8 and await ev("Object.keys(ME().bm).length") == bm0 + 1)
        await ev("for (const k in ME().bm) delete ME().bm[k]; save()")
        await ev("tourSteps()[8].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: playing a verse ends the tour in the reader, with a message and the meanings back', await ev("!TOUR && document.querySelector('#tour').hidden && document.querySelector('#coach').hidden && CURVIEW === 'reader' && PL.on && !S.settings.recite && /Tour complete|परिचय पूरा/.test(document.querySelector('#toast').textContent)"))
        await ev("setSize(-2)"); await ev("stopAudio()")
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
        # no greeting when the app starts, on a refresh, or on a quiet open (owner, 2026-10-19)
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
        rows = await ev("document.querySelectorAll('#libList [data-node]').length")
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
        await ev("S.settings.layers.e = true; S.settings.layers.h = true; save()")
        check('the meanings do not change the language of the app', await ev("LANG()") == other)
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
                # after "Ends now", the next verse is lit at once (review mode), so its start can be marked; the bar moves
                a0 = await ev("AUT[0][1] ? AUT[0][1] : AUT[0][0]")
                if await ev("AUT[0].length > 3"):
                    v1, s1 = await ev("[AUT[0][1][0], AUT[0][1][1]]"); v2 = await ev("AUT[0][2][0]"); s2 = await ev("AUT[0][2][1]")
                    if s2 - s1 > 2:
                        await ev(f"PL.on = true; PL.t = 0; PL.end = null; ytOK = true; ytInfo.t = {s1} + 1; setTime({v1}, 2, {s1} + 0.5)")
                        check(f'{tag}: after an end is set, the next verse is lit at once', await ev("PL.cur") == v2, [await ev("PL.cur"), v2])
                        check(f'{tag}: the progress bar moves while playing', (await ev("document.querySelector('#pProg').style.width")) not in ('', '0%'))
                        await ev("S.timing.on = false; PL.cur = -1; tick()")
                        check(f'{tag}: outside review mode the highlight follows the starts only', await ev("PL.cur") == await ev("curAt(ytInfo.t)"), [await ev("PL.cur"), v1])
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
            await ev("S.settings.ui = 'en'; S.settings.layers.e = true; S.settings.layers.h = false; applyLang(); refreshReader()"); await pg.wait_for_timeout(500)
            en_hdr = await ev("document.querySelector('#rMid').innerText")
            check(f'{tag}: English interface works in the reader', bool(en_hdr.strip()), en_hdr)
            # recitation mode is the fourth button of the reader's capsule: it hides the meanings; a meaning turned on ends it
            await ev("S.settings.recite = false; S.settings.layers.h = true; S.settings.layers.e = true; save(); applyRecite(); refreshReader()")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(400)
            ok1 = await ev("S.settings.recite && !S.settings.layers.h && !S.settings.layers.e && !S.settings.layers.w && document.body.classList.contains('recite') && document.querySelector('#rLayers [data-l=r]').classList.contains('on')")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(400)
            ok2 = await ev("!S.settings.recite && S.settings.layers.h && S.settings.layers.e")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(300)
            await (await pg.query_selector('#rLayers [data-l=h]')).click(); await pg.wait_for_timeout(300)
            ok3 = await ev("!S.settings.recite && S.settings.layers.h && !document.body.classList.contains('recite')")
            check(f'{tag}: recitation mode from the capsule hides meanings and restores them; a meaning ends it', ok1 and ok2 and ok3, [ok1, ok2, ok3])
            wide2 = await ev("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(f'{tag}: the reader header still fits', wide2 <= 0, wide2)
            # English app, Hindi meaning only inside the work: the reader's words are Hindi; back on the work page, English
            await ev("S.settings.ui = 'en'; S.settings.layers.e = false; S.settings.layers.h = true; applyLang(); refreshReader()"); await pg.wait_for_timeout(400)
            check(f'{tag}: inside the work the words follow the Hindi meaning', await ev("LANG()") == 'hi')
            await ev("show('home')"); await pg.wait_for_timeout(200)
            check(f'{tag}: the work page keeps the app language', await ev("LANG()") == 'en')
            await ev("show('reader')"); await pg.wait_for_timeout(200)
            await ev("S.settings.ui = 'hi'; S.settings.layers.h = true; S.settings.layers.e = false; applyLang()")
            # the work menu (☰) leads to bookmarks and settings
            await ev("show('home')"); await pg.wait_for_timeout(300)
            await (await pg.query_selector('#hMenu')).click(); await pg.wait_for_timeout(300)
            items = await ev("Array.from(document.querySelectorAll('#sheetBody [data-go]')).map(b => b.dataset.go)")
            check(f'{tag}: ☰ holds bookmarks and settings', 'bookmarks' in items and 'settings' in items, items)
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
        check('settings: no Readers section, the new titles', 'Readers' not in st and 'पढ़नेवाले' not in st and ('My bookmarks & notes' in st or 'मेरे बुकमार्क और टिप्पणियाँ' in st) and 'Show while reading' not in st, st[:80])
        await ev("show('library')"); await pg.wait_for_timeout(500)
        s0 = await ev("S.settings.size"); await ev("document.querySelector('#library .szp').click()"); s1 = await ev("S.settings.size")
        check('library: A+ in its header changes the text size', s1 == s0 + 2, [s0, s1])
        await ev("document.querySelector('#library .szm').click()")
        fits = await ev("(() => { const b = document.querySelector('#library .bar .wrap'); return b.scrollWidth <= b.clientWidth + 1; })()")
        check('library: the header still fits a phone', fits)
        # ▶ after a seek: an old time reported by the player does not light the previous verse
        guard = await ev("(() => { PL.seekT = null; seekGuard(100); ytInfo.t = 40; const a = playTime(); ytInfo.t = 100.2; const b = playTime(); ytInfo.t = 99; const c = playTime(); return [a, b, c]; })()")
        check('a stale time right after a seek is held at the asked-for start', guard == [100, 100.2, 99], guard)
        # a refresh keeps you on the same page (owner, 2026-10-19)
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
        gap = await ev("(async () => { show('settings'); await new Promise(r => setTimeout(r, 300)); const b = [...document.querySelectorAll('#setBody .acts .btn')].slice(0, 2).map(x => x.getBoundingClientRect()); return b.length == 2 ? Math.round(b[1].left - b[0].right) : -1; })()")
        check('settings buttons stand apart', gap >= 8, gap)
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
        # timing: "Ends now" on a verse whose estimated start lies after now takes the previous verse's set end as its start
        te = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
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
        ns = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
            const a = AUT[0], i = a[8][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); PL.on = true; PL.t = 0; PL.hold = 0; setCur(i); await new Promise(r => setTimeout(r, 900));
            const y0 = scrollY; ytInfo.t = a[8][1] + 1; setTime(i, 2, a[8][1] + 1); await new Promise(r => setTimeout(r, 900)); const y1 = scrollY;
            PL.on = false; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [y0, y1]; })()""")
        check('timing: marking a verse does not move the page', abs(ns[0] - ns[1]) < 2, ns)
        nu = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
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
        row = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
            const a = AUT[0], i = a[10][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); setTime(i, 1, a[10][1]); setTime(i, 2, SRC.au.at[IT[i].id][1] + 3); rerenderItem(i);
            const bs = [...document.getElementById('v' + i).querySelectorAll('.tmark .tgrp button')].map(b => Math.round(b.getBoundingClientRect().top));
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return bs; })()""")
        check('timing: − Starts now + and − Ends now + sit on one line at phone width', len(row) == 6 and max(row) - min(row) < 4, row)
        link = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
            const a = AUT[0], i = a[10][0], n = a[11][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); setTime(i, 1, a[10][1]); const s0 = SRC.au.at[IT[i].id][1]; setTime(n, 1, s0 + 4); setTime(n, 2, s0 + 7); setTime(i, 2, s0 + 4);
            setTime(i, 2, s0 + 4.5); const ns = SRC.au.at[IT[n].id][1] - s0, ie = SRC.au.at[IT[i].id][2] - s0;
            setTime(n, 1, s0 + 4.2); const ie2 = SRC.au.at[IT[i].id][2] - s0;
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [ie, ns, ie2].map(x => Math.round(x * 10) / 10); })()""")
        check('timing: an end pushed past the next start moves that start along; a start pulled back moves the previous end', link == [4.5, 4.5, 4.2], link)
        # ---- audio timing, reviewed 2026-10-20 (docs/handoff/2026-10-20-timing-review.md): the order rule in the app and in the
        # generator give the same figures for the same marks; every write path keeps the order of the text ----
        T0 = "S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); const keep = JSON.stringify(S.timing.fix[tkey()] || {}); PL.on = false; stopAudio();"
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
        # Undo in the ⋮ menu redraws the verse (no more − / +, not "yours") and the neighbours it had moved
        un = await ev("""(async () => { """ + T0 + """
            const a = AUT[0], i = a[10][0], n = a[11][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            setTime(i, 1, a[10][1]); setTime(i, 2, a[11][1] + 2); const nMoved = SRC.au.at[IT[n].id][1];
            itemMenu(i); await new Promise(r => setTimeout(r, 200)); const b = [...document.querySelectorAll('#sheetBody [data-t]')].find(x => x.dataset.t === 'undo'); if (!b) return 'no undo';
            b.click(); await new Promise(r => setTimeout(r, 200));
            const v = document.getElementById('v' + i), r = [!!myStarts()[IT[i].id], v.querySelectorAll('.tgrp .tn').length, /yours|आपका/.test(v.querySelector('.tinfo').textContent), document.getElementById('v' + n).querySelector('.tinfo').textContent.includes(fmtT(SRC.au.at[IT[n].id][1])), nMoved !== SRC.au.at[IT[n].id][1]];
            """ + T1 + """ return r; })()""")
        check('timing: Undo in the ⋮ menu redraws the verse and the neighbour it had moved', un == [False, 0, False, True, True], un)
        # "Until next" on a verse that has no end does nothing (it used to make the estimated start "yours")
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
            setTime(p, 1, s); setTime(p, 2, s + 10); setTime(x, 1, s + 12); setTime(x, 1, s + 8);
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
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); delete S.timing.fix[tkey()]; buildAudio(); const a = AUT[0]; let k = a.findIndex((x, q) => q > 5 && !toCheck(x[0]) && !toCheck(a[q + 1][0]) && !toCheck(a[q + 2][0]) && a[q + 2][1] - a[q][1] > 8); if (k < 0) return 'no run';
            const x = a[k][0], y = a[k + 1][0], z = a[k + 2][0], ys = a[k + 1][1], zs = a[k + 2][1]; setTime(x, 1, ys + 1);   // x starts after y's heard start: y is placed again
            const moved = toCheck(y) && SRC.au.at[IT[y].id][1] > ys; PL.on = true; PL.t = 0; PL.end = null; ytOK = true; PL.seekT = null; PL.cur = x; ytInfo.t = SRC.au.at[IT[y].id][1] + 0.3; tick(); const lit = PL.cur;
            ytInfo.t = zs + 0.3; tick(); const lit2 = PL.cur; PL.on = false; ytOK = false; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [moved, lit === x, lit2 === z]; })()""")
        check('timing: the light waits on your verse past a start that was placed again, and follows the next heard one', mv == [True, True, True], mv)
        # the library's workflow (tools/audio/apply_owner_timing.py): a second send that gives a moved verse its own start back is applied
        tmp = tempfile.mkdtemp(); wp = 'hinduism/aarti/shirdi-sai/dhoop-aarti'; sp = 'tools/works/shirdi-sai-dhoop-aarti/audio/pramod-medhi'
        os.makedirs(os.path.join(tmp, 'library', wp, 'audio')); shutil.copy(os.path.join(ROOT, 'library', wp, 'work.json'), os.path.join(tmp, 'library', wp)); shutil.copytree(os.path.join(ROOT, sp), os.path.join(tmp, sp))
        env = dict(os.environ, SCRIPTURES_REPO=tmp); out = []
        r0 = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/audio/make_timings.py'), os.path.join(tmp, sp)], env=env, capture_output=True, text=True)
        raw = json.load(open(os.path.join(tmp, 'library', wp, 'audio', 'pramod-medhi.json')))['at']
        for end in (100, 60):   # the first send pushes the heard verses after pad1 to 100; the second lets pad3 (heard at 65.6) return to its own start
            body = os.path.join(tmp, 'body.txt'); open(body, 'w').write('```json\n' + json.dumps({'path': wp, 'source': 'pramod-medhi', 'starts': {'QKf_JPbN6Lw': {'aarti.pad1': [30.6, end]}}}) + '\n```\n')
            r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools/audio/apply_owner_timing.py'), body], env=env, capture_output=True, text=True); out.append((r.returncode, r.stdout.strip().split('\n')[-1]))
        after = json.load(open(os.path.join(tmp, 'library', wp, 'audio', 'pramod-medhi.json')))['at']; shutil.rmtree(tmp)
        check('timing: a second send that lets a moved verse go back to its own start is applied by the workflow', r0.returncode == 0 and out[0][0] == 0 and out[1][0] == 0 and after['aarti.pad3'] == raw['aarti.pad3'] and 60 < raw['aarti.pad3'][1] < 100, (r0.stderr[-200:], out, raw.get('aarti.pad3'), after.get('aarti.pad3')))
        # ---- app review, 2026-10-20: five bugs of flow and navigation, each reproduced before the fix ----
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
        # a meaning switched in Settings lights the reader's capsule when you come back
        await ev("(async () => { await openWork('ramraksha', true); show('home'); openReader('k', 0); S.settings.layers.h = false; S.settings.layers.e = true; save(); syncLayers(); show('settings'); })()"); await pg.wait_for_timeout(300)
        await ev("document.querySelector('#sh').click()"); await pg.wait_for_timeout(100); await pg.go_back(); await pg.wait_for_timeout(900)
        cap = await ev("[S.settings.layers.h, document.querySelector('#rLayers [data-l=h]').classList.contains('on'), CURVIEW]")
        check('a meaning switched in Settings shows lit in the reader’s capsule', cap == [True, True, 'reader'], cap)
        await ev("S.settings.layers.h = false; save(); syncLayers()")
        pin = await ev("""(async () => { S.timing.on = false; applyTiming(); await openWork('manas', true); show('home'); openReader('k', 30); await new Promise(r => setTimeout(r, 700));
            PL.on = true; PL.hold = 0; PL.cur = -1; setCur(34); await new Promise(r => setTimeout(r, 1200));
            const bar = document.querySelector('#reader .bar').getBoundingClientRect().bottom, v = document.getElementById('v34'), pv = v.previousElementSibling;
            const t = (pv && pv.classList.contains('vtype') ? pv : v).getBoundingClientRect().top, nx = document.getElementById('v35').getBoundingClientRect().top;
            PL.on = false; return [Math.round(t - bar), nx < innerHeight]; })()""")
        check('playing: the verse being recited is kept at the top, the next verse in view below it', 0 <= pin[0] <= 12 and pin[1], pin)
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
        check('☰ › Take the tour starts the tour; Settings no longer has it', tm == [True, False], tm)
        ft = await ev("""(async () => { await openWork('manas', true); show('home'); openReader('k', 30); await new Promise(r => setTimeout(r, 500));
            document.querySelector('#rMid').click(); await new Promise(r => setTimeout(r, 300)); const ok = document.querySelector('#sheet').classList.contains('on') && !!document.querySelector('#sheetBody .secs [data-to]'); closeSheet(); return ok; })()""")
        check('reader: tapping the footer opens the section picker', ft)
        bd = await ev("""(async () => { const me = ME(); me.bm[KEY(IT[40].id)] = 1; me.bm[KEY(IT[41].id)] = 2; save(); show('bookmarks'); await new Promise(r => setTimeout(r, 300));
            const n0 = document.querySelectorAll('#bmBody [data-del]').length; document.querySelector('#bmBody [data-del="40"]').click(); await new Promise(r => setTimeout(r, 300));
            const r = [n0, document.querySelectorAll('#bmBody [data-del]').length, !me.bm[KEY(IT[40].id)], !!me.bm[KEY(IT[41].id)]]; delete me.bm[KEY(IT[41].id)]; save(); return r; })()""")
        check('bookmarks: each bookmark can be removed on its own', bd == [2, 1, True, True], bd)
        check('no script errors anywhere', not errs, '; '.join(errs[:3]))
        await b.close()
    print(f'\n{sum(results)}/{len(results)} checks passed')
    sys.exit(0 if all(results) else 'UX TEST FAILED')
asyncio.run(main())
