# Aitareya Upaniṣad — how the text is settled

## The source and its limits
The owner's book (Swami Gurubhaktananda, Sandeepany Text 34) is the Kaṭha's series and typesetting: every mantra is printed in Devanagari (font "BRH Devanagari", whose text layer is the font's own byte codes and cannot be read), in IAST (font "BRH Latin"), and as the author's word-by-word. The two scripts stand side by side on the same lines, so `source/extract.py` reads the IAST by its font from the PDF's spans and decodes the Latin-1 symbols with the Kaṭha's map (`tools/works/katha-upanishad/reconciliation.md`). The author's line numbers ("11.", "1)") are dropped. `source/settle.py` converts the IAST letter for letter with the Kaṭha's `iast2deva`; a visarga the font gives as ":" (प्राणाद्वायुः, प्रहासीः) is ḥ, and the pluta's 3 joins its vowel (इती३). The book's own word-by-word transliteration (its "Om aatmaa vaa …" column) is a second reading of every word by the same author; it is read only to settle a slip, never copied.

## The witnesses
- **sanskritdocuments.org** (`aitareya.itx`, Sunder Hattangadi, proofread with John Manetta; the owner's printout, in scriptures-data at `<work path>/printouts/sanskritdocuments/aitareya.pdf`): all 33 mantras, with the śānti before and after. Its text layer scrambles the vowel signs, so it was read on its page images (rendered with PyMuPDF) into `source/witness/sanskritdocuments-full.txt`, as printed, slips and all. It prints the same edition as the book: it shares most of the book's slips.
- **upanishads.org.in** (`/u/aitareya/p/<a.k.m>`, Sri Aurobindo's text, CWSA 18; the raw pages in scriptures-data at `<work path>/printouts/upanishads-org/aitareya/`): all 33 mantras, no śānti. It never writes ॐ, and never the avagraha after ā (प्रतिष्ठान्तरिक्षं, यथाण्डम्); `check.py` reads both texts that way for it (`NORM`). An independent edition.
- **IIT Kanpur Heritage** (the reader's API, `AIU`; the raw JSON in scriptures-data at `<work path>/printouts/iitk/AIU/`): all 33 mantras, no śānti; many typing slips of its own (below). An independent typing.

`source/check.py` compares letters, not word division: the text is prose and the witnesses divide words differently (अधस्तात्ता आपः · अधस्तात् ता आपः). The spellings the library's standard makes one (class nasal or ं, word-final म् or ं) are read alike. After the corrections and the differences below it finds **no other difference** in any item of any witness (sanskritdocuments.org: the śānti twice and the 33 mantras; the other two: the 33 mantras).

## Corrections to the book's reading (settle.py → FIX)
Each is a slip in the book's IAST (a non-word, a broken form, or a form its own word-by-word contradicts), corrected to the form that witnesses give.
- **1.1.2 अधस्तात्ता आपः** (tāḥ āpaḥ, "those are the waters"): the book has *adhastātta āpaḥ*; its word-by-word has *taah aapah*; upanishads.org and IITK have ता. sanskritdocuments.org shares the slip.
- **1.1.4 निरभिद्येतां … निरभिद्येतामक्षीभ्यां** (the dual nirabhidyetām, "the two burst open", as कर्णौ निरभिद्येतां in the same mantra): the book has *nirabhidyetaṃ*, *nirabhidyetam*; its word-by-word has *nirabhidyetaam* both times; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **1.1.4 प्राणः प्राणाद्वायुः**: two words (the book runs them together).
- **1.2.1 तमशनायापिपासाभ्याम्** (aśanāyā, hunger, as in 1.2.5 twice): the book has *aśanāpipāsābhyām*; its word-by-word has *ashanaayaa pipaasaabhyaam*; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **1.2.5 भागिन्यौ**: the book's *bhāginnyau* doubles the n; every witness has भागिन्यौ, as the book itself in the next line (भागिन्यावेव).
- **1.3.5 ग्रहीतुं स**: the book's *grahītun sa* (an n before s); 1.3.4–1.3.9 have ग्रहीतुं स, as upanishads.org and IITK here. sanskritdocuments.org prints ग्रहीतु/न्.
- **1.3.5, 1.3.9 हैवान्नमत्रप्स्यत्** (ha eva annam, "he would have been satisfied with food"): the book has *haivānam* in these two, *haivānnam* in the other six; upanishads.org and IITK have अन्नम्. sanskritdocuments.org shares the slip.
- **1.3.6 यद्धैनच्छ्रोत्रेणा-** (śrotreṇa, as in the same mantra's first line): the book has *śroteṇa*. sanskritdocuments.org shares the slip.
- **1.3.9 यद्विसृज्य** (visṛjya, "by emitting"): the book has *yadvitsṛjya*; its word-by-word has *visrijya*; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **1.3.10 यद्वायुरन्नायुर्वा** (annāyuḥ, "whose life is food"): the book has *anāyur*; its word-by-word has *annaayuh*; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **1.3.13 इदमदर्शमिती३** (adarśam, "I have seen"): the book has *adarśanam*; its word-by-word has *idam adarsham iti 3*; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **2.1.1 आत्मन्येवाऽऽत्मानं** (eva ātmānam): the book's *eva''tmānaṃ* drops the long ā that the double avagraha stands for, as the book writes it in 3.1.4 (*prājñenā''tmanā*); IITK has एवाऽऽत्मानं, upanishads.org एवात्मानं. sanskritdocuments.org shares the slip (एवऽऽत्मानं).
- **2.1.3 गर्भं बिभर्ति** (the object, "bears him as an embryo"): the book has *garbha*; its word-by-word has *garbham*; every witness agrees.
- **2.1.3 भावयत्येषां लोकानां** (the genitive plural): the book has *eṣaṃ*; its word-by-word has *eshaam*; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **2.1.4 अथास्यायमितर आत्मा**: the book has *athāsyāyāmitara atmā*, two slips; every witness has अयमितर आत्मा.
- **2.1.6 उत्क्रम्य** (the gerund, as in 3.1.4): the book has *utkrāmya*; every witness has उत्क्रम्य.
- **3.1.2 धृतिर्मतिर्मनीषा** (dhṛtiḥ and matiḥ, two of the sixteen names): the book has *dhṛtimatir*; its word-by-word lists *dhritih* and *matih* apart; upanishads.org and IITK agree. sanskritdocuments.org shares the slip.
- **3.1.3 आकाश आपो** (āpaḥ, the waters): the book has *apo*; every witness has आपो.

## Layout of the book's lines (settle.py)
- **1.3.2 / 1.3.3:** the book ends its "Verse 3.2" with तदेनत्सृष्टं पराङ्त्यजिघांसत्; every witness begins mantra 1.3.3 with these words. They begin 1.3.3 here, and 1.3.2 ends with तत् ॥२॥.
- **3.1.3:** the book prints the mantra in two parts ("Verse 5.3A", "5.3B"), the first ending यच्च स्थावरं ॥; it is one mantra in every witness, and the ॥ inside it is dropped.
- **2.1.1:** the book breaks अयमादितो over two lines (*ayam- / ādito*); it is one line here.
- **1.1.2:** the book writes *imām̐ llokān* as two words and puts a bar inside the sandhi प्रतिष्ठा-ऽन्तरिक्षं; here इमाँल्लोकानसृजत, as every witness, and no bar.
- **1.2.4:** *bhūtvā 'kṣiṇī* (a space before the avagraha) is भूत्वाऽक्षिणी, as every witness.
- **1.3.11:** the ॥ after प्रपद्या इति, inside the mantra, is । ; the author's question mark after कोऽहमिति is dropped.
- **1.3.12:** the author's hyphen inside the sandhi *etan-nāndanam* is dropped (एतन्नान्दनम्).
- **The śānti:** the book's closing *|| om̐ śāntiḥ śāntiḥ śāntiḥ||* is the śānti's last line, ॐ शान्तिः शान्तिः शान्तिः ॥; the author's commas are dropped (as the Kaṭha's).

## Differences left as they are (source/check.py)
**Pausa at the book's line or daṇḍa** (`PAUSA`): the book ends a line or a phrase in its pausa form where the witnesses carry the sandhi on; the words are the same. 1.1.4 (अग्निः । नासिके, वायुः । अक्षिणी, दिशः । त्वङ्), 1.2.1 (अब्रुवन् । आयतनं), 1.2.4 (प्राविशद् / आदित्य…, प्राविशन् / ओषधि…, प्राविशन् / चन्द्रमा, प्राविशद् / आपो), 1.3.11 (विसृष्टम् / अथ), 1.3.12 (द्वास्तद् / एतन्, आवसथाः / त्रयः, अयमावसथः ×3 / इति), 2.1.1 (अङ्गेभ्यः / तेजः, संभूतम् । आत्मन्येव…), 2.1.3 (भावयति / आत्मानमेव), 2.1.6 and 3.1.4 (उत्क्रम्य / अमुष्मिन्), 3.1.3 (ज्योतींषीति । एतानीमानि, च । अण्डजानि, च । अश्वा), 3.1.4 (आप्त्वा / अमृतः), and the śānti (प्रतिष्ठितं / आविः…, प्रहासीः । अनेन…, संदधामि । ऋतं, तद्वक्तारमवतु / अवतु माम् अवतु वक्तारम् / अवतु वक्तारम्, where sanskritdocuments.org runs on: …वक्तारमवत्ववतु मामवतु…).

**sanskritdocuments.org's own readings** (`EXPECTED`): its opening śānti has no ॐ (its closing one has); and, beside the book's slips it shares (above), four slips of its own: 1.1.4 श्रोत्रद्दिशः (for श्रोत्राद्), 1.2.4 प्राविशाद्दिशः (for प्राविशद्), 1.3.12 विदर्यैतया (for विदार्य) and नाऽन्दनम् (an avagraha inside नान्दनम्).

**upanishads.org.in's own readings:** 1.1.1 आसीत् । नान्यत् (the pausa at its daṇḍa; the book runs it on, आसीन्नान्यत्); 1.1.4 अक्षिभ्यां (the book, sanskritdocuments.org and IITK have अक्षीभ्यां, the dual of the Vedic stem akṣī; the base stays); 3.1.4 प्रज्ञेनात्मना (the book and sanskritdocuments.org have प्राज्ञेनाऽऽत्मना, "by the conscious Self", a sound reading; the base stays).

**IIT Kanpur's typing slips:** 1.1.1 आसीत्। नान्यत्; 1.1.3 लोकाः लोक-, पुरूषं, समुध्दृत्यामरूच्छयत्; 1.1.4 त्वङनिरभिद्यत; 1.2.1 ता ता (for ता एता), अर्णव (for अर्णवे), ता नमब्रुवन् (for ता एनम्), यस्मिन् प्रतिष्ठिता; 1.2.2 आनयता; 1.2.4 लोनानि; 1.3.1 लोकश्च, -श्चन्न्नमेभ्यः; 1.3.3 पराङत्य-, अभिव्याहृय; 1.3.6 -च्छ्रत्रेण; 1.3.7 तत्तवचा; 1.3.8 -द्धयात्वा; 1.3.13 पुरूषं, ततममपश्यदिदम्…; 2.1.1 आत्मयेवाऽऽत्मानं; 2.1.2 सास्यै; 3.1.2 यदेतत् हृदयं; 3.1.3 पुरूषा; 3.1.4 स तेन प्रज्ञेना-, सर्वान, समभवत (no virāma).

## Decisions
- **Mantra count and numbering.** The standard count and numbering, as every witness: 1.1 (4), 1.2 (5), 1.3 (14), 2.1 (6), 3.1 (4) = 33 mantras, cited adhyāya.khaṇḍa.mantra.
- **The śānti** वाङ् मे मनसि is the work's opening item, `shanti.1`, from the book's chapter 6 (the book prints it only at the end, following Śaṅkara, who counts it as a sixth chapter); sanskritdocuments.org prints it before and after. The work ends with 3.1.4 and the śānti is not repeated (PLAYBOOK §11, as the Kaṭha). Its lines are the book's.
- **The teacher's two calls** around the second adhyāya, अपक्रामन्तु गर्भिण्यः ("let the expectant mothers leave", printed by the book in Devanagari only, before 2.1.1) and यथास्थानं गर्भिण्यः ("expectant mothers, to your places", after 2.1.6), are the author's notes of the classroom tradition, not mantras, and are in no witness; they are not in the text.
- **Readings of the base kept against a witness** (a sound reading of the book's edition, PLAYBOOK §2): अक्षीभ्यां (1.1.4), प्राज्ञेनाऽऽत्मना (3.1.4), नान्दनम् (1.3.12, against sanskritdocuments.org's नाऽन्दनम्).
- **Line division** follows the book: its lines are the phrases its author numbers; prose phrases end where the book ends them, in pausa (above). A word broken across lines keeps the hyphen at the line end, as in the Kaṭha (1.1.1 आसीन्-/नान्यत्, 1.1.2, 1.3.12 विदार्यै-/तया, 1.3.14 नामे-/दन्द्रो, 2.1.6).
- **Punctuation.** The book's `|` and `||` become । and ॥; each mantra's last line ends with its number within the khaṇḍa (॥१॥). The śānti's commas are dropped.
- **ॐ** is written with the sign ॐ, the book's *om̐* (1.1.1, 2.1.1, 3.1.1 and the śānti, as sanskritdocuments.org).
- **The library's writing standard** (docs/PLAYBOOK.md §3) is applied by the exporter: a nasal before a stop as its class letter (किञ्चन, सन्तमिन्द्र, गन्धान्), ॐ, and the ISO 15919 transliteration `t` made from the verse. A Ṛgveda text: the anusvāra stays ं (no ꣳ).

## Open
- None.
