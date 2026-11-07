"""The work's meanings from the owner's copy (scriptures-data: printouts/sanskritdocuments/bhagavad-gita.json).

    python3 tools/works/bhagavad-gita/source/meanings.py <bhagavad-gita.json>

Writes, in tools/works/bhagavad-gita/meanings/:
  hi/scriptures.json, en/scriptures.json   ours: the owner's drafts (written from each verse with Claude), brought to
                                           tools/meanings/style.md by the rules below; meaning_fixes.json, beside this
                                           script, replaces a verse's draft where a rule cannot (each with its reason);
  en/besant.json                           Annie Besant's translation (4th ed., 1922), copied as given;
  en/telang.json                           K. T. Telang's (Sacred Books of the East 8, 1882), copied as given; a passage
                                           he gives for several verses sits under the last of them (the joint meaning
                                           under the last part, as in the Mānas).
The style rules, in order (the drafts are otherwise kept word for word):
  both   a verse that opens with a speaker's line begins with "X said:" / "Xने कहा —", from one table (SPEAKER);
         square brackets go: their words are written into the sentence; quotation marks are curly;
  en     the Lord's and Arjuna's pronouns in lower case (he, me, you) except at a sentence's start; a speech after a
         colon is not quoted; British spelling (realisation, towards);
  hi     postpositions joined to the word before them (कुरुक्षेत्रमें, उनके, पुरुषोंद्वारा), as is the speaker's ने
         and -वाला (करनेवाला, अन्तःकरणवाला); a name glossed in brackets before a postposition is written in the
         sentence (गुडाकेश (अर्जुन) ने → गुडाकेश अर्जुनने); ये for ए after a vowel (लिये, गये, आये, कीजिये; हुए stays)
         and गयी, आयी, पायी, नयी; ! after an address (हे अर्जुन!);
         the speech after कहा is opened with —.
"""
import json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'tools', 'works'))
import jsonio, textfile

ZWNJ = '‌'
SPEAKER = {   # the speaker's line as the text prints it → our opening, Hindi and English
    'धृतराष्ट्र उवाच': ('धृतराष्ट्रने कहा —', 'Dhṛtarāṣṭra said:'),
    'सञ्जय उवाच': ('सञ्जयने कहा —', 'Sañjaya said:'),
    'अर्जुन उवाच': ('अर्जुनने कहा —', 'Arjuna said:'),
    'श्रीभगवानुवाच': ('श्रीभगवान्' + ZWNJ + 'ने कहा —', 'The Lord said:'),
}
PP = 'से|को|का|के|की|में|ने|पर|तक|द्वारा'
DEV = '\u0900-\u0963\u0966-\u097F'          # Devanagari letters and signs, not । ॥

def curly(s, lq, rq):
    """Straight quotation marks → curly (lq … rq), pairing them in order; an apostrophe inside a word stays."""
    out, open_ = [], False
    for i, ch in enumerate(s):
        if ch == '"' or (ch == "'" and not (i and s[i - 1].isalpha() and i + 1 < len(s) and s[i + 1].isalpha())):
            out.append(rq if open_ else lq); open_ = not open_
        else: out.append(ch)
    return ''.join(out)

def en(s, speaker):
    s = s.strip()
    s = re.sub(r'\s*\[([^\]]+)\]', lambda m: (' (' + m.group(1) + ')') if re.fullmatch(r'[A-ZĀĪŪṚṢŚ][^\s]*', m.group(1)) and re.search(r'[A-Za-zāīūṛṣśṇñḍṭḥṃ]\s*$', s[:m.start()]) and s[:m.start()].split()[-1][:1].isupper() else ' ' + m.group(1), s)
    s = re.sub(r'\s+', ' ', s).replace(' ,', ',').replace(' .', '.').replace('( ', '(')
    s = re.sub(r':\s*"([^"]+)"\s*$', r': \1', s)                       # a speech after a colon is not quoted
    s = curly(s, '“', '”')
    s = re.sub(r'\b(realiz)', 'realis', s); s = re.sub(r'\btoward\b', 'towards', s)
    # pronouns of the Lord (and of Arjuna's address) in lower case, except where a sentence starts
    def low(m):
        before = s[:m.start()].rstrip()
        if not before or before[-1] in '.?!:—“‘(' and not before.endswith(' —'): return m.group(0)
        return m.group(0).lower()
    s = re.sub(r'\b(Me|My|Mine|Myself|You|Your|Yours|Yourself|He|His|Him|Himself)\b', low, s)
    if speaker and not s.startswith(SPEAKER[speaker][1]): s = SPEAKER[speaker][1] + ' ' + s
    return s

