"""Sri Guru Granth Sahib: the Shabad OS database (@shabados/database 4.8.7 on npm) → ../text.txt.

    python3 tools/works/guru-granth-sahib/source/make.py [--db <database.sqlite>]   (or $SHABADOS_DB; shabados.py)

The database holds the Granth as 5,549 "shabads" (its display units) of 60,555 lines (pangtis), each line with its Ang.
Its lines are the Granth's own, each ending with ॥ as printed; shabados.py converts them. This script makes them the
library's verses (README.md, "Structure"; every choice in reconciliation.md):

- parts: the 51 sections of the Granth (the database's sections: Jap, So Dar, So Purakh, Sohila, the 31 raags, the
  closing compositions from Salok Sahaskriti to Raagmala);
- the Japji Sahib and the Sukhmani Sahib are taken from their works ([take …]); their lines equal the database's
  (check.py proves it on every run);
- one verse is one shabad, or one pauri or salok of a composition: the database's units, except
  · a unit of headings only (ਰਾਗੁ ਆਸਾ ਮਹਲਾ ੩ ਪਟੀ ॥) joins the verse after it;
  · a chhant the database cuts into its stanzas and their saloks (ਡਖਣੇ) is one verse again, as the Granth numbers it
    (॥੫॥੧॥੩॥ at its end): a run of one-stanza units whose numbers interleave, closed by the stanza that numbers the whole;
    a shabad of three or four stanzas cut the same way (Kuchaji) also;
  · a bani the database keeps whole although the Granth numbers its pauris or saloks one by one (the Anand, the Oankar,
    the Pattis, the Thitis, Kabir's Bavan Akhri, the Gatha, the Phunhe, the Saloks Varan te Vadhik) and the units that
    hold two or more pauris or saloks of a series (the Sidh Gosht) are cut at every stanza's number, a rahao in them
    being a verse of its own (as in the Sukhmani Sahib);
- ids: the Ang a verse begins on and its place among this text's verses beginning there (14.1, 14.2 …); permanent;
- sections: the Ang (the reader's footer and pages: "Ang 14"); a verse is cited by its Ang and its place (Shabad 14.2);
- types: shabad, pauri, salok, rahao, pad (a stanza of the Bara Mahas, the Ruti, the Gatha, the Phunhe, the Chaubole),
  swayya (the Swayye);
- topics: every shabad, and every salok and swayya of the closing compositions, by its first line; a composition (a
  vaar, a bani of pauris or stanzas) once, at its start, by its heading.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE); WORKS = os.path.dirname(WORK)
sys.path.insert(0, HERE); import shabados
sys.path.insert(0, WORKS); import textfile
import importlib.util
_j = importlib.util.spec_from_file_location('japji_make', os.path.join(WORKS, 'japji-sahib', 'source', 'make.py'))
japji = importlib.util.module_from_spec(_j); _j.loader.exec_module(japji); pratik = japji.pratik   # the Japji's topic names

G2A = str.maketrans('੦੧੨੩੪੫੬੭੮੯', '0123456789')
# the database's units that are whole banis whose pauris or saloks the Granth numbers one by one (cut at each number)
WHOLE = {'D91': 'pauri',    # Gauri, Bavan Akhri Kabir Ji (Ang 340)
         '0A5': 'pauri',    # Gauri, Thiti Kabir Ji (Ang 343)
         '8KZ': 'pauri',    # Asa, Patti Likhi Mahala 1 (Ang 432)
         'YGD': 'pauri',    # Asa, Patti Mahala 3 (Ang 434)
         'D8X': 'pauri',    # Bilaval, Thiti Mahala 1 (Ang 838)
         'TUY': 'pauri',    # Ramkali, Anand Mahala 3 (Ang 917)
         'TNM': 'pauri',    # Ramkali, Dakhni Oankar Mahala 1 (Ang 929)
         '15N': 'pad',      # Gatha Mahala 5 (Ang 1360)
         'FMU': 'pad',      # Phunhe Mahala 5 (Ang 1361)
         'G51': 'pauri',    # Ramkali, Sidh Gosht (Ang 938): its first unit (pauris 1–2 and the rahao)
         '6EE': 'salok', '6X5': 'salok', '39Y': 'salok', '6NP': 'salok'}   # Salok Varan te Vadhik (Ang 1410–1426)
SALOK_PARTS = {36, 40, 41, 48, 49, 50}          # Salok Sahaskriti, Kabir, Farid, Varan te Vadhik, Mahala 9, Mundavani
STANZA_PARTS = {37, 38, 39}                     # Gatha, Phunhe, Chaubole
SWAYYE = set(range(42, 48))
SALOK_HEAD = re.compile(r'(^|\s)(ਸਲੋਕ|ਸਲੋਕੁ)( |$)|^(ਮਃ|ਮਹਲਾ [੧-੯] ॥$|ਡਖਣਾ|ਡਖਣੇ|ਮਰਦਾਨਾ)')
PAURI = re.compile(r'^(ਪਉੜੀ|ਪਵੜੀ)')
# compositions of stanzas the database keeps one per unit, from their first unit to the stanza that numbers the whole:
# the type of their stanzas (their saloks are saloks)
COMPS = {'FME': 'pad',      # Majh, Bara Maha Mahala 5 (Ang 133)
         '4CY': 'pad',      # Tukhari, Bara Maha Mahala 1 (Ang 1107)
         '7N1': 'pad',      # Ramkali, Ruti Mahala 5 (Ang 927)
         '5KD': 'pauri'}    # Ramkali, the Vaar of Rai Balvand and Satta Doom (Ang 966)

# corrections of the database's text: {database line id: (as the database has it, as it is written here)}; each is in
# reconciliation.md §3 with its witnesses
FIX = {'B5FS': ('ਕਿਸੁ ਹਉ ਜਾਚੀ ਕਿਸੁ ਆਰਾਧੀ ਜਾ ਸਭੁ ਕੋ ਕੀਤਾ ਹੋਸੀ ॥', 'ਕਿਸੁ ਹਉ ਜਾਚੀ ਕਿਸ ਆਰਾਧੀ ਜਾ ਸਭੁ ਕੋ ਕੀਤਾ ਹੋਸੀ ॥')}   # Ang 608

KEYS = ['jap', 'so-dar', 'so-purakh', 'sohila', 'sri-raag', 'majh', 'gauri', 'asa', 'gujri', 'devgandhari', 'bihagra',
        'vadhans', 'sorath', 'dhanasari', 'jaitsri', 'todi', 'bairari', 'tilang', 'suhi', 'bilaval', 'gond', 'ramkali',
        'nat-narain', 'mali-gaura', 'maru', 'tukhari', 'kedara', 'bhairao', 'basant', 'sarang', 'malar', 'kanra', 'kalyan',
        'prabhati', 'jaijavanti', 'salok-sahaskriti', 'gatha', 'phunhe', 'chaubole', 'salok-kabir', 'salok-farid',
        'swayye-mukhbak', 'swayye-m1', 'swayye-m2', 'swayye-m3', 'swayye-m4', 'swayye-m5', 'salok-vadhik', 'salok-m9',
        'mundavani', 'raagmala']


def chain(s):
    """The numbers at a line's end: ॥੪॥੧॥੩੪॥ → [4, 1, 34]; a vaar's last pauri's ਸੁਧੁ (ਕੀਚੇ) after them is passed over."""
    s = re.sub(r'\s*ਸੁਧੁ( ਕੀਚੇ)?( ॥)?\s*$', '', s)
    m = re.search(r'((?:॥[੦-੯]+)+॥)\s*$', s)
    return [int(x.translate(G2A)) for x in re.findall('[੦-੯]+', m.group(1))] if m else []


