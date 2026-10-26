"""Legacy ASCII Gurmukhi (GurbaniAkhar / AnmolLipi / GurbaniLipi font encoding) → Unicode Gurmukhi.

The owner's PDF types the Gurmukhi in the GurbaniAkharThick font: plain ASCII letters drawn as Gurmukhi
("siqgur pRswid ]" is ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥). Its text layer therefore holds Latin letters. This module turns them
into Unicode text that any Gurmukhi font shows correctly.

    to_unicode('<> siqgur pRswid ]')   → 'ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥'

How (three steps):
1. Each legacy character has a class and a Unicode value (TABLE below).
2. The characters are grouped into clusters: one base letter (a consonant or a vowel bearer ੳ ਅ ੲ) with the
   marks that follow it. The legacy sihari 'i' is typed BEFORE the letter it belongs to (it is drawn on the
   left), so it is carried to the next base letter. Inside a cluster the marks are written in Unicode order:
       base, subjoined letter (੍ਰ ੍ਹ ੍ਵ ੵ ੑ), vowel sign(s), nasal (ੰ ਂ), addak (ੱ), visarga (ਃ)
   e.g. 'ismrau'  i s m r a u  → ਸ+ਿ ਮ ਰ ੳ+ੁ → ਸਿਮਰਉ
        'AMimRq' A M i m R q  → ਅ+ੰ ਮ+੍ਰ+ਿ ਤ  → ਅੰਮ੍ਰਿਤ   (the sihari goes after the subjoined ਰ)
3. A vowel bearer with its vowel sign becomes the independent vowel Unicode prescribes
   (ੳ+ੁ → ਉ, ਅ+ਾ → ਆ, ੲ+ਿ → ਇ …), and the result is NFC-normalised (the app looks words up in NFC).

Conventions (the same as the Gurbani databases of SikhiToTheMax / Shabad OS):
- '´' (half yayya under a letter, as in ਸੁਧਾਖੵਰ) is U+0A75 GURMUKHI SIGN YAKASH, not ੍ਯ.
- '@' (the small half haha under ਮ/ਨ, as in ਤੁਮੑਾਰੀ) is U+0A51 GURMUKHI SIGN UDAAT; 'H' (the full pairin haha) is ੍ਹ.
- ']' is ॥ (U+0965, the Devanagari double danda Gurmukhi shares), '[' is । ; digits are Gurmukhi digits ੦–੯;
  '<>' is ੴ (ik-oankaar).
Characters not in the table raise an error, so nothing is silently dropped.
"""
import unicodedata

# legacy character → (Unicode, class).  Classes: B base letter, S subjoined letter / sign below,
# V vowel sign, I sihari (pre-base in the legacy text), N nasal, A addak, X visarga, P punctuation/digit/space.
TABLE = {
    # vowel bearers
    'a': ('ੳ', 'B'), 'A': ('ਅ', 'B'), 'e': ('ੲ', 'B'),
    # consonants (row by row of the Gurmukhi alphabet)
    's': ('ਸ', 'B'), 'h': ('ਹ', 'B'),
    'k': ('ਕ', 'B'), 'K': ('ਖ', 'B'), 'g': ('ਗ', 'B'), 'G': ('ਘ', 'B'), '|': ('ਙ', 'B'),
    'c': ('ਚ', 'B'), 'C': ('ਛ', 'B'), 'j': ('ਜ', 'B'), 'J': ('ਝ', 'B'), '\\': ('ਞ', 'B'),
    't': ('ਟ', 'B'), 'T': ('ਠ', 'B'), 'f': ('ਡ', 'B'), 'F': ('ਢ', 'B'), 'x': ('ਣ', 'B'),
    'q': ('ਤ', 'B'), 'Q': ('ਥ', 'B'), 'd': ('ਦ', 'B'), 'D': ('ਧ', 'B'), 'n': ('ਨ', 'B'),
    'p': ('ਪ', 'B'), 'P': ('ਫ', 'B'), 'b': ('ਬ', 'B'), 'B': ('ਭ', 'B'), 'm': ('ਮ', 'B'),
    'X': ('ਯ', 'B'), 'r': ('ਰ', 'B'), 'l': ('ਲ', 'B'), 'v': ('ਵ', 'B'), 'V': ('ੜ', 'B'),
    # consonants with nukta (none occurs in Sukhmani Sahib; kept for completeness)
    'S': ('ਸ਼', 'B'), '^': ('ਖ਼', 'B'), 'Z': ('ਗ਼', 'B'), 'z': ('ਜ਼', 'B'), '&': ('ਫ਼', 'B'), 'L': ('ਲ਼', 'B'),
    # subjoined letters (pairin) and signs below
    'R': ('੍ਰ', 'S'), '®': ('੍ਰ', 'S'),          # pairin rara (® is the narrow form used under a sihari)
    'H': ('੍ਹ', 'S'), '@': ('ੑ', 'S'),           # pairin haha; the small half haha (udaat sign)
    'Í': ('੍ਵ', 'S'), 'ç': ('੍ਚ', 'S'), '†': ('੍ਟ', 'S'), 'œ': ('੍ਤ', 'S'), '˜': ('੍ਨ', 'S'),
    '´': ('ੵ', 'S'), 'Ï': ('ੵ', 'S'),             # half yayya (yakash)
    # vowel signs
    'w': ('ਾ', 'V'), 'I': ('ੀ', 'V'), 'u': ('ੁ', 'V'), 'ü': ('ੁ', 'V'), 'U': ('ੂ', 'V'), '¨': ('ੂ', 'V'),
    'y': ('ੇ', 'V'), 'Y': ('ੈ', 'V'), 'o': ('ੋ', 'V'), 'O': ('ੌ', 'V'), 'E': ('ਓ', 'B'),
    'i': ('ਿ', 'I'),
    'W': ('ਾਂ', 'V'),                              # kanna with bindi; split below
    # nasals, addak, visarga
    'M': ('ੰ', 'N'), 'µ': ('ੰ', 'N'), 'N': ('ਂ', 'N'), 'ˆ': ('ਂ', 'N'),
    '`': ('ੱ', 'A'), '~': ('ੱ', 'A'),
    'Ú': ('ਃ', 'X'),
    # punctuation, digits
    ']': ('॥', 'P'), '[': ('।', 'P'), ' ': (' ', 'P'),
    **{str(d): (chr(0x0A66 + d), 'P') for d in range(10)},
}
IKONKAR = ('<>', 'ੴ')

