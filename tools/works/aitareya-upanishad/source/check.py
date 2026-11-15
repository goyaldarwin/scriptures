"""Checks text.txt (the Aitareya Upaniṣad) against the Devanagari witnesses in source/witness/.

Every verse in a witness file (plain text: verses separated by blank lines, each ending in ॥ N॥; a block without a
number is the śānti mantra; a line "# 1.2" names the khaṇḍa the following verses belong to) must have the same letters
as text.txt. The text is prose, and the witnesses divide its words and lines differently (अधस्तात्त / अधस्तात् ता), so
spaces are not compared; neither are daṇḍas, bars, numbers, hyphens at line breaks and the printout's stray "/".
Spellings the library's standard makes one (docs/PLAYBOOK.md §3: a class nasal or ं, a word-final म् or ं, ꣳ) are
read alike (tools/text/standard.py → fold), and ॐ as ओं. The only differences allowed are those listed in
reconciliation.md (EXPECTED below, per witness).
Usage: python3 tools/works/aitareya-upanishad/source/check.py
"""
import difflib, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'text')); import standard
ITEMS = textfile.read(os.path.join(HERE, '..', 'text.txt'))
BY = {x['id']: x for x in ITEMS}

def letters(s):
    s = re.sub(r'-\s*\n\s*', '', s)                          # a word broken over two lines (आसीन्-/नान्यत्)
    s = s.replace('ॐ', 'ओं').replace('‍', '')
    words = re.sub(r'[।॥|,/0-9०-९\-—]', ' ', s).split()
    return ''.join(standard.fold(w) for w in words)

