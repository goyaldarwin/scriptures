"""Taittirīya Upaniṣad: source/taittiriya_raw.json (the shlokam.org page's blocks) → ../text.txt (the settled text: one
item per paragraph of an anuvāka, as the page and the tradition number them, with the vallīs' śānti pāṭhas and closing
words, the parts, the sections and our topic headings).

The Devanagari is the page's own. Its transliteration is a second witness: every line is compared with it (`WITNESS`
names the lines where the two write the sāman's pluta differently, the only differences). Then the corrections below
(`FIX`), each recorded in ../reconciliation.md, and the page's own headings (an editor's titles, not the Upaniṣad's
words) are left out. The transliteration of the library is made by the exporter (tools/text/standard.py).
Run: python3 settle.py   (then python3 tools/works/export.py taittiriya-upanishad)
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..')); import textfile
from taittiriya_text import tr2deva, key

# ---- the page's first line is an editor's heading in these blocks (not recited); our topics replace them ----
HEADING = {'1.1.1': 'प्रथमा शीक्षावल्ली', '1.2.1': 'शिक्षाशास्त्रार्थसङ्ग्रहः', '1.3.1': 'संहितोपासनम्',
           '1.4.1': 'मेधादिसिद्ध्यर्था आवहन्तीहोममन्त्राः', '1.5.1': 'व्याहृत्युपासनम्',
           '1.6.1': 'मनोमयत्वादिगुणकब्रह्मोपासनया स्वाराज्यसिद्धिः', '1.7.1': 'पृथिव्याद्युपाधिकपञ्चब्रह्मोपासनम्',
           '1.8.1': 'प्रणवोपासनम्', '1.9.1': 'स्वाध्यायप्रशंसा', '1.10.1': 'ब्रह्मज्ञ्यानप्रकाशकमन्त्रः', '1.11.1': 'शिष्यानुशासनम्',
           '1.12.1': 'उत्तरशान्तिपाठः', '2.0.1': 'द्वितीया ब्रह्मानन्दवल्ली', '2.0.2': 'उपनिषत्सारसङ्ग्रहः',
           '2.2.1': 'पञ्चकोशोविवरणम्', '2.7.1': 'अभयप्रतिष्ठा', '2.8.1': 'ब्रह्मानन्दमीमांसा', '3.0.1': 'तृतीया भृगुवल्ली',
           '3.2.1': 'पञ्चकोशान्तःस्थितब्रह्मनिरूपणम्', '3.7.1': 'अन्नब्रह्मोपासनम्', '3.10.1': 'सदाचारप्रदर्शनम् । ब्रह्मानन्दानुभवः'}

# ---- the lines where the page's transliteration writes the pluta (३) as a long vowel (hāāāvu, ṛtāāāsya) or ꣳ as ṃ:
#      a convention of the two scripts, not a difference of words; every other line must agree letter for letter ----
WITNESS = {('1.3.1', 4), ('3.10.5', 7), ('3.10.6', 1), ('3.10.6', 2), ('3.10.6', 3), ('3.10.6', 4), ('3.10.6', 5),
           ('3.10.6', 6), ('3.10.6', 7)}

# ---- corrections: (block, wrong, right); each must occur exactly once in that block (../reconciliation.md) ----
FIX = [
    ('1.3.1', 'सन्धिः वायुः', 'सन्धिः । वायुः'),                 # the daṇḍa the page's transliteration has (sandhiḥ. vāyuḥ)
    ('1.3.1', 'उपनिषदम् व्याख्यास्यामः', 'उपनिषदं व्याख्यास्यामः'),   # a word-final m before a consonant is ं (PLAYBOOK §3)
    ('1.3.2', 'अथाधिजौतिषम्', 'अथाधिज्यौतिषम्'),               # as 1.3.1 and इत्यधिज्यौतिषम् in the same paragraph
    ('1.3.4', 'इतीमामहासꣳहिताः', 'इतीमा महासꣳहिताः'),         # two words, as the next line's एता महासꣳहिता
    ('1.3.4', 'वे`द', 'वेद'),                                    # a stray accent mark
    ('1.5.1', 'सर्वेलोक महीयन्ते', 'सर्वे लोका महीयन्ते'),        # as सर्वे वेदा (1.5.2): the plural लोकाः
    ('1.5.2', 'सर्वेवेदा', 'सर्वे वेदा'),
    ('1.5.3', 'सर्वे प्राण महीयन्ते', 'सर्वे प्राणा महीयन्ते'),      # the plural प्राणाः, as सर्वे वेदा
    ('1.5.3', 'चतस्रश्चतुर्ध ', 'चतस्रश्चतुर्धा '),                # the adverb चतुर्धा, "in four ways"
    ('1.5.3', 'सर्वेऽस्मैदेवा', 'सर्वेऽस्मै देवा'),
    ('1.6.1', 'एषोऽन्तहृदय', 'एषोऽन्तर्हृदय'),                    # अन्तः + हृदय
    ('1.6.2', 'योग्योपास्व', 'योग्योपास्स्व'),                      # उप + आस् + स्व; every independent witness
    ('1.7.1', 'चर्ममाꣳस स्नावा', 'चर्ममाꣳसꣳ स्नावा'),              # माꣳसम्, a nominative of the list; every witness
    ('1.7.1', 'पाङ्क्तग् स्पृणोतीति', 'पाङ्क्तꣳ स्पृणोतीति'),        # the page's ꣳ (gͫ) lost its sign
    ('1.8.1', 'ॐꣳशोमिति', 'ओꣳशोमिति'),                         # ॐ already holds the nasal
    ('1.9.1', 'राथी तरः', 'राथीतरः'),                             # one name, Rāthītara
    ('1.10.1', 'सुमेध अमृतोक्षितः', 'सुमेधा अमृतोक्षितः'),          # सुमेधाः, the predicate of अस्मि
    ('1.11.1', 'चार्योन्तेवासिन', 'चार्योऽन्तेवासिन'),   # आचार्यः + अन्तेवासिनम्
    ('1.11.2', 'त्वयोपास्यानि ।नो', 'त्वयोपास्यानि । नो'),
    ('1.11.4', 'इत्येकादशऽनुवाकः', 'इत्येकादशोऽनुवाकः'),           # एकादशः + अनुवाकः
    ('2.1.1', 'ओषधीभ्योन्नम्', 'ओषधीभ्योऽन्नम्'),                   # ओषधीभ्यः + अन्नम्
    ('2.6.1', 'कश्चन गच्छती', 'कश्चन गच्छती३ ।'),                 # the question's pluta, as समश्नुता३ उ
    ('2.6.1', 'बहुस्यां', 'बहु स्यां'),
    ('2.7.1', 'तदात्मान स्वयमकुरुत', 'तदात्मानꣳ स्वयमकुरुत'),       # आत्मानम्
    ('2.7.1', 'तत्वेव भयं', 'तत्त्वेव भयं'),                       # तत् + तु + एव
    ('2.8.2', 'एकः पितृणां', 'एकः पितॄणां'),                      # the genitive plural of पितृ (GRETIL, upanishads.org.in)
    ('2.8.2', 'शतं पितृणां', 'शतं पितॄणां'),
    ('2.9.1', 'विद्वानेते आत्मान स्पृणुते', 'विद्वानेते आत्मानꣳ स्पृणुते'),
    ('2.9.1', 'एते आत्मान स्पृणुते ।', 'एते आत्मानꣳ स्पृणुते ।'),
    ('3.2.1', 'भुतानि', 'भूतानि'),
    ('3.6.1', 'आनन्दाध्येव', 'आनन्दाद्ध्येव'),                     # as अन्नाद्ध्येव, प्राणाद्ध्येव, विज्ञानाद्ध्येव
    ('3.10.1', 'एदद्वा', 'एतद्वा'),                              # as एतद्वै in the two lines before
    ('3.10.1', 'अन्न राध्यते', 'अन्नꣳ राध्यते'),                   # as अन्नꣳराध्यते in the lines before
    ('3.10.5', 'इमाँल्लोकन्कामान्नी', 'इमाँल्लोकान्कामान्नी'),        # लोकान्, accusative plural
    ('3.10.5', 'हा ३ वु हा ३ वु हा ३ वु', 'हा३वु हा३वु हा३वु'),     # the pluta joined to its syllable, as ऋता३स्य
    ('3.10.6', 'दोऽ३अहमन्नादः', 'दोऽ३हमन्नादः'),       # written as the repetition before it
    ('3.10.6', 'मा३अऽवाः', 'मा३ऽवाः'),                           # the elided अ is the avagraha
]
# the śānti pāṭha's words as the page writes them after the Upaniṣad's last paragraph (तेजस्वि नावधीतमस्तु: तेजस्वि अधीतम्, नौ)
SAHA = 'तेजस्विनावधीतमस्तु'

def blocks():
    B = json.load(open(os.path.join(HERE, 'taittiriya_raw.json'), encoding='utf-8'))
    # the second witness: the page's own transliteration, line by line
    differ = {(b['ref'], i) for b in B for i, (v, t) in enumerate(zip(b['v'], b['t'])) if key(v) != key(tr2deva(t))}
    assert all(len(b['v']) == len(b['t']) for b in B)
    assert differ == WITNESS, sorted(differ ^ WITNESS)
    L = {}
    for b in B:
        v = list(b['v'])
        if b['ref'] in HEADING: assert v[0] == HEADING[b['ref']], (b['ref'], v[0]); v = v[1:]
        L[b['ref']] = '\n'.join(v)
    for ref, a, b_ in FIX:
        assert L[ref].count(a) == 1, (ref, a)
        L[ref] = L[ref].replace(a, b_)
    for ref in L: L[ref] = L[ref].replace(SAHA, 'तेजस्वि नावधीतमस्तु')
    return {ref: house(t) for ref, t in L.items()}

def house(text):
    """The page's daṇḍas as the library writes them (॥१॥), and the words that close an anuvāka on a line of their own."""
    out = []
    for l in text.split('\n'):
        l = re.sub(r'\s*॥\s*([०-९]+)\s*॥', r' ॥\1॥', l)
        l = re.sub(r'(॥[०-९]+॥)\s*(इत.*?ऽनुवाकः ॥)', r'\1\n\2', l)
        l = re.sub(r'[ \t]+', ' ', l.replace('।', ' । ')).replace(' । ॥', ' ॥')
        out += [x.strip() for x in l.split('\n')]
    return [x for x in out if x]

