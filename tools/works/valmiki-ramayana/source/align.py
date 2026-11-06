"""Compare the Gita Press text with a witness, sarga by sarga, letter by letter after normalising both the same way.

Every difference is reported with the Gita Press verse it falls in, the two readings, and context.
"""
import json, re, sys, difflib, unicodedata

DIG = str.maketrans('०१२३४५६७८९', '0123456789')
KANDAS = ['bala', 'ayodhya', 'aranya', 'kishkindha', 'sundara', 'yuddha', 'uttara']

def norm_line(s):
    """The comparison form: conventions of spelling folded so only real differences remain."""
    s = unicodedata.normalize('NFC', s).replace('‍', '').replace('‌', '')
    s = s.replace(':', 'ः')
    s = re.sub(r'[।॥|0-9०-९\.\-\s,;\'"‘’“”()\[\]ऽ*]', '', s)
    s = s.replace('ँ', 'ं')
    s = re.sub('[ङञणनम]्(?=[क-ह])', 'ं', s)
    s = re.sub('म्$', 'ं', s)
    s = re.sub('ः(?=[शषस])', '', s)
    s = re.sub(r'([शषस])्(?=\1)', '', s)
    s = re.sub(r'र्([क-ह])्\1', r'र्\1', s)          # धर्म्म = धर्म
    s = re.sub('ं(?=[क-ह])', 'ं', s)
    return s

def halves(text):
    """A text cut after each । or ॥ (or ।।, |, ||): half-verses, whatever the printed line breaks."""
    t = text.replace('।।', '॥').replace('||', '॥').replace('|', '।')
    parts = re.split(r'(?<=[।॥])', t)
    out = []
    for p in parts:
        if not p.strip():
            continue
        if out and re.fullmatch(r'[\s०-९0-9.॥।-]*', p):
            out[-1] += p              # a verse number after the mark stays with its half
        else:
            out.append(p)
    return out

def gp_lines(sarga):
    """[(verse n, half-verse)] of a Gita Press sarga."""
    out = []
    for v in sarga['verses']:
        for h in halves(' '.join(v['lines'])):
            out.append((v['n'], h))
    return out

def diff(gp, wit):
    """gp: [(n, line)], wit: [line]. Returns differences [(n, gp_text, wit_text, gp_ctx)]."""
    a_chars, a_owner = [], []
    for n, l in gp:
        t = norm_line(l)
        a_chars.append(t); a_owner.extend([n] * len(t))
    A = ''.join(a_chars)
    B = ''.join(norm_line(l) for l in wit)
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        n = a_owner[min(i1, len(a_owner) - 1)] if a_owner else None
        out.append({'n': n, 'gp': A[i1:i2], 'wit': B[j1:j2], 'ctx': A[max(0, i1 - 12):i2 + 12],
                    'wctx': B[max(0, j1 - 12):j2 + 12], 'i': i1})
    return out, sm.ratio()
