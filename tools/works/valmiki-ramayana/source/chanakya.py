"""Chanakya (Gita Press legacy font) text layer → Unicode Devanagari, read directly (no OCR).

The PDF's text layer gives each glyph as the Mac Roman character of its font code ('¤' for 219).
Each code was read from the glyph shape of the font embedded in the PDF (sheets rendered from its
outlines: `glyphsheet.py`) and confirmed by the words it occurs in. Some glyphs are pieces that only
make sense with others: the prebase ि, the reph written after its syllable, half forms completed by
the ā bar (or by the bar inside ो / ौ), ई as इ with a hook, ऐ as ए with a sign, ॄ as two ृ, and an
anusvāra typed inside a conjunct. `decode` puts them in Unicode order.
"""
import re, unicodedata

PRE_I, PRE_I_REPH, REPH, REPH_M, PRE_I_M, PRE_I_REPH_M, FLOAT_M, FLOAT_CB = '\x01\x02\x03\x04\x05\x06\x07\x08'
MARKERS = PRE_I + PRE_I_REPH + REPH + REPH_M + PRE_I_M + PRE_I_REPH_M + FLOAT_M + FLOAT_CB

# code (Mac Roman byte) → Unicode; '' = a spacer glyph with no letter.
CODE = {
    32: ' ', 35: 'प्त', 37: 'त्न', 40: '(', 41: ')', 42: '*', 44: ',', 45: '-', 46: '.',
    48: '०', 49: '१', 50: '२', 51: '३', 52: '४', 53: '५', 54: '६', 55: '७', 56: '८', 57: '९',
    59: ';', 64: 'ञ्च', 65: '्न', 67: 'ष्ट', 68: 'ष्ठ', 69: 'श्व', 70: 'स्न', 72: '॥', 75: '्य',
    76: 'रु', 77: 'रू', 78: 'हृ', 79: 'ह्र', 81: 'क्त', 83: 'स्', 84: 'ञ्ज', 85: '', 86: 'ङ्क',
    87: 'ङ्ख', 88: 'ङ्ग', 89: 'ङ्घ', 90: REPH_M, 91: '[', 93: ']', 94: 'ट्ट', 96: 'क्व', 99: 'ष्',
    100: 'स्र', 101: 'द्ग', 103: 'द्द', 104: 'द्ध', 105: 'द्ब', 106: 'द्भ', 107: 'द्म', 108: 'द्य',
    109: 'द्व', 111: 'श', 112: 'श्च', 113: 'ह्न', 114: 'ह्म्', 115: 'ह्य', 116: 'ह्ल', 117: 'ह्व',
    118: '1', 119: '2', 120: '3', 121: '4', 122: '5', 123: '6', 124: '7', 125: '8', 126: '9', 174: '0',
    128: 'क्', 129: 'ख्', 130: 'ग्', 131: 'घ्', 132: 'ल्ल', 133: 'ज्', 134: 'ञ्', 135: 'ण्',
    136: 'त्', 137: 'थ्', 138: 'ध्', 139: 'न्', 140: 'प्', 141: 'फ्', 142: 'ब्', 143: 'भ्',
    144: 'म्', 145: 'च्', 147: 'च्च्', 148: 'ज्ज्', 151: '—', 152: 'त्र्', 153: 'ज्ञ्', 158: 'त्त्',
    159: 'श्र्', 161: 'ँ', 162: 'ं', 164: '', 165: 'अ', 166: 'ष्ट्व', 167: 'इ', 168: PRE_I_M,
    169: 'उ', 170: 'ऊ', 171: 'ऋ', 176: 'ए', 180: 'ं', 181: 'द्ब्र', 183: 'क', 185: 'ख', 187: 'ग',
    188: 'द', 190: 'ङ', 191: 'च', 192: 'छ', 193: 'ज', 194: 'प', 195: 'व्', 196: 'य्', 197: 'ट',
    198: 'ठ', 199: 'ड', 200: 'फ', 201: 'ढ', 203: 'ल्', 204: 'त', 205: 'थ', 206: 'द', 207: 'ध',
    208: '।', 209: 'ः', 210: '‘', 211: '’', 212: 'े', 213: 'ब', 214: 'भ', 215: 'म', 216: 'य',
    217: 'न', 218: 'र', 219: 'झ्', 220: 'ल', 223: 'व', 224: 'श्', 225: 'ष', 226: 'स', 227: 'ह',
    228: 'ु', 229: 'ू', 230: 'ा', 231: PRE_I, 232: 'ी', 233: 'ु', 234: 'ू', 235: 'ृ',
    236: PRE_I_REPH_M, 237: PRE_I_REPH, 239: '', 240: 'े', 241: 'ै', 243: 'न्न्', 244: 'ो', 245: 'ौ',
    246: 'ह्ण', 247: '्', 249: 'ऽ', 250: 'ॐ', 252: REPH, 253: '्र', 254: '्र', 255: 'क्ष्',
}

def byte(ch):
    return 219 if ch == '¤' else ch.encode('mac_roman')[0]

C = '[क-हळ]'
CLUS = f'(?:{C}्)*{C}'
SIGNS = 'ािीुूृॄेैोौ'

def dedupe(chars, xs, tol=0.6):
    """Drop a glyph printed again at the same place (the PDF overprints some glyphs)."""
    out = []
    for c, x in zip(chars, xs):
        if any(c == c2 and abs(x - x2) < tol for c2, x2 in out[-4:]):
            continue
        out.append((c, x))
    return ''.join(c for c, _ in out)

