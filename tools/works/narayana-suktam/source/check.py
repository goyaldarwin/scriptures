"""Checks text.txt (the Nārāyaṇa Sūkta) against the Devanagari witnesses in source/witness/ (made by witnesses.py), with
the comparison shared by the six Sūktas (tools/works/sukta_witness.py: what is not compared and what is read alike).
The only differences allowed are those recorded in reconciliation.md (EXPECTED below).
Usage: python3 tools/works/narayana-suktam/source/check.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..')); import sukta_witness

BOTH = [   # readings of the recited text that both witnesses word otherwise (reconciliation.md, "Kept")
    ('', 'ओम्'),                                   # the ॐ the recitation opens the sūkta, the Gāyatrī and the śānti with
    ('परमं प्रभुम्', 'परमं पदम्'), ('परमं नित्यं', 'परमान्नित्यं'), ('जगत्यस्मिन् दृश्यते', 'जगत्सर्वं दृश्यते'),
    ('हृदयं तद्विजानीयाद्', 'ज्वालमालाकुलं भाती'), ('मस्तकम्', 'मस्तकः'), ('मध्यस्था विद्युल्', 'मध्यस्थाद्विद्युल्')]
# A pair is compared in key form inside the run (sukta_witness.letters), so it ends on a whole following word where a
# sandhi joins it to the next (a visarga before स, a final न् before a consonant).
EXPECTED = {   # witness file: [(witness, ours)]
    'wikisource-ta.txt': BOTH + [
        ('नारायणपरं ब्रह्म तत्वं नारायणः परः । नारायणपरो ज्योतिरात्मा नारायणः परः ।',     # the two lines in the other order,
         'नारायणपरो ज्योतिरात्मा नारायणः परः । नारायणपरं ब्रह्म तत्त्वं नारायणः परः । नारायणपरो ध्याता ध्यानं नारायणः परः ।'),  # no ध्याता line
        ('वितस्त्यान्तु', 'वितस्त्यान्ते'),
        ('कविः सन्तापयति', 'कविः तिर्यगूर्ध्वमधश्शायी रश्मयस्तस्य सन्तताः सन्तापयति'),   # the line the page lacks
        ('पीताभास्यात्तनूपमा', 'पीता भास्वत्यणूपमा'),
        ('स ब्रह्मा स शिवस्सेन्द्रः सो', 'स ब्रह्म स शिवः स हरिः सेन्द्रः सो'), ('वै नमः', 'वै नमो नमः'),
        # svaras the page places otherwise, kept as the recited text has them (the witness's word, ours)
        ('ना॒राय॒णप॑रं', 'ना॒राय॒णपर॑-म्ब्र॒ह्म॒'), ('त॒त्वन्ना॑राय॒णः', 'तत्त्व-न्ना॑राय॒णः'), ('अन॑न्त॒मव्य॑यङ्क॒विꣳ', 'अनन्त॒मव्यय॑-ङ्क॒विग्ं')],
    'wikisource-mnu.txt': BOTH + [
        ('नारायणः परं ब्रह्म तत्त्वं नारायणः परः । नारायणः परो ज्योतिरात्मा नारयणः परः । नारायणः परो ध्याता',
         'नारायणपरो ज्योतिरात्मा नारायणः परः । नारायणपरं ब्रह्म तत्त्वं नारायणः परः । नारायणपरो ध्याता'),
        ('व्यवस्थिता नील', 'व्यवस्थितः नील'), ('नीवारशूक्वत्', 'नीवारशूकवत्'), ('भास्वत्यणूपम तस्याः शिखाया', 'भास्वत्यणूपमा तस्याः शिखाया'),
        ('स ब्रह्मा स शिवः स', 'स ब्रह्म स शिवः स')],
}

if __name__ == '__main__':
    sys.exit(1 if sukta_witness.compare(os.path.join(HERE, '..', 'text.txt'), os.path.join(HERE, 'witness'), EXPECTED) else 0)
