# Muṇḍaka Upaniṣad — how the text is settled

**Source of truth:** the shlokam.org page <https://shlokam.org/text/mundaka-upanishad.htm>, saved as HTML (private copy in scriptures-data at `hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/printouts/shlokam/mundaka-upanishad.html`). It gives the śānti mantra and mantras 1.1.1–3.2.10 in Devanagari (`div.detail-sanskrit`, lines split at `<br>`), each with its own transliteration, and the closing words of khaṇḍas 1.1–3.1. It has no svara marks, no zero-width characters and no mantra 3.2.11.

**Witnesses:** the page's own transliteration, read first (below), and four web texts, compared with the settled text word for word by `source/check.py` (next section).

**The page's own transliteration.** `source/settle.py` reads every transliteration line back into Devanagari and compares it with the Devanagari line letter for letter before any correction: all 241 lines agree. So each slip below is in both scripts, and it is settled on the page's third layer, its word-by-word list for that mantra (only its Devanagari headwords are read), with the grammar and the metre.

The library's writing standard (docs/PLAYBOOK.md §3) applies: ॥ and compact verse numbers (`॥१॥`), Pāṇini's spelling, the ISO 15919 transliteration made from the verse. This is an Atharvaveda text: the anusvāra is ं, never ꣳ.

## The śānti mantra
The page's block starts with the heading मुण्डकोपनिषत्, the title, not part of the mantra: left out. It then has the same five lines as the Māṇḍūkya's śānti (the Atharvaveda Upaniṣads' śānti pāṭha: भद्रं कर्णेभिः … and the four svasti lines), and the text writes them as the Māṇḍūkya does:

| Page | Settled | Why |
|---|---|---|
| श्रुणुयाम | शृणुयाम | A broken form: the optative of श्रु is शृणुयाम (Ṛgveda 1.89.8); the Māṇḍūkya's text has it. Only the sanskritdocuments family prints the śānti (Wikisource, the Heritage Portal: श्रुणुयाम, the page's own reading), so no independent witness speaks to it. |
| तुष्टुवाꣳसस् | तुष्टुवांसस् | ꣳ is the Yajurveda's way of writing the anusvāra; this is an Atharvaveda text. |
| …बृहस्पतिर्दधातु। / ॥ ॐ शान्तिः शान्तिः शान्तिः ॥ | …बृहस्पतिर्दधातु ॥ / ॐ शान्तिः शान्तिः शान्तिः ॥ | The daṇḍas only: the line had no space before its daṇḍa, and the mantra ends there; written as in the Māṇḍūkya, so the one śānti reads alike on one shelf. |

## The web witnesses
Each is written as a Devanagari text in `source/witness/<site>.txt` by `source/witnesses.py` from its raw download (scriptures-data, `hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/printouts/<site>/`). All four number the mantras muṇḍaka.khaṇḍa.mantra and count 64: 9, 13, 10, 11, 10, 11.
- **IIT Kanpur**, Heritage reader, text MNU (the primary मूलम् of each verse; `printouts/iitk/`): no śānti; the closing words of khaṇḍas 1.1, 1.2, 2.2, 3.1 and 3.2 inside the last mantra. Many typing slips of its own (ध्द for द्ध throughout, पुरूष for पुरुष, missing avagrahas, समावेदो, अप्रणो, वायुज्र्योति, नमरूपाद्), so it counts only where another witness agrees. `witness/iitk.txt`.
- **upanishads.org.in** (Sri Aurobindo's text, one page per mantra, the page's `p.sloka`; `printouts/upanishads-org/`): no śānti, no closing words. `witness/upanishads-org.txt`.
- **Sanskrit Wikisource**, मुण्डकोपनिषद् (`action=raw`; `printouts/wikisource/`) and the **Vedic Heritage Portal** (`printouts/vedicheritage/`): both are the sanskritdocuments.org text (Wikisource names it; both have its headings ॥ श्रीः ॥, ॥ ॐ ब्रह्मणे नमः ॥, ॥ प्रथममुण्डके प्रथमः खण्डः ॥ … and its colophon), and so is the shlokam.org page: they share its slips (तं 1.1.2, जायाते 1.1.9, अग्नीर् 2.1.4, पश्यन्त्विहैव 3.1.7, अर्चयेत् भूति- 3.1.10, and in Wikisource also तापः, शारो, ज्योतिषं, प्रणो, कर्मण). The three are one witness (PLAYBOOK §2): their agreement does not by itself decide a reading. The Heritage Portal writes ꣳ with a private-use glyph of its font (U+E001), read as ꣳ. `witness/wikisource.txt`, `witness/vedicheritage.txt`.
- GRETIL has no Muṇḍaka.

`source/check.py` compares each block (mantra, śānti, closing words) as one run of letters: the witnesses divide words and lines differently, so spaces, line breaks, daṇḍas and numbers are not compared, and the spellings the library's standard makes one (a class nasal or ं, a word-final म् or ं, ꣳ) are read alike. After the corrections below it finds no difference with any witness apart from those listed under "Witness readings left as they are".

