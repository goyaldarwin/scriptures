# Nīlā Sūkta (नीलासूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › संहिता › नीलासूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/samhita/neela-suktam/`, work id `neela-suktam`). The sūkta to Nīḷā Devī, Viṣṇu's consort: the invocation नीळां देवीं शरणमहं प्रपद्ये, the two mantras of the Taittirīya Saṃhitā (4.4.12) beginning गृणाहि, the Nīlā Gāyatrī and ॐ शान्तिः, as the page gives them. It is also called the Viṣṇupatnī Sūkta.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram does. The page's own introduction names the Taittirīya Saṃhitā, and Sanskrit Wikisource's accented Taittirīya Saṃhitā has the passage beginning गृणाहि at its 4.4.12.5, so the sūkta goes on the existing Kṛṣṇa Yajurveda › Saṃhitā shelf, beside the Rudram. The Vaiṣṇava Pañca Sūkta is to be a work of its own that takes these verses (`[take neela-suktam …]`), so the grouping does not move any sūkta from its Veda.

## Sources
- **Text (source of truth).** shlokam.org's page [Neela Suktam](https://shlokam.org/shloka/neela-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/samhita/neela-suktam/printouts/shlokam/neela-suktam.html`. The Devanagari, with its svaras, follows the page exactly, except for the corrections in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Witnesses.** Sanskrit Wikisource's Taittirīya Saṃhitā, accented (kāṇḍas 1–4) and unaccented (4.4), raw wikitext in scriptures-data at `…/neela-suktam/printouts/wikisource/`; every word, and every svara, is checked against them (`source/check.py`, `reconciliation.md`).
- **Recording.** Soul Sadhana, YouTube `NZF4y9MDkSQ` (105.4 s), whose downloaded file names it "Neela Suktam (Vishnu Patni Suktam) Lyrics Meaning, Soul Sadhana". Audio source id `soul-sadhana`: `audio/soul-sadhana/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/neela-suktam/audio/soul-sadhana/NZF4y9MDkSQ.opus`. Transcribed (`transcripts/`), not yet timed (a draft). It sings the invocation, the two mantras and the śānti; it does not sing the Gāyatrī, which stays, untimed.
- **Word meanings:** every word, in the shared dictionary (`library/glossary/sa.json`; the readings decided: `reconciliation.md`, "Word meanings").
- **Meanings.** Written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, from the mantra's words, their grammar and Monier-Williams and Apte; no reading is put to any commentator (Sāyaṇa's commentary is not at hand). Brief context and well-known second readings are in the footnotes (`notes`); the readings decided are in `reconciliation.md`, "Meanings". The English on the shlokam.org page was read only to check ours, which shares no run of ten words with it (`tools/meanings/overlap.py`).
- **Introduction:** written and checked (`intro` in `library/index.json`, Hindi and English alike): every sentence matched against the mantras and our meanings, every fact about the work confirmed online.

## Files
The folder's format: `tools/works/README.md`.
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `source/extract.py <neela-suktam.html>` → `source/neela-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the corrections (`FIX`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `source/witnesses.py <dir>` → `source/witness/<site>.txt`: each independent witness's words, from its raw download (in scriptures-data at `printouts/<site>/`, with `.meta.json`), as runs of Devanagari headed by the verses they cover.
- `source/check.py`: compares `text.txt` with every witness, word for word and, where a witness has svaras, svara for svara (`tools/works/sukta_witness.py`, shared by the six Sūktas: what is read alike); it fails on any difference `reconciliation.md` does not record.
- `audio/soul-sadhana/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/neela-suktam/source/settle.py && python3 tools/works/export.py neela-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › two sections (`sukta`: the invocation and mantras 1–2; `end`: the Gāyatrī and the śānti) › items.
- **Numbering:** the page prints no numbers; the two mantras are numbered 1–2, each cited by its own number. The others have none.
- **Items:** `mangala` (type `mangala`, नीळां देवीं…), `m01`, `m02` (type `mantra`, the page's blocks 2 and 3), `gayatri` (type `gayatri`, ॐ महादेव्यै च विद्महे…), `shanti.end` (type `shanti`). 5 items. Ids are permanent.
- **Types** (`work.json` → `types`): maṅgala mantra, the invocation (मङ्ग॰ / Mang., as the Śrī Rudram's), mantra (मं॰ / Man.), Gāyatrī mantra (गा॰ / Gay.), śānti mantra (शा॰ / Shan.).
- **Topics** (ours): refuge in Neela Devi; Vishnu's consort, steadfast ruler of the quarters (1); Neela Gayatri and shanti.
- **Reading plans:** none.
