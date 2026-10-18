# शास्त्र · Scriptures

A personal, ad-free library for studying scriptures. Each work has the same reading experience: verses with their meanings from selectable sources, word-by-word meanings, natural divisions, reading plans, bookmarks and notes, and hands-free recitation with audio from YouTube.

**Website:** https://goyaldarwin.github.io/scriptures/

| Shelf | Work | Edition |
|---|---|---|
| Gosvāmī Tulasīdāsa | Śrī Rāmacaritamānasa: 7 kāṇḍas, 30-day and 9-day pārāyaṇa | Gita Press, Gorakhpur |
| Āratī › Shirdi Sāī Bābā | Dhūpa Āratī (evening āratī): Marathi, Sanskrit, Hindi | Shirdi tradition |

## What's where

```
index.html, sw.js, manifest.json    the website (GitHub Pages serves the repository root)   [generated]
app/                                 website code, styles, fonts                              [generated]
library/                             the scriptures, as data
  index.json                           the shelf: authors / collections / works, any depth
  glossary/                            word meanings, one dictionary per language (sa, awa, …) + languages.json
  aarti/shirdi-sai/dhoop-aarti/       the Shirdi Sāī Bābā evening āratī (work.json, meanings/)
  tulsidas/ramcharitmanas/
    work.json                          verses + numbers, kāṇḍas, topics, plans, pārāyaṇa vidhi
    meanings/hi-gitapress.json         a Hindi meaning source
    meanings/en-gitapress.json         an English meaning source
    audio/kamlesh-upadhyay.json        an audio source: YouTube video ids + verse timings     [generated]
docs/
  START-HERE.md                      resume the project in a new session
  HOW-TO.md                          add a work, a meaning source or a reciter; fix text; change the app
  LIBRARY.md                         the data format and its rules
  PLAYBOOK.md                        the owner's preferences, decisions and lessons
tools/                               everything that makes the data and the website (see tools/README.md)
  site/  audio/  fonts/  works/ramcharitmanas/  works/shirdi-sai-dhoop-aarti/
```

## Sources and permissions

The verse text of the Rāmacaritamānasa is in the public domain. The Hindi bhāvārtha (Hanumānprasād Poddār) and the English translation are © Gita Press, Gorakhpur, and are included here for personal study while permission from Gita Press is requested. Audio plays from the published YouTube recordings of Pt. Kamlesh Upadhyay "Haripuri"; no audio is stored in this repository.

The Shirdi Dhūpa Āratī: the verse text (Mādhava Aḍakara, Dāsagaṇu, Saint Nāmadeva, Mohinīrāja, Upāsanī Mahārāja, Vedic and traditional prayers) is in the public domain. It was settled by comparing two web printouts supplied by the owner (missionkuldevi.in and shirdisaibabakripa.org); see `tools/works/shirdi-sai-dhoop-aarti/reconciliation.md`. The Hindi and English meanings and the word meanings were written for this library. The Śrī Guru-prasāda-yācanā-daśaka is left out until its copyright status is confirmed.
