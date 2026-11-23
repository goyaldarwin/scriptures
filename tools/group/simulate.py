"""Group paath: a simulation of real use, against the real relay (wrangler dev, tools/group/worker.js) and the built site.

Usage:  python3 tools/group/simulate.py [--shots DIR]     (about 6 minutes; after python3 tools/site/build.py)
Needs:  Node with wrangler (npx wrangler, or WRANGLER=/path/to/wrangler), playwright (CHROMIUM=/path/to/chrome if not found)
It starts its own relay (wrangler dev on port 8787) and web server (port 8000), and stops them at the end.

One leader phone (YouTube simulated: it reports its time as the real player does, ends tracks, follows seek/play/pause)
and six follower phones, each its own browser context at phone size; 50 more lightweight followers on raw WebSockets.
Every scenario prints PASS/FAIL; sync is sampled throughout (time difference and lit verse, leader vs every follower).
"""
import asyncio, json, os, signal, subprocess, sys, time, random
from playwright.async_api import async_playwright

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WR = [os.environ['WRANGLER']] if os.environ.get('WRANGLER') else ['npx', '--yes', 'wrangler@4']
SITE = 'http://localhost:8000/'; RELAY = 'ws://127.0.0.1:8787'
SH = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
if SH: os.makedirs(SH, exist_ok=True)
res = []; notes = []
def check(n, ok, seen=''):
    res.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + n + (f'  [{seen}]' if seen != '' else ''), flush=True)

