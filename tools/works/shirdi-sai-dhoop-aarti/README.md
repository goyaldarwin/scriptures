# Shirdi Sāī Bābā — Dhūpa Āratī (evening āratī)

Shelf: Āratī › Shirdi Sāī Bābā › Dhūpa Āratī (`library/aarti/shirdi-sai/dhoop-aarti/`, work id `shirdi-sai-dhoop-aarti`).

- `text.txt`: the verse text, section by section, with each verse's type and language (`mr` Marathi, `sa` Sanskrit, `hi` Hindi). `reconciliation.md` records how it was settled from the two source printouts.
- `meanings/hi.json`, `meanings/en.json`: one meaning per verse, written for this library → `meanings/hi-scriptures.json`, `en-scriptures.json`.
- `glossary/mr.json`, `sa.json`, `hi.json`: word meanings, filed by the language of the verse the word is in. The exporter adds new words to `library/glossary/<lang>.json`; it never overwrites a word that is already there.
- `export.py`: run it, then `python3 tools/site/build.py`. It stops if a verse lacks a meaning or a word lacks a meaning in its language (Marathi and Hindi fall back to Sanskrit).

The work has one part (Dhūpa Āratī). Its pages are the sections (āratī, abhaṅga, namana …), and each section is also a topic. Verse types are declared in `work.json` → `types` (dhruvapada, pada, abhaṅga, śloka, mantra, jayaghoṣa).

Item ids look like `aarti.pad3` or `mahimna.shloka9` (section, type, number). They are permanent.

Audio (Pramod Medhi, YouTube `QKf_JPbN6Lw`) is not timed yet. Transcription needs the Whisper model, which this workspace could not download (huggingface.co is not reachable). Follow `docs/HOW-TO.md` → "Add a new audio source" once it is.