## Corrections to the mantras
Each is a slip in both scripts that the page's own word list for the mantra gives correctly. The independent witnesses (IIT Kanpur, upanishads.org.in) have every corrected form, except तां (1.1.2), where upanishads.org.in has तं; the sanskritdocuments family (Wikisource, the Heritage Portal) shares several of the page's slips (above).

| Item | Page | Settled | Why |
|---|---|---|---|
| 1.1.2 | …ब्रह्माऽथर्वा तं पुरोवाच… | …ब्रह्माऽथर्वा तां पुरोवाच… | तां, the feminine accusative: it takes up यां … ब्रह्मविद्याम्, the knowledge Atharvan told Aṅgir, as in the word list (tāṃ) and Śaṅkara's reading; the masculine तं has no noun to refer to. IIT Kanpur and the Heritage Portal have तां; upanishads.org.in and Wikisource have तं. |
| 1.1.9 | …ज्ञानमयं तापः | …ज्ञानमयं तपः | The word list has तपः; ताप ("heat, pain") breaks the sense and the metre (the even pāda of the anuṣṭubh needs a short seventh syllable: ज्ञा-न-म-यं-त-पः after यस्य). |
| 1.1.9 | …अन्नं च जायाते | …अन्नं च जायते | जायाते is not a word; the word list has जायते. |
| 1.2.9 | अविद्यायं बहुधा… | अविद्यायां बहुधा… | A dropped ā: the locative अविद्यायाम्, as in 1.2.8 (अविद्यायामन्तरे) and the word list. |
| 2.1.4 | अग्नीर्मूर्धा… | अग्निर्मूर्धा… | "Fire is his head": the nominative अग्निः, as in the word list; अग्नीः is an accusative plural. |
| 2.2.4 | …धनुः शारो ह्यात्मा | …धनुः शरो ह्यात्मा | The arrow, शरः, as in 2.2.3 (शरं) and the same mantra's शरवत्; the word list has शरः. |
| 2.2.9 | तच्छुभ्रं ज्योतिषं ज्योतिः… | तच्छुभ्रं ज्योतिषां ज्योतिः… | "The light of lights": the genitive plural ज्योतिषाम्, as in the word list. |
| 3.1.2 | …निमग्नोऽनिशया शोचति… | …निमग्नोऽनीशया शोचति… | "By helplessness": the instrumental of अनीशा (अन् + ईशा, "lack of mastery"), as in the word list (anīśayā); अनिशा is not the word. |
| 3.1.4 | प्रणो ह्येष… | प्राणो ह्येष… | प्राणः, the life of all, as in the word list; प्रण is not the word. |
| 3.1.7 | …पश्यन्त्विहैव निहितं… | …पश्यत्स्विहैव निहितं… | "In those who see": the locative plural पश्यत्सु (with इहैव, पश्यत्स्विहैव), as in the word list (paśyatsu); पश्यन्तु ("let them see") breaks the sentence. |
| 3.1.8 | …तपसा कर्मण वा | …तपसा कर्मणा वा | The instrumental कर्मणा beside चक्षुषा, वाचा, तपसा, as in the word list; the dropped ā also breaks the triṣṭubh's cadence (⏑ – –). |
| 3.1.10 | …ह्यर्चयेत् भूतिकामः | …ह्यर्चयेद्भूतिकामः | The sandhi: a final त् before a voiced consonant becomes द् (Pāṇini 8.2.39), as the page itself writes it elsewhere (यद्भूतयोनिं 1.1.6, तद्भावगतेन 2.2.3); the word list gives the two words, अर्चयेत् and भूतिकामः. |
| 3.2.5 | …वीतरागाः प्रशान्ताः | …वीतरागाः प्रशान्ताः । | The half-verse's daṇḍa, dropped: every other half-verse of the page has one. |
| 3.2.8 | …समुद्रेऽ / स्तं गच्छन्ति… | …समुद्रेऽ- / स्तं गच्छन्ति… | A word (समुद्रेऽस्तं) broken at the line end without the hyphen the page puts at every other such break (अवर्ण-, क्रियावा-, कामां-). |

## Kept as printed (valid forms, not errors)
- अद्रेश्यम् (1.1.6), योषितायाम् (2.1.5), वेद्धव्यम् (2.2.2, 2.2.4), कामभिर्जायते (3.2.2): the readings of the received text, which the word lists confirm.
- The Vedic hiatus: तत्रापरा ऋग्वेदो (1.1.5), सप्त इमे लोका (2.1.8), सर्वे एकीभवन्ति (3.2.7), विज्ञानमयश्च आत्मा (3.2.7), कृतात्मनस्तु / इहैव (3.2.2).
- A word kept in its pausa form at a pāda's end or before a pause (धनुर् गृहीत्वा, वाग् विवृताः, सर्वविद् यस्य, पुरस्ताद् ब्रह्म, तद् विज्ञानेन): the page's spacing, the same words.
- 2.2.7: two lines of anuṣṭubh (यः सर्वज्ञः … प्रतिष्ठितः ॥) and four of triṣṭubh (मनोमयः …) as one mantra, with the inner ॥, as the page numbers it.
- 3.1.8: the last pāda on two lines (…निष्कलं / ध्यायमानः ॥८॥), as the page breaks it.
- The line divisions are the page's throughout.