# The book ends a line or a phrase (at its daṇḍa) in pausa where the witnesses run the sandhi on: the same words.
PAUSA = {   # item id: [(witness, ours)]; each must be found in at least one witness
 '1.1.4': [('ग्निर्नासिके', 'ग्निः । नासिके'), ('वायुरक्षिणी', 'वायुः । अक्षिणी'), ('दिशस्त्वङ्', 'दिशः । त्वङ्')],
 '1.2.1': [('ब्रुवन्नायतनं', 'ब्रुवन् । आयतनं')],
 '1.2.4': [('प्राविशदादित्य', 'प्राविशद् आदित्य'), ('प्राविशन्नोषधि', 'प्राविशन् ओषधि'), ('प्राविशंश्चन्द्रमा', 'प्राविशन् चन्द्रमा'), ('प्राविशदापो', 'प्राविशद् आपो')],
 '1.3.11': [('विसृष्टमथ', 'विसृष्टम् अथ')],
 '1.3.12': [('द्वास्तदेतन्', 'द्वास्तद् एतन्'), ('आवसथास्त्रयः', 'आवसथाः त्रयः'), ('यमावसथोऽयमावसथोऽयमावसथ इति', 'यमावसथः अयमावसथः अयमावसथः इति')],
 '2.1.1': [('ङ्गेभ्यस्तेजः', 'ङ्गेभ्यः तेजः'), ('संभूतमात्मन्', 'संभूतम् । आत्मन्')],
 '2.1.3': [('भावयत्यात्मानमेव', 'भावयति आत्मानमेव')],
 '2.1.6': [('उत्क्रम्यामुष्मिन्', 'उत्क्रम्य अमुष्मिन्')],
 '3.1.3': [('ज्योतींषीत्येतानीमानि', 'ज्योतींषीति । एतानीमानि'), ('चेतराणि चाण्डजानि', 'चेतराणि च । अण्डजानि'), ('चोद्भिज्जानि चाश्वा', 'चोद्भिज्जानि च । अश्वा')],
 '3.1.4': [('त्क्रम्यामुष्मिन्', 'त्क्रम्य अमुष्मिन्'), ('कामानाप्त्वाऽमृतः', 'कामानाप्त्वा अमृतः')],
 'shanti.1': [('प्रतिष्ठितमाविरावीर्म', 'प्रतिष्ठितं आविरावीर्म'), ('प्रहासीरनेनाधीतेना', 'प्रहासीः । अनेनाधीतेना'), ('सन्दधाम्यृतं', 'संदधामि । ऋतं'),
              ('तद्वक्तारमवत्ववतु मामवतु वक्तारमवतु वक्तारम्', 'तद्वक्तारमवतु अवतु माम् अवतु वक्तारम् अवतु वक्तारम्')],
}
EXPECTED = {   # witness file: {item id: [(witness, ours)]}: the witness's own readings, each in reconciliation.md
 'sanskritdocuments-full.txt': {   # the book's edition: it shares most of the book's slips, corrected in settle.py → FIX
  'shanti.1': [('^वाङ् मे मनसि', 'ॐ वाङ् मे मनसि')],                # its opening śānti has no ॐ (its closing one has; ^: at the start)
  '1.1.2': [('अधस्तात्त आपः', 'अधस्तात्ता आपः')],
  '1.1.4': [('निरभिद्येतं नासिका', 'निरभिद्येतां नासिका'), ('निरभिद्येतमक्षी', 'निरभिद्येतामक्षी'), ('श्रोत्रद्दिश', 'श्रोत्राद्दिश')],
  '1.2.1': [('तमशनापिपासा', 'तमशनायापिपासा')],
  '1.2.4': [('प्राविशाद्दिशः', 'प्राविशद् दिशः')],
  '1.3.5': [('ग्रहीतु/न् स', 'ग्रहीतुं स'), ('हैवानमत्रप्स्यत्', 'हैवान्नमत्रप्स्यत्')],
  '1.3.6': [('यद्धैनच्छ्रोतेणा', 'यद्धैनच्छ्रोत्रेणा')],
  '1.3.9': [('यद्वित्सृज्य', 'यद्विसृज्य'), ('हैवानमत्रप्स्यत्', 'हैवान्नमत्रप्स्यत्')],
  '1.3.10': [('यद्वायुरनायुर्वा', 'यद्वायुरन्नायुर्वा')],
  '1.3.12': [('विदर्यैतया', 'विदार्यैतया'), ('नाऽन्दनम्', 'नान्दनम्')],
  '1.3.13': [('इदमदर्शनमिती', 'इदमदर्शमिती')],
  '2.1.1': [('त्मन्येवऽऽत्मानं', 'त्मन्येवाऽऽत्मानं')],
  '2.1.3': [('भावयत्येषं', 'भावयत्येषां')],
  '3.1.2': [('धृतिमतिर्मनीषा', 'धृतिर्मतिर्मनीषा')],
 },
 'upanishads-org.txt': {   # Sri Aurobindo's text (CWSA 18); NORM below
  '1.1.1': [('आसीत् । नान्यत्', 'आसीन्नान्यत्')],
  '1.1.4': [('क्षिभ्यां', 'क्षीभ्यां')],
  '3.1.4': [('प्रज्ञेनात्मना', 'प्राज्ञेनात्मना')],
 },
 'iitk.txt': {   # the IIT Kanpur Heritage reader's text, with its typing slips
  '1.1.1': [('आसीत्। नान्यत्', 'आसीन्नान्यत्')],
  '1.1.3': [('लोकाः लोक', 'लोका लोक'), ('पुरूषं', 'पुरुषं'), ('समुध्दृत्यामरूच्छयत्', 'समुद्धृत्यामूर्छयत्')],
  '1.1.4': [('त्वङनिरभिद्यत', 'त्वङ्निरभिद्यत')],
  '1.2.1': [('ता ता देवताः', 'ता एता देवताः'), ('महत्यर्णव प्रापतन्', 'महत्यर्णवे प्रापतन्'), ('ता नमब्रुवन्', 'ता एनमब्रुवन्'), ('यस्मिन् प्रतिष्ठिता', 'यस्मिन्प्रतिष्ठिता')],
  '1.2.2': [('गामानयता अब्रुवन्', 'गामानयत्ता अब्रुवन्')],
  '1.2.4': [('लोनानि', 'लोमानि')],
  '1.3.1': [('लोकश्च लोकपालाश्चन्न्नमेभ्यः', 'लोकाश्च लोकपालाश्चान्नमेभ्यः')],
  '1.3.3': [('पराङत्यजिघांसत्', 'पराङ्त्यजिघांसत्'), ('भिव्याहृय', 'भिव्याहृत्य')],
  '1.3.6': [('नाशक्नोच्छ्रत्रेण', 'नाशक्नोच्छ्रोत्रेण')],
  '1.3.7': [('तत्तवचा', 'तत्त्वचा')],
  '1.3.8': [('यद्धैनन्मनसाऽग्रहैष्यद्धयात्वा', 'यद्धैनन्मनसाऽग्रहैष्यद्ध्यात्वा')],
  '1.3.13': [('पुरूषं', 'पुरुषं'), ('ततममपश्यदिदमदर्शमिती', 'ततममपश्यत् । इदमदर्शमिती')],
  '2.1.1': [('त्मयेवाऽऽत्मानं', 'त्मन्येवाऽऽत्मानं')],
  '2.1.2': [('सास्यै', 'साऽस्यै')],
  '3.1.2': [('यदेतत् हृदयं', 'यदेतद्धृदयं')],
  '3.1.3': [('पुरूषा', 'पुरुषा')],
  '3.1.4': [('स तेन प्रज्ञेना', 'स एतेन प्राज्ञेना'), ('सर्वान कामाना', 'सर्वान् कामाना'), ('समभवत समभवत', 'समभवत् समभवत्')],
 },
}
NORM = {   # a witness's own writing convention, applied to it and to our text alike
 'upanishads-org.txt': lambda s: re.sub('ाऽ+', 'ा', s.replace('ओं', '')),   # no ॐ, and no avagraha after ā
}

