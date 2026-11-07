# Reconciliation: Śrīmad Bhāgavata Mahāpurāṇa

The base is the owner's Gita Press book (codes 26–27), read from its glyph ids (`README.md`). Every difference from the book, and every choice made where the e-book is broken, is listed here.

## The e-book's layout, read as the book prints it
- **Two flows on a page.** The e-book draws the verses and the Hindi as two flows: a page can end a verse's first lines, show the Hindi of the verses before it, and finish the verse on the next page. The verses and the Hindi are therefore read as two separate streams in each adhyāya, joined again by the verse numbers (`source/verses.py`, `source/hindi.py`).
- **Visible halants.** Where the e-book draws a conjunct as a halant and a zero-width space (श्रीमद्‌भागवतम्, दृष्ट्‌वा), the space is dropped and the word is written whole (श्रीमद्भागवतम्, दृष्ट्वा).
- **Long pādas.** The e-book's column wraps a long pāda (śārdūlavikrīḍita, mandākrāntā, sragdharā …) in two; the two halves are one line here, a hyphen at the wrap removed (जन्माद्यस्य यतोऽन्वयादितरत- / श्चार्थेष्वभिज्ञः स्वराट् → जन्माद्यस्य यतोऽन्वयादितरतश्चार्थेष्वभिज्ञः स्वराट्). A hyphen at the end of a pāda, where the book carries a word over to the next pāda, stays.
- **Prose.** The Sanskrit prose is joined into one line per numbered passage; the e-book's hyphens inside its words, left from the printed book's line breaks, are removed.
- **Visarga.** In 19 places the e-book types the visarga as a colon (आत्मदेव: पुरे); it is ः.
- **Daṇḍas and numbers** are written by the library's standard (`tools/text/standard.py`): । । is ॥, a verse number ॥१॥; a Sanskrit nasal before a stop is that stop's own nasal (संतोष → सन्तोष), as the standard writes every Sanskrit text.
- **Variant readings** (the book's superscript १ २ … on the readings of its old manuscript, प्रा॰ पा॰, printed under each adhyāya) are not part of the text and are left out with their marks (`docs/PLAYBOOK.md` §2: fix, don't annotate).
- **The book's notes** (टिप्पणी, 185, marked * † ‡ in the Hindi and once in a verse of the Māhātmya, 1.36) are under the meaning that carries their mark, each starting with its mark, the mark kept in the Hindi as printed (`source/notes.py`). The book prints an adhyāya's notes after its closing words; marks and notes are paired in order through each skandha, a pair having the same mark, so a note printed with the next adhyāya's notes still finds its verse (10.3.53, 10.9.23, 10.19.12). How the notes were read:
  - the same marks * † ‡ come round again and again, so a mark is matched only to the note in its place in the sequence;
  - several short notes on one line (10.5.5: * पौराणिक। † वंशका वर्णन करनेवाले। ‡ …; 11.7.8) are one note each;
  - a stray * that the e-book prints before the second point of a numbered note (10.17.25: * १. … * २. …) does not start a new note;
  - a heading over a note (अग्नि-पान, 10.17.25) starts it, followed by —;
  - a note that begins on the same line as variant readings (2.7.9) is taken from after them; volume 2 prints its variants without प्रा॰ पा॰ (१. ऽम्बुपूरिताः। २. …) and they are left out the same way;
  - a mark after a paragraph's verse number (11.12: ॥ २४ ॥ *) stays after it;
  - 10.87: one note to verse 14 introduces Śrīdhara Svāmī's 28 verses on the Veda-stuti, each verse with its Hindi under the verse it explains (14–41).
  - Not included: two notes in the Māhātmya's instructions for a saptāha (the instructions themselves are not in the library) and the book's closing note on its end marks.

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

## English meanings (Tagare)
G. V. Tagare's translation (Motilal Banarsidass) follows another edition of the Bhāgavata (Kṣemarāja Śrīkṛṣṇadāsa's), whose verses are sometimes divided or numbered differently and which has verses the Gita Press lacks. The owner's copy of wisdomlib.org puts each English entry beside the Gita Press verse of the same number, so where the two numberings part, the English sits under the wrong verse (1.6.36 had the English of the vīṇā verse, which is the Gita Press's 33). Each Gita Press verse here takes Tagare's verse of the same number unless `source/english/placement.json` says otherwise; `source/english/shifts.py` finds where the numberings part by looking for the names and other Sanskrit words of each English verse in the Gita Press verse and its Hindi, and every adhyāya it lists was read verse by verse against the Hindi:

| Adhyāya | Gita Press | Tagare | Why |
|---|---|---|---|
| m.6 | 47–100 | 50–103 | Tagare has three more verses of food rules (47–49); Gita Press 101–103 have no English in the copy |
| 1.6 | 29–36 | 32–39 | Tagare repeats 26–28 as 29–31; Gita Press 37–39 have no English in the copy |
| 1.16 | 7–8 | 7–9 | the same lines divided into three verses: one meaning under 8 |
| 1.16 | 9–35 | 10–36 | |
| 2.2 | 9–23, 24–25 | 10–24, 25 | Tagare's 9 (on holding the mind steady) has no verse of its own here; his 25 covers 24–25 (one meaning under 25) |
| 5.7 | 8–13 | 9–14 | Tagare has a verse 8 the Gita Press lacks |
| 8.7 | 43–46 | 42–45 | Tagare has no verse for 42 (Śiva takes up the poison) |
| 9.8 | — | — | the copy's English for this adhyāya is the Rāma story of 9.10, repeated: none here |
| 10.16 | 3–27 | 4–28 | the copy has lost Tagare's 3; Gita Press 28–29 together are Tagare's 29 |
| 10.37 | 1–2, 3–34 | 1, 2–33 | Tagare's 1 is Gita Press 1–2 |
| 10.51 | 21, 22–63 | 21–22, 23–64 | |
| 10.57 | 14–17, 18–29, 30–31, 32–34, 35–41 | 14–18, 19–30, 31–32, 33–35, 36–42 | |

Read and found to agree by number (the words matched a neighbour by chance): 3.21, 4.21, 9.10, 10.84; and, read at the places a looser search pointed to, 2.6, 3.28, 4.15, 7.2, 9.22, 11.19.

The copy's entries are taken back out and renumbered from the text itself (`source/english/read.py`): an entry that goes on into later verses (9.7's 21–23 also holds "24-25(A). …" and "25(B)-27. …") is split at those numbers; an entry that starts with its own number (10.82: "12. …", "14. …") takes it; what follows a line like "[ Padaratnāvalī’s Text adds:]" is another recension's verse and is left out (10.22, 10.44, 10.53, 10.90); two misprinted numbers are read as 83 (m.6) and 11-12 (10.60). Gita Press and Tagare verses linked by the placement form one meaning, under the last Gita Press verse, with the Gita Press numbers when there are several: "(24–27)". Tagare's footnotes (2,723) go with the meaning of the verse that carries them. Tagare's verses not placed are listed in `source/english/not_placed.txt` (38: Tagare's extra verses above, and 9.8).

Verses with no English: 10.80 and 12.6, which the copy does not have; 9.8; and these, whose English the copy lacks (Tagare may join them with a neighbour, but the copy does not say): m.2.72; m.3.13,60–74; m.4.51; m.5.5; m.6.101–103; 1.6.13,37–39; 1.7.23; 1.16.36; 2.5.8; 2.9.40; 3.2.2; 3.4.21; 3.6.1–2; 3.11.28; 3.28.1; 3.29.2; 3.30.14; 4.6.16–19; 4.7.52,55; 4.14.12–13,20; 4.24.14,32–33; 4.28.16; 5.1.31; 5.4.6; 5.7.14; 5.14.40; 5.17.15; 5.20.39; 5.21.9; 5.26.11,23–25,34; 6.6.30–31; 6.7.7–9; 6.9.38; 6.18.12–14; 6.19.26; 7.3.6–7,9–10; 7.5.39–40; 7.8.19; 7.9.4; 7.11.19–20; 8.5.7,15,19; 8.7.42; 8.8.35–37; 8.9.16; 8.10.13–14,19–22; 8.13.15; 8.22.29; 8.23.11; 10.10.2; 10.23.10; 10.32.20; 10.33.17–22; 10.36.3; 10.51.64; 10.53.18–19,32; 10.57.42; 10.64.9; 10.67.21; 10.71.29; 10.72.1–2; 10.74.13–15; 10.82.6,11,13; 10.83.25; 10.86.17–18; 10.89.8; 11.3.47; 11.4.8; 11.19.20–23; 11.21.39–40; 11.22.34,53; 11.23.17–19; 11.29.13–14; 11.31.1–4; 12.1.15; 12.2.19; 12.7.9,23; 12.11.39; 12.12.11,26.
