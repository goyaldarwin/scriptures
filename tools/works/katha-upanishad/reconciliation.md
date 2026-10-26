# Kaṭha Upaniṣad — how the text is settled

## The source and its limits
The owner's book (Swami Gurubhaktananda, Sandeepany Text 20) prints every mantra three times: in Devanagari (font "BRH Devanagari"), in IAST, and as the author's word-by-word. The Devanagari text layer is the font's own byte codes (`Á EzÉlÉç Wû uÉæ …`) and cannot be read; the IAST layer is clean once sixteen Latin-1 symbols the font uses for the accented letters are decoded (`¡` ā, `£` e, `µ` o, `¯` ṃ, `§` ī, `¾` ś, `»` ṛ, `¦` ḥ, `½` ṣ, `³` ṇ, `°` m̐, `À` ū, `¿` ṭ, `±` ṅ, `²` ñ, `¢` ḍ; the avagraha comes out as `:'`). The text is therefore the book's transliteration converted letter for letter to Devanagari (`source/settle.py` → `iast2deva`). The conversion is deterministic: every IAST letter has exactly one Devanagari spelling, and anusvāra (ṃ) and candrabindu (m̐) are kept as the book writes them.

## The witnesses
- **shlokam.org** (<https://shlokam.org/text/kathopanishad.htm>): the page serves mantras 1.1.1–1.1.20 and the śānti mantra to a reader (the rest loads only in a browser). These 21 verses are in `source/witness/shlokam-1.1.1-20.txt`, and `check.py` finds **no difference** in words between them and our text. The two sources are independent (the book's IAST, the site's Devanagari), so this agreement is the check that the decoding and the conversion are right.
- **sanskritdocuments.org** (`doc_upanishhat/katha.html`, the owner's saved copy, in scriptures-data at `<work path>/printouts/sanskritdocuments/`): the standard Devanagari text, all 119 mantras in six vallīs, the śānti before and after (the closing one numbered ॥ १९॥ in vallī 2.3, as in the book). Its verses are in `source/witness/sanskritdocuments-full.txt`; after the corrections below `check.py` finds **no difference** in words in any of the 121 items, apart from the four line-division cases listed as expected.

## Corrections to the book's reading (settle.py → FIX), from the full witness
- **1.3.3 रथिनं** (rathinam, "the lord of the chariot"): the book's IAST has *rathitaṃ*, a slip.
- **2.2.2 शुचिषद्वसुरन्तरिक्षसद्** (vasur antarikṣasat, Ṛgveda 4.40.5): the book has *-rāntarikṣa-*, a slip.
- **1.1.26 जरयन्ति**: the book's *jarayaṃti* would give an anusvāra before त; the witness has the dental न्, as the grammar requires.
- **ꣳ before a sibilant** (तपाꣳसि, पदꣳ, तनूꣳ, स्पर्शाꣳश्च) and **सङ्ग्रहेण**: IAST writes all of these with ṃ, so the book cannot show which Devanagari sign the tradition uses; the Kṛṣṇa Yajurveda witness writes ꣳ and ङ्, as the library's Śrī Rudram does. `t` renders ꣳ as gͫ, as there.
- **2.3.2 किं च**: two words, as the witness divides them (the book's IAST runs them together).
- The witness writes श‍ृ with a joiner (1.2.7); the check ignores it.

## Differences left as they are (check.py → EXPECTED)
- Line division inside a sandhi: 1.2.18 विपश्चिन् / नायं, 2.1.1 स्वयम्भूः / तस्मात् and ऐक्षद् / आवृत्त, 2.3.17 प्रवृहेन् / मुञ्जादिव — the book ends the line at the pāda, in pausa form; the witness writes the sandhi across it on one line. The words are the same.
- The closing śānti: the witness sets it without the opening ॐ and with सह वीर्यं, तेजस्विनावधीतमस्तु; ours repeats the opening śānti exactly, as the recitation does.

## Decisions
- **Mantra count and numbering.** The standard count: 1.1 (29), 1.2 (25), 1.3 (17), 2.1 (15), 2.2 (15), 2.3 (18). The book numbers the closing śānti mantra as 2.3.19; it is the same सह नाववतु as the opening, and is item `shanti.2`.
- **Line division** follows the book (which follows the metre): two lines for an anuṣṭubh, four for a triṣṭubh; a word broken across lines keeps the hyphen at the line end, as the witnesses print it (1.1.9 मे-/ऽनश्नन्, 1.1.20, 1.2.1, 1.2.20, 2.1.2, 2.2.2, 2.3.16, 2.3.18). The refrain एतद्वै तत् is on its own line when the book sets it so (2.1.3, 2.1.5 …) and at the end of the last line where the book puts it there (2.3.1). 1.3.17 has three lines as in the book.
- **Punctuation.** The book's `|` and `||` become । and ।।; each mantra's last line ends with its number within the vallī in Devanagari digits (।।१।।). The book's two commas (1.1.1 after वाजश्रवसः, 1.3.14 after जाग्रत) are the author's and are dropped.
- **ॐ** is written with the sign ॐ (as shlokam.org), the book's `om̐`.
- **Candrabindu** (तँ ह, कुमारँ, किँ स्वित्, सुखँ, हँसः …): kept where the book's IAST has `m̐` (the font's `°`), which is exactly where shlokam.org has ँ.
- **Transliteration `t`** is made back from the settled Devanagari in the library's convention (ṁ for anusvāra, ’ for the avagraha, ॥N॥), so it always spells the text; `check.py` proves it.

## Open
- None for the text. The owner may want to check 2.3.18's audio start by ear (`audio/smvedroad/fixes.md`).
