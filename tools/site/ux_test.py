"""End-to-end test of navigation and the reading experience, at phone size, for every work on the shelf.

Usage:  python3 tools/site/ux_test.py [--shots DIR] [--shard K/N] [--works a,b]   (serves the repository root on a free port)
        python3 tools/site/check.py runs it as shards side by side, with every other check
        --works a,b runs only these works' per-work checks (python3 tools/site/check.py --works a,b)
Needs:  pip install playwright (Chromium; set CHROMIUM=/path/to/chrome if it is not found)

Each check prints PASS/FAIL with what it saw; the run fails if any check fails or the page logs a script error.
--shots saves a screenshot after each step, for a person to look at.
"""
import asyncio, functools, http.server, json, os, random, re, shutil, socketserver, subprocess, sys, tempfile, threading
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'site')); import split_fixture   # a work loaded by part (the Kaṭha, exported again with "load": "parts")
sys.path.insert(0, os.path.join(ROOT, 'tools', 'audio')); import order as ORDER   # the order rule, shared with make_timings.py
from playwright.async_api import async_playwright

SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
# --shard K/N: the per-work checks (one work at a time, as a reader goes through it; most of the run) are shared among N
# processes run side by side: shard 0 runs every other check and none of them, shards 1 … N-1 a share of the works each
SHARD, NSHARD = (map(int, sys.argv[sys.argv.index('--shard') + 1].split('/')) if '--shard' in sys.argv else (0, 1))
# --works a,b: the per-work checks of these works only (a change to their data); the checks of the whole app are left out
ONLY = set(sys.argv[sys.argv.index('--works') + 1].split(',')) if '--works' in sys.argv else None
# the checks of the whole app (shard 0) take about as long as 15% of all the per-work checks (measured: 654 s against
# 1,350–1,580 s for each of three shards of the works), so shard 0 takes a share of the works too, after them
APP_SHARE = 0.15
def mine(works):
    """This shard's share of the works, balanced by size: the biggest first, each to the shard with the least so far (a
    work's checks take longer the more parts and verses it has: the Valmiki's alone are a shard's worth); shard 0 starts
    with the checks of the whole app as its load (APP_SHARE)."""
    if ONLY is not None:
        works = [w for w in works if w[0]['work'] in ONLY]
        if NSHARD == 1: return works
    if NSHARD == 1: return works
    size = lambda w: 1 + os.path.getsize(os.path.join(ROOT, 'library', w[0]['path'], 'work.json')) / 2e6   # a work's checks: ~15 s, and more with its size (the Valmiki's 11 MB: as 6 small works)
    if ONLY is not None:   # --works: the app-wide checks are left out, so the works are shared among shards 1 … N-1 only
        if not SHARD: return []
        load, first = [0.0] * NSHARD, 1; load[0] = float('inf')
    else: load, first = [APP_SHARE * sum(size(w) for w in works)] + [0.0] * (NSHARD - 1), 0
    out = []
    for k in sorted(range(len(works)), key=lambda k: -size(works[k])):
        s = min(range(first, NSHARD), key=lambda j: load[j]); load[s] += size(works[k])
        if s == SHARD: out.append(k)
    return [works[k] for k in sorted(out)]
results = []

def YT_ERR(e):
    """An error thrown inside YouTube's own player scripts, not the app's (its stack names only YouTube's files)."""
    st = getattr(e, 'stack', '') or ''
    return ('youtube.com' in st or 'ytimg.com' in st) and '/app/app.js' not in st

def check(name, ok, seen=''):
    results.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + name + (f'  [{seen}]' if seen != '' else ''), flush=True)

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    s = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT)); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

def leaves(nodes, trail=()):
    for n in nodes:
        if 'work' in n: yield n, trail
        else: yield from leaves(n['children'], trail + (n['id'],))

