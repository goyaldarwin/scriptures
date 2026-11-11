"""text.txt of the Śrī Durgā Saptaśatī from the owner's copy of sanskritdocuments.org's text.

    python3 tools/works/durga-saptashati/source/make_text.py <durga-saptashati.json>

<durga-saptashati.json> is in scriptures-data at hinduism/stotra/durga/durga-saptashati/printouts/sanskritdocuments/:
the owner's structured copy of https://sanskritdocuments.org/doc_devii/durga700.html (19 sections in the order the
recording sings them: the Caṇḍikā-dhyāna, Argalā, Kīlaka, Kavaca, the 13 adhyāyas, the Aparādha-kṣamāpaṇa stotra and
the Devī Sūkta), each item with its lines, with his drafts of the meanings. The text is read as the copy prints it, with
these rules (reconciliation.md):
  - each section is a part and one section (page) of the work, in the copy's order;
  - a numbered item's last line ends with its number (॥ → ॥N॥); runs of spaces are one space; र + ृ is written र्ऋ
    (नैर्ऋत्यै, विष्णुर्ऋषिः), as Unicode spells r + ṛ;
  - adhyāya 5's triple namaskāras, which the copy gives as one item numbered 14-16 …, are three mantras, as Gita Press
    numbers them (॥१४॥ ॥१५॥ ॥१६॥): the first with the stanza's opening line, each with its own namaskāra, so the
    adhyāyas count 700 mantras (`5.14`, `5.15`, `5.16`); the joint meaning sits under the last (meanings.py);
  - a stotra's opening speaker (मार्कण्डेय उवाच) is the first line of its first verse, as the book prints it;
  - every other change is in corrections.json, with its reason;
  - each section's colophon (स्वस्ति … / इति …) is its last item, `<section>.iti`, without the copy's opening ॥.
Left out, not being the text: the copy's header lines (॥ देवी माहात्म्यम् ॥, ॥ श्री ॥, ॥ श्रीदुर्गायै नमः ॥,
॥ अथ श्रीदुर्गासप्तशती ॥, ॥ श्रीसप्तशतीदेवीमाहात्म्यं समाप्तम् ॥, ॥ ॐ तत् सत् ॐ ॥), the word अथवा before the
alternative dhyāna, and each adhyāya's tally of its mantras (उवाच १४, अर्धश्लोकाः २४, … एवमादितः ॥१०४॥).
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'works'))
import textfile

DIG = str.maketrans('0123456789', '०१२३४५६७८९')
SEC = {'dhyanam': 'dhyana', 'argala': 'argala', 'kilaka': 'kilaka', 'kavacha': 'kavacha', 'aparadha': 'aparadha', 'devi-sukta': 'devi-sukta'}
for c in range(1, 14): SEC[f'chapter-{c}'] = str(c)

def clean(l):
    l = re.sub(r'\s+', ' ', unicodedata.normalize('NFC', l)).strip()
    l = l.replace('रृ', 'र्ऋ').replace(' ,', ',')
    return l

def fix(lines, F, ref):
    out = list(lines)
    for old, new, _ in F.get(ref, []):
        hit = [i for i, l in enumerate(out) if old in l]
        assert len(hit) == 1 and out[hit[0]].count(old) == 1, f'{ref}: correction anchor not found once: {old}'
        out[hit[0]] = out[hit[0]].replace(old, new)
    return out

def number(L, n):
    assert L[-1].endswith('॥'), (n, L[-1])
    L[-1] = L[-1][:-1].rstrip() + ' ॥' + str(n).translate(DIG) + '॥'
    return L

def items_of(J, C):
    out = []
    for p, sec in enumerate(J['sections']):
        s = SEC[sec['id']]; ch = sec['kind'] == 'chapter'
        k = {'unnumbered': 0, 'dhyana': 0}
        for it in sec['items']:
            L = fix([clean(l) for l in it['text']['dv']], C['lines'], it['ref'])
            kind = it['kind']
            if kind == 'viniyoga':
                out.append({'id': f'{s}.viniyoga', 'p': p, 's': s, 'y': 'viniyoga', 'n': '', 'v': L}); continue
            if kind == 'unnumbered':
                if it['label'] == 'dhyānam' or s == 'dhyana':
                    k['dhyana'] += 1
                    out.append({'id': f"dhyana.{k['dhyana']}" if s == 'dhyana' else f'{s}.dhyana', 'p': p, 's': s, 'y': 'dhyana', 'n': '', 'v': L}); continue
                if re.fullmatch(r'ॐ नमश्चण्डिकायै [।॥]', ' '.join(L)):
                    out.append({'id': f'{s}.namah', 'p': p, 's': s, 'y': 'mantra', 'n': '', 'v': L}); continue
                assert s == '13', it['ref']                      # the closing repeat of 13.28–29, with क्लीं ॐ
                out.append({'id': '13.end', 'p': p, 's': s, 'y': 'mantra', 'n': '', 'v': L}); continue
            assert kind == 'verse', it['ref']
            num = it['number']
            if '-' in num:                                       # adhyāya 5's या देवी … नमस्तस्यै ×3: three mantras
                a, b = map(int, num.split('-')); assert b == a + 2 and len(L) == 2, it['ref']
                assert L[1] == 'नमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः ॥', it['ref']
                parts = [[L[0], 'नमस्तस्यै ॥'], ['नमस्तस्यै ॥'], ['नमस्तस्यै नमो नमः ॥']]
                for i, v in enumerate(parts):
                    out.append({'id': f'{s}.{a + i}', 'p': p, 's': s, 'y': 'mantra', 'n': str(a + i), 'v': number(v, a + i)})
                continue
            if not ch and int(num) == 1 and it['speaker'] and sec['id'] in ('argala', 'kilaka', 'kavacha'):
                L = [it['speaker']['dv']] + L                    # मार्कण्डेय उवाच, above the stotra's first verse
            y = 'mantra' if ch else ('rc' if s == 'devi-sukta' else 'shloka')
            rid = it['ref'] if ch else f'{s}.{num}'
            out.append({'id': rid, 'p': p, 's': s, 'y': y, 'n': num, 'v': number(L, num)})
        if sec['colophon']:
            col = clean(sec['colophon']['dv'])
            col = re.sub(r'^॥\s*', '', col); col = re.sub(r'॥\s*([०-९]+)\s*॥$', r'॥\1॥', col)
            out.append({'id': f'{s}.iti', 'p': p, 's': s, 'y': 'iti', 'n': '', 'v': [col]})
    return out

def main(src):
    J = json.load(open(src, encoding='utf-8'))
    C = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8'))
    items = items_of(J, C)
    used = {r for r in C['lines']}
    refs = {it['ref'] for sec in J['sections'] for it in sec['items']}
    assert used <= refs, used - refs
    ids = [x['id'] for x in items]; assert len(ids) == len(set(ids)), 'duplicate ids'
    for x in items:
        for l in x['v']: assert re.fullmatch(r'[ऀ-ॿ ,\-]+', l), (x['id'], l)
    mantras = [x for x in items if x['y'] == 'mantra' and x['n']]
    assert len(mantras) == 700, len(mantras)
    keys = [SEC[s['id']] for s in J['sections']]
    textfile.write(os.path.join(HERE, '..', 'text.txt'), items, [], keys, 'sa',
                   ["Śrī Durgā Saptaśatī: made by source/make_text.py from the owner's copy of sanskritdocuments.org's text;",
                    'change it there, not here. Every correction and choice: reconciliation.md.'])
    print(len(items), 'items;', len(mantras), 'mantras of the adhyāyas')

if __name__ == '__main__':
    main(sys.argv[1])
