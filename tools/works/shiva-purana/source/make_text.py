"""Make text.txt of the Śrī Śivamahāpurāṇa from the owner's copy of sanskritdocuments.org's text.

    python3 tools/works/shiva-purana/source/make_text.py <shiva-purana.json> tools/works/shiva-purana

<shiva-purana.json> is in scriptures-data at hinduism/purana/mahapurana/shiva/printouts/sanskritdocuments/. It follows
the Gita Press edition (code 2223 and its second part) verse for verse; the owner's Gita Press scan is the printed
witness, read by eye where a check here or in `check.py` flags a place (reconciliation.md). No OCR.

What this script does, in order (each step is listed in reconciliation.md):
  1. parts and sections: the Māhātmya, the seven saṃhitās, the Rudra-saṃhitā's five khaṇḍas and the Vāyavīya's two
     bhāgas are the parts (key = the copy's chapter prefix: 1, 2.1 … 2.5, 3 … 6, 7.1, 7.2); each adhyāya is a section;
  2. a verse's number: the copy's, read as the last level where it writes the whole reference (5.26.10 → 10);
     corrections.json → "number" for the misprints;
  3. a half-verse the copy leaves unnumbered (split off at a speaker's line) joins the numbered verse after it;
     corrections.json → "unnumbered" for the few that are something else;
  4. an adhyāya's opening maṅgala-śloka, numbered 1 with the first verse in the copy, is its verse 0, without a number;
  5. lines: a speaker's line (शौनक उवाच) is the verse's first line, without its daṇḍa, as the book prints it; a comma that
     marks a pāda inside a line starts a new line (one line per pāda in long metres); the last line ends ॥N॥;
  6. the copy's headers (॥ श्रीगणेशाय नमः ॥ …), its end-of-khaṇḍa lines, its proofreaders' credits and its variant
     readings (variants, "(स भक्त्या)") are not part of the text and are left out;
  7. the closing words (इति … अध्यायः) are each adhyāya's last item, `<section>.iti`, numbered as Gita Press: ॥N॥;
  8. zero-width joiners (श‍ृ for शृ, a web font's workaround) are removed; corrections.json → "lines" fixes the rest;
  9. a verse's first half-śloka (16 syllables) that lacks its । gets it, as the book prints every half-śloka;
 10. corrections.json → "insert": a verse the copy drops, from the witness reconciliation.md names, after the verse keyed.
"""
import json, re, sys, os, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
import textfile

DEV = str.maketrans('0123456789', '०१२३४५६७८९')
PARTS = ['mahatmya', '1', '2.1', '2.2', '2.3', '2.4', '2.5', '3', '4', '5', '6', '7.1', '7.2']

def part_of(ref):
    """The part key of a chapter ref: 0.5 → mahatmya, 1.3 → 1, 2.3.12 → 2.3, 7.2.4 → 7.2."""
    a = ref.split('.')
    if a[0] == '0': return 'mahatmya'
    return '.'.join(a[:2]) if a[0] in ('2', '7') else a[0]

def section_of(ref):
    return 'm.' + ref.split('.')[1] if ref.startswith('0.') else ref

def clean(s):
    s = s.replace('‍', '').replace('‌', '')
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'\s+', ' ', s).strip()

def speaker(sp):
    """A speaker's line as the book prints it: no daṇḍa (शौनक उवाच)."""
    s = clean(sp)
    s = re.sub(r'\s*[-–]?\s*।\s*$', '', s)
    return s

def syllables(line):
    """The syllables of a line: its vowels (an independent vowel, or a consonant not closed by a halant)."""
    t = re.sub(r'[^\u0900-\u097F]', '', line)
    n = len(re.findall(r'[\u0905-\u0914\u0960\u0961]', t))
    n += len(re.findall(r'[\u0915-\u0939\u0958-\u095F](?!\u093C?\u094D)', t))
    return n

SPEAKER = re.compile(r'(उवाच|ऊचुः|ऊचतुः|उचुः)$')

def half_danda(v):
    """A half-śloka (16 syllables) that is the first of a verse's two lines ends with ।, as Gita Press prints it."""
    L = [i for i, l in enumerate(v) if not SPEAKER.search(l)]
    if len(L) == 2:
        i = L[0]
        if not re.search(r'[।॥-]$', v[i]) and 15 <= syllables(v[i]) <= 17:
            v[i] += ' ।'; return True
    return False

def split_padas(lines):
    """A comma that ends a pāda inside a line starts a new line."""
    out = []
    for L in lines:
        parts = [p.strip() for p in L.split(',')]
        out += [p for p in parts if p]
    return out

