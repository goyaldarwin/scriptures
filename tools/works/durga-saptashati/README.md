# श्रीदुर्गासप्तशती (Shri Durga Saptashati)

Shelf: हिन्दू धर्म › ग्रन्थ › महर्षि वेदव्यास › श्रीदुर्गासप्तशती (`library/hinduism/granth/vyasa/durga-saptashati/`, work id `durga-saptashati`). The Devī Māhātmya of the Mārkaṇḍeya Purāṇa, the sage Medhas's account to King Suratha and the merchant Samādhi of the Devī's three deeds, as Mārkaṇḍeya tells it: 13 adhyāyas, 700 mantras, in Sanskrit (`sa`), with the stotras recited before and after it in the owner's recording.

| Part | Items | Part | Mantras | Part | Mantras |
|---|---|---|---|---|---|
| श्रीचण्डिकाध्यान | 4 dhyānas | 3 महिषासुरवध | 44 | 10 शुम्भवध | 32 |
| अर्गलास्तोत्र | 27 ślokas | 4 शक्रादिस्तुति | 42 | 11 नारायणीस्तुति | 55 |
| कीलकस्तोत्र | 16 ślokas | 5 देवीदूतसंवाद | 129 | 12 भगवतीवाक्य | 41 |
| देवीकवच | 61 ślokas | 6 धूम्रलोचनवध | 24 | 13 सुरथवैश्यवरप्रदान | 29 |
| 1 मधुकैटभवध | 104 | 7 चण्डमुण्डवध | 27 | अपराधक्षमापणस्तोत्र | 9 ślokas |
| 2 महिषासुरसैन्यवध | 69 | 8 रक्तबीजवध, 9 निशुम्भवध | 63, 41 | देवीसूक्त | 8 ṛcs |