# ---------- servers (own process groups, so they can be stopped and restarted) ----------
procs = {}
def start(name):
    if name == 'relay':
        procs[name] = subprocess.Popen(WR + ['dev', '--port', '8787', '--ip', '127.0.0.1'], cwd=REPO + '/tools/group', stdout=open('/tmp/sim-relay.log', 'a'), stderr=subprocess.STDOUT, start_new_session=True)
    else:
        procs[name] = subprocess.Popen([sys.executable, '-m', 'http.server', '8000', '--bind', '127.0.0.1'], cwd=REPO, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
def stop(name):
    p = procs.pop(name, None)
    if p:
        try: os.killpg(p.pid, signal.SIGTERM)
        except Exception: pass
        p.wait(timeout=15)
def up(url, most=60):
    import urllib.request
    t = time.time()
    while time.time() - t < most:
        try: urllib.request.urlopen(url, timeout=2); return True
        except Exception: time.sleep(0.5)
    return False

FAKE_YT = """(() => { if (window.__fake) return; window.__fake = 1;
  window.ytLoad = (vid, start) => { ytVid = vid; ytOK = true; ytInfo = {t: start, st: 1, d: 0, at: performance.now()}; };
  window.ytPost = (f, a) => { if (f === 'seekTo'){ ytInfo.t = a[0]; ytInfo.at = performance.now(); } if (f === 'playVideo') ytInfo.st = 1; if (f === 'pauseVideo') ytInfo.st = 2; };
  setInterval(() => { if (ytInfo.st === 1 && PL.on){ ytInfo.t += 0.25 * RATE(); ytInfo.at = performance.now();
    const tr = SRC.au && SRC.au.tracks[PL.t]; if (tr && ytInfo.t >= (tr.end != null ? tr.end : tr.dur)){ ytInfo.st = 0; onEnded(); } } }, 250);
})()"""

async def main():
    stop_all_old()
    start('site'); start('relay')
    check('setup: site and relay are up', up(SITE) and up('http://127.0.0.1:8787/'))
    async with async_playwright() as p:
        b = await p.chromium.launch(**({'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}))
        errs = {}
        async def phone(name, lang='en', tour=True):
            ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
            pg = await ctx.new_page(); errs[name] = []
            await pg.add_init_script(f"window.__SALUTE_MS = 0; window.__GROUP_URL = '{RELAY}'")
            pg.on('pageerror', lambda e: errs[name].append((e.stack or str(e))[:600]))
            pg.name = name; pg.ctx = ctx; pg.lang = lang; pg.tour = tour
            return pg
        async def boot(pg, url=SITE):
            await pg.goto(url); await pg.wait_for_function("typeof LIB !== 'undefined' && !!LIB", timeout=20000)
            if pg.tour: await pg.evaluate(f"S.settings.tour = 1; S.settings.ui = '{pg.lang}'; save(); closeTour(); applyLang()")
        async def shot(pg, tag):
            if SH: await pg.screenshot(path=f'{SH}/{tag}.png')

        L = await phone('leader'); await boot(L); await L.evaluate(FAKE_YT)
        F = [await phone('F1'), await phone('F2', 'hi'), await phone('F3'), await phone('F4'), await phone('F5', tour=False), await phone('F6')]

        async def lead_play(work, org='k', at=None):
            await L.evaluate(f"""(async () => {{ if (!W || W.id !== {json.dumps(work)}) await openWork({json.dumps(work)}); await whenReady();
              const i = {at if at is not None else 'firstAu(0, IT.length - 1)'}; openReader({json.dumps(org)}, i); playFrom(i); }})()""")
            await L.wait_for_function("PL.on && PL.cur >= 0 && ytOK", timeout=30000)
        async def sync(fs, secs, tag, tol=0.4):
            """sample every 0.5 s: each follower's time within tol of the leader's, the same lit verse unless the leader is
            within 0.6 s of a verse boundary"""
            worst = 0; bad = []
            for _ in range(int(secs * 2)):
                l = await L.evaluate("(() => { const t = gpTime(), a = AUT[PL.t] || []; return [PL.cur, t, a.reduce((m, x) => Math.min(m, Math.abs(x[1] - t)), 99), PL.on, ytInfo.st, Date.now(), ytInfo.st === 1 ? RATE() : 0] })()")
                for f in fs:
                    v = await f.evaluate("(() => { const b = GP.base; return [PL.cur, b ? b.t + (b.p ? b.r * (performance.now() - b.at) / 1000 : 0) : -1, PL.on, Date.now()] })()")
                    if not l[3]: continue
                    tl = l[1] + l[6] * (v[3] - l[5]) / 1000   # the leader's time at the instant the follower was read
                    d = abs(v[1] - tl); worst = max(worst, d)
                    if d > tol or (v[0] != l[0] and l[2] > 0.6) or not v[2]: bad.append((f.name, round(tl, 2), round(v[1], 2), l[0], v[0]))
                await asyncio.sleep(0.5)
            check(f'{tag}: {len(fs)} followers in step for {secs} s (worst {worst:.2f} s)', not bad, bad[:3])
            return worst

        # ---------- 1. the Mānas, 30-day plan, day 1; the leader starts a group paath from ☰ ----------
        await L.evaluate("openWork('manas')"); await L.wait_for_function("!!document.querySelector('#orgList [data-open]')", timeout=30000)
        await lead_play('manas', 'M', "dayRange('M', 1)[0]")
        await L.click('#rMore'); await L.click('[data-m="group"]'); await L.click('#gpLead')
        await L.wait_for_function("GP.live", timeout=10000); code = await L.evaluate('GP.code'); await shot(L, '01-leader-sheet')
        await L.evaluate('closeSheet()')
        # F1: a fresh phone opens the shared link
        await F[0].goto(SITE + '?join=' + code)
        await F[0].wait_for_function("GP.role === 'follow' && PL.on && PL.cur >= 0", timeout=30000)
        check('1: F1 joins by the link, opens the Mānas in the leader\'s plan and day', await F[0].evaluate("W.id === 'manas' && R.org === 'M' && R.n === 1"), await F[0].evaluate("[W.id, R.org, R.n]"))
        # F2: Hindi phone on the library types the code in ☰ › Group paath
        await boot(F[1]); await F[1].evaluate('mainMenu()'); await F[1].click('[data-m="group"]'); await F[1].fill('#gpIn', code[:3] + ' ' + code[3:]); await F[1].click('#gpJoin')
        await F[1].wait_for_function("GP.role === 'follow' && PL.on && PL.cur >= 0", timeout=30000)
        check('1: F2 (Hindi) joins by typing the code with a space, from the library', await F[1].evaluate("W.id === 'manas' && S.settings.ui === 'hi'"), await F[1].evaluate("[W.id, S.settings.ui, LANG()]"))
        # F4: reading the Gita when it joins: switches to the Mānas
        await boot(F[3]); await F[3].evaluate("openWork('bhagavad-gita').then(() => openReader('k', 5))"); await F[3].wait_for_function("W && W.id === 'bhagavad-gita' && document.querySelector('#reader').classList.contains('on')", timeout=30000)
        await F[3].evaluate(f"gpStart('follow', '{code}')"); await F[3].wait_for_function("W.id === 'manas' && PL.on && PL.cur >= 0", timeout=30000)
        check('1: F4, reading the Gita, joins and is taken to the Mānas at the leader\'s verse', True)
        await L.wait_for_function("GP.n === 3", timeout=5000); check('1: the leader counts 3 phones', '3 phones following' in await L.inner_text('#pTrack'), await L.inner_text('#pTrack'))
        await sync([F[0], F[1], F[3]], 12, '1')
        # F3 joins late, mid-playback
        await F[2].goto(SITE + '?join=' + code); await F[2].wait_for_function("PL.on && PL.cur >= 0", timeout=30000)
        await sync([F[2]], 4, '1 (late joiner F3)')
        await shot(F[1], '02-F2-hindi-following')

        # ---------- 2. rapid pause/play, speed ----------
        for k in range(6): await L.evaluate("ytPost(playing() ? 'pauseVideo' : 'playVideo')"); await asyncio.sleep(0.3)
        await asyncio.sleep(1.5)   # 6 toggles: playing again
        await sync(F[:3] + [F[3]], 4, '2: after six quick pause/play taps')
        await L.evaluate("ytPost('pauseVideo')"); await asyncio.sleep(1.2)
        st = [await f.evaluate("ytInfo.st") for f in F[:4]]; check('2: pause reaches every follower', all(x == 2 for x in st), st)
        await asyncio.sleep(3); await L.evaluate("ytPost('playVideo')")
        await sync(F[:4], 4, '2: after a 3 s pause')
        await L.click('#pRate'); await L.click('#pRate'); await asyncio.sleep(1)   # 1× → 1.25× → 1.5×, tapped
        rates = [await f.evaluate("GP.base.r") for f in F[:4]]; check('2: speed 1.5× reaches every follower', all(r == 1.5 for r in rates), rates)
        await sync(F[:4], 6, '2: at 1.5×')
        for _ in range(4): await L.click('#pRate')   # round to 1×
        await asyncio.sleep(1)

        # ---------- 3. ⏭ steps, and the end of a recording (day 1 → day 2's video) ----------
        before = await L.evaluate('PL.cur')
        for _ in range(3): await L.click('#pNext'); await asyncio.sleep(0.4)
        await asyncio.sleep(1); await sync(F[:4], 3, '3: after ⏭ ⏭ ⏭')
        k0 = await L.evaluate('PL.t'); await L.evaluate("(() => { const tr = SRC.au.tracks[PL.t], e = (tr.end != null ? tr.end : tr.dur) - 4; seekGuard(e); ytPost('seekTo', [e, true]); })()")
        await L.wait_for_function(f"PL.t !== {k0}", timeout=20000); await asyncio.sleep(1.5)
        ks = [await f.evaluate('PL.t') for f in F[:4]]; k1 = await L.evaluate('PL.t')
        check('3: the recording ends, the next one plays: every follower moves to the next recording', all(k == k1 for k in ks), f'leader {k0}→{k1}, followers {ks}')
        await sync(F[:4], 4, '3: in the next recording')

        # ---------- 4. the leader goes to another part (Lanka Kand) ----------
        await L.evaluate("(() => { const i = IT.findIndex(x => x.id.startsWith('lanka.')); openReader('k', i); playFrom(i); })()"); await asyncio.sleep(2)
        parts = [await f.evaluate("IT[PL.cur].id.split('.')[0]") for f in F[:4]]
        check('4: the leader jumps to Lanka Kand: every follower lights it', all(x == 'lanka' for x in parts), parts)
        await sync(F[:4], 4, '4')

        # ---------- 5. followers do their own thing ----------
        f = F[0]; await f.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        try: await f.wait_for_function("!document.querySelector('#pJump').hidden", timeout=1500); pj = True   # until the next verse brings the page back by itself
        except Exception: pj = False
        await f.click('#pJump') if pj else None; await asyncio.sleep(1)
        inview = await f.evaluate("(() => { const el = document.getElementById('v' + PL.cur); if (!el) return false; const r = el.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; })()")
        check('5: F1 scrolls away: "↑ Go to" shows and brings the lit verse back', pj and inview, f'pill={pj} inview={inview}')
        f = F[1]; await f.evaluate("show('bookmarks')"); await asyncio.sleep(1)
        sub = await f.inner_text('#pTrack'); await f.click('#pInfo'); await asyncio.sleep(1)
        check('5: F2 opens Bookmarks: the bar says it follows and the way back; a tap returns to the verse', 'पदपर जाएँ' in sub and await f.evaluate("document.querySelector('#reader').classList.contains('on')"), sub)
        f = F[3]; await f.evaluate("S.settings.layers = {h: true, e: true, w: true}; save(); syncLayers(); refreshReader()"); await f.click('#rMore') ; await f.evaluate('closeSheet()')
        await f.evaluate("setSize(2)") if await f.evaluate("typeof setSize === 'function'") else None
        await sync([F[3]], 3, '5: F4 with both meanings, word meanings and bigger letters')
        await shot(F[3], '03-F4-own-view')
        await F[0].evaluate("playFrom(PL.cur + 1)"); await asyncio.sleep(0.5)
        check('5: F1 taps ▶ on a verse: no player of its own, still following', await F[0].evaluate("!document.querySelector('#ytf') && GP.role === 'follow'"))

        # ---------- 6. a follower refreshes; a follower loses the network ----------
        await F[2].reload(); await F[2].wait_for_function("GP.role === 'follow' && GP.live && PL.on && PL.cur >= 0", timeout=30000)
        await sync([F[2]], 3, '6: F3 refreshed')
        await F[3].ctx.set_offline(True); await asyncio.sleep(4)
        off_live = await F[3].evaluate('GP.live'); await F[3].ctx.set_offline(False)
        await F[3].wait_for_function("GP.live", timeout=30000); await asyncio.sleep(1.5)
        notes.append(f'F4 offline 4 s: socket live while offline = {off_live}')
        await sync([F[3]], 3, '6: F4 back online')

        await F[3].evaluate("(() => { const ws = GP.ws; ws.__send = ws.send; ws.send = m => m === 'ping' ? undefined : ws.__send(m); window.__deadWs = ws; gpPing(); })()")   # its pings go nowhere
        await F[3].wait_for_function("GP.ws !== window.__deadWs && GP.live", timeout=20000)
        check('6: F4\'s connection goes silent (pings unanswered): it notices within 8 s and connects again', True)
        await asyncio.sleep(1.5); await sync([F[3]], 3, '6: F4 after the silent connection')
        # ---------- 7. the leader refreshes in the middle ----------
        await L.reload(); await L.wait_for_function("typeof GP !== 'undefined' && GP.role === 'lead' && GP.live", timeout=30000); await L.evaluate(FAKE_YT)
        await asyncio.sleep(1.5)
        w = [await f.evaluate("[PL.on, document.querySelector('#pTrack').textContent]") for f in F[:4]]
        check('7: the leader refreshes: it is still the leader (same code), followers wait for it to play', await L.evaluate(f"GP.code === '{code}'") and all(not x[0] and 'Waiting' in x[1] or 'प्रतीक्षा' in x[1] for x in w), w)
        await lead_play('manas', 'k', "IT.findIndex(x => x.id.startsWith('lanka.')) + 20")
        await asyncio.sleep(1.5); await sync(F[:4], 4, '7: the leader plays again')

        # ---------- 8. the relay restarts (as when Cloudflare deploys a new version) ----------
        stop('relay'); await asyncio.sleep(3)
        away = [await f.evaluate("[GP.live, GP.away, ytInfo.st]") for f in F[:4]]
        check('8: the relay goes down: followers know they are not connected', all(not a[0] for a in away), away)
        start('relay'); up('http://127.0.0.1:8787/')
        await L.wait_for_function("GP.live", timeout=40000)
        for f in F[:4]: await f.wait_for_function("GP.live && !GP.away && PL.on", timeout=40000)
        await asyncio.sleep(1.5); await sync(F[:4], 4, '8: the relay is back: everyone reconnected by itself')
        await L.wait_for_function("GP.n === 4", timeout=10000); check('8: the leader counts its 4 phones again', True)

        # ---------- 9. many phones: 50 more followers on raw WebSockets ----------
        nodef = subprocess.Popen(['node', '-e', f"""
          const N = 50, got = new Array(N).fill(0), ws = [];
          for (let k = 0; k < N; k++){{ const w = new WebSocket('{RELAY}/s/{code}?role=follow'); w.onmessage = e => {{ if (e.data !== 'pong' && JSON.parse(e.data).type === 'state') got[k]++; }}; ws.push(w); }}
          setTimeout(() => {{ console.log(JSON.stringify({{open: ws.filter(w => w.readyState === 1).length, withState: got.filter(x => x > 0).length, msgs: got.reduce((a, b) => a + b, 0)}})); ws.forEach(w => w.close()); setTimeout(() => process.exit(0), 500); }}, 12000);
        """], stdout=subprocess.PIPE, text=True)
        await asyncio.sleep(4); n = await L.evaluate('GP.n')
        await L.evaluate("ytPost('pauseVideo')"); await asyncio.sleep(1); await L.evaluate("ytPost('playVideo')")
        await sync(F[:4], 4, '9: with 54 phones in the session')
        out, _ = nodef.communicate(timeout=30); r = json.loads(out.strip().splitlines()[-1])
        check('9: 50 more phones join: the leader counts 54, each of them gets the state and the pause/play', n == 54 and r['open'] == 50 and r['withState'] == 50 and r['msgs'] >= 150, f'count {n}, {r}')
        await asyncio.sleep(2); check('9: they leave: the count is back to 4', await L.evaluate('GP.n') == 4, await L.evaluate('GP.n'))

        # ---------- 10. another work and recording; the follower's own recording comes back after ----------
        await F[0].evaluate("(S.src['aditya-hridayam'] = S.src['aditya-hridayam'] || {}).au = 'the-sanskrit-channel'; save()")
        await lead_play('aditya-hridayam')
        await L.evaluate("(async () => { (S.src[W.id] = S.src[W.id] || {}).au = 'braja-beats'; save(); stopAudio(); await loadSources(); const i = firstAu(0, IT.length - 1); openReader('k', i); playFrom(i); })()")
        await asyncio.sleep(3)
        got = [await f.evaluate("[W.id, SRC.au && SRC.au.meta.id]") for f in F[:4]]
        check('10: the leader opens Aditya Hridayam and picks another recording: every follower has both', all(g == ['aditya-hridayam', 'braja-beats'] for g in got), got)
        await sync(F[:4], 4, '10')

        # ---------- 11. Sri Guru Granth Sahib: loaded by part, kirtan timed line by line ----------
        await lead_play('guru-granth-sahib', 'k', "IT.findIndex(x => x.id === '14.1') >= 0 ? IT.findIndex(x => x.id === '14.1') : firstAu(0, IT.length - 1)")
        await asyncio.sleep(4)
        got = [await f.evaluate("[W.id, SRC.au && SRC.au.meta.id, PL.cur]") for f in F[:4]]; lc = await L.evaluate('[SRC.au.meta.id, PL.cur]')
        check('11: Sri Guru Granth Sahib (loaded by part) with its kirtan recording: every follower follows', all(g == ['guru-granth-sahib', lc[0], lc[1]] for g in got), f'leader {lc} followers {got}')
        await sync(F[:4], 6, '11')
        await shot(F[0], '04-F1-granth')

        # ---------- 12. leaving, a wrong code, and a code already taken ----------
        await F[0].click('#pClose'); await asyncio.sleep(1.2)
        check('12: F1 leaves with ✕: its bar goes, the leader counts 3', await F[0].evaluate("GP.role === null && document.querySelector('#player').hidden") and await L.evaluate('GP.n') == 3)
        check('12: F1\'s own choice of recording came back (Aditya Hridayam: The Sanskrit Channel)', await F[0].evaluate("S.src['aditya-hridayam'].au") == 'the-sanskrit-channel', await F[0].evaluate("S.src['aditya-hridayam']"))
        wrong = '1' + code[1:] if code[0] != '1' else '2' + code[1:]
        await boot(F[4]); await F[4].evaluate(f"gpStart('follow', '{wrong}')"); await asyncio.sleep(2.5)
        sub = await F[4].inner_text('#pTrack'); await shot(F[4], '05-F5-wrong-code')
        notes.append(f'F5 joined an unused code: its bar says "{sub}"')
        check('12: a wrong code: the bar says so (and it still waits, in case the leader starts later)', 'check the number' in sub and await F[4].evaluate("GP.role === 'follow' && !PL.on"), sub)
        await F[4].evaluate("gpStop()")
        # another phone claims the leader's code with another key: refused, it gets a new code
        await boot(F[5]); await F[5].evaluate(f"GP.role = 'lead'; GP.code = '{code}'; GP.key = 'x'.repeat(32); gpConnect()"); await asyncio.sleep(2)
        new = await F[5].evaluate('GP.code'); check('12: a second phone cannot take the leader\'s code: it is given a new one', new != code and await F[5].evaluate('GP.live') and await L.evaluate(f"GP.code === '{code}' && GP.live"), new)
        await F[5].evaluate("gpStop()")

        # ---------- 12b. the leader's phone locks: its connection stays open but nothing comes ----------
        await L.evaluate("window.__lock = GP.live; GP.live = false")   # its app sends nothing (the socket stays open)
        t_lock = time.time(); await F[1].wait_for_function("GP.away", timeout=25000); waited = time.time() - t_lock
        t1 = await F[1].evaluate("GP.base.t"); await asyncio.sleep(1); t2 = await F[1].evaluate("GP.base.t")
        check('12b: the leader\'s phone locks: followers stop after about 16 s and wait for it', 14 < waited < 20 and t1 == t2 and 'leader' in await F[1].inner_text('#pTrack'), f'{waited:.1f} s, {await F[1].inner_text("#pTrack")}')
        await L.evaluate("GP.live = true"); await F[1].wait_for_function("!GP.away", timeout=10000); await asyncio.sleep(1)
        await sync(F[1:4], 3, '12b: the leader\'s phone unlocked')
        # ---------- 13. the leader's phone goes; then the leader ends it ----------
        await L.evaluate("GP.ws.close()"); await asyncio.sleep(1)
        aw = [await f.evaluate("GP.away") for f in F[1:4]]; check('13: the leader\'s connection drops: followers stop and wait for it', all(aw), aw)
        await L.wait_for_function("GP.live", timeout=20000); await asyncio.sleep(1.5); await sync(F[1:4], 3, '13: back')
        await L.click('#rMore'); await L.click('[data-m="group"]'); await L.click('#gpEnd'); await asyncio.sleep(1.5)
        gone = [await f.evaluate("[GP.role, document.querySelector('#player').hidden, document.querySelector('#toast').textContent]") for f in F[1:4]]
        check('13: the leader ends it: every follower leaves, its bar goes, a message says so', all(g[0] is None and g[1] for g in gone), gone)
        await shot(F[1], '06-F2-ended')
        await F[2].reload(); await F[2].wait_for_function("typeof LIB !== 'undefined' && !!LIB", timeout=20000); await asyncio.sleep(1)
        check('13: a follower that refreshes afterwards is not in a session any more', await F[2].evaluate("GP.role === null"))

        for k, v in errs.items():
            check(f'no script errors on {k}', not v, len(v))
            for e in v[:2]: print('STACK', k, e)
        await b.close()
    stop('relay'); stop('site')
    print('\n'.join('NOTE ' + n for n in notes))
    print(f'\n{sum(res)}/{len(res)} passed'); sys.exit(0 if all(res) else 1)

def stop_all_old():
    """A relay or web server left from an earlier run holds its port: stop it. Only those programs (by program name: node,
    workerd, python), never a shell whose command line merely mentions them (docs/PLAYBOOK.md §10: no pkill -f)."""
    out = subprocess.run(['ps', '-eo', 'pid=,comm=,args='], capture_output=True, text=True).stdout
    for line in out.splitlines():
        pid, comm, args = (line.strip().split(None, 2) + ['', ''])[:3]
        if int(pid) == os.getpid(): continue
        if (comm in ('node', 'MainThread') and 'wrangler' in args and ' dev' in args) or comm == 'workerd' or (comm.startswith('python') and 'http.server 8000' in args):
            try: os.kill(int(pid), signal.SIGTERM)
            except Exception: pass
    time.sleep(1)

asyncio.run(main())
