# Nārāyaṇa Sūkta (नारायणसूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › आरण्यक › नारायणसूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/`, work id `narayana-suktam`). The sūkta of the Taittirīya Āraṇyaka's tenth prapāṭhaka (the Mahānārāyaṇa), with the śānti pāṭha सह नाववतु before it, the Nārāyaṇa Gāyatrī and ॐ शान्तिः after it, as the page gives them.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram sits at `…/krishna-yajurveda/samhita/`. The sūkta is in the Taittirīya Āraṇyaka (the page's own introduction says so, and Sanskrit Wikisource's accented Taittirīya Āraṇyaka has it in its Mahānārāyaṇa prapāṭhaka), so it goes on the Kṛṣṇa Yajurveda's Āraṇyaka shelf, beside the Puruṣa and Durgā Sūktas. The Mahānārāyaṇa is also read as an Upaniṣad, but a reader looks for the sūkta among the Vedic hymns, not among the Upaniṣads, and the Āraṇyaka is the book it is from. The Vaiṣṇava Pañca Sūkta is to be a work of its own that takes these verses (`[take narayana-suktam …]`), so the grouping does not move any sūkta from its Veda.

## Sources
- **Text (source of truth).** shlokam.org's page [Narayana Suktam](https://shlokam.org/shloka/narayana-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/printouts/shlokam/narayana-suktam.html`. The Devanagari, with its svaras, follows the page exactly, except for the seven corrections in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Witnesses.** Sanskrit Wikisource's accented Taittirīya Āraṇyaka and its Mahānārāyaṇa Upaniṣad, raw wikitext in scriptures-data at `…/narayana-suktam/printouts/wikisource/`; every word, and every svara the accented one has, is checked against them (`source/check.py`, `reconciliation.md`).
- **Recording.** Sri Sathya Sai Official, YouTube `dD5leb7NpNQ` (228.2 s), whose downloaded file names it "Narayana Suktam With Lyrics & Meaning, Ancient Vedic Chants In Sanskrit". `audio/sri-sathya-sai/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/narayana-suktam/audio/sri-sathya-sai/dD5leb7NpNQ.opus`. Transcribed (`transcripts/`), not yet timed (a draft). It opens with Puruṣa Sūkta mantra 17 (धाता पुरस्तात्…), taken from that work before mantra 1, then sings the fourteen mantras, the Gāyatrī and the śānti; it does not sing the opening सह नाववतु, which stays, untimed.
- **Word meanings:** every word, in the shared dictionary (`library/glossary/sa.json`; the readings decided: `reconciliation.md`, "Word meanings").
- **Meanings.** Written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, from the mantra's words, their grammar and Monier-Williams and Apte; no reading is put to any commentator (Sāyaṇa's commentary is not at hand). Brief context and well-known second readings are in the footnotes (`notes`); the readings decided are in `reconciliation.md`, "Meanings". The English on the shlokam.org page was read only to check ours, which shares no run of ten words with it (`tools/meanings/overlap.py`). Mantra `m17` (धाता पुरस्तात्), taken from the Puruṣa Sūkta, keeps that work's meaning.
- **Introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `source/extract.py <narayana-suktam.html>` → `source/narayana-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the correction (`FIX`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `source/witnesses.py <dir>` → `source/witness/<site>.txt`: each independent witness's words, from its raw download (in scriptures-data at `printouts/<site>/`, with `.meta.json`), as runs of Devanagari headed by the verses they cover.
- `source/check.py`: compares `text.txt` with every witness, word for word and, where a witness has svaras, svara for svara (`tools/works/sukta_witness.py`, shared by the six Sūktas: what is read alike); it fails on any difference `reconciliation.md` does not record.
- `audio/sri-sathya-sai/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/narayana-suktam/source/settle.py && python3 tools/works/export.py narayana-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › three sections (`shanti`: the opening śānti pāṭha; `sukta`: the opening taken from the Puruṣa Sūkta and mantras 1–14; `end`: the Gāyatrī and the closing śānti) › items.
- **Numbering:** the page prints no numbers; mantras are numbered 1–14 in the page's order (its blocks 2–15), each cited by its own number (Mantra 7). The śānti pāṭhas and the Gāyatrī have none.
- **Items:** `shanti.1` (type `shanti`), `m01`–`m14` (type `mantra`, one per page block of two lines), `gayatri` (type `gayatri`, ॐ नारायणाय विद्महे…), `shanti.end` (type `shanti`). 17 items of its own, and Puruṣa Sūkta `m17` taken before `m01` (`[take purusha-suktam m17]`: it keeps its id and its citation there, Mantra 17 of the Puruṣa Sūkta). Ids are permanent.
- **Types** (`work.json` → `types`): śānti mantra (शा॰ / Shan.), mantra (मं॰ / Man.), Gāyatrī mantra (गा॰ / Gay.).
- **Topics** (ours): Shanti Paath; Opening: Dhata purastat; Narayana, all that is and beyond all (1); the flame in the lotus of the heart (7); Narayana Gayatri and shanti.
- **Reading plans:** none.