def ends(u): return [i for i, l in enumerate(u['lines']) if chain(l['v'])]
def headonly(u): return all(l['type'] in (1, 2) for l in u['lines'])
def piece(u): return len(u['c']) == 1 and len(u['ends']) == 1 and not headonly(u)


def takes(U):
    """The database units of the Japji Sahib (section 1) and of the Sukhmani Sahib (Ang 262–296)."""
    jap = [k for k, u in enumerate(U) if u['section'] == 1]
    a = next(k for k, u in enumerate(U) if u['lines'][0]['v'] == 'ਗਉੜੀ ਸੁਖਮਨੀ ਮਃ ੫ ॥')
    b = next(k for k, u in enumerate(U) if k > a and u['lines'][-1]['v'].endswith('॥੮॥੨੪॥'))
    assert jap == list(range(jap[0], jap[-1] + 1)) and U[b + 1]['lines'][0]['v'] == 'ਥਿਤੀ ਗਉੜੀ ਮਹਲਾ ੫ ॥'
    return set(jap), set(range(a, b + 1))


def cut(lines, y):
    """Cut a whole bani at every stanza's number: [(type, lines)]; a rahao (database type 3) that follows a stanza's
    number is a verse of its own (as in the Sukhmani Sahib)."""
    out, cur, rahao = [], [], False
    for l in lines:
        if l['type'] == 3 and not cur: rahao = True
        cur.append(l)
        if rahao and 'ਰਹਾਉ' in l['v']: out.append(('rahao', cur)); cur, rahao = [], False
        elif not rahao and chain(l['v']): out.append((y, cur)); cur = []
    assert not cur, [x['v'] for x in cur]
    return out


