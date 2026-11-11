"""Read one volume of the owner's Gita Press Mahābhārata e-book (codes 32–37, EPUB) into its parvas, adhyāyas, verses,
Hindi paragraphs and notes. No OCR and no glyph decoding: the e-book's text is Unicode.

    python3 epub.py <volume.epub> <out.json>

The e-book marks each kind of block by its style (font, size, alignment, indent), not by a stable class name (calibre
numbers its classes afresh in each volume), so every block is classed by its resolved style (role()), and every block
that fits no class is logged. Inside an adhyāya:
  - a verse line: a justified block with a left margin and no first-line indent; a verse ends with ॥ N ॥ (N may end
    in ½, an image in the e-book); a line in ( … ) is the book's dākṣiṇātya (southern) reading, unnumbered, ending ॥;
  - a Sanskrit prose passage (gadya): a bold justified block with a first-line indent;
  - a Hindi paragraph: a regular justified block with a first-line indent;
  - a speaker (… उवाच): a centred regular block; it is a line of the verse it is printed before (or inside);
  - the closing words: a centred block starting इति (Sanskrit), then इस प्रकार (Hindi), then the dākṣiṇātya count.
Everything after an <hr> in a file is the notes; a mark in the text is a link to its note.
The output keeps every block as printed (after normalize()); make_text.py builds the text and meanings from it.
"""
import html, json, os, re, sys, zipfile, posixpath

HALF = '½'

def css(src):
    out = {}
    for m in re.finditer(r'\.([\w-]+)\s*\{([^}]*)\}', src):
        d = {}
        for p in m.group(2).split(';'):
            if ':' in p: k, v = p.split(':', 1); d[k.strip()] = v.strip()
        out[m.group(1)] = d
    return out

def pct(v):
    m = re.match(r'(-?[\d.]+)%', v or ''); return float(m.group(1)) if m else 0.0

def style(d):
    return {'bold': 'Bold' in d.get('font-family', ''), 'size': d.get('font-size', ''), 'align': d.get('text-align', ''),
            'ml': pct(d.get('margin-left')), 'ti': pct(d.get('text-indent'))}

C = '[\u0915-\u0939\u0958-\u095f]\u093c?'
def joiners(t):
    """The e-book's zero-width joiners: between two consonants a ZWJ (or a ZWNJ before य) stands for a lost virāma
    (बुद्ध\u200dया is बुद्ध्या, वह\u200dने is वह्ने); every other joiner only steers the glyphs (भगवान्, महद्दिव्यं) and goes."""
    t = re.sub('(%s)(?:[\u200c\u200d]*\u200d[\u200c\u200d]*|\u200c+(?=य))(?=[\u0915-\u0939])' % C, '\\1\u094d', t)
    return t.replace('\u200c', '').replace('\u200d', '')

def normalize(t):
    """The e-book's spacing marks → plain text: word joiners out, no-break spaces as spaces, ।। as ॥."""
    t = joiners(t).replace('\u2060', '').replace('\xa0', ' ').replace('\u2003', ' ').replace('\ufeff', '')
    t = re.sub(r'।\s*।', '॥', t)
    t = re.sub(r'[ \t]+', ' ', t).strip()
    return t

