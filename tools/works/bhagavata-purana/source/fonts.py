"""Download the official Noto Sans Devanagari 1.05 Regular and Bold (googlefonts/noto-fonts, tag v2015-09-29-license-adobe),
whose glyphs the Gita Press e-book PDFs embed unchanged (fontcheck.py proves it), into the current folder as Ref-*.ttf."""
import urllib.request
for w in ('Regular', 'Bold'):
    urllib.request.urlretrieve(f'https://raw.githubusercontent.com/googlefonts/noto-fonts/v2015-09-29-license-adobe/hinted/NotoSansDevanagari-{w}.ttf', f'Ref-{w}.ttf')
