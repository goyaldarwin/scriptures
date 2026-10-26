# Kaṭha Upaniṣad (कठोपनिषद्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › उपनिषद् › कठोपनिषद् (`library/hinduism/veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad/`, work id `katha-upanishad`). The Upaniṣad of the Kaṭha śākhā of the Kṛṣṇa Yajurveda: two adhyāyas of three vallīs each, 119 mantras (29 + 25 + 17, 15 + 15 + 18), with the śānti mantra सह नाववतु before and after.

## Sources
- **Text.** The owner's book: Swami Gurubhaktananda, *Katha Upanishad — A Leap into the Beyond* (The Sandeepany Experience, Text 20; web edition 2018). The private copy is in scriptures-data at `<work path>/books/sandeepany/katha-upanishad-gurubhaktananda.pdf`. Its Devanagari is set in a legacy font (BRH Devanagari) whose text layer cannot be read, so the text is taken from the book's **IAST transliteration** (clean, once the font's Latin-1 symbols are decoded: `source/extract.py`) and converted letter for letter to Devanagari (`source/settle.py`). The result is checked against Devanagari witnesses of the standard text (`check.py`, `source/witness/`): shlokam.org (mantras 1.1.1–20, all that its page serves) — and the full text of sanskritdocuments.org once the owner provides it (see `reconciliation.md`, which also records every decision about the text).
- **Meanings.** Written for this library (`hi-scriptures`, `en-scriptures`, both `order: 1`): one to three sentences per mantra, in the verse's order, following Śaṅkara's reading, with the speaker named where he changes (Naciketā / Yama / the father). The book's word-by-word English was read as a guide for the words, never copied; its prose is not in this repository. Other readings and brief context are in the footnotes.
- **Word meanings.** Written for this library: 913 words added to `library/glossary/sa.json` (`glossary/*.json`, one file per vallī). Five words whose shared entry carries another text's sense (हर, परा, प्रथमो, विश्वे, देवा) have this work's sense in `glossary.json` (`WORK_SENSES` in `export.py`).
- **Audio.** SMVedroad, “Kathopnishad … With Lyrics” (YouTube `NQhdLn7FHwA`, 35 min), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `<work path>/audio/smvedroad/`. Transcribed in the cloud (`docs/HOW-TO.md` → “Add a new audio source”), then `make_timings.py`.

## Files
- `source/extract.py <the PDF>` → `source/pdf_raw.json`: each mantra's transliteration lines, decoded (and the śānti mantra's).
- `source/settle.py` → `text.json`: the settled text, one item per mantra, in house style (`v` Devanagari, `t` IAST made back from the Devanagari).
- `source/witness/*.txt`: Devanagari witnesses (verses separated by blank lines, `# 1.2` naming a vallī).
- `check.py`: `t` must spell `v`; every witness verse must spell the same words as `v` (only the differences in `reconciliation.md` are allowed). Run it after any change to the text.
- `meanings/hi.json`, `meanings/en.json`: `{item id: [meaning, [footnotes]]}` → `meanings/hi-scriptures.json`, `en-scriptures.json`.
- `glossary/shanti.json`, `v1.1.json` … `v2.3.json`: word meanings, merged into `library/glossary/sa.json` (add-only).
- `export.py`: run it, then `python3 tools/site/build.py`. It stops if a mantra lacks a meaning in either language or a word has no meaning.

Rebuild: `python3 tools/works/katha-upanishad/source/settle.py && python3 tools/works/katha-upanishad/check.py && python3 tools/works/katha-upanishad/export.py && python3 tools/site/build.py`. Run `extract.py` again only if the PDF changes.

## Structure
- **Parts:** प्रथम अध्याय, द्वितीय अध्याय.
- **Sections (pages):** the six vallīs (`v1.1` … `v2.3`), plus `shanti` (opening) and `shanti2` (closing).
- **Items:** `shanti.1`; `1.1.1` … `2.3.18` (adhyāya.vallī.mantra, the standard numbering, also in `n`; each verse ends with its number within the vallī, ।।१।।); `shanti.2`. The book counts the closing śānti as “2.3.19”; it is the opening śānti again. Ids are permanent.
- **Types:** `shanti` (शा॰ / Śā.) and `mantra` (मं॰ / Man.).
- **Topics:** one per vallī with its theme, plus the two śānti pāṭhas.
- **Reading plans:** none; the Upaniṣad is read in one or two sittings.
