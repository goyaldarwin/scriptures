# Māṇḍūkya Upaniṣad (माण्डूक्योपनिषद्)

Shelf: हिन्दू धर्म › वेद › अथर्ववेद › उपनिषद् › माण्डूक्योपनिषद् (`library/hinduism/veda/atharvaveda/upanishad/mandukya-upanishad/`, work id `mandukya-upanishad`). The śānti mantra, 12 mantras and the closing words.

## Sources
- **Text:** the owner's printout of <https://sanskritdocuments.org/doc_upanishhat/maandu.html>; the śānti mantra as SMVedroad chants it and the owner's freepressjournal.in printout (NJ Reddy) gives it. Copies for scriptures-data: `hinduism/veda/atharvaveda/upanishad/mandukya-upanishad/printouts/` (to add). Every choice is in `reconciliation.md`.
- **Meanings:** written for this library (`hi-scriptures`, `en-scriptures`), following Śaṅkara's reading.
- **Word meanings:** written for this library (`glossary_sa.json`); three words whose shared sense doesn't fit here are in `WORK_SENSES` (`export.py`).
- **Audio:** SMVedroad, "Mandukya Upanishad Chant … With Lyrics" (YouTube `mZTo8OEhRpc`), in `audio/smvedroad/`.

## Files
- `text.txt`: the settled text, one item per mantra (`[<id> <type> <number>]`, then the lines).
- `meanings/hi.json`, `en.json`: `{item id: [meaning, [footnotes]]}`.
- `export.py`: run it, then `python3 tools/site/build.py`. It stops if an item lacks a meaning or a word lacks a meaning.

## Structure
One part. Items `shanti.1`, `m01`–`m12` (type `mantra`), `iti`. Each item is its own section. Topics: Śānti Pāṭha and the recording's four khaṇḍas (mantras 1–2, 3–7, 8–11, 12). Item ids are permanent.
