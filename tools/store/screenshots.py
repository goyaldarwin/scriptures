"""Store screenshots, made from the real app (the site in this repository) with a caption above each.

  python3 tools/store/screenshots.py [--lang en|hi|both]   →  tools/store/out/<store>/<lang>/NN-<scene>.png

Sizes: App Store iPhone 6.9" (1320×2868), Google Play phone (1080×1920) and tablets (7-inch 1080×1920, 10-inch
1440×2560), plus the Play feature graphic (1024×500).
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
 ('play', 'Listen, hands-free', 'सुनते हुए पढ़ें', 'The verse being recited is highlighted and the page auto-scrolls to the next verse with the recitation', 'जो पद गाया जा रहा है वह हाइलाइट होता है, और पाठके साथ पन्ना अपने आप अगले पदपर बढ़ता है',
  """await openWork('sundarkand'); S.settings.layers.h = true; syncLayers();
     openReader('k', ID['chalisa.cau1']); await new Promise(r => setTimeout(r, 900));
     const i = ID['chalisa.cau2']; PL.on = true; PL.t = 0; PL.cur = -1; $('#player').hidden = false; document.body.classList.add('playing');
     $('#ytBox').innerHTML = '<div style="width:200px;height:200px;border-radius:12px;background:#FBF3E4;border:1px solid #EAD9BC;display:flex;align-items:center;justify-content:center;color:#D9822B;font:700 72px serif">ॐ</div>';
     setCur(i); $('#pProg').style.width = '34%'; syncPlayer = () => {}; $('#pPlay').innerHTML = '<svg><use href="#i-pause"/></svg>';"""),
 ('word', 'Tap any word for its meaning', 'किसी भी शब्दको छूकर अर्थ देखें', 'Meaning, root and grammar of every word', 'हर शब्दका अर्थ, मूल शब्द और व्याकरण',
  """await openWork('sundarkand'); S.settings.layers.h = false; S.settings.layers.e = false; syncLayers(); openReader('k', ID['chalisa.cau5']); await new Promise(r => setTimeout(r, 900));
     const w = [...document.querySelectorAll('#rBody .verse .vtext .w')].find(x => x.getBoundingClientRect().top > 160); w.click();"""),
 ('meanings', 'Hindi and English meanings', 'हिंदी और अंग्रेज़ी अर्थ', 'Under every verse — switch each on or off', 'हर पदके नीचे — जो चाहें वही दिखाएँ',
  """await openWork('sundarkand'); S.settings.layers.h = true; S.settings.layers.e = true; syncLayers(); openReader('k', ID['chalisa.do1']); await new Promise(r => setTimeout(r, 900));"""),
 ('verse', 'Play one verse — or from any verse', 'एक पद सुनें — या कहींसे भी', '▶ beside a verse plays just that one; “Listen from here” goes on', 'पदके पास ▶ केवल वही पद; “यहाँसे सुनें” आगे तक',
  """await openWork('sundarkand'); S.settings.layers.h = true; syncLayers(); openReader('k', ID['chalisa.cau9']); await new Promise(r => setTimeout(r, 900));
     const v = [...document.querySelectorAll('#rBody .verse')].find(x => x.getBoundingClientRect().top > 300); itemMenu(+v.dataset.i);"""),
 ('plans', '30-day and 9-day readings', '३० दिन और ९ दिनका पाठ', 'Your progress and place are kept', 'प्रगति और स्थान याद रहता है',
  """await openWork('manas'); WS().org = PLANS[0] ? PLANS[0].id : 'k'; show('home'); renderHome(); window.scrollTo(0, 0);"""),
 ('library', 'A growing library', 'बढ़ता हुआ पुस्तकालय', 'Rāmacaritamānasa, Sundarakāṇḍa, Śrī Rudram, Sukhmani Sahib and more', 'रामचरितमानस, सुन्दरकाण्ड, श्रीरुद्रम्, सुखमनी साहिब और भी',
  """libPath = []; show('library'); renderLibrary(); window.scrollTo(0, 0);"""),
]
# Only verses whose meanings are our own appear in store pictures (the opening prayers, the Chālīsā), never a
# copyrighted meaning. (css width, css height, scale, width of the app inside the frame)
# Play tablets: 7-inch 1080×1920, 10-inch 1440×2560 (9:16), the app at tablet width.
SIZES = {'appstore': (440, 956, 3, 390), 'play': (360, 640, 3, 390), 'play-tablet7': (540, 960, 2, 540), 'play-tablet10': (720, 1280, 2, 680)}

def page(cw, ch, cap, sub, url, lang, aw=390):
    top = 0.2 * ch; fw = cw * 0.86; scale = fw / aw; fh = (ch - top - 0.02 * ch) / scale
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:D;src:url(data:font/woff2;base64,{FONT})}}@font-face{{font-family:L;src:url(data:font/woff2;base64,{LAT})}}
html,body{{margin:0;width:{cw}px;height:{ch}px;overflow:hidden;background:radial-gradient(120% 70% at 50% 0%,#FFFDF8 0%,#F7EFE1 55%,#EFE3CC 100%)}}
.cap{{position:absolute;top:0;left:0;right:0;height:{top}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 20px;color:#26307A}}
.cap b{{font:600 {0.072 * cw if lang == 'en' else 0.068 * cw}px/1.2 {'L' if lang == 'en' else 'D'},serif}}.cap span{{margin-top:8px;font:400 {0.036 * cw}px/1.35 {'L' if lang == 'en' else 'D'},serif;color:#A4561A}}
.ph{{position:absolute;top:{top}px;left:{(cw - fw) / 2}px;width:{aw}px;height:{fh}px;transform:scale({scale});transform-origin:0 0;border-radius:{34 / scale}px;overflow:hidden;
    box-shadow:0 0 0 {5 / scale}px #2A2A35,0 18px 44px rgba(80,50,10,.22);background:#F6F6F2}}
iframe{{border:0;width:{aw}px;height:{fh}px}}</style></head><body>
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
            for store, (cw, ch, dpr, aw) in SIZES.items():
                for lang in langs:
                    d = os.path.join(OUT, store, lang); os.makedirs(d, exist_ok=True)
                    for n, (name, ce, ch_, se, sh, js) in enumerate(SCENES, 1):
                        ctx = await b.new_context(viewport={'width': cw, 'height': ch}, device_scale_factor=dpr)
                        # a fresh reader: tour seen, the chosen interface language
                        await ctx.add_init_script("try{ if (!localStorage.getItem('manas.personal.v1')) {} }catch(e){}")
                        pg = await ctx.new_page()
                        await pg.add_init_script('window.__SALUTE_MS = 0')   # the 1.5 s greeting is tested on its own
                        open(os.path.join(ROOT, '_shot.html'), 'w').write(page(cw, ch, ce if lang == 'en' else ch_, se if lang == 'en' else sh, base + 'index.html', lang, aw))
                        await pg.goto(base + '_shot.html'); await pg.wait_for_timeout(2500)
                        fr = pg.frame_locator('#f'); f = pg.frames[1]
                        await f.evaluate(f"""async () => {{ closeTour(); const st = document.createElement('style'); st.textContent = '#toast{{display:none!important}}'; document.head.appendChild(st); S.settings.ui = '{lang}'; S.settings.layers.e = {'true' if lang == 'en' else 'false'}; S.settings.layers.w = false; applyLang(); save(); {js} }}""")
                        await pg.wait_for_timeout(1200)
                        await pg.screenshot(path=os.path.join(d, f'{n:02d}-{name}.png'))
                        await ctx.close()
                    print(store, lang, '→', os.path.relpath(d, ROOT))
            # Google Play feature graphic, one per listing language, with the app's store name
            for lang, title, line in (('en', 'Sunderkand &amp; Ramcharitmanas', 'Read and listen · Hindi &amp; English meanings · word by word'),
                                      ('hi', 'सुंदरकांड और रामचरितमानस', 'पढ़ें और सुनें · हिंदी और अंग्रेज़ी अर्थ · शब्द-शब्दका अर्थ')):
              ctx = await b.new_context(viewport={'width': 1024, 'height': 500}); pg = await ctx.new_page()
              await pg.set_content(f"""<style>@font-face{{font-family:D;src:url(data:font/woff2;base64,{FONT})}}@font-face{{font-family:L;src:url(data:font/woff2;base64,{LAT})}}
              body{{margin:0;width:1024px;height:500px;background:radial-gradient(120% 120% at 20% 30%,#FFFDF8 0%,#F7EFE1 55%,#EFE3CC 100%);display:flex;align-items:center;gap:48px;padding:0 70px;box-sizing:border-box;color:#26307A}}
              .om{{width:190px;height:190px;border-radius:44px;background:#2B3A8C;box-shadow:0 0 0 3px #F2A65355;display:flex;align-items:center;justify-content:center;color:#F2A653;font:700 120px/1 D}}
              h1{{font:700 {'52px' if lang == 'en' else '56px'}/1.15 {'L' if lang == 'en' else 'D'};margin:0}}p{{font:600 28px/1.35 {'L' if lang == 'en' else 'D'};margin:14px 0 0;color:#A4561A}}</style>
              <div class=om>ॐ</div><div><h1>{title}</h1><p>{line}</p></div>""")
              await pg.wait_for_timeout(500); os.makedirs(os.path.join(OUT, 'play'), exist_ok=True)
              await pg.screenshot(path=os.path.join(OUT, 'play', f'feature-graphic-{lang}.png')); await ctx.close()
            await b.close()
    finally:
        os.remove(os.path.join(ROOT, '_shot.html'))
asyncio.run(main())
