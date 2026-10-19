"""Store screenshots, made from the real app (the site in this repository) with a caption above each.

  python3 tools/store/screenshots.py [--lang en|hi|both]   →  tools/store/out/<store>/<lang>/NN-<scene>.png

Sizes: App Store iPhone 6.9" (1320×2868) and Google Play phone (1080×1920), plus the Play feature graphic (1024×500).
YouTube cannot be reached from the build machine, so in the "playing" scene the video area shows the app's ॐ tile;
a capture from a real phone can replace that one picture.
"""
import asyncio, base64, functools, http.server, os, socketserver, sys, threading
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'out')
FONT = base64.b64encode(open(os.path.join(ROOT, 'tools', 'fonts', 'noto-serif-devanagari-devanagari-700-normal.woff2'), 'rb').read()).decode()
LAT = base64.b64encode(open(os.path.join(ROOT, 'tools', 'fonts', 'literata-latin-600-normal.woff2'), 'rb').read()).decode()

# (name, caption en, caption hi, small line en, small line hi, setup js run inside the app)
SCENES = [
 ('play', 'Listen, hands-free', 'सुनते हुए पढ़ें', 'The verse being recited is lit and the page turns by itself', 'जो पद गाया जा रहा है वह चमकता है, पन्ना अपने आप आगे बढ़ता है',
  """await openWork('sundarkand'); S.settings.layers.h = true; syncLayers();
     openReader('k', 12); await new Promise(r => setTimeout(r, 900));
     const i = 14; PL.on = true; PL.t = 0; PL.cur = -1; $('#player').hidden = false; document.body.classList.add('playing');
     $('#ytBox').innerHTML = '<div style="width:200px;height:200px;background:#2B3A8C;display:flex;align-items:center;justify-content:center;color:#F2A653;font:700 52px serif">ॐ</div>';
     setCur(i); $('#pProg').style.width = '34%'; syncPlayer = () => {}; $('#pPlay').innerHTML = '<svg><use href="#i-pause"/></svg>';"""),
 ('word', 'Tap any word for its meaning', 'किसी भी शब्दको छूकर अर्थ देखें', 'Meaning, root and grammar of every word', 'हर शब्दका अर्थ, मूल शब्द और व्याकरण',
  """await openWork('manas'); S.settings.layers.h = true; syncLayers(); openReader('k', 40); await new Promise(r => setTimeout(r, 900));
     const w = [...document.querySelectorAll('#rBody .verse .vtext .w')].find(x => x.getBoundingClientRect().top > 160); w.click();"""),
 ('meanings', 'Hindi and English meanings', 'हिंदी और अंग्रेज़ी अर्थ', 'Under every verse — switch each on or off', 'हर पदके नीचे — जो चाहें वही दिखाएँ',
  """await openWork('manas'); S.settings.layers.h = true; S.settings.layers.e = true; syncLayers(); openReader('k', 60); await new Promise(r => setTimeout(r, 900));"""),
 ('verse', 'Play one verse — or from any verse', 'एक पद सुनें — या कहींसे भी', '▶ beside a verse plays just that one; “Listen from here” goes on', 'पदके पास ▶ केवल वही पद; “यहाँसे सुनें” आगे तक',
  """await openWork('sundarkand'); S.settings.layers.h = true; syncLayers(); openReader('k', 30); await new Promise(r => setTimeout(r, 900));
     const v = [...document.querySelectorAll('#rBody .verse')].find(x => x.getBoundingClientRect().top > 300); itemMenu(+v.dataset.i);"""),
 ('plans', '30-day and 9-day readings', '३० दिन और ९ दिनका पाठ', 'Your progress and place are kept', 'प्रगति और स्थान याद रहता है',
  """await openWork('manas'); WS().org = PLANS[0] ? PLANS[0].id : 'k'; show('home'); renderHome(); window.scrollTo(0, 0);"""),
 ('library', 'A growing library', 'बढ़ता हुआ पुस्तकालय', 'Rāmacaritamānasa, Sundarakāṇḍa, Śrī Rudram, Sukhmani Sahib and more', 'रामचरितमानस, सुन्दरकाण्ड, श्रीरुद्रम्, सुखमनी साहिब और भी',
  """libPath = []; show('library'); renderLibrary(); window.scrollTo(0, 0);"""),
]
SIZES = {'appstore': (440, 956, 3), 'play': (360, 640, 3)}

