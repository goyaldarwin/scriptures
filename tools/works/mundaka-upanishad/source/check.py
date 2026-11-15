"""Checks text.txt (the Muṇḍaka Upaniṣad) against the Devanagari witnesses in source/witness/ (made by witnesses.py).

Every block in a witness file (plain text: blocks separated by blank lines; a mantra ends in ॥ N॥; a block without a
number is the śānti mantra before the first khaṇḍa and the khaṇḍa's closing words (इति …) after it; a line "# 1.2"
names the khaṇḍa the following blocks belong to) must have the same letters as text.txt. The witnesses divide words
and lines differently (विद्वान् नामरूपाद् / विद्वान्नामरूपाद्, परम ऋषिभ्यो / परमऋषिभ्यो), so spaces are not compared;
neither are daṇḍas, bars, numbers, commas, dashes and hyphens at line breaks. Spellings the library's standard makes
one (docs/PLAYBOOK.md §3: a class nasal or ं, a word-final म् or ं, ꣳ or ँ) are read alike (tools/text/standard.py →
fold), and ॐ as ओं. The only differences allowed are those listed in reconciliation.md (EXPECTED below, per witness).
Usage: python3 tools/works/mundaka-upanishad/source/check.py
"""
import difflib, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'text')); import standard
ITEMS = textfile.read(os.path.join(HERE, '..', 'text.txt'))
BY = {x['id']: x for x in ITEMS}

def letters(s):
    s = re.sub(r'-\s*\n\s*', '', s)                          # a word broken over two lines (अवर्ण-/मचक्षुः)
    s = s.replace('ॐ', 'ओं').replace('‍', '')
    words = re.sub(r'[।॥|,/0-9०-९\-—–]', ' ', s).split()
    return standard.fold(''.join(re.sub('म्$', 'ं', w) for w in words))   # across words: यस्मिन् द्यौः · यस्मिंद्यौः