def verses(U):
    """The database units → this text's verses [{'y', 'lines', 'part', 'db'}] (and the takes, as {'take': …})."""
    JAP, SUKH = takes(U)
    for k, u in enumerate(U): u['k'] = k
    done = set()
    for u in U:
        for l in u['lines']:
            if l['id'] in FIX:
                assert l['v'] == FIX[l['id']][0], (l['id'], l['v']); l['v'] = FIX[l['id']][1]; done.add(l['id'])
    assert done == set(FIX), set(FIX) - done
    # 0. a shabad's heading that the database puts at the end of the unit before it goes to its own shabad
    for a, b in zip(U, U[1:]):
        if a['lines'][-1]['type'] == 2 and b['lines'][0]['type'] in (3, 4) and len(a['lines']) > 1:
            b['lines'].insert(0, a['lines'].pop()); b.setdefault('moved', []).append(a['sid'])
    for u in U: u['c'] = chain(u['lines'][-1]['v']); u['ends'] = ends(u)
    # 1. units of headings only join the next unit
    V, carry = [], []
    for u in U:
        if headonly(u) and u['k'] not in JAP | SUKH: carry += u['lines']; continue
        if carry: u = dict(u, lines=carry + u['lines']); carry = []
        V.append(u)
    assert not carry
    # 2. a chhant cut into its stanzas and their saloks is one verse again (not inside a composition of COMPS)
    inside, on = set(), False
    for u in V:
        on = on or u['sid'] in COMPS
        if on: inside.add(u['k'])
        if on and len(u['c']) >= 2: on = False
    merged, k = [], 0
    while k < len(V):
        u = V[k]
        if u['section'] < 36 and piece(u) and u['k'] not in JAP | SUKH | inside:
            j = k
            while j < len(V) and piece(V[j]) and V[j]['section'] == u['section'] and V[j]['k'] not in inside: j += 1
            run = V[k:j]; nxt = V[j] if j < len(V) else None
            nums = [x['c'][0] for x in run]
            pauri = any(PAURI.match(x['lines'][0]['v']) for x in run)
            inc = nums[0] == 1 and all(b == a + 1 for a, b in zip(nums, nums[1:]))
            closer = nxt is not None and len(nxt['c']) >= 2 and nxt['section'] == u['section']
            if not pauri and closer and not inc and nxt['c'][0] in (max(nums), max(nums) + 1):
                merged.append(dict(nxt, lines=[l for x in run for l in x['lines']] + nxt['lines'], merged=[x['sid'] for x in run] + [nxt['sid']]))
                k = j + 1; continue
            merged += run; k = j; continue
        merged.append(u); k += 1
    # 3. verses, with their types; whole banis, series chunks and units of two saloks cut at each stanza
    out, prev_take, comp = [], None, None
    for i, u in enumerate(merged):
        if u['k'] in JAP or u['k'] in SUKH:
            t = 'japji' if u['k'] in JAP else 'sukhmani'
            if t != prev_take: out.append({'take': t, 'part': u['section'] - 1})
            prev_take = t; continue
        prev_take = None
        part = u['section'] - 1; L = u['lines']; sec = u['section']
        if u['sid'] in COMPS: comp = COMPS[u['sid']]
        nxt = merged[i + 1] if i + 1 < len(merged) else None; prv = merged[i - 1] if i else None
        salok = len(u['c']) <= 1 and any(SALOK_HEAD.search(l['v']) and 'ਵਾਰ' not in l['v'] for l in L if l['type'] in (1, 2) or l is L[0])
        series = (len(u['c']) >= 1 and len(u['ends']) >= 2 and not any(l['type'] == 3 for l in L) and
                  ((prv and prv['c'][:1] == [chain(L[u['ends'][0]]['v'])[0] - 1]) or
                   (nxt and nxt['ends'] and chain(nxt['lines'][nxt['ends'][0]]['v'])[:1] == [u['c'][0] + 1])))
        if sec in SWAYYE: y = 'swayya'
        elif sec in SALOK_PARTS: y = 'salok'
        elif sec in STANZA_PARTS: y = 'pad'
        elif PAURI.match(L[0]['v']): y = 'pauri'
        elif salok: y = 'salok'
        elif comp: y = comp
        else: y = 'shabad'
        if u['sid'] in WHOLE: y = WHOLE[u['sid']]
        if series and y == 'shabad': y = 'pauri'   # two or more pauris of a series (the Sidh Gosht)
        if comp and len(u['c']) >= 2: comp = None   # the stanza that numbers the whole ends the composition
        if (u['sid'] in WHOLE or series or (y in ('salok', 'pad') and len(u['ends']) >= 2)) and y != 'shabad':
            for yy, ls in cut(L, y): out.append({'y': yy, 'lines': ls, 'part': part, 'comp': u['sid'], 'db': u['sid']})
            continue
        out.append({'y': y, 'lines': L, 'part': part, 'db': u['sid'], 'merged': u.get('merged')})
    return out