## Sources
- **Text:** the owner's copy of sanskritdocuments.org's *Devī Māhātmyam or Durgā Saptaśatī* (https://sanskritdocuments.org/doc_devii/durga700.html: a JSON of the page, 19 sections in Devanagari and IAST with each section's colophon), in `scriptures-data` at `printouts/sanskritdocuments/durga-saptashati.json`. `source/make_text.py` makes `text.txt` from it; `source/corrections.json` holds every change, each with its reason (`reconciliation.md`).
- **Witness and guide:** the owner's Gita Press *Śrīdurgāsaptaśatī* with Hindi translation (code 118; © Gita Press), in `scriptures-data` at `books/gitapress/sanskrit-hindi.pdf`. Its text layer is the Chanakya font, read without OCR by `source/gitapress.py` (with `tools/works/valmiki-ramayana/source/chanakya.py`) into `source/witness/gitapress.json`, the Sanskrit of its 700 mantras, compared word for word with the text by `source/compare.py` (`source/witness/differences.json`, `reconciliation.md`). Its stotras (Kavaca, Argalā, Kīlaka) are another recension than the copy's, so they are not compared word for word. It has no word-by-word meanings; it is used to check our word meanings and meanings, and nothing of its Hindi is copied.
- **Hindi and English meaning** (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`, ours, "भावार्थ — शास्त्र" / "English meaning — Scriptures", shown first): the owner's drafts in the same JSON, written from each verse with Claude, brought to `tools/meanings/style.md` by `source/meanings.py`: a mantra that is only a speaker's line (ऋषिरुवाच ॥) has one meaning from one table ("मेधा ऋषिने कहा —" / "The sage Medhas said:"); the triple namaskāras of adhyāya 5 are one refrain, the same every time; the Devī, addressed by those who praise her, is आप with honorific verbs; square brackets gone, their words in the sentence; Hindi postpositions joined, ये spellings (लिये, गये, किये), ! after an address; "the Devī" in English. `source/meaning_fixes.json` replaces a draft where a rule cannot, with its reason (nine English sentences reworded, wording only, where they shared ten or more words with Pargiter). The closing words of each adhyāya and stotra are ours, in one pattern. Like the Bhagavad Gītā's, these stand until a reviewed meaning replaces them (`docs/PLAYBOOK.md` §4).
- **English meaning copied:** F. E. Pargiter, *The Mārkaṇḍeya Purāṇa*, Bibliotheca Indica, 1904, cantos 81–93 (`meanings/en/pargiter.json`, "F. E. Pargiter — English meaning"), public domain, from the owner's copy (archive.org's scan, corrected and divided by mantra), as given. A passage for several mantras sits under the last of them, as the Mānas's joint meanings do; the stotras have none.
- **Word meanings** (`glossary/sa.json`, the work's own; Hindi and English): the drafts' word-by-word glosses, lined up with the words as the verse prints them and gathered per word by `source/words.py` (the Bhagavad Gītā's method); a word the shared dictionary has is left to it. The colophons' words and the pieces of compounds a line breaks have our own entries (`source/words_ours.json`), from Monier-Williams and Apte. Root and grammar are not written yet.

## Sources and permissions
The Sanskrit text is public domain (sanskritdocuments.org: for personal study and research). Pargiter (1904) is public domain. The Gita Press book is the owner's copy, used only to check facts; nothing of it is published. No permission has been requested from sanskritdocuments.org.

## Structure
- **Hierarchy:** nineteen parts, in the order the recording sings them: the Caṇḍikā-dhyāna, the Argalā, Kīlaka and Kavaca stotras (marked ॐ in the list of parts), the 13 adhyāyas (keys `1` … `13`, marked 1 … 13 and named by their deed), the Aparādha-kṣamāpaṇa stotra and the Devī Sūkta (marked ॐ) › one section each, named (`work.json` → `sections`: "Adhyay 1", "Argala Stotram") › items.
- **Numbering:** a mantra's id is adhyāya.mantra (`1.47`), its `n` the number that ends it (॥४७॥), as Gita Press numbers the 700: each speaker's line (ऋषिरुवाच ॥१॥) is a mantra of its own, and each triple namaskāra of adhyāya 5 (या देवी सर्वभूतेषु … नमस्तस्यै ॥१४॥ नमस्तस्यै ॥१५॥ नमस्तस्यै नमो नमः ॥१६॥) is three. It is cited adhyāya.mantra (`work.json` → `cite`: `["part", "n"]`, "Mantra 1.47"). A stotra's verse is `<stotra>.<n>` (`argala.3`), cited by its own number ("Shloka 3", "Richa 3").
- **Items without a number:** a section's viniyoga (`<section>.viniyoga`), its dhyāna (`<section>.dhyana`; the opening Caṇḍikā-dhyāna's four are `dhyana.1` … `dhyana.4`), ॐ नमश्चण्डिकायै (`<section>.namah`), the repeat of 13.28–29 that closes the Māhātmya with क्लीं ॐ (`13.end`), and each section's colophon (`<section>.iti`), its last item.
- **Types:** `mantra` (the adhyāyas' 700, and the unnumbered ॐ नमश्चण्डिकायै and `13.end`); `shloka` (the stotras); `rc` (the Devī Sūkta's ṛcs, Ṛgveda 10.125); `dhyana`; `viniyoga`; `iti` (the colophon).
- **Lines:** one per half-śloka, one per pāda in the longer metres, as the copy has them; a compound the copy breaks across lines keeps its hyphen.
- **Topics:** none; each part is one page.
- **Plan:** the 7-day pāṭha of Gita Press's pāṭha-vidhi (one, two, one, four, two, one and two adhyāyas a day: 1, 2–3, 4, 5–8, 9–10, 11, 12–13); the opening stotras are read on the first day before adhyāya 1, the closing ones on the seventh after adhyāya 13.

## Audio
Braja Beats (`audio/braja-beats/`, YouTube `zmGU9QbLUVM`, 3 h 28 min): the whole pāṭha in the text's order, the colophons sung. Starts and ends from Meta's MMS forced aligner (`tools/audio/METHOD.md` steps 2–4; `aligned.md`: 93% within 1 s of the owner's 101 starts set by ear, against 27% for the transcript alone), the owner's own starts winning (`owner.json`); a draft until checked by ear. `fixes.md` has the starts checked by hand.

## How it is made
```bash
D=<clone of scriptures-data>/hinduism/granth/vyasa/durga-saptashati
J=$D/printouts/sanskritdocuments/durga-saptashati.json
python3 tools/works/durga-saptashati/source/make_text.py $J     # text.txt
python3 tools/works/durga-saptashati/source/meanings.py $J      # meanings/
python3 tools/works/durga-saptashati/source/words.py $J         # glossary/sa.json
python3 tools/works/durga-saptashati/source/gitapress.py $D/books/gitapress/sanskrit-hindi.pdf   # source/witness/gitapress.json
python3 tools/works/durga-saptashati/source/compare.py          # source/witness/differences.json
python3 tools/works/export.py durga-saptashati
```
They read the owner's copies from `scriptures-data`, so `regen_check.py` cannot run them: after changing a script or one of its data files, run it and diff what it writes.

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- The text itself and `reconciliation.md`: its parts and their order (the dhyāna, Argalā, Kīlaka and Kavaca before, the Aparādha-kṣamāpana and Devī-sūkta after), the 700 mantras counted with the speakers' lines, the hymns' parts (Śakrādi-stuti, Nārāyaṇī-stuti), the seven-day plan; the README: the recording recites the stotras in that order.
- Wikipedia, "Devi Mahatmya" (https://en.wikipedia.org/wiki/Devi_Mahatmya, and its mirrors): Mārkaṇḍeya Purāṇa chapters 81–93, the names Durgā Saptaśatī and Caṇḍī Pāṭha, 700 verses in 13 chapters, its place in Shaktism, the frame story (Suratha, Samādhi, Medhas), the three episodes and their goddesses (chapter 1 Mahākālī, 2–4 Mahālakṣmī, 5–13 Mahāsarasvatī), its reading at Navarātri; hindutone.com, "Devi Mahatmya … Complete Guide": the limbs (Kavaca, Argalā, Kīlaka) recited with it.
