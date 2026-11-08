# Reconciliation: Śrī Śivamahāpurāṇa

The base is the owner's copy of sanskritdocuments.org's text, which follows Gita Press (codes 2223–2224) verse for verse (`README.md`). The witnesses are the owner's Gita Press scan of code 2223 (Māhātmya to Rudra-saṃhitā, Sanskrit with Hindi) and his scan of Kalyan's 2018 *Śrīśivamahāpurāṇāṅka* (Śatarudra- to Vāyavīya-saṃhitā, Hindi with verse numbers), read by eye where a check flags a place, and wisdomlib.org's *Shiva Purana [sanskrit]* (numbered as Gita Press). Every difference from the copy, and every choice made on it, is listed here; the data is in `source/corrections.json` and the rules in `source/make_text.py`.

## The copy's layout, read as the book prints it
- **Parts and adhyāyas.** The copy's twelve pages are the Māhātmya and the seven saṃhitās, the Rudra-saṃhitā in five khaṇḍas and the Vāyavīya in two; each khaṇḍa is a part here, as in the book's own division, and each adhyāya a section.
- **Speaker lines** (शौनक उवाच ।) are the first line of their verse, without the daṇḍa or dash the copy puts after them: the book prints them alone above the verse (scan p. 45). Typing slips in them are corrected (`corrections.json` → `speaker_lines`): उवाच् → उवाच, नारद् → नारद, सन्त्कुमार → सनत्कुमार, ऋष्य → ऋषय, ऋषि रुवाच → ऋषिरुवाच, दक्षवाच → दक्ष उवाच, उचुः → ऊचुः, a visarga left before a vowel against sandhi (मुनयः ऊचुः → मुनय ऊचुः; ईश्वरः, सनत्कुमारः, देवाः before उवाच / ऊचुः); at 2.2.1.1 the adhyāya's title (सतीसङ्क्षेपचरित्रवर्णनं) run into the speaker line is left out.
- **Half-verses split off at a speaker line.** Where a speaker's words begin in the middle of a śloka, the copy gives the first half without a number; the book prints the whole śloka as one verse, the speaker line above it (2.1.12.8 on scan p. 252: ब्रह्मोवाच / इति पृष्टास्तदा … / पुनः प्रणम्य … / विनिवेदयितुं … ॥ ८॥). Each such half joins the numbered verse after it, ending with । (43 places): 1.18.26, 2.1.12.8, 2.1.14.2, 2.1.17.8, 2.1.18.63, 2.2.5.43, 2.2.7.10, 2.2.12.36, 2.2.15.55, 2.2.19.76, 2.2.31.36, 2.2.34.22, 2.2.36.39, 2.2.39.4, 2.3.12.33, 2.3.22.4, 2.3.22.12, 2.3.24.1, 2.3.44.50, 2.3.51.12, 2.3.54.19, 2.4.2.12, 2.4.7.30, 2.4.19.9, 2.4.19.16, 2.4.19.50, 2.5.7.23, 2.5.13.44, 2.5.13.50, 2.5.14.12, 2.5.16.17, 2.5.22.49, 2.5.23.2, 2.5.30.27, 2.5.33.3, 2.5.42.33, 2.5.43.15, 4.13.41, 4.38.31, 5.3.30, 5.44.125, 5.46.47, 6.13.1.
- **Opening maṅgala-ślokas.** The copy numbers the opening śloka of 1.1 (आद्यन्तमङ्गल…) and 3.1 (वन्दे महानन्द…) 1, together with the verse that is 1; the book prints it without a number (scan p. 45). They are `1.1.0` and `3.1.0`.
- **Prose before an adhyāya's first verse**, without a number: Śukra's namaskāra (ॐ नमस्ते देवेशाय …, `2.5.49.0`; the book runs it on into verse 1 and gives the two one Hindi paragraph, ॥ १ ॥, scan p. 1026: here it is its own item, so each has its own meaning) and the list of mahāvākyas (`6.19.0`, numbered within the list, (१) … (२२), as the Kalyan scan prints it on p. 421: "सुब्रह्मण्य बोले — अब महावाक्योंको कहता हूँ — १-प्रज्ञानं ब्रह्म …"; the copy's quotation marks around अथ महावाक्यानि left out).
- **Numbers.** In the Umā- and Kailāsa-saṃhitā the copy writes every tenth verse's number as the whole reference (॥ ५.२६.१०॥); it is the verse's own number (10). Two dropped digits: 4.10.32 (printed ३, between 31 and 33) and 4.12.12 (printed १, between 11 and 13).
- **Pādas.** Where the copy puts two pādas of a long metre on one line with a comma between them (6.12.44–45, 6.23.34–36, 7.2.31.2), the comma starts a new line: one line per pāda.
- **Daṇḍas.** A verse's first half-śloka (16 syllables) that lacks its । gets it (16 places), as the book ends every half-śloka with ।; the last line ends with the verse's number, ॥N॥, by the library's standard; an opening maṅgala-śloka and a prose passage end with ॥.
- **Closing words.** Each adhyāya's इति … अध्यायः is its last item, numbered as the book prints it, by the adhyāya: ॥५॥ (the copy: ॥ ०.५॥). At 2.3.27 the copy takes them for a verse; they are the closing words here too.
- **Left out, not being the book's text:** the headers the copy prints over every adhyāya (॥ श्रीगणेशाय नमः ॥ ॥ श्रीगौरीशङ्कराभ्यां नमः ॥ …); its end-of-khaṇḍa lines (॥ इति श्रीशिवमहापुराणे … खण्डः समाप्तः, after 2.1.20, 2.2.43, 2.3.55, 2.4.20, 2.5.59) and end-of-saṃhitā lines; the headings अथ षष्ठी कैलाससंहिता प्रारभ्यते (6.1), अथ नन्दीश्वरावतारमाह (3.6.1) and अथ भैरवावतारमाह (3.8.1), where the book begins with the speaker (Kalyan scan pp. 72, 77); a proofreaders' credit (after 2.4.20); its variant readings (the two in its variant lists, and "(स भक्त्या)" in 6.8.35), by `docs/PLAYBOOK.md` §2: fix, don't annotate.
- **Characters.** Zero-width joiners (श‍ृ, a web font's workaround for शृ, 721 verses) are removed; the text is NFC.

## Verses
| Verse | The copy | Here | Why |
|---|---|---|---|
| 5.49.20 | missing (19 is followed by 21) | चरित्रमीदृशं यस्य तमेव शरणं श्रये । इति सञ्चिन्तयामास सहस्राक्षः पुनःपुनः ॥२०॥ | the Kalyan Hindi has the verse (॥ १९-२० ॥: "तब इन्द्रने बार-बार यह विचार किया कि जिसका ऐसा चरित्र है, मुझे उसीके शरणमें जाना चाहिये", scan p. 371); the text from wisdomlib.org, *Shiva Purana [sanskrit]* 9.49.20 (its book 9 is the Umā-saṃhitā), संचिन्तयामास written सञ्चिन्तयामास by the standard |
| 6.13.28 | … मयोत्पन्नं मुनीश्वर | … मायोत्पन्नं मुनीश्वर | a dropped ा: the Kalyan Hindi reads "ये पाँचों मायासे उत्पन्न हैं" (॥ २४-२८ ॥, scan p. 406), and 6.13.29 names Māyā as their source; the metre is the same |
| 6.14.20 | missing (19 is followed by 21) | सद्योजातम्प्रपद्यामीत्युपक्रम्य सदाशिवोम् । इति प्राह श्रुतिस्तारं ब्रह्मपञ्चकवाचकम् ॥२०॥ | the Kalyan Hindi has the verse (॥ १९-२० ॥: the five mantras from 'सद्योजातं प्रपद्यामि' to 'सदाशिवोम्' and their vācaka, the tāra, ॐ; scan p. 410); the text from wisdomlib.org, *Shiva Purana [sanskrit]* 6.14.20 (the owner's screenshot, in `scriptures-data`), पंच written पञ्च by the standard |
| 3.1.50 | the adhyāya's last verse, unnumbered | ॥५०॥ | the Kalyan Hindi numbers it ५० (scan p. 65) |
| 2.2.34.22 | धिक् जन्म तव दक्षाद्य महामूढोऽसि पापधीःस् | धिग् जन्म तव दक्षाद्य महामूढोऽसि पापधीः | as the book prints it (scan p. 460): a stray स्, and धिक् not assimilated before ज |
| 2.5.45.54 | एतद्वचस्तद्विधसोऽपि | एतद्वचस्तद्विघसोऽपि | the demon is Vighasa (2.5.46), as the book prints it here too (scan p. 1010) |
| 3.3.28 | मुने ।` | मुने । | a stray backtick |
| 4.17.26 | बहुश; | बहुशः | a semicolon typed for the visarga |
| 6.14.18 | … प्रणवे नव वेष्टयेत् । त-व | … प्रणवे नव वेष्टयेत् । | "त-व" is an editor's mark of the copy, not text; प्रणवे नव is wisdomlib.org's reading too (6.14.18) |


## Hindi meaning
Read from the owner's scans of Gita Press code 2223 (the Māhātmya to 2.5.59) and Kalyan 2018 (3.1 to 7.2.41) as `source/hindi/README.md` describes; each flagged word as the readers found it on the page is in `source/hindi/<book>.read.json`, each word the readers' whole lines set right in `<book>.lines.json`, each Kalyan paragraph proofread whole in `kalyan-2018.proof.json`, and each paragraph read on the page by hand in `source/hindi/corrections.json`.

| Place | Choice |
|---|---|
| 1.1.0, 2.1.1.1, 2.4.1.1, 2.5.49.0, 3.1.0 | The opening's Hindi stands under the title page and headings, which the OCR ran into it: the paragraph is read on the page (code 2223 pp. 45, 1025; Kalyan p. 63), or starts at its first words. Kalyan prints the maṅgala-śloka in Sanskrit above the Hindi; only the Hindi is kept, as for every other opening. |
| Code 2223 p. 322; Kalyan p. 291 | ह्रद (a lake: नाभि ह्रदके समान; ह्रदमें स्नान): the conjunct is this type's ह्र, the same glyph as in the Sanskrit निम्ननाभिह्रदां beside it. |
| 2.5.59 (pp. 1065–1068) | दुन्दुभिनिर्ह्लाद: the conjunct is the ह्ल of प्रह्लाद on the same page. |
| 6.22.13 | ह्रां ह्रीं ह्रूं ह्रैं ह्रौं ह्रः: each of the six bold bījas has the stroke of ह्र inside its bowl (Kalyan p. 430, read at 400 dpi). |
| 5.5.4, 6.12.3 | No paragraph: 5.5.4's verse is inside the ॥ ४-५ ॥ paragraph, and 6.12.3's inside ॥ ३-१३ ॥ (what stood there was a footnote's mantra lines). |
| 3.39.18, 3.29.10 | Left out: an ink blot covers a word (Kalyan p. 151, the word before शरीरसे; p. 125, the first letter of the word before दिये). |
| Verse marks | A range is written with a hyphen (॥ ३-५ ॥), as in the Bhāgavata's Hindi, where Kalyan prints a long dash in some; a half verse as ½. |
| Proofread whole | Every paragraph was then read against its page by eye (`source/hindi/<book>.full.json`: each change as the page has it, a paragraph given whole where much was wrong, and the paragraphs the adhyāya walk had missed). |
| Not yet carried | The books' footnotes (`source/hindi/<book>.notes.json` marks the lines left out); the Hindi of 2.1.14.87 and 7.2.31.126–132, which the proofreading did not place. |