def role(st, t):
    sz, al, b = st['size'], st['align'], st['bold']
    if re.search(r'द(ा|)क्षिणात्य', t) and 'श्लोक' in t and t[:1] in '([': return 'daknote'
    if b and re.fullmatch(r'\[[^\[\]]+\]', t) and al in ('center', 'justify'): return 'head'
    if b and sz == '1.125em' and al == 'center': return 'head'   # श्रवणमहिमा inside the last adhyāya
    if b and sz == '1em' and al == 'center' and re.fullmatch(r'\([^()]+\)', t): return 'head'   # (कृष्णावतारः)
    if sz == '2em' and al == 'center': return 'parva' if t.endswith('पर्व') else 'big'
    if sz == '1.66667em' and al == 'center': return 'upaparva'
    if sz == '1.83333em' and al == 'center': return 'big' if 'सम्पूर्ण' in t else 'adh'
    if sz == '1.41667em' and al == 'center': return 'title'
    if (al == 'center' and t.startswith('इति ')) or re.match(r'इति श्रीम(न्म)?हाभारते', t): return 'iti'
    if (al == 'center' and t.startswith('इस प्रकार')) or re.match(r'इस प्रकार (व्यासनिर्मित )?श्रीमहाभारत', t) and re.search(r'पूरा हुआ\s*॥', t): return 'iti_hi'
    if al == 'center' and re.search(r'द(ा|)क्षिणात्य', t): return 'daknote'
    if sz in ('0.75em',): return 'small'
    if al == 'center' and not sz: return 'speaker' if not b and re.search(r'(वाच|ऊचुः|ऊचतुः|चतुः|चुः)\)?$', t) else 'caption'
    if st['ti'] < 0: return 'toc'
    if al in ('justify', '') and not sz:
        if not b and len(t) < 45 and re.search(r'(उवाच|ऊचुः|ऊचतुः|उवाचः)\)?$', t): return 'speaker'
        if st['ti'] > 0: return 'gadya' if b else 'para'
        if st['ml'] > 0: return 'verse'
        if st['ml'] == 0 and st['ti'] == 0: return 'verse' if b else 'para'   # a Sanskrit lead-in (अत्रानुवंशश्लोको भवति—); a Hindi run-on
    if al == 'right': return 'small'
    return 'other'

def is_sanskrit(t):
    """Sanskrit prose set in the Hindi paragraph's style: no word ends as Hindi words do (Gita Press joins the
    postposition: अर्जुनको, देवर्षि नारदने), and words end in visarga or virāma."""
    words = re.findall(r'[\u0900-\u097f\u200c\u200d]+', re.sub(r'॥.*?॥', '', t))
    hi = sum(1 for w in words if re.search(r'(को|से|में|ने|का|की|के|कर|दिया|दी|हुए|हुआ|गया|गये|गयी|है|हैं|था|थे|थी|लिये|रहे|वाले|ँ|ों|ें)$', w))
    sa = sum(1 for w in words if re.search(r'(ः|्)$', w))
    return sa >= 2 and hi * 5 < sa   # a Sanskrit word may end like a Hindi one (प्रभुरेकाकी, व्यथा)
def is_hindi(t):
    """Hindi set in the Sanskrit prose's bold: letters and words Sanskrit prose does not use (ँ ों ें ड़, है, था)."""
    return len(HINDI_MARK.findall(t)) >= 2
HINDI_MARK = re.compile(r'ँ|ों|ें|ड़|ढ़|(^|\s)(है|हैं|था|थे|थी|कि|और|यह|वह)(\s|[,।—!?‘’]|$)')   # marks of Hindi that Sanskrit prose lacks
HINDI = re.compile(r'(^| )(है|हैं|था|थे|थी|और|के|की|का|में|को|से|ने|कहा|बोले|लिये|हुए|हुआ)( |[,।—!?]|$)')

