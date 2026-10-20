"""The verse number at the end of our own meanings (owner, 2026-10-19: "keep the verse number in the meaning").

The number is never written in the meaning files; exporters add it from the verse, so it always matches:
- the number the verse's last line ends with (dohā ।।२९।।, ।।३० (क)।।, śloka ।।१।।);
- otherwise, for a caupāī or a chhanda, its number `n` (the app shows a caupāī's number at the end of its last line;
  the printed book numbers chhandas the same way);
- otherwise none.
Hindi gets Devanagari digits, English Latin digits (letters such as क stay), as the verse shows in each language.
"""
import re

DEV = '०१२३४५६७८९'
_END = re.compile(r'।।\s*([^।]*?)\s*।।\s*$')
_HAS = re.compile(r'।।\s*[०-९0-9]')

def mark(item):
    """'।।२९।।' style mark for an item, in Devanagari digits, or '' when the verse has no number."""
    m = _END.search(item['v'][-1]) if item.get('v') else None
    if m and m.group(1): return '।।' + m.group(1) + '।।'
    if item.get('y') in ('cau', 'cha') and item.get('n'):
        return '।।' + re.sub(r'\d', lambda d: DEV[int(d.group())], str(item['n'])) + '।।'
    return ''

def latin(s): return re.sub('[०-९]', lambda d: str(DEV.index(d.group())), s)

def with_number(text, item, lang):
    """The meaning as shown: text, a space, the verse's number (if any)."""
    assert not _HAS.search(text), f'{item["id"]}: the meaning file must not carry a verse number: {text[-20:]}'
    m = mark(item)
    if not m: return text
    return f'{text} {latin(m) if lang == "en" else m}'