EXPECTED = {   # witness file: {item id: [(witness, ours)]}: the witness's own readings, each in reconciliation.md
 'iitk.txt': {   # the IIT Kanpur Heritage reader's text, with its typing slips (NORM below for the two that recur)
  '1.1.2': [('ब्रह्माथर्वा', 'ब्रह्माऽथर्वा'), ('पुरोवाचाङ्गिर ब्रह्म', 'पुरोवाचाङ्गिरे ब्रह्म'), ('सत्यवहाय', 'सत्यवाहाय'), ('भारद्वाजोङ्गिरसे', 'भारद्वाजोऽङ्गिरसे')],
  '1.1.3': [('महाशालोङ्गिरसं', 'महाशालोऽङ्गिरसं')],
  '1.1.5': [('समावेदो', 'सामवेदो'), ('निरूक्तं', 'निरुक्तं')],
  '1.1.7': [('तथाक्षरात्सं', 'तथाऽक्षरात्सं')],
  '1.2.4': [('विश्वरूची', 'विश्वरुची')],
  '1.2.9': [('तेनाऽऽतुराः', 'तेनातुराः'), ('लोकाश्चयवन्ते', 'लोकाश्च्यवन्ते')],
  '1.2.11': [('भैक्षचर्यां', 'भैक्ष्यचर्यां'), ('यत्रामृताः', 'यत्रामृतः')],
  '1.2.12': [('लोकांकर्मचितांब्राह्मणो', 'लोकान्कर्मचितान्ब्राह्मणो'), ('गुरूमेवा', 'गुरुमेवा')],
  '2.1.1': [('तथाक्षराद्विविधाः', 'तथाऽक्षराद्विविधाः')],
  '2.1.2': [('अप्रणो', 'अप्राणो')],
  '2.1.3': [('वायुज्र्योति', 'वायुर्ज्योति')],
  '2.1.5': [('बह्वी प्रजाः', 'बह्वीः प्रजाः')],
  '2.1.6': [('यजूँषि', 'यजूंषि'), ('सर्व क्रतवो', 'सर्वे क्रतवो')],
  '2.1.7': [('पश्चक्षद्धा', 'पश्च श्रद्धा')],
  '2.1.10': [('पुरुष वेदं', 'पुरुष एवेदं'), ('परामृतम् तद्यो', 'परामृतम् एतद्यो')],
  '2.2.2': [('यदणुभ्योणु', 'यदणुभ्योऽणु')],
  '2.2.6': [('नाडयः', 'नाड्यः')],
  '2.2.7': [('संनिधाय', 'सन्निधाय')],
  '3.1.3': [('विधूय विरञ्जनः', 'विधूय निरञ्जनः'), ('विद्वांपुण्य', 'विद्वान्पुण्य')],
  '3.1.4': [('विद्वांभवते', 'विद्वान्भवते')],
  '3.1.6': [('येनाक्रमन्त्यृषयो', 'येनाऽऽक्रमन्त्यृषयो')],
  '3.2.1': [('ये ह्याकामास्ते', 'ये ह्यकामास्ते')],
  '3.2.7': [('सर्वं एकीभवन्ति', 'सर्वे एकीभवन्ति')],
  '3.2.8': [('विद्वान्नमरूपा', 'विद्वान्नामरूपा')],
  '3.2.10': [('एकर्षि श्रद्धयन्तः', 'एकर्षिं श्रद्धयन्तः')],
  '3.2.11': [('व्रतोधीते', 'व्रतोऽधीते')],
 },
 'upanishads-org.txt': {   # Sri Aurobindo's text (CWSA 18)
  '1.1.2': [('ब्रह्माऽथर्वा तं', 'ब्रह्माऽथर्वा तां')],
  '1.2.2': [('प्रतिपादयेच्छ्रद्धया हुतम्', 'प्रतिपादयेत्')],
  '2.2.7': [('संनिधाय', 'सन्निधाय')],
  '3.1.6': [('येनाक्रमन्त्यृषयो', 'येनाऽऽक्रमन्त्यृषयो')],
 },
 'wikisource.txt': {   # the sanskritdocuments.org text (the page names it), as is shlokam.org's: it shares the base's slips
  'shanti.1': [('श्रुणुयाम', 'शृणुयाम'), ('तुष्टुवाँसस्', 'तुष्टुवांसस्')],
  '1.1.2': [('ब्रह्माऽथर्वा तं', 'ब्रह्माऽथर्वा तां')],
  '1.1.9': [('ज्ञानमयं तापः', 'ज्ञानमयं तपः'), ('च जायाते', 'च जायते')],
  '1.2.13': [('तत्वतो', 'तत्त्वतो')],
  '2.1.3': [('जायते प्रणो', 'जायते प्राणो')],
  '2.1.4': [('अग्नीर्मूर्धा', 'अग्निर्मूर्धा'), ('प्रणो हृदयं', 'प्राणो हृदयं')],
  '2.1.7': [('श्रद्ध सत्यं', 'श्रद्धा सत्यं')],
  '2.2.4': [('शारो ह्यात्मा', 'शरो ह्यात्मा')],
  '2.2.9': [('ज्योतिषं ज्योतिस्', 'ज्योतिषां ज्योतिस्')],
  '3.1.4': [('प्रणो ह्येष', 'प्राणो ह्येष')],
  '3.1.7': [('पश्यन्त्विहैव', 'पश्यत्स्विहैव')],
  '3.1.8': [('कर्मण वा', 'कर्मणा वा')],
  '3.1.10': [('ह्यर्चयेत् भूतिकामः', 'ह्यर्चयेद्भूतिकामः')],
 },
 'vedicheritage.txt': {   # the sanskritdocuments.org text again (the same headings and colophon), with slips of its own
  'shanti.1': [('श्रुणुयाम देवाः', 'शृणुयाम देवा')],
  '1.1.9': [('च जायाते', 'च जायते')],
  '1.2.9': [('वर्तमानाः वयं', 'वर्तमाना वयं')],
  '2.1.4': [('अग्नीर्मूर्धा', 'अग्निर्मूर्धा')],
  '2.1.8': [('सप्तेमे', 'सप्त इमे')],
  '2.1.9': [('सर्वे अस्मात्', 'सर्वेऽस्मात्')],
  '2.2.2': [('यस्मिंल्लोका', 'यस्मिँल्लोका')],
  '2.2.3': [('सन्दधीत', 'संधयीत')],
  '2.2.7': [('व्योमन्यात्मा', 'व्योम्न्यात्मा')],
  '3.1.1': [('स्वाद्वत्ति अनश्नन्नन्योऽभिचाकशीति', 'स्वाद्वत्त्यनश्नन्नन्यो अभिचाकशीति')],
  '3.1.7': [('पश्यन्त्विहैव', 'पश्यत्स्विहैव')],
  '3.1.10': [('ह्यर्चयेत्भूतिकामः', 'ह्यर्चयेद्भूतिकामः')],
  '3.2.5': [('धीराः युक्तात्मानः', 'धीरा युक्तात्मानः')],
  '3.2.7': [('सर्व एकीभवन्ति', 'सर्वे एकीभवन्ति')],
 },
}
NORM = {   # a witness's recurring typing slip, corrected before the comparison
 'iitk.txt': lambda s: s.replace('ध्द', 'द्ध').replace('पुरूष', 'पुरुष'),   # ध्द for द्ध, रू for रु in पुरुष
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
        if m: vid = '%s.%d' % (khanda, int(m.group(1).translate(str.maketrans('०१२३४५६७८९', '0123456789'))))
        else: vid = 'shanti.1' if khanda is None else khanda + '.iti'
        if vid not in BY: print('≠', name, 'has', vid, 'which is not in text.txt'); bad += 1; continue
        a, b = letters(norm(blk)), letters('\n'.join(BY[vid]['v']))
        for w, o in exp.get(vid, []):
            w, o = letters(norm(w)), letters(o)
            if w in a: USED.add((name, vid, w)); a = a.replace(w, o)
        seen += 1
        if a != b:
            bad += 1
            print('≠', name, vid, ' '.join('[%s → %s]' % d for d in diff(a, b)))
    return seen, bad

bad = 0
for path in sorted(glob.glob(os.path.join(HERE, 'witness', '*.txt'))):
    seen, b = witness(path); bad += b
    print(os.path.basename(path) + ':', seen, 'blocks compared,', b, 'differences')
for name, E in EXPECTED.items():
    for vid, pairs in E.items():
        for w, o in pairs:
            if (name, vid, letters(NORM.get(name, lambda s: s)(w))) not in USED: print('listed but not found:', name, vid, w); bad += 1
sys.exit(1 if bad else 0)