## The khaṇḍas' closing words
The page prints ॥ इति मुण्डकोपनिषदि … खण्डः ॥ after the last mantra of khaṇḍas 1.1, 1.2, 2.1, 2.2 and 3.1, inside that mantra's block. They are separate items of type `iti` (`1.1.iti` …), so a mantra holds only its own words.

## Mantra 3.2.11 and the closing words of khaṇḍa 3.2 (settle.py → ADDED)
The page ends with 3.2.10; every witness has a mantra 3.2.11 and all but upanishads.org.in the closing words after it. They are added from the witnesses, word by word:

| Item | Settled | Witnesses |
|---|---|---|
| 3.2.11, line 1 | तदेतत्सत्यमृषिरङ्गिराः | All four; Wikisource writes तदेतत् सत्यम्, a space only. |
| 3.2.11, line 2 | पुरोवाच नैतदचीर्णव्रतोऽधीते । | upanishads.org.in, Wikisource, the Heritage Portal (न एतत् अचीर्णव्रतः अधीते: the avagraha marks the a dropped after -o); IIT Kanpur's व्रतोधीते drops it, one of its typing slips. |
| 3.2.11, line 3 | नमः परमऋषिभ्यो नमः परमऋषिभ्यः ॥११॥ | upanishads.org.in, Wikisource, the Heritage Portal; IIT Kanpur writes परम ऋषिभ्यो, a space only (the Vedic hiatus, as तत्रापरा ऋग्वेदो 1.1.5). |
| 3.2.iti | ॥ इति मुण्डकोपनिषदि तृतीयमुण्डके द्वितीयः खण्डः ॥ | Wikisource, the Heritage Portal, IIT Kanpur (with ।। for ॥); the same words as the other khaṇḍas' closings on the page. |

The line division is upanishads.org.in's and Wikisource's (the Heritage Portal and IIT Kanpur put the first two lines on one).

## Witness readings left as they are (source/check.py → EXPECTED)
- **A reading of one witness against the base and the others**: upanishads.org.in's प्रतिपादयेच्छ्रद्धया हुतम् (1.2.2; the others end प्रतिपादयेत्); IIT Kanpur's भैक्षचर्यां (1.2.11; the others भैक्ष्य-); the Heritage Portal's सन्दधीत (2.2.3; the others संधयीत).
- **The Vedic hiatus and pausa** the base keeps (above), where one witness writes the sandhi or the reverse: the Heritage Portal's सप्तेमे (2.1.8), सर्वे अस्मात् (2.1.9), स्वाद्वत्ति अनश्नन्नन्योऽभि- (3.1.1), सर्व एकीभवन्ति (3.2.7), and IIT Kanpur's सर्वं एकीभवन्ति (3.2.7).
- **Spellings**: संनिधाय (2.2.7; upanishads.org.in, IIT Kanpur) for the base's सन्निधाय; येनाक्रमन्ति (3.1.6; upanishads.org.in, IIT Kanpur) without the base's ऽऽ, and IIT Kanpur's तेनाऽऽतुराः (1.2.9) with it; the Heritage Portal's यस्मिंल्लोका (2.2.2) for यस्मिँल्लोका and IIT Kanpur's यजूँषि (2.1.6) for यजूंषि; IIT Kanpur's and the Heritage Portal's लोकां कर्मचितां (1.2.12) for लोकान् कर्मचितान्.
- **The sanskritdocuments family's slips** that the base shared and phase 1 corrected (above), and its own: Wikisource's तत्वतो (1.2.13), प्रणो (2.1.3, 2.1.4), श्रद्ध (2.1.7), तुष्टुवाँसस् (the śānti); the Heritage Portal's देवाः भद्रं (the śānti), वर्तमानाः वयं (1.2.9), व्योमन्यात्मा (2.2.7), धीराः युक्तात्मानः (3.2.5).
- **IIT Kanpur's typing slips** (`check.py` lists each; ध्द and पुरूष are read as द्ध and पुरुष throughout): अङ्गिर, सत्यवहाय, समावेदो, निरूक्तं, विश्वरूची, चयवन्ते, अमृताः, गुरू, अप्रणो, वायुज्र्योति, बह्वी, सर्व क्रतवो, पश्चक्षद्धा, पुरुष वेदं, तद्यो, नाडयः, विरञ्जनः, विद्वां, ह्याकामाः, नमरूपाद्, एकर्षि, and missing avagrahas.

## What the page lacks and the text leaves out
After 3.2.iti, Wikisource and the Heritage Portal print the Upaniṣad's colophon (॥ इत्यथर्ववेदीय मुण्डकोपनिषत्समाप्ता ॥) and the śānti again; IIT Kanpur and upanishads.org.in print neither. Only the sanskritdocuments family has them, one witness, so the text ends with 3.2.iti.