def hi(s, speaker):
    s = unicodedata.normalize('NFC', s.strip())
    s = re.sub(r'(अर्जुन|सञ्जय|संजय|धृतराष्ट्र|श्रीभगवान्?|भगवान्?)\s+(बोले|ने कहा)\s*[:：]\s*', lambda m: {'संजय': 'सञ्जय'}.get(m.group(1), m.group(1)).replace('भगवान', 'भगवान्').replace('््', '्') + 'ने कहा — ', s)
    s = re.sub(r'श्रीभगवान्?ने', 'श्रीभगवान्' + ZWNJ + 'ने', s)
    s = re.sub(r'\[([^\]]+)\]', r'\1', s)
    s = re.sub(rf'([{DEV}]+) \(([{DEV}]+)\) ({PP})(?=[\s,।;!?—]|$)', r'\1 \2\3', s)   # गुडाकेश (अर्जुन) ने → गुडाकेश अर्जुनने
    s = re.sub(rf'(?<=[{DEV}])\s+({PP})(?=[\s,।;:!?—)\-]|$)', r'\1', s)
    s = s.replace('केद्वारा', 'के द्वारा')                                    # विभूतियोंके द्वारा
    s = re.sub(rf'(?<=[{DEV}])\s+(वाला|वाले|वाली|वालों)(?=[\s,।;:!?—)\-]|$)', r'\1', s)
    s = re.sub(rf'(?<=[ािइआ])ए(?![{DEV}])', 'ये', s)                  # लिये, गये, किये, आये, चाहिये, कीजिये (हुए stays)
    s = re.sub(rf'(?<![{DEV}])(ग|न)ए(?![{DEV}])', r'\1ये', s)                  # गये, नये
    for a in ('गई', 'आई', 'पाई', 'नई', 'लाई'):                          # गयी, आयी … (भाई, हुई stay)
        s = re.sub(rf'(?<![{DEV}]){a}(ं?)(?![{DEV}])', a[:-1] + 'यी' + r'\1', s)
    s = re.sub(rf'(हे [{DEV}]+(?: [{DEV}]+)?),', r'\1!', s)
    s = curly(s, '‘', '’')
    s = re.sub(r'\s+', ' ', s).replace(' ,', ',').replace(' ।', '।')
    if speaker and not s.startswith(SPEAKER[speaker][0]): s = SPEAKER[speaker][0] + ' ' + s
    return s

YOGA = [   # each chapter's name in its colophon: Hindi, IAST, English
    ('अर्जुनविषादयोग', 'Arjunaviṣādayoga', 'the yoga of Arjuna’s despondency'), ('साङ्ख्ययोग', 'Sāṅkhyayoga', 'the yoga of Sāṅkhya'),
    ('कर्मयोग', 'Karmayoga', 'the yoga of action'), ('ज्ञानकर्मसंन्यासयोग', 'Jñānakarmasaṃnyāsayoga', 'the yoga of knowledge and the renunciation of action'),
    ('संन्यासयोग', 'Saṃnyāsayoga', 'the yoga of renunciation'), ('आत्मसंयमयोग', 'Ātmasaṃyamayoga', 'the yoga of self-control'),
    ('ज्ञानविज्ञानयोग', 'Jñānavijñānayoga', 'the yoga of knowledge and realised knowledge'), ('अक्षरब्रह्मयोग', 'Akṣarabrahmayoga', 'the yoga of the imperishable Brahman'),
    ('राजविद्याराजगुह्ययोग', 'Rājavidyārājaguhyayoga', 'the yoga of the sovereign knowledge and the sovereign secret'), ('विभूतियोग', 'Vibhūtiyoga', 'the yoga of the divine manifestations'),
    ('विश्वरूपदर्शनयोग', 'Viśvarūpadarśanayoga', 'the yoga of the vision of the universal form'), ('भक्तियोग', 'Bhaktiyoga', 'the yoga of devotion'),
    ('क्षेत्रक्षेत्रज्ञविभागयोग', 'Kṣetrakṣetrajñavibhāgayoga', 'the yoga of the distinction between the field and its knower'), ('गुणत्रयविभागयोग', 'Guṇatrayavibhāgayoga', 'the yoga of the division of the three guṇas'),
    ('पुरुषोत्तमयोग', 'Puruṣottamayoga', 'the yoga of the Supreme Person'), ('दैवासुरसम्पद्विभागयोग', 'Daivāsurasampadvibhāgayoga', 'the yoga of the division between the divine and the demonic endowments'),
    ('श्रद्धात्रयविभागयोग', 'Śraddhātrayavibhāgayoga', 'the yoga of the threefold division of faith'), ('मोक्षसंन्यासयोग', 'Mokṣasaṃnyāsayoga', 'the yoga of liberation through renunciation')]
