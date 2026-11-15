# Nārāyaṇa Sūkta (नारायणसूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › आरण्यक › नारायणसूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/`, work id `narayana-suktam`). The sūkta of the Taittirīya Āraṇyaka's tenth prapāṭhaka (the Mahānārāyaṇa), with the śānti pāṭha सह नाववतु before it, the Nārāyaṇa Gāyatrī and ॐ शान्तिः after it, as the page gives them.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram sits at `…/krishna-yajurveda/samhita/`. The sūkta is in the Taittirīya Āraṇyaka (the page's own introduction says so, and Sanskrit Wikisource's accented Taittirīya Āraṇyaka has it in its Mahānārāyaṇa prapāṭhaka), so it goes on the Kṛṣṇa Yajurveda's Āraṇyaka shelf, beside the Puruṣa and Durgā Sūktas. The Mahānārāyaṇa is also read as an Upaniṣad, but a reader looks for the sūkta among the Vedic hymns, not among the Upaniṣads, and the Āraṇyaka is the book it is from. The Vaiṣṇava Pañca Sūkta is to be a work of its own that takes these verses (`[take narayana-suktam …]`), so the grouping does not move any sūkta from its Veda.

## Sources
- **Text (source of truth).** shlokam.org's page [Narayana Suktam](https://shlokam.org/shloka/narayana-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/printouts/shlokam/narayana-suktam.html`. The Devanagari, with its svaras, follows the page exactly, except for the one correction in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Recording.** Sri Sathya Sai Official, YouTube `dD5leb7NpNQ` (228.2 s), whose downloaded file names it "Narayana Suktam With Lyrics & Meaning, Ancient Vedic Chants In Sanskrit". `audio/sri-sathya-sai/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/narayana-suktam/audio/sri-sathya-sai/dD5leb7NpNQ.opus`. Not yet transcribed or timed (a draft). What it sings is known here only from its title (the sūkta); whether it sings the śānti pāṭha, the Gāyatrī and the closing śānti, in what order, and any opening the page lacks, the transcript will show; an opening it sings is then added as text from a written witness (PLAYBOOK §3).
- **Meanings, word meanings, introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <narayana-suktam.html>` → `source/narayana-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the correction (`FIX`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `audio/sri-sathya-sai/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/narayana-suktam/source/settle.py && python3 tools/works/export.py narayana-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › three sections (`shanti`: the opening śānti pāṭha; `sukta`: mantras 1–14; `end`: the Gāyatrī and the closing śānti) › items.
- **Numbering:** the page prints no numbers; mantras are numbered 1–14 in the page's order (its blocks 2–15), each cited by its own number (Mantra 7). The śānti pāṭhas and the Gāyatrī have none.
- **Items:** `shanti.1` (type `shanti`), `m01`–`m14` (type `mantra`, one per page block of two lines), `gayatri` (type `gayatri`, ॐ नारायणाय विद्महे…), `shanti.end` (type `shanti`). 17 items. Ids are permanent.
- **Types** (`work.json` → `types`): śānti mantra (शा॰ / Shan.), mantra (मं॰ / Man.), Gāyatrī mantra (गा॰ / Gay.).
- **Topics** (ours): Shanti Paath; Narayana, all that is and beyond all (1); the flame in the lotus of the heart (7); Narayana Gayatri and shanti.
- **Reading plans:** none.
