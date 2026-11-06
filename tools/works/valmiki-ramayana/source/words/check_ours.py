"""Check the word meanings written by us (src.json: any origin with "ours") against Monier-Williams and Apte.

    python3 tools/works/valmiki-ramayana/source/words/check_ours.py

For each entry of glossary/sa.json written by us, wholly or in part:
  1. every stem in `r` (split at " + ", a prefix chain at "-") is a headword of Monier-Williams or Apte, allowing
     anusvāra for a class nasal and a stem's final t/d, s or n; grammar labels in brackets are skipped;
  2. the parts in `p`, their junction letters set aside, occur in the word in order (so no part is missing or foreign);
  3. a single word's stated case and number (द्वितीया एकवचन, तृतीया/षष्ठी/सप्तमी बहुवचन, …) fit its ending.
It prints what fails each test. What it lists is read by hand: a proper name, a negative compound, a feminine or causal
stem, a neuter s-stem or a consonant stem is right though no dictionary prints it so.
"""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
sys.path.insert(0, os.path.join(REPO, 'tools', 'meanings'))
import sanskrit_dict as sd

GL = json.load(open(os.path.join(HERE, '../../glossary/sa.json'), encoding='utf-8'))
SRC = json.load(open(os.path.join(HERE, 'src.json'), encoding='utf-8'))
OURS = [k for k, v in SRC.items() if 'ours' in v and k in GL]
MW, AP = sd.index('mw'), sd.index('ap90')
NAS = {'ङ्क': 'ंक', 'ङ्ख': 'ंख', 'ङ्ग': 'ंग', 'ङ्घ': 'ंघ', 'ञ्च': 'ंच', 'ञ्छ': 'ंछ', 'ञ्ज': 'ंज', 'ञ्झ': 'ंझ', 'ण्ट': 'ंट', 'ण्ड': 'ंड',
       'न्त': 'ंत', 'न्द': 'ंद', 'न्ध': 'ंध', 'न्थ': 'ंथ', 'म्प': 'ंप', 'म्ब': 'ंब', 'म्भ': 'ंभ', 'ङ्श': 'ंश'}

def keys(x):
    y = x
    for a, b in NAS.items(): y = y.replace(a, b)
    out = set()
    for v in (x, y, x.replace('ं', 'म्')):
        k = sd.slp1(v); out |= {k, k.rstrip('H'), k.rstrip('M')}
        if k[-1:] in 'td': out |= {k[:-1] + 't', k[:-1] + 'd'}
        if k[-1:] in 'sn': out.add(k[:-1])
    return out

def known(stem):
    stem = re.sub(r'\([^)]*\)', '', stem).strip(' ;')
    return not stem or all(any(c in MW or c in AP for c in keys(p)) for p in stem.split('-') if p)

CONS = set('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')
def skel(w): return [c for c in w if c in CONS]
def inorder(a, b):
    it = iter(b); return all(c in it for c in a)

END = {('द्वितीया', 'एकवचन'): r'(ं|म्|म|न्)$', ('तृतीया', 'बहुवचन'): r'(ैः|ै|ैर्|ैश्|ैस्|भिः|भिर्|भिश्|भिस्|भि)$',
       ('षष्ठी', 'बहुवचन'): r'(णां|नां|षां|सां|ाम्|ां|णाम्|नाम्|षाम्|साम्)$', ('सप्तमी', 'बहुवचन'): r'(षु|सु|ष्व|स्व)$',
       ('तृतीया', 'एकवचन'): r'(ेन|ेण|ा|या|णा|ना)$'}
GRAMMAR = re.compile(r'^(णिच्|सन्|यङ्|तरप्|तमप्|मयट्|मतुप्|तसिल्)\)?$')

stems, parts, ends = collections.Counter(), [], []
for w in OURS:
    e = GL[w]
    for x in re.split(r'\s*\+\s*|,\s*|/|;', e.get('r', '')):
        if x.strip() and not GRAMMAR.match(x.strip()) and not known(x): stems[x.strip()] += 1
    if e.get('p'):
        core = []
        for p in e['p']:
            k = skel(p[0]); core += k[1:-1] if len(k) > 2 else []
        if not inorder(core, skel(w)): parts.append((w, [p[0] for p in e['p']]))
    elif not re.search('संधि|समास', e.get('g', '')):
        for (c, n), pat in END.items():
            if re.search(c + r'[,\s]+' + n, e['g']) and not re.search(pat, w.rstrip('ऽ')): ends.append((w, e['g'])); break

print(f'{len(OURS)} entries written by us, wholly or in part')
print(f'1. stems in neither dictionary: {sum(stems.values())} uses of {len(stems)} stems:', ' '.join(f'{k}×{v}' for k, v in stems.most_common()))
print(f'2. parts out of order: {len(parts)}'); [print('  ', w, p) for w, p in parts]
print(f'3. endings that do not fit the case: {len(ends)}'); [print('  ', w, g) for w, g in ends]