def page(cw, ch, cap, sub, url, lang):
    top = 0.2 * ch; fw = cw * 0.86; scale = fw / 390; fh = (ch - top - 0.02 * ch) / scale
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:D;src:url(data:font/woff2;base64,{FONT})}}@font-face{{font-family:L;src:url(data:font/woff2;base64,{LAT})}}
html,body{{margin:0;width:{cw}px;height:{ch}px;overflow:hidden;background:linear-gradient(170deg,#2B3A8C,#1B2565)}}
.cap{{position:absolute;top:0;left:0;right:0;height:{top}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 20px;color:#fff}}
.cap b{{font:600 {0.072 * cw if lang == 'en' else 0.068 * cw}px/1.2 {'L' if lang == 'en' else 'D'},serif}}.cap span{{margin-top:8px;font:400 {0.036 * cw}px/1.35 {'L' if lang == 'en' else 'D'},serif;color:#F2C894}}
.ph{{position:absolute;top:{top}px;left:{(cw - fw) / 2}px;width:390px;height:{fh}px;transform:scale({scale});transform-origin:0 0;border-radius:{34 / scale}px;overflow:hidden;
    box-shadow:0 0 0 {6 / scale}px #0E1440,0 20px 50px rgba(0,0,0,.45);background:#F6F6F2}}
iframe{{border:0;width:390px;height:{fh}px}}</style></head><body>
<div class=cap><b>{cap}</b><span>{sub}</span></div><div class=ph><iframe id=f src="{url}"></iframe></div></body></html>"""

def serve():
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    s = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT)); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

async def main():
    langs = ['en', 'hi'] if '--lang' not in sys.argv or sys.argv[sys.argv.index('--lang') + 1] == 'both' else [sys.argv[sys.argv.index('--lang') + 1]]
    srv = serve(); base = f'http://127.0.0.1:{srv.server_address[1]}/'
    open(os.path.join(ROOT, '_shot.html'), 'w').close()
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for store, (cw, ch, dpr) in SIZES.items():
                for lang in langs:
                    d = os.path.join(OUT, store, lang); os.makedirs(d, exist_ok=True)
                    for n, (name, ce, ch_, se, sh, js) in enumerate(SCENES, 1):
                        ctx = await b.new_context(viewport={'width': cw, 'height': ch}, device_scale_factor=dpr)
                        # a fresh reader: tour seen, the chosen interface language
                        await ctx.add_init_script("try{ if (!localStorage.getItem('manas.personal.v1')) {} }catch(e){}")
                        pg = await ctx.new_page()
                        open(os.path.join(ROOT, '_shot.html'), 'w').write(page(cw, ch, ce if lang == 'en' else ch_, se if lang == 'en' else sh, base + 'index.html', lang))
                        await pg.goto(base + '_shot.html'); await pg.wait_for_timeout(2500)
                        fr = pg.frame_locator('#f'); f = pg.frames[1]
                        await f.evaluate(f"""async () => {{ closeTour(); const st = document.createElement('style'); st.textContent = '#toast{{display:none!important}}'; document.head.appendChild(st); S.settings.ui = '{lang}'; S.settings.layers.e = {'true' if lang == 'en' else 'false'}; S.settings.layers.w = false; applyLang(); save(); {js} }}""")
                        await pg.wait_for_timeout(1200)
                        await pg.screenshot(path=os.path.join(d, f'{n:02d}-{name}.png'))
                        await ctx.close()
                    print(store, lang, '→', os.path.relpath(d, ROOT))
            # Google Play feature graphic
            ctx = await b.new_context(viewport={'width': 1024, 'height': 500}); pg = await ctx.new_page()
            await pg.set_content(f"""<style>@font-face{{font-family:D;src:url(data:font/woff2;base64,{FONT})}}@font-face{{font-family:L;src:url(data:font/woff2;base64,{LAT})}}
              body{{margin:0;width:1024px;height:500px;background:linear-gradient(160deg,#2B3A8C,#1B2565);display:flex;align-items:center;gap:48px;padding:0 70px;box-sizing:border-box;color:#fff}}
              .om{{width:190px;height:190px;border-radius:44px;background:#2B3A8C;box-shadow:0 0 0 3px #F2A65355;display:flex;align-items:center;justify-content:center;color:#F2A653;font:700 120px/1 D}}
              h1{{font:700 64px/1.1 D;margin:0}}p{{font:600 30px/1.35 L;margin:12px 0 0;color:#F2C894}}</style>
              <div class=om>ॐ</div><div><h1>शास्त्र</h1><p>Read and listen · Hindi &amp; English meanings · word by word</p></div>""")
            await pg.wait_for_timeout(500); os.makedirs(os.path.join(OUT, 'play'), exist_ok=True)
            await pg.screenshot(path=os.path.join(OUT, 'play', 'feature-graphic.png')); await b.close()
    finally:
        os.remove(os.path.join(ROOT, '_shot.html'))
asyncio.run(main())
