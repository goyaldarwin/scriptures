# Īśāvāsya Upaniṣad (ईशावास्योपनिषद्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › शुक्ल यजुर्वेद › उपनिषद् › ईशावास्योपनिषद् (`library/hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/`, work id `isha-upanishad`). Vājasaneyi Saṃhitā chapter 40, Kāṇva recension: 18 mantras, with the śānti mantra पूर्णमदः पूर्णमिदम्.

## Sources
- **Text:** the owner's printout of <https://shlokam.org/text/isha-upanishad.htm> is the source of truth. The private copy is in scriptures-data at `hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/printouts/shlokam/isha-upanishad.pdf`. It is checked against the standard Kāṇva text, with sanskritdocuments.org as the second witness. Every correction, and why, is in `reconciliation.md`. The printout has no svara marks, so neither does the text.
- **Meanings:** written for this library (`hi-scriptures`, `en-scriptures`), one to three sentences per mantra. They follow Śaṅkara's reading, are informed by the printout, and are not copied from it. Brief context and other readings are in the footnotes.
- **Word meanings:** written for this library, informed by the printout's word-by-word lists.
- **Audio:** SMVedroad, “Ishavashya Upanishad Chant … With Lyrics” (YouTube `mzczDkOtk0k`), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/audio/smvedroad/`. Live: `make_timings.py` times all 19 items from the transcript (`transcripts/`); two starts are hand-checked (`fixes.json`, evidence in `fixes.md`).

## Files
The folder's format: `tools/works/README.md`.
- `text.txt`: the settled text, in Devanagari; the export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `source/check.py <printout.pdf>`: compares `text.txt` with the printout's transliteration (only the corrections in `reconciliation.md` may differ). Run it after any change to the text.
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `glossary/sa.json`: two words whose shared sense doesn't fit here (कृतं “what has been done”, देव “O god”); every other word is in `library/glossary/sa.json`.

## Structure
One part (the Upaniṣad). Items: `shanti.1` (type `shanti`) and `m01`–`m18` (type `mantra`, with the printed number in `n`). Both types are declared in `work.json` → `types`. Each item is its own section. The topics follow the printout's sections: Śānti Pāṭha (`shanti.1`), mantras 1–2, 3–8, 9–14 and 15–18. Item ids are permanent.
