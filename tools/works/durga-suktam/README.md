# Durgā Sūkta (दुर्गासूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › आरण्यक › दुर्गासूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/`, work id `durga-suktam`). The seven mantras of the Taittirīya Āraṇyaka's tenth prapāṭhaka (the Mahānārāyaṇa) to Agni and Durgā, with the Durgā Gāyatrī, the closing words इति दुर्गा सूक्तम् and ॐ शान्तिः, as the page gives them.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram sits at `…/krishna-yajurveda/samhita/`. Sanskrit Wikisource's accented Taittirīya Āraṇyaka has these mantras in its Mahānārāyaṇa prapāṭhaka, so the sūkta goes on the Kṛṣṇa Yajurveda's Āraṇyaka shelf, beside the Puruṣa and Nārāyaṇa Sūktas, one level from the Rudram (Kṛṣṇa Yajurveda › Saṃhitā). The Śaiva grouping that is to come (the Rudram and the Durgā Sūkta) is to be a work of its own that takes their verses (`[take shri-rudram …]`, `[take durga-suktam …]`, as the Sundarakāṇḍa takes the Mānas's), so it moves neither from its Veda; both are of the same śākhā.

## Sources
- **Text (source of truth).** shlokam.org's page [Durga Suktam](https://shlokam.org/shloka/durga-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/printouts/shlokam/durga-suktam.html`. The Devanagari, with its svaras, follows the page exactly, except for its heading and the two corrections in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Recording.** The Sri Sathya Sai International Organization's Young Adults Veda Programme (SSSIO), YouTube `eAlAmnM9UGM` (186.6 s), whose downloaded file names it "Durga Suktam with Lyrics and Meaning, Sri Sathya Sai Young Adults Veda Programme". Audio source id `sssio` (the organisation, as `sri-sathya-sai` names Sri Sathya Sai Official): `audio/sssio/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/durga-suktam/audio/sssio/eAlAmnM9UGM.opus`. Not yet transcribed or timed (a draft). What it sings is known here only from its title (the sūkta); whether it sings the Gāyatrī, the closing words and the śānti, in what order, and any opening the page lacks, the transcript will show; an opening it sings is then added as text from a written witness (PLAYBOOK §3).
- **Meanings, word meanings, introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <durga-suktam.html>` → `source/durga-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the corrections (`FIX`), the page's heading left out (`HEADING`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `audio/sssio/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/durga-suktam/source/settle.py && python3 tools/works/export.py durga-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › two sections (`sukta`: mantras 1–7; `end`: the Gāyatrī, the closing words, the śānti) › items.
- **Numbering:** the page prints no numbers; mantras are numbered 1–7 in the page's order, each cited by its own number (Mantra 2). The others have none.
- **Items:** `m01`–`m07` (type `mantra`), `gayatri` (type `gayatri`, ॐ कात्यायनाय विद्महे…), `iti` (type `iti`, इति दुर्गा सूक्तम् ॥), `shanti.end` (type `shanti`). 10 items. Ids are permanent.
- **Types** (`work.json` → `types`): mantra (मं॰ / Man.), Gāyatrī mantra (गा॰ / Gay.), closing words (इति / Iti: "समापन (पुष्पिका)" / "Closing words (iti)"), śānti mantra (शा॰ / Shan.).
- **Topics** (ours): Agni, carry us across every hardship (1); Durga Gayatri and closing.
- **Reading plans:** none.
