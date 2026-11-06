"""The Gita Press English (Nalanda fonts) text layer → Unicode with IAST diacritics."""
import re
PAIRS = [('µu', 'ū'), ('§R', 'Ṛ'), ('ªU', 'Ū'), ('µU', 'Ū')]
ONE = {'å': 'ā', '∂': 'ī', 'ƒ': 'ṇ', '›': 'Ś', '‹': 'ś', '¶': 'ṣ', '∆': 'ṅ', '¢': 'ṭ', 'Œ': 'ḍ', 'æ': 'ṛ',
       '≈': 'ṁ', '√': 'ṁ', '¤': 'ñ', '¨': 'ḥ', 'Å': 'Ā', 'À': 'ṁ', '∫': 'Ī', '°': 'Ṇ',
       'ì': '“', 'î': '”', 'ë': '‘', 'í': '’', 'ó': '—', 'ñ': '–', '¡': 'ṛ'}
def convert(t):
    for a, b in PAIRS:
        t = t.replace(a, b)
    return ''.join(ONE.get(c, c) for c in t)
LEFT = set('•œ')

WORD = r"[A-Za-zāīūṛṅñṇṭḍśṣṁḥĀĪŪṚŚṢṬḌṆ’]+"
def hyphen_rule(texts):
    """A line-end hyphen (marked \\u00ad by parse.py) is decided by the book's own usage mid-line: the hyphenated
    form if the book writes it so at least as often as joined; joined if only the joined word occurs; otherwise
    the hyphen stays (a compound: the book hyphenates compounds)."""
    import collections, re
    words = collections.Counter(w.lower() for t in texts for w in re.findall(WORD + r"(?:-" + WORD + r")*", t.replace('­', '|')))
    def fix(t):
        def one(m):
            a, b = m[1], m[2]; h = (a + '-' + b).lower(); j = (a + b).lower()
            if words[h] >= words[j] or words[j] == 0:
                return a + '-' + b
            return a + b
        return re.sub("(" + WORD + ")­(" + WORD + ")", one, t).replace('­', '-')
    return fix
