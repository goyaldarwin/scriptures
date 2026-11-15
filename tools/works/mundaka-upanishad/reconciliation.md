# Muṇḍaka Upaniṣad — how the text is settled

**Source of truth:** the shlokam.org page <https://shlokam.org/text/mundaka-upanishad.htm>, saved as HTML (private copy in scriptures-data at `hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/printouts/shlokam/mundaka-upanishad.html`). It gives the śānti mantra and mantras 1.1.1–3.2.10 in Devanagari (`div.detail-sanskrit`, lines split at `<br>`), each with its own transliteration, and the closing words of khaṇḍas 1.1–3.1. It has no svara marks, no zero-width characters and no mantra 3.2.11.

**Second witness:** the page's own transliteration. `source/settle.py` reads every transliteration line back into Devanagari and compares it with the Devanagari line letter for letter before any correction: all 241 lines agree. So each slip below is in both scripts, and it is settled on the page's third layer, its word-by-word list for that mantra (only its Devanagari headwords are read), with the grammar and the metre.

The library's writing standard (docs/PLAYBOOK.md §3) applies: ॥ and compact verse numbers (`॥१॥`), Pāṇini's spelling, the ISO 15919 transliteration made from the verse. This is an Atharvaveda text: the anusvāra is ं, never ꣳ.

## The śānti mantra
The page's block starts with the heading मुण्डकोपनिषत्, the title, not part of the mantra: left out. It then has the same five lines as the Māṇḍūkya's śānti (the Atharvaveda Upaniṣads' śānti pāṭha: भद्रं कर्णेभिः … and the four svasti lines), and the text writes them as the Māṇḍūkya does:

| Page | Settled | Why |
|---|---|---|
| श्रुणुयाम | शृणुयाम | A broken form: the optative of श्रु is शृणुयाम (Ṛgveda 1.89.8); the Māṇḍūkya's text has it. |
| तुष्टुवाꣳसस् | तुष्टुवांसस् | ꣳ is the Yajurveda's way of writing the anusvāra; this is an Atharvaveda text. |
| …बृहस्पतिर्दधातु। / ॥ ॐ शान्तिः शान्तिः शान्तिः ॥ | …बृहस्पतिर्दधातु ॥ / ॐ शान्तिः शान्तिः शान्तिः ॥ | The daṇḍas only: the line had no space before its daṇḍa, and the mantra ends there; written as in the Māṇḍūkya, so the one śānti reads alike on one shelf. |

## Corrections to the mantras
Each is a slip in both scripts that the page's own word list for the mantra gives correctly.

| Item | Page | Settled | Why |
|---|---|---|---|
| 1.1.9 | …ज्ञानमयं तापः | …ज्ञानमयं तपः | The word list has तपः; ताप ("heat, pain") breaks the sense and the metre (the even pāda of the anuṣṭubh needs a short seventh syllable: ज्ञा-न-म-यं-त-पः after यस्य). |
| 1.1.9 | …अन्नं च जायाते | …अन्नं च जायते | जायाते is not a word; the word list has जायते. |
| 1.2.9 | अविद्यायं बहुधा… | अविद्यायां बहुधा… | A dropped ā: the locative अविद्यायाम्, as in 1.2.8 (अविद्यायामन्तरे) and the word list. |
| 2.1.4 | अग्नीर्मूर्धा… | अग्निर्मूर्धा… | "Fire is his head": the nominative अग्निः, as in the word list; अग्नीः is an accusative plural. |
| 2.2.4 | …धनुः शारो ह्यात्मा | …धनुः शरो ह्यात्मा | The arrow, शरः, as in 2.2.3 (शरं) and the same mantra's शरवत्; the word list has शरः. |
| 2.2.9 | तच्छुभ्रं ज्योतिषं ज्योतिः… | तच्छुभ्रं ज्योतिषां ज्योतिः… | "The light of lights": the genitive plural ज्योतिषाम्, as in the word list. |
| 3.1.4 | प्रणो ह्येष… | प्राणो ह्येष… | प्राणः, the life of all, as in the word list; प्रण is not the word. |
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

## What the page lacks
The page ends with 3.2.10. It has no mantra 3.2.11, no closing words for khaṇḍa 3.2 or the Upaniṣad, and no closing śānti. They wait for the owner's sanskritdocuments.org printout (a written witness); the text adds nothing from memory.