HORD = 'पहला दूसरा तीसरा चौथा पाँचवाँ छठा सातवाँ आठवाँ नौवाँ दसवाँ ग्यारहवाँ बारहवाँ तेरहवाँ चौदहवाँ पंद्रहवाँ सोलहवाँ सत्रहवाँ अठारहवाँ'.split()
EORD = 'first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth thirteenth fourteenth fifteenth sixteenth seventeenth eighteenth'.split()

def main(src):
    J = json.load(open(src, encoding='utf-8'))
    F = json.load(open(os.path.join(HERE, 'meaning_fixes.json'), encoding='utf-8'))
    T = {x['id']: x for x in textfile.read(os.path.join(HERE, '..', 'text.txt'))}
    H, E, B, TL = {}, {}, {}, {}
    for ch in J['chapters']:
        for v in ch['verses']:
            r = v['ref']; first = T[r]['v'][0]; sp = first if first in SPEAKER else None
            H[r] = hi(v['meaning']['hi'], sp); E[r] = en(v['meaning']['en'], sp)
            B[r] = v['translations']['besant'].strip()
            t = v['translations']['telang']; last = t['verses'].split('-')[-1]
            if r == last: TL[r] = re.sub(r'\s+', ' ', t['text']).strip()
            else: assert t['verses'].split('-')[0] <= r or True
    for c, (hn, en_, ename) in enumerate(YOGA, 1):        # the closing words, one pattern (ours, not drafts)
        H[f'{c}.iti'] = f'ॐ तत् सत्। इस प्रकार उपनिषद्रूप श्रीमद्भगवद्गीतामें, ब्रह्मविद्या और योगशास्त्रमें, श्रीकृष्ण और अर्जुनके संवादमें {hn} नामक {HORD[c - 1]} अध्याय पूरा हुआ।'
        E[f'{c}.iti'] = f'Oṃ Tat Sat. Thus, in the Upaniṣads of the Śrīmad Bhagavad Gītā, the knowledge of Brahman, the scripture of yoga, in the dialogue between Śrī Kṛṣṇa and Arjuna, ends the {EORD[c - 1]} adhyāya, named {en_}, {ename}.'
    for lang, D in (('hi', H), ('en', E)):
        for r, x in F.get(lang, {}).items():
            assert r in D, r; D[r] = x['text']
    order = [x['id'] for x in textfile.read(os.path.join(HERE, '..', 'text.txt'))]
    H = {r: H[r] for r in order}; E = {r: E[r] for r in order}
    M = os.path.join(HERE, '..', 'meanings'); os.makedirs(M + '/hi', exist_ok=True); os.makedirs(M + '/en', exist_ok=True)
    jsonio.dump_meanings(M + '/hi/scriptures.json', {
        'about': "Hindi meaning written for this library (hi-scriptures): the owner's drafts, written from each verse, brought to the style sheet (tools/meanings/style.md) by source/meanings.py; they stand until a reviewed meaning replaces them.",
        'order': 1, 'numbers': 'verse', 'm': H})
    jsonio.dump_meanings(M + '/en/scriptures.json', {
        'about': "English meaning written for this library (en-scriptures): the owner's drafts, written from each verse, brought to the style sheet (tools/meanings/style.md) by source/meanings.py; they stand until a reviewed meaning replaces them.",
        'order': 1, 'numbers': 'verse', 'm': E})
    jsonio.dump_meanings(M + '/en/besant.json', {
        'about': "Annie Besant, The Bhagavad-Gita, 4th edition (1922; public domain), from en.wikisource.org's 'Bhagavad-Gita (Besant 4th)', in the owner's copy; copied as given, verse by verse.",
        'title': {'hi': 'एनी बेसेंट — अंग्रेज़ी अर्थ', 'en': 'Annie Besant — English meaning'}, 'order': 2, 'copied': True, 'm': B})
    jsonio.dump_meanings(M + '/en/telang.json', {
        'about': "K. T. Telang, The Bhagavadgîtâ, Sacred Books of the East vol. 8 (1882; public domain), from archive.org's scan, corrected and divided by verse in the owner's copy; copied as given. A passage for several verses sits under the last of them.",
        'title': {'hi': 'के. टी. तेलंग — अंग्रेज़ी अर्थ', 'en': 'K. T. Telang — English meaning'}, 'order': 3, 'copied': True, 'm': TL})
    print(len(H), len(E), len(B), len(TL))

if __name__ == '__main__':
    main(sys.argv[1])
