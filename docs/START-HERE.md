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
| `tools/meanings/style.md` | how our meanings are written |
| `tools/works/README.md` | the format of a work's folder (`work.json`, `text.txt`, meanings, recordings) and the one exporter |
| `tools/works/<work>/README.md` | each work: its sources, files and structure; `reconciliation.md`: every difference from its sources and why |

## Two repositories, one hierarchy

| Repository | Visibility | What it holds |
|---|---|---|
| `goyaldarwin/scriptures` (this one) | public | the website, the library data made from the sources (text, meanings, word meanings, verse times), every script and intermediate file, the docs |
| `goyaldarwin/scriptures-data` | **private, always** | the raw sources that are not ours to publish: books, printouts, screenshots, recordings, reference dictionaries, each with a `<file>.meta.json` (see its README) |

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
| Śrī Rāmacaritamānasa (`granth/tulsidas/ramcharitmanas`) | Gita Press, complete; 30-day and 9-day plans with vidhi, āratī and visarjana | Gita Press (ours, the second source, written for the Araṇya-, Kiṣkindhā-, Sundara- and Uttara-kāṇḍas) | Pt. Kamlesh Upadhyay, live; the owner corrects times by ear |
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

## Open with the owner
- The questions in `docs/reviews/` (word senses; readings in the Rāma Rakṣā and the Sukhmani Sahib).
- The āratīs: recordings for आरती कीजे श्रीरामलला की and आरती कीजै रामचन्द्र जी की (the owner will share them); the "open" corrections in each āratī's `reconciliation.md`.
- Offered, not built: "⏹ End / ⏱ Next starts" buttons in the player for audio timing.
