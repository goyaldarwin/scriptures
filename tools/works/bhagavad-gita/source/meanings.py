"""The work's meanings from the owner's copy (scriptures-data: printouts/sanskritdocuments/bhagavad-gita.json).

    python3 tools/works/bhagavad-gita/source/meanings.py <bhagavad-gita.json>

Writes, in tools/works/bhagavad-gita/meanings/, the copied translations:
  en/besant.json                           Annie Besant's translation (4th ed., 1922), copied as given;
  en/telang.json                           K. T. Telang's (Sacred Books of the East 8, 1882), copied as given; a passage
                                           he gives for several verses sits under the last of them (the joint meaning
                                           under the last part, as in the Mānas).
Our own meanings (hi/scriptures.json, en/scriptures.json) are reviewed meanings kept in their files
(tools/meanings/apply_batches.py, docs/HOW-TO.md); this script no longer writes them. Its style rules below are
still used by words.py for the word meanings' Hindi.
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
import jsonio

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
    s = re.sub(rf'(?<=[{DEV}])\s+(?=वाल(?:ा|े|ी|ों))', '', s)                 # करनेवाला, करनेवालोंका
    s = re.sub(rf'(?<=[ािइआ])ए(?![{DEV}])', 'ये', s)                  # लिये, गये, किये, आये, चाहिये, कीजिये (हुए stays)
    s = re.sub(rf'(?<![{DEV}])(ग|न)ए(?![{DEV}])', r'\1ये', s)                  # गये, नये
    for a in ('गई', 'आई', 'पाई', 'नई', 'लाई'):                          # गयी, आयी … (भाई, हुई stay)
        s = re.sub(rf'(?<![{DEV}]){a}(ं?)(?![{DEV}])', a[:-1] + 'यी' + r'\1', s)
    s = re.sub(rf'(हे [{DEV}]+(?: [{DEV}]+)?),', r'\1!', s)
    s = curly(s, '‘', '’')
    s = re.sub(r'\s+', ' ', s).replace(' ,', ',').replace(' ।', '।')
    if speaker and not s.startswith(SPEAKER[speaker][0]): s = SPEAKER[speaker][0] + ' ' + s
    return s


def main(src):
    J = json.load(open(src, encoding='utf-8'))
    B, TL = {}, {}
    for ch in J['chapters']:
        for v in ch['verses']:
            r = v['ref']
            B[r] = v['translations']['besant'].strip()
            t = v['translations']['telang']; last = t['verses'].split('-')[-1]
            if r == last: TL[r] = re.sub(r'\s+', ' ', t['text']).strip()
            else: assert t['verses'].split('-')[0] <= r or True
    M = os.path.join(HERE, '..', 'meanings'); os.makedirs(M + '/en', exist_ok=True)
    jsonio.dump_meanings(M + '/en/besant.json', {
        'about': "Annie Besant, The Bhagavad-Gita, 4th edition (1922; public domain), from en.wikisource.org's 'Bhagavad-Gita (Besant 4th)', in the owner's copy; copied as given, verse by verse.",
        'title': {'hi': 'एनी बेसेंट — अंग्रेज़ी अर्थ', 'en': 'Annie Besant — English meaning'}, 'order': 2, 'copied': True, 'm': B})
    jsonio.dump_meanings(M + '/en/telang.json', {
        'about': "K. T. Telang, The Bhagavadgîtâ, Sacred Books of the East vol. 8 (1882; public domain), from archive.org's scan, corrected and divided by verse in the owner's copy; copied as given. A passage for several verses sits under the last of them.",
        'title': {'hi': 'के. टी. तेलंग — अंग्रेज़ी अर्थ', 'en': 'K. T. Telang — English meaning'}, 'order': 3, 'copied': True, 'm': TL})
    print(len(B), len(TL))

if __name__ == '__main__':
    main(sys.argv[1])
