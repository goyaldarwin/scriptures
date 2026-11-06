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
| `docs/HOW-TO.md` | step-by-step procedures: add a work, a meaning source, a recording; fix a text; change the app |
| `docs/LIBRARY.md` | the data format (`library/`), field by field |
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

- The verse and its number are the core of each work. Meanings (Hindi, English, Punjabi) and recordings are selectable sources; word meanings are one dictionary per language (`library/glossary/<lang>.json`), each verse looked up in its own language.
- The app is the same for every work: the library, the work's home (parts, plans, ▶), and a continuous reader. Bookmarks, notes, progress and hands-free playing are built in; readers' data stays on their phone.
- The working rules (branches, tests, merging, the environment) are in `docs/PLAYBOOK.md` §10.

## Status of the works

| Work (shelf path under `hinduism/` or `sikhism/`) | Text | Meanings shown first | Recording |
|---|---|---|---|
| Śrī Rāmacaritamānasa (`granth/tulsidas/ramcharitmanas`) | Gita Press, complete; 30-day and 9-day plans with vidhi, āratī and visarjana | Gita Press (ours, the second source, written for every kāṇḍa but the Bāla-kāṇḍa) | Pt. Kamlesh Upadhyay, live; the owner corrects times by ear; 136 starts where Meta's MMS aligner disagrees by more than 5 s are on the to-check list (`check.json`) |
| Sundarakāṇḍa (`granth/tulsidas/sundarkand`) | from the Mānas, plus opening prayers, Hanumān Chālīsā, āratī | ours | Pt. Ashwin Kumar Pathak, live |
| Śrī Rāma Rakṣā Stotram (`stotra/rama/ramraksha`) | a video's on-screen text | ours | Vande Guru Paramparaam, live |
| Bilvāṣṭakam (`stotra/shiva/bilvashtakam`) | the owner's pasted text, checked against sanskritdocuments.org | ours | Sounds of Isha, live (it does not sing śloka 2 or the phalaśruti) |
| Bhaja Govindam (`stotra/krishna/bhaja-govindam`) | sanskritdocuments.org, checked against the recording | ours | Chinmaya Mission Boston, live (verse 13अ is not sung) |
| Āratīs of Śrī Rāma: श्रीरामचन्द्र कृपालु, आरती कीजे श्रीरामलला की, आरती कीजै रामचन्द्र जी की (`aarti/rama/…`) | one printout; corrections open | ours | the stuti: Satya Adhikari, live; the other two: none yet |
| Hanumān āratī (`aarti/hanuman/hanuman-aarti`) | from the Sundarakāṇḍa | ours | the Sundarakāṇḍa's, live |
| ॐ जय जगदीश हरे (`aarti/vishnu/jagdish-aarti`) | the owner's pasted text | ours | Mahendra Kapoor, live |
| ॐ जय शिव ओंकारा (`aarti/shiva/shiv-aarti`) | Anuradha Paudwal's version, from four written witnesses | ours | Anuradha Paudwal, live |
| ॐ जय गंगे माता (`aarti/ganga/ganga-aarti`) | the owner's screenshot | ours | Anuradha Paudwal, live |
| Shirdi Sāī Dhūpa Āratī (`aarti/shirdi-sai/dhoop-aarti`) | two printouts reconciled | ours | Pramod Medhi (Times Music), live |
| Śrī Rudram (`veda/yajurveda/krishna-yajurveda/samhita/shri-rudram`) | shlokam.org, with Vedic accents | ours | Sri Sathya Sai Official, live; checked by ear by the owner |
| Kaṭha Upaniṣad (`veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad`) | the owner's Sandeepany book, checked word for word against his sanskritdocuments.org copy and shlokam.org | ours | SMVedroad, live |
| Īśāvāsya Upaniṣad (`veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad`) | shlokam.org | ours | SMVedroad, live |
| Māṇḍūkya Upaniṣad (`veda/atharvaveda/upanishad/mandukya-upanishad`) | sanskritdocuments.org; the svasti lines confirmed by shlokam.org | ours | SMVedroad, live |
| Sukhmani Sahib (`gurbani/guru-arjan-dev/sukhmani-sahib`) | the owner's PDF (Gurmukhi) | ours (Hindi, English, Punjabi) | Parminder Singh, live; 207 starts not yet set by ear are listed for the owner to check (`review`) |
| Śrīmad Vālmīki Rāmāyaṇa (`granth/valmiki/ramayana`) | Gita Press (codes 452–453), read from the Chanakya font without OCR, checked against IIT Kanpur and valmikiramayan.net; 23,701 verses; `source/make_text.py` writes `text.txt` from the PDF | Gita Press Hindi (code 77) and English with its 240 footnotes, copied; every word's meaning (the English IIT Kanpur's or valmikiramayan.net's gloss as given, else ours: `source/words/src.json`); loaded by kāṇḍa. To do: a check of the meanings written by us (16,526, Uttara's all) | none yet (the owner's list covers five kāṇḍas) |

## For a session to settle (PLAYBOOK §2: decide, never leave doubts for the owner)
- The readings still listed in `docs/reviews/` (the Mānas's that no reviewer has passed, the Rāma Rakṣā's, the Bilvāṣṭakam's, the Sukhmani Sahib's): settle each with the dictionaries and the grammar, apply it, and take it off its list.
- The Vālmīki Rāmāyaṇa's word meanings written by us (16,526 whole, about 8,600 in part; `tools/works/valmiki-ramayana/source/words/src.json`): a second check, Uttara first.

## Open with the owner
- The āratīs: recordings for आरती कीजे श्रीरामलला की and आरती कीजै रामचन्द्र जी की (the owner will share them); the "open" corrections in each āratī's `reconciliation.md`.
- The Sundarakāṇḍa's Hanumān Chālīsā and āratī: the sung words are still to be compared with the text (`tools/works/sundarkand/reconciliation.md`, "Still to do").
- Private copies not yet in `scriptures-data`: the Gaṅgā āratī screenshot, the jansatta.com printout of the Rāma āratīs, the Māṇḍūkya's sanskritdocuments.org and freepressjournal.in printouts and its recording.
- The Mānas timings: the owner is setting by ear the 136 starts MMS doubts (`tools/works/manas/audio/kamlesh-upadhyay/check.json`). Then compare his times with MMS's and the library's to decide whether MMS retimes, or lists for checking, the 1,108 verses where the two differ by more than 2 s (the experiment and its figures: `experiments/align/README.md` in `scriptures-data`).
- Names to confirm: the Dhūpa Āratī's section names (Aarti, Shirdi Majhe, Naman, Namasmaran, Namaskarashtak, Aisa Yei Ba, Mahimna, Dashak, Pushpanjali, Prarthana; `tools/works/shirdi-sai-dhoop-aarti/work.json` → `sections`), its padas called Stanza like every other āratī's, and the Mānas's closing ślokas as "Closing".
- Offered, not built: "⏹ End / ⏱ Next starts" buttons in the player for audio timing.
- Offered, not built: sending a listener's "Review audio timing" marks to the owner, as times are sent (marks stay on the phone they were made on).
