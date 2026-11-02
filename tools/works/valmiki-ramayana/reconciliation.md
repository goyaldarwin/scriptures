# Śrīmad Vālmīki Rāmāyaṇa — how the text is settled

## The source
The owner's Gita Press *Śrīmad Vālmīki-Rāmāyaṇa, with Sanskrit text and English translation* (codes 452–453, revised edition). The text is the book's own, read from its text layer, never by OCR (the owner's rule):
- The Devanagari is set in the legacy Chanakya font. Its 171 codes are mapped to Unicode in `source/chanakya.py`: each code was read from the glyph's shape in the font embedded in the PDF (`source/glyphsheet.py` renders its outlines) and confirmed by the words it occurs in across the book. The font's pieces are put in Unicode order there (the pre-base ि, the reph written after its syllable, half forms completed by the ā bar or by the bar inside ो / ौ, an anusvāra typed inside a conjunct, ई as इ with a hook).
- Checks: an unknown code stops the decoding; every word of the 2,303 pages is well-formed Devanagari (no sign without a consonant, no two vowel signs, no sign after a virāma); a glyph printed twice at the same place (the PDF overprints) is read once; a space inside a word (justification) is dropped, and a word gap with no space character (two places) is a space.
- `source/parse.py` divides the book into kāṇḍas, sargas, verses and English paragraphs (page regions, columns, wrapped colophons, the book's misprinted verse marks).

## The witnesses
- **IIT Kanpur / Rashtriya Sanskrit Vidyapeetha, Tirupati** (valmiki.gitasupersite.in) and **valmikiramayan.net** (sanskritdocuments.org copy), the owner's scrapes, Bāla to Yuddha; their Sanskrit is in `source/witness/`. Both follow one other Southern edition, so their agreement against Gita Press is usually that edition's reading, not a Gita Press error.
- Every sarga was compared half-verse by half-verse (`source/run_wit.py`: confident line matches as anchors, letters compared after folding conventions of spelling: ं and class nasals, ःस and स्स, doubled consonants after र्, spaces). Gita Press stays the text. A place was examined where Gita Press differs from both witnesses and either breaks the metre (16 syllables a half-anuṣṭubh) or has a word found nowhere else in its 23,700 verses nor in IIT Kanpur (`source/suspects.py`): 754 places, each decided with a reason (`source/review/batch-*.decisions.json`); every correction was then checked independently against the printed page (`source/review/corrections.checked.json`).
- **Rule:** Gita Press is corrected only where its reading is clearly wrong (a non-word, a broken form or construction, broken metre, a dropped or extra sign, a name against the book's own spelling) and the witnesses give the right form; a valid reading of this edition is kept, whatever the others read.
- The Uttara-kāṇḍa has no witness: its half-verses that break the anuṣṭubh were examined (all kept), and the long-metre verses with uneven pādas (`source/review/longmetre.json`: half-equal metres of the vaitālīya family) are as printed.

## Corrections to the book's reading (settle.py)
### Printing slips found by the decoding checks, confirmed on the page
- bala.5.8 मुक्तपुष्पावकीेर्णेन → मुक्तपुष्पावकीर्णेन (a stray e-sign in the text layer, not printed)
- bala.45.4 जगााम → जगाम (the book prints a doubled ā)
- yuddha.92.43 भु्ङ्क्ते → भुङ्क्ते (a stray virāma in the text layer, not printed)

### Verse numbers
- The book numbers two verses 63 in yuddha.17, 25 in yuddha.61 and 22 in uttara.20: the second is 64, 26 and 23 (the sequence; the English marks in the first two).
- The book's slips in verse marks (॥॥४०, ॥ 4॥ with a Latin digit, विना९॥, ॥ ६८ without the closing ॥, ॥ ३१॥ ॥) are written ॥N॥.

### A verse the book does not print
- **sundara.1.154**: the book prints its English ("At the command of Śrī Rāma, I am going to seek her presence as his messenger …") but not its Sanskrit. Filled from IIT Kanpur (its 5.1.155): तस्याः सकाशं दूतोऽहं गमिष्ये रामशासनात्। कर्तुमर्हसि रामस्य साह्यं विषयवासिनि॥ — its रामशासनात् is the English's "at the command"; valmikiramayan.net has रामकारणात्.

### Readings corrected against the witnesses (67)
| Verse | Gita Press | Text | Why |
|---|---|---|---|
| bala.2.10 | पुमासं | पुमांसं | पुमासं is not a form; the accusative of पुंस् is पुमांसम्, with the anusvāra dropped in print. |
| bala.3.26 | अङ्गलीयकदानं | अङ्गुलीयकदानं | अङ्गलीयक is not a word; the ु of अङ्गुलीयक (ring), which Gita Press prints elsewhere, was dropped. |
| bala.5.8 | मुक्तपुष्पावकीेर्णेन | मुक्तपुष्पावकीर्णेन | The stray े on की is an extra sign that makes a non-word. |
| bala.6.25 | भद्रैर्मद्रैर्मृगैश्चैव | भद्रैर्मन्द्रैर्मृगैश्चैव | The verse lists the three classes of elephants (भद्र, मन्द्र, मृग) and their mixtures, so मद्रैः is a slip for मन्द्रैः. |
| bala.15.15 | एतच्छ्रत्वा | एतच्छ्रुत्वा | The ु of श्रुत्वा was dropped, giving a non-word. |
| bala.18.54 | राजार्षिशब्देन | राजर्षिशब्देन | राजार्षि is not a word; the compound is राजर्षि. |
| bala.26.2 | कौसिकस्येति | कौशिकस्येति | Gita Press spells Viśvāmitra's name कौशिक everywhere else, so स is a slip. |
| bala.26.33 | ववनमब्रवीत् | वचनमब्रवीत् | ववनम् is not a word; the formula is इदं वचनमब्रवीत्. |
| bala.28.6 | नैरास्यविमलावुभौ | नैराश्यविमलावुभौ | The word is नैराश्य, which is Gita Press's spelling everywhere else; नैरास्य is a misspelling. |
| bala.30.4 | रक्षतां | रक्षतं | With युवाम्, a second-person dual imperative (रक्षतम्) is required; रक्षताम् is third person. |
| bala.39.26 | यज्ञहनोऽस्माकमनेनाश्वोऽपनीयते | यज्ञहरोऽस्माकमनेनाश्वोऽपनीयते | अयं needs a nominative noun, and यज्ञहनः (genitive/ablative of यज्ञहन्) does not fit; यज्ञहरः 'stealer of our sacrifice' matches the horse being carried off. |
| bala.41.16 | सुपर्णमनिलोपम् | सुपर्णमनिलोपमम् | The pāda has only 7 syllables and अनिलोपम् is not a form; the accusative is अनिलोपमम्. |
| bala.43.37 | जह्रुं | जह्नुं | The sage is जह्नु, as Gita Press prints in the same sarga (verses 35 and 38), so र is a slip for न. |
| bala.55.9 | भग्नद्रंष्ट्र | भग्नदंष्ट्र | द्रंष्ट्र is not a word; the stray ् र makes it a misspelling of दंष्ट्रा (fang). |
| bala.73.40 | अथोपकार्यं | अथोपकार्यां | The noun 'royal tent' is the feminine उपकार्या (as Gita Press prints elsewhere), so the accusative is उपकार्याम्; the dropped ा gives a non-noun. |
| bala.76.11 | जामदग्नयोऽसौ | जामदग्न्योऽसौ | जामदग्नय is not a word and gives the pāda 9 syllables; the patronymic is जामदग्न्यः. |
| bala.77.14 | सदिता | सहिता | सदिता is not a word; the sense is भर्तृभिः सहिताः 'together with their husbands'. |
| ayodhya.4.31 | चानयिता | चानायिता | The sense 'Sītā had been brought' needs the causative participle आनायिता; आनयिता is an agent noun and does not fit. |
| ayodhya.9.2 | यौवराज्ये भरतं | यौवराज्ये च भरतं | The pāda यौवराज्ये भरतं has only 7 syllables; the च that both other editions have restores the metre. |
| ayodhya.9.23 | प्रत्युदीक्षेया | प्रत्युदीक्षेथा | With मा स्म, the second-person optative middle is प्रत्युदीक्षेथाः (written -था before म); प्रत्युदीक्षेया is not a form. |
| ayodhya.9.63 | गताभितो | गतामितो | मां … गताम् इतः 'me gone hence to Yama's realm' needs the accusative गताम्; the nominative गता does not agree with मां, so भ is a slip for म. |
| ayodhya.24.20 | पितरपेक्षया | पितुरपेक्षया | पितरपेक्षया is not a possible form; the compound needs the genitive पितुः, a dropped ु sign. |
| ayodhya.30.10 | प्रस्थितुमर्हसि | प्रस्थातुमर्हसि | प्रस्थितुम् is not a possible infinitive of स्था; the correct form is प्रस्थातुम्. |
| ayodhya.43.16 | चामरप्रभाः | चामरप्रभः | चामरप्रभाः is plural against the singular subject; the bahuvrīhi must be चामरप्रभः, an extra ा. |
| ayodhya.48.25 | सर्वमनालम्भमनायकम् | सर्वमनालम्बमनायकम् | आलम्भ means 'seizing, killing', not 'support'; the sense 'without support' needs अनालम्बम्, a ब/भ slip. |
| ayodhya.52.86 | समक्षसे | समीक्षसे | समक्षसे is not a verb form; a dropped ी, the verb is samīkṣase 'you look upon (Brahmaloka)'. |
| ayodhya.56.1 | व्यातीतायामवसुप्तमनन्तरम् | व्यतीतायामवसुप्तमनन्तरम् | vi+atīta gives vyatīta; व्यातीता is an impossible form with an extra ा. |
| ayodhya.58.33 | प्रव्रज्य | प्रव्राज्य | With the object रामं the sense 'having banished Rāma' needs the causative absolutive pravrājya, as Gita Press itself prints 'रामं प्रव्राज्य' at 2.79.2; intransitive pravrajya cannot take रामं. |
| ayodhya.65.20 | करेणेव इवारण्ये | करेणव इवारण्ये | Followed by इव, the word must be the plural noun kareṇavaḥ (करेणव इव 'like she-elephants'); करेणेव would double the इव and is a slip of an extra े. |
| ayodhya.69.14 | निषष्ण्णं | निषण्णं | निषष्ण्णं is a non-word with a doubled ष्; the participle is niṣaṇṇa. |
| ayodhya.73.3 | क्षारमिवाददाः | क्षारमिवादधाः | Putting salt on a wound needs ā-dhā (ādadhāḥ 'you placed'); ā-dā means 'take', so द for ध is a slip. |
| ayodhya.91.75 | समुद्रेष्ववतिष्ठतः | समुद्गेष्ववतिष्ठतः | Sandal pastes kept 'in oceans' (samudra) makes no sense; the sense requires samudga 'caskets', as both sources read, so र is a typesetting slip for ग. |
| ayodhya.104.23 | वाक्यमब्रतीत् | वाक्यमब्रवीत् | अब्रतीत् is a non-word; the verb is अब्रवीत्, with त printed for व. |
| ayodhya.107.9 | क्षिप्रमेवाभिषिञ्चनात् | क्षिप्रमेवाभिषेचनात् | अभिषिञ्चन is not a Sanskrit noun (MW and Apte have no such headword); the noun is अभिषेचन, which Gita Press itself prints in the same phrase at Ayodhyā 4.15. |
| ayodhya.118.15 | चास्म्युचितां | चास्म्युचितं | The feminine accusative उचितां has nothing to agree with; the sense 'what fitting and dear thing shall I do' (उचितं … प्रियं च किम्) needs neuter उचितं, as the other sources read. |
| aranya.9.32 | त्रैलोक्यामपि | त्रैलोक्यमपि | त्रैलोक्य is neuter only, so the accusative is त्रैलोक्यम्; त्रैलोक्याम् is an impossible form with an extra ा. |
| aranya.41.12 | भुज्यन्ते | भज्यन्ते | The simile of chariots wrecked on rough ground requires भज्यन्ते 'are broken' (√भञ्ज्); भुज्यन्ते 'are eaten/enjoyed' gives no sense and is a one-vowel slip. |
| aranya.52.30 | प्रशोभयत | प्राशोभयत | The imperfect of प्र-√शुभ् causative needs the augment (प्र+अ = प्रा), and Gita Press has no augmentless form of this verb elsewhere; the ा is dropped. |
| aranya.52.34 | उत्पातवाताभिरता | उत्पातवाताभिहता | Trees 'struck' (अभिहता) by portent-winds is the sense; अभिरता 'delighting in' makes no sense here and is a र/ह slip. |
| aranya.54.28 | युस्माकं | युष्माकं | युस्माकं is a non-word; the pronoun is युष्माकम् with retroflex ष. |
| aranya.55.1 | कृत्कृत्यममन्यत | कृतकृत्यममन्यत | कृत्कृत्य is a non-word and leaves the half-verse at 15 syllables; कृतकृत्य mends both. |
| aranya.63.8 | नाभिपातः | नाभिभातः | The two breasts are the subject, so the verb must be dual न अभिभातः 'do not shine'; नाभिपातः gives a singular noun with no construction, a भ/प slip. |
| aranya.68.27 | दिधक्ष्यामि | दिधक्षामि | दिधक्ष्यामि is no valid form (the desiderative future would be दिधक्षिष्यामि); the present desiderative दिधक्षामि 'I wish to burn' is the intended word, with an intrusive य्. |
| aranya.69.5 | त्रिकोशं | त्रिक्रोशं | The distance measure is क्रोश; कोश has no such sense in MW and Gita Press has त्रिकोश nowhere else, so the र is dropped. |
| aranya.69.14 | समालम्भत | समालम्बत | The imperfect 'clung to' is from सम्-आ-√लम्ब्; √लभ् takes no nasal in the imperfect, so समालम्भत is a भ/ब slip. |
| aranya.70.8 | अच्छिन्दन्तां | अच्छिन्दतां | The dual imperfect of √छिद् is अच्छिन्दताम्; अच्छिन्दन्तां is an impossible form with an extra nasal. |
| kishkindha.7.16 | सुग्रीवचनात् | सुग्रीववचनात् | सुग्रीवचनात् is a non-word with a dropped व, leaving the half-verse at 15 syllables. |
| kishkindha.10.22 | विकान्तं | विक्रान्तं | विकान्तं is a non-word; the र is dropped from विक्रान्त 'valiant'. |
| kishkindha.13.28 | जम्मुः | जग्मुः | जम्मुः is a non-word; the perfect of √गम् is जग्मुः. |
| kishkindha.20.22 | बाह्व्यो | बह्व्यो | बाह्व्यो is a non-word; the feminine plural of बहु is बह्व्यः. |
| kishkindha.26.21 | वसुधायं | वसुधायां | वसुधायं is an impossible form; the locative 'on the ground' is वसुधायाम्. |
| kishkindha.26.36 | अभ्यषिञ्चत | अभ्यषिञ्चन्त | The verb has the many monkeys named in verse 35 as its subject and must be plural; the singular drops न्. |
| kishkindha.28.39 | दृतं | द्रुतं | The rivers hasten to the ocean, so the adverb is द्रुतम् 'swiftly'; दृतं (only a lexicon word) is the common ृ/्रु slip. |
| kishkindha.31.5 | स्ववीक्षितं | स्ववेक्षितं | सु+अवेक्षित gives स्ववेक्षितम् 'well-considered'; स्ववीक्षितं is broken sandhi with no sense. |
| kishkindha.35.1 | ब्रूवाणं | ब्रुवाणं | The participle of √ब्रू is ब्रुवाण with short ु; ब्रूवाणं is an impossible form. |
| kishkindha.39.18 | अनेकैर्बहुसास्रैर्वानराणां | अनेकैर्बहुसाहस्रैर्वानराणां | बहुसास्रैः is a non-word with a dropped ह, leaving the half-verse at 15 syllables. |
| sundara.1.69 | अभिध्नंस्तु | अभिघ्नंस्तु | अभिध्नन् is a non-word; the participle of abhi-√han is अभिघ्नन्, a ध/घ glyph slip. |
| sundara.1.205 | विलोकयत् | विलोकयन् | The verse depends on ददर्श of verse 204 and needs the participle agreeing with the subject (cf. परिलोकयन् in 203); विलोकयत् is a त/न slip. |
| sundara.2.25 | दंष्ट्राभिर्बहुभिः | दंष्ट्रिभिर्बहुभिः | Feminine दंष्ट्राभिः cannot agree with masculine बहुभिः शूरैः; the adjective दंष्ट्रिभिः "fanged" is required. |
| sundara.6.6 | दान्तकाञ्चनराजतीः | दान्तकाञ्चनराजतैः | The compound qualifies the instrumental रथैः and must end in -ऐः; the feminine accusative -ईः agrees with nothing. |
| sundara.9.33 | नानावेषबिभूषितम् | नानावेषविभूषितम् | बिभूषित is a non-word (a ब/व slip); Gita Press prints विभूषित everywhere else (69 times). |
| sundara.9.36 | संवृतदान्तानि | संवृतदन्तानि | दान्त means "tamed", not "teeth"; the faces have closed teeth (दन्त), so the extra ा is a slip. |
| sundara.10.42 | परिविद्ध्यांगैः | परिपीड्यांगैः | परिविद्ध्य is not a possible absolutive of pari-√vyadh (that is परिविध्य); the sense "pressing the drum with her limbs" needs परिपीड्य, as the other sources read. |
| yuddha.18.30 | आनाय | आदाय | आनाय is only a noun ('net'), not the gerund needed with सुकृतं ... गच्छेत्; the sense 'taking his merit' requires आदाय, as both sources read. |
| yuddha.36.20 | मध्यमेऽस्थापयद गल्मे बहभिः | मध्यमेऽस्थापयद् गुल्मे बहुभिः | अस्थापयद गल्मेबहभिः drops the virāma and two ु signs (17 syllables, non-words); गुल्मे बहुभिः restores grammar, sense and the 16-syllable metre as the sources read. |
| yuddha.83.38 | विचिन्विता | विचिन्वता | विचिन्विता is no form; the instrumental of the participle विचिन्वत् (agreeing with अधनेन) is विचिन्वता, an extra ि sign. |
| yuddha.90.56 | तद्विहितं | तद्विहतं | विहितं 'arranged' gives no sense; the Vāruṇa weapon was struck down, विहतं, an extra ि sign as the sources show. |

### Proposed and kept as printed (valid readings of this edition)
- **bala.2.12** पत्त्रिणा: पत्त्रिन् is a valid spelling (MW headword pattrin) and the book uses the same त्त्र in पतत्त्रिन् (1.14.34, 36) and तोत्त्र, so it is the edition's spelling, not a slip.
- **bala.38.21** प्राहसन्नित्यं: प्राहसन्नित्यं is valid sandhi of the singular imperfect प्राहसत् + नित्यम्, and the edition's translation ("laughed to see them drowning") reads a finite verb, so nothing is wrong.
- **ayodhya.8.1** त्वभ्यसूय्यैनामुत्सृज्याभरणं: अभ्यसूय्य is the regular absolutive of the denominative असूय with a preverb (असूय + ल्यप्, final a dropped by अतो लोपः, giving -असूय्य), so the printed form is correct.
- **ayodhya.64.49** मूलमुपैष्यथः: उपैष्यथः is a correct second-person dual, and the epic construes भवत् with second-person verbs (the book has स भवान् … कर्तुमर्हसि at 3.40.16), so the reading is valid.
- **ayodhya.73.17** पुत्रगर्द्धिनीम्: Doubling a consonant after reph is a valid spelling, and the book spells this word with र्द्ध again in समरगर्द्धिना (7.14.2) and महर्द्धिनां (5.8.5), so it is the edition's orthography, not an error.
- **aranya.53.26** नृपात्मजामागतगात्रवेपथुः: The nominative construes with पापः, and the edition's own translation reads it so ("although a tremor ran through his limbs"), so -वेपथुः is a deliberate reading of this edition.
- **sundara.38.40** अपारवारमक्षोभ्यं: अपारवार is a meaningful compound, "without limit (पार) or bound in time (वार)", and the edition's translation reads exactly "limitless in time or space", so it is the edition's reading, not a प/व slip.
- **sundara.58.67** कंचिदपश्यन्तीं: कंचित् त्राणम् construes as "anyone as a refuge" (masculine pronoun with a predicative neuter noun), and the edition translates "finding no saviour", so the printed reading is valid.

### The epic's active use of -ईक्ष्यमाण, kept
The book writes -ईक्ष्यमाण in an active sense (looking at) in six places, an old epic usage the other editions smooth to -ईक्षमाण; it is the edition's reading, not a slip, and stays: ayodhya.47.19, sundara.58.67, yuddha.82.1, uttara.48.25, and
- **bala.7.21** अवेक्ष्यमाणश्चारेण (the other editions: अवेक्षमाणश्चारेण)
- **ayodhya.68.19** प्रेक्ष्यमाणा (the other editions: प्रेक्षमाणा)

## The English (meanings/en/gitapress.json)
Gita Press's English, its diacritics converted (`source/english.py`). A joint translation of several verses (the book's `(19—22)`) sits under the last of them, with the mark as printed. The book's misprinted marks are read as meant: `14)` and `76)` without "(", `(I)` and `(l00)` with letters for digits, `(99)` for (69), `(133-34)` abbreviated. Where the book prints no mark, its two verses' English stays one (bala.70: the English of 37 breaks off mid-sentence and 38 follows; yuddha.32.7–8; yuddha.59.133–134; uttara.76: 24 breaks off; split where the next verse begins); uttara.15 prints no English for verses 1–5. A line-end hyphen is decided by the book's own usage mid-line (joined when the book writes the word whole, e.g. forthwith, however; kept for compounds). The book's 240 footnotes are under the verses whose English carries their mark (198 verses, `notes`), read from the footnote region of each page and matched mark by mark (`source/footnotes/report.md`); the few line-end hyphens in them were each decided by hand (kept in compounds, removed in after-noon). An English line printed in a mixed font, or beside the Devanagari of a quoted word, is part of the paragraph it stands in.

## The Hindi (meanings/hi/gitapress.json)
Gita Press's Hindi translation (code 77), read from its glyph ids against the official Noto Sans Devanagari 2.000, with no OCR (`source/hindi/report.md`: method, checks and every anomaly of the e-book). Its verse numbering is the Sanskrit edition's (640 of 648 sargas end on the same verse). A paragraph marked ½ (it runs into the next verse) or with a bare ॥ (1,412 paragraphs: the book prints no number) is not a boundary: it joins the next into one meaning under the last verse it covers, every printed mark kept; a run of bare paragraphs that covers exactly one verse each goes under those verses.

## Topics
One per sarga: the Hindi title of the Hindi edition and the English title of the English edition.

## Open
- None in the text.