ORD = ['प्रथम', 'द्वितीय', 'तृतीय', 'चतुर्थ', 'पञ्चम', 'षष्ठ', 'सप्तम', 'अष्टम', 'नवम', 'दशम', 'एकादश', 'द्वादश']
# one topic per anuvāka, in our words (the page's headings are not copied)
THEME = {
    1: [('शान्तिपाठ: देवताओंसे कल्याणकी प्रार्थना', 'Shanti paath: a prayer to the gods for welfare'),
        ('उच्चारणकी शिक्षा', 'The science of pronunciation'),
        ('पाँच महासंहिताएँ', 'The five great joinings'),
        ('मेधा और श्रीके लिए आचार्यकी प्रार्थना', 'The teacher’s prayer for wisdom and plenty'),
        ('चार व्याहृतियाँ', 'The four vyahritis'),
        ('हृदयमें ब्रह्म और स्वराज्य', 'Brahman in the heart, and self-rule'),
        ('सब कुछ पाँच-पाँचका', 'All things in fives'),
        ('ॐकी उपासना', 'Meditation on Om'),
        ('स्वाध्याय और प्रवचनके साथ', 'With study and teaching'),
        ('त्रिशङ्कुका वचन', 'The words of Trishanku'),
        ('विदा होते शिष्यको उपदेश', 'The teacher’s parting counsel'),
        ('उत्तर शान्तिपाठ: प्रार्थना पूरी हुई', 'Closing shanti paath: the prayer fulfilled')],
    2: [('ब्रह्म सत्य, ज्ञान, अनन्त; सृष्टिक्रम और अन्नमय आत्मा', 'Brahman: truth, knowledge, the infinite; creation and the self of food'),
        ('अन्नकी महिमा; प्राणमय आत्मा', 'Food, and the self of breath'),
        ('प्राणकी महिमा; मनोमय आत्मा', 'Breath, and the self of mind'),
        ('जहाँसे मन लौट आता है; विज्ञानमय आत्मा', 'Where the mind turns back; the self of understanding'),
        ('विज्ञानकी महिमा; आनन्दमय आत्मा', 'Understanding, and the self of bliss'),
        ('सत् और असत्; सृष्टि रचकर उसीमें प्रवेश', 'Being and non-being; creating and entering it'),
        ('रसो वै सः; अभय', 'He is the essence; fearlessness'),
        ('आनन्दकी मीमांसा', 'The measure of bliss'),
        ('जहाँसे वाणी लौट आती है', 'Where words turn back')],
    3: [('भृगु पिता वरुणके पास', 'Bhrigu goes to his father Varuna'),
        ('अन्न ब्रह्म है', 'Food is Brahman'),
        ('प्राण ब्रह्म है', 'Breath is Brahman'),
        ('मन ब्रह्म है', 'Mind is Brahman'),
        ('विज्ञान ब्रह्म है', 'Understanding is Brahman'),
        ('आनन्द ब्रह्म है', 'Bliss is Brahman'),
        ('अन्नकी निन्दा न करे', 'Do not belittle food'),
        ('अन्नका त्याग न करे', 'Do not reject food'),
        ('अन्न बहुत उपजाए', 'Make food plentiful'),
        ('अतिथि-सत्कार, उपासना और मुक्तका साम-गान', 'Hospitality, meditations, and the song of the free')],
}