def diff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(a[max(0, i1 - 4):i2 + 4], b[max(0, j1 - 4):j2 + 4]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']

USED = set()

def witness(path):
    name = os.path.basename(path); exp = EXPECTED.get(name, {}); norm = NORM.get(name, lambda s: s)
    khanda, bad, seen = None, 0, 0
    for blk in re.split(r'\n\s*\n', open(path, encoding='utf-8').read().strip()):
        blk = blk.strip()
        if blk.startswith('#'): khanda = blk[1:].strip(); continue
        m = re.search(r'॥\s*([०-९0-9]+)\s*॥\s*$', blk)
        vid = '%s.%d' % (khanda, int(m.group(1).translate(str.maketrans('०१२३४५६७८९', '0123456789')))) if m else 'shanti.1'
        if vid not in BY: print(name, 'has', vid, 'which is not in text.txt'); bad += 1; continue
        a, b = norm(letters(blk)), norm(letters('\n'.join(BY[vid]['v'])))
        for kind, pairs in (('E', exp.get(vid, [])), ('P', PAUSA.get(vid, []))):
            for w, o in pairs:
                start = w.startswith('^'); w, o = norm(letters(w.lstrip('^'))), norm(letters(o))
                if (a.startswith(w) if start else w in a):
                    USED.add((name if kind == 'E' else '*', vid, w)); a = o + a[len(w):] if start else a.replace(w, o)
        seen += 1
        if a != b:
            bad += 1
            print('≠', name, vid, ' '.join('[%s → %s]' % d for d in diff(a, b)))
    return seen, bad

bad = 0
for path in sorted(glob.glob(os.path.join(HERE, 'witness', '*.txt'))):
    seen, b = witness(path); bad += b
    print(os.path.basename(path) + ':', seen, 'verses compared,', b, 'differences')
for name, E in list(EXPECTED.items()) + [('*', PAUSA)]:
    norm = NORM.get(name, lambda s: s)
    for vid, pairs in E.items():
        for w, o in pairs:
            if (name, vid, norm(letters(w.lstrip('^')))) not in USED: print('listed but not found:', name, vid, w); bad += 1
sys.exit(1 if bad else 0)
