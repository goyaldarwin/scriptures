# Reconciliation: Śrīmad Bhagavad Gītā

The base is the owner's copy of sanskritdocuments.org's text (`README.md`). The witness is the Sanskrit of github.com/gita/gita (`data/verse.json`, public domain), compared with the base word for word after spacing, the avagraha and nasal spelling are set aside: 31 verses differ, and each is decided below. Where the witness alone differs, by a slip of its own (श्चशुराः, अथ चैत्, broken conjuncts), the base stands and nothing is listed. The data is in `source/corrections.json` and the rules in `source/make_text.py`.

## The copy's layout, read as the book prints it
- **Speaker lines** (श्रीभगवानुवाच, अर्जुन उवाच, सञ्जय उवाच, धृतराष्ट्र उवाच) are the first line of their verse, without the daṇḍa the copy gives them; the copy gives some as a field of the verse and some as its first line, here all alike. At 1.21 and 1.28 the copy gives अर्जुन उवाच in the middle of the śloka, where Sañjaya's half-line ends and Arjuna's words begin; it stays there.
- **Numbers.** The last line ends with the verse's number (॥४७॥), which the copy leaves out; adhyāya 13 has 35 ślokas, its first being Arjuna's question (प्रकृतिं पुरुषं चैव …), as the copy and the witness number it (701 in all).
- **Colophons.** Each adhyāya's ॐ तत्सदिति … is its last item (`<adhyāya>.iti`), ending ॥N॥ (the copy: ॥ N॥).
- **Variant readings** the copy lists for five verses are left out (`docs/PLAYBOOK.md` §2: fix, don't annotate); the copy's own reading stays, a valid reading of its edition: 1.8 सौमदत्तिस्तथैव च (variant सौमदत्तिर्जयद्रथः), 1.19 तुमुलोऽभ्यनुनादयन् (तुमुलो व्यनुनादयन्, the witness's), 1.44 नरके नियतं (नरकेऽनियतं, the witness's), 4.35 भूतान्यशेषेण (भूतान्यशेषाणि), 8.7 मामेवैष्यस्यसंशयः (संशयम्). At 2.64 the copy prints its variant in brackets in the line, (रागद्वेषवियुक्तैस्तु); it is left out and रागद्वेषविमुक्तैस्तु stays.
- **Left out, not being the Gītā's text:** the page's header lines (श्रीमद्भगवद्गीता, ॥ ॐ श्री परमात्मने नमः ॥, ॥ अथ श्रीमद्भगवद्गीता ॥) and the Viṣṇu dhyāna-śloka it prints after the text (शान्ताकारं भुजगशयनं …).
- **Characters.** Runs of spaces are one space (6.17, 11.16); the text is NFC.

## The Gītā Dhyānam
The nine verses are typed from the owner's printout of shlokam.org (`source/dhyana.txt`). Its text layer puts a space inside some words (फु ल्ल, कृ ष्णाय, कं स, वेलाकु ला, के शवः, यत्कृ पा, षट् पदै); each word is joined as the printout's own transliteration gives it (phullāravinda…, kṛṣṇāya …), and the letters then equal the printout's, all 985. Its readings stand: नानाख्यानककेशरं (केशर, the classical spelling of केसर, "filament"), पाण्डवै रणनदी (पाण्डवैः before र loses its visarga). The printout has no daṇḍas or numbers: a । ends each half-verse and ॥N॥ each verse, as in the Gītā.

## Verses
| Verse | The copy | Here | Why |
|---|---|---|---|
| 8.9 | …मणोरणीयंसमनुस्मरेद्यः | …मणोरणीयांसमनुस्मरेद्यः | अणीयांसम्, the accusative of अणीयस् ("subtler"); अणीयंसम् is not a word. The witness reads अणोरणीयांसम्, and the triṣṭubh needs the long syllable |
| 11.46 | …चक्रहस्तं / इच्छामि… | …चक्रहस्त- / मिच्छामि… | a word-final m before a vowel is joined to it (चक्रहस्तमिच्छामि, the witness's), written across the line with a hyphen as the copy itself does at 8.9 |
| 12.2 | …परयोपेताः ते मे… | …परयोपेतास्ते मे… | visarga before त is स् (उपेतास्ते); the witness agrees |
| 15.3 | …सुविरूढमूलं / असङ्गशस्त्रेण… | …सुविरूढमूल- / मसङ्गशस्त्रेण… | as 11.46 (सुविरूढमूलमसङ्गशस्त्रेण, the witness's) |
| 17.23 | ॐतत्सदिति… | ॐ तत्सदिति… | a missing space: ॐ is a word of its own, as in every colophon |
| colophon 15 | …श्रीकृष्णार्जुन संवादे… | …श्रीकृष्णार्जुनसंवादे… | an extra space; the compound as in the other seventeen colophons |
| colophon 18 | …नाम अष्टादशोऽध्यायः | …नामाष्टादशोऽध्यायः | the vowels joined by sandhi, as in नामाष्टमोऽध्यायः (8) and नामैकादशोऽध्यायः (11) |

## Readings where the witness differs and the base stays
| Verse | Base | Witness | Why the base stays |
|---|---|---|---|
| 1.19 | तुमुलोऽभ्यनुनादयन् | तुमुलो व्यनुनादयन् | both are readings of the text (the copy lists the witness's as its variant); the base's is valid |
| 1.44 | नरके नियतं | नरकेऽनियतं | the same |
| 4.29 | प्राणं प्राणेऽपानं | प्राण प्राणेऽपानं | the witness drops the anusvāra of प्राणम्, the object of जुह्वति |
| 8.7 | मामेवैष्यस्यसंशयः | …असंशयम् | the copy's own reading (it lists असंशयम् as its variant); both stand in the editions |
| 11.21, 11.28 | सुरसङ्घा विशन्ति, अभिमुखा द्रवन्ति | सुरसङ्घाः विशन्ति, अभिमुखाः द्रवन्ति | after ā a visarga before a voiced sound is dropped: the base has the sandhi right |
| 11.54 | शक्य अहमेवंविधोऽर्जुन, द्रष्टुं | शक्यमहम्…, दृष्टुं | शक्यः + अहम् gives शक्य अहम्; द्रष्टुम् is the infinitive (दृष्टुं is a slip) |
| 14.23 | इत्येवं | इत्येव | both are readings; the metre is the same |
| 15.4 | परिमार्गितव्यं यस्मिन् | परिमार्गितव्य यस्मिन् | the witness drops the anusvāra |
| 16.1, 16.20 | सत्त्वसंशुद्धिर्ज्ञान…, आसुरीं | …शुद्धिः ज्ञान…, असुरीं | the base has the sandhi; आसुरी, "demonic", as in 16.19 |
| 17.25 | मोक्षकाङ्क्षिभिः | मोक्षकाङ्क्षि | the witness drops the ending; the metre needs it |
| 18.68 | य इदं परमं गुह्यं | य इमं परमं गुह्यं | both are readings; इदं agrees with गुह्यम् |
| 2.64 | रागद्वेषविमुक्तैस्तु | रागद्वेषवियुक्तैस्तु | both are readings (the copy prints the witness's in brackets beside its own); the base's is valid |

## Readings of our meanings
Our meanings follow Śaṅkara's reading; where another well-known reading differs materially it is a footnote. The places where the writers and checkers weighed two readings, and what was settled:

| Verse | Settled reading | Why |
|---|---|---|
| dhyana.1 | अनुसन्दधामि: "I meditate on you again and again" | the received sense of the dhyāna verse; Monier-Williams and Apte's anu-sam-√dhā "to think of, aim at" is the same act, continued |
| dhyana.6 | Gāndhārī as the river's blue lotus | the text as printed (गान्धारी-); editions that read गान्धार- make it Śakuni |
| 1.18 | सर्वशः "all of them" | the plain sense with पृथक् पृथक् |
| 2.5 | अर्थकामान् describes the gurus ("though they seek their own gain") | an adjective beside गुरून्; Madhusūdana Sarasvatī |
| 2.44, 2.53 | समाधि as the mind (2.44) and the Self (2.53); विधीयते "is formed" | Śaṅkara; the sense "absorption" in the footnotes |
| 2.46 | the well and the flood: all a well serves is served where water floods everywhere, as all the Vedas serve is gained by the knower | Śaṅkara; the other reading in the footnote |
| 3.41 | प्रजहि "cast off" | Śaṅkara reads प्रजहिहि, "give up" (प्र + √हा); "slay" (प्र + √हन्, as जहि in 3.43) in the footnote |
| 5.11 | केवलैः "with the senses alone" | the plain sense of केवल with इन्द्रियैः |
| 5.14 | प्रभुः "the master" | the plain word; Śaṅkara's "the Self" and the reading "God" in the footnote |
| 5.20 | the second line describes the one of the first | Śaṅkara: the knower of Brahman, established in Brahman, should not rejoice … |
| 5.26 | अभितः "here and hereafter" | Śaṅkara (ubhayataḥ) |
| 9.32 | women, vaiśyas and śūdras are named beside "those of sinful birth", not as instances of it | the plain order of the words, and a line about a group of people is never made harsher than the verse (`tools/meanings/style.md` §2); Śaṅkara's reading in the footnote |
| 13.21 | कार्यकारण "effect and cause" | the text as printed; Śaṅkara explains this reading beside कार्यकरण |
| 13.31 | ब्रह्म सम्पद्यते "becomes Brahman" | Śaṅkara (brahmaiva bhavati); Monier-Williams sam-√pad "to become" |
| 14.7 | तृष्णासङ्गसमुद्भवम् "the source of craving and attachment" | Śaṅkara; Monier-Williams gives both senses of samudbhava |
| 14.20 | birth, death, old age and sorrows, four things | Śaṅkara takes the compound as a dvandva |
| 16.8 | अपरस्परसम्भूतम् "born of the union of man and woman" | Śaṅkara (with Telang and Besant); the word-by-word reading "not produced one by the other" in the footnote |
| 18.10 | अकुशल / कुशल "inauspicious / auspicious" action | the dictionary senses; Śaṅkara's sense (action from desire, which binds / obligatory action, which purifies) in the footnote |
| 18.16 | केवलम् "the pure Self" | Śaṅkara (kevalaṃ śuddham) |
| 18.28 | नैष्कृतिक "ruinous to others' livelihood" | Śaṅkara (paravṛtticchedanapara); the work's own word entry gives it beside the dictionaries' "dishonest" |

