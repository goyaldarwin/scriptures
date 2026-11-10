# Start here

This repository holds everything about the scriptures library: the website, the data, every script that makes the data, and the rules. A new session can continue from it alone.

## Prompt to paste in a new session

> Clone github.com/goyaldarwin/scriptures and read `CLAUDE.md`, `docs/START-HERE.md`, `docs/PLAYBOOK.md`, `docs/HOW-TO.md` and `docs/LIBRARY.md` before doing anything. Then: **[the task]**. Follow the playbook. Each work's source of truth is the source I gave for it (see its README). Test at phone size (390×844) with screenshots. Commit and push when done, and tell me in plain words what changed.

## The documents

| File | What it is for |
|---|---|
| `CLAUDE.md` | the non-negotiables, in brief |
| `docs/START-HERE.md` | this page: the repositories, how the pieces fit, the status of each work, what is open |
| `docs/PLAYBOOK.md` | every rule and preference of the owner, by topic |
| `docs/HOW-TO.md` | step-by-step procedures: add a work, a meaning source, a commentary, a recording; fix a text; change the app |
| `docs/LIBRARY.md` | the data format (`library/`), field by field |
| `docs/WORKS.md` | every work side by side (made by the build, never edited): its levels, verse types, how a verse is cited, its meanings and recordings, and what is not yet the same in every work |
| `docs/ROADMAP.md` | work not done yet |
| `docs/APPS.md` | the store apps |
| `docs/reviews/` | open questions for the owner |
| `tools/meanings/style.md` | how our meanings are written (§1 first: from the verse, its word meanings, the dictionaries and its context in the work and the nearby verses; accuracy never traded away) |
| `tools/meanings/LINES-BRIEF.md` | the brief for dividing an existing meaning into one piece per verse line |
| `tools/meanings/briefs/` | the brief for each step of writing a kāṇḍa of the Mānas: writer, reviewer, copy auditor, accuracy checker, consistency pass (`docs/HOW-TO.md`) |
| `tools/README.md` | every script, folder by folder, and how to rebuild everything |
| `tools/audio/README.md` | the audio sources: how a recording is transcribed, aligned and timed |
| `tools/works/README.md` | the format of a work's folder (`work.json`, `text.txt`, meanings, recordings) and the one exporter |
| `tools/works/<work>/README.md` | each work: its sources, files and structure; `reconciliation.md`: every difference from its sources and why |

## Two repositories, one hierarchy

