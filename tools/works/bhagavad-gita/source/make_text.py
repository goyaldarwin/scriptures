"""text.txt of the Śrīmad Bhagavad Gītā from the owner's copy of sanskritdocuments.org's text.

    python3 tools/works/bhagavad-gita/source/make_text.py <bhagavad-gita.json>

<bhagavad-gita.json> is in scriptures-data at hinduism/granth/vyasa/bhagavad-gita/printouts/sanskritdocuments/: the
owner's structured copy of https://sanskritdocuments.org/doc_giitaa/bhagvadnew.html (18 chapters, 701 verses, each with
its speaker, its lines and the page's variant readings; each chapter's colophon), with his drafts of the meanings.
The text is read as the copy prints it, with these rules (reconciliation.md):
  - a speaker's line (श्रीभगवानुवाच, अर्जुन उवाच …) is a line of the verse it opens, without its daṇḍa, as the book
    prints it above the verse; where the copy gives it in the middle of a śloka (1.21, 1.28) it stays there;
  - the last line ends with the verse's number (॥ → ॥N॥); runs of spaces are one space;
  - the copy's variant readings are left out (docs/PLAYBOOK.md §2: fix, don't annotate); its own reading stays;
  - every other change is in corrections.json, with its reason;
  - each chapter's colophon (ॐ तत्सदिति …) is its last item, `<chapter>.iti`.
The page's own header lines (॥ ॐ श्री परमात्मने नमः ॥, ॥ अथ श्रीमद्भगवद्गीता ॥) and the Viṣṇu dhyāna-śloka it prints
after the text (शान्ताकारं भुजगशयनं …) are not the Gītā's text and are left out. The Gītā Dhyānam the recording sings
before chapter 1 is dhyana.txt beside this script (its source is in reconciliation.md).
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'works'))
import textfile

DIG = str.maketrans('0123456789', '०१२३४५६७८९')
SPK = re.compile(r'^(श्रीभगवानुवाच|(धृतराष्ट्र|सञ्जय|अर्जुन) उवाच)\s*।?$')

def fix(lines, F, ref):
    out = list(lines)
    for old, new, _ in F.get(ref, []):
        hit = [i for i, l in enumerate(out) if l == old]
        assert len(hit) == 1, f'{ref}: correction anchor not found once: {old}'
        out[hit[0]] = new
    return out

def dhyana():
    """The Gītā Dhyānam, dhyana.txt: '[n]' then its lines; blank lines between verses."""
    p = os.path.join(HERE, 'dhyana.txt')
    if not os.path.exists(p): return []
    out = []
    for raw in open(p, encoding='utf-8'):
        l = raw.strip()
        if not l or l.startswith('#'): continue
        m = re.fullmatch(r'\[(\d+)\]', l)
        if m: out.append({'id': f'dhyana.{m.group(1)}', 'p': 0, 's': 'dhyana', 'y': 'dhyana', 'n': m.group(1), 'v': []}); continue
        out[-1]['v'].append(l)
    return out

def main(src):
    J = json.load(open(src, encoding='utf-8'))
    C = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8'))
    items = dhyana(); base = 1 if items else 0
    for ch in J['chapters']:
        c = ch['number']; p = c - 1 + base; prev = 0
        for v in ch['verses']:
            assert v['chapter'] == c and v['verse'] == prev + 1, v['ref']; prev = v['verse']
            L = [re.sub(r'\s+', ' ', unicodedata.normalize('NFC', l)).strip() for l in v['text']['dv']]
            L = fix(L, C['lines'], v['ref'])
            if v['speaker']: L = [v['speaker']['dv']] + L
            L = [SPK.match(l).group(1) if SPK.match(l) else l for l in L]
            assert L[-1].endswith('॥') and not re.search(r'[०-९]', L[-1]), v['ref']
            L[-1] = L[-1][:-1].rstrip() + ' ॥' + str(v['verse']).translate(DIG) + '॥'
            for l in L: assert re.fullmatch(r'[ऀ-ॿ \-]+', l), (v['ref'], l)
            items.append({'id': v['ref'], 'p': p, 's': str(c), 'y': 'shloka', 'n': str(v['verse']), 'v': L})
        col = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', ch['colophon']['dv'])).strip()
        for old, new, _ in C['colophons'].get(str(c), []):
            assert col.count(old) == 1, (c, old); col = col.replace(old, new)
        col = re.sub(r'॥\s*([०-९]+)\s*॥$', r'॥\1॥', col)
        assert col.endswith('॥' + str(c).translate(DIG) + '॥'), col
        items.append({'id': f'{c}.iti', 'p': p, 's': str(c), 'y': 'iti', 'n': '', 'v': [col]})
    keys = (['dhyana'] if base else []) + [str(i) for i in range(1, 19)]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, [], keys, 'sa',
                   ['Śrīmad Bhagavad Gītā: made by source/make_text.py from the owner\'s copy of sanskritdocuments.org\'s text',
                    '(and source/dhyana.txt); change it there, not here. Every correction and choice: reconciliation.md.'])
    print(len(items), 'items;', sum(x['y'] == 'shloka' for x in items), 'ślokas')

if __name__ == '__main__':
    main(sys.argv[1])
