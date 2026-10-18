# Īśāvāsya Upaniṣad (ईशावास्योपनिषद्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › शुक्ल यजुर्वेद › उपनिषद् › ईशावास्योपनिषद् (`library/hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/`, work id `isha-upanishad`). Vājasaneyi Saṃhitā chapter 40, Kāṇva recension: 18 mantras, with the śānti mantra पूर्णमदः पूर्णमिदम्.

## Sources
- **Text:** the owner's printout of <https://shlokam.org/text/isha-upanishad.htm> is the source of truth. The private copy is in scriptures-data at `hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/printouts/shlokam/isha-upanishad.pdf`. It was checked against the standard Kāṇva text, with sanskritdocuments.org as the second witness. Every correction, and why it was made, is in `reconciliation.md`. The printout has no svara marks, so neither does the text.
- **Meanings:** written for this library (`hi-scriptures`, `en-scriptures`), one to three sentences per mantra. They follow Śaṅkara's reading, are informed by the printout, and are not copied from it. Brief context and other readings are in the footnotes.
- **Word meanings:** written for this library, informed by the printout's word-by-word lists.
- **Audio:** SMVedroad, “Ishavashya Upanishad Chant … With Lyrics” (YouTube `mzczDkOtk0k`), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/audio/smvedroad/`. It is not timed yet: transcribe it in the cloud, then run `make_timings.py` (`docs/HOW-TO.md` → “Add a new audio source”).

## Files
- `text.json`: the settled text, items in reading order, in house style (`v` Devanagari, `t` transliteration).
- `check.py <printout.pdf>`: compares `text.json` with the printout's transliteration (only the corrections in `reconciliation.md` may differ), and checks that `t` spells the same text as `v`. Run it after any change to the text.
- `meanings/hi.json`, `meanings/en.json`: `{item id: [meaning, [footnotes]]}` → `meanings/hi-scriptures.json`, `en-scriptures.json` (both `order: 1`).
- `glossary_sa.json`: every word of the text. The exporter adds the new ones to `library/glossary/sa.json` and never overwrites an existing word. Two words already in the shared dictionary with a sense that doesn't fit here (कृतं “what has been done”, देव “O god”) go to the work's own `glossary.json` (`WORK_SENSES` in `export.py`).
- `export.py`: run it, then `python3 tools/site/build.py`. It stops if a mantra lacks a meaning in either language, and it reports any word without a meaning.

## Structure
One part (the Upaniṣad). Items: `shanti.1` (type `shanti`) and `m01`–`m18` (type `mantra`, with the printed number in `n`). Both types are declared in `work.json` → `types`. Each item is its own section. The topics follow the printout's sections: Śānti Pāṭha (`shanti.1`), mantras 1–2, 3–8, 9–14 and 15–18. Item ids are permanent.
