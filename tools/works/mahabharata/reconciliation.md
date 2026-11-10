# Reconciliation: the Mahābhārata and its source

The base is the owner's Gita Press e-books (codes 32–37). Every change below is one the book itself settles (its own sequence of numbers, its Hindi, its own counts) or a fault of the e-book's encoding, never a reading taken from another edition, but for one garbled word settled by a witness (below). Every place is listed, with what the book has and what the text has, in `source/check.md` (made by `source/make_text.py` with the text); the rules are these.

## The e-book's encoding
- **Lost virāmas.** Between two consonants the e-book often has a zero-width joiner where the virāma belongs (बुद्ध‍या for बुद्ध्या, वह‍ने for वह्ने, द्व‍यधिक for द्व्यधिक: 925 places in the verses), or a zero-width non-joiner before य (विद्ध‌यनादी for विद्ध्यनादी). The joiner is read as the virāma it stands for (`source/epub.py` → `joiners`). Every other joiner only steers the glyphs (भगवान्‌, महद्‌दिव्यं, a non-joiner before र) and is dropped; the letters are the same.
- **The ½ of a verse number** is an image in the e-book (॥ ८½ ॥); it is written ½.
- **Marks:** ।। is ॥ (the standard), word joiners and no-break spaces are spaces; an ASCII colon typed for the visarga in a verse (सोमपा:) is ः (11 places).
- **Styles set by mistake** are read by what the block is: Sanskrit prose set in the Hindi paragraph's style (6 passages: Vana 192 (two), Śānti 190, Śānti 342 (three)) is prose; Hindi set in the prose's bold (3 paragraphs) is Hindi; a speaker's line set as a paragraph is a speaker's line; closing words set as prose are closing words. A verse that ends "। २३ ॥", "॥ ११।" or "॥ ३५" ends ॥ २३ ॥ (11 places).
- **A half verse printed after the number at an adhyāya's end** (its Hindi covers both) is a line of the verse before it (Droṇa 60, 112, 138; Anuśāsana 96).

## Verse numbers
- **A misprinted number** that breaks the run while its neighbours keep it (… १२, ५३, १४ … in Virāṭa 1) is corrected to its place in the run, and the printed number with it (17 places, each listed with its neighbours in `source/check.md`).
- **A verse printed without its number** between n and n+2 (a bare ॥, outside brackets), whose Hindi names n+1, or a run of such verses that fills a gap exactly (a list of names in Ādi 116), is numbered (6 places).
- **A verse the book numbers twice** (16 and 16½ in Vana 176) keeps both, as printed.
- **Adhyāya numbers** follow the book's order in each parva; where its closing words print another number (Bhīṣma 30 "६", Bhīṣma 93 "१३"), the closing words keep it as printed.

## The dākṣiṇātya reading
- The book prints the southern reading among the numbered verses, without numbers: in ( … ) through most of the epic, and without brackets in the long passages of the Anuśāsana (13, 96, 145) and Āśvamedhika (92). Every unnumbered verse is an item of its own (`dshloka`, `dgadya`), the brackets left out (the type says what it is). Its count is checked against the one the book prints under the adhyāya (462 counts: 460 agree within one śloka; Ādi 80 and Virāṭa 3 count about two ślokas more than the unnumbered lines the book prints there; the text keeps what is printed).
- Where a passage opens inside a numbered verse (between its halves), the numbered verse stays whole and the passage follows it. Where the book leaves a bracket open, the next numbered verse closes it (Sabhā 38, Vana 157, Vana 233). A bracket closed inside a line ends the passage there (a prose passage in Vana 199; elsewhere before the line's daṇḍa). A bracket opened while one is open (Ādi 123) ends the first passage in a half verse.

## What is left out
- The pictures and their captions; the Gītā verse printed under a picture (Udyoga 7); the tables of verse counts after the Vana and Virāṭa parvas and at the end; the Bhārata-sāvitrī printed on the last page of each volume (it is in the text at Svargārohaṇa 5.60–64); the "श्रवण-महिमा" printed after the Droṇaparva, which repeats its last adhyāya's last three verses.
- The Sanskrit closing words of Udyoga 95, which the book does not print (its Hindi closing words are there): the adhyāya has no `iti` item.
- The book's bracketed headings inside a few long dākṣiṇātya passages (95) are not shown yet (they need English).

## Hindi and notes
- Copied as printed; each paragraph under the last verse its mark names (27 marks name a verse its paragraph does not follow, a misprint of the mark: the paragraph stays under the verse it follows, its mark as printed); a paragraph printed before its verse ends joins the next one (the Vālmīki Rāmāyaṇa's rule). A paragraph after the last verse of an adhyāya with its verse still running on (4) goes under the verses before it.
- **Two corrections of a verse by hand** (`source/corrections.json`), each a word the e-book's glyphs garbled: Śalya 46.39 तथद्ध्र्या → तथर्द्ध्या (तथा + ऋद्ध्या, as the Hindi reads it); Ādi 2.129 शाङ्गर्या → शार्ङ्ग्यां (Sørensen's index of the Mahābhārata, from the Calcutta edition, the vulgate Gita Press follows: *maharṣer Mandapālasya śārṅgyāṃ tanayasambhavaḥ*; the critical edition śārṅgyaṃ; the book's Hindi शार्ङ्गी पक्षीके गर्भसे).
