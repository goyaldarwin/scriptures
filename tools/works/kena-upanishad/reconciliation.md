# Kena Upaniṣad — how the text is settled

## The source and its limits
The owner's book (Swami Gurubhaktananda, Sandeepany Text 38) prints every mantra three times: in Devanagari (font "BRH Devanagari"), in IAST, and as the author's word-by-word. The Devanagari text layer is the font's own byte codes and cannot be read as text, but it can be read by eye letter by letter; the IAST layer is clean once the font's Latin-1 symbols for the accented letters are decoded (the Kaṭha's map: `¡` ā, `£` e, `µ` o, `¯` ṃ, `§` ī, `¾` ś, `»` ṛ, `¦` ḥ, `½` ṣ, `³` ṇ, `°` m̐, `À` ū, `¿` ṭ, `±` ṅ, `²` ñ, `¢` ḍ; the avagraha comes out as `:'`, and as `:` at a line's end with `'` starting the next). The text is therefore the book's transliteration converted letter for letter to Devanagari (`source/settle.py` → `iast2deva`); anusvāra (ṃ) and candrabindu (m̐) are kept as the book writes them.

## The witnesses
- **upanishads.org.in** (`/u/kena/p/<khaṇḍa>~<mantra>`, the Sanskrit of each page's `p.sloka`; raw pages in scriptures-data at `<work path>/printouts/upanishads-org/`): all 34 mantras, divided and numbered as the book does in khaṇḍa 1 (eight mantras; its 1.3 has both of the book's halves) and at 3.1/3.2; it has no śānti and no closing words. `source/witness/upanishads-org.txt`.
- **Sanskrit Wikisource**, केनोपनिषद् (`action=raw`; raw page at `<work path>/printouts/wikisource/`): the text as sanskritdocuments.org gives it (the page names it), with the śānti before and after and the closing words of each khaṇḍa; nine mantras in khaṇḍa 1. `source/witness/wikisource.txt`. It shares the book's readings where the book differs from the other witnesses (दहरम्, मीमाँस्येमेव, शशाकादतुम्, यद्देतद्, किमिदं in 3.3, and the IAST's तसै), so the book's Devanagari and this witness are one edition: their agreement does not by itself decide a reading (PLAYBOOK §2).
- **IIT Kanpur**, Heritage reader, text KNU (the primary moolam of each verse; raw JSON at `<work path>/printouts/iitk/`): nine mantras in khaṇḍa 1, the śānti before and after; many typing slips of its own (विध्दि, ब्रहम्न, विदमो, श्रृणोति, सर्वाड्गानि, तध्द, स्त्वाम …), so it counts only where it agrees with another witness. `source/witness/iitk.txt`.

`source/check.py` compares each khaṇḍa as one run of words (the witnesses divide some mantras differently), treating spacing, a nasal the library's standard folds, and candrabindu for anusvāra as conventions; after the corrections below it finds **no difference** with any witness apart from those listed under "Differences left as they are".