| Repository | Visibility | What it holds |
|---|---|---|
| `goyaldarwin/scriptures` (this one) | public | the website, the library data made from the sources (text, meanings, word meanings, verse times), every script and intermediate file (except the Sukhmani Sahib's Punjabi meaning records, whose batches quote copyrighted commentaries: they are in `scriptures-data` under `sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/meaning-records/`), the docs |
| `goyaldarwin/scriptures-data` | **private, always** | the raw sources that are not ours to publish: books, printouts, screenshots, recordings, reference dictionaries, each with a `<file>.meta.json` (see its README); `meaning-records/` under a work (our meaning batches that quote copyrighted commentaries); `experiments/` (alignment experiments) |

Both use the same address for a work, the shelf path the reader sees: `hinduism/granth/tulsidas/ramcharitmanas` is `library/hinduism/granth/tulsidas/ramcharitmanas/` here and `hinduism/granth/tulsidas/ramcharitmanas/` there. Under a work, the private repo groups files as `<kind>/<source-id>/<file>` (`books/gitapress/hindi.pdf`, `audio/kamlesh-upadhyay/…`); the source id is the one used here for the meaning or audio source made from it. Reference books shared by all works are under `reference/<lang>/…` there.

## How the pieces fit

```
the owner's sources (scriptures-data) ─ tools/works/<work>/ (source/ scripts → text.txt, meanings/) ─ tools/works/export.py ─► library/<path>/work.json, meanings/, glossary
recordings ─ transcription ─► tools/works/<work>/audio/<source>/transcripts ─ tools/audio/make_timings.py ─► library/<path>/audio/<source>.json
library/ ─ tools/site/build.py (checks everything first) ─► index.html, app/, sw.js, manifest.json  +  dist/ (offline file)
```

- The verse and its number are the core of each work. Meanings (Hindi, English, Punjabi), commentaries (off until the reader picks one) and recordings are selectable sources, footnotes coming with their meaning; word meanings are one dictionary per language (`library/glossary/<lang>.json`), each verse looked up in its own language.
- The app is the same for every work: the library, the work's home (parts, plans, ▶), and a continuous reader. Bookmarks, notes, progress and hands-free playing are built in; readers' data stays on their phone.
- The working rules (branches, tests, merging, the environment) are in `docs/PLAYBOOK.md` §10.

## Status of the works

| Work (shelf path under `hinduism/` or `sikhism/`) | Text | Meanings shown first | Recording |
|---|---|---|---|
| Śrī Rāmacaritamānasa (`granth/tulsidas/ramcharitmanas`) | Gita Press, complete; 30-day and 9-day plans with vidhi, āratī and visarjana | ours for every verse, and Gita Press (the second source) | Pt. Kamlesh Upadhyay, live; starts from Meta's MMS forced aligner (`aligned.json`), 637 set by the owner by ear; the 5 the aligner is unsure of are on the to-check list (`check.json`) |
| Sundarakāṇḍa (`granth/tulsidas/sundarkand`) | from the Mānas, plus opening prayers, Hanumān Chālīsā, āratī | ours | Pt. Ashwin Kumar Pathak, live: starts from MMS (91% within 1 s of the owner's 46, `aligned.md`); 207 listed to check |
| Śrī Rāma Rakṣā Stotram (`stotra/rama/ramraksha`) | a video's on-screen text | ours | Vande Guru Paramparaam, live |
| Bilvāṣṭakam (`stotra/shiva/bilvashtakam`) | the owner's pasted text, checked against sanskritdocuments.org | ours | Sounds of Isha, live (it does not sing śloka 2 or the phalaśruti) |
| Bhaja Govindam (`stotra/krishna/bhaja-govindam`) | sanskritdocuments.org, checked against the recording | ours | Chinmaya Mission Boston, live (verse 13अ is not sung) |
| Āditya Hṛdayam (`stotra/surya/aditya-hridayam`) | the owner's sanskritdocuments.org printout (the recitation text: viniyoga, nyāsas, 31 ślokas), checked word for word against the Gita Press sarga (Yuddha 105), IIT Kanpur and the recordings; the sarga's closing words that Braja Beats sings; every choice in `reconciliation.md` | ours | Sri Sathya Sai Official (default), Braja Beats and The Sanskrit Channel, live for review: starts from MMS (lean 0.6 s, not yet scored on the owner's ear), all on the to-check list until set by ear |
| श्रीरामचन्द्र कृपालु (`aarti/rama/shri-ramchandra-kripalu`) | the jansatta.com printout, its corrections confirmed by sanskritdocuments.org and shlokam.org | ours | Satya Adhikari, live |
| आरति श्रीरामायनजी की (`aarti/rama/ramayan-aarti`) | the Gita Press Mānas's āratī, taken from the Mānas's extraction by its generator; the Mānas's plans open it after their last day | ours | Pt. Kamlesh Upadhyay, the end of the Mānas's 30th day, live: starts checked in the transcript (MMS unsure over the harmonium, `aligned.md`) |
| आरती कीजे श्री रामलला की (`aarti/rama/ramlala-aarti`) | the words shown with Sohini Mishra's song (the owner's screenshot) | ours | Sohini Mishra, live |
| Hanumān āratī (`aarti/hanuman/hanuman-aarti`) | from the Sundarakāṇḍa | ours | the Sundarakāṇḍa's, live |
| ॐ जय जगदीश हरे (`aarti/vishnu/jagdish-aarti`) | the owner's pasted text | ours | Mahendra Kapoor, live |
| ॐ जय शिव ओंकारा (`aarti/shiva/shiv-aarti`) | Anuradha Paudwal's version, from four written witnesses | ours | Anuradha Paudwal, live |
| ॐ जय गंगे माता (`aarti/ganga/ganga-aarti`) | the owner's screenshot | ours | Anuradha Paudwal, live |
| Shirdi Sāī Dhūpa Āratī (`aarti/shirdi-sai/dhoop-aarti`) | two printouts reconciled | ours | Pramod Medhi (Times Music), live: starts from MMS (100% within 1 s of the owner's 53, `aligned.md`) |
| Śrī Rudram (`veda/yajurveda/krishna-yajurveda/samhita/shri-rudram`) | shlokam.org, with Vedic accents | ours | Sri Sathya Sai Official, live; checked by ear by the owner; starts from MMS (98% within 1 s of his 298, `aligned.md`) |
| Kaṭha Upaniṣad (`veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad`) | the owner's Sandeepany book, checked word for word against his sanskritdocuments.org copy and shlokam.org | ours | SMVedroad, live: starts from MMS (92% within 1 s of the owner's 62, `aligned.md`) |
| Īśāvāsya Upaniṣad (`veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad`) | shlokam.org | ours | SMVedroad, live |
| Māṇḍūkya Upaniṣad (`veda/atharvaveda/upanishad/mandukya-upanishad`) | sanskritdocuments.org; the svasti lines confirmed by shlokam.org | ours | SMVedroad, live |
| Śrīmad Bhagavad Gītā (`granth/vyasa/bhagavad-gita`) | sanskritdocuments.org's text (the owner's JSON), 18 adhyāyas, 701 ślokas, checked against github.com/gita/gita; the Gītā Dhyānam from shlokam.org; every choice in `reconciliation.md` | ours (Hindi, English): the owner's drafts brought to the style sheet, standing until reviewed meanings replace them; Besant and Telang (public domain) copied; word meanings (Hindi, English) from the drafts' word-by-word glosses, root and grammar to come | Voice of Rishis (`C5UHgA9C3kw`, the whole Gītā chanted, the default) and The Sanskrit Channel (`WITUOwi3EYk`, with a spoken meaning), both with the Gītā Dhyānam, live for review: starts from MMS (lean 0.6 s, not yet scored on the owner's ear), all on the to-check list until set by ear |
| Śrīmad Bhāgavata Mahāpurāṇa (`purana/mahapurana/bhagavata`) | Gita Press (codes 26–27), the Māhātmya and 12 skandhas, 14,603 verses, read from the e-book's glyph ids; 7-day Saptāha plan | Gita Press Hindi with the book's 185 notes, copied; Tagare's English with his footnotes (wisdomlib), copied and placed on the Gita Press verses by content; no word meanings yet (`"words": "partial"`) | Sanskrit Parayan, 30 recordings, published: starts from MMS (14,576 of 14,945 items; 94% within 1 s of the owner's 132 by-ear starts, `aligned.md`); the verses the checks flag on the to-check list |
| Śrī Śivamahāpurāṇa (`purana/mahapurana/shiva`) | sanskritdocuments.org's copy (the owner's JSON), which follows Gita Press (codes 2223–2224); the Māhātmya and 7 saṃhitās, 24,676 verses; checked on the owner's Gita Press and Kalyan scans by eye; two verses the copy drops (5.49.20, 6.14.20) from wisdomlib.org (`reconciliation.md`) | ours in English: the owner's drafts brought to the style sheet, standing until reviewed meanings replace them; English word meanings from his word-by-word glosses (`"words": "partial"`); Gita Press Hindi, copied, read from the owner's two scans by OCR (his choice for them): every flagged word read by eye, then every paragraph proofread against its page; adhyāya headings ours | none yet |
| Sri Guru Granth Sahib (`gurbani/guru-granth-sahib`) | the Shabad OS database (SGPC, 1,430 Angs), 51 parts, 5,767 verses of its own and the Japji and Sukhmani taken; checked word for word against the Darpan's and the Faridkot Teeka's Gurbani, one correction (Ang 608); loaded by part | none yet (Punjabi only, to come: the Shabdarth, then the Santhya); commentary: the Faridkot Teeka, line by line; no word meanings yet (`"words": "partial"`) | Bhai Pishora Singh Ji's Sahaj Paath (`pishora-singh`, 66 recordings of about an hour, the whole Granth), live: starts from MMS (lean 0.55 s, not yet scored on the owner's ear), 1,991 listed to check; five video titles give the wrong Angs (volumes 20, 39, 40, 51, 56), the Angs each reads in its `.meta.json` in `scriptures-data` |
| Japji Sahib (`gurbani/guru-nanak-dev/japji-sahib`) | the owner's SikhNet PDF (Gurmukhi), word for word as the Shabad OS database | ours (Hindi, English, Punjabi), line by line with notes | Nirvair Khalsa Jatha UK, live for review: starts from MMS (98% within 1 s of the owner's 41, `aligned.md`); the rest on the to-check list until set by ear |
| Sukhmani Sahib (`gurbani/guru-arjan-dev/sukhmani-sahib`) | the owner's PDF (Gurmukhi) | ours (Hindi, English, Punjabi) | Parminder Singh, live; 207 starts not yet set by ear are listed for the owner to check (`review`) |
| Śrīmad Vālmīki Rāmāyaṇa (`granth/valmiki/ramayana`) | Gita Press (codes 452–453), read from the Chanakya font without OCR, checked against IIT Kanpur and valmikiramayan.net; 23,701 verses; `source/make_text.py` writes `text.txt` from the PDF | Gita Press Hindi (code 77) and English with its 240 footnotes, copied; every word's meaning (the English IIT Kanpur's or valmikiramayan.net's gloss as given, else ours: `source/words/src.json`); loaded by kāṇḍa. the word meanings written by us checked against Monier-Williams and Apte (`source/words/check_ours.py`) | Sanatana Dharma Parayana, live: one video per sarga for Bāla, Ayodhyā, Araṇya, Sundara and Yuddha (467); Kiṣkindhā and Uttara have none yet; starts from MMS (`aligned.md`), found accurate by the owner's ear; the starts the checks flag are on the to-check list |
| Śrī Durgā Saptaśatī (`granth/vyasa/durga-saptashati`) | sanskritdocuments.org's text (the owner's JSON): the Caṇḍikā-dhyāna, Argalā, Kīlaka, Kavaca, 13 adhyāyas (700 mantras, numbered as Gita Press), Aparādha-kṣamāpaṇa, Devī Sūkta; checked word for word against the owner's Gita Press book (code 118), every choice in `reconciliation.md` | ours (Hindi, English): the owner's drafts brought to the style sheet, standing until reviewed meanings replace them; Pargiter (1904, public domain) copied; word meanings (Hindi, English) from the drafts' word-by-word glosses, root and grammar to come | Braja Beats (`zmGU9QbLUVM`), live: starts from MMS (93% within 1 s of the owner's 101), his own winning |

