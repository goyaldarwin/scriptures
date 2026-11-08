"""The work's meanings from the owner's copy (scriptures-data: printouts/sanskritdocuments/durga-saptashati.json).

    python3 tools/works/durga-saptashati/source/meanings.py <durga-saptashati.json>

Writes, in tools/works/durga-saptashati/meanings/:
  hi/scriptures.json, en/scriptures.json   ours: the owner's drafts (written from each verse with Claude), brought to
                                           tools/meanings/style.md by the rules below; meaning_fixes.json, beside this
                                           script, replaces a verse's draft where a rule cannot (each with its reason);
  en/pargiter.json                         F. E. Pargiter's English (The Mārkaṇḍeya Purāṇa, Bibliotheca Indica, 1904;
                                           public domain), copied as given; a passage he gives for several mantras sits
                                           under the last of them (the joint meaning under the last part, as in the Mānas).
The style rules, in order (the drafts are otherwise kept word for word):
  both   a mantra that is only a speaker's line (ऋषिरुवाच ॥, देवा ऊचुः ॥) has one meaning from one table (SPEAKER),
         its bīja first (ॐ ऐं।); square brackets go: their words are written into the sentence; quotation marks are curly,
         and a speech after a colon or कहा — is not quoted;
         adhyāya 5's triple namaskāras (या देवी सर्वभूतेषु …, three mantras each) are one refrain, the same every
         time (NAMAH): the stanza's opening line with the first namaskāra, then the second, then the third;
  en     the Devī is "the Devī" (the drafts' "the Goddess"), her pronouns in lower case; British spelling;
  hi     postpositions joined to the word before them (प्राणियोंमें, देवीको), as is the speaker's ने and -वाला
         (करनेवाली); ये for ए after a vowel (लिये, गये, किये; हुए stays) and गयी, आयी; ! after an address (हे देवि!);
         the Devī, addressed by those who praise her (the stutis, the stotras, ADDRESS), is आप, with honorific verbs
         (आप … हैं, रक्षा करें, प्रसन्न हों), as style.md §4 has a devotee address the Lord.
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'works')); sys.path.insert(0, HERE)
import jsonio, textfile
import make_text

ZWNJ = '‌'
SPEAKER = {   # a mantra that is a speaker's line → our meaning, Hindi and English (the bīja before it is kept)
    'मार्कण्डेय उवाच': ('मार्कण्डेयजीने कहा —', 'Mārkaṇḍeya said:'),
    'ऋषिरुवाच': ('मेधा ऋषिने कहा —', 'The sage Medhas said:'),
    'राजोवाच': ('राजा सुरथने कहा —', 'King Suratha said:'),
    'वैश्य उवाच': ('समाधि वैश्यने कहा —', 'Samādhi the merchant said:'),
    'ब्रह्मोवाच': ('ब्रह्माजीने कहा —', 'Brahmā said:'),
    'श्रीभगवानुवाच': ('श्रीभगवान्' + ZWNJ + 'ने कहा —', 'The Lord said:'),
    'देव्युवाच': ('देवीने कहा —', 'The Devī said:'),
    'देवा ऊचुः': ('देवताओंने कहा —', 'The gods said:'),
    'दूत उवाच': ('दूतने कहा —', 'The messenger said:'),
}
BIJA = {'ॐ': ('ॐ।', 'Oṃ.'), 'ॐ ऐं': ('ॐ ऐं।', 'Oṃ aiṃ.'), 'ॐ ह्रीं': ('ॐ ह्रीं।', 'Oṃ hrīṃ.'), 'ॐ क्लीं': ('ॐ क्लीं।', 'Oṃ klīṃ.')}
SPK = re.compile(r'^(?:(ॐ(?: ऐं| ह्रीं| क्लीं)?) )?(' + '|'.join(SPEAKER) + r') ॥')

# Where devotees address the Devī: the stotras, Brahmā's stuti (1.70–87), the gods' (4.3–27, 4.35–37, 5.9–82),
# the Nārāyaṇī stuti (11.2–35); never the Devī's own words, the sage's to the king or the demons'.
def ADDRESS(r):
    s, _, n = r.partition('.')
    if s in ('argala', 'kavacha', 'aparadha', 'kilaka'): return r != 'kavacha.46'   # 46: Brahmā to Mārkaṇḍeya
    if not n.isdigit(): return False
    n = int(n)
    return (s == '1' and 70 <= n <= 87) or (s == '4' and (3 <= n <= 27 or 35 <= n <= 37)) or (s == '5' and 9 <= n <= 82) or (s == '11' and 2 <= n <= 35)

PP = 'से|को|का|के|की|में|ने|पर|तक|द्वारा'
DEV = 'ऀ-ॣ०-ॿ'

def curly(s, double, single):
    """Straight quotation marks → curly, each kind paired in order (a quotation inside another keeps its own kind);
    an apostrophe inside a word stays."""
    out, open_ = [], {'"': False, "'": False}
    for i, ch in enumerate(s):
        if ch == "'" and i and s[i - 1].isalpha() and i + 1 < len(s) and s[i + 1].isalpha(): out.append('’'); continue
        if ch in open_:
            q = double if ch == '"' else single
            out.append(q[1] if open_[ch] else q[0]); open_[ch] = not open_[ch]
        else: out.append(ch)
    return ''.join(out)

def aap(s):
    """तुम → आप with honorific verbs, where a devotee speaks to the Devī."""
    W = r'(?![' + DEV + '])'
    for a, b in (('तुम्हारा', 'आपका'), ('तुम्हारे', 'आपके'), ('तुम्हारी', 'आपकी'), ('तुम्हें', 'आपको'), ('तुमने', 'आपने'),
                 ('तुमसे', 'आपसे'), ('तुममें', 'आपमें'), ('तुमको', 'आपको'), ('तुम', 'आप')):
        s = re.sub(rf'(?<![{DEV}]){a}{W}', b, s)
    s = re.sub(r'प्रसन्न हो(?=[\s,।;!—]|$)', 'प्रसन्न हों', s)                    # a request: be gracious
    s = s.replace('आप चाहो', 'आप चाहें')
    # requests: करो → करें (only where the verb ends its clause, so दो बिन्दु "two dots" stays)
    END = r'(?=\s*[,।;!?—]|\s+और\s|\s+तथा\s|$)'
    for v, w in (('करो', 'करें'), ('दो', 'दें'), ('हो जाओ', 'हो जायँ'), ('बचाओ', 'बचायें'), ('बनाओ', 'बनायें'), ('लो', 'लें'),
                 ('जाओ', 'जायँ'), ('रहो', 'रहें'), ('हरो', 'हरें'), ('रखो', 'रखें'), ('चाहो', 'चाहें'), ('दीजिए', 'दीजिये')):
        s = re.sub(rf'(?<![{DEV}]){v}{END}', w, s)
    # आप … हो → आप … हैं: in a sentence whose subject is आप (not आपकी, आपको …), every हो that is its verb
    # (not a wish, जय हो, nor "be it", सत् हो या असत्)
    def verb(m):
        t = m.group(0)
        if not re.search(rf'(?<![{DEV}])आप(?: ही)? ', t): return t
        return re.sub(rf'(?<!जय)(?<!सत्)(?<![{DEV}]हो) हो(?=[\s,।;?!]|$)(?! या)', ' हैं', t)
    s = re.sub(r'[^।;?!]+[।;?!]?', verb, s)
    return s

def unpaired(s):
    """A quotation mark left open or closed by a draft whose speech runs over several verses goes (style.md §3)."""
    for q in '"\'':
        if s.count(q) % 2: s = re.sub(rf'(?<![A-Za-z]){q}|{q}(?![A-Za-z])', '', s) if q == "'" else s.replace(q, '')
    return s

def hi(s, honour=False):
    s = unpaired(unicodedata.normalize('NFC', s.strip()))
    s = re.sub(r'\[([^\]]+)\]', r'\1', s)
    if honour: s = aap(s)
    s = re.sub(rf'(?<=[{DEV}])\s+({PP})(?=[\s,।;:!?—)\-]|$)', r'\1', s)
    s = s.replace('केद्वारा', 'के द्वारा')
    s = re.sub(rf'(?<=[{DEV}])\s+(वाला|वाले|वाली|वालों)(?=[\s,।;:!?—)\-]|$)', r'\1', s)
    s = re.sub(rf'(?<=[ािइआ])ए(?![{DEV}])', 'ये', s)
    s = re.sub(rf'(?<![{DEV}])(ग|न)ए(?![{DEV}])', r'\1ये', s)
    for a in ('गई', 'आई', 'पाई', 'नई', 'लाई'):
        s = re.sub(rf'(?<![{DEV}]){a}(ं?)(?![{DEV}])', a[:-1] + 'यी' + r'\1', s)
    # ! after an address (हे देवि!), where the word is a vocative and no list goes on after the comma (हे धर्म, काम और अर्थ …)
    def bang(m):
        rest = s[m.end():]; seg = re.split(r'[,!।;]', rest, maxsplit=1)[0]
        return m.group(0) if re.search(r' (और|तथा|आदि)( |$)', seg) else m.group(1) + '!'
    s = re.sub(rf'(हे [{DEV}]*[ाीेिो](?: [{DEV}]*[ाीेिो])?),', bang, s)
    s = re.sub(r'(कहा|बोले|पूछा)\s*[:—–-]+\s*', r'\1 — ', s)
    s = re.sub(r'(कहा|पूछा|बोले) — [‘\'"]([^‘’\'"]+)[’\'"]', r'\1 — \2', s)
    s = curly(s, '“”', '‘’')
    s = re.sub(r'\s+', ' ', s).replace(' ,', ',').replace(' ।', '।').strip()
    return s

def en(s):
    s = unpaired(s.strip())
    s = re.sub(r'\s*\[([^\]]+)\]', r' \1', s)
    s = re.sub(r'\bGoddess\b', 'Devī', s)
    s = re.sub(r'\s+', ' ', s).replace(' ,', ',').replace(' .', '.').replace('( ', '(')
    s = re.sub(r':\s*"([^"]+)"\s*$', r': \1', s)
    s = curly(s, '“”', '‘’')
    s = re.sub(r'^Om\b', 'Oṃ', s)
    s = re.sub(r'\b(realiz)', 'realis', s); s = re.sub(r'\btoward\b', 'towards', s); s = re.sub(r'\bhonor', 'honour', s)
    return s.strip()

NAMAH = {   # adhyāya 5: the noun of each या देवी … stanza (by its first mantra), Hindi and English
    14: ('विष्णुमाया नामसे कही जाती हैं', 'is called Viṣṇumāyā'), 17: ('चेतना कहलाती हैं', 'is called consciousness'),
    20: ('बुद्धिरूपसे स्थित हैं', 'abides in all beings as intelligence'), 23: ('निद्रारूपसे स्थित हैं', 'abides in all beings as sleep'),
    26: ('क्षुधा (भूख)-रूपसे स्थित हैं', 'abides in all beings as hunger'), 29: ('छायारूपसे स्थित हैं', 'abides in all beings as shadow'),
    32: ('शक्तिरूपसे स्थित हैं', 'abides in all beings as power'), 35: ('तृष्णारूपसे स्थित हैं', 'abides in all beings as thirst'),
    38: ('क्षमारूपसे स्थित हैं', 'abides in all beings as forbearance'), 41: ('जाति (जन्म)-रूपसे स्थित हैं', 'abides in all beings as birth'),
    44: ('लज्जारूपसे स्थित हैं', 'abides in all beings as modesty'), 47: ('शान्तिरूपसे स्थित हैं', 'abides in all beings as peace'),
    50: ('श्रद्धारूपसे स्थित हैं', 'abides in all beings as faith'), 53: ('कान्तिरूपसे स्थित हैं', 'abides in all beings as beauty'),
    56: ('लक्ष्मीरूपसे स्थित हैं', 'abides in all beings as fortune'), 59: ('वृत्ति (जीविका)-रूपसे स्थित हैं', 'abides in all beings as livelihood'),
    62: ('स्मृतिरूपसे स्थित हैं', 'abides in all beings as memory'), 65: ('दयारूपसे स्थित हैं', 'abides in all beings as compassion'),
    68: ('तुष्टि (सन्तोष)-रूपसे स्थित हैं', 'abides in all beings as contentment'), 71: ('मातृरूपसे स्थित हैं', 'abides in all beings as mother'),
    74: ('भ्रान्तिरूपसे स्थित हैं', 'abides in all beings as delusion'),
}

def namah(n):
    """The meanings of the three mantras of a या देवी … stanza whose first mantra is n."""
    if n == 78:
        h0, e0 = 'जो चैतन्यरूपसे इस सम्पूर्ण जगत्‌को व्याप्त करके स्थित हैं, उन्हें नमस्कार है।', 'Salutation to her who, as consciousness, pervades this whole world and abides in it.'
    else:
        h, e = NAMAH[n]
        h0 = f'जो देवी सब प्राणियोंमें {h}, उन्हें नमस्कार है।'
        e0 = f'Salutation to the Devī who {e}.' if e.startswith('abides') else f'Salutation to the Devī who in all beings {e}.'
    return [(h0, e0), ('उन्हें नमस्कार है।', 'Salutation to her.'), ('उन्हें बार-बार नमस्कार है।', 'Salutation to her, salutation again and again.')]

ORD_HI = 'प्रथम द्वितीय तृतीय चतुर्थ पञ्चम षष्ठ सप्तम अष्टम नवम दशम एकादश द्वादश त्रयोदश'.split()
ORD_HI = 'पहला दूसरा तीसरा चौथा पाँचवाँ छठा सातवाँ आठवाँ नौवाँ दसवाँ ग्यारहवाँ बारहवाँ तेरहवाँ'.split()
ORD_EN = 'first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth'.split()
CH = [   # each adhyāya's name in its colophon: Hindi, English
    ('मधुकैटभवध', 'the slaying of Madhu and Kaiṭabha'), ('महिषासुरसैन्यवध', 'the slaying of Mahiṣāsura’s army'),
    ('महिषासुरवध', 'the slaying of Mahiṣāsura'), ('शक्रादिस्तुति', 'the praise by Śakra and the gods'),
    ('देवीदूतसंवाद', 'the dialogue of the Devī and the messenger'), ('शुम्भनिशुम्भके सेनापति धूम्रलोचनका वध', 'the slaying of Dhūmralocana, general of Śumbha and Niśumbha'),
    ('चण्डमुण्डवध', 'the slaying of Caṇḍa and Muṇḍa'), ('रक्तबीजवध', 'the slaying of Raktabīja'),
    ('निशुम्भवध', 'the slaying of Niśumbha'), ('शुम्भवध', 'the slaying of Śumbha'),
    ('नारायणीस्तुति', 'the praise of Nārāyaṇī'), ('भगवतीका वचन', 'the words of the Bhagavatī'),
    ('सुरथ और वैश्यको वरदान', 'the boons to Suratha and the merchant')]
ITI = {   # the stotras' closing words: Hindi, English
    'argala': ('इस प्रकार श्रीमार्कण्डेयपुराणका अर्गलास्तोत्र पूरा हुआ।', 'Thus ends the Argalā Stotra of the Śrī Mārkaṇḍeya Purāṇa.'),
    'kilaka': ('इस प्रकार भगवतीका कीलकस्तोत्र पूरा हुआ।', 'Thus ends the Kīlaka Stotra of the Bhagavatī.'),
    'kavacha': ('इस प्रकार श्रीमार्कण्डेयपुराणमें हरि, हर और ब्रह्माका रचा हुआ देवीकवच पूरा हुआ।', 'Thus ends the Devī Kavaca of the Śrī Mārkaṇḍeya Purāṇa, composed by Hari, Hara and Brahmā.'),
    'aparadha': ('इस प्रकार अपराधक्षमापणस्तोत्र पूरा हुआ।', 'Thus ends the Aparādha-kṣamāpaṇa Stotra.'),
    'devi-sukta': ('इस प्रकार ऋग्वेदमें कहा हुआ देवीसूक्त पूरा हुआ।', 'Thus ends the Devī Sūkta, as the Ṛgveda gives it.'),
}

def main(src):
    J = json.load(open(src, encoding='utf-8'))
    F = json.load(open(os.path.join(HERE, 'meaning_fixes.json'), encoding='utf-8'))
    C = json.load(open(os.path.join(HERE, 'corrections.json'), encoding='utf-8'))
    T = textfile.read(os.path.join(HERE, '..', 'text.txt')); order = [x['id'] for x in T]
    BY = {}   # text item id → the copy's item
    for p, sec in enumerate(J['sections']):
        s = make_text.SEC[sec['id']]
        for it in sec['items']: BY.setdefault(s, []).append(it)
    made = make_text.items_of(J, C)
    src_of = {}
    for x, it in zip([m for m in made if not m['id'].endswith('.iti')], [it for sec in J['sections'] for it in sec['items'] for _ in range(3 if '-' in (it['number'] or '') else 1)]):
        src_of[x['id']] = it
    H, E, P = {}, {}, {}
    for x in made:
        r = x['id']; s, _, n = r.partition('.')
        if r.endswith('.iti'):
            if s.isdigit():
                c = int(s); hn, en_ = CH[c - 1]
                H[r] = f'स्वस्ति। श्रीमार्कण्डेयपुराणमें सावर्णिक मन्वन्तरकी कथाके अन्तर्गत देवीमाहात्म्यमें ‘{hn}’ नामक {ORD_HI[c - 1]} अध्याय पूरा हुआ।'
                E[r] = f'Svasti. Thus, in the Devī Māhātmya of the Śrī Mārkaṇḍeya Purāṇa, in the account of the Sāvarṇika manvantara, ends the {ORD_EN[c - 1]} adhyāya, named {en_}.'
            else: H[r], E[r] = ITI[s]
            continue
        it = src_of[r]
        m = SPK.match(' '.join(x['v']))
        if m and len(x['v']) == 1:
            b = BIJA.get(m.group(1) or '', ('', '')); h, e = SPEAKER[m.group(2)]
            H[r] = (b[0] + ' ' + h).strip(); E[r] = (b[1] + ' ' + e).strip(); continue
        if '-' in (it['number'] or ''):
            a = int(it['number'].split('-')[0]); H[r], E[r] = namah(a)[int(n) - a]; continue
        H[r] = hi(it['meaning']['hi'], ADDRESS(r)); E[r] = en(it['meaning']['en'])
    for sec in J['sections']:                       # Pargiter: each passage once, under the last mantra it covers
        for it in sec['items']:
            t = it['translations'].get('pargiter')
            if not t: continue
            a, _, b = t['mantras'].partition('-'); b = b or a
            last = b if '.' in b else a.split('.')[0] + '.' + b
            assert last in H, (it['ref'], last)
            P[last] = re.sub(r'\s+', ' ', t['text']).strip()
    for lang, D in (('hi', H), ('en', E)):
        for r, x in F.get(lang, {}).items():
            assert r in D, r; D[r] = x['text']
    assert set(H) == set(order), set(order) ^ set(H)
    H = {r: H[r] for r in order}; E = {r: E[r] for r in order}; P = {r: P[r] for r in order if r in P}
    M = os.path.join(HERE, '..', 'meanings')
    jsonio.dump_meanings(M + '/hi/scriptures.json', {
        'about': "Hindi meaning written for this library (hi-scriptures): the owner's drafts, written from each verse, brought to the style sheet (tools/meanings/style.md) by source/meanings.py; they stand until a reviewed meaning replaces them.",
        'order': 1, 'numbers': 'verse', 'm': H})
    jsonio.dump_meanings(M + '/en/scriptures.json', {
        'about': "English meaning written for this library (en-scriptures): the owner's drafts, written from each verse, brought to the style sheet (tools/meanings/style.md) by source/meanings.py; they stand until a reviewed meaning replaces them.",
        'order': 1, 'numbers': 'verse', 'm': E})
    jsonio.dump_meanings(M + '/en/pargiter.json', {
        'about': "F. E. Pargiter, The Mārkaṇḍeya Purāṇa (Bibliotheca Indica, 1904; public domain), cantos 81–93, from archive.org's scan, corrected and divided by mantra in the owner's copy; copied as given. A passage for several mantras sits under the last of them.",
        'title': {'hi': 'एफ़. ई. पार्जिटर — अंग्रेज़ी अर्थ', 'en': 'F. E. Pargiter — English meaning'}, 'order': 2, 'copied': True, 'm': P})
    print(len(H), len(E), len(P))

if __name__ == '__main__':
    main(sys.argv[1])
