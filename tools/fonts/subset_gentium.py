"""The transliteration's font: Gentium Book Plus 6.200 (SIL, OFL: gentium-LICENSE.txt), cut down to the letters the
library's transliterations use, so the reader downloads ~25 KB, not 1 MB.

    python3 tools/fonts/subset_gentium.py <folder with GentiumBookPlus-Regular.ttf and GentiumBookPlus-Italic.ttf>

The folder is the release zip from GitHub (github.com/silnrsi/font-gentium/releases, v6.200), unpacked. Writes
gentium-tr-regular.woff2 and gentium-tr-italic.woff2 here, and gentium-tr.chars: every character they hold, which
tools/site/library.py reads to refuse a transliteration that uses a character the font lacks (it would be drawn in
another font, and a combining accent of a Vedic text could sit apart from its vowel). Run it again when a new letter
or mark appears in a transliteration (the check names it).
"""
import glob, json, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))

def used():
    """Every Latin character and mark of every transliteration in the library, and the ISO 15919 letters besides."""
    out = set(chr(c) for c in range(0x20, 0x7f)) | set('āīūēōṛṝḷḹṁṃḥṅñṭḍṇśṣm̐r̥l̥ïüŏ’‘“”—–…ꞌ') | {chr(c) for c in range(0x300, 0x370)}
    for f in glob.glob(os.path.join(REPO, 'library', '**', '*.json'), recursive=True):
        try: w = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for it in (w.get('items') or []) if isinstance(w, dict) else []:
            t = it.get('t') or []
            for ch in ''.join(t if isinstance(t, list) else [t]):
                if ord(ch) < 0x900 or 0x1e00 <= ord(ch) <= 0x2bff: out.add(ch)
    return out

def main(src):
    chars = used(); have = set()
    for style, name in (('regular', 'GentiumBookPlus-Regular.ttf'), ('italic', 'GentiumBookPlus-Italic.ttf')):
        font = TTFont(os.path.join(src, name))
        cmap = font.getBestCmap(); keep = sorted(ord(c) for c in chars if ord(c) in cmap)
        o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True
        s = subset.Subsetter(o); s.populate(unicodes=keep); s.subset(font)
        font.flavor = 'woff2'; font.save(os.path.join(HERE, f'gentium-tr-{style}.woff2'))
        have = set(keep) if not have else have & set(keep)
    open(os.path.join(HERE, 'gentium-tr.chars'), 'w', encoding='utf-8').write(''.join(chr(c) for c in sorted(have)) + '\n')
    print(f'{len(have)} characters; not in Gentium: {"".join(sorted(c for c in chars if ord(c) not in have)) or "none"}')

if __name__ == '__main__': main(sys.argv[1])