## For a session to settle (PLAYBOOK §2: decide, never leave doubts for the owner)
- Nothing open. A new work's or kāṇḍa's doubts go to `docs/reviews/` and are settled before its pull request is merged.

## To build next
- The timing method's fixes (`tools/audio/METHOD.md`, step 5: re-align between trusted neighbours, snap to the onset, spread and list); steps 2–4 run in the public `align` workflow.
- MMS on the recordings still timed from the transcript alone (`docs/WORKS.md`, last section): those whose MMS run waits for the owner's starts by ear to be scored (`mms/score.md` beside each: the Sukhmani Sahib's).

## Open with the owner
- Private copies that would complete `scriptures-data` (nothing depends on them; only the owner has them, from earlier chats): the Gaṅgā āratī screenshot, the jansatta.com printout of Śrī Rāmacandra Kṛpālu, the Māṇḍūkya's sanskritdocuments.org and freepressjournal.in printouts and its recording.
- Recordings missing from `scriptures-data`, so MMS cannot time them (`docs/WORKS.md`): the Māṇḍūkya's (SMVedroad), Śrī Rāmacandra Kṛpālu's (Satya Adhikari), and the Jagadīśa, Śiva and Gaṅgā āratīs' (Mahendra Kapoor, Anuradha Paudwal).
