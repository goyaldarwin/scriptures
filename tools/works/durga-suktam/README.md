# Durgā Sūkta (दुर्गासूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › आरण्यक › दुर्गासूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/`, work id `durga-suktam`). The seven mantras of the Taittirīya Āraṇyaka's tenth prapāṭhaka (the Mahānārāyaṇa) to Agni and Durgā, with the Durgā Gāyatrī, the closing words इति दुर्गा सूक्तम् and ॐ शान्तिः, as the page gives them.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram sits at `…/krishna-yajurveda/samhita/`. Sanskrit Wikisource's accented Taittirīya Āraṇyaka has these mantras in its Mahānārāyaṇa prapāṭhaka, so the sūkta goes on the Kṛṣṇa Yajurveda's Āraṇyaka shelf, beside the Puruṣa and Nārāyaṇa Sūktas, one level from the Rudram (Kṛṣṇa Yajurveda › Saṃhitā). The Śaiva grouping that is to come (the Rudram and the Durgā Sūkta) is to be a work of its own that takes their verses (`[take shri-rudram …]`, `[take durga-suktam …]`, as the Sundarakāṇḍa takes the Mānas's), so it moves neither from its Veda; both are of the same śākhā.

## Sources
- **Text (source of truth).** shlokam.org's page [Durga Suktam](https://shlokam.org/shloka/durga-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/printouts/shlokam/durga-suktam.html`. The Devanagari, with its svaras, follows the page exactly, except for its heading and the two corrections in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Witnesses.** Sanskrit Wikisource's accented Taittirīya Āraṇyaka and its Mahānārāyaṇa Upaniṣad, raw wikitext in scriptures-data at `…/durga-suktam/printouts/wikisource/`; every word, and every svara the accented one has, is checked against them (`source/check.py`, `reconciliation.md`).
- **Recording.** The Sri Sathya Sai International Organization's Young Adults Veda Programme (SSSIO), YouTube `eAlAmnM9UGM` (186.6 s), whose downloaded file names it "Durga Suktam with Lyrics and Meaning, Sri Sathya Sai Young Adults Veda Programme". Audio source id `sssio` (the organisation, as `sri-sathya-sai` names Sri Sathya Sai Official): `audio/sssio/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/durga-suktam/audio/sssio/eAlAmnM9UGM.opus`. Transcribed (`transcripts/`), not yet timed (a draft). It sings the seven mantras, the Gāyatrī and the śānti, in the page's order, with no opening the page lacks.
- **Word meanings:** every word, in the shared dictionary (`library/glossary/sa.json`; the readings decided: `reconciliation.md`, "Word meanings").
- **Meanings.** Written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, from the mantra's words, their grammar and Monier-Williams and Apte; no reading is put to any commentator (Sāyaṇa's commentary is not at hand). Brief context and well-known second readings are in the footnotes (`notes`); the readings decided are in `reconciliation.md`, "Meanings". The English on the shlokam.org page was read only to check ours, which shares no run of ten words with it (`tools/meanings/overlap.py`).
- **Introduction:** written and checked (`intro` in `library/index.json`, Hindi and English alike): every sentence matched against the mantras and our meanings, every fact about the work confirmed online.

## Files
The folder's format: `tools/works/README.md`.
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `source/extract.py <durga-suktam.html>` → `source/durga-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the corrections (`FIX`), the page's heading left out (`HEADING`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `source/witnesses.py <dir>` → `source/witness/<site>.txt`: each independent witness's words, from its raw download (in scriptures-data at `printouts/<site>/`, with `.meta.json`), as runs of Devanagari headed by the verses they cover.
- `source/check.py`: compares `text.txt` with every witness, word for word and, where a witness has svaras, svara for svara (`tools/works/sukta_witness.py`, shared by the six Sūktas: what is read alike); it fails on any difference `reconciliation.md` does not record.
- `audio/sssio/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/durga-suktam/source/settle.py && python3 tools/works/export.py durga-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › two sections (`sukta`: mantras 1–7; `end`: the Gāyatrī, the closing words, the śānti) › items.
- **Numbering:** the page prints no numbers; mantras are numbered 1–7 in the page's order, each cited by its own number (Mantra 2). The others have none.
- **Items:** `m01`–`m07` (type `mantra`), `gayatri` (type `gayatri`, ॐ कात्यायनाय विद्महे…), `iti` (type `iti`, इति दुर्गा सूक्तम् ॥), `shanti.end` (type `shanti`). 10 items. Ids are permanent.
- **Types** (`work.json` → `types`): mantra (मं॰ / Man.), Gāyatrī mantra (गा॰ / Gay.), closing words (इति / Iti: "समापन (पुष्पिका)" / "Closing words (iti)"), śānti mantra (शा॰ / Shan.).
- **Topics** (ours): Agni, carry us across every hardship (1); Durga Gayatri and closing.
- **Reading plans:** none.
