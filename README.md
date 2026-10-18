# शास्त्र · Scriptures

A personal, ad-free library for studying scriptures. Each work has the same reading experience: verses with their meanings from selectable sources, word-by-word meanings, natural divisions, reading plans, bookmarks and notes, and hands-free recitation with audio from YouTube.

**Website:** https://goyaldarwin.github.io/scriptures/

| Shelf | Work | Edition |
|---|---|---|
| Gosvāmī Tulasīdāsa | Śrī Rāmacaritamānasa: 7 kāṇḍas, 30-day and 9-day pārāyaṇa | Gita Press, Gorakhpur |
| Stotras | Śrī Rāma Rakṣā Stotram (Budha Kauśika): viniyoga, dhyāna, 38 ślokas | Vande Guru Paramparaam (video) |
| Āratī › Shirdi Sāī Bābā | Dhūpa Āratī (evening āratī): Marathi, Sanskrit, Hindi | Shirdi tradition |

## What's where

```
index.html, sw.js, manifest.json    the website (GitHub Pages serves the repository root)   [generated]
app/                                 website code, styles, fonts                              [generated]
library/                             the scriptures, as data
  index.json                           the shelf: tradition / genre / group… / work (docs/LIBRARY.md §1)
  glossary/                            word meanings, one dictionary per language (sa, awa, …) + languages.json
  hinduism/granth/tulsidas/ramcharitmanas/
    work.json                          verses + numbers, kāṇḍas, topics, plans, pārāyaṇa vidhi
    meanings/hi-gitapress.json         a Hindi meaning source
    meanings/en-gitapress.json         an English meaning source
    audio/kamlesh-upadhyay.json        an audio source: YouTube video ids + verse timings     [generated]
  hinduism/stotra/rama/ramraksha/                  Śrī Rāma Rakṣā Stotram: work.json, meanings/, audio/
  hinduism/aarti/shirdi-sai/dhoop-aarti/   the Shirdi Sāī Bābā evening āratī (work.json, meanings/, audio/)
docs/
  START-HERE.md                      resume the project in a new session
  HOW-TO.md                          add a work, a meaning source or a reciter; fix text; change the app
  LIBRARY.md                         the data format and its rules
  PLAYBOOK.md                        the owner's preferences, decisions and lessons
  ROADMAP.md                         what keeps the library sustainable, and what to build next
tools/                               everything that makes the data and the website (see tools/README.md)
  site/  audio/  fonts/  works/ramcharitmanas/  works/ramraksha/  works/shirdi-sai-dhoop-aarti/
```

## Raw sources

Books, printouts, screenshots and recordings live in the private repository `goyaldarwin/scriptures-data`, at the same path as each work (see `docs/START-HERE.md`).

## Sources and permissions

The verse text of the Rāmacaritamānasa is in the public domain. The Hindi bhāvārtha (Hanumānprasād Poddār) and the English translation are © Gita Press, Gorakhpur, and are included here for personal study while permission from Gita Press is requested. Audio plays from the published YouTube recordings of Pt. Kamlesh Upadhyay "Haripuri"; no audio is stored in this repository.

The text of the Śrī Rāma Rakṣā Stotram is in the public domain. Its text, transliteration and English meaning follow the on-screen text of the Vande Guru Paramparaam video “Sri Rama Raksha Stotram” (YouTube `ZIDdE4SZAuw`, Kuldeep M. Pai); the Hindi meaning is from the web page “श्री राम रक्षा स्तोत्र हिंदी में अर्थ सहित” on स्तुति चालीसा संग्रह (Shiv, 12 April 2020). Both meanings are included for personal study; permission from their publishers has not been requested. Audio plays from the same YouTube video.

The Shirdi Dhūpa Āratī: the verse text (Mādhava Aḍakara, Dāsagaṇu, Saint Nāmadeva, Mohinīrāja, Upāsanī Mahārāja, B. V. Deva, Vedic and traditional prayers) was settled by comparing two web printouts supplied by the owner (missionkuldevi.in and shirdisaibabakripa.org); see `tools/works/shirdi-sai-dhoop-aarti/reconciliation.md`. The default English meaning is copied from the shirdisaibabakripa.org printout (“Shirdi Sai Baba Evening (Dhoop) Arati”, by Manisha Rautela Bisht; the site states a Creative Commons Attribution-Noncommercial-No Derivative Works 2.5 licence) for every verse it translates, with only typos fixed; it is included for personal study, and permission has not been requested. The Hindi meaning, a second English meaning covering every verse, and the word meanings were written for this library, because neither printout has them. The Śrī Guru-prasāda-yācanā-daśaka (B. V. Deva) is included at the owner's request.
