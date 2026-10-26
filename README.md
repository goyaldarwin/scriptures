# शास्त्र · Scriptures

A personal, ad-free library for studying scriptures. Each work has the same reading experience: verses with their meanings from selectable sources, word-by-word meanings, natural divisions, reading plans, bookmarks and notes, and hands-free recitation with audio from YouTube.

**Website:** https://scriptures.craadle.org/

| Shelf | Work | Edition |
|---|---|---|
| Granthas › Gosvāmī Tulasīdāsa | Śrī Rāmacaritamānasa: 7 kāṇḍas, 30-day and 9-day pārāyaṇa | Gita Press, Gorakhpur |
| Granthas › Gosvāmī Tulasīdāsa | Sundarakāṇḍa, with the Hanumān Chālīsā and the āratī | Gita Press (generated from the Mānas) |
| Stotras › Śrī Rāma | Śrī Rāma Rakṣā Stotram (Budha Kauśika): viniyoga, dhyāna, 38 ślokas | Vande Guru Paramparaam (video) |
| Āratī › Śrī Rāma, Śrī Hanumān, Bhagavān Viṣṇu, Bhagavān Śiva, Mother Gaṅgā | Śrī Rāmacandra Kṛpālu, Āratī Kīje Śrī Rāmalalā Kī, Āratī Kījai Rāmacandra Jī Kī, Śrī Hanumānjī kī Āratī, Om Jaya Jagadīśa Hare, Om Jaya Śiva Oṅkārā, Śrī Gaṅgājī kī Āratī | the owner's printouts and screenshots |
| Āratī › Shirdi Sāī Bābā | Dhūpa Āratī (evening āratī): Marathi, Sanskrit, Hindi | Shirdi tradition |
| Veda › Kṛṣṇa Yajurveda › Saṃhitā | Śrī Rudram: Namakam and Chamakam, 11 + 11 anuvākas, with svaras | shlokam.org (printout) |
| Veda › Kṛṣṇa Yajurveda › Upaniṣads | Kaṭha Upaniṣad: 2 adhyāyas, 6 vallīs, 119 mantras | Swami Gurubhaktananda (Sandeepany) |
| Veda › Śukla Yajurveda › Upaniṣads | Īśāvāsya Upaniṣad: śānti pāṭha, 18 mantras | shlokam.org (printout) |
| Veda › Atharvaveda › Upaniṣads | Māṇḍūkya Upaniṣad: śānti pāṭha, 12 mantras | sanskritdocuments.org (printout) |
| Sikhism › Gurbāṇī › Guru Arjan Dev Ji | Sukhmani Sahib: 24 Ashtapadis, Gurmukhi | Sri Guru Granth Sahib, Ang 262–296 |

## What's where

```
index.html, sw.js, manifest.json    the website (GitHub Pages serves the repository root)   [generated]
app/                                 website code, styles, fonts, icons                      [generated]
privacy.html, CNAME, .well-known/    privacy policy, the site's domain, Android app links     [generated]
library/                             the scriptures, as data (docs/LIBRARY.md)
  index.json                           the shelf: tradition / genre / group… / work
  apps.json                            which shelves each store app shows
  glossary/                            word meanings, one dictionary per language (sa, awa, hi, mr, bra, pa) + languages.json
  <tradition>/<genre>/<group…>/<work>/ one folder per work, e.g. hinduism/granth/tulsidas/ramcharitmanas/:
    work.json                          verses and numbers, parts, topics, plans
    meanings/<source>.json             one file per meaning source (hi-gitapress, en-scriptures, …)
    audio/<source>.json                one file per reciter: YouTube video ids + verse times   [generated]
    glossary.json                      optional: this work's own word senses
apps/                                the Android app (docs/APPS.md)
docs/
  START-HERE.md                      resume the project in a new session; the state of each work
  PLAYBOOK.md                        the owner's preferences and rules
  HOW-TO.md                          add a work, a meaning source or a reciter; fix text; change the app
  LIBRARY.md                         the data format and its rules
  ROADMAP.md                         what to build next
  APPS.md                            the store apps
  design/                            designs of features, built and not yet built
  store/                             store listings
  reviews/                           open questions for the owner
tools/                               everything that makes the data and the website (tools/README.md)
  site/  audio/  meanings/  store/  fonts/  works/<work id>/
dist/                                single-file builds (not committed)                       [generated]
```

## Raw sources

Books, printouts, screenshots and recordings live in the private repository `goyaldarwin/scriptures-data`, at the same path as each work (see `docs/START-HERE.md`).

## Sources and permissions

Meanings marked "Scriptures" (`hi-scriptures`, `en-scriptures`, `pa-scriptures`) and all word meanings were written for this library. They are written from the verse and its words (`tools/meanings/style.md`), and checked with `tools/meanings/overlap.py` so that no sentence is copied from a published translation. No audio is stored in this repository: it plays from published YouTube recordings.

**Śrī Rāmacaritamānasa.** The verse text is in the public domain. The Hindi bhāvārtha (Hanumānprasād Poddār) and the English translation are © Gita Press, Gorakhpur, and are shown credited to Gita Press. Gita Press is the default source. Our own Hindi and English meanings cover the Sundara-kāṇḍa, the close of the Kiṣkindhā-kāṇḍa and Bāla 17, as a second source. Audio: Pt. Kamlesh Upadhyay "Haripuri".