class Book:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        opf_path = re.search(r'full-path="([^"]+)"', self.z.read('META-INF/container.xml').decode()).group(1)
        opf = self.z.read(opf_path).decode('utf-8'); base = posixpath.dirname(opf_path)
        man = {}
        for m in re.finditer(r'<item\b[^>]*>', opf):
            a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(0))); man[a['id']] = posixpath.join(base, a['href'])
        self.spine = [man[i] for i in re.findall(r'<itemref[^>]*idref="([^"]+)"', opf)]
        self.css = {}
        for n in self.z.namelist():
            if n.endswith('.css'): self.css.update(css(self.z.read(n).decode('utf-8')))
        self.half = self.find_half()
        self.notes = {}   # (file, id) → [note text, …] (a note's first block, then its continuation blocks)
        for f in self.spine: self.read_notes(f)

    def find_half(self):
        """The image the e-book prints ½ with: the one small image (about 11×21 px) used inside text, hundreds of times."""
        from collections import Counter
        c = Counter()
        for f in self.spine:
            for m in re.finditer(r'<img src="([^"]+)"', self.z.read(f).decode('utf-8')): c[posixpath.join(posixpath.dirname(f), m.group(1))] += 1
        import io
        from PIL import Image
        small = [(n, k) for k, n in c.items() if Image.open(io.BytesIO(self.z.read(k))).size[0] < 30]
        assert len(small) == 1, small
        return posixpath.basename(small[0][1])

    def blocks(self, f):
        """The blocks of one file in order: (style, inner html, id, after_hr)."""
        s = self.z.read(f).decode('utf-8'); s = s[s.find('<body'):]
        hr = s.find('<hr')
        for m in re.finditer(r'<div([^>]*)>(.*?)</div>', s, re.S):
            a = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
            yield style(self.css.get(a.get('class', ''), {})), m.group(2), a.get('id'), (hr >= 0 and m.start() > hr)

    def text(self, h, marks=None):
        """A block's text: ½ for its image, other images dropped, note marks taken out into marks [(file, id, mark)]."""
        def mk(m):
            if marks is not None: marks.append((m.group(1), m.group(2), normalize(html.unescape(re.sub('<[^>]+>', '', m.group(3))))))
            return '\x00' + str(len(marks) - 1 if marks is not None else 0) + '\x00'
        h = re.sub(r'<a href="([^"#]*)#([^"]+)"[^>]*>(.*?)</a>', mk, h, flags=re.S)
        h = re.sub(r'<img src="([^"]+)"[^>]*/?>', lambda m: HALF if posixpath.basename(m.group(1)) == self.half else ' ', h)
        return normalize(html.unescape(re.sub(r'<[^>]+>', '', h)))

    def read_notes(self, f):
        cur = None
        for st, h, i, after in self.blocks(f):
            if not after: continue
            # one block may hold several notes, each starting at an anchor <span id="…"></span>
            pieces = re.split(r'<span id="([^"]+)"></span>', h)
            head = [(i, pieces[0])] + [(pieces[k], pieces[k + 1]) for k in range(1, len(pieces), 2)]
            for j, (pid, ph) in enumerate(head):
                t = self.text(re.sub(r'<a href[^>]*>(.*?)</a>', r'\1', ph))
                if pid: cur = (posixpath.basename(f), pid); self.notes[cur] = [t] if t else []
                elif cur and t: self.notes[cur].append(t)

