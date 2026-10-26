"""The library's writing standard for verses, in one place (docs/PLAYBOOK.md §3 "How verses are written").

Every work's exporter passes its items through `apply(items, work_lang, yajur)` before writing `work.json`, and
tools/site/library.py refuses an item that does not already equal what `apply` makes, so no work can differ.

1. The double daṇḍa is the Unicode character ॥ (U+0965), never two single daṇḍas; a verse number sits inside it
   with no spaces: ॥१॥. All languages.
2. Sanskrit verses (language `sa`) follow Pāṇini:
   - ॐ for the sacred syllable (ओं, ओम् standing alone become ॐ; the Vedic pluta ओ३म् is kept as printed);
   - inside a word, a nasal before a stop is the nasal of that stop's class, written as the letter (8.4.58):
     सङ्कल्प, पञ्च, दण्ड, अन्त, कम्प — never the dot;
   - a word-final m stays म् at a pause (before । or ॥) and before a vowel; it becomes ं only before a consonant
     (8.3.23): दारुणम् । · अलक्षणम् अचिन्त्यम् · रामं वन्दे;
   - in the Yajurveda's texts (`yajur`), the anusvāra before श ष स ह र is written ꣳ, as the Yajurveda recites it;
     elsewhere ꣳ is written ं (the other traditions recite it as anusvāra). ꣳ typed as ग्ं is written ꣳ.
   The avagraha ऽ cannot be added by rule (it needs the words split); `avagraha_candidates` lists places to check.
3. The Roman transliteration (`t`) of every Devanagari verse is ISO 15919, made from the verse itself (`iso`): every
   letter written, every inherent a written; ऋ r̥, ड़ ṛ, anusvāra ṁ, candrabindu m̐, visarga ḥ, avagraha ’, ꣳ gͫ; इ उ after an a
   are ï ü (गउ gaü, never gau = गौ).
   Vedic accents stay on the vowel of their syllable: udātta ॑ → ◌̍, anudātta ॒ → ◌̠, double svarita ᳚ → ◌̎.
   A daṇḍa inside or at the end of a line is ",", a line ending in ॥ ends with "." (a line that opens with ॥ also
   closes with it), and a verse number is " ॥N॥" (Latin digits; Gurbani's chain ॥੮॥੧੧॥ stays a chain, ॥8॥11॥).
   Gurmukhi is transliterated the same way, letter for letter (`gurmukhi`: each Gurmukhi letter is its Devanagari twin;
   tippi and bindi ṁ, addak doubles the next consonant, yakash y, ੴ ik oaṅkār).
"""
import re

SVARA = re.compile('[॑-॔᳐-᳿꣠-꣱]')
DEV_DIG = '०१२३४५६७८९'
STOPS = {'क': 'ङ', 'ख': 'ङ', 'ग': 'ङ', 'घ': 'ङ', 'च': 'ञ', 'छ': 'ञ', 'ज': 'ञ', 'झ': 'ञ', 'ट': 'ण', 'ठ': 'ण', 'ड': 'ण',
         'ढ': 'ण', 'त': 'न', 'थ': 'न', 'द': 'न', 'ध': 'न', 'प': 'म', 'फ': 'म', 'ब': 'म', 'भ': 'म'}
USHMAN_R = set('शषसहर')
VOWELS = set('अआइईउऊऋॠऌॡएऐओऔ')
MARKS = SVARA.pattern[1:-1]


# ---- 1. daṇḍas (every language) ----
def dandas(line):
    """।। → ॥; a number inside the double daṇḍa without spaces; one space before a daṇḍa that follows a word."""
    l = line.replace('।।', '॥')
    l = re.sub(r'॥[ \t]*([०-९0-9੦-੯][^॥]*?)[ \t]*॥', r'॥\1॥', l)
    l = re.sub(r'(?<=[^\s०-९0-9੦-੯॥)])[ \t]*(॥|।)', r' \1', l)   # not inside a number (॥१॥, ॥३ (क)॥)
    return re.sub(r'[ \t]+', ' ', l).strip()


# ---- 2. Sanskrit (Pāṇini) ----
def _next_letter(s, i):
    """The next character after position i that is not a Vedic accent mark ('' at the end)."""
    i += 1
    while i < len(s) and SVARA.match(s[i]): i += 1
    return s[i] if i < len(s) else ''

