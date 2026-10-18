"""App icons from one design (indigo square, saffron ॐ in Noto Serif Devanagari bold), drawn in a browser so the glyph
is the same on every device. Writes tools/store/icons/*.png; build.py copies the web ones into app/.

  icon-192.png, icon-512.png      web app / Android (rounded corners, any purpose)
  maskable-512.png                Android adaptive icon (full bleed, ॐ inside the safe zone)
  apple-touch-icon.png (180)      iPhone home screen
  store-1024.png                  App Store icon (square, no transparency; Apple rounds it)
  play-512.png                    Google Play listing icon (square; Google rounds it)
Run: python3 tools/store/make_icons.py
"""
import asyncio, base64, os
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'icons'); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, '..', 'fonts', 'noto-serif-devanagari-devanagari-700-normal.woff2')
INDIGO, SAFFRON = '#2B3A8C', '#F2A653'
ICONS = [('icon-192.png', 192, 0.22, 0.62), ('icon-512.png', 512, 0.22, 0.62), ('maskable-512.png', 512, 0, 0.46),
         ('apple-touch-icon.png', 180, 0, 0.62), ('store-1024.png', 1024, 0, 0.58), ('play-512.png', 512, 0, 0.58)]

async def main():
    font = base64.b64encode(open(FONT, 'rb').read()).decode()
    async with async_playwright() as p:
        b = await p.chromium.launch()
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
        await b.close()
    print('icons →', os.path.relpath(OUT))
asyncio.run(main())