NO_START = set('ािीुूृॄेैोौंँः्') | {REPH, REPH_M}

def drop_inner_spaces(raw):
    """A space inside a word (justification) after a half form or prebase mark, or before a sign, is dropped."""
    toks = [CODE[byte(c)] for c in raw]
    keep = []
    for i, c in enumerate(raw):
        if c == ' ':
            prev = next((toks[j] for j in range(i - 1, -1, -1) if toks[j] not in (' ', '')), None)
            nxt = next((toks[j] for j in range(i + 1, len(toks)) if toks[j] not in (' ', '')), None)
            if prev is not None and nxt is not None and (
                    (prev.endswith('्') and prev != '्') or prev in (PRE_I, PRE_I_M, PRE_I_REPH, PRE_I_REPH_M)
                    or nxt in NO_START or nxt.startswith('्')):
                continue
        keep.append(c)
    return ''.join(keep)

def decode(raw):
    parts = []
    for ch in drop_inner_spaces(raw):
        t = CODE[byte(ch)]          # KeyError = a code not in the table: stop, never guess
        last = next((x for x in reversed(parts) if x != ''), '')
        if t in ('ं', 'ँ') and last.endswith('्') and last != '्':
            t = FLOAT_M if t == 'ं' else FLOAT_CB   # typed inside a conjunct
        if t in ('ा', 'ो', 'ौ'):
            j = len(parts) - 1
            while j >= 0 and parts[j] in (FLOAT_M, FLOAT_CB, ''):
                j -= 1
            if j >= 0 and parts[j].endswith('्') and parts[j] != '्':
                # the bar completes the half form; ो / ौ glyphs are the bar with े / ै on it
                parts[j] = parts[j][:-1] + {'ा': '', 'ो': 'े', 'ौ': 'ै'}[t]
                # a nasal typed between the half form and its bar sits on the completed letter
                for k in range(j + 1, len(parts)):
                    parts[k] = {FLOAT_M: 'ं', FLOAT_CB: 'ँ'}.get(parts[k], parts[k])
                continue
        parts.append(t)
    s = ''.join(parts)
    s = (s.replace('ाे', 'ो').replace('ाै', 'ौ').replace('अा', 'आ').replace('अो', 'ओ').replace('अौ', 'औ')
          .replace('एे', 'ऐ').replace('ृृ', 'ॄ').replace('््र', '्र्').replace('््', '्'))
    s = re.sub('([ंँ])(्' + C + ')', r'\2\1', s)           # ग ं ्न = ग्नं (ं typed before a subscript letter)
    s = s.replace('इ' + REPH_M, 'ईं').replace('इ' + REPH, 'ई')
    s = s.replace(PRE_I + 'ं', PRE_I_M).replace(PRE_I_REPH + 'ं', PRE_I_REPH_M)   # ि then ं typed apart
    # a reph typed after a half letter belongs before the whole conjunct (मूर्च्छित, मूर्ध्नि)
    s = re.sub('((?:' + C + '्)+)' + REPH, 'र्' + r'\1', s)
    # a floating candrabindu nasalises the vowel before the half letters; a floating anusvara goes after the cluster
    s = re.sub('((?:' + C + '्)+)' + FLOAT_CB, 'ँ' + r'\1', s)
    s = re.sub(FLOAT_M + '((?:' + C + '्)*' + C + ')', r'\1' + FLOAT_M, s)
    s = re.sub(PRE_I + '(' + CLUS + ')', r'\1ि', s)
    s = re.sub(PRE_I_M + '(' + CLUS + ')', r'\1िं', s)
    s = re.sub(PRE_I_REPH + '(' + CLUS + ')', r'र्\1ि', s)
    s = re.sub(PRE_I_REPH_M + '(' + CLUS + ')', r'र्\1िं', s)
    s = re.sub(FLOAT_M + '([' + SIGNS + ']*)', r'\1ं', s)
    s = re.sub('(' + CLUS + '|ऋ)([' + SIGNS + ']*)' + REPH, r'र्\1\2', s)
    s = re.sub('(' + CLUS + '|ऋ)([' + SIGNS + ']*)' + REPH_M, r'र्\1\2ं', s)
    s = re.sub('([ुूेैं])्र', r'्र\1', s)              # छ ु ्र = छ्रु, प े ्र = प्रे, घ ं ्र = घ्रं
    s = re.sub('ि(' + CLUS + ')ंः', r'िं\1ः', s)         # त्रि ं शः: no syllable ends ंः
    s = re.sub('([ंँ])([' + SIGNS + '])', r'\2\1', s)  # रं typed र ं (bar piece)
    return unicodedata.normalize('NFC', s)

V = 'ािीुूृॄेैोौ'
def problems(s):
    """Reasons a decoded string is not well-formed Devanagari."""
    r = []
    if any(c in MARKERS for c in s) or re.search(r'\?.', s): r.append('unplaced mark')
    if re.search('[' + V + '][' + V + ']', s): r.append('two vowel signs')
    if re.search('(^|[^क-हळ])[' + V + '्]', s): r.append('sign without consonant')
    if re.search('्[' + V + 'ंँः]', s): r.append('sign after halant')
    if re.search('[अआइईउऊऋएऐओऔ][' + V + ']', s): r.append('vowel sign after a vowel')
    if re.search('([ंँः])[ंँः]', s): r.append('two nasal/visarga marks')
    if re.search('ञ्[^चछजझश]', s): r.append('nasal before a stop of another class')
    return r