def sanskrit(line, yajur=False):
    line = line.replace('ग्ं', 'ꣳ')   # ꣳ as typed in some sources (shlokam.org): ग् + ं
    toks = line.split(' ')
    out = []
    for k, tok in enumerate(toks):
        bare = SVARA.sub('', tok)
        if bare in ('ओं', 'ओम्'): tok = 'ॐ'
        s = list(tok)
        for i, ch in enumerate(s):
            if ch != 'ं': continue
            nx = _next_letter(tok, i)
            if nx in STOPS: s[i] = STOPS[nx] + '्'                       # inside a word: the class nasal
            elif yajur and nx in USHMAN_R: s[i] = 'ꣳ'
            elif nx == '':                                                # word-final: look at what follows
                nxt = next((t for t in toks[k + 1:] if t), '')
                first = SVARA.sub('', nxt)[:1]
                if first in ('।', '॥') or first in VOWELS: s[i] = 'म्'
                elif yajur and first in USHMAN_R: s[i] = 'ꣳ'
        out.append(''.join(s))
    l = ' '.join(out)
    return l if yajur else l.replace('ꣳ', 'ं')   # ꣳ belongs to the Yajurveda's recitation only

_FOLD_NASAL = re.compile('[ङञणनम]्(?=[' + ''.join(STOPS) + '])')

def fold(w):
    """A word's lookup form, so that the spellings the standard chooses between are one word in the dictionaries:
    a class nasal before its stop, ꣳ (also as typed, ग्ं) and a word-final म् all become ं (गङ्गा · गंगा,
    इदम् · इदं). The app's fold() in tools/site/app.js is the same rule."""
    return re.sub('म्$', 'ं', _FOLD_NASAL.sub('ं', w.replace('ग्ं', 'ं').replace('ꣳ', 'ं')))

def avagraha_candidates(line):
    """Places where an a may have been dropped after -e/-o without ऽ (to check by eye, never changed by rule)."""
    return [m.start() for m in re.finditer(r'(?<=[ऀ-ॿ])[ोे](?=अ)', line)]


