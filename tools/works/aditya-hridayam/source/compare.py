"""Compare text.txt with its two witnesses, word by word, and print every difference:
  - the owner's sanskritdocuments.org printout (adityahriday.pdf in scriptures-data), its recitation text
    (the part after स्तोत्रपाठ: the viniyoga, the nyāsas and the 31 ślokas), read from its Unicode text layer;
  - the Vālmīki Rāmāyaṇa's own text of the sarga (tools/works/valmiki-ramayana/text.txt, yuddha.105).
Every difference it prints is a choice in reconciliation.md.

    python3 compare.py <scriptures-data clone>
"""
import os, re, subprocess, sys, difflib, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
PDF = 'hinduism/stotra/surya/aditya-hridayam/printouts/sanskritdocuments/adityahriday.pdf'

def norm(s):
    s = unicodedata.normalize('NFC', s).replace('‍', '').replace('‌', '')
    s = re.sub(r'॥\s*[०-९]+\s*॥', ' ', s)
    s = re.sub(r'[।॥]', ' ', s)
    return s.split()

def ours():
    items, cur = {}, None
    for line in open(os.path.join(WORK, 'text.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'\[(\S+)', line)
        if m: cur = m.group(1); items[cur] = []; continue
        if not line or line[0] in '#@': continue
        items[cur].append(line)
    return items

def printout(data):
    t = subprocess.run(['pdftotext', '-raw', os.path.join(data, PDF), '-'], capture_output=True, text=True, check=True).stdout
    t = t[t.index('स्तोत्रपाठ'):]
    t = re.sub(r'\n?(?:\d+\s*)?(?:sanskritdocuments\.org|adityahriday\.pdf)(?:\s*\d+)?\n', '\n', t)
    t = re.sub(r'\n\s*आदित्यहृदयम्\s*\n', '\n', t)
    t = re.sub(r'\bor [^\n]*', '', t)                        # the printout's alternative readings ("or …")
    t = t[:t.index('Aditya Hridayam is Sarga')]
    return t

def valmiki():
    out, keep = {}, None
    for line in open(os.path.join(WORK, '..', 'valmiki-ramayana', 'text.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        m = re.match(r'\[yuddha\.105\.(\d+) ', line)
        if m: keep = 'sh' + m.group(1); out[keep] = []; continue
        if line.startswith('[') or line.startswith('@section'): keep = None; continue
        if keep and line and line[0] not in '#@': out[keep].append(line)
    return out

def show(name, a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            print(f'  {name}: {" ".join(a[i1:i2]) or "—"}  →  {" ".join(b[j1:j2]) or "—"}')

if __name__ == '__main__':
    data = sys.argv[1]
    o = ours()
    print('== the printout → text.txt')
    words = [w for k, v in o.items() if k != 'iti' for w in norm(' '.join(v))]
    pw = norm(printout(data))
    show('text', pw, words)
    print('== the Vālmīki Rāmāyaṇa (yuddha.105) → text.txt')
    v = valmiki()
    for k in v:
        show(k, norm(' '.join(v[k])), norm(' '.join(o[k])))
