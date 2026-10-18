# Shirdi Sāī Bābā — Dhūpa Āratī (evening āratī)

Shelf: हिन्दू धर्म › Āratī › Shirdi Sāī Bābā › Dhūpa Āratī (`library/hinduism/aarti/shirdi-sai/dhoop-aarti/`, work id `shirdi-sai-dhoop-aarti`).

- `text.txt`: the verse text, section by section, with each verse's type and language (`mr` Marathi, `sa` Sanskrit, `hi` Hindi). `reconciliation.md` records how it was settled from the two source printouts.
- `meanings/en-shirdisaibabakripa.json`: the English meaning copied from the shirdisaibabakripa.org printout (dhoop.pdf), for 62 of the 63 verses (not the closing jayaghoṣa `prarthana.jay2`). It is the default English source (`order: 1`). How its paragraphs were mapped to our verses and every typo fixed are in `reconciliation.md`. A value is the meaning, or `[meaning, [footnotes]]`.
- `meanings/hi.json`, `meanings/en.json`: one meaning per verse, written for this library → `meanings/hi-scriptures.json` (the only Hindi source; the printouts have no Hindi meaning) and `en-scriptures.json` (the second English source, `order: 2`, covering every verse).
- `glossary/mr.json`, `sa.json`, `hi.json`: word meanings, filed by the language of the verse the word is in. The exporter adds new words to `library/glossary/<lang>.json`; it never overwrites a word that is already there.
- `export.py`: run it, then `python3 tools/site/build.py`. It stops if a verse lacks a meaning or a word lacks a meaning in its language (Marathi and Hindi fall back to Sanskrit).

The work has one part (Dhūpa Āratī). Its pages are the sections (āratī, abhaṅga, namana … the Guru-prasāda-yācanā-daśaka between the Mahimna stotra and the Puṣpāñjali), and each section is also a topic. Verse types are declared in `work.json` → `types` (dhruvapada, pada, abhaṅga, śloka, mantra, jayaghoṣa).

Item ids look like `aarti.pad3` or `mahimna.shloka9` (section, type, number). They are permanent.

Audio (Pramod Medhi, YouTube `QKf_JPbN6Lw`) is not timed yet. Transcription needs the Whisper model, which this workspace could not download (huggingface.co is not reachable). Follow `docs/HOW-TO.md` → "Add a new audio source" once it is.
