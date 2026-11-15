# Muṇḍaka Upaniṣad (मुण्डकोपनिषद्)

Shelf: हिन्दू धर्म › वेद › अथर्ववेद › उपनिषद् › मुण्डकोपनिषद् (`library/hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/`, work id `mundaka-upanishad`). The śānti mantra, three muṇḍakas of two khaṇḍas each (64 mantras, 1.1.1–3.2.11), and the closing words of each khaṇḍa.

## Sources
- **Text:** the shlokam.org page <https://shlokam.org/text/mundaka-upanishad.htm> (the owner allowed it), saved as HTML in scriptures-data at `hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/printouts/shlokam/mundaka-upanishad.html`. Its Devanagari is the base; its own transliteration is the first check of every line; its word-by-word lists (the Devanagari headwords only) settle its slips. The page has no svara marks, so neither does the text. Every choice is in `reconciliation.md`.
- **Witnesses:** IIT Kanpur's Heritage reader (MNU), upanishads.org.in, Sanskrit Wikisource and the Vedic Heritage Portal, raw downloads in scriptures-data at `hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/printouts/<site>/`. Mantra 3.2.11 and the closing words of khaṇḍa 3.2, which the page lacks, are taken from them.
- **Meanings:** written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, following Śaṅkara's reading, checked against his bhāṣya (IIT Kanpur's Sanskrit). Other readings and brief context are in the footnotes (`notes`). shlokam.org's English and word glosses, Swami Sitarama Sastri's translation of the bhāṣya and Sri Aurobindo's English (upanishads.org.in) were read only to check a reading; our meanings share no run of ten words with them (`tools/meanings/overlap.py`). The readings that were weighed are in `reconciliation.md`.
- **Word meanings:** written for this library, in `library/glossary/sa.json`.
- **Introduction:** not written yet.
- **Audio:** SMVedroad, "Mundaka Upanishad Chant | मुण्डक उपनिषद् गान | With Lyrics" (YouTube `kIJO1xhPs-Q`, 1538.8 s), in `audio/smvedroad/` (`source.json`, `recordings.json`). The speech-quality copy is in scriptures-data at `hinduism/veda/atharvaveda/upanishad/mundaka-upanishad/audio/smvedroad/kIJO1xhPs-Q.opus`. Not transcribed or timed yet. The video's title and description name no structure and carry no lyrics, so whether it chants the whole text, in which order and with which opening is read from its transcript when it is timed.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <page.html>`: reads the page's verse blocks (`div.detail-sanskrit` and the transliteration after it, split at `<br>`) into `source/mundaka-upanishad_raw.json`. Only the Sanskrit and its transliteration are kept; the page's English, translation and word glosses are © shlokam.org and never enter this repository.
- `source/settle.py`: checks every Devanagari line against the page's own transliteration, applies the corrections in `reconciliation.md`, adds 3.2.11 and 3.2.iti from the witnesses and writes `text.txt` through `tools/works/textfile.py`.
- `source/witnesses.py <printouts folder>`: the witnesses' raw downloads → `source/witness/<site>.txt` (Devanagari, one block per mantra).
- `source/check.py`: compares every item of `text.txt` with every witness; the only differences allowed are those `reconciliation.md` records.
- `text.txt`: the settled text; the export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).

## Structure
- **Hierarchy:** three parts (the muṇḍakas, keys `1`–`3`) › one section per khaṇḍa (`k1.1` … `k3.2`) › the mantras. The śānti is in its own section, `shanti`, in part 1.
- **Numbering:** a mantra's `n` is its number within its khaṇḍa, as the page prints it at its end (॥१॥); it is cited muṇḍaka.khaṇḍa.mantra (`work.json` → `cite`: Mantra 2.2.3), as the Kaṭha is cited adhyāya.vallī.mantra. Count: 1.1 (9), 1.2 (13), 2.1 (10), 2.2 (11), 3.1 (10), 3.2 (11).
- **Items:** `shanti.1` (type `shanti`), `1.1.1` … `3.2.11` (type `mantra`), and `1.1.iti` … `3.2.iti` (type `iti`, "समापन (पुष्पिका)" / "Closing words (iti)"): each khaṇḍa's closing words (॥ इति मुण्डकोपनिषदि प्रथममुण्डके प्रथमः खण्डः ॥), which the page prints inside its last mantra's block, are their own items, with no number. Item ids are permanent.
- **Topics:** Śānti Pāṭha and one per khaṇḍa, in our own words.
- **Against its models:** the Kaṭha (a three-level citation) leaves out its vallīs' closing words; this text keeps the khaṇḍa closings because the page prints them. The Māṇḍūkya (the same shelf) has one closing item at the end; this text ends with the closing words of khaṇḍa 3.2, because only the sanskritdocuments.org text (Wikisource, the Heritage Portal) prints the Upaniṣad's colophon and a closing śānti (`reconciliation.md`).
