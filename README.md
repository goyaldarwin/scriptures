# शास्त्र · Scriptures

A personal, ad-free library for studying scriptures. Each work has the same reading experience: verses with their meanings from selectable sources, word-by-word meanings, natural divisions, reading plans, bookmarks and notes, and hands-free recitation with audio from YouTube.

**Website:** https://goyaldarwin.github.io/scriptures/

| Shelf | Work | Edition |
|---|---|---|
| Gosvāmī Tulasīdāsa | Śrī Rāmacaritamānasa: 7 kāṇḍas, 30-day and 9-day pārāyaṇa | Gita Press, Gorakhpur |

## What's where

```
index.html, sw.js, manifest.json    the website (GitHub Pages serves the repository root)   [generated]
app/                                 website code, styles, fonts                              [generated]
library/                             the scriptures, as data
  index.json                           the shelf: tradition / genre / group… / work (docs/LIBRARY.md §1)
  glossary/                            word meanings, one dictionary per language (sa, awa, …) + languages.json
  hindu/granth/tulsidas/ramcharitmanas/
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
  site/  audio/  fonts/  works/ramcharitmanas/
```

## Sources and permissions

The verse text of the Rāmacaritamānasa is in the public domain. The Hindi bhāvārtha (Hanumānprasād Poddār) and the English translation are © Gita Press, Gorakhpur, and are included here for personal study while permission from Gita Press is requested. Audio plays from the published YouTube recordings of Pt. Kamlesh Upadhyay "Haripuri"; no audio is stored in this repository.