**Sundarakāṇḍa** (a work of its own). Its text is generated from the Rāmacaritamānasa. Our own Hindi and English meanings are the default. Gita Press's meanings, generated from the Mānas (credited the same way), are the second source under ☰ › More › Sources. The Śrī Hanumān Chālīsā (Tulasīdāsa) and the āratī "आरती कीजै हनुमान लला की" are traditional texts in the public domain; their wording was settled from bhaktibharat.com, Kavita Kosh and Bharatkosh (`tools/works/sundarkand/reconciliation.md`). Audio: Pt. Ashwin Kumar Pathak.

**Śrī Rāma Rakṣā Stotram.** The text is in the public domain. Its text and transliteration follow the on-screen text of the Vande Guru Paramparaam video "Sri Rama Raksha Stotram" (YouTube `ZIDdE4SZAuw`, Kuldeep M. Pai). Our own Hindi and English meanings are the default. The second sources are the video's English meaning and the Hindi meaning from the web page "श्री राम रक्षा स्तोत्र हिंदी में अर्थ सहित" on स्तुति चालीसा संग्रह (Shiv, 12 April 2020); both are included for personal study, and permission from their publishers has not been requested. Audio: the same video.

**The āratīs** (Śrī Rāma, Hanumān, Viṣṇu, Śiva, Gaṅgā). Traditional texts, from the owner's printouts, screenshots and pasted text; every choice is in each work's `reconciliation.md` under `tools/works/aartis/`. The Hanumān āratī is taken from the Sundarakāṇḍa work. The meanings are our own; the two Mānas verses that close "Śrī Rāmacandra Kṛpālu" also carry Gita Press's meanings (same permission status as the Mānas). Audio: Mahendra Kapoor, Anuradha Paudwal, Satya Adhikari, Pt. Ashwin Kumar Pathak.

**Shirdi Dhūpa Āratī.** The verse text (Mādhava Aḍakara, Dāsagaṇu, Saint Nāmadeva, Mohinīrāja, Upāsanī Mahārāja, B. V. Deva, Vedic and traditional prayers) was settled by comparing two web printouts supplied by the owner (missionkuldevi.in and shirdisaibabakripa.org); see `tools/works/shirdi-sai-dhoop-aarti/reconciliation.md`. Our own Hindi and English meanings are the default and cover all 64 verses. The second English source is copied from the shirdisaibabakripa.org printout ("Shirdi Sai Baba Evening (Dhoop) Arati", by Manisha Rautela Bisht; the site states a Creative Commons Attribution-Noncommercial-No Derivative Works 2.5 licence) for every verse it translates, with only typos fixed. It is included for personal study, and permission has not been requested. The Śrī Guru-prasāda-yācanā-daśaka (B. V. Deva) is included at the owner's request. Audio: Pramod Medhi.

**Śrī Rudram** (Namakam and Chamakam, Taittirīya Saṃhitā 4.5 and 4.7). The Vedic text is in the public domain. Its Devanagari, with svaras, follows the owner's printouts of shlokam.org's pages "Rudram Namakam" and "Rudram Chamakam" (shlokam.org/shloka/rudram-namakam.htm, rudram-chamakam.htm). The text-layer repairs and two typo fixes are in `tools/works/shri-rudram/reconciliation.md`. The meanings are our own; shlokam.org's English is not included. The transliteration is made from the Devanagari. Audio: shlokam.org's YouTube recordings (`GbQM33333xs`, `0Gap1jjn2EM`), a draft until its times are checked by ear.

**Kaṭha Upaniṣad.** The text is in the public domain. It is taken from the IAST of the owner's book, Swami Gurubhaktananda, *Katha Upanishad — A Leap into the Beyond* (The Sandeepany Experience), and checked against shlokam.org; every choice is in `tools/works/katha-upanishad/reconciliation.md`. The meanings are our own; the book's prose is not included. Audio: SMVedroad (`NQhdLn7FHwA`).

**Īśāvāsya Upaniṣad** (Śukla Yajurveda, Kāṇva Saṃhitā 40). The text is in the public domain. It follows the owner's printout of shlokam.org ("Isha Upanishad", https://shlokam.org/text/isha-upanishad.htm), checked against the standard Kāṇva text with sanskritdocuments.org as a second witness; every correction is in `tools/works/isha-upanishad/reconciliation.md`. The meanings are our own; nothing is copied from shlokam.org's translation or commentary. Audio: SMVedroad (`mzczDkOtk0k`).

**Māṇḍūkya Upaniṣad.** The text is in the public domain. It follows the owner's printout of sanskritdocuments.org; every choice is in `tools/works/mandukya-upanishad/reconciliation.md`. The meanings are our own. Audio: SMVedroad (`mZTo8OEhRpc`).

**Sukhmani Sahib** (Guru Arjan Dev Ji, Sri Guru Granth Sahib, Ang 262–296). The Gurbani is in the public domain. The text and the English translation come from the owner's PDF "Sukhmani Sahib with phonetic transliteration & English translation, Gurmukhi" (K. Thind, 2003); its Gurmukhi, typed in a legacy font encoding, was converted to Unicode and checked as described in `tools/works/sukhmani-sahib/reconciliation.md`. Our own Punjabi, Hindi and English meanings are the default. The second English source is © its translator, Dr. Sant Singh Khalsa, and is included for personal study; permission has not been requested. Audio: Parminder Singh, a draft until its times are checked by ear.