def item(id_, p, s, y, n, v):
    return {'id': id_, 'p': p, 's': s, 'y': y, 'n': n, 'v': v}

def build():
    L = blocks(); I = []; topics = []
    refs = list(L)
    def anuvakas(v):
        """[(anuvāka, [paragraph refs])] of vallī v, in the page's order (2.0.x is the vallī's opening)."""
        A = {}
        for r in refs:
            a, b, c = r.split('.')
            if a == str(v) and b != '0': A.setdefault(int(b), []).append(r)
        return sorted(A.items())
    for v in (1, 2, 3):
        p = v - 1
        if v > 1:   # the vallī's opening śānti pāṭha (2.0.1, 3.0.1)
            I.append(item('shanti.%d' % v, p, 'shanti.%d' % v, 'shanti', '', L['%d.0.1' % v]))
            topics.append({'id': 'shanti.%d' % v, 'hi': 'शान्तिपाठ', 'en': 'Shanti Paath'})
        for a, rs in anuvakas(v):
            for r in rs:
                lines = L[r]
                if r == '2.1.1': lines = L['2.0.2'] + lines   # ब्रह्मविदाप्नोति परम्: the first words of anuvāka 2.1
                n = r.split('.')[2]
                # the printed number of the paragraph is its own (॥२॥ ends 1.3.2)
                y = 'shanti' if r in ('1.1.1', '1.12.1') else 'mantra'
                tail = []
                if r in ('1.12.1', '2.9.1', '3.10.6'):   # the vallī's closing words are an item of its own
                    k = next(i for i, l in enumerate(lines) if l.startswith('॥ इति') and 'वल्ली समाप्ता' in l)
                    lines, tail = lines[:k], lines[k:]
                I.append(item(r, p, 'a%d.%d' % (v, a), y, n, lines))
                if n == '1':
                    h, e = THEME[v][a - 1]
                    topics.append({'id': r, 'hi': '%s अनुवाक — %s' % (ORD[a - 1], h), 'en': 'Anuvak %d — %s' % (a, e)})
                if tail:
                    # the सह नाववतु the page prints again after vallīs 2 and 3 is not an item: the recording does not
                    # sing it there (PLAYBOOK §11; reconciliation.md, "Structure")
                    I.append(item('iti.%d' % v, p, 'iti.%d' % v, 'iti', '', tail[:1]))
    assert [x['id'] for x in I].count('2.0.2') == 0 and len({x['id'] for x in I}) == len(I)
    return I, topics

if __name__ == '__main__':
    I, topics = build()
    textfile.write(os.path.join(HERE, '..', 'text.txt'), I, topics, ['1', '2', '3'], 'sa', [
        'Taittirīya Upaniṣad: the three vallīs (Śīkṣā, Brahmānanda, Bhṛgu), shlokam.org. Made by source/settle.py from the',
        'page (scriptures-data); do not edit here. Every correction and choice: reconciliation.md.'])
    print(len(I), 'items:', ', '.join('%s %d' % (y, sum(x['y'] == y for x in I)) for y in ('shanti', 'mantra', 'iti')))