# ---- 3. ISO 15919 ----
_V = {'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 'ऋ': 'r̥', 'ॠ': 'r̥̄', 'ऌ': 'l̥', 'ॡ': 'l̥̄',
      'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'ऍ': 'ê', 'ऑ': 'ô'}
_M = {'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū', 'ृ': 'r̥', 'ॄ': 'r̥̄', 'ॢ': 'l̥', 'ॣ': 'l̥̄', 'े': 'e', 'ै': 'ai',
      'ो': 'o', 'ौ': 'au', 'ॅ': 'ê', 'ॉ': 'ô'}
_C = {'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ', 'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
      'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ', 'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
      'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'ळ': 'ḷ', 'व': 'v',
      'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h'}
_NUKTA = {'क': 'q', 'ख': 'k͟h', 'ग': 'ġ', 'ज': 'z', 'फ': 'f', 'ड': 'ṛ', 'ढ': 'ṛh', 'य': 'ẏ'}
_PRE = {'क़': 'क़', 'ख़': 'ख़', 'ग़': 'ग़', 'ज़': 'ज़', 'ड़': 'ड़', 'ढ़': 'ढ़', 'फ़': 'फ़', 'य़': 'य़'}
_SIGN = {'ं': 'ṁ', 'ँ': 'm̐', 'ः': 'ḥ', 'ऽ': '’', 'ꣳ': 'gͫ', 'ॐ': 'oṁ', '॰': '.', '३': '3'}
_ACCENT = {'\u0951': '\u030d', '\u0952': '\u0320', '\u1cda': '\u030e'}
_VOWEL_OUT = set(_V.values()) | set(_M.values()) | {'a'}

def iso_word(w):
    for a, b in _PRE.items(): w = w.replace(a, b)
    w = w.replace('\u200c', '').replace('\u200d', '')
    if w == 'ੴ': return 'ik oaṅkār'
    out, i = [], 0
    while i < len(w):
        ch = w[i]
        if SVARA.match(ch):   # a Vedic accent: on the vowel of the syllable just written
            mark = _ACCENT.get(ch)
            k = max((j for j, o in enumerate(out) if o in _VOWEL_OUT), default=None)
            if mark and k is not None: out[k] += mark
            i += 1; continue
        if ch in _C:
            if w[i + 1:i + 2] == '़' and ch in _NUKTA: out.append(_NUKTA[ch]); i += 2
            else: out.append(_C[ch]); i += 1
            nx = w[i:i + 1]
            if nx == '्': i += 1; continue
            if nx in _M: out.append(_M[nx]); i += 1; continue
            out.append('a'); continue
        if ch in _V:   # इ उ after an a are ï ü, so that a-i, a-u never read as ai, au (ऐ, औ)
            out.append({'i': 'ï', 'u': 'ü'}.get(_V[ch], _V[ch]) if out and out[-1].endswith('a') and _V[ch] in ('i', 'u') else _V[ch])
        elif ch in _SIGN: out.append(_SIGN[ch])
        elif ch in DEV_DIG: out.append(str(DEV_DIG.index(ch)))
        else: out.append(ch)
        i += 1
    return ''.join(out)

# Gurmukhi: its letters sit 0x100 above their Devanagari twins in Unicode; the marks of its own are mapped here
_GUR = {'\u0a70': 'ं', '\u0a02': 'ं', '\u0a75': '्य', '\u0a51': '', 'ੴ': 'ੴ'}

def gurmukhi(s):
    """Gurmukhi → Devanagari letter for letter, for the transliteration (addak ੱ doubles the next consonant)."""
    s = re.sub('\u0a71(.)', lambda m: gurmukhi(m.group(1)) + '्' + gurmukhi(m.group(1)), s)
    out = []
    for ch in s:
        c = ord(ch)
        if ch in _GUR: out.append(_GUR[ch])
        elif 0x0a01 <= c <= 0x0a6f: out.append(chr(c - 0x100))
        else: out.append(ch)
    return ''.join(out)

def iso_line(l, n=None):
    """One Devanagari verse line → ISO 15919. n: a caupāī's or chhand's number, printed after its last line when the
    line ends in a bare ॥ (the Mānas prints the number at the end of the caupāī and the chhand)."""
    l = dandas(l)
    m = re.search(r'\s*((?:॥[०-९0-9][^॥]*)+)॥$', l)
    if not m and n and l.endswith('॥'): l = l[:-1].rstrip() + ' ॥' + str(n) + '॥'; m = re.search(r'\s*((?:॥[^॥]+)+)॥$', l)
    num = None
    if m: num = '॥'.join(iso_word(x.replace(' ', '\0')).replace('\0', ' ') for x in m.group(1).split('॥')[1:]); l = l[:m.start()]
    end = ''
    if not m:
        if l.endswith('॥'): l, end = l[:-1].rstrip(), '.'
        elif l.endswith('।'): l, end = l[:-1].rstrip(), ','
    lead = ''
    if l.startswith('॥'):
        l, lead = l[1:].lstrip(), '॥ '
        if end == '.': end = ' ॥'
    l = re.sub(r'\s*।\s*', ', ', l)
    l = re.sub(r'\s*॥\s*', ' ॥ ', l).strip()
    t = ' '.join(iso_word(w) for w in l.split())
    return lead + t + (' ॥' + num + '॥' if num else end)

def iso(lines, n=None):
    return [iso_line(l, n if k == len(lines) - 1 else None) for k, l in enumerate(lines)]


# ---- applying the standard to a work's files ----
def double(s):
    """Any text (a meaning, a heading): ।। → ॥, and a number inside the double daṇḍa without spaces."""
    return re.sub(r'॥[ \t]*([०-९0-9੦-੯][^॥]*?)[ \t]*॥', r'॥\1॥', s.replace('।।', '॥'))

def _texts(o):
    if isinstance(o, str): return double(o)
    if isinstance(o, list): return [_texts(x) for x in o]
    if isinstance(o, dict): return {k: _texts(v) for k, v in o.items()}
    return o

def yajur(rel):
    """A work of the Yajurveda (its shelf path), whose recitation writes ꣳ."""
    return '/yajurveda/' in '/' + rel

def finish(rel, obj):
    """A work's file (`rel`, its path under library/) as the standard writes it: every text with ॥; a work.json's
    items by `apply`."""
    obj = _texts(obj)
    if rel.endswith('work.json') and 'items' in obj: apply(obj['items'], obj['lang'], yajur(rel))
    return obj

DEVANAGARI = re.compile('[\u0900-\u0963\u0966-\u097f]')   # a Devanagari letter (the daṇḍas are shared with Gurmukhi)
GURMUKHI = re.compile('[\u0a01-\u0a75]')

def apply(items, work_lang, yajur=False):
    """Rewrite each item's verse lines (`v`) by the standard, and its transliteration (`t`) as ISO 15919 of them
    (Devanagari verses only; a verse in another script keeps its own `t`). Returns the items (changed in place)."""
    for x in items:
        lang = x.get('l', work_lang)
        v = [dandas(l) for l in x['v']]
        if lang == 'sa': v = [sanskrit(l, yajur) for l in v]
        x['v'] = v
        if DEVANAGARI.search(''.join(v)):
            x['t'] = iso(v, x['n'] if x.get('y') in ('cau', 'cha') and x.get('n') else None)
        elif GURMUKHI.search(''.join(v)):
            x['t'] = iso([gurmukhi(l) for l in v])
    return items


# ---- cases the build checks (tools/site/library.py), each a mistake this module must never make ----
CASES = [
    (dandas, ('राम ।। १२ ।।',), 'राम ॥१२॥'),
    (dandas, ('दोइ ।।३ (क)।।',), 'दोइ ॥३ (क)॥'),                                         # a lettered number stays whole
    (sanskrit, ('ओं शान्तिः',), 'ॐ शान्तिः'),
    (sanskrit, ('संकल्प पंच दंड अंत कंप',), 'सङ्कल्प पञ्च दण्ड अन्त कम्प'),
    (sanskrit, ('दारुणं । रामं वन्दे अलक्षणं अचिन्त्यं',), 'दारुणम् । रामं वन्दे अलक्षणम् अचिन्त्यं'),   # a line's end without a daṇḍa is left
    (sanskrit, ('संसारं रूपं शृणु',), 'संसारं रूपं शृणु'),                                   # not Yajurveda: ꣳ never
    (lambda l: sanskrit(l, True), ('संसारं रूपं रसं ।',), 'सꣳसारꣳ रूपꣳ रसम् ।'),
    (lambda l: sanskrit(l, True), ('तेषाग्ं॑ सहस्र',), 'तेषाꣳ॑ सहस्र'),                       # ꣳ typed as ग्ं, never doubled
    (iso_line, ('कृष्ण ड़ ॐ हँस रामः सोऽहम् ॥',), 'kr̥ṣṇa ṛa oṁ ham̐sa rāmaḥ so’ham.'),
    (iso_line, ('॥ इति समाप्ता ॥',), '॥ iti samāptā ॥'),
    (iso_line, ('दोइ ॥३ (क)॥',), 'doi ॥3 (ka)॥'),
    (iso_line, ('नमो॒ नम॑ः ॥',), 'namo̠ nama̍ḥ.'),
    (lambda l: iso_line(l, 4), ('सुजाना ॥',), 'sujānā ॥4॥'),
    (iso_line, ('गउ भइ गौ भै ॥',), 'gaü bhaï gau bhai.'),
    (lambda l: iso_line(gurmukhi(l)), ('ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥',), 'ik oaṅkār satigura prasādi.'),
    (lambda l: iso_line(gurmukhi(l)), ('ਨਾਨਕ ਸੱਚ ਸਿੰਮ੍ਰਿਤਿ ਸੁਧਾਖੵਰ ॥੮॥੧੧॥',), 'nānaka sacca siṁmriti sudhākhyara ॥8॥11॥'),
    (fold, ('गङ्गा',), 'गंगा'), (fold, ('इदम्',), 'इदं'), (fold, ('अग्ंशुः',), 'अंशुः'), (fold, ('अन्न',), 'अन्न'),
]

def selftest():
    bad = [(f'{getattr(f, "__name__", "λ")}{a}', want, f(*a)) for f, a, want in CASES if f(*a) != want]
    items = [{'id': 'g', 'v': ['ਸਲੋਕੁ ॥'], 't': ['saloku.']}]                                   # Gurmukhi keeps its own t
    if apply(items, 'pa')[0]['t'] != ['saloku.']: bad.append(('apply Gurmukhi', ['saloku.'], items[0]['t']))
    return bad