## Corrections to the book's reading (settle.py → FIX)
- **Śānti धर्माः**: the IAST has *dharmāh*; the book's Devanagari has धर्माः, as every witness.
- **3.5 तस्मिंस्त्वयि**: the IAST's *tasminstvayi* would give तस्मिन्स्त्वयि; the book's Devanagari has तस्मिंस्त्वयि, as upanishads.org.in.
- **4.2 पस्पर्शुः**: the IAST has *pasparśuh*; the book's Devanagari has पस्पर्शुः.
- **4.8 तस्यै**: the IAST has *tasai* (and Wikisource तसै), not a word; the book's Devanagari has तस्यै, as upanishads.org.in and IIT Kanpur ("for it", the upaniṣad of 4.7).
- **4.9 प्रतितिष्ठतीति**: the IAST spells the last word *pratitiṣṭhateeti*; the book's Devanagari has प्रतितिष्ठतीति. The other witnesses end प्रतितिष्ठति प्रतितिष्ठति; the book's closing इति is a valid reading of its edition and stays.
- **2.1 मीमाँस्यमेव**: the book (both layers) and Wikisource have मीमाँस्येमेव, which is no form of any word; *mīmāṃsyam eva*, "is still to be enquired into", is the reading of upanishads.org.in and IIT Kanpur. The book's candrabindu stays.
- **3.10 शशाकादातुं**: the book (both layers) and Wikisource have शशाकादतुं; *ādātum*, "to take" (ā-√dā, as आददीय in 3.9), is the only form, as upanishads.org.in and IIT Kanpur have it.
- **4.5 यदेतद्**: the book (both layers) and Wikisource have यद्देतद्, which no sandhi of यत् and एतत् can give; upanishads.org.in and IIT Kanpur have यदेतद्, *yad etad gacchatīva ca manaḥ*, "this, that the mind seems to go to (Brahman)".
- **4.2, 4.3 विदाञ्-/चकार**: the book breaks the word over two lines without a hyphen in the IAST (its Devanagari has one); the hyphen is kept at the line end, as the Kaṭha keeps मे-/ऽनश्नन्.

## Differences left as they are (source/check.py → LINE, READING)
- **Line division inside a sandhi**: the book ends a line in pausa form where the witnesses write the sandhi across it on one line, the words being the same: śānti श्रोत्रम् / अथो, निराकरोद् । अनिराकरणम्, धर्माः / ते; 3.1 ऐक्षन्त / अस्माकमेवायं; 3.4 कोऽसीति / अग्निर्वा; 3.5, 3.9 इति- / अपीदं; 3.7 वायव्- / एतद्; 4.2 पस्पर्शुः / ते; 4.9 पाप्मानम् / अनन्ते. Wikisource ends a line at 1.2 चक्षुषश्चक्षुः / अतिमुच्य, where the book has the sandhi.
- **1.1 ॐ**: the book (and Wikisource) begin the first mantra with ॐ; upanishads.org.in and IIT Kanpur do not. It stays, as printed.
- **1.4 यद्वाचाऽनभ्युदितं**: the avagraha for the a joined to ā, as the book and Wikisource write it; upanishads.org.in writes यद्वाचानभ्युदितं. A spelling, not a reading.
- **2.1 दहरमेवापि**: the book and Wikisource read दहरम् (dahara, "small"); upanishads.org.in and IIT Kanpur read दभ्रम् (dabhra, "little"). Both are words of the same sense and known readings; the base stays.
- **3.3 किमिदं यक्षमिति**: the book and Wikisource; upanishads.org.in and IIT Kanpur have किमेतद्यक्षमिति, as in 3.7 and 3.11. Both valid; the base stays.
- **4.9 प्रतितिष्ठतीति**: above.
- **IIT Kanpur's own slips** (no ॐ, ड्ग for ङ्ग, वाक्प्राण चक्षुः, माहं, मेस्तु in the śānti; विदमो, विध्दि, श्रृणोति, ब्रहम्न, विघ्दि in khaṇḍa 1; an extra च in 2.1; तध्दैषां, स्त्वाम, संकल्पः तध्द, वेदाऽभि, सर्वाड्गानि) are its own and change nothing; its 1.3 मनो before न विद्मो is the sandhi across its line, where the book ends the line मनः ।.

