"""App icons from one design (indigo square, saffron ॐ in Noto Serif Devanagari bold), drawn in a browser so the glyph
is the same on every device. Writes tools/store/icons/*.png; build.py copies the web ones into app/.

  icon-192.png, icon-512.png      web app / Android (rounded corners, any purpose)
  maskable-512.png                Android adaptive icon (full bleed, ॐ inside the safe zone)
  apple-touch-icon.png (180)      iPhone home screen
  store-1024.png                  App Store icon (square, no transparency; Apple rounds it)
  play-512.png                    Google Play listing icon (square; Google rounds it)
  share-card.png (1200×630)       the picture a chat app (WhatsApp …) shows under a shared link: the icon, the name, what is
                                  in the library (build.py copies it into app/ and names it in the page's og:image)
Run: python3 tools/store/make_icons.py
"""
import asyncio, base64, os
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'icons'); os.makedirs(OUT, exist_ok=True)
FONTS = os.path.join(HERE, '..', 'fonts'); FONT = os.path.join(FONTS, 'noto-serif-devanagari-devanagari-700-normal.woff2')
INDIGO, SAFFRON = '#2B3A8C', '#F2A653'
ICONS = [('icon-192.png', 192, 0.22, 0.62), ('icon-512.png', 512, 0.22, 0.62), ('maskable-512.png', 512, 0, 0.46),
         ('apple-touch-icon.png', 180, 0, 0.62), ('store-1024.png', 1024, 0, 0.58), ('play-512.png', 512, 0, 0.58)]

async def main():
    font = base64.b64encode(open(FONT, 'rb').read()).decode()
    async with async_playwright() as p:
        b = await p.chromium.launch(**({'executable_path': os.environ['CHROMIUM']} if os.environ.get('CHROMIUM') else {}))   # CHROMIUM: a browser of your own, as for the tests
        for name, px, radius, glyph in ICONS:
            pg = await b.new_page(viewport={'width': px, 'height': px})
            await pg.set_content(f"""<style>@font-face{{font-family:I;src:url(data:font/woff2;base64,{font})}}html,body{{margin:0;background:transparent}}</style>
              <canvas id=c width={px} height={px}></canvas><span style="font-family:I">ॐ</span>""")
            await pg.evaluate("document.fonts.load('700 40px I')"); await pg.wait_for_timeout(300)
            await pg.evaluate(f"""(() => {{ const c = document.getElementById('c'), x = c.getContext('2d'), s = {px}, r = {radius} * s;
              x.fillStyle = '{INDIGO}'; x.beginPath(); x.roundRect(0, 0, s, s, r); x.fill();
              x.font = '700 ' + ({glyph} * s) + 'px I'; x.fillStyle = '{SAFFRON}'; x.textAlign = 'center'; x.textBaseline = 'alphabetic';
              const m = x.measureText('ॐ'), h = m.actualBoundingBoxAscent + m.actualBoundingBoxDescent, w = m.actualBoundingBoxLeft + m.actualBoundingBoxRight;
              x.fillText('ॐ', s / 2 - (m.actualBoundingBoxRight - m.actualBoundingBoxLeft) / 2, s / 2 + (m.actualBoundingBoxAscent - m.actualBoundingBoxDescent) / 2); }})()""")
            el = await pg.query_selector('#c'); await el.screenshot(path=os.path.join(OUT, name), omit_background=radius > 0)
            await pg.close()
        # the link card: wide, light, the icon on the left, the name and the library's contents beside it (Hindi, then English)
        css = ''.join(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode(open(os.path.join(FONTS, f), 'rb').read()).decode()})}}"
                      for fam, w, f in [('D', 400, 'noto-serif-devanagari-devanagari-400-normal.woff2'), ('D', 700, 'noto-serif-devanagari-devanagari-700-normal.woff2'),
                                        ('L', 400, 'literata-latin-400-normal.woff2'), ('L', 600, 'literata-latin-600-normal.woff2'),
                                        ('L', 400, 'literata-latin-ext-400-normal.woff2'), ('L', 600, 'literata-latin-ext-600-normal.woff2')])
        icon = base64.b64encode(open(os.path.join(OUT, 'icon-512.png'), 'rb').read()).decode()
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        await pg.set_content(f"""<style>{css}html,body{{margin:0}}body{{width:1200px;height:630px;background:#F6F6F2;display:flex;align-items:center;gap:56px;padding:0 70px;box-sizing:border-box;font-family:L,D,serif;color:#1D1C1A}}
          img{{width:300px;height:300px;flex:none}}h1{{font:700 76px/1.15 D,L,serif;color:{INDIGO};margin:0 0 22px}}h1 span{{font-family:L,serif;font-weight:600}}
          p{{margin:0 0 14px;font-size:31px;line-height:1.35}}.hi{{font-family:D,serif}}.free{{color:#C9741C;font-weight:600;margin-top:22px}}</style>
          <img src="data:image/png;base64,{icon}"><div><h1>शास्त्र · <span>Scriptures</span></h1>
          <p class="hi" style="font-size:27px;white-space:nowrap">श्रीरामचरितमानस · सुन्दरकाण्ड · हनुमान चालीसा · उपनिषद् · आरती</p>
          <p>Text, Hindi and English meanings, the meaning of every word, recitation audio</p>
          <p class="free"><span class="hi">निःशुल्क, बिना विज्ञापन</span> · Free, no ads</p></div>""")
        await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(500)
        await pg.screenshot(path=os.path.join(OUT, 'share-card.png')); await pg.close()
        await b.close()
    print('icons →', os.path.relpath(OUT))
asyncio.run(main())