def main(src, work):
    C = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8'))
    D = json.load(open(src, encoding='utf-8'))
    items, log, problems, keymap = [], Counter(), [], {}
    for f in D['files']:
        for ch in f['chapters']:
            ref = ch['ref']; sec = section_of(ref); part = PARTS.index(part_of(ref))
            mtype = 'mshloka' if part == 0 else 'shloka'
            pending = []                       # unnumbered lines waiting for the next numbered verse
            pkeys = []                         # their keys in the copy
            late_colophon = None
            out = []
            vs = ch['verses']
            for i, v in enumerate(vs):
                key = f"{ref}#{v['seq']}"
                lines = [clean(x) for x in v['text']['dv']]
                if key in C['lines']: lines = C['lines'][key]['v']; log['lines'] += 1
                sp = speaker(v['speaker']['dv']) if v.get('speaker') else ''
                if key in C['speaker']: sp = C['speaker'][key]['v']; log['speaker'] += 1
                n = v['number']
                if key in C['drop']: log['drop'] += 1; continue
                if n is None and key in C['unnumbered']:
                    u = C['unnumbered'][key]
                    if u['as'] == 'verse': n = u['n']; log['unnumbered as verse'] += 1
                    elif u['as'] == 'item':                 # a passage of its own, without a number (prose, a list)
                        body = ([sp] if sp else []) + (u.get('v') or lines)
                        body[-1] = body[-1].rstrip(' ।॥') + ' ॥'
                        out.append({'n': '', 'y': u['y'], 'v': body, 'k': [key]}); log['unnumbered passage'] += 1; continue
                    elif u['as'] == 'prev':
                        out[-1]['v'] += ([sp] if sp else []) + lines; out[-1]['k'].append(key); log['unnumbered to previous'] += 1; continue
                    else: raise SystemExit(f'{key}: unknown "as" {u["as"]}')
                if n is None:
                    half = list(lines)
                    if half and not re.search(r'[।॥-]$', half[-1]): half[-1] += ' ।'   # the half-verse it is ends with ।
                    pending += ([sp] if sp else []) + half; pkeys.append(key); log['unnumbered joined to next'] += 1; continue
                if re.fullmatch(r'[\d.]+', n) and '.' in n:
                    if re.fullmatch(re.escape(ref) + r'\.\d+', n):   # the whole reference: 5.26.10 → 10
                        n = n[len(ref) + 1:]; log['number written whole'] += 1
                    elif n == ref and lines[0].startswith('इति'):   # the closing words taken for a verse (2.3.27)
                        late_colophon = ' '.join(lines); log['closing words taken for a verse'] += 1; continue
                    elif ref.startswith(n + '.'):                 # the copy's end-of-khaṇḍa line (॥ इति … खण्डः समाप्तः)
                        log['end-of-khaṇḍa line left out'] += 1; continue
                    else: problems.append(f'{key}: number {n}'); continue
                if key in C['number']: n = C['number'][key]['n']; log['number'] += 1
                if not n.isdigit(): problems.append(f'{key}: number {n}'); continue
                body = split_padas(lines)
                if len(body) != len(lines): log['comma pāda split'] += 1
                body = pending + ([sp] if sp else []) + body; pending = []
                keys = pkeys + [key]; pkeys = []
                # the opening maṅgala-śloka: numbered 1 in the copy, before the verse that really is 1
                y = mtype
                if key in C['opening']: n = ''; log['opening maṅgala'] += 1
                if key in C['type']: y = C['type'][key]['y']
                out.append({'n': n, 'y': y, 'v': body, 'k': keys})
                if key in C['insert']:                      # a verse the copy dropped, from a witness
                    x = C['insert'][key]; out.append({'n': x['n'], 'y': mtype, 'v': list(x['v']), 'k': []}); log['verse inserted'] += 1
            if pending: problems.append(f'{ref}: unnumbered lines at the end: {pending}')
            SL = C['speaker_lines']['map']
            for x in out:
                for i, l in enumerate(x['v']):
                    if l in SL: x['v'][i] = SL[l]; log['speaker line fixed'] += 1
            # ids, numbers, the closing words
            seen = set(); prev = 0
            for x in out:
                if x['n']:
                    k = int(x['n'])
                    if k != prev + 1 and f'{ref}:{k}' not in C['gap']:
                        problems.append(f'{ref}: verse {k} after {prev}')
                    prev = k; vid = f"{sec}.{k}"
                    x['v'][-1] = x['v'][-1].rstrip(' ।॥') + f' ॥{str(k).translate(DEV)}॥'
                    if half_danda(x['v']): log['। added after a half-śloka'] += 1
                else:
                    vid = f"{sec}.0"
                    x['v'][-1] = x['v'][-1].rstrip(' ।॥') + ' ॥'
                if vid in seen: problems.append(f'{vid}: two verses'); continue
                seen.add(vid)
                items.append({'id': vid, 'p': part, 's': sec, 'y': x['y'], 'n': x['n'], 'v': x['v']}); keymap[vid] = x['k']
            col = ch.get('colophon') or ({'dv': late_colophon} if late_colophon else None)
            if col:
                t = clean(col['dv'])
                if ref in C['colophon']: t = C['colophon'][ref]['v']; log['colophon'] += 1
                adh = int(ref.split('.')[-1])
                t = re.sub(r'\s*॥[\s०-९.]*॥\s*$', '', t).rstrip(' ।॥') + f' ॥{str(adh).translate(DEV)}॥'
                items.append({'id': f'{sec}.iti', 'p': part, 's': sec, 'y': 'iti', 'n': '', 'v': [t]}); keymap[f'{sec}.iti'] = [f'{ref}#colophon']
            else:
                raise SystemExit(f'{ref}: no closing words')
    if problems:
        print('\n'.join(problems)); raise SystemExit(f'{len(problems)} problems')
    used = {k for sect in ('lines', 'speaker', 'drop', 'unnumbered', 'number', 'opening', 'type', 'insert') for k in C[sect]}
    header = ["Śrī Śivamahāpurāṇa with its Māhātmya: made by source/make_text.py from the owner's copy of sanskritdocuments.org's",
              "text, which follows Gita Press (code 2223 and its second part); change it there, not here. Every choice: reconciliation.md."]
    textfile.write(os.path.join(work, 'text.txt'), items, [], PARTS, 'sa', header)
    with open(os.path.join(HERE, 'keys.json'), 'w', encoding='utf-8') as f:    # each verse's entries in the copy, for its meanings
        f.write('{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in keymap.items()) + '\n}\n')
    print(f'{len(items)} items')
    for k, v in sorted(log.items()): print(f'  {k}: {v}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