def parse(path):
    B = Book(path)
    log = []
    vol = {'parvas': [], 'half': B.half}
    P = A = None; upa = None; state = 'out'; pending_spk = []; cur = None; inparen = False
    def L(kind, msg): log.append({'kind': kind, 'at': f"{P['name'] if P else '-'} {A['n'] if A else '-'}", 'msg': msg})
    held = None; dq = []
    def emit(x):
        """A finished block: while a numbered verse waits for a dākṣiṇātya passage inside it, the passage (and its Hindi)
        goes after that verse."""
        nonlocal dq
        if held is not None: dq.append(x); return
        A['blocks'].append(x)
        if x.get('end') == 'n' or x.get('end') == 'none': A['blocks'].extend(dq); dq = []
    def flush_verse(reason):
        nonlocal cur, held, dq
        if held is not None:
            L('unended', f'{reason} (held): {held["lines"]}'); h = held; held = None; h['end'] = 'none'; emit(h)
        if cur and cur['lines']:
            prev = [x for x in A['blocks'] if x.get('kind') in ('v', 'g')] if A else []
            if reason == 'iti' and prev and len(cur['lines']) == 1:
                L('tail_joined', f'{cur["lines"]} → {prev[-1]["lines"][-1]}'); prev[-1]['lines'] += cur['lines']; prev[-1]['tail'] = True
            else:
                L('unended', f'{reason}: {cur["lines"]}')
                cur['end'] = 'none'; emit(cur)
        cur = None
        if dq: A['blocks'].extend(dq); dq = []
    def take(s, r, notes, st):
        """One verse line, prose passage or speaker, into the verse being read."""
        nonlocal cur, held, inparen, pending_spk
        if s.startswith('('):   # a dākṣiṇātya passage opens; inside a numbered verse, that verse waits for it
            if cur is not None and cur['lines'] and not cur['dak']:
                if held is not None: L('held2', f'{held["lines"]}')
                held = cur; cur = None
            elif cur is not None and cur['lines']:   # a bracket opens while one is open: the first ends in a half verse
                L('nested', f'{cur["lines"]} / {s}'); cur['end'] = 'paren'; emit(cur); cur = None
            inparen = True; s = s[1:].lstrip()
        cl = s.endswith(')')
        if cl: s = s[:-1].rstrip()
        if r == 'speaker' and cur is None: pending_spk.append(s)
        else:
            if cur is None:
                cur = {'kind': 'g' if r == 'gadya' else 'v', 'lines': list(pending_spk), 'spk': list(pending_spk), 'dak': inparen, 'paren': inparen, 'notes': [], 'ml': st['ml']}
                pending_spk = []
            cur['lines'].append(s); cur['notes'] += notes
            if r == 'speaker': cur.setdefault('mid', []).append(s)
            if r == 'gadya': cur['kind'] = 'g'
            m = re.search(r'॥\s*([०-९]+%s?)\s*॥$' % HALF, s)
            if m:
                if cur['dak']:   # a numbered verse inside ( … ): the book left the bracket open after the last bare ॥
                    L('paren_unclosed', s); cur['dak'] = False; inparen = False
                    if held is not None: L('held_lost', f'{held["lines"]}'); h = held; held = None; h['end'] = 'none'; emit(h)
                cur['n'] = m.group(1); cur['end'] = 'n'; emit(cur); cur = None
            elif s.endswith('॥'):   # no number: the dākṣiṇātya reading, in ( … ) or (in a long passage) without
                cur['dak'] = True; cur['end'] = 'bare'; emit(cur); cur = None
        if cl:
            if cur is not None and cur['lines']:   # a dākṣiṇātya passage that ends in a half verse
                cur['dak'] = True; cur['end'] = 'paren'; emit(cur); cur = None
            elif pending_spk and inparen: L('spk_paren', f'{pending_spk}')
            inparen = False
            if held is not None: cur = held; held = None
    for f in B.spine:
        fb = posixpath.basename(f)
        for st, h, bid, after in B.blocks(f):
            if after: continue
            marks = []
            t = B.text(h, marks)
            notes = [dict(mark=mk, note=B.notes.get((posixpath.basename(tf) or fb, ti))) for tf, ti, mk in marks]
            t_plain = re.sub(r'\x00\d+\x00', '', t)
            t_marked = re.sub(r'\x00(\d+)\x00', lambda m: marks[int(m.group(1))][2], t)
            if not t_plain and not notes: continue
            r = role(st, t_plain)
            if A is not None and r in ('verse', 'gadya', 'para', 'speaker', 'iti', 'iti_hi'):
                for n in notes:
                    if n['note'] is None: L('note', f'no note for mark {n["mark"]} in {t_plain[:60]}')
            if r == 'parva':
                flush_verse('parva')
                P = {'name': t_plain, 'adh': []}; vol['parvas'].append(P); A = None; state = 'parva'; upa = None; continue
            if P is None: continue   # front matter
            if r == 'upaparva' and re.search(r'श्लोक-?संख्या', t_plain):   # the book's table of verse counts: the end
                flush_verse('count'); A = None; state = 'out'; continue
            if r == 'upaparva' and re.fullmatch(r'श्रवण-?महिमा', t_plain):   # the hearing's merit, after a parva's last adhyāya
                flush_verse('mahima')
                A = {'word': None, 'title': t_plain, 'upaparva': upa, 'blocks': [], 'iti': None, 'iti_hi': None, 'daknote': None, 'n': None, 'extra': 'mahima'}
                P['adh'].append(A); state = 'in'; pending_spk = []; inparen = False; continue
            if r == 'upaparva':
                flush_verse('upaparva'); upa = t_plain.strip('()'); state = 'parva'; continue
            if r == 'title' and state == 'parva' and A is not None:   # a closing piece with a heading and no adhyāya number
                flush_verse('extra')
                A = {'word': None, 'title': t_plain, 'upaparva': upa, 'blocks': [], 'iti': None, 'iti_hi': None, 'daknote': None, 'n': None, 'extra': 'vidhi'}
                P['adh'].append(A); state = 'in'; pending_spk = []; inparen = False; continue
            if r == 'adh':
                flush_verse('adh')
                A = {'word': t_plain, 'title': None, 'upaparva': upa, 'blocks': [], 'iti': None, 'iti_hi': None, 'daknote': None, 'n': None}
                if not t_plain.endswith('ध्यायः'): A['extra'] = 'mahima' if 'महिमा' in t_plain else 'mahatmya'; A['title'] = t_plain   # महाभारत-माहात्म्य
                P['adh'].append(A); state = 'title'; pending_spk = []; inparen = False; continue
            if A is None:
                if r not in ('toc', 'caption', 'big'): L('outside', f'{r}: {t_plain[:80]}')
                continue
            if state == 'title':
                if r == 'title': A['title'] = t_plain; state = 'in'; continue
                state = 'in'
            if r == 'title' and state == 'in' and not A['blocks'] and not pending_spk and A['title'] and A['title'].startswith('('):
                A['sub'] = A['title'].strip('()'); A['title'] = t_plain; continue   # the Gītā's adhyāyas: (श्रीमद्भगवद्‌गीतायां प्रथमोऽध्यायः), then the title
            if state == 'end' and re.fullmatch(r'श्रवण-?महिमा', t_plain):   # the hearing's merit, after a parva's last adhyāya
                flush_verse('mahima')
                A = {'word': None, 'title': t_plain, 'upaparva': upa, 'blocks': [], 'iti': None, 'iti_hi': None, 'daknote': None, 'n': None, 'extra': 'mahima'}
                P['adh'].append(A); state = 'in'; pending_spk = []; inparen = False; continue
            if r == 'title' and state in ('in', 'end'):
                L('title2', t_plain[:80]); continue
            if r == 'iti':
                flush_verse('iti'); A['iti'] = dict(t=t_plain, notes=notes); state = 'end'
                m = re.search(r'॥\s*([०-९]+)\s*॥\s*$', t_plain)
                A['n'] = int(m.group(1).translate(str.maketrans('०१२३४५६७८९', '0123456789'))) if m else None
                if not m: L('iti', f'no number: {t_plain}')
                continue
            if r == 'iti_hi':
                if A['iti_hi']: L('iti_hi2', t_plain)
                else: A['iti_hi'] = dict(t=t_marked, notes=notes)
                continue
            if r == 'daknote': A['daknote'] = t_plain; continue
            if state == 'end' and r == 'para' and t_plain.startswith('इस प्रकार') and not A['iti_hi']:
                A['iti_hi'] = dict(t=t_marked, notes=notes); continue
            if state == 'end':
                if r not in ('caption', 'small', 'toc', 'big', 'title'): L('after_iti', f'{r}: {t_plain[:100]}')
                continue
            if r == 'head':
                if A is not None and state == 'in': A['blocks'].append(dict(kind='head', t=t_plain))
                elif A is not None: L('head_after', t_plain)
                continue
            if r == 'caption' and re.fullmatch(r'\[[^\[\]]+\]|\([^()]+पर्व\)', t_plain):
                A['blocks'].append(dict(kind='head', t=t_plain)); continue
            if r in ('caption', 'toc', 'big'):
                if r == 'caption': L('caption', t_plain[:80])
                continue
            if r == 'small' or r == 'other':
                L(r, f'{st} {t_plain[:100]}'); continue
            if r == 'gadya' and is_hindi(t_plain):   # Hindi set in bold by mistake
                L('bold_hindi', t_plain[:100]); r = 'para'
            if r == 'para' and is_sanskrit(t_plain) and re.search(r'॥\s*[०-९]+%s?\s*॥$' % HALF, t_plain):
                L('para_sanskrit', t_plain[:80]); r = 'gadya'
            if r == 'para':
                emit(dict(kind='para', t=t_marked, notes=notes, open=bool((cur and cur['lines']) or held)))
                continue
            if r == 'verse' and t_plain.startswith('मातापितृसहस्राणि') and P['name'] != 'स्वर्गारोहणपर्व' and (A is None or A.get('extra') or state != 'in'):
                flush_verse('savitri'); A = None; state = 'out'; L('savitri', P['name']); continue   # a volume's last page: the Bhārata-sāvitrī (Svargārohaṇa 5.60–64)
            if r in ('verse', 'gadya') and re.search(r'\((गीता|मनुस्मृति)[^()]*\)?\s*$', t_plain):   # a verse quoted under a picture
                L('caption_verse', f'{(cur or {}).get("lines")} / {t_plain}'); cur = None; continue
            if r == 'gadya' and t_plain.startswith('ॐ नमो भगवते वासुदेवाय') and cur is None:   # the Ādiparva's opening invocation
                emit({'kind': 'g', 'lines': [t_plain], 'spk': [], 'dak': False, 'paren': False, 'notes': notes, 'end': 'invocation'}); continue
            if r == 'speaker' or r in ('verse', 'gadya'):
                s = t_plain
                # the number's marks as the book slips them: । १८ ॥, ॥ ११।, ॥ ३५, ॥ ७३ ॥,
                s2 = re.sub(r'(?:॥|।)\s*([०-९]+%s?)\s*(?:॥|।)?\s*,?$' % HALF, r'॥ \1 ॥', s) if re.search(r'[०-९]\s*[।॥]?\s*,?$', s) else s
                if s2 != s:
                    if not re.search(r'॥\s*[०-९]+%s?\s*॥$' % HALF, s): L('end_fixed', f'{s[-30:]} → {s2[-30:]}')
                    s = s2
                # a prose paragraph that holds several numbered passages: one item each
                cuts = [m.end() for m in re.finditer(r'॥\s*[०-९]+%s?\s*॥' % HALF, s) if s[m.end():].strip()] if r == 'gadya' else []
                parts = [s[a:b].strip() for a, b in zip([0] + cuts, cuts + [len(s)])]
                if len(parts) > 1 and all(re.search(r'॥\s*[०-९]+%s?\s*॥$' % HALF, x) for x in parts[:-1]):
                    L('gadya_split', f'{len(parts)}: {s[:60]}')
                    for x in parts[:-1]: take(x, r, notes, st); notes = []
                    s = parts[-1]
                # a bracket that closes inside the line: before it is the dākṣiṇātya reading, after it the text goes on
                k = s.find(')')
                if 0 <= k < len(s) - 1 and (inparen or s.startswith('(')):
                    rest = s[k + 1:].strip()
                    if re.fullmatch(r'[।॥\s]*', rest): take(s[:k].rstrip() + (' ' + rest if rest else '') + ')', r, notes, st)
                    else:
                        L('split_paren', s); take(s[:k + 1], r, notes, st); take(rest, r, [], st)
                else: take(s, r, notes, st)
                continue
            L('unclassed', f'{r} {st} {t_plain[:80]}')
    return vol, log

if __name__ == '__main__':
    vol, log = parse(sys.argv[1])
    vol['log'] = log
    json.dump(vol, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print(os.path.basename(sys.argv[1]), 'parvas', [(p['name'], len(p['adh'])) for p in vol['parvas']])
    print(' log', Counter(l['kind'] for l in log))
