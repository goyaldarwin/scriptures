# Reconciliation: Śrīmad Bhāgavata Mahāpurāṇa

The base is the owner's Gita Press book (codes 26–27), read from its glyph ids (`README.md`). Every difference from the book, and every choice made where the e-book is broken, is listed here.

## The e-book's layout, read as the book prints it
- **Two flows on a page.** The e-book draws the verses and the Hindi as two flows: a page can end a verse's first lines, show the Hindi of the verses before it, and finish the verse on the next page. The verses and the Hindi are therefore read as two separate streams in each adhyāya, joined again by the verse numbers (`source/verses.py`, `source/hindi.py`).
- **Visible halants.** Where the e-book draws a conjunct as a halant and a zero-width space (श्रीमद्‌भागवतम्, दृष्ट्‌वा), the space is dropped and the word is written whole (श्रीमद्भागवतम्, दृष्ट्वा).
- **Long pādas.** The e-book's column wraps a long pāda (śārdūlavikrīḍita, mandākrāntā, sragdharā …) in two; the two halves are one line here, a hyphen at the wrap removed (जन्माद्यस्य यतोऽन्वयादितरत- / श्चार्थेष्वभिज्ञः स्वराट् → जन्माद्यस्य यतोऽन्वयादितरतश्चार्थेष्वभिज्ञः स्वराट्). A hyphen at the end of a pāda, where the book carries a word over to the next pāda, stays.
- **Prose.** The Sanskrit prose is joined into one line per numbered passage; the e-book's hyphens inside its words, left from the printed book's line breaks, are removed.
- **Visarga.** In 19 places the e-book types the visarga as a colon (आत्मदेव: पुरे); it is ः.
- **Daṇḍas and numbers** are written by the library's standard (`tools/text/standard.py`): । । is ॥, a verse number ॥१॥; a Sanskrit nasal before a stop is that stop's own nasal (संतोष → सन्तोष), as the standard writes every Sanskrit text.
- **Footnote marks** (the book's superscript १ २ … on the variant readings of its old manuscript, प्रा॰ पा॰, and its * † on notes to the Hindi) are not part of the text and are left out, with the variant readings themselves (`docs/PLAYBOOK.md` §2: fix, don't annotate). The Hindi notes (about 170, printed at each adhyāya's end) are not included.

## The dropped ्य (बुद्धया for बुद्ध्या)
The e-book's text often writes a conjunct ending in द्ध, द्भ, द्व, ह्व, ग्र, द्र, ष्ट, ष्ण, ष्ठ, ह्न, ङ्ग, ह्म, घ्र followed by य without its halant (बुद्धया, पद्भयां, दिष्टया, बह्वयो), which a reader takes for a different word and which breaks the metre. `source/halant.py` finds every verse line one syllable longer than its metre whose only possible repair is one such ्य; that word is then written with ्य wherever it occurs (`source/halant.json`, 86 words, about 150 places; बुद्धया → बुद्ध्या alone 31). The words it proposes that are right as printed were struck out by hand (सृष्टिविवृद्धये, स्वनिष्ठया: their lines are long for another reason; प्रहसञ्शलक्ष्णया: its fault is श्ल, below). Where the e-book has the right form elsewhere (श्रद्धया, the instrumental of श्रद्धा), it is left alone: only words a metre decides are changed. A ्य dropped in a line whose metre cannot show it is not found by this check.

## Verses
| Verse | The e-book | Here | Why |
|---|---|---|---|
| 10.33.17–22 | missing (its Hindi for them is printed) | the six verses, from the witnesses: 17–19 vedabase.io ŚB 10.33.16–18 (BBT numbers one lower here: Gita Press 10.33.16, कर्णोत्पलालक…, is a verse BBT does not count separately), 19 also vedapath.app; 20–22 wisdomlib.org, Bhāgavata Purāṇa [sanskrit] 10.33.20–22, which follows Gita Press's numbering | each matches the book's Hindi for that number; wisdomlib prints some words apart (तासां अतिविहारेण), which are joined by sandhi as the book writes (तासामतिविहारेण, भगवांस्ताभिरात्मारामोऽपि) |
| 4.14.25 | को यज्ञपुरुषो नाम यत्र वो भक्तिरीदृशी ॥ | … भक्तिरीदृशी । | a ॥ printed for । inside the verse: the next line is the verse's second half (॥२५॥) |
| 7.8.19 | ॥११॥ | ॥१९॥ | misprinted number: 18 before it, 20 after it |
| 7.9.4 | ननाम विधृताञ्जलिः ॥ (no number) | ॥४॥ | the number is missing; 3 and 5 surround it |
| 5.20.1 | ॥ ॥ (no number) | ॥१॥ | the number is missing in the prose passage |
| 10.2.27 | its last two lines printed again at the top of the next page | once | a page-turn repeat |
| 3.21.46 | तद्व + an empty glyph + ्याहृतामृत… | तद्व्याहृतामृत… | the e-book's empty glyph (.notdef) inside व्या |
| 5.9.3 | कर्मबन्धsविध्वंसन… | कर्मबन्धविध्वंसन… | a stray Latin s inside the compound |
| 7.7.4 | 1तेषामतिबलोद्योगं | तेषामतिबलोद्योगं | a stray digit before the verse |
| 9.20.10 | प्रहसञ्शलक्ष्णया | प्रहसञ्श्लक्ष्णया | श्ल drawn as श and ल; the metre needs श्ल |
| 10.80.21 | अग्रहीच्छिसा | अग्रहीच्छिरसा | र dropped (शिरसा); the metre needs it |
| 10.42.7 | पद्भयामाक्रम्य … द्वयंगुल्यु… | पद्भ्यामाक्रम्य … द्व्यङ्गुल्यु… | two dropped ्य in one line (the line is two syllables long) |
| 10.47.12, 10.17.19, 10.44.51, 11.4.21 | कुङकुम, …ङकमारोप्य, शङकितौ, सलङकं | कुङ्कुम, …ङ्कमारोप्य, शङ्कितौ, सलङ्कं | the halant between ङ and क dropped |
| 5.3.10 | हृार्हत्तम | ह्यर्हत्तम | a broken ह्य (हि अर्हत्तम) |
| 6.6.43, 11.11.40 | जहााास, नोपयुञ्ज्याान्… | जहास, नोपयुञ्ज्यान्… | a vowel sign printed two or three times |

Left as printed, for want of a witness: 4.28.47 आत्मानं शोचती दीनबन्धुं विक्लवाश्रुभिः (a syllable short; दीनमबन्धुं would fill it).

## Hindi meanings
Each Hindi paragraph ends with the mark of the verse (or verses) it explains; it is placed under the last verse its mark names, the mark kept as printed (॥ ३२-३३ ॥ under 33). Misprinted marks, read by the sequence around them:

| Adhyāya | Printed | Read as |
|---|---|---|
| 2.1 | ॥ ३ ॥ (between 32 and 34) | ॥ ३३ ॥ |
| 6.1 | ॥ ४२ ॥ (between 40 and 42) | ॥ ४१ ॥ |
| 7.9 | ॥ ०४ ॥ (between 13 and 15) | ॥ १४ ॥ |
| 10.22 | ॥ २३ ॥ (between 1 and 4) | ॥ २-३ ॥ |
| 10.85 | ॥ ४०-४३ ॥ (after 40) | ॥ ४१-४३ ॥ |

Where the book prints no mark after a verse's Hindi, that Hindi runs on into the next verse's paragraph and the verse has no meaning of its own: 1.17.43, 2.10.41, 3.27.25, 3.30.14–15, 3.31.12, 4.1.19, 7.10.56, 10.9.18.