# a vowel bearer + its vowel sign → the independent vowel
INDEPENDENT = {'ੳੁ': 'ਉ', 'ੳੂ': 'ਊ', 'ੳੋ': 'ਓ', 'ਅਾ': 'ਆ', 'ਅੈ': 'ਐ', 'ਅੌ': 'ਔ', 'ੲਿ': 'ਇ', 'ੲੀ': 'ਈ', 'ੲੇ': 'ਏ'}
# the order of vowel signs when a letter carries two (ਹੋੁ: hora before aunkar, as in the Gurbani databases)
VORDER = 'ਾਿੀੇੈੋੌੁੂ'


def _emit(cl):
    base, subs, vows, nas, add, vis = cl
    vows = sorted(vows, key=VORDER.index)
    if vows and base + vows[0] in INDEPENDENT and not subs:
        base, vows = INDEPENDENT[base + vows[0]], vows[1:]
    return base + ''.join(subs) + ''.join(vows) + ''.join(nas) + ''.join(add) + ''.join(vis)


def to_unicode(s):
    """Convert one line of legacy ASCII Gurmukhi to NFC Unicode Gurmukhi. Raises ValueError on unknown input."""
    out, cl, sihari = [], None, False

    def flush():
        nonlocal cl
        if cl: out.append(_emit(cl)); cl = None

    i = 0
    s = s.strip()
    while i < len(s):
        if s.startswith(IKONKAR[0], i):
            flush(); out.append(IKONKAR[1]); i += 2; continue
        ch = s[i]
        if ch not in TABLE: raise ValueError(f'unknown legacy character {ch!r} in {s!r}')
        u, k = TABLE[ch]
        if k == 'B':
            flush(); cl = [u, [], [], [], [], []]
            if sihari: cl[2].append('ਿ'); sihari = False
        elif k == 'I':
            if sihari: raise ValueError(f'two sihari in a row in {s!r}')
            flush(); sihari = True
        elif k == 'P':
            if sihari: raise ValueError(f'sihari without a letter in {s!r}')
            flush(); out.append(u)
        else:
            if cl is None: raise ValueError(f'mark {ch!r} without a letter in {s!r}')
            if k == 'S': cl[1].append(u)
            elif k == 'V':
                for c in u: (cl[2] if c != 'ਂ' else cl[3]).append(c)
            elif k == 'N': cl[3].append(u)
            elif k == 'A': cl[4].append(u)
            elif k == 'X': cl[5].append(u)
        i += 1
    if sihari: raise ValueError(f'sihari at the end of {s!r}')
    flush()
    return unicodedata.normalize('NFC', ''.join(out))


if __name__ == '__main__':
    import sys
    for a in sys.argv[1:] or ['<> siqgur pRswid ]']:
        print(a, '→', to_unicode(a))
