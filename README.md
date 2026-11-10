# शास्त्र · Scriptures

A personal, ad-free library for studying scriptures. Each work has the same reading experience: verses with their meanings from selectable sources, word-by-word meanings, natural divisions, reading plans, bookmarks and notes, and hands-free recitation with audio from YouTube.

**Website:** https://scriptures.craadle.org/

| Shelf | Work | Edition |
|---|---|---|
| Granthas › Gosvāmī Tulasīdāsa | Śrī Rāmacaritamānasa: 7 kāṇḍas, 30-day and 9-day pārāyaṇa | Gita Press, Gorakhpur |
| Granthas › Gosvāmī Tulasīdāsa | Sundarakāṇḍa, with the Hanumān Chālīsā and the āratī | Gita Press (generated from the Mānas) |
| Granthas › Maharṣi Vedavyāsa | Śrī Durgā Saptaśatī (Devī Māhātmya): 13 adhyāyas, 700 mantras, with the Argalā, Kīlaka and Kavaca, the Aparādha-kṣamāpaṇa stotra and the Devī Sūkta | sanskritdocuments.org (the owner's copy), checked against Gita Press
| Stotras › Śrī Rāma | Śrī Rāma Rakṣā Stotram (Budha Kauśika): viniyoga, dhyāna, 38 ślokas | Vande Guru Paramparaam (video) |
| Chālīsā › 46 deities | 55 chālīsās: Śrī Gaṇeśa, Hanumān (with the Bajaraṅga Bāṇa), Rāma, Kṛṣṇa, Śiva, Durgā and her forms, the Navagrahas, the saints and folk deities … | ५१ चालीसा संग्रह आरतियों सहित (Randhir Prakashan, 2000), and Drik Panchang for those it lacks |
| Āratī › 52 deities | 99 āratīs, among them Śrī Rāmacandra Kṛpālu, Om Jaya Jagadīśa Hare, Om Jaya Śiva Oṅkārā, Om Jaya Gaṅge Mātā, Jaya Gaṇeśa Devā, the nine Durgās | the same book, Drik Panchang, and the owner's printouts and screenshots |
| Nāmāvalī › Bhagavān Viṣṇu | Śrī Viṣṇu Sahasranāma Stotram (Mahābhārata, Anuśāsana-parva): opening prayers, pūrva-pīṭhikā, nyāsa, dhyāna, 108 ślokas, uttara-pīṭhikā | vishnusahasranamam.in (the owner's PDF), checked against the critical edition |
| Nāmāvalī › Śrī Sathya Sai Bābā | Śrī Sathya Sai Aṣṭottara Śatanāmāvalī: the 108 names | Bhakti Bharat (the owner's PDF), checked against the Sathya Sai Organisation's list |
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

**Śrī Rāmacaritamānasa.** The verse text is in the public domain. The Hindi bhāvārtha (Hanumānprasād Poddār) and the English translation are © Gita Press, Gorakhpur, and are shown credited to Gita Press. Gita Press is the default source. Our own Hindi and English meanings cover every kāṇḍa except the Bāla-kāṇḍa (there only Bāla 17, the sorṭhā), as a second source. Audio: Pt. Kamlesh Upadhyay "Haripuri".

**Śrīmad Bhāgavata Mahāpurāṇa** (with the Śrīmad Bhāgavata Māhātmya). The Sanskrit text is in the public domain; it is read from the owner's Gita Press books (codes 26–27). The Hindi commentary (सरल हिन्दी व्याख्या) is © Gita Press, Gorakhpur, shown credited to Gita Press, the only meaning so far; permission has not been requested. Word meanings are not written yet. Six verses the e-book leaves out (10.33.17–22) are from vedabase.io and wisdomlib.org (`tools/works/bhagavata-purana/reconciliation.md`).

**Śrīmad Bhagavad Gītā.** The Sanskrit text is in the public domain; it follows the owner's copy of sanskritdocuments.org's text, checked word for word against the public-domain dataset github.com/gita/gita (`tools/works/bhagavad-gita/reconciliation.md`). Our own Hindi and English meanings (the owner's drafts, brought to the style sheet) are the default. The second and third English sources are Annie Besant's translation (4th edition, 1922) and K. T. Telang's (Sacred Books of the East, 1882), both in the public domain. The owner's copy of *Bhagavad-gītā As It Is* in Hindi (© The Bhaktivedanta Book Trust) is used only to check word meanings; nothing of it is included.

**Śrī Durgā Saptaśatī** (the Devī Māhātmya). The Sanskrit text is in the public domain; it follows the owner's copy of sanskritdocuments.org's text, checked word for word against the owner's Gita Press book (code 118) (`tools/works/durga-saptashati/reconciliation.md`). Our own Hindi and English meanings (the owner's drafts, brought to the style sheet) are the default. The second English source is F. E. Pargiter's translation of the Mārkaṇḍeya Purāṇa (Bibliotheca Indica, 1904), in the public domain. The Gita Press book (© Gita Press, Gorakhpur) is used only to check the text, word meanings and meanings; nothing of it is included.

**Sundarakāṇḍa** (a work of its own). Its text is generated from the Rāmacaritamānasa. Our own Hindi and English meanings are the default. Gita Press's meanings, generated from the Mānas (credited the same way), are the second source under ☰ › More settings › Sources. The Śrī Hanumān Chālīsā (Tulasīdāsa) and the āratī "आरती कीजै हनुमान लला की" are traditional texts in the public domain; their wording was settled from bhaktibharat.com, Kavita Kosh and Bharatkosh (`tools/works/sundarkand/reconciliation.md`). Audio: Pt. Ashwin Kumar Pathak.

**Śrī Rāma Rakṣā Stotram.** The text is in the public domain. Its text and transliteration follow the on-screen text of the Vande Guru Paramparaam video "Sri Rama Raksha Stotram" (YouTube `ZIDdE4SZAuw`, Kuldeep M. Pai). Our own Hindi and English meanings are the default. The second sources are the video's English meaning and the Hindi meaning from the web page "श्री राम रक्षा स्तोत्र हिंदी में अर्थ सहित" on स्तुति चालीसा संग्रह (Shiv, 12 April 2020); both are included for personal study, and permission from their publishers has not been requested. Audio: the same video.

**Bilvāṣṭakam.** A traditional stotra, in the public domain. The text is the owner's pasted text (the words of the Sounds of Isha recording), checked against the owner's printout of sanskritdocuments.org, N. Balasubramanian's *सार्थ बिल्वाष्टकम्*; every choice is in `tools/works/bilvashtakam/reconciliation.md`. Our own Hindi and English meanings are the default. The second English source is copied from that printout ("Meaning of the verse", N. Balasubramanian; the site says its texts are for personal study and research, not to be reposted for promotion or commercial use without permission); it is included for personal study, and permission has not been requested. Audio: Sounds of Isha (`6rJExE8HGVg`).

**Bhaja Govindam** (Ādi Śaṅkarācārya). The text is in the public domain. It follows the owner's printout of sanskritdocuments.org (*भज गोविन्दम्*), checked against the recording; every choice is in `tools/works/bhaja-govindam/reconciliation.md`. Our own Hindi and English meanings are the default. The second English source is copied from that printout (same terms as above); it is included for personal study, and permission has not been requested. Audio: Chinmaya Mission Boston (`xrNOEva86pA`).

**The āratīs** (Śrī Rāma, Hanumān, Viṣṇu, Śiva, Gaṅgā). Traditional texts, from the owner's printouts, screenshots and pasted text; every choice is in each work's `reconciliation.md` (`tools/works/<work>/`). The Hanumān āratī is taken from the Sundarakāṇḍa work. The meanings are our own; the two Mānas verses that close "Śrī Rāmacandra Kṛpālu" also carry Gita Press's meanings (same permission status as the Mānas). Audio: Mahendra Kapoor, Anuradha Paudwal, Satya Adhikari, Pt. Ashwin Kumar Pathak.

**The Nāmāvalī shelf.** The Viṣṇu Sahasranāma from the owner's printout of vishnusahasranamam.in, checked against the Mahābhārata critical edition and sanskritdocuments.org; the Sathya Sai 108 names from the owner's Bhakti Bharat printout, checked against the Sathya Sai Organisation's *108 Mirrors*; every choice in `reconciliation.md`. Meanings and word meanings our own. Audio: M. S. Subbulakshmi (Sahasranāma), and the owner's download of the 108 names.

**The Chālīsā and Āratī shelves** (Chālīsā Saṅgraha, Āratī Saṅgraha). Traditional texts. The base is the owner's book ५१ चालीसा संग्रह आरतियों सहित (Randhir Prakashan, Haridwar, 2000), read on its page images; where the book lacks a text, the owner's saved Drik Panchang page (Drik Panchang's collection is typed largely from the same book). Every reading is in each work's `reconciliation.md`; web sources were used only to settle a single doubtful reading. An āratī follows the version sung in its chosen recording, when it has one. The meanings and word meanings are our own; open questions are in `docs/reviews/<work>-doubts.jsonl`.

**Shirdi Dhūpa Āratī.** The verse text (Mādhava Aḍakara, Dāsagaṇu, Saint Nāmadeva, Mohinīrāja, Upāsanī Mahārāja, B. V. Deva, Vedic and traditional prayers) was settled by comparing two web printouts supplied by the owner (missionkuldevi.in and shirdisaibabakripa.org); see `tools/works/shirdi-sai-dhoop-aarti/reconciliation.md`. Our own Hindi and English meanings are the default and cover all 64 verses. The second English source is copied from the shirdisaibabakripa.org printout ("Shirdi Sai Baba Evening (Dhoop) Arati", by Manisha Rautela Bisht; the site states a Creative Commons Attribution-Noncommercial-No Derivative Works 2.5 licence) for every verse it translates, with only typos fixed. It is included for personal study, and permission has not been requested. The Śrī Guru-prasāda-yācanā-daśaka (B. V. Deva) is included at the owner's request. Audio: Pramod Medhi.

**Śrī Rudram** (Namakam and Chamakam, Taittirīya Saṃhitā 4.5 and 4.7). The Vedic text is in the public domain. Its Devanagari, with svaras, follows the owner's printouts of shlokam.org's pages "Rudram Namakam" and "Rudram Chamakam" (shlokam.org/shloka/rudram-namakam.htm, rudram-chamakam.htm). The text-layer repairs and two typo fixes are in `tools/works/shri-rudram/reconciliation.md`. The meanings are our own; shlokam.org's English is not included. The transliteration is made from the Devanagari. Audio: the Sri Sathya Sai Official channel's YouTube recordings (`GbQM33333xs` Namakam, `0Gap1jjn2EM` Chamakam), checked by ear by the owner.

**Kaṭha Upaniṣad.** The text is in the public domain. It is taken from the IAST of the owner's book, Swami Gurubhaktananda, *Katha Upanishad — A Leap into the Beyond* (The Sandeepany Experience), and checked against shlokam.org; every choice is in `tools/works/katha-upanishad/reconciliation.md`. The meanings are our own; the book's prose is not included. Audio: SMVedroad (`NQhdLn7FHwA`).

**Īśāvāsya Upaniṣad** (Śukla Yajurveda, Kāṇva Saṃhitā 40). The text is in the public domain. It follows the owner's printout of shlokam.org ("Isha Upanishad", https://shlokam.org/text/isha-upanishad.htm), checked against the standard Kāṇva text with sanskritdocuments.org as a second witness; every correction is in `tools/works/isha-upanishad/reconciliation.md`. The meanings are our own; nothing is copied from shlokam.org's translation or commentary. Audio: SMVedroad (`mzczDkOtk0k`).

**Māṇḍūkya Upaniṣad.** The text is in the public domain. It follows the owner's printout of sanskritdocuments.org; every choice is in `tools/works/mandukya-upanishad/reconciliation.md`. The meanings are our own. Audio: SMVedroad (`mZTo8OEhRpc`).

**Sri Guru Granth Sahib** (1,430 Angs). The Gurbani is in the public domain. The text comes from the Shabad OS database (`@shabados/database` 4.8.7, https://github.com/shabados/database), typed from the SGPC's 1,430-Ang edition: its Gurbani is marked public domain (Creative Commons Public Domain Mark 1.0), and what the Shabad OS team made or arranged (its typing, line division and the translations it compiled) is © Shabad OS, under Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0); the files made from it here are shared under the same licence. The text was checked word for word against the Gurbani printed in Prof. Sahib Singh's Sri Guru Granth Darpan and in the Faridkot Teeka (`tools/works/guru-granth-sahib/reconciliation.md`). The Japji Sahib and the Sukhmani Sahib are taken from their works. Commentary: the Faridkot Teeka (1883–1905, public domain), as typed in the Shabad OS database (CC BY-SA 4.0), also on the Japji Sahib and the Sukhmani Sahib. Introduction: Wikipedia, "Guru Granth Sahib".

**Sukhmani Sahib** (Guru Arjan Dev Ji, Sri Guru Granth Sahib, Ang 262–296). The Gurbani is in the public domain. The text and the English translation come from the owner's PDF "Sukhmani Sahib with phonetic transliteration & English translation, Gurmukhi" (K. Thind, 2003); its Gurmukhi, typed in a legacy font encoding, was converted to Unicode and checked as described in `tools/works/sukhmani-sahib/reconciliation.md`. Our own Punjabi, Hindi and English meanings are the default. The second English source is © its translator, Dr. Sant Singh Khalsa, and is included for personal study; permission has not been requested. Audio: Parminder Singh, published while the owner checks its times by ear.
