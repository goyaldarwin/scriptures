"""Decode the Gita Press Hindi Vālmīki-Rāmāyaṇa PDF (code 77) to Unicode from glyph ids — no OCR,
no use of the PDF's broken ToUnicode map for Devanagari.

How it works
  * The Devanagari is set in an embedded subset of Noto Sans Devanagari Regular, Identity-H, so each
    PDF character code is a glyph id.  The embedded outlines and advances of all 254 non-empty glyphs
    are identical to the official NotoSansDevanagari-Regular.ttf version 2.000
    (googlefonts/noto-fonts, tag v2017-10-24-phase3-second-cleanup), so glyph ids mean the same as in
    that font.
  * glyphs.json (made by build_glyphs.py) gives each used glyph id its Unicode value and its role,
    settled by shaping the official font with HarfBuzz.
  * decode_run() turns one run of glyph ids (one span of the Noto font, i.e. text between two
    Times-font characters) into Unicode by rebuilding logical order:
        - a pre-base ि glyph (any width; combined ि+ं / ि+ँ / reph+ि forms) is written after the
          consonant cluster (half forms + base) that follows it;
        - a reph glyph drawn after its syllable (also combined े/ो/ी/ै/ौ+reph and reph+ं forms) is
          written as र् at the start of that syllable;
        - U+25CC dotted circles inserted by the shaper and the zero-width dummy mark are dropped.
  * Every run is checked by shaping the decoded Unicode again with the official font: the glyph id
    sequence must equal the PDF's (roundtrip()).
  * The Times New Roman spans (spaces, Latin punctuation, ‘ ’ — , ; ! ? ( ) [ ] / * etc.) are taken
    from the PDF's ToUnicode, which is correct for that font (checked: one code point per glyph id).

Usage: python3 decode.py  -> writes pages_raw.json: per page, a list of lines, each a list of
       segments {x0,x1,y,ymin,size,bold,italic,blue,noto,text,ok,gids} in reading order.
"""
import json, os, pickle, unicodedata
HERE=os.path.dirname(os.path.abspath(__file__))
G={int(k):v for k,v in json.load(open(os.path.join(HERE,'glyphs.json')))['glyphs'].items()}

class Unknown(Exception): pass

def decode_run(gids):
    """gids: glyph ids of one Noto run in visual order -> Unicode (NFC)."""
    syl=[]          # each: dict(reph, pre, cons(list), post(list), closed)
    cur=None
    def new():
        nonlocal cur
        cur=dict(reph=False,pre='',prepost='',cons=[],post=[],closed=False); syl.append(cur); return cur
    for g in gids:
        t=G.get(g)
        if t is None: raise Unknown(g)
        r=t['role']
        if r=='dummy': continue
        if r=='pre':
            s=new(); s['pre']=t['value']; s['prepost']=t.get('post',''); s['reph']=t.get('reph',False)
        elif r=='half':
            if cur is None or cur['closed']: new()
            cur['cons'].append(t['value'])
        elif r=='base':
            if cur is None or cur['closed']: new()
            cur['cons'].append(t['value']); cur['closed']=True
        elif r=='dotted':
            if cur is None or cur['closed']: new()
            cur['closed']=True
        elif r=='post':
            if cur is None: raise Unknown('mark without base')
            cur['post'].append(t['value'])
            if t.get('reph'): cur['reph']=True
        elif r=='reph':
            if cur is None: raise Unknown('reph without base')
            cur['reph']=True
            if t.get('post'): cur['post'].append(t['post'])
    out=[]
    for s in syl:
        out.append(('र्' if s['reph'] else '')+''.join(s['cons'])+s['pre']+''.join(s['post'])+s['prepost'])
    return unicodedata.normalize('NFC',''.join(out))

_shape=None
def roundtrip(text,gids):
    """True when shaping `text` with the official font gives exactly `gids`."""
    global _shape
    if _shape is None:
        from hb import shape as _s; _shape=_s
    return _shape(text)==list(gids)

def page_lines(trace_page):
    """One page of get_texttrace() data -> list of lines in content (reading) order.
    Each line is a list of segments {x0,x1,y,size,bold,italic,noto,text,ok}.  A new line starts
    when the pen jumps back to the left (> 20 pt) or moves more than 12 pt up or down (superscript
    and subscript offsets are at most 9 pt; line spacing is 15.75 pt or more): the PDF draws lines in reading order, and a
    space at a line end is not drawn, so a run of Devanagari glyphs can continue across a line
    break; it is cut there and each part is decoded separately."""
    chars=[]
    for s in trace_page:
        noto=s['font'].startswith('Noto')
        bold=(s['opacity']==0.0) or ('Bold' in s['font'])   # bold Devanagari is drawn fill+stroke (alpha 0 fill)
        blue=tuple(s['color'])!=(0.0,0.0,0.0)                # link text (contents, footnote numbers) is blue
        for c in s['chars']:
            chars.append((noto,bold,'Italic' in s['font'],s['size'],blue,c))
    lines=[]; line=None; lastx=None; lasty=None
    for ch in chars:
        noto,bold,ital,size,blue,c=ch
        x=c[2][0]; y=c[2][1]
        if line is None or x < lastx-20 or abs(y-lasty)>12:
            line=[]; lines.append(line)
        lastx=max(x,lastx) if line else x; lasty=y
        line.append(ch)
    out=[]
    for L in lines:
        segs=[]
        for ch in L:
            noto,bold,ital,size,blue,c=ch
            key=(noto,bold,ital,size,blue)
            if segs and segs[-1]['key']==key: segs[-1]['chars'].append(c)
            else: segs.append(dict(key=key,chars=[c]))
        res=[]
        for sg in segs:
            noto,bold,ital,size,blue=sg['key']; cs=sg['chars']
            if noto:
                gids=[c[1] for c in cs]
                try:
                    txt=decode_run(gids); ok=roundtrip(txt,gids)
                except Unknown:
                    txt='\ufffd'; ok=False
            else:
                gids=None; txt=''.join(chr(c[0]) for c in cs); ok=True
            res.append(dict(x0=round(cs[0][3][0],2),x1=round(cs[-1][3][2],2),y=round(cs[0][2][1],2),
                            ymin=round(min(c[2][1] for c in cs),2),size=size,bold=bold,italic=ital,blue=blue,noto=noto,text=txt,ok=ok,gids=gids))
        out.append(res)
    return out

if __name__=='__main__':
    T=pickle.load(open(os.path.join(HERE,'trace.pkl'),'rb'))
    pages=[page_lines(p) for p in T]
    json.dump(pages,open(os.path.join(HERE,'pages_raw.json'),'w'),ensure_ascii=False)
    bad=sum(1 for p in pages for l in p for s in l if not s['ok'])
    runs=sum(1 for p in pages for l in p for s in l if s['noto'])
    print('pages',len(pages),'lines',sum(map(len,pages)),'Devanagari runs',runs,'roundtrip failures',bad)