## Decisions
- **Mantra count and numbering.** The book's: 8 + 5 + 12 + 9 = 34 (its title page, "4 Chapters, 34 No. Verses"), cited khaṇḍa.mantra. The book prints mantra 1.3 in two halves, "1.3.1" न तत्र चक्षुर्गच्छति … and "1.3.2" अन्यदेव तद्विदितात् … (its headings "Verse 1.3a", "1.3b"): they are one mantra of four lines, 1.3, as upanishads.org.in prints it; a daṇḍa ends its second line (the end of the book's first half). Wikisource and IIT Kanpur count the two halves as 1.3 and 1.4, so their 1.5–1.9 are our 1.4–1.8.
- **Mantra division in khaṇḍa 3.** The book's: 3.1 runs to … महिमेति (with upanishads.org.in; Wikisource and IIT Kanpur begin their 3.2 at त ऐक्षन्त), and 3.12 begins तदभ्यद्रवत्तस्मात्तिरोदधे (all three witnesses end 3.11 with these words). A division of the prose, not a reading; the base stays.
- **The śānti** is the Sāmaveda's आप्यायन्तु, as the book prints it before the text (before it the book also prints सह नाववतु, which it calls a general invocation from the Kṛṣṇa Yajurveda; it is not the Kena's own and is left out). The book does not print it after the text, and the work ends with the closing words (PLAYBOOK §11).
- **Closing words.** Each khaṇḍa's, as the book prints them (इति केनोपनिषदि प्रथमः खण्डः …), and the Upaniṣad's, इति केनोपनिषत्, with the fourth's; the book's ॐ तत् सत् after them is the author's close and is not part of the text.
- **Line division** follows the book (its lines and indented half-lines); a word broken over two lines keeps the hyphen at the line end (3.5, 3.9 इति-, 3.7 वायव्-, 3.11 अब्रुवन्-, 4.2, 4.3 विदाञ्-, 4.3 इन्द्रो-/ऽतितराम्, 4.5 मनो-/ऽनेन).
- **Punctuation.** The book's `|` and `||` become । and ॥, including its daṇḍas inside the prose (3.6, 3.12, 4.4); each mantra's last line ends with its number within the khaṇḍa in Devanagari digits (॥१॥), the bar the book prints before the number in 3.1 going. The author's commas (3.1, 4.1, 4.6) are dropped.
- **Pluta (4.4)**: व्यद्युतदा३ and न्यमीमिषदा३, the prolonged ā with the figure 3 as the book prints it (its footnote mark after the first is the author's).
- **ॐ** is written with the sign ॐ, the book's `om̐`.
- **Candrabindu** (चक्षूँषि, मीमाँस्यम्, तस्मिँस्त्वयि, अपीदँ, उमाँ, ताँहोवाच, अभीक्ष्णँ): kept where the book's IAST has `m̐`.
- **The library's writing standard** (docs/PLAYBOOK.md §3) is applied by the exporter: a nasal before a stop as its class letter (सङ्कल्पः, संवाञ्छन्ति), a final म् at a pause (दग्धुम् ।), ॐ, and the ISO 15919 transliteration `t` made from the verse.

## Meanings
Our Hindi and English follow Śaṅkara's padabhāṣya. The readings settled while writing them:
- **2.1–2.2, the speakers.** The teacher's words end at मीमाँस्यमेव ते ("it is still to be inquired into by you"); मन्ये विदितम् is the disciple's reply after reflecting, and he goes on in 2.2 ("I know, and I do not know": Śaṅkara reads वेद च as "and I do not know too").
- **2.3–2.5, the speaker.** From यस्यामतं the Upaniṣad speaks in its own voice, leaving the dialogue of teacher and disciple (Śaṅkara), so 2.3 opens "The Upaniṣad says:".
- **4.2, प्रथमो विदाञ्चकार with the plural ते.** Śaṅkara glosses प्रथमः as प्रथमाः and the verb as viditavantaḥ: the three gods were the first to know it.
- **4.2–4.3, इव in अतितरामिव.** Śaṅkara takes इव as without meaning or emphatic, so the meaning says "far above the other gods", with no "as it were".
- **4.5, the construction.** The mind's seeming to go to Brahman, the seeker's remembering it again and again by the mind, and the mind's resolve are the teaching with regard to the self (Śaṅkara); the reading of the mind as a likeness of Brahman is not taken.
- **4.8, प्रतिष्ठा वेदाः सर्वाङ्गानि.** Śaṅkara's first reading in the meaning (austerity, self-restraint and rites are the foundation, and so are the Vedas and all their auxiliary sciences); his second (the three its feet, the Vedas its other limbs) in the footnote.

## Open
- None.
