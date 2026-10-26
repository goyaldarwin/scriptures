# Shirdi Sāī Bābā — Dhūpa Āratī (evening āratī)

Shelf: हिन्दू धर्म › Āratī › Shirdi Sāī Bābā › Dhūpa Āratī (`library/hinduism/aarti/shirdi-sai/dhoop-aarti/`, work id `shirdi-sai-dhoop-aarti`).

- `text.txt`: the verse text, section by section, with each verse's type and language (`mr` Marathi, `sa` Sanskrit, `hi` Hindi). `reconciliation.md` records how it is settled from the two source printouts.
- `meanings/hi.json`, `meanings/en.json`: one meaning per verse, written for this library → `meanings/hi-scriptures.json` (the only Hindi source; the printouts have no Hindi meaning) and `en-scriptures.json`. Both are the default (`order: 1`) and cover all 64 verses.
- `meanings/en-shirdisaibabakripa.json`: the English meaning copied from the shirdisaibabakripa.org printout (dhoop.pdf), for 62 of the 64 verses (not the two closing jayaghoṣas, `prarthana.jay2` and `jay3`). It is the second English source (`order: 2`), still selectable. How its paragraphs map to our verses and every typo fixed are in `reconciliation.md`. A value is the meaning, or `[meaning, [footnotes]]`.
- `glossary/mr.json`, `sa.json`, `hi.json`: word meanings, filed by the language of the verse the word is in. The exporter adds new words to `library/glossary/<lang>.json`; it never overwrites a word that is already there.
- `export.py`: run it, then `python3 tools/site/build.py`. It stops if a verse lacks a meaning or a word lacks a meaning in its language (Marathi and Hindi fall back to Sanskrit).

The work has one part (Dhūpa Āratī). Its pages are the sections (āratī, abhaṅga, namana … the Guru-prasāda-yācanā-daśaka between the Mahimna stotra and the Puṣpāñjali), and each section is also a topic. Verse types are declared in `work.json` → `types` (dhruvapada, pada, abhaṅga, śloka, mantra, jayaghoṣa).

Item ids look like `aarti.pad3` or `mahimna.shloka9` (section, type, number). They are permanent.

Audio (Pramod Medhi), two uploads of the same recording:
- `audio/pramod-medhi-times/`: the Times Music upload (YouTube `b_JJzjc2Rgk`), the live source (`order: 1`). Its starts are the owner's, set by ear in the app's timing mode (`owner.json`, written by `tools/audio/apply_owner_timing.py`); `source.json` → `checked`.
- `audio/pramod-medhi/`: the Sai Aashirwad upload (YouTube `QKf_JPbN6Lw`), a draft: YouTube does not allow it to be played inside other sites. It keeps its hand-checked starts (`fixes.json`, evidence in `fixes.md`).
