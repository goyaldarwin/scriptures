import uharfbuzz as hb
_F={}
def font(bold=False):
    k='Ref-Bold.ttf' if bold else 'Ref-Regular.ttf'
    if k not in _F:
        blob=hb.Blob.from_file_path(k); face=hb.Face(blob); _F[k]=hb.Font(face)
    return _F[k]
def shape(text,bold=False):
    b=hb.Buffer(); b.add_str(text); b.guess_segment_properties()
    b.direction='ltr'; b.script='Deva'; b.language='hi'
    hb.shape(font(bold),b,{})
    return [g.codepoint for g in b.glyph_infos]