def main(argv):
    db = argv[argv.index('--db') + 1] if '--db' in argv else shabados.EXTRACT   # the committed extract, or the database
    U = shabados.units(db)
    V = verses(U)
    # stanzas of compositions: a run of pauri/salok/pad verses (not shabads) in a raag; they are typed in verses()
    seen, items, topics = {}, [], []
    comp_open = None
    for x in V:
        if 'take' in x: items.append(x); comp_open = None; continue
        ang = x['lines'][0]['ang']; seen[ang] = seen.get(ang, 0) + 1
        x['id'] = f'{ang}.{seen[ang]}'; x['n'] = str(seen[ang]); x['s'] = str(ang); x['p'] = x['part']
        x['v'] = [l['v'] for l in x['lines']]
        alone = x['y'] == 'shabad' or (x['part'] + 1 in SALOK_PARTS | SWAYYE and x['y'] in ('salok', 'swayya'))
        pankti = next((l['v'] for l in x['lines'] if l['type'] == 4), x['v'][0])
        if alone: topics.append({'id': x['id'], **pratik(pankti)}); comp_open = None
        elif comp_open is None or comp_open != (x['part'], x.get('comp') or 'run'):
            topics.append({'id': x['id'], **pratik(x['v'][0])}); comp_open = (x['part'], x.get('comp') or 'run')
        items.append(x)
    write(items, topics)
    vw = views(U, items)
    # one writer's or one Ang's entry per line, so the file reads and diffs line by line
    with open(os.path.join(WORK, 'views.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(vw, ensure_ascii=False, separators=(',', ':')).replace('{"id":', '\n{"id":') + '\n')
    own =[x for x in items if 'take' not in x]
    import collections
    for x in own:
        if x.get('merged'): print('one verse again:', x['id'], x['merged'])
    print(f'{len(own)} verses of our own, {sum(len(x["v"]) for x in own)} lines; {len(topics)} topics;',
          dict(collections.Counter(x['y'] for x in own)))


# The writers (the database's writer ids; names as the database gives them in Gurmukhi, in plain English and Hindi), in
# four groups, each group's writers in the order of their English names (the Gurus by Mahala)
GROUPS = [({'hi': 'गुरु साहिबान', 'en': 'Gurus', 'pa': 'ਗੁਰੂ ਸਾਹਿਬਾਨ'}, [
    (1, 'guru-nanak-dev', 'गुरु नानक देव जी', 'Guru Nanak Dev Ji', 'ਗੁਰੂ ਨਾਨਕ ਦੇਵ ਜੀ', 1),
    (2, 'guru-angad-dev', 'गुरु अंगद देव जी', 'Guru Angad Dev Ji', 'ਗੁਰੂ ਅੰਗਦ ਦੇਵ ਜੀ', 2),
    (3, 'guru-amar-das', 'गुरु अमरदास जी', 'Guru Amar Das Ji', 'ਗੁਰੂ ਅਮਰਦਾਸ ਜੀ', 3),
    (4, 'guru-ram-das', 'गुरु रामदास जी', 'Guru Ram Das Ji', 'ਗੁਰੂ ਰਾਮਦਾਸ ਜੀ', 4),
    (5, 'guru-arjan-dev', 'गुरु अर्जन देव जी', 'Guru Arjan Dev Ji', 'ਗੁਰੂ ਅਰਜਨ ਦੇਵ ਜੀ', 5),
    (6, 'guru-tegh-bahadur', 'गुरु तेग़ बहादुर जी', 'Guru Tegh Bahadur Ji', 'ਗੁਰੂ ਤੇਗ਼ ਬਹਾਦਰ ਜੀ', 9)]),
  ({'hi': 'भगत', 'en': 'Bhagats', 'pa': 'ਭਗਤ'}, [
    (8, 'bhagat-beni', 'भगत बेणी जी', 'Bhagat Beni Ji', 'ਭਗਤ ਬੇਣੀ ਜੀ', None),
    (9, 'bhagat-bhikhan', 'भगत भीखन जी', 'Bhagat Bhikhan Ji', 'ਭਗਤ ਭੀਖਨ ਜੀ', None),
    (10, 'bhagat-dhanna', 'भगत धन्ना जी', 'Bhagat Dhanna Ji', 'ਭਗਤ ਧੰਨਾ ਜੀ', None),
    (12, 'bhagat-jaidev', 'भगत जयदेव जी', 'Bhagat Jaidev Ji', 'ਭਗਤ ਜੈਦੇਵ ਜੀ', None),
    (13, 'bhagat-kabir', 'भगत कबीर जी', 'Bhagat Kabir Ji', 'ਭਗਤ ਕਬੀਰ ਜੀ', None),
    (14, 'bhagat-namdev', 'भगत नामदेव जी', 'Bhagat Namdev Ji', 'ਭਗਤ ਨਾਮਦੇਵ ਜੀ', None),
    (15, 'bhagat-parmanand', 'भगत परमानंद जी', 'Bhagat Parmanand Ji', 'ਭਗਤ ਪਰਮਾਨੰਦ ਜੀ', None),
    (16, 'bhagat-pipa', 'भगत पीपा जी', 'Bhagat Pipa Ji', 'ਭਗਤ ਪੀਪਾ ਜੀ', None),
    (17, 'bhagat-ramanand', 'भगत रामानंद जी', 'Bhagat Ramanand Ji', 'ਭਗਤ ਰਾਮਾਨੰਦ ਜੀ', None),
    (18, 'bhagat-ravidas', 'भगत रविदास जी', 'Bhagat Ravidas Ji', 'ਭਗਤ ਰਵਿਦਾਸ ਜੀ', None),
    (19, 'bhagat-sadhna', 'भगत सधना जी', 'Bhagat Sadhna Ji', 'ਭਗਤ ਸਾਧਨਾ ਜੀ', None),
    (20, 'bhagat-sain', 'भगत सैण जी', 'Bhagat Sain Ji', 'ਭਗਤ ਸੈਣ ਜੀ', None),
    (11, 'sheikh-farid', 'शेख़ फ़रीद जी', 'Sheikh Farid Ji', 'ਸ਼ੇਖ ਫਰੀਦ ਜੀ', None),
    (21, 'bhagat-surdas', 'भगत सूरदास जी', 'Bhagat Surdas Ji', 'ਭਗਤ ਸੂਰਦਾਸ ਜੀ', None),
    (22, 'bhagat-trilochan', 'भगत त्रिलोचन जी', 'Bhagat Trilochan Ji', 'ਭਗਤ ਤ੍ਰਿਲੋਚਨ ਜੀ', None)]),
  ({'hi': 'भट्ट', 'en': 'Bhatts', 'pa': 'ਭੱਟ'}, [
    (24, 'bhatt-balh', 'भट्ट बल्ह', 'Bhatt Balh', 'ਭੱਟ ਬਲੵ', None),
    (25, 'bhatt-bhalh', 'भट्ट भल्ह', 'Bhatt Bhalh', 'ਭੱਟ ਭਲੵ', None),
    (26, 'bhatt-bhikha', 'भट्ट भिखा', 'Bhatt Bhikha', 'ਭੱਟ ਭਿਖਾ', None),
    (27, 'bhatt-gayand', 'भट्ट गयंद', 'Bhatt Gayand', 'ਭੱਟ ਗਯੰਦ', None),
    (28, 'bhatt-harbans', 'भट्ट हरिबंस', 'Bhatt Harbans', 'ਭੱਟ ਹਰਿਬੰਸ', None),
    (29, 'bhatt-jalap', 'भट्ट जालप', 'Bhatt Jalap', 'ਭੱਟ ਜਾਲਪ', None),
    (30, 'bhatt-kalh-sahar', 'भट्ट कल्ह सहार', 'Bhatt Kalh Sahar', 'ਭੱਟ ਕਲੵ ਸਹਾਰ', None),
    (31, 'bhatt-kirat', 'भट्ट कीरत', 'Bhatt Kirat', 'ਭੱਟ ਕੀਰਤੁ', None),
    (32, 'bhatt-mathura', 'भट्ट मथुरा', 'Bhatt Mathura', 'ਭੱਟ ਮਥੁਰਾ', None),
    (33, 'bhatt-nalh', 'भट्ट नल्ह', 'Bhatt Nalh', 'ਭੱਟ ਨਲੵ', None),
    (34, 'bhatt-salh', 'भट्ट सल्ह', 'Bhatt Salh', 'ਭੱਟ ਸਲੵ', None)]),
  ({'hi': 'अन्य', 'en': 'Others', 'pa': 'ਹੋਰ'}, [
    (35, 'satta-balwand', 'सत्ता और बलवंड', 'Satta and Balwand', 'ਸਤਾ ਤੇ ਬਲਵੰਡਿ', None),
    (23, 'baba-sundar', 'बाबा सुंदर', 'Baba Sundar', 'ਬਾਬਾ ਸੁੰਦਰ', None)])]
# the Raagmala: the Granth names no writer for it (the database's "Poet Alam" is an attribution, not the text's), so it is
# in no writer's list
NO_WRITER = {42}
# a verse whose own heading names a Mahala, where the database names a Bhagat: the heading is the Granth's word
# (reconciliation.md §4); a vaar's heading names the vaar's writer, not its saloks', so it does not count
MAHALA = {'੧': 1, '੨': 2, '੩': 3, '੪': 4, '੫': 5, '੯': 6}


def writer_of(x, W):
    """A verse's writer: the database's for its unit, unless its own heading names a Mahala and the database a Bhagat."""
    w = W[x['db']]
    for l in x['lines']:
        if l['type'] not in (1, 2): break
        m = re.search(r'(?:ਮਹਲਾ|ਮਃ) ([੧-੯])', l['v'])
        if m and 'ਵਾਰ' not in l['v']:
            if w > 6 and w not in NO_WRITER: w = MAHALA[m.group(1)]
            break
    return w


def views(U, items):
    """The Granth's other two classifications (work.json → views): its writers (the verses each wrote, in the Granth's
    order) and its Angs (for each of the 1,430 Angs, the verse its first line is in)."""
    W = {u['sid']: u['writer'] for u in U}
    JAP, SUKH = takes(U)
    taken = {w: [x for x in textfile.read(os.path.join(WORKS, w, 'text.txt'))] for w in ('japji-sahib', 'sukhmani-sahib')}
    by = {}; ang = {}
    for x in items:
        if 'take' in x:
            ks = sorted(JAP if x['take'] == 'japji' else SUKH); wr = {U[k]['writer'] for k in ks}
            assert len(wr) == 1, wr; wr = wr.pop()   # the database's writer of the whole bani
            vs = taken['japji-sahib' if x['take'] == 'japji' else 'sukhmani-sahib']
            # the database's lines of the taken bani, one by one beside the work's own (check.py proves them equal; the
            # Japji's Mool Mantar is one database line and four of the work's)
            dl = [l for k in ks for l in U[k]['lines']]; mine = [(v['id'], n) for v in vs for n in range(len(v['v']))]
            if x['take'] == 'japji': mine = [mine[0]] + mine[4:]
            assert len(dl) == len(mine)
            for l, (vid, _) in zip(dl, mine): ang.setdefault(l['ang'], vid)
            by.setdefault(wr, []).extend(v['id'] for v in vs)
            continue
        for l in x['lines']: ang.setdefault(l['ang'], x['id'])
        by.setdefault(writer_of(x, W), []).append(x['id'])
    assert sorted(ang) == list(range(1, 1431)), 'an Ang without a line'
    groups, named = [], set()
    for head, ws in GROUPS:
        lst = []
        for wid, key, hi, en, pa, mahala in ws:
            named.add(wid); w = {'id': key, 'hi': hi, 'en': en, 'pa': pa}
            if mahala: w['mahala'] = mahala
            w['items'] = by[wid]; lst.append(w)
        groups.append(dict(head, list=lst))
    assert set(by) - named == NO_WRITER, set(by) - named
    return {'views': [
        {'id': 'writer', 'name': {'hi': 'बाणीकार', 'en': 'Writer', 'pa': 'ਬਾਣੀਕਾਰ'}, 'groups': groups},
        {'id': 'ang', 'name': {'hi': 'अंग', 'en': 'Ang', 'pa': 'ਅੰਗ'}, 'at': [ang[n] for n in range(1, 1431)]}]}


def write(items, topics):
    """text.txt, through textfile.write (takes as [take …] lines)."""
    T = {t['id']: t for t in topics}
    out = ['# Sri Guru Granth Sahib. Made by source/make.py from the Shabad OS database (@shabados/database 4.8.7); do not',
           '# edit here. Every choice: reconciliation.md; source/check.py checks the text against its witnesses.']
    part = sec = None
    RUN = {'japji': '[take japji-sahib mool .. salok.close]', 'sukhmani': '[take sukhmani-sahib a01.title .. a24.p8]'}
    for x in items:
        if x['part'] != part: part = x['part']; out += ['', f'@part {KEYS[part]}']
        if 'take' in x: out.append(RUN[x['take']]); sec = None; continue
        if x['s'] != sec: sec = x['s']; out.append(f'@section {sec}')
        if x['id'] in T: out.append(f"@topic {T[x['id']]['hi']} | {T[x['id']]['en']}")
        out.append(f"[{x['id']} {x['y']} {x['n']}]")
        out += x['v']
    open(os.path.join(WORK, 'text.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