DUP_IDS = "(() => { const c = {}; for (const e of document.querySelectorAll('[id]')) c[e.id] = (c[e.id] || 0) + 1; return Object.keys(c).filter(k => c[k] > 1); })()"   # docs/PLAYBOOK.md §10: an element id is used once
async def main():
    srv = serve(); url = f'http://127.0.0.1:{srv.server_address[1]}/'
    shelf = json.load(open(os.path.join(ROOT, 'library', 'index.json')))
    async with async_playwright() as p:
        kw = {'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}
        b = await p.chromium.launch(**kw)
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); errs = []
        await pg.add_init_script('window.__SALUTE_MS = 0')   # the 1.5 s greeting is tested on its own
        pg.on('pageerror', lambda e: None if YT_ERR(e) else errs.append(str(e)))   # YouTube's own script errors (the real player on the CI runner) are not the app's
        n = 0
        async def shot(tag):
            nonlocal n
            if SHOTS: n += 1; os.makedirs(SHOTS, exist_ok=True); await pg.screenshot(path=os.path.join(SHOTS, f'{n:02d}-{tag}.png'))
        ev = pg.evaluate
        async def until(js, most=15000):
            """Wait for what the next step needs to see, never a fixed time: a slow runner only takes longer (and a check
            that follows still fails if it never comes); then a frame for the page to settle."""
            try: await pg.wait_for_function(js, timeout=most)
            except Exception: pass
            await pg.wait_for_timeout(60)
        # every check of one work, as a reader goes through it; with --shard K/N the works are shared among N processes (tools/site/check.py)
        async def per_work(leaf, trail):
            wid = leaf['work']; tag = wid
            # walk the shelf exactly as a reader would: tap down the path, two levels at a time
            await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(200)
            path = await ev(f"(() => {{ let r = null; (function w(ns, at){{ ns.forEach(n => n.work === {json.dumps(leaf['work'])} ? r = at.concat(n.id) : w(n.children || [], at.concat(n.id))); }})(LIB, []); return r; }})()")   # its place in the library the reader sees
            k = 0; opened = False
            while k < len(path):
                key = '/'.join(path[k:k + 2]) if k + 1 < len(path) else path[k]
                btn = await pg.query_selector(f'#libList [data-node="{key}"]')
                if not btn: key = path[k]; btn = await pg.query_selector(f'#libList [data-node="{key}"]')
                if not btn: break
                await btn.click()
                if k + key.count('/') + 1 >= len(path): await until(f"document.querySelector('#home').classList.contains('on') && W && W.id === {json.dumps(wid)} && !!document.querySelector('#orgList [data-open]')")
                else: await pg.wait_for_timeout(300)
                k += key.count('/') + 1
                if k >= len(path): opened = True
            on_home = await ev("document.querySelector('#home').classList.contains('on') && W && W.id")
            check(f'{tag}: reached from the library by tapping its shelves', opened and on_home == wid, ' › '.join(path))
            if on_home != wid: await ev(f"openWork({json.dumps(wid)})"); await until("!!document.querySelector('#orgList [data-open]')")
            await shot(f'{tag}-home')
            title = await ev("document.querySelector('#hTitle').textContent")
            check(f'{tag}: home shows the title', title.strip() != '', title)
            single = await ev("PARTS.length === 1")
            seg_hidden = await ev("document.querySelector('#orgSeg').hidden")
            check(f'{tag}: plan switch only when there are plans or other views', seg_hidden == (await ev("PLANS.length === 0 && VIEWS.length === 0")))
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
                # each day is named by the plan's own word (विश्राम / Vishram, दिन / Day), and a day read as one part whole says the part once
                days = await ev(f"[...document.querySelectorAll('#orgList [data-mark]')].map(b => b.closest('li').querySelector('.ti').textContent)")
                unit = await ev(f"TT(PLAN[{json.dumps(pid)}].unit)")
                twice = await ev("[...document.querySelectorAll('#orgList .ds')].map(d => d.innerHTML.split('<br>')).flat().filter(l => { const m = /^(.+?): (.+)$/.exec(l); return m && m[1] === m[2]; })")
                check(f'{tag}: plan {pid} names each day “{unit} N” and never a part twice', len(days) == await ev(f"PLAN[{json.dumps(pid)}].n") and all(unit in d for d in days) and not twice, f'{days[:2]} {twice[:2]}')
            # a plan's page that is a work of its own (the Mānas's āratī: vidhi.open) opens that work's reading, with its recording; ‹ comes back
            opens = await ev("Object.entries((W.vidhi || {}).open || {})")
            if opens:
                me, pid = await ev("W.id"), await ev("PLANS.find(p => (p.after || []).concat(p.before || []).length).id")
                for pgk, wk in opens:
                    await ev(f"WS().org = {json.dumps(pid)}; renderHome()"); await pg.wait_for_timeout(200)
                    await pg.click(f'#orgList [data-page="{pgk}"]', timeout=3000); await pg.wait_for_timeout(2500)
                    op = await ev("[W.id, CURVIEW, document.querySelectorAll('#pages .verse').length, document.querySelectorAll('#pages .vplay').length]")
                    await pg.click('#rBack', timeout=3000); await pg.wait_for_timeout(2500)
                    op.append(await ev("[W.id, CURVIEW, homeOrg()]"))
                    check(f'{tag}: the plan\'s {pgk} page opens the work {wk} with ▶ on its verses, and ‹ returns to the plan', op[:2] == [wk, 'reader'] and op[2] > 0 and op[3] == op[2] and op[4] == [me, 'home', pid], op)
                    # its row has ▶ with its time, as a day has; the end of the last day offers it as the next button, with its time, and ‹ comes back to that day
                    await ev(f"WS().org = {json.dumps(pid)}; renderHome()"); await pg.wait_for_timeout(1200)
                    row = await ev(f"[!!document.querySelector('#orgList [data-ppg=\"{pgk}\"]'), (document.querySelector('#orgList [data-pdur=\"{pgk}\"]') || {{}}).textContent]")
                    await ev(f"openReader({json.dumps(pid)}, PLAN[{json.dumps(pid)}].ends[PLAN[{json.dumps(pid)}].n - 1])"); await pg.wait_for_timeout(1500)
                    await pg.locator(f'#endB [data-after="{pgk}"]').scroll_into_view_if_needed(timeout=3000); await pg.wait_for_timeout(300)
                    end = await ev(f"(document.querySelector('#endB [data-pdur=\"{pgk}\"]') || {{}}).textContent")
                    await pg.click(f'#endB [data-after="{pgk}"]', timeout=3000); await pg.wait_for_timeout(2500)
                    went = await ev("[W.id, CURVIEW]"); await pg.click('#rBack', timeout=3000); await pg.wait_for_timeout(2500)
                    went.append(await ev("[W.id, CURVIEW, R.org]"))
                    check(f'{tag}: the plan\'s {pgk} row has ▶ with its time, and the end of the last day opens it as the next button; ‹ returns to that day',
                          row[0] and bool(re.search(r'\d', row[1] or '')) and (end or '').startswith('▶ ') and went[:2] == [wk, 'reader'] and went[2] == [me, 'reader', pid], [row, end, went])
            if await ev("PLANS.length"): await ev("WS().org = 'k'; renderHome()"); await pg.wait_for_timeout(200)
            # timing review: drafts only with ☰ › More settings › Audio timing on; a start and an end set by ear take effect at once
            drafts = await ev("(W.sources.au || []).filter(s => s.draft).map(s => s.id)")
            if drafts:
                check(f'{tag}: a draft recording is not played to readers', (await ev("SRC.au ? SRC.au.meta.id : null")) not in drafts)
            await ev("S.timing.on = true; applyTiming()"); await ev("loadSources()"); await pg.wait_for_timeout(600)
            if await ev("!!SRC.au && !!(AUT[0] || []).length"):   # a draft not yet timed (still being transcribed) has no verse to set
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
                    # the light follows a predicted start too: it moves on from the verse you marked when the next one's guessed start comes
                    await ev("S.timing.fix[tkey()] = {}; save(); buildAudio()")
                    va, sa = await ev(f"[AUT[0][{g}][0], AUT[0][{g}][1]]"); vb, sb = await ev(f"[AUT[0][{g} + 1][0], AUT[0][{g} + 1][1]]")
                    await ev(f"PL.on = true; PL.t = 0; PL.end = null; ytOK = true; ytInfo.t = {sa} + 0.2; setTime({va}, 1, {sa})")
                    await ev(f"ytInfo.t = {sb} + 1; tick()")
                    held = await ev("PL.cur")
                    await ev(f"setTime({vb}, 1, {sb} + 0.8)")
                    check(f'{tag}: the light moves to the next verse at its predicted start, and marking it keeps it there', held == vb and await ev("PL.cur") == vb, [held, va, await ev("PL.cur"), vb])
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
                check(f'{tag}: a helper file loads as marks to check, not sent', await ev(f"fromOf({json.dumps(jid)})") == 'Asha' and not await ev("Object.keys(pendingStarts()).length") and await ev(f"(() => {{ rerenderItem({j}); const v = document.getElementById('v{j}'); return !v || !!v.querySelector('.vundo [data-a=tok]') && !v.querySelector('[data-a=tundo]'); }})()"), await ev("pendingStarts()"))
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
            await (await pg.query_selector('#orgList [data-open]')).click(); await until("document.querySelector('#reader').classList.contains('on') && document.querySelectorAll('#reader .verse').length > 0 && wReady"); await pg.wait_for_timeout(300); await shot(f'{tag}-reader')
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
            # a pair chosen in another work never names a language this work lacks (a reader's ਪੰ · हिं from the Sukhmani Sahib hid the Granth's English)
            badpair = await ev("""(() => { const old = S.settings.pair, ks = workKinds(), bad = [];
              for (const p of ['pa,hi', 'pa,en', 'hi,en', 'sa,hi']) { S.settings.pair = p; const c = capKinds(); if (ks.length >= 2 && c.some(k => !ks.includes(k))) bad.push(p + '→' + c); }
              S.settings.pair = old; return bad; })()""")
            check(f'{tag}: the meaning pair names only languages the work has', not badpair, badpair)
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
                # the bookmark names its verse by the player's number (docs/PLAYBOOK.md §3: one number per verse), as Resume does
                bw = await ev("(() => { const r = document.querySelector('#bmBody .bmrow .res'); if (!r) return null; const i = +r.dataset.i; return [r.querySelector('.where').textContent, playLabel(i)]; })()")
                check(f'{tag}: a bookmark is named by the number the player shows', bw and bw[0].endswith(bw[1]), bw)
                await ev("history.back()"); await pg.wait_for_timeout(500)
                await ev("Object.keys(ME().bm).filter(k => k.startsWith(W.id + ':')).forEach(k => delete ME().bm[k]); save()")
            # search for a word of the first verse
            word = await ev("cleanWord((IT[0].v[0].split(/\\s+/).find(x => cleanWord(x).length > 2)) || '')")
            if word:
                await ev("openSearch('text')"); await pg.fill('#q', word); await until("document.querySelectorAll('#sRes .res').length > 0"); await pg.wait_for_timeout(300); await shot(f'{tag}-search')
                hits = await ev("document.querySelectorAll('#sRes .res').length")
                check(f'{tag}: search finds a word of its first verse', hits > 0, f'{word}: {hits}')
                if hits:
                    # a locator, found again at the tap: a work loaded by part draws its results again as each part's meanings come
                    await pg.locator('#sRes .res').first.click(); await until("document.querySelector('#reader').classList.contains('on')"); await pg.wait_for_timeout(300)
                    check(f'{tag}: a search result opens the reader', await ev("document.querySelector('#reader').classList.contains('on')"))
            # English interface
            await ev("S.settings.ui = 'en'; S.settings.layers.e = true; S.settings.layers.h = false; applyLang(); refreshReader()"); await pg.wait_for_timeout(500)
            en_hdr = await ev("document.querySelector('#rMid').innerText")
            check(f'{tag}: English interface works in the reader', bool(en_hdr.strip()), en_hdr)
            # recitation mode is the fourth button of the reader's capsule: it hides the meanings; a meaning turned on ends it
            await ev("S.settings.recite = false; S.settings.layers.h = true; S.settings.layers.e = true; if (workKinds().length > 2) S.settings.pair = 'pa,hi'; save(); applyRecite(); syncLayers(); refreshReader()")
            size0 = await ev("getComputedStyle(document.querySelector('.vtext')).fontSize")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(400)
            ok1 = await ev("S.settings.recite && !S.settings.layers.h && !S.settings.layers.e && !S.settings.layers.w && document.body.classList.contains('recite') && document.querySelector('#rLayers [data-l=r]').classList.contains('on')")
            size1 = await ev("getComputedStyle(document.querySelector('.vtext')).fontSize")
            check(f'{tag}: recitation mode keeps the reader’s letter size', size0 == size1, [size0, size1])
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(400)
            ok2 = await ev("!S.settings.recite && S.settings.layers.h && S.settings.layers.e")
            await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(300)
            if await ev("!!document.querySelector('#rLayers [data-l=h]:not([hidden])')"):   # a work without a Hindi meaning has no हिं to end it
                await (await pg.query_selector('#rLayers [data-l=h]')).click(); await pg.wait_for_timeout(300)
                ok3 = await ev("!S.settings.recite && S.settings.layers.h && !document.body.classList.contains('recite')")
            else:
                await (await pg.query_selector('#rLayers [data-l=r]')).click(); await pg.wait_for_timeout(300)
                ok3 = await ev("!S.settings.recite && !document.body.classList.contains('recite')")
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
            # the capsule's meaning switches: only languages the work has a meaning in, at most two (none for a work without meanings)
            sw = await ev("[[...document.querySelectorAll('#rLayers button')].slice(0, 2).filter(b => !b.hidden).map(b => b.dataset.l), workKinds().map(LK)]")
            check(f'{tag}: the reader shows a meaning switch only for a meaning the work has (at most two)', len(sw[0]) == min(2, len(sw[1])) and set(sw[0]) <= set(sw[1]), sw)
            # the work menu (☰) leads to bookmarks and settings
            await ev("show('home')"); await pg.wait_for_timeout(300)
            await (await pg.query_selector('#hMenu')).click(); await pg.wait_for_timeout(300)
            items = await ev("Array.from(document.querySelectorAll('#sheetBody [data-m], #sheetBody [data-tour], #sheetBody #mth, #sheetBody #mtm')).map(b => b.dataset.m || (b.dataset.tour != null ? 'tour' : b.id === 'mtm' ? 'timing' : 'dark-theme'))")
            check(f'{tag}: ☰ holds Bookmarks, Dark theme, Share the app, Take the tour and More settings — nothing else', items == ['bm', 'dark-theme', 'share', 'tour', 'set'] and not await ev("!!document.querySelector('#sheetBody [data-rate], #sheetBody [data-m=sec], #sheetBody #mtr')"), items)
            await ev("closeSheet()")
            # back goes home
            await ev("show('home')"); await pg.wait_for_timeout(300)
            check(f'{tag}: back to the work home', await ev("document.querySelector('#home').classList.contains('on')"))
            # one number for each verse (work.json → cite): what the player shows for a verse finds that verse in the work's search,
            # the number the reader prints at its end is the citation's own, and the reader's Go to / Back to pills say what the player says
            # (every verse, or a sample of about 4,000 in a work of more than 30,000: each look-up reads the whole work; the build checks every printed number)
            cit = await ev("""(async () => { const bad = [], miss = [], pr = [], step = IT.length > 30000 ? Math.floor(IT.length / 4000) : 1; setScope('text');
                for (let i = 0; i < IT.length; i += step){ const c = CIT(IT[i]); if (!vNum(c)) continue;
                  const wd = W.cite && W.cite.word && W.cite.word[IT[i].y], q = (wd ? TT(wd) : TYPE[IT[i].y]) + ' ' + c, Q = numQuery(q);
                  if (!Q){ bad.push(q); continue; } const hits = []; numHits(Q, hits); if (!hits.some(h => h[1] === i)) miss.push(IT[i].id + ' ← ' + q);
                  const t = IT[i].v.length && (IT[i].v[IT[i].v.length - 1].match(/॥([0-9०-९੦-੯]+)[^॥]*॥(?:[^॥]*॥)*\s*$/) || [])[1];
                  if (t && !['sec', 'none'].includes((W.cite || {}).mark)){ const last = CKEY(c).split('.').pop().replace(/[^0-9]/g, ''); if (CKEY(t) !== last) pr.push(IT[i].id + ': ॥' + t + '॥ but ' + c); } }
                return [bad.slice(0, 3), miss.slice(0, 3), pr.slice(0, 3)]; })()""")
            check(f'{tag}: every verse number the player shows finds that verse; the number at a verse\'s end is its citation\'s', cit == [[], [], []], cit)
            # a verse's place (bookmarks, notes, search results, the verse menu, the to-check list) ends with the player's label:
            # one number, never one built from the section and the verse's own number beside it ("Doha 106 · Chaupai 3")
            pl = await ev("""(() => { const bad = [], step = Math.max(1, Math.floor(IT.length / 4000));
                for (let i = 0; i < IT.length; i += step) if (!itemLabel(i).endsWith(playLabel(i))) bad.push(itemLabel(i) + ' ≠ ' + playLabel(i));
                return bad.slice(0, 3); })()""")
            check(f'{tag}: a verse\'s place says the number the player shows', pl == [], pl)
            # a verse's place, a section's label and a range never say one name twice ("Pauri 12 · Pauri 12", "Refrain – Refrain")
            rp = await ev("""(() => { const bad = [], dup = l => l.split(/ · | – /).some((x, k, a) => k && x === a[k - 1]), step = Math.max(1, Math.floor(IT.length / 4000));
                for (let i = 0; i < IT.length; i += step) if (dup(itemLabel(i))) bad.push(itemLabel(i));
                PAGES.forEach(p => { if (dup(secLabel(p))) bad.push(secLabel(p)); });
                return [...new Set(bad)].slice(0, 3); })()""")
            check(f'{tag}: no place or section label repeats a name', rp == [], rp)
            # search finds a verse by its bare number too ("10.2", the way a reader types what the player shows)
            bare = await ev("""(() => { setScope('text'); const miss = [], step = Math.max(1, Math.floor(IT.length / 3000));
                for (let i = 0; i < IT.length; i += step){ const c = CIT(IT[i]); if (!vNum(c) || !/\\./.test(c)) continue; const Q = numQuery(c); const hits = []; if (Q) numHits(Q, hits); if (!hits.some(h => h[1] === i)) miss.push(IT[i].id + ' ← ' + c); }
                return miss.slice(0, 3); })()""")
            check(f'{tag}: a dotted number typed bare (10.2) finds its verse', bare == [], bare)
        await pg.goto(url); await pg.wait_for_timeout(2500)
        if SHARD or ONLY is not None:   # a shard (or --works) runs only its share of the per-work checks, from a reader who has seen the tour
            await ev("(() => { S.settings.tour = 1; S.admin = 1; closeTour(); S.settings.layers.h = false; save(); })()"); await pg.reload(); await until("typeof LIB !== 'undefined' && !!LIB && LIB.length > 0 && !!document.querySelector('#libList [data-node]')", 20000)
            for leaf, trail in mine(list(leaves(shelf))): await per_work(leaf, trail)
            dups = await ev(DUP_IDS); check(f'shard {SHARD}/{NSHARD}: every element id is used once in the page', not dups, dups[:5])
            check(f'shard {SHARD}/{NSHARD}: no script errors', not errs, '; '.join(errs[:3]))
            await b.close(); print(f'\n{sum(results)}/{len(results)} checks passed'); sys.exit(0 if all(results) else 'UX TEST FAILED')
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
        await ev("tourSteps()[8].t().click()"); await pg.wait_for_timeout(1600)
        check('tour: search opens on this part, then the reader comes back for ▶', await ev("TOUR && TOUR.k") == 9 and await ev("CURVIEW") == 'reader', [await ev("TOUR && TOUR.k"), await ev("CURVIEW")])
        await ev("tourSteps()[9].t().click()"); await pg.wait_for_timeout(1200)
        check('tour: while the verse plays, the tour waits in the reader', await ev("TOUR && TOUR.waiting && CURVIEW === 'reader' && document.querySelector('#coach').hidden"))
        await pg.wait_for_timeout(5600)   # the verse plays for 5 seconds
        check('tour: after 5 s the library, with the parting message in the light card, the meanings back', await ev("!TOUR && !PL.on && CURVIEW === 'library' && libPath.length === 0 && !S.settings.recite && /Tour complete|परिचय पूरा/.test(document.querySelector('#toast').textContent) && document.querySelector('#toast').classList.contains('act')"))
        await ev("setSize(-2)")
        check('the tour is remembered', await ev("S.settings.tour === 1"))
        await ev("S.work = null; S.admin = 1; save()")   # the checks below are an admin's phone (the timing tools); a reader's is checked on its own
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
        # stepping into a work from the library: a quick open goes straight to the work's page, with no greeting screen
        await pg2.wait_for_function("document.querySelector('#loading').hidden", timeout=10000)
        quick = await pg2.evaluate("(async () => { W = null; let seen = false; const o = new MutationObserver(() => { if (!$('#loading').hidden) seen = true; }); o.observe($('#loading'), {attributes: true}); const t0 = performance.now(); await openWork('ramraksha'); o.disconnect(); return [seen, performance.now() - t0, CURVIEW]; })()")
        check('a quick open shows no greeting screen', not quick[0] and quick[1] < 400 and quick[2] == 'home', quick)
        # a slow open (the work takes 0.8 s to arrive): the greeting shows while it loads, and goes when it is here
        async def late(route): await asyncio.sleep(0.8); await route.continue_()
        await pg2.route('**/hinduism/stotra/shiva/bilvashtakam/work.json*', late)
        slow = await pg2.evaluate("(async () => { const p = openWork('bilvashtakam'); await new Promise(r => setTimeout(r, 500)); const r = [!$('#loading').hidden, $('#loading').textContent]; await p; r.push($('#loading').hidden, CURVIEW); return r; })()")
        await pg2.unroute('**/hinduism/stotra/shiva/bilvashtakam/work.json*')
        check('a slow open greets the work while it loads, then shows its page', slow[0] and slow[1] == await pg2.evaluate("saluteOf('bilvashtakam')") and slow[2] and slow[3] == 'home', slow)
        # opening the work that is already open: no greeting, no wait
        again = await pg2.evaluate("(async () => { const t0 = performance.now(); const p = openWork('bilvashtakam'); const t = document.querySelector('#loading').hidden; await p; return [t, performance.now() - t0]; })()")
        check('no greeting for the work already open', again[0] and again[1] < 200, again)
        # the work's page shows before the meanings and dictionaries arrive (here the Awadhi dictionary takes 1.5 s); the reader, opened
        # in the meantime, waits for them and then shows the verses with their meanings
        async def slowdict(route): await asyncio.sleep(1.5); await route.continue_()
        await pg2.route('**/glossary/awa.json*', slowdict)
        early = await pg2.evaluate("""(async () => { show('library'); const t0 = performance.now(); const p = openWork('sundarkand');
            while (!(CURVIEW === 'home' && W && W.id === 'sundarkand')) await new Promise(r => setTimeout(r, 20)); const t = performance.now() - t0, ready = wReady;
            openReader('k', PARTS[2].a); const before = CURVIEW; await p; await new Promise(r => setTimeout(r, 500));
            return [t, ready, before, CURVIEW, document.querySelectorAll('#rBody .verse').length, !!SRC.hi, !!GL.awa && Object.keys(GL.awa).length > 0]; })()""")
        await pg2.unroute('**/glossary/awa.json*')
        check("the work's page shows before its meanings and dictionaries; the reader waits for them", early[0] < 1200 and not early[1] and early[2] == 'home' and early[3] == 'reader' and early[4] > 0 and early[5] and early[6], early)
        # a refresh on a work's page, with the dictionaries slow: the cover stays (blank, no greeting) until the page is back;
        # the library underneath never shows in between
        await pg2.evaluate("(async () => { await openWork('sundarkand'); })()"); await pg2.wait_for_timeout(500)
        await pg2.route('**/glossary/awa.json*', slowdict)
        await pg2.reload(wait_until='commit'); seen = []
        for _ in range(60):
            try: seen.append(await pg2.evaluate("[typeof CURVIEW === 'string' ? CURVIEW : '', !!document.querySelector('#loading') && document.querySelector('#loading').hidden]"))
            except Exception: pass
            await pg2.wait_for_timeout(50)
        await pg2.unroute('**/glossary/awa.json*')
        flash = [x for x in seen if x[1] and x[0] != 'home']
        check('a refresh on a work page shows no library in between, and ends on the work page', not flash and seen and seen[-1] == ['home', True], [flash[:3], seen[-1:] if seen else None])
        # opened again (not a refresh): always the library, whatever screen was last used (readers asked for it)
        res = []
        for last in ('library', 'home', 'reader'):
            await pg2.evaluate(f"""(async () => {{ await openWork('sundarkand', true); if ('{last}' === 'library') show('library'); else if ('{last}' === 'reader') openReader('k', PARTS[2].a); else show('home'); }})()""")
            await pg2.wait_for_timeout(700); await pg2.goto(url); await pg2.wait_for_timeout(2500)
            res.append(await pg2.evaluate("CURVIEW"))
        check('opening the app again opens the library, whatever screen was last used', res == ['library', 'library', 'library'], res)
        await pg2.close()
        # a store app shows only its shelves (?app=<id>, library/apps.json)
        apps = json.load(open(os.path.join(ROOT, 'library', 'apps.json')))
        for aid, a in apps.items():
            if aid.startswith('_'): continue
            await pg.goto(url + '?app=' + aid); await pg.wait_for_timeout(2000)
            got = await ev("(() => { const r = []; (function w(ns, at){ ns.forEach(n => n.work ? r.push(n.path) : w(n.children || [], at.concat(n.id))); })(LIB, []); return r; })()")
            ok = got and all(any(g == s_ or g.startswith(s_ + '/') for s_ in a['shelves']) for g in got)
            check(f'app {aid}: only its shelves', ok, got)
        await pg.goto(url); await pg.wait_for_timeout(2000)

        # ---- library: one row per genre, no headings and no tradition; the Sikh gurbani among the Granthas ----
        await ev("libPath=[]; show('library')"); await pg.wait_for_timeout(300); await shot('library')
        heads = await ev("Array.from(document.querySelectorAll('#libList .lhead')).map(x => x.textContent)")
        genres = [g for t in shelf for g in t['children'] if 'shelf' not in g]
        rows = await ev("[...document.querySelectorAll('#libList button.it[data-node]')].map(b => b.dataset.node)")   # not the '+N' chip of a shelf with more works
        check('library: one row per genre, no headings, no tradition', not heads and rows == [g['id'] for g in genres], [heads, rows])
        sukh = await ev("(async () => { libPath = ['gurbani']; renderLibrary(); const n = document.querySelectorAll('#libList [data-node=\"guru-arjan-dev\"]').length; libPath = []; renderLibrary(); return [n, !!document.querySelector('#libList button.it[data-node=\"gurbani\"]')]; })()")
        check('library: Gurbani is a shelf of its own, the Sukhmani Sahib’s Guru on it', sukh == [1, True], sukh)
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

        if NSHARD == 1:
            for leaf, trail in mine(list(leaves(shelf))): await per_work(leaf, trail)

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
        await ev("show('library'); libPath = [LIB[0].id]; history.pushState(snap('library'), ''); renderLibrary()"); await pg.reload(); await pg.wait_for_timeout(2500)
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
        check('under the title: the author and parent text, no publisher', subs == {'manas': 'Goswami Tulsidas', 'sundarkand': 'Goswami Tulsidas · Shri Ramcharitmanas', 'ramraksha': 'Budha Kaushik Rishi'}, subs)
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
        # a fixed sample to check (checkOnly): a verse the order rule moves around a set time is not added to the list
        co = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
            const A = SRC.au, a = AUT[0], j = a.findIndex((x, n) => n > 2 && !A.ownSet.has(IT[x[0]].id) && !A.ownSet.has(IT[a[n + 1][0]].id)), i = a[j][0], nx = a[j + 1][0], keep = JSON.stringify(S.timing.fix[tkey()] || {});
            setTime(i, 1, a[j + 1][1] + 2); const mv = A.moved.has(IT[nx].id), was = toCheck(nx); A.checkOnly = true; const now = toCheck(nx);
            delete A.checkOnly; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [mv, was, !now]; })()""")
        check('timing: a fixed sample to check (checkOnly) does not grow when neighbours are moved', co == [True, True, True], co)
        # what you hear now wins: "Starts now" after a later verse's start set (and not sent) on this phone removes that start
        lw = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home');
            const A = SRC.au, a = AUT[0].slice().sort((x, y) => x[0] - y[0]), j = a.findIndex((x, n) => n > 2 && n + 2 < a.length && ![0, 1, 2].some(d => A.ownSet.has(IT[a[n + d][0]].id)));
            const i = a[j][0], nx = a[j + 1][0], keep = JSON.stringify(S.timing.fix[tkey()] || {});
            setTime(nx, 1, a[j][1] + 1); const r = setTime(i, 1, a[j][1] + 3), gone = !myStarts()[IT[nx].id], set = myStarts()[IT[i].id] && myStarts()[IT[i].id][1] === Math.round((a[j][1] + 3) * 10) / 10;
            S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [r !== false, gone, !!set]; })()""")
        check('timing: Starts now after a later verse\'s unsent start removes that start (what you hear wins)', lw == [True, True, True], lw)
        # a timing mark never scrolls the page while the lit verse is on screen
        ns = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('shri-rudram', true); await loadSources(); show('home'); { const A = SRC.au; A.at0 = Object.fromEntries(Object.entries(A.at0).map(([k, v]) => [k, v.slice(0, 2)])); A.own = []; A.ownSet = new Set(); A.checkSet = new Set(Object.keys(A.at0)); A.guess = []; A.guessSet = new Set(); A.raw = {}; buildAudio(); }
            const a = AUT[0], i = a[8][0]; openReader('k', i); await new Promise(r => setTimeout(r, 600));
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); PL.on = true; PL.t = 0; setCur(i); await new Promise(r => setTimeout(r, 900));
            const y0 = scrollY; ytInfo.t = a[8][1] + 1; setTime(i, 2, a[8][1] + 1); await new Promise(r => setTimeout(r, 900)); const y1 = scrollY;
            PL.on = false; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [y0, y1]; })()""")
        check('timing: marking a verse does not move the page', abs(ns[0] - ns[1]) < 2, ns)
        # while the first verse of a section is recited, the section's blue title stays above it, below the bar
        sh = await ev("""(async () => { await openWork('sundarkand', true); await loadSources(); show('home');
            const a = AUT[0], t = TOPICS.find(t => t.i > 20 && a.some(x => x[0] === t.i)), i = t.i; openReader('k', i - 6); await new Promise(r => setTimeout(r, 600));
            PL.on = true; PL.t = 0; PL.cur = null; $('#player').hidden = false; document.body.classList.add('playing'); setCur(i); await new Promise(r => setTimeout(r, 1200));
            const bar = $('#reader .bar').getBoundingClientRect().bottom, pl = $('#player').getBoundingClientRect().top, hd = document.getElementById('t' + i).getBoundingClientRect(), v = document.getElementById('v' + i).getBoundingClientRect();
            PL.on = false; stopAudio(); return [Math.round(hd.top - bar), Math.round(pl - v.top), i]; })()""")
        check('playing: a section’s blue title stays in view above its first verse', 0 <= sh[0] <= 30 and sh[1] > 0, sh)
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
                        rows, mv = ORDER.keep_order(sorted([[IDX[k], v[1], v[2] if len(v) > 2 and v[2] is not None else None] for k, v in base.items() if v[0] == ti and k in IDX]), lambda i: items[i][0] in ownset, lambda i: items[i][0] not in guess, lambda i: max(8, items[i][1]), tr.get('end', tr['dur']))
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
        # order between verses set by ear: a start at or past the next set start (unsent) removes that start, one at or before
        # the previous set start removes that one (what you hear now wins); between them it simply moves
        ordr = await ev("""(async () => { """ + T0 + """ const a = AUT[0], p = a[10][0], i = a[11][0], n = a[12][0], s0 = Math.round(a[10][1] * 10) / 10, has = q => !!myStarts()[IT[q].id];
            setTime(p, 1, s0); setTime(n, 1, s0 + 20); setTime(i, 1, s0 + 10); const r0 = [setTime(i, 1, s0 + 19), has(p), has(n)];
            setTime(i, 1, s0 + 20.5); const r1 = [has(p), has(n), Math.abs(SRC.au.at[IT[i].id][1] - (s0 + 20.5)) < 0.05];
            setTime(i, 1, s0 - 1); const r2 = [has(p), Math.abs(SRC.au.at[IT[i].id][1] - (s0 - 1)) < 0.05];
            """ + T1 + """ return [r0, r1, r2]; })()""")
        check('timing: a start out of order with an unsent set start removes that start; between them it moves', ordr == [[None, True, True], [True, False, True], [False, True]], ordr)
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
        # the light follows a start placed again by the order rule, as with Audio timing off, and then the next heard one
        mv = await ev("""(async () => { S.timing.on = true; applyTiming(); await openWork('manas', true); await loadSources(); show('home');
            const keep = JSON.stringify(S.timing.fix[tkey()] || {}); delete S.timing.fix[tkey()]; buildAudio(); const a = AUT[0]; let k = a.findIndex((x, q) => q > 5 && [0, 1, 2].every(d => !toCheck(a[q + d][0]) && !ownAt(IT[a[q + d][0]].id)) && a[q + 2][1] - a[q][1] > 8);   // three heard verses, none set by ear (the owner's sent times would be kept, not placed again) if (k < 0) return 'no run';
            const x = a[k][0], y = a[k + 1][0], z = a[k + 2][0], ys = a[k + 1][1], zs = a[k + 2][1]; setTime(x, 1, ys + 1);   // x starts after y's heard start: y is placed again
            const moved = toCheck(y) && SRC.au.at[IT[y].id][1] > ys; PL.on = true; PL.t = 0; PL.end = null; ytOK = true; PL.seekT = null; PL.cur = x; ytInfo.t = SRC.au.at[IT[y].id][1] + 0.3; tick(); const lit = PL.cur;
            ytInfo.t = zs + 0.3; tick(); const lit2 = PL.cur; PL.on = false; ytOK = false; S.timing.fix[tkey()] = JSON.parse(keep); S.timing.on = false; save(); applyTiming(); await loadSources(); return [moved, lit === y, lit2 === z]; })()""")
        check('timing: the light moves to a start that was placed again, as with Audio timing off, and follows the next heard one', mv == [True, True, True], mv)
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
        await ev("WS().last = {org: 'k', i: 999, id: 'gone.1'}; WS().pos = {k: 999}; save(); history.replaceState(Object.assign({}, history.state, {r: {org: 'k', id: 'gone.1'}}), '')")   # the place on this phone and in the page's history entry
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
        sp = await ev("""(async () => { W = null; await openWork('manas', true); const g = srcList('hi').find(s => /gitapress/.test(s.file)), hi = g && await getJSON(W.path + '/' + g.file), m = id => ((hi && hi.m[id]) || [''])[0];
            return [ID['bal.6.cau3-5'] == null, ['bal.6.cau3', 'bal.6.cau4', 'bal.6.cau5'].every(id => ID[id] != null), /चौपाई ५/.test(m('bal.6.cau3')), /३-५/.test(m('bal.6.cau5')), IT[ID['bal.6.cau5']].v.length]; })()""")
        check('Mānas: joint caupāīs are separate verses; Gita Press\'s joint meaning sits under the last', sp == [True, True, True, True, 1], sp)
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
        card = await ev("Promise.all([fetch('get/').then(r => r.text()), fetch('app/share-card.png').then(r => r.ok)]).then(([h, img]) => img && ['og:title', 'og:description', 'og:image'].every(k => h.includes('property=\"' + k + '\"')) && h.includes('share-card.png'))")
        dest = {}
        for ua, tag in (('Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/130 Mobile Safari/537.36', 'android'), ('Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148', 'iphone')):
            cx = await b.new_context(user_agent=ua); gp = await cx.new_page(); seen = []
            async def to_store(r): seen.append(r.request.url); await r.abort()   # the store itself is never opened
            await gp.route('https://play.google.com/**', to_store)
            try: await gp.goto(url + 'get/', wait_until='domcontentloaded'); await gp.wait_for_timeout(800)
            except Exception: pass
            dest[tag] = 'play' if seen and 'org.craadle.scriptures.hinduism' in seen[0] else 'site' if gp.url == url else gp.url
            await cx.close()
        check('<site>/get: a link card for chat apps (picture app/share-card.png); Android goes to the Play Store, an iPhone to the website', [card, dest.get('android'), dest.get('iphone')] == [True, 'play', 'site'], [card, dest])
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
        # "Read the bookmarked verses": only they, as the reader shows a verse (meanings, ▶), in the work's order; ‹ comes back
        last = await ev("(() => { const me = ME(), l = IT.length - 1; [40, 43, l].forEach((i, n) => me.bm[KEY(IT[i].id)] = n + 1); save(); show('bookmarks'); return l; })()"); await pg.wait_for_timeout(400)
        await pg.click('#bmRead', timeout=3000); await pg.wait_for_timeout(900)
        br = await ev("""[R.org, [...document.querySelectorAll('#pages .verse')].map(e => +e.dataset.i), !!document.querySelector('#v40 .vbm.bm-on'), !!document.querySelector('#v41'), document.querySelector('#rMid small').textContent]""")
        await pg.click('#rBack', timeout=3000); await pg.wait_for_timeout(500)
        br.append(await ev("CURVIEW")); await ev("(() => { const me = ME(); [40, 43, IT.length - 1].forEach(i => delete me.bm[KEY(IT[i].id)]); save(); })()")
        check('bookmarks: "Read the bookmarked verses" opens a reading of only them, in order, and ‹ returns to Bookmarks',
              br[0] == 'bm' and br[1][:2] == [40, 43] and set(br[1]) <= {40, 43, last} and br[2] and not br[3] and br[4] == 'Bookmarks' and br[5] == 'bookmarks', br)
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
            window.scrollBy(0, 1200); await new Promise(r => setTimeout(r, 400)); jumpPill(); r.push(!pill.hidden, pill.textContent.startsWith('↑') && (pill.textContent.includes('Go to') || pill.textContent.includes('पर जाएँ')) && pill.textContent.includes(playLabel(v1)));   // scrolled past it: the pill, pointing up
            pill.click(); await new Promise(r => setTimeout(r, 900)); jumpPill(); r.push(pill.hidden, inView(document.getElementById('v' + v1)));   // a tap: back to the verse, pill gone
            window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 400)); jumpPill(); r.push(!pill.hidden && pill.textContent.startsWith('↓'));   // scrolled before it: pointing down
            ytInfo.t = a[4][1] + 0.2; tick(); await new Promise(r => setTimeout(r, 1200)); jumpPill(); r.push(pill.hidden, PL.cur === v2);   // the next verse starts: the page follows, no pill
            stopAudio(); ytOK = false; r.push(pill.hidden); return r; })()""")
        check('playing: the “now playing” pill shows only while the lit verse is off screen, points the way, and brings it back on a tap', jp == [True, True, True, True, True, True, True, True, True], jp)
        # a verse timed line by line (kirtan, the audio file's "lines"): the light moves forward only — a line is lit from its first
        # singing until the next line starts, and stays lit while it is sung again (the owner: as an āratī's repeated first line)
        ln = await ev("""(async () => { await openWork('ramraksha', true); show('home'); S.timing.on = false; openReader('k', 0); await new Promise(r => setTimeout(r, 500));
            const a = AUT[0], v1 = a[3][0], s = a[3][1], d = a[4][1] - a[3][1], id = IT[v1].id;
            SRC.au.lines = {[id]: [[0, s, 0, s + 0.2 * d], [0, s + 0.4 * d, 1, null], [0, s + 0.7 * d, 0, null]]}; buildAudio();
            const sung = () => [...document.getElementById('v' + v1).querySelectorAll('.vtext p')].map(p => p.classList.contains('sung'));
            document.querySelector('#player').hidden = false; document.body.classList.add('playing');
            PL.on = true; PL.t = 0; PL.end = null; PL.cur = -1; ytOK = true; PL.seekT = null; ytInfo.t = s + 0.1 * d; tick(); await new Promise(r => setTimeout(r, 900));
            const r = []; r.push(PL.cur === v1, sung()[0] && !sung()[1]);                              // the first line lights
            ytInfo.t = s + 0.3 * d; tick(); r.push(sung()[0] && !sung()[1]);                           // after its singing, until the next starts: still lit
            ytInfo.t = s + 0.5 * d; tick(); r.push(sung()[1] && !sung()[0]);                           // the next line
            ytInfo.t = s + 0.8 * d; tick(); r.push(sung()[1] && !sung()[0]);                           // the first sung again: the light does not go back
            r.push(document.querySelector('#pLine').hidden);
            stopAudio(); ytOK = false; r.push(!sung().some(x => x));
            delete SRC.au.lines; buildAudio(); return r; })()""")
        check('playing a verse timed line by line: the light moves forward only, each line lit from its first singing until the next starts', ln == [True] * 7, ln)
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
        # ✓ Correct under a verse the library lists to check keeps its start as it is, as one set by ear: it leaves the list
        nx.append(await ev("(() => { const i = window.__nx[1], id = IT[i].id, t = SRC.au.at[id][1]; rerenderItem(i); const b = document.querySelector('#v' + i + ' .vundo [data-a=tok]'); if (!b) return 'no ✓ Correct in the corner'; b.click(); return [myStarts()[id] && myStarts()[id][1] === Math.round(t * 10) / 10, $('#pCheck').textContent === T('अगला ▸ ', 'Next ▸ ') + DEV(1)]; })()"))
        lay = await ev("(() => { const r = s => document.querySelector(s).getBoundingClientRect(), v = r('.ytw'), c = r('#pCheck'), t = r('#pStep'), x = r('#pClose'); return [c.left >= v.right, t.left >= v.right, x.bottom <= Math.min(c.top, t.top) + 1, Math.abs(c.top - t.top) < 2]; })()")
        check('timing: in the player bar ✕ sits on its own line above Next ▸ and ±step, which stay clear of the video', lay == [True, True, True, True], lay)
        RT = "(() => { const r = s => document.querySelector(s).getBoundingClientRect(), t = r('#pRate'), x = r('#pClose'), p = r('#pPlay'); return [t.right <= innerWidth, t.top < p.top ? 'top' : 'controls', Math.abs((t.top + t.bottom) / 2 - (x.top + x.bottom) / 2) < 4]; })()"
        rw = [await ev(RT)]; await pg.set_viewport_size({'width': 360, 'height': 844}); await pg.wait_for_timeout(300); rw.append(await ev(RT)); await pg.set_viewport_size({'width': 390, 'height': 844}); await pg.wait_for_timeout(300)
        check('player bar: 1× stays after ⏭ on a 390-px phone, and moves up beside ✕ on a 360-px one, never cut off', rw == [[True, 'controls', False], [True, 'top', True]], rw)
        await pg.click('#pNext'); await pg.wait_for_timeout(300); nx.append(await ev("window.__t1 > window.__t0"))   # ⏭ still goes on to the next verse
        nx.append(await ev("(() => { const ids = [...document.querySelectorAll('[id]')].map(e => e.id); return ids.length === new Set(ids).size; })()"))   # an id used twice took ⏭'s tap away once
        nx.append(await ev("(async () => { window.__h.forEach(([s, f, c]) => $(s).removeEventListener('click', f, c)); stopAudio(); ytOK = false; $('#player').hidden = true; const keep = window.__keep; " + T1 + " syncStep(); return $('#pCheck').hidden; })()"))
        check('timing: Next ▸ in the player bar (saffron) goes to the next verse to check and plays it, round to the first; the count drops when one is set or ✓ Correct; hidden when timing is off; no id is used twice; ⏭ still works', nx == [[True, True, True], [0, 1, 2], True, [True, True], True, True, True], nx)
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
            const row = [...document.querySelectorAll('#libList li')].find(li => li.querySelector('[data-node="veda"]')); const chips = [...row.querySelectorAll('[data-open-work]')].map(b => b.dataset.openWork), more = row.querySelector('.more');
            const g = [...document.querySelectorAll('#libList li')].find(li => li.querySelector('[data-node="granth"]')); const gchips = g.querySelectorAll('[data-open-work]').length;
            const a = [...document.querySelectorAll('#libList li')].find(li => li.querySelector('button.it[data-node="aarti"]')), lw = a.querySelector('.lworks'), cnt = a.querySelector('.it .cnt').textContent;
            const oneLine = getComputedStyle(lw).flexWrap === 'nowrap' && lw.scrollWidth > lw.clientWidth && document.documentElement.scrollWidth <= innerWidth, all = a.querySelector('.lworks .more');
            JSON.parse(keep); Object.entries(JSON.parse(keep)).forEach(([k, v]) => { if (S.w[k]) { if (v) S.w[k].at = v; else delete S.w[k].at; } }); save(); return [chips[0], chips.length, !!more, gchips, a.querySelectorAll('[data-open-work]').length, cnt, oneLine, !!all && all.dataset.node === 'aarti']; })()""")
        check('library: a shelf shows three works on one line that swipes, the one used most recently first, its count beside its name and “All N” at the end', sh2[0] == 'isha-upanishad' and sh2[1] <= 3 and sh2[3] <= 3 and sh2[4] == 3 and sh2[5].strip().isdigit() and int(sh2[5]) > 3 and sh2[6] and sh2[7], sh2)
        # one word for one thing: no "text" for a verse, no "listen/hear" for play, no "translation", no "Adjust audio timing"
        words = await ev("""(() => { const src = [...document.querySelectorAll('[data-en]')].map(e => e.dataset.en).join(' | '); return src; })()""")
        bad = [w for w in ('Listen', 'translation', 'Adjust audio timing', 'the text') if w in words]
        check('labels: the template uses the app\'s vocabulary', not bad, bad)
        # ⋮ order: Play from here · Write a note · Copy verse and meaning · Correct …
        order = await ev("(async () => { await openWork('manas', true); show('home'); openReader('k', 0); await new Promise(r => setTimeout(r, 300)); itemMenu(0); await new Promise(r => setTimeout(r, 200)); const r = [...document.querySelectorAll('#sheetBody [data-x]')].map(b => b.dataset.x); closeSheet(); return r; })()")
        check('⋮: Play from here · Write a note · Review audio timing · Copy verse and meaning, and no Improve (no editing in the app)', order[:4] == ['play', 'note', 'flag', 'copy'] and 'edit' not in order, order)
        # a tapped word's sheet: its language in brackets beside it; parts, Hindi, English, then root and grammar; no Edit or Add meaning
        ws = await ev("""(async () => { await openWork('valmiki-ramayana', true); await loadSources(); show('home'); openReader('k', ID['bala.1.1']); await new Promise(r => setTimeout(r, 1200));
            wordSheet('वाग्विदां', null, 'sa'); await new Promise(r => setTimeout(r, 300)); const b = $('#sheetBody');
            const r = [b.querySelector('h2 .wlang') && b.querySelector('h2 .wlang').textContent, $$('#sheetBody .kv dt').map(d => d.textContent), !b.querySelector('#gEdit'), !b.querySelector('p.small.muted:not(:has(b))')];
            closeSheet(); return r; })()""")
        check("a word's sheet: (Sanskrit) beside the word; Parts, Hindi, English, Root, Grammar; no Edit meaning", ws[0] in ('(Sanskrit)', '(संस्कृत)') and ws[1] in (['Parts', 'Hindi', 'English', 'Root', 'Grammar'], ['शब्द-खण्ड', 'हिंदी', 'English', 'मूल', 'व्याकरण']) and ws[2] and ws[3], ws)
        # line by line: a source with a piece per verse line shows each piece under its line; a source
        # without pieces, and a verse with no pieces at all, show the meaning whole after the verse
        lbl = await ev("""(async () => { await openWork('sukhmani-sahib', true); S.settings.layers = {h: true, e: true, w: false}; S.settings.pair = 'hi,en'; S.settings.recite = false; S.settings.lines = true; await loadSources();
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
            SRC.hi.p = {[it.id]: it.v.map((_, k) => 'HI' + k)}; S.settings.lines = false; d.innerHTML = verseHTML(i); const o = d.firstElementChild;
            const r4 = [o.querySelectorAll('.vline').length === 0, o.querySelectorAll('.layer.h').length === 1]; S.settings.lines = true;
            SRC.hi.p = keep.h; SRC.en.p = keep.e; delete S.settings.pair; return [...r1, ...r2, ...r3, ...r4]; })()""")
        check('meanings line by line (when chosen): each piece under its line; a source without pieces shows whole after the verse; none at all keeps the verse whole; not chosen, the meaning is whole', all(lbl), lbl)
        # line by line looks like pairs: no ॰ between a line and its meaning, a short dash between pairs, the full rule only at the end
        look = await ev("""(async () => { await openWork('sukhmani-sahib', true); S.settings.layers = {h: false, e: true, w: false}; S.settings.recite = false; S.settings.lines = true; delete S.settings.pair; await loadSources(); syncLayers();
            show('home'); openReader('k', IT.findIndex(x => x.id === 'a01.p3')); await new Promise(r => setTimeout(r, 500));
            const v = [...document.querySelectorAll('.verse')].find(e => e.querySelector('.vline')), ls = v.querySelectorAll('.vline'), m = v.querySelector('.vline + .layer');
            const dot = getComputedStyle(m, '::before').content, d1 = getComputedStyle(ls[0], '::before'), d2 = getComputedStyle(ls[1], '::before');
            return [dot === 'none', d1.content === 'none', d2.content === '""' && parseFloat(d2.width) < 80 && d2.borderTopStyle === 'solid', getComputedStyle(v).borderBottomStyle === 'solid']; })()""")
        check('line by line: each line sits on its meaning, a short dash parts the pairs, the verse ends with the full rule', all(look), look)
        # a verse taller than the screen: while it plays, the page turns inside it — the line being recited, with its meaning, comes up below the bar
        tall = await ev("""(async () => { stopAudio(); ytOK = false; await openWork('sukhmani-sahib', true); S.settings.layers = {h: false, e: true, w: false}; S.settings.recite = false; S.settings.lines = true; delete S.settings.pair; await loadSources(); syncLayers();
            const i = IT.findIndex(x => x.id === 'a01.p3'); show('home'); openReader('k', i); await new Promise(r => setTimeout(r, 500));
            PL.t = AUT.findIndex(a => a.some(x => x[0] === i)); const a = AUT[PL.t], m = a.findIndex(x => x[0] === i), s = a[m][1], e = endOf(i) ?? a[m + 1][1];
            PL.on = true; PL.cur = -1; $('#player').hidden = false; document.body.classList.add('playing'); setCur(i); await new Promise(r => setTimeout(r, 900));
            const y0 = scrollY; followLines(i, s + 0.02 * (e - s)); await new Promise(r => setTimeout(r, 700)); const y1 = scrollY;
            for (let n = 0; n < 5; n++){ followLines(i, e - 0.3); await new Promise(r => setTimeout(r, 300)); }   // as each tick does
            await new Promise(r => setTimeout(r, 500)); const y2 = scrollY, ls = document.getElementById('v' + i).querySelectorAll('.vline'), last = ls[ls.length - 1].getBoundingClientRect();
            const ok = [document.getElementById('v' + i).offsetHeight > innerHeight, y1 === y0, y2 > y0 + 100, last.top > $('#reader .bar').getBoundingClientRect().bottom && last.bottom < $('#player').getBoundingClientRect().top];
            window.scrollBy(0, -300); await new Promise(r => setTimeout(r, 300)); const y3 = scrollY; for (let n = 0; n < 3; n++){ followLines(i, e - 0.2); await new Promise(r => setTimeout(r, 300)); } ok.push(Math.abs(scrollY - y3) < 2);   // scrolled back by hand: left there
            stopAudio(); return ok; })()""")
        check('playing a verse taller than the screen: the page follows its lines, from the first to the last, once each', all(tall), tall)
        # a third meaning language: with a Punjabi source the capsule shows ਪੰ · En (English app) or ਪੰ · हिं
        # (Hindi app), always four places; Punjabi pieces sit under their lines; Sources lists it and "Meanings in the bar";
        # search finds it; recitation mode turns it off too
        pa = await ev("""(async () => { await openWork('sukhmani-sahib', true); show('home'); const S0 = JSON.stringify(S.settings);
            S.settings.ui = 'en'; S.settings.layers = {h: false, e: true, w: false, pa: true}; S.settings.recite = false; S.settings.lines = true; delete S.settings.pair;
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
        # footnotes and commentary: the book's footnotes show under their meaning, and ☰ › More settings › Footnotes (shown only for
        # a work with footnotes) hides them; a commentary is off until chosen in Sources (its picker shown only for a work that has
        # one), then sits after the meanings under its name, with its own footnotes
        cm = await ev("""(async () => { await openWork('shiv-aarti', true); show('settings'); await new Promise(r => setTimeout(r, 200));
            const none = [!document.querySelector('#setBody [data-src="cm"]'), !document.querySelector('#setBody #sfn')];
            await openWork('bhagavata-purana', true); show('home'); const S0 = JSON.stringify(S.settings), C0 = JSON.stringify(S.src[W.id] || {});
            S.settings.layers = {h: true, e: false, w: false}; S.settings.recite = false; delete S.settings.fn;
            const i = IT.findIndex(x => x.id === '10.9.14'); openReader('k', i); for (let n = 0; n < 40 && !(SRC.hi && SRC.hi.m['10.9.14']); n++) await new Promise(r => setTimeout(r, 150));
            const at = () => { const d = document.createElement('div'); d.innerHTML = verseHTML(i); return d.firstElementChild; };
            const fn1 = !!at().querySelector('.layer.h .fn'); S.settings.fn = false; const fn0 = !at().querySelector('.fn'); delete S.settings.fn;
            show('settings'); await new Promise(r => setTimeout(r, 200)); const sw = !!document.querySelector('#setBody #sfn') && !document.querySelector('#setBody [data-src="cm"]');
            W.sources.cm = [{id: 'sa-test', file: 'commentary/sa-test', title: {hi: 'परीक्षा टीका', en: 'Test commentary'}, lang: 'sa'}];
            show('settings'); await new Promise(r => setTimeout(r, 200)); const sel = document.querySelector('#setBody [data-src="cm"]');
            const pick = [!!sel, sel && sel.value === 'off', srcChoice('cm') === null, !at().querySelector('.layer.cm')];
            SRC.cm = {meta: W.sources.cm[0], id: 'sa-test', m: {'10.9.14': ['परीक्षा व्याख्या', ['टीकाकी टिप्पणी']]}, got: new Set(PARTS.map(P => P.k))};
            const v = at(), c = v.querySelector('.layer.cm'), last = [...v.children].filter(x => x.classList.contains('layer')).pop();
            const shown = [!!c, c && c.querySelector('.lbl').textContent === TT(W.sources.cm[0].title), c && c.textContent.includes('परीक्षा व्याख्या'), c && !!c.querySelector('.fn'), last === c];
            delete W.sources.cm; SRC.cm = null; S.settings = JSON.parse(S0); S.src[W.id] = JSON.parse(C0); save(); show('home');
            return {none, fn1, fn0, sw, pick, shown}; })()""")
        check('footnotes: under their meaning, hidden by ☰ › More settings › Footnotes, which only a work with footnotes shows', all(cm['none']) and cm['fn1'] and cm['fn0'] and cm['sw'], cm)
        check('commentary: its picker only for a work with one, Off until chosen; when chosen, after the meanings under its name, with its footnotes', all(cm['pick']) and all(cm['shown']), cm)
        # a footnote grows and shrinks with A−/A+, a step below its meaning, never larger
        fz = await ev("""(async () => { await openWork('bhagavata-purana', true); show('home'); const S0 = JSON.stringify(S.settings);
            S.settings.layers = {h: true, e: false, w: false}; S.settings.recite = false; delete S.settings.fn; syncLayers();
            const i = IT.findIndex(x => x.id === '10.9.14'); openReader('k', i); for (let n = 0; n < 40 && !document.querySelector('#v' + i + ' .fn'); n++) await new Promise(r => setTimeout(r, 150));
            const out = []; for (const sz of [16, 21, 34]){ S.settings.size = sz; applyTheme(); const f = document.querySelector('#v' + i + ' .fn'); out.push(f ? [parseFloat(getComputedStyle(f).fontSize), parseFloat(getComputedStyle(f.closest('.layer')).fontSize)] : null); }
            S.settings = JSON.parse(S0); applyTheme(); syncLayers(); save(); show('home'); return out; })()""")
        check('footnotes: sized with A−/A+, below their meaning at every size (13.5px at the default)', all(fz) and all(f < m for f, m in fz) and fz[0][0] < fz[1][0] < fz[2][0] and abs(fz[1][0] - 13.5) < .2, fz)
        # a Roman-letter search shows the verse itself; Play from here ends with the open section
        rs = await ev("(async () => { await openWork('manas', true); show('home'); openSearch('text'); document.querySelector('#q').value = 'asur chal chonip'; runSearch(); await new Promise(r => setTimeout(r, 300)); const r = document.querySelector('#sRes .res'); return r ? [r.querySelector('.where').textContent, r.querySelector('.snip').textContent.slice(0, 12)] : 'none'; })()")
        check('search: a verse found by Roman letters is shown as the verse', rs != 'none' and ('Verses' in rs[0] or 'मूल पाठ' in rs[0]) and 'रहे' in rs[1], rs)
        # search forgives spelling: Tulsīdās's forms, sound-alike letters, a missing word, spaces, Roman letters, Hindi letters for Gurmukhi
        fz = await ev("""(async () => { const top = async (w, q) => { await openWork(w, true); show('home'); await loadSources(); openSearch('text'); document.querySelector('#q').value = q; runSearch(); const r = document.querySelector('#sRes .res'); return r ? IT[+r.dataset.i].id : null; };
            const out = {};
            for (const [w, q] of [['manas', 'aise bachan'], ['manas', 'मंगल भवन अमंगल हारी'], ['manas', 'सियाराम मय सब जग जानी'], ['manas', 'राम काज कीन्हे बिनु मोहि कहाँ बिश्राम'], ['manas', 'बिनु पग चलै सुनै बिनु काना'],
                ['manas', 'जय राम रमा रमनं समनं'], ['manas', 'होई है वही जो राम रचि राखा'], ['manas', 'mangal bhavan amangal hari'], ['manas', 'Jahan lagi nath'], ['manas', 'tan dhan dham'], ['sukhmani-sahib', 'प्रभ कै सिमरनि गरभि न बसै']]) out[q] = await top(w, q);
            out.none = await top('manas', 'श्री रामचंद्र कृपालु भजु मन'); return out; })()""")
        want = {'aise bachan': 'ayodhya.67.do67', 'सियाराम मय सब जग जानी': 'bal.8.cau1', 'राम काज कीन्हे बिनु मोहि कहाँ बिश्राम': 'sundar.1.do1', 'बिनु पग चलै सुनै बिनु काना': 'bal.118.cau3',
                'जय राम रमा रमनं समनं': 'uttar.14.cha1', 'होई है वही जो राम रचि राखा': 'bal.52.cau4', 'Jahan lagi nath': 'ayodhya.65.cau2', 'tan dhan dham': 'ayodhya.65.cau2', 'प्रभ कै सिमरनि गरभि न बसै': 'a01.p2'}
        bad = {q: fz.get(q) for q in want if fz.get(q) != want[q]}
        check('search forgives spelling: the verse meant comes first', not bad and fz['मंगल भवन अमंगल हारी'] and fz['mangal bhavan amangal hari'] == fz['मंगल भवन अमंगल हारी'] and fz['none'] is None, bad or fz)
        # Sri Guru Granth Sahib: first letters, Gurbani's silent word endings, an Ang by its number, names that open what they name
        gg = await ev("""(async () => { await openWork('guru-granth-sahib', true); show('home');
            const run = async q => { openSearch('text'); document.querySelector('#q').value = q; runSearch(); await new Promise(r => setTimeout(r, 50)); const r = document.querySelector('#sRes .res'); return r ? IT[+r.dataset.i].id : null; };
            const jump = async q => { await run(q); return [...document.querySelectorAll('#sRes [data-jump]')].map(b => b.dataset.jump); };
            const s = await run('ਹਰ ਹਰ ਨਾਮ ਧਿਆਇ');
            return {fl: await run('ਸਨਕਪ'), flr: await run('snkp'), fls: await run('ਸ ਨ ਕ ਪ'), sihari: s && IT[ID[s]].v.join(' ').includes('ਹਰਿ ਹਰਿ ਨਾਮੁ ਧਿਆ'), ang: await run('ਅੰਗ ੧੪'), ang608: await run('608'),
              raag: await jump('ਆਸਾ'), kabir: await jump('kabir')}; })()""")
        check('Gurbani search: first letters (ਸਨਕਪ, snkp), a final sihari or aunkar left off, an Ang by its number, a raag or writer by name', gg['fl'] == gg['flr'] == gg['fls'] == 'mool' and gg['sihari'] and gg['ang'] == '14.1' and gg['ang608'] == '607.3' and 'part.7' in gg['raag'] and 'writer.bhagat-kabir' in gg['kabir'], gg)
        vw = await ev("""(async () => { await openWork('guru-granth-sahib', true); show('home'); WS().org = 'writer'; renderHome();
            const seg = [...document.querySelectorAll('#orgSeg button')].map(b => b.dataset.org), rows = document.querySelectorAll('#orgList [data-group]').length;
            document.querySelector('[data-group="writer.guru-tegh-bahadur"]').click(); await new Promise(r => setTimeout(r, 400));
            const G = RG(), only = () => [...document.querySelectorAll('#rBody .verse')].every(v => G.set.has(+v.dataset.i)), o1 = only();
            for (let n = 0; n < 6; n++){ window.scrollTo(0, document.body.scrollHeight); ensure(); await new Promise(r => setTimeout(r, 100)); }
            const o2 = only(), shown = document.querySelectorAll('#rBody .verse').length;
            openSearch('text', false, true); const chip = document.querySelector('#sIn .chip').textContent;
            show('home'); WS().org = 'ang'; S.settings.atOpen = {}; renderHome(); document.querySelector('[data-hund="601"]').click();
            [...document.querySelectorAll('#orgList [data-at]')][7].click(); await new Promise(r => setTimeout(r, 400));
            const ang = [R.org, !!document.getElementById('v' + ID['607.3'])]; WS().org = 'k'; S.settings.atOpen = {}; save();
            return {seg, rows, n: G.list.length, o1, o2, shown, chip, own: chip === GNAME('writer.guru-tegh-bahadur'), ang}; })()""")
        check('Sri Guru Granth Sahib: Part · Writer · Ang; a writer opens a reading of only their verses, search from it narrowed to them; Ang 608 opens its part at the verse it begins in', vw['seg'] == ['k', 'writer', 'ang'] and vw['rows'] == 34 and vw['o1'] and vw['o2'] and vw['shown'] > 20 and vw['own'] and vw['ang'] == ['k', True], vw)
        # an Ang that begins inside a verse begun on the page before (Ang 110 at ਸੇਵਾ ਸੁਰਤਿ, the third line of 109.3): it opens at that
        # line, and the footer names the page of the line at the top of the screen (110 there, 109 above it)
        ap = await ev("""(async () => { await openWork('guru-granth-sahib', true); show('home'); WS().org = 'ang'; S.settings.atOpen = {}; renderHome();
            document.querySelector('[data-hund="101"]').click(); [...document.querySelectorAll('#orgList [data-at]')][9].click(); await new Promise(r => setTimeout(r, 500));
            const bar = $('#reader .bar').getBoundingClientRect().bottom, p = lineEl(ID['109.3'], 2), top = p ? Math.round(p.getBoundingClientRect().top - bar) : null;
            updateHeader(); const f110 = $('#rMid .ml').textContent;
            window.scrollBy(0, -(lineEl(ID['109.3'], 2).getBoundingClientRect().top - lineEl(ID['109.3'], 0).getBoundingClientRect().top)); await new Promise(r => setTimeout(r, 300));
            updateHeader(); const f109 = $('#rMid .ml').textContent; WS().org = 'k'; S.settings.atOpen = {}; save();
            return {txt: p && p.textContent, top, f110, f109}; })()""")
        check('Sri Guru Granth Sahib: an Ang that begins inside a verse opens at its first line, and the footer names the page of the line at the top', ap['txt'] and ap['txt'].startswith('ਸੇਵਾ ਸੁਰਤਿ') and ap['top'] is not None and 0 <= ap['top'] <= 30 and ap['f110'].startswith('Ang 110') and ap['f109'].startswith('Ang 109'), ap)
        # “Review audio timing” in the verse's ⋮ menu: only that verse joins the to-check list (seen in timing mode); one blue dot on ▶
        # and in the menu shows it is marked; it leaves the list once its start is set
        fg = await ev("""(async () => { const k0 = JSON.stringify(S.timing.flags); await openWork('manas', true); await loadSources(); show('home');
            const i = IT.findIndex(x => x.id === 'bal.1.cau2'); openReader('k', i); await new Promise(r => setTimeout(r, 500));
            S.timing.on = true; const before = new Set(toCheckIds()); S.timing.on = false;
            itemMenu(i); await new Promise(r => setTimeout(r, 150)); const menu = [...document.querySelectorAll('#sheetBody [data-x]')].map(b => b.dataset.x);
            document.querySelector('#sheetBody [data-x=flag]').click(); await new Promise(r => setTimeout(r, 200));
            S.timing.on = true; const added = toCheckIds().filter(j => !before.has(j)); S.timing.on = false;
            itemMenu(i); await new Promise(r => setTimeout(r, 150)); const off = !!document.querySelector('#sheetBody [data-x=flag] .revd') && !!document.querySelector('#v' + i + ' .vplay .revd'); closeSheet();
            flagDone(IT[i].id); S.timing.on = true; const gone = !toCheckIds().includes(i) || before.has(i); S.timing.on = false;
            S.timing.flags = JSON.parse(k0); syncFlags(); save();
            return [menu.slice(0, 4).join() === 'play,note,flag,copy' && !menu.includes('edit'), added.length === 1 && added[0] === i, off, gone]; })()""")
        check('timing flag in ⋮: “Review audio timing” (third in ⋮) puts only that verse on the check list; one blue dot on ▶ and in ⋮ shows it; it leaves once set', all(fg), fg)
        # "Review timing" (Audio timing settings): off, no flag; on, while playing, a blue ⚑ bottom left of the verse recited and
        # its neighbours, outside timing mode; a tap fills it, marks the verse (on the settings' to-check list too, and ▶ needs no dot); timing mode hides it
        vf = await ev("""(async () => { const k0 = JSON.stringify(S.timing.flags), f0 = S.timing.flagsOn; await openWork('manas', true); await loadSources(); show('home');
            const i = IT.findIndex(x => x.id === 'bal.1.cau2'); S.timing.flagsOn = false; openReader('k', i); await new Promise(r => setTimeout(r, 400)); const none = !document.querySelector('#v' + i + ' .vflag');
            S.timing.flagsOn = true; refreshReader(); await new Promise(r => setTimeout(r, 400)); const d = j => getComputedStyle(document.querySelector('#v' + j + ' .vflag')).display, idle = d(i) === 'none';
            stopAudio(); ytOK = false; PL.on = true; PL.t = AUT.findIndex(a => a.some(x => x[0] === i)); PL.cur = -1; $('#player').hidden = false; document.body.classList.add('playing'); setCur(i); await new Promise(r => setTimeout(r, 400));
            const shown = [d(i - 1), d(i), d(i + 1), d(i + 2)].join() === 'flex,flex,flex,none' && !document.querySelector('#v' + i + ' .vflag .on');
            document.querySelector('#v' + (i + 1) + ' [data-a=tflag]').click(); await new Promise(r => setTimeout(r, 200)); stopAudio(); await new Promise(r => setTimeout(r, 100));
            const kept = d(i + 1) === 'flex' && d(i) === 'none'; document.querySelector('#v' + (i + 1) + ' [data-a=tflag]').click(); await new Promise(r => setTimeout(r, 100));
            document.querySelector('#v' + i + ' [data-a=tflag]').click(); await new Promise(r => setTimeout(r, 200));
            const filled = !!document.querySelector('#v' + i + ' .vflag .on') && !document.querySelector('#v' + i + ' .vplay .revd') && FLAGGED.has(IT[i].id);
            const listed = checkList().includes('data-go-i="' + i + '"');
            S.timing.on = true; refreshReader(); await new Promise(r => setTimeout(r, 300)); const hidden = !document.querySelector('#v' + i + ' .vflag'); S.timing.on = false;
            S.timing.flags = JSON.parse(k0); S.timing.flagsOn = f0; syncFlags(); save(); refreshReader();
            return [none, idle, shown, kept, filled, listed, hidden]; })()""")
        check('“Review timing”: while playing, a blue ⚑ on the verse recited and its neighbours; a tap fills it (shown after playing too) and lists the verse; hidden in timing mode', all(vf), vf)
        # every number is shown as 1 2 3, in Hindi too; a digit inside a word (ओ३म्) and what a textarea holds stay as written
        nm = await ev("""(async () => { const ui = S.settings.ui, ly = JSON.stringify(S.settings.layers); S.settings.ui = 'hi'; applyLang(); await openWork('manas', true); await loadSources(); S.settings.layers = {h: true, e: false, w: false}; syncLayers();
            show('home'); renderHome(); await new Promise(r => setTimeout(r, 300)); const home = document.querySelector('#home').innerText;
            openReader('k', IT.findIndex(x => x.id === 'bal.1.cau1')); await new Promise(r => setTimeout(r, 600)); const rd = document.querySelector('#rBody').innerText + document.querySelector('#reader .navbar').innerText;
            const ta = document.createElement('textarea'); ta.textContent = 'ओ३म् ॥१॥'; document.body.appendChild(ta); const d = document.createElement('div'); d.textContent = 'ओ३म् ॥१॥ १०८ ੧੨'; document.body.appendChild(d);
            await new Promise(r => setTimeout(r, 50)); const r = [!/[०-९]/.test(home), !/[०-९]/.test(rd), rd.includes('॥1॥'), ta.value === 'ओ३म् ॥१॥', d.textContent === 'ओ३म् ॥1॥ 108 12'];
            ta.remove(); d.remove(); S.settings.ui = ui; S.settings.layers = JSON.parse(ly); syncLayers(); applyLang(); return r; })()""")
        check('numbers are shown as 1 2 3 in Hindi too; ओ३म् and a textarea keep their digits', all(nm), nm)
        # each plan day's ▶ says how long it plays; the days add up to the recordings; the speed shortens it; the next-day button says it too
        du = await ev("""(async () => { await openWork('manas', true); await loadSources(); const o = PLANS[0].id; WS().org = o; show('home'); renderHome(); await new Promise(r => setTimeout(r, 300));
            const rows = document.querySelectorAll('#orgList .lplay.timed[data-pa] + .ldur').length;   /* the days (a page's ▶, the āratī's, is not a day) */ let sum = 0; for (let n = 1; n <= PLAN[o].n; n++){ const [a, b] = dayRange(o, n); sum += spanSecs(a, b); }
            const tr = AUT.reduce((s, L, t) => s + trEnd(SRC.au.tracks[t]) - L[0][1], 0), [a1, b1] = dayRange(o, 1), one = spanSecs(a1, b1);
            const r0 = S.settings.rate; S.settings.rate = 2; const two = spanSecs(a1, b1); S.settings.rate = r0;
            openReader(o, b1); await new Promise(r => setTimeout(r, 600)); const nx = document.querySelector('.endb [data-next] + .ndur'); WS().org = 'k';
            return [rows === PLAN[o].n, Math.abs(sum - tr) < 60, Math.abs(two * 2 - one) < 1, !!nx && nx.textContent.startsWith('▶')]; })()""")
        check('a plan day\'s ▶ shows how long it plays, at the speed set; so does the next day at a day\'s end', all(du), du)
        # the timing panel can draw while a recording's lists are still being made: it must not throw
        tc = await ev("""(async () => { await openWork('manas', true); await loadSources(); const A = SRC.au, on = S.timing.on, c = A.checkSet; S.timing.on = true; A.checkSet = undefined;
            let ok = true; try { timingHTML(); } catch (e) { ok = String(e); } A.checkSet = c; S.timing.on = on; return ok; })()""")
        check('the audio-timing panel draws before the recording\'s lists are ready', tc is True, tc)
        pf = await ev("(async () => { const P = PLANS[0]; const [a, b] = dayRange(P.id, 2); openReader(P.id, a + 3); await new Promise(r => setTimeout(r, 300)); itemMenu(a + 3); await new Promise(r => setTimeout(r, 200)); document.querySelector('#sheetBody [data-x=play]').click(); const r = [PL.end === b, PL.endMsg]; stopAudio(); return r; })()")
        check('Play from here ends with the open vishram, with its message', pf[0] and 'finished' in pf[1], pf)
        # ---- fixes found by an audit: each is driven the way a reader does it ----
        keep = await ev("JSON.stringify(S)")
        # a search result opened during a plan opens on that plan's day; Back returns to the day and verse that were open, and Continue too
        await ev("""(async () => { await openWork('manas', true); await loadSources(); WS().org = PLANS[PLANS.length - 1].id; show('home'); const o = WS().org, [a] = dayRange(o, 4); openReader(o, a + 2); await new Promise(r => setTimeout(r, 600)); window.__at = [o, IT[a + 2].id]; })()""")
        await ev("openSearch('text')"); await pg.fill('#q', 'सिया राम मय'); await pg.wait_for_timeout(800)
        await (await pg.query_selector('#sRes .res')).click(); await pg.wait_for_timeout(800)
        in_plan = await ev("R.org === window.__at[0]")
        await pg.go_back(); await pg.wait_for_timeout(600); await pg.go_back(); await pg.wait_for_timeout(1200)
        back_to = await ev("[CURVIEW, R.org === window.__at[0], R.n, IT[topVisibleItem()].id === window.__at[1] || Math.abs(topVisibleItem() - ID[window.__at[1]]) <= 1]")
        await pg.go_back(); await pg.wait_for_timeout(800)
        cont = await ev("[CURVIEW, WS().last.org === window.__at[0], WS().last.id]")
        check('a search result opens in the plan being read; Back returns to that day and verse, and so does Continue', in_plan and back_to[0] == 'reader' and back_to[1] and back_to[2] == 4 and back_to[3] and cont[0] == 'home' and cont[1], [in_plan, back_to, cont])
        # the headings above the first verse of a part (the part, the topic, ॥ चौपाई ॥) are below the top bar, not under it
        hd = await ev("""(async () => { await openWork('manas', true); openReader('k', PARTS[1].a); await new Promise(r => setTimeout(r, 600)); const bar = $('#reader .bar').getBoundingClientRect().bottom;
            return [...document.querySelectorAll('#rBody .part-h, #rBody .topic-h, #rBody .vtype')].filter(e => e.getBoundingClientRect().bottom > 0).slice(0, 3).map(e => Math.round(e.getBoundingClientRect().top - bar)); })()""")
        check('opening a part: its headings are in view below the top bar', bool(hd) and all(y >= 0 for y in hd), hd)
        # Back with a word's drawer open closes the drawer and stays in the reader
        await (await pg.query_selector('#rBody .verse .w')).click(); await pg.wait_for_timeout(400)
        opened = await ev("$('#sheet').classList.contains('on')")
        await pg.go_back(); await pg.wait_for_timeout(600)
        st = await ev("[$('#sheet').classList.contains('on'), CURVIEW]")
        await pg.go_back(); await pg.wait_for_timeout(800)
        check('Back with a drawer open closes it and stays on the page; Back again leaves', opened and st == [False, 'reader'] and await ev("CURVIEW") == 'home', [opened, st])
        # recitation mode: tapping हिं ends it and shows only the Hindi meaning (the interface follows: only Hindi → Hindi)
        rc = await ev("""(async () => { S.settings.ui = 'en'; S.settings.layers = {h: false, e: true, w: false}; S.settings.recite = false; save(); applyLang(); openReader('k', 5); await new Promise(r => setTimeout(r, 400));
            toggleRecite(); document.querySelector('#rLayers [data-l=h]').click(); await new Promise(r => setTimeout(r, 300)); const r = [S.settings.recite, S.settings.layers.h, S.settings.layers.e, S.settings.ui];
            S.settings.ui = 'en'; S.settings.layers = {h: true, e: true, w: false}; save(); applyLang(); syncLayers(); return r; })()""")
        check('recitation mode: tapping हिं ends it and shows only the meaning tapped', rc == [False, True, False, 'hi'], rc)
        # the Sukhmani Sahib: no number or space can be tapped as a word
        sk = await ev("""(async () => { await openWork('sukhmani-sahib', true); openReader('k', 0); await new Promise(r => setTimeout(r, 800));
            return [...document.querySelectorAll('#rBody .w')].filter(w => !cleanWord(w.dataset.w || w.textContent)).map(w => w.textContent); })()""")
        check('Sukhmani Sahib: “ਮਃ ੫ ॥” — the number is not a word', sk == [], sk)
        # library search forgives spelling, as verse search does
        await ev("libPath = []; show('library'); openSearch('lib')"); await pg.fill('#q', 'सुंदरकांड'); await pg.wait_for_timeout(600)
        ls = await ev("[...document.querySelectorAll('#sRes .snip')].map(x => x.textContent)")
        await pg.fill('#q', 'Sunderkand'); await pg.wait_for_timeout(600)
        ls2 = await ev("[...document.querySelectorAll('#sRes .snip')].map(x => x.textContent)")
        check('library search: “सुंदरकांड” and “Sunderkand” find the Sundarkand', any(t in x for x in ls for t in ('सुन्दरकाण्ड', 'Sundarkand')) and any(t in x for x in ls2 for t in ('सुन्दरकाण्ड', 'Sundarkand')), [ls[:3], ls2[:3]])
        # a shelf of many deity shelves is an index: every deity a chip with its count; a tap opens its shelf, one row of its works
        sv = await ev("""(async () => { libPath = ['aarti']; show('library'); await new Promise(r => setTimeout(r, 300));
            const chip = document.querySelector('#libList .lindex [data-node="rama"]'), n = document.querySelectorAll('#libList .lindex [data-node]').length, label = chip ? chip.textContent : '';
            const g = document.querySelector('#libList .lindex [data-node="ganesha"]'), short = g ? !/Bhagwan|भगवान/.test(g.textContent) : false;
            chip.click(); await new Promise(r => setTimeout(r, 300)); const works = document.querySelectorAll('#libList button.it[data-node]').length, path = libPath.join('/');
            const names = [...document.querySelectorAll('#libList .lindex [data-node] span:first-child')].map(x => x.textContent), sorted = names.join() === [...names].sort((a, b) => a.localeCompare(b, 'en')).join();
            libPath = []; show('library'); return [n, /\\d/.test(label), short, path, works, sorted]; })()""")
        check('Aarti is an index of deities with their counts (no honorific), A to Z; a tap opens that deity’s shelf with its works', sv[0] > 12 and sv[1] and sv[2] and sv[3] == 'aarti/rama' and sv[4] >= 2 and sv[5], sv)
        # searched from a shelf, the library looks on that shelf only, and finds a work by a line of a verse; a chip widens it
        ls3 = await ev("""(async () => { libPath = ['aarti']; show('library'); openSearch('lib'); const chips = [...document.querySelectorAll('#sIn .chip')].map(c => c.textContent);
            $('#q').value = 'jai ambe gauri'; await libSearch('jai ambe gauri'); const lines = [...document.querySelectorAll('#sRes [data-line]')].length;
            const wr = [...document.querySelectorAll('#sRes .res .where')].map(x => x.textContent);
            $('#q').value = 'hanuman'; await libSearch('hanuman'); const onShelf = [...document.querySelectorAll('#sRes [data-hit]')].every(b => !/Chalisa|चालीसा/.test(b.textContent));
            document.querySelector('#sIn [data-in="all"]').click(); await new Promise(r => setTimeout(r, 400)); await libSearch('hanuman'); const wide = [...document.querySelectorAll('#sRes [data-hit]')].some(b => /Chalisa|चालीसा/.test(b.textContent));
            history.back(); await new Promise(r => setTimeout(r, 300)); libPath = []; show('library'); return [chips, lines, wr.slice(0, 3), onShelf, wide]; })()""")
        check('library search from Aarti: only āratīs, a line finds its āratī, “Whole library” widens it', len(ls3[0]) == 2 and ls3[1] >= 1 and ls3[3] and ls3[4], ls3)
        # the timing tools are the admins' only: on another phone no Audio timing, no ⚑, no Review audio timing in ⋮
        ad = await ev("""(async () => { const a0 = S.admin, f0 = S.timing.flagsOn; S.admin = 0; S.timing.flagsOn = true; await openWork('sundarkand', true); await loadSources(); show('home');
            show('settings'); renderSettings(); const set = !!document.querySelector('#stm') || !!document.querySelector('#stf');
            openReader('k', ID['sundar.1.cau1'] || 5); await new Promise(r => setTimeout(r, 400)); const flag = !!document.querySelector('#rBody .vflag');
            itemMenu(ID['sundar.1.cau1'] || 5); await new Promise(r => setTimeout(r, 200)); const menu = !!document.querySelector('#sheetBody [data-x="flag"]'); closeSheet();
            S.admin = 1; show('settings'); renderSettings(); const set1 = !!document.querySelector('#stm');
            S.admin = a0; S.timing.flagsOn = f0; save(); libPath = []; show('library'); return [set, flag, menu, set1]; })()""")
        check('timing tools: hidden on a phone that is not an admin’s, shown on one that is', ad == [False, False, False, True], ad)
        pg4 = await ctx.new_page()
        await pg4.goto(url); await pg4.wait_for_timeout(2500); await pg4.evaluate("S.admin = 0; save()")
        await pg4.goto(url + '?admin=not-the-phrase'); await pg4.wait_for_timeout(2500)
        wrong = await pg4.evaluate("[!!S.admin, location.search.includes('admin')]")
        await pg4.evaluate("(async () => { await openWork('sundarkand', true); show('home'); openReader('k', 3); savePos(3); })()"); await pg4.wait_for_timeout(1500)
        await pg4.goto(url); await pg4.wait_for_timeout(3000)
        fresh = await pg4.evaluate("CURVIEW")
        await pg4.evaluate("S.admin = 1; save()"); await pg4.close()
        check('a wrong admin phrase does nothing and leaves the address bar; a fresh start opens the library, not the reader', wrong == [False, False] and fresh == 'library', [wrong, fresh])
        # offline, playing says it needs the internet (not that YouTube is not allowed)
        await ctx.set_offline(True)
        off = await ev("(() => { ytBlocked(); return $('#ytBox').innerText; })()")
        await ctx.set_offline(False)
        check('offline: playing says it needs the internet', 'internet' in off.lower() or 'इंटरनेट' in off, off)
        # YouTube slow to answer: a note with "Play on YouTube" lies over the player, which is kept (it may still start)
        slow = await ev("(() => { ytLoad('QjSpUgnEPLU', 0); ytBlocked(); const r = [!!$('#ytf'), $$('#ytBox .ytno').length, $('#ytBox').innerText]; ytNoteOff(); r.push($$('#ytBox .ytno').length); return r; })()")
        check('a slow YouTube start keeps the player under a note that can go', slow[0] and slow[1] == 1 and 'allowed' not in slow[2] and slow[3] == 0, slow)
        # a work that is a slice of a longer video (the Hanumān āratī at the end of the Sundarakāṇḍa's) plays from its own first verse, not the video's start
        ha = await ev("(async () => { await openWork('hanuman-aarti', true); show('home'); playRange('k', 0, IT.length - 1); const r = [Math.floor(PL.seekT), Math.floor(SRC.au.at[IT[0].id][1])]; stopAudio(); return r; })()")   # the time the app seeks to, whether it loads a player or reuses one (a live player reports 0 for a moment)
        check('the Hanumān āratī plays from the āratī, not from the start of the Sundarakāṇḍa', ha[0] == ha[1] and ha[0] > 6000, ha)
        # a track that is one song of a jukebox (recordings.json "start" / "end"): it plays from its first verse, stops at its own
        # end (never runs on into the next song) and its ▶ counts only its own length, not the rest of the video
        jb = await ev("""(async () => { await openWork('lakshmi-aarti', true); await loadSources(); show('home'); const tr = SRC.au.tracks[0], had = [tr.start, tr.end], s0 = SRC.au.at[IT[0].id][1];
            tr.start = Math.max(0, s0 - 5); tr.end = s0 + 600; const sp = Math.round(spanSecs(0, IT.length - 1) * RATE());
            playRange('k', 0, IT.length - 1); const seek = Math.floor(PL.seekT), ok0 = ytOK; ytOK = true; PL.seekT = null; ytInfo.t = tr.end + 0.5; ytInfo.at = performance.now(); tick(); const on = PL.on;
            ytOK = ok0; stopAudio(); ['start', 'end'].forEach((k, n) => { if (had[n] == null) delete tr[k]; else tr[k] = had[n]; }); return [seek, Math.floor(s0), sp, on]; })()""")
        check('a jukebox track plays from its first verse, stops at its own end and counts only its own length', jb[0] == jb[1] and 0 < jb[2] <= 601 and jb[3] is False, jb)
        # while playing, the work's page scrolls its last row clear of the player
        clr = await ev("""(async () => { await openWork('sundarkand', true); show('home'); playRange('k', 0, IT.length - 1); await new Promise(r => setTimeout(r, 400)); show('home'); await new Promise(r => setTimeout(r, 300));
            window.scrollTo(0, 1e6); await new Promise(r => setTimeout(r, 200)); const rows = $$('#orgList li').filter(x => x.offsetHeight); const r = [rows[rows.length - 1].getBoundingClientRect().bottom, $('#player').getBoundingClientRect().top]; stopAudio(); return r; })()""")
        check('while playing, the last section scrolls clear of the player', clr[0] <= clr[1], clr)
        # ⓘ About this work: under the title, with the work's language and length
        ab = await ev("(async () => { await openWork('ramraksha', true); show('home'); $('#hAbout').click(); await new Promise(r => setTimeout(r, 300)); const t = $('#sheetBody').innerText; closeSheet(); return t; })()")
        check('About this work shows the language and length', ('Sanskrit' in ab or 'संस्कृत' in ab) and ('verses' in ab or 'पद' in ab), ab[:120])
        # the work's page: About on the author's line; a plan shows its progress as a bar; a vishram's number marks it done and back
        wp = await ev("""(async () => { await openWork('manas', true); WS().org = 'M'; show('home'); await new Promise(r => setTimeout(r, 300));
            const d = DONE(ME(), 'M'), had = Object.assign({}, d); for (const k in d) delete d[k]; d[1] = 1; save(); renderHome();
            const inRow = !!$('.hsubrow #hAbout'), bar = $('.pdn') && $('.pdn').textContent, w0 = $('.pdbar span').style.width;
            const m = $('#orgList [data-mark="2"]'); m.click(); const on = !!DONE(ME(), 'M')[2], bar2 = $('.pdn').textContent, view = CURVIEW;
            $('#orgList [data-mark="2"]').click(); const off = !DONE(ME(), 'M')[2];
            for (const k in d) delete d[k]; Object.assign(d, had); save(); renderHome(); return [inRow, bar, w0, on, bar2, view, off]; })()""")
        check("work page: About beside the author, a progress bar, and a vishram's number marks it done and not done", wp[0] and wp[1] == '1 / 30' and wp[2] == '3%' and wp[3] and wp[4] == '2 / 30' and wp[5] == 'home' and wp[6], wp)
        # the reading anchor (Resume, Back to): calm reading moves it; a fling or a jump does not; reading the new place for a while
        # does (the old place is kept as "before that"); a recording playing 10 s makes the recited verse the anchor
        an = await ev("""(async () => { AN.manual = true; await openWork('sundarkand', true); const ws = WS(); delete ws.anchor; delete ws.prev; AN.cand = null; AN.calm = 0;
            const k = PARTS[2]; openReader('k', k.a); await new Promise(r => setTimeout(r, 300)); const tick = n => { for (let x = 0; x < n; x++) anchorTick(true); };
            const step = async dy => { window.scrollBy(0, dy); await new Promise(r => setTimeout(r, 30)); };
            tick(1); for (let x = 0; x < 6; x++){ await step(80); tick(1); }
            const read = anchorOf().i, readTop = topVisibleItem();
            await step(4 * innerHeight); tick(1); const afterFling = anchorOf().i, cand = !!AN.cand; await new Promise(r => setTimeout(r, 50)); backPill();
            const pill = !$('#rAnchor').hidden && $('#rAnchor').textContent.includes(playLabel(read)) && $('#rAnchor').getBoundingClientRect().bottom <= $('#reader .navbar').getBoundingClientRect().top;   // above the bottom bar, not over it
            $('#rAnchor').click(); await new Promise(r => setTimeout(r, 400)); const el = document.getElementById('v' + read).getBoundingClientRect(); const back = el.top < innerHeight && el.bottom > 0, pillGone = $('#rAnchor').hidden;
            openReader('k', PARTS[3].a); await new Promise(r => setTimeout(r, 300)); tick(5); const notYet = anchorOf().i === read;
            for (let x = 0; x < 22; x++){ await step(60); tick(1); } const moved = anchorOf().i >= PARTS[3].a, before = (WS().prev || [])[0] && ID[WS().prev[0].id] === read;
            show('home'); const resume = $('#cGo') && $('#cGo').textContent.includes('Resume'), named = $('#cGo').textContent.includes(playLabel(anchorOf().i)), earlier = !$('#cPrev') && $('#contAt').hidden;
            PL.on = true; PL.cur = -1; setCur(PARTS[4].a + 1); const byAudio = anchorOf().i === PARTS[4].a + 1; PL.on = false;   // pressing play is reading: at once
            openReader('k', PARTS[2].a); await new Promise(r => setTimeout(r, 200)); backPill(); const pillAgain = !$('#rAnchor').hidden;
            S.timing.on = true; backPill(); const noPillTiming = $('#rAnchor').hidden; S.timing.on = false;
            WS().anchor.t = Date.now() - 16 * 60e3; backPill(); const noPillStale = $('#rAnchor').hidden; WS().anchor.t = Date.now();
            AN.manual = false; return [read >= k.a, afterFling === read, cand, pill, back, pillGone, notYet, moved, before, resume, named, earlier, byAudio, pillAgain, noPillTiming, noPillStale]; })()""")
        check('the reading anchor: reading moves it, a fling does not; Back to returns; a new place takes over once read; Resume names it; playing moves it at once; no Back to in timing mode or after 15 minutes', all(an), an)
        # a number in a work's search finds by doha: "45" the doha 45 of each kand, "45.3" chaupai 3 under it, "दोहा ४५" too;
        # in a work without dohas, the verse of that number
        nums = await ev("""(async () => { const find = async (w, q) => { await openWork(w, true); setScope('text'); $('#q').value = q; runSearch(); await new Promise(r => setTimeout(r, 400)); return $$('#sRes .res').map(b => +b.dataset.i); };
            const m = await find('manas', '45'), mOk = m.length > 3 && m.every(i => ['do', 'so'].includes(IT[i].y) && IT[i].s === '45');
            const kands = new Set(m.map(i => IT[i].p)).size === m.length;
            const c = await find('manas', '45.3'), cOk = c.length > 3 && c.every(i => IT[i].y === 'cau' && IT[i].s === '45' && parseInt(IT[i].n) === 3);
            const h = await find('manas', 'दोहा ४५'), hOk = h.join() === m.join();
            const s = await find('sundarkand', '2'), sOk = s.length === 1 && IT[s[0]].id === 'sundar.2.do2';
            const r = await find('ramraksha', '5'), rOk = r.length >= 1 && r.every(i => parseInt(IT[i].n) === 5);
            return [mOk, kands, cOk, hOk, sOk, rOk, m.length, c.length]; })()""")
        check('a number in a work search finds that doha in each kand, N.M a chaupai under it; elsewhere the verse of that number', all(nums[:6]), nums)
        # the citation (tools/text/cite.py) is the one number: the Katha's 2.1.1 (its verse prints ॥१॥) in the player and search,
        # the Rudram's 11.17, a Manas chhand apart from the chaupai of the same number, a lettered doha, Bhaja Govindam's 13a, and the
        # Manas's śloka of a dohā's lettered group (Uttar ॥१२२ (ग)॥, after dohās 122क and 122ख)
        cn = await ev("""(async () => { const find = async (w, q) => { await openWork(w, true); setScope('text'); $('#q').value = q; runSearch(); await new Promise(r => setTimeout(r, 50)); return $$('#sRes .res').map(b => IT[+b.dataset.i].id); };
            const k = await find('katha-upanishad', '2.1.1'), kl = playLabel(ID['2.1.1']), kv = IT[ID['2.1.1']].v.slice(-1)[0].includes('॥१॥');
            const k2 = await find('katha-upanishad', '1.2'), r = await find('shri-rudram', '11.17'), rl = playLabel(ID['chamakam.a11.m17']);
            const s = await find('sukhmani-sahib', '3.5'), sl = playLabel(ID['a03.p5']);
            const c = await find('manas', 'chhand 10.1'), cl = playLabel(ID['bal.10.cha1']), ul = playLabel(ID['bal.10.cau1']), d = await find('manas', '3'), b = await find('bhaja-govindam', '13a');
            const g = await find('manas', '122ग'), gl = playLabel(ID['uttar.123.shloka122ग']), gs = IT[ID['uttar.123.shloka122ग']].s;
            return [k, kl, kv, k2, r, rl, s, sl, c, cl, ul, d.includes('bal.3.do3क') && d.includes('bal.3.do3ख'), b, g, gl, gs]; })()""")
        check('one number per verse: Katha 2.1.1, Rudram 11.17 and Sukhmani 3.5 in the player and search; a Manas chhand is not the chaupai of its number; 3 finds 3क, 3ख; the śloka ॥१२२ (ग)॥ is in Doha 122, cited 122ग, and 122ग finds it',
              cn == [['2.1.1'], 'Mantra 2.1.1', True, ['1.2.1'], ['chamakam.a11.m17'], 'Mantra 11.17', ['a03.p5'], 'Pauri 3.5', ['bal.10.cha1', 'kishkindha.10.cha1'], 'Chhand 10.1', 'Verse 10.1', True, ['sh13a'], ['uttar.123.shloka122ग'], 'Shloka 122ग', '122'], cn)
        # searched from the reader, a work's search stays in the part (or day, or the section of a one-part work) on screen; a chip widens it
        sin = await ev("""(async () => { const go = async q => { $('#q').value = q; runSearch(); await new Promise(r => setTimeout(r, 80)); return $$('#sRes .res').map(b => +b.dataset.i); };
            await openWork('manas', true); await loadSources(); show('home'); openReader('k', PARTS[1].a + 40); await new Promise(r => setTimeout(r, 400));
            $('#rSearch').click(); const chips = $$('#sIn .chip').map(c => c.textContent + (c.classList.contains('on') ? '*' : ''));
            const inPart = await go('राम'), inP = [inPart.length, inPart.every(i => IT[i].p === 1)], d45 = (await go('45')).map(i => IT[i].id); $$('#sIn .chip')[1].click(); await new Promise(r => setTimeout(r, 80)); const whole = $$('#sRes .res').map(b => +b.dataset.i).some(i => IT[i].p !== 1);
            show('home'); $('#hSearch').click(); const homeHidden = $('#sIn').hidden;
            await openWork('shirdi-sai-dhoop-aarti', true); await loadSources(); show('home'); openReader('k', ID['namaskarashtak.pad3']); await new Promise(r => setTimeout(r, 400));
            $('#rSearch').click(); const sh = $$('#sIn .chip')[0].textContent, shHits = await go('साई'), sec = TOPICS.find(t => t.id.startsWith('namaskarashtak'));
            return [chips, inP[0] > 0 && inP[1], d45, whole, homeHidden, sh, shHits.length > 0 && shHits.every(i => i >= sec.i && i <= sec.end)]; })()""")
        check('searched from the reader, the search stays in its part or section; Whole work widens it; from the home it searches everything',
              sin == [['Ayodhya Kand*', 'Whole work'], True, ['ayodhya.45.do45'], True, True, sin[5], True] and sin[5] != 'Whole work', sin)
        # a work loaded by part (the Valmiki): as each part's meanings arrive the search runs again; when its results are the same
        # the list stays put (the same buttons, so a result being tapped does not vanish) and only the "Searching…" note goes;
        # a new query draws a new list
        sp = await ev("""(async () => { await openWork('valmiki-ramayana', true); show('home'); openSearch('text'); $('#q').value = 'राम'; runSearch();
            for (let k = 0; k < 150 && (SLOADING || $('#sRes .sload')); k++) await new Promise(r => setTimeout(r, 200));   // every part's meanings in
            const box = $('#sRes'), first = box.querySelector('.res'), n0 = !!first;
            box.insertAdjacentHTML('afterbegin', '<p class="small muted sload">x</p>'); runSearch(); const kept = !!first && box.contains(first) && box.querySelector('.res') === first;
            const noteGone = !box.querySelector('.sload');
            $('#q').value = 'सीता'; runSearch(); const redrawn = !box.contains(first);
            let tapped = null; const f2 = box.querySelector('.res'); const oo = openReader; openReader = (o, i) => { tapped = i; }; runSearch(); f2.click(); openReader = oo;
            return [n0, kept, noteGone, redrawn, tapped === +f2.dataset.i]; })()""")
        check('a work loaded by part: the same search results stay in place as parts load (a tap still opens its verse); a new query redraws them', sp == [True, True, True, True, True], sp)
        # at the end of a part, the button to the next part shows how long it plays, as the button to the next day of a plan does
        nd = await ev("""(async () => { const out = []; for (const w of ['katha-upanishad', 'manas']){ await openWork(w, true); await loadSources(); show('home');
              openReader('k', PARTS[0].b); await new Promise(r => setTimeout(r, 300)); const e = document.querySelector('#reader .endb');
              out.push([!!(e && e.querySelector('[data-next]')), !!(e && e.querySelector('.ndur') && /▶ \\d/.test(e.querySelector('.ndur').textContent))]); } return out; })()""")
        check('the next part\'s button shows its listening time in every work, as a plan\'s next day does', nd == [[True, True], [True, True]], nd)
        # the two capsules: the dark one answers a tap and has no button; an ending (Recitation complete) is in the white one, as "Finished · ▶ Play on" is
        cap = await ev("""(() => { toast('x'); const dark = !$('#toast').classList.contains('act') && !$('#toast').querySelector('button'); $('#toast').classList.remove('on');
              toastLight('y'); const white = $('#toast').classList.contains('act'); $('#toast').classList.remove('on', 'act');
              const src = onEnded.toString() + tick.toString(); return [dark, white, /toastLight\\(msg\\)/.test(src)]; })()""")
        check('capsules: a toast is dark with no button; an ending is in the white capsule', cap == [True, True, True], cap)
        # a reading timer set just before leaving (scrolling, then Back and another work opened within its 200 ms) does nothing:
        # it once read the new work's verses with the old reading's range (smoke test: "reading 's'" in updateHeader)
        n0 = len(errs)
        race = await ev("""(async () => { await openWork('bhagavata-purana', true); openReader('k', IT.length - 40); await new Promise(r => setTimeout(r, 300));
              window.scrollBy(0, 400); window.dispatchEvent(new Event('scroll')); show('home'); await openWork('ganga-aarti', true); await new Promise(r => setTimeout(r, 450)); return W.id; })()""")
        check('a reading timer from the work just left does nothing in the next one', race == 'ganga-aarti' and len(errs) == n0, errs[n0:n0 + 2])
        # the white capsule looks the same wherever it shows: the message after an ending and the reader's ↑ Go to / ↓ Back to pills
        # share the page's surface, its rule, its shadow, the ink for words and the round ends; the dark one is ink on the page colour
        look = await ev("""(() => { const st = e => { const c = getComputedStyle(e); return [c.backgroundColor, c.color, c.boxShadow, c.borderTopColor, c.borderTopLeftRadius]; };
              toastLight('y'); const w = st($('#toast')); $('#toast').classList.remove('on', 'act'); toast('x'); const d = st($('#toast')); $('#toast').classList.remove('on');
              const pj = $('#pJump'), was = pj.hidden; pj.hidden = false; const p = st(pj); pj.hidden = was; return [JSON.stringify(w) === JSON.stringify(p), w[0] !== d[0] && d[2] === 'none']; })()""")
        check('capsules: the white capsule and the Go to / Back to pills look alike; the dark one does not', look == [True, True], look)
        # a long message in the white capsule wraps inside the screen (nothing wider than the screen)
        fit = await ev("""(() => { toastLight(T('आगेके अंशकी रिकॉर्डिंग नहीं है — अगली रिकॉर्डिंगसे जारी', 'No recording for the next part — continuing with the next one')); const t = $('#toast'), r = t.getBoundingClientRect(), ok = r.left >= 0 && r.right <= innerWidth && t.scrollWidth <= t.clientWidth + 1; t.classList.remove('on', 'act'); return ok; })()""")
        check('capsules: a long message in the white capsule stays inside the screen', fit)
        # A−/A+ scale the sheets and search results too, with nothing spilling sideways at the largest size
        zs = await ev("""(async () => { const was = S.settings.size, out = []; for (const sz of [21, 34]){ S.settings.size = sz; applyTheme(); await openWork('manas', true); openReader('M', dayRange('M', 27)[0]); await new Promise(r => setTimeout(r, 300)); $('#rMid').click(); await new Promise(r => setTimeout(r, 400));
            const sb = $('#sheetBody'); out.push([+getComputedStyle(sb).zoom, sb.scrollWidth <= sb.clientWidth + 1, +getComputedStyle($('#sRes')).zoom]); closeSheet(); }
            S.settings.size = was; applyTheme(); return out; })()""")
        check('A−/A+ scale the sheets and search results; nothing spills sideways at the largest size', zs[0][0] == 1 and zs[1][0] > 1.3 and zs[1][1] and zs[1][2] > 1.3, zs)
        # the player: only the place, short ("Verse 1.3": the third verse under Doha 1); outside the reader "Go to verse ›" under it, and a tap opens the verse playing; in the reader nothing under it
        pg_ = await ev("""(async () => { await openWork('sundarkand', true); show('home'); playRange('k', PARTS[2].a, PARTS[2].b); await new Promise(r => setTimeout(r, 300));
            const yf = ytFrame(); if (yf) yf.src = 'about:blank'; ytOK = false;   // a quiet player: on the CI runner YouTube plays for real and would move the lit verse
            PL.cur = -1; setCur(PARTS[2].a + 5);
            const inR = $('#pTrack').textContent; show('home'); await new Promise(r => setTimeout(r, 200)); const lab = $('#pVerse').textContent, sub = $('#pTrack').textContent;
            $('#pInfo').click(); await new Promise(r => setTimeout(r, 400)); const r = [lab, sub, inR, CURVIEW, !!document.querySelector('#v' + (PARTS[2].a + 5) + '.now')]; stopAudio(); return r; })()""")
        check('the player outside the reader shows only the place and "Go to verse", which opens the verse playing', pg_[0] == 'Verse 1.3' and pg_[1] == 'Go to verse ›' and pg_[2] == '' and pg_[3] == 'reader' and pg_[4], pg_)
        # ⏭ after a single verse was played: the next verse alone plays and stops (it stopped at once before); within a section, playing goes on
        stp = await ev("""(async () => { await openWork('sundarkand', true); show('home'); const i = PARTS[2].a + 4; openReader('k', i); await new Promise(r => setTimeout(r, 200));
            playFrom(i, i); PL.cur = -1; setCur(i); stepVerse(1); const one = [PL.on, PL.end === i + 1, PL.one];
            stepVerse(1); one.push(PL.end === i + 2);
            playFrom(i, i + 6); PL.cur = -1; setCur(i); stepVerse(1); const range = [PL.on, PL.end === i + 6, !PL.one]; stopAudio(); return one.concat(range); })()""")
        check('after a single verse, ⏭ plays the next verse alone (and again); within a section it keeps playing to the end', all(stp), stp)
        # "Back to …" never outlives its reader: leaving the reader hides it, and another work never shows the last one's place
        xw = await ev("""(async () => { AN.manual = true; await openWork('katha-upanishad', true); const ws = WS(); delete ws.anchor; openReader('k', PARTS[1].a); await new Promise(r => setTimeout(r, 200)); anchorTick(true);
            openReader('k', 0); await new Promise(r => setTimeout(r, 200)); backPill(); const up = !$('#rAnchor').hidden;
            show('home'); const goneHome = $('#rAnchor').hidden; libPath = []; show('library'); await openWork('manas'); await new Promise(r => setTimeout(r, 200));
            const goneOther = $('#rAnchor').hidden && !$('#rAnchor').textContent.includes('Mantra'); AN.manual = false; return [up, goneHome, goneOther]; })()""")
        check('"Back to" hides on leaving the reader, and another work never shows the last one\'s place', all(xw), xw)
        # the library lists works by name only (ⓘ About is on the work's own page)
        nolib = await ev("(async () => { libPath = []; show('library'); await new Promise(r => setTimeout(r, 300)); return [$$('#libList [data-open-work]').length, $$('#libList .winfo, #libList [data-info-work]').length]; })()")
        check('the library shows works by name, without ⓘ', nolib[0] > 0 and nolib[1] == 0, nolib)
        # a long press on a work opens About this work (and not the work); a tap still opens the work
        hold = await ev("""(async () => { libPath = []; show('library'); await new Promise(r => setTimeout(r, 300));
            const b = $('#libList [data-open-work]'), id = b.dataset.openWork, ev = (k) => b.dispatchEvent(new PointerEvent(k, {bubbles: true, button: 0, clientX: 5, clientY: 5}));
            ev('pointerdown'); await new Promise(r => setTimeout(r, 650)); ev('pointerup'); b.click(); await new Promise(r => setTimeout(r, 300));
            const r = [id, $('#sheet').classList.contains('on'), CURVIEW, $('#sheetBody h2') ? $('#sheetBody h2').textContent === TT(workNode(id).title) : false];
            closeSheet(); ev('pointerdown'); ev('pointerup'); b.click(); await new Promise(r => setTimeout(r, 1500)); r.push(CURVIEW, W && W.id === id); return r; })()""")
        check('a long press on a work in the library opens About this work; a tap opens the work', hold[1] and hold[2] == 'library' and hold[3] and hold[4] == 'home' and hold[5], hold)
        # a saved file: “Add them to this phone” shows them at once; “Replace everything” with an older file (no timing) keeps the app working
        f = {'kind': 'manas-personal', 'v': 3, 'settings': {'ui': 'en', 'layers': {'h': False, 'e': True, 'w': False}, 'tr': False, 'size': 21, 'theme': 'light', 'tour': 1}, 'src': {}, 'w': {},
             'profiles': [{'id': 'px', 'name': 'Me', 'notes': {'manas:bal.1.cau1': [{'t': 'a note', 'ts': 1}]}, 'bm': {'manas:bal.1.cau2': 1}, 'done': {}, 'gloss': {}, 'fix': {}}], 'active': 'px', 'show': ['px']}
        await ev("""(async () => { S.profiles[0].bm = {}; S.profiles[0].notes = {}; save(); await openWork('manas', true); show('bookmarks'); })()"""); await pg.wait_for_timeout(400)
        payload = {'name': 'my-file.json', 'mimeType': 'application/json', 'buffer': json.dumps(f).encode()}
        await pg.set_input_files('#fileIn', payload); await pg.wait_for_timeout(500)
        one = await ev("$('#sheetBody').innerText")
        await (await pg.query_selector('#imAdd')).click(); await pg.wait_for_timeout(500)
        added = await ev("$('#bmBody').innerText")
        n_err = len(errs)
        await pg.set_input_files('#fileIn', payload); await pg.wait_for_timeout(500)
        await (await pg.query_selector('#imRep')).click(); await pg.wait_for_timeout(300); await (await pg.query_selector('#askOk')).click(); await pg.wait_for_timeout(600)
        await ev("openReader('k', 0)"); await pg.wait_for_timeout(800)
        rep = await ev("[document.querySelectorAll('#rBody .verse').length, !!(S.timing && S.timing.fix)]")
        check('a saved file: “1 note” (not “1 notes”); added bookmarks show at once; Replace with an older file keeps the reader working', '1 note' in one and '1 notes' not in one and 'Bookmarks (1)' in added and rep[0] > 0 and rep[1] and len(errs) == n_err, [one[:80], added[:40], rep, errs[n_err:]])
        # a personal source (a meaning file kept on this phone only): Open a file adds it as the work's first meaning in its
        # language, shown at once; it stays after a reload; Sources removes it
        ps = {'kind': 'scriptures-source', 'work': 'isha-upanishad', 'source': {'id': 'pa-test', 'lang': 'pa', 'title': {'hi': 'परख', 'en': 'Test', 'pa': 'ਪਰਖ'}},
              'm': {'m01': ['ਪਰਖ ਦਾ ਅਰਥ ।੧।\nਦੂਜੀ ਸਤਰ', ['ਪਦ ਅਰਥ: ਪਰਖ']]}}
        await ev("(async () => { await openWork('isha-upanishad', true); S.settings.recite = false; save(); })()"); await pg.wait_for_timeout(400)
        await pg.set_input_files('#fileIn', {'name': 'pa-test.json', 'mimeType': 'application/json', 'buffer': json.dumps(ps).encode()}); await pg.wait_for_timeout(800)
        await ev("openReader('k', IT.findIndex(x => x.id === 'm01'))"); await pg.wait_for_timeout(600)
        pa1 = await ev("""[W.sources.pa[0].id, !!S.settings.layers.pa, (() => { const v = document.querySelector('#v' + IT.findIndex(x => x.id === 'm01')), l = v && v.querySelector('.layer.pa'); return l ? l.innerHTML : ''; })()]""")
        await pg.reload(); await pg.wait_for_timeout(2500)
        await ev("(async () => { await openWork('isha-upanishad', true); })()"); await pg.wait_for_timeout(600)
        pa2 = await ev("[(W.sources.pa || []).map(x => x.id), !!(SRC.pa && SRC.pa.m.m01)]")
        await ev("(async () => { await persRemove('pa-test'); })()"); await pg.wait_for_timeout(400)
        pa3 = await ev("(async () => [(W.sources.pa || []).map(x => x.id), (SRC.pa && SRC.pa.id) || null, (await persOf('isha-upanishad')).length])()")
        check('a personal source: Open a file adds it first in its language and shows it (a line per break); it stays after a reload; Remove takes it off this phone',
              pa1[0] == 'pa-test' and pa1[1] and 'ਪਰਖ ਦਾ ਅਰਥ' in pa1[2] and '<br>' in pa1[2] and pa2 == [['pa-test'], True] and 'pa-test' not in pa3[0] and pa3[1] != 'pa-test' and pa3[2] == 0, [pa1, pa2, pa3])
        await ev("(() => { S.settings.layers.pa = false; save(); })()")
        # the hard words of our meanings: underlined, a tap opens its meaning; the work's own sense first (विद्या in the Īśāvāsya)
        hw = await ev("""(async () => { await openWork('isha-upanishad', true); S.settings.layers = {h: true, e: true, w: false}; S.settings.recite = false; await loadSources(); syncLayers(); openReader('k', IT.findIndex(x => x.id === 'm09')); await new Promise(r => setTimeout(r, 600));
            const v = document.querySelector('#v' + IT.findIndex(x => x.id === 'm09')), ws = [...v.querySelectorAll('.layer .mw')].map(w => w.dataset.mw), plain = !v.querySelector('.layer .mw[data-mw="जो"]');
            return [ws, plain]; })()""")
        await (await pg.query_selector('#rBody .layer .mw[data-mw="avidyā"]')).click(); await pg.wait_for_timeout(400)
        sheet = await ev("$('#sheet').classList.contains('on') ? $('#sheetBody').innerText : ''")
        await ev("closeSheet()")
        check('hard words of a meaning are underlined and open their meaning (the work’s own sense first); other words are plain', 'अविद्या' in hw[0] and 'avidyā' in hw[0] and 'उपासना' in hw[0] and hw[1] and 'ritual works' in sheet, [hw, sheet[:120]])
        # a word with an entry of its own is that word: परे ("beyond", a plain entry) is never underlined as परा ("supreme"), a plural
        # is looked through only when the word has no entry (देवियों → देवी, a plain word, before देवि, the hard vocative), and
        # a postposition still is (अपकीर्तियोंको → अपकीर्ति)
        hk = await ev("(() => [hardKey('परे', 'hi'), hardKey('देवियों', 'hi'), hardKey('रसोंके', 'hi'), hardKey('सिद्धिके', 'hi'), hardKey('अपकीर्तियोंको', 'hi'), hardKey('विभीषणजीने', 'hi')])()")
        check('a meaning word with an entry of its own is never taken for another hard word (परे is not परा); joined endings are still looked through', hk[:3] == [None, None, None] and hk[3] == 'सिद्धि' and hk[4] == 'अपकीर्ति' and hk[5] == 'विभीषण', hk)
        # ☰ › More settings › "Meaning per line": shown only for a work with a meaning line by line (as Footnotes, Commentary);
        # off by default; the switch turns it on
        hidden = await ev("(async () => { show('settings'); await new Promise(r => setTimeout(r, 200)); return !document.querySelector('#slines') && !hasLines(); })()")   # the Īśāvāsya: whole meanings only
        await ev("openWork('sundarkand', true)"); await pg.wait_for_timeout(1500)
        await ev("delete S.settings.lines; save(); show('settings')"); await pg.wait_for_timeout(300)
        off0 = await ev("!!document.querySelector('#slines') && !document.querySelector('#slines').checked")
        await (await pg.query_selector('label:has(#slines)')).click(); await pg.wait_for_timeout(200)
        check('“Meaning per line” shows only in a work with line-by-line meanings, is off by default and its switch turns it on', hidden and off0 and await ev("S.settings.lines === true"))
        await ev(f"(() => {{ S = JSON.parse({json.dumps(keep)}); save(); applyState(); }})()")
        dups = await ev(DUP_IDS); check('every element id is used once in the page (a second one takes the first one\'s tap)', not dups, dups[:5])
        check('no script errors anywhere', not errs, '; '.join(errs[:3]))
        await split_work(b, SHOTS)
        if NSHARD > 1:   # shard 0's share of the works, after every check of the whole app (those change the reader's settings), as a reader who has seen the tour
            await pg.goto(url); await pg.wait_for_timeout(2500)
            await ev("(() => { S.settings.tour = 1; S.admin = 1; closeTour(); S.settings.layers.h = false; save(); })()"); await pg.reload(); await until("typeof LIB !== 'undefined' && !!LIB && LIB.length > 0 && !!document.querySelector('#libList [data-node]')", 20000)
            for leaf, trail in mine(list(leaves(shelf))): await per_work(leaf, trail)
            dups = await ev(DUP_IDS); check(f'shard 0/{NSHARD}: every element id is used once in the page', not dups, dups[:5])
            check(f'shard 0/{NSHARD}: no script errors', not errs, '; '.join(errs[:3]))
        await b.close()
    print(f'\n{sum(results)}/{len(results)} checks passed')
    sys.exit(0 if all(results) else 'UX TEST FAILED')
async def split_work(b, shots):
    """A work loaded by part ("load": "parts", docs/LIBRARY.md §3): it opens without fetching any other part, shows the
    meanings and word meanings of a second part once the reader goes there (the footer's section picker, tapped), finds
    meanings across every part in search (the verses at once, the meanings as each part comes), shows its own section
    labels ("sections"), and keeps a part opened once for reading offline."""
    tmp = tempfile.mkdtemp(); lib, path = split_fixture.make(tmp); srv = split_fixture.serve(lib, path); url = f'http://127.0.0.1:{srv.server_address[1]}/'
    W = split_fixture.WORK; base = f'library/{path}/'
    G1 = json.load(open(os.path.join(lib, path, 'glossary', '1.json'), encoding='utf-8'))
    ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
    pg = await ctx.new_page(); errs = []; got = []; slow = {'on': False}
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('request', lambda r: got.append(r.url.split(base, 1)[1].split('?')[0]) if base in r.url else None)
    async def late(route):   # while "slow" is on, a part file takes 1.5 s, as on a phone
        if slow['on'] and ('/meanings/' in route.request.url and route.request.url.split('?')[0].rsplit('/', 2)[-2] != 'meanings' or '/glossary/' in route.request.url): await asyncio.sleep(1.5)
        await route.continue_()
    await pg.route('**/library/**', late)
    await pg.add_init_script('window.__SALUTE_MS = 0')
    n = [0]
    async def shot(tag):
        if shots: n[0] += 1; os.makedirs(shots, exist_ok=True); await pg.screenshot(path=os.path.join(shots, f'split-{n[0]:02d}-{tag}.png'))
    ev = pg.evaluate
    await pg.goto(url); await pg.wait_for_timeout(1500)
    await ev(f"""(async () => {{ S.settings.tour = 1; closeTour(); S.settings.ui = 'en'; S.settings.layers = {{h: true, e: true, w: false}}; S.settings.recite = false; save(); applyLang(); syncLayers();
        await openWork({json.dumps(W)}); }})()"""); await pg.wait_for_timeout(1200)
    await shot('home')
    home = await ev("[W.load, [...document.querySelectorAll('#orgList .ds')].map(x => x.textContent)]")
    first = sorted(set(got))
    check('split work: it opens with the verses only and the first part’s meanings and word senses, never a whole source or another part',
          home[0] == 'parts' and 'work.json' in first and any(f.startswith('meanings/hi-scriptures/0') for f in first) and 'glossary/0.json' in first
          and not any(f.endswith('/1.json') for f in first) and 'glossary.json' not in first, first)
    await (await pg.query_selector('#orgList [data-open]')).click(); await pg.wait_for_timeout(1200)
    r0 = await ev("[R.n, document.querySelectorAll('#rBody .layer').length, document.querySelector('#rMid .ml').textContent]")
    await shot('part1')
    check('split work: the first part shows its meanings; the footer shows the work’s own section label', r0[0] == 0 and r0[1] > 4 and r0[2].startswith('Shanti Paath'), r0)
    # to the second part the way a finger does: the footer, the second part, its first section
    slow['on'] = True; got.clear()
    await pg.click('#rMid'); await pg.wait_for_timeout(400)
    await pg.click('#sheetBody .pick [data-pick="1"]'); await pg.wait_for_timeout(300)
    rows = await ev("[...document.querySelectorAll('#sheetBody .secs .sr')].map(x => x.textContent)")
    await shot('picker')
    await pg.click('#sheetBody .secs [data-to]'); await pg.wait_for_timeout(300)
    early = await ev("[R.n, document.querySelectorAll('#rBody .verse').length, document.querySelectorAll('#rBody .layer').length, Math.round(document.getElementById('v' + R.a).getBoundingClientRect().top)]")
    await pg.wait_for_timeout(2500)
    r1 = await ev("""(() => { const i = R.a, v = document.getElementById('v' + i); return [R.n, document.querySelectorAll('#rBody .layer').length, IT[i].p, !!(v && v.querySelector('.layer')), document.querySelector('#rMid .ml').textContent, Math.round(v.getBoundingClientRect().top)]; })()""")
    await shot('part2')
    check('split work: the section picker lists the second part’s sections by their labels (Valli 2.1 …)', rows[:3] == ['Valli 2.1', 'Valli 2.2', 'Valli 2.3'], rows)
    check('split work: the second part shows its verses at once and its meanings when its files come, the page kept in place',
          early[0] == 1 and early[1] > 0 and early[2] == 0 and r1[0] == 1 and r1[1] > 4 and r1[2] == 1 and r1[3] and r1[4].startswith('Valli 2.1') and abs(r1[5] - early[3]) <= 2 and
          any(f.startswith('meanings/en-scriptures/1') for f in got) and 'glossary/1.json' in got, (early, r1, sorted(set(got))))
    slow['on'] = False
    # a word of the second part: the work's own sense, which only glossary/1.json has
    wid = next(x['id'] for x in json.load(open(os.path.join(lib, path, 'work.json'), encoding='utf-8'))['items'] if 'विश्वे' in ' '.join(x['v']))
    await ev(f"(() => {{ const i = ID[{json.dumps(wid)}]; jumpTo(i); }})()"); await pg.wait_for_timeout(600)
    loc = pg.locator(f'#v{await ev(f"ID[{json.dumps(wid)}]")} .w', has_text='विश्वे').first
    await loc.click(); await pg.wait_for_timeout(500)
    sheet = await ev("$('#sheet').classList.contains('on') ? $('#sheetBody').innerText : ''")
    await shot('word'); await ev("closeSheet()")
    check('split work: a word of the second part opens the work’s own sense from that part', G1['sa']['विश्वे']['en'][:30] in sheet or G1['sa']['विश्वे']['hi'][:30] in sheet, sheet[:160])
    hard = await ev("(() => { const v = document.getElementById('v' + ID['2.1.15']); return v ? [...v.querySelectorAll('.layer .mw')].map(x => x.dataset.mw) : null; })()")
    if hard is None: await ev("jumpTo(ID['2.1.15'])"); await pg.wait_for_timeout(600); hard = await ev("[...document.getElementById('v' + ID['2.1.15']).querySelectorAll('.layer .mw')].map(x => x.dataset.mw)")
    check('split work: a hard word of a second-part meaning is underlined from that part’s senses', 'गौतम' in hard, hard)
    # labels in Hindi, numbers in Latin digits; a verse's place names its section
    await ev("S.settings.ui = 'hi'; S.settings.layers.e = false; save(); applyLang(); syncLayers(); refreshReader()"); await pg.wait_for_timeout(500)
    hi = await ev("[document.querySelector('#rMid .ml').textContent, itemLabel(ID['2.2.3'])]")
    await shot('hindi')
    await ev("S.settings.ui = 'en'; S.settings.layers.e = true; save(); applyLang(); syncLayers(); refreshReader()")
    check('split work: the section labels in Hindi, with 1 2 3; a verse’s place names its section', hi[0].startswith('वल्ली 2.') and 'वल्ली ' in hi[1] and '२' not in hi[0], hi)
    # search on a fresh start: the verses at once, then a meaning only the second part has, as that part comes
    await ev("(() => { const ws = S.w[W.id]; ws.last = null; ws.pos = {}; save(); })()")   # no place in the second part: “Continue” does not fetch it
    await pg.close(); pg = await ctx.new_page(); ev = pg.evaluate; pg.on('pageerror', lambda e: errs.append(str(e))); await pg.route('**/library/**', late)   # a fresh start, not back in the reader
    await pg.goto(url); await pg.wait_for_timeout(1500); slow['on'] = True
    await ev(f"(async () => {{ await openWork({json.dumps(W)}, true); show('home'); }})()"); await pg.wait_for_timeout(1500)
    await pg.click('#hSearch'); await pg.wait_for_timeout(300)
    await pg.fill('#q', 'devourer'); await pg.wait_for_timeout(700)
    s0 = await ev("[!!document.querySelector('#sRes .sload'), [...document.querySelectorAll('#sRes .res .where')].map(w => w.textContent)]")
    await pg.wait_for_timeout(4500)
    s1 = await ev("[!!document.querySelector('#sRes .sload'), [...document.querySelectorAll('#sRes .res')].map(b => [IT[+b.dataset.i].id, IT[+b.dataset.i].p, b.querySelector('.where').textContent])]")
    await shot('search')
    check('split work: search shows “searching every part” at first, then finds a meaning only the second part has, with its section label',
          s0[0] and not any('English meaning' in w for w in s0[1]) and not s1[0] and any(r[0] == '2.1.7' and r[1] == 1 and 'English meaning' in r[2] and 'Valli 2.1' in r[2] for r in s1[1]), (s0, s1))
    await pg.fill('#q', 'विश्वे देवा'); await pg.wait_for_timeout(600)
    s2 = await ev("[...document.querySelectorAll('#sRes .res')].map(b => IT[+b.dataset.i].id)")
    check('split work: the verse text is found at once', wid in s2, s2)
    check('split work: no script errors', not errs, '; '.join(errs[:3]))
    await ctx.close()
    # offline: a part opened once is kept by the service worker
    ctx2 = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); pg2 = await ctx2.new_page(); errs2 = []
    pg2.on('pageerror', lambda e: errs2.append(str(e))); await pg2.add_init_script('window.__SALUTE_MS = 0; window.__SW_TEST = 1')
    await pg2.goto(url); await pg2.wait_for_timeout(2500); await pg2.reload(); await pg2.wait_for_timeout(2000)
    await pg2.evaluate(f"(async () => {{ S.settings.tour = 1; closeTour(); S.settings.layers = {{h: true, e: true, w: false}}; save(); await openWork({json.dumps(W)}, true); show('home'); openReader('k', PARTS[1].a + 3); }})()"); await pg2.wait_for_timeout(2500)
    srv.shutdown(); srv.server_close()
    await pg2.reload(); await pg2.wait_for_timeout(3000)
    off = await pg2.evaluate(f"(async () => {{ if (!W || W.id !== {json.dumps(W)}) await openWork({json.dumps(W)}, true); show('home'); openReader('k', PARTS[1].a + 3); await new Promise(r => setTimeout(r, 1500)); return [W && W.id, document.querySelectorAll('#rBody .verse').length, document.querySelectorAll('#rBody .layer').length]; }})()")
    check('split work offline: a part opened once is readable with its meanings', off[0] == W and off[1] > 0 and off[2] > 4 and not errs2, (off, errs2[:2]))
    await ctx2.close(); shutil.rmtree(tmp, ignore_errors=True)

asyncio.run(main())
