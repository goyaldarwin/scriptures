# Śrī Sūkta (श्रीसूक्तम्)

Shelf: हिन्दू धर्म › वेद › ऋग्वेद › संहिता › श्रीसूक्तम् (`library/hinduism/veda/rigveda/samhita/shri-suktam/`, work id `shri-suktam`). The fifteen ṛks of the Śrī Sūkta, its phalaśruti, the verses in praise of Lakṣmī recited after it, and the closing, 37 verses numbered as the page prints them.

**Why this shelf.** A Vedic text sits by its Veda and division (`docs/LIBRARY.md` §1), as the Śrī Rudram does. The Śrī Sūkta is a khila (an appendix hymn) of the Ṛgveda: the page's own introduction says it is found in the Ṛgveda's khilas, and GRETIL's Ṛgveda-khilāni (Scheftelowitz) has it after khila 2.5 (`hiraṇya.varṇām`). A khila belongs to the saṃhitā it supplements, so it goes on the Ṛgveda › Saṃhitā shelf, with no new level for khilas (reuse before adding, §1); `by` says "Rigveda, khila 2.6". The id is `shri-suktam`, spelt as `shri-rudram`. The Ṛgveda shelf is new on `main` (the Aitareya Upaniṣad's branch adds the same `rigveda` shelf, titled alike). The Vaiṣṇava Pañca Sūkta is to be a work of its own that takes these verses (`[take shri-suktam …]`), so the grouping does not move any sūkta from its Veda.

## Sources
- **Text (source of truth).** shlokam.org's page [Sri Suktam](https://shlokam.org/shloka/sri-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/rigveda/samhita/shri-suktam/printouts/shlokam/sri-suktam.html`. The page has no svaras, so neither does the text. The Devanagari follows the page exactly, except for its two headings and the corrections in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Recording.** Sri Sathya Sai Official, YouTube `r-HQ8MrQiDM` (487.3 s), whose downloaded file names it "Sri Suktam With Lyrics & Meaning, Vedic Chants". `audio/sri-sathya-sai/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/shri-suktam/audio/sri-sathya-sai/r-HQ8MrQiDM.opus`. Not yet transcribed or timed (a draft). What it sings is known here only from its title (the sūkta); whether it sings the phalaśruti and the later verses, in the page's order, and any opening the page lacks, the transcript will show. A verse it leaves out stays in the text, untimed; an opening it sings is added as text from a written witness (PLAYBOOK §3). It is a Vedic chant: it may sing the ṛks with svaras the page does not print.
- **Meanings, word meanings, introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <sri-suktam.html>` → `source/sri-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the corrections (`FIX`), the page's headings left out (`HEADING`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `audio/sri-sathya-sai/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/shri-suktam/source/settle.py && python3 tools/works/export.py shri-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › three sections (`sukta`: ṛks 1–15; `phala`: the phalaśruti, 16; `stotra`: verses 17–37) › verses.
- **Numbering:** each verse's `n` is the number the page prints at its end (॥१॥ … ॥३७॥), and it is cited by it (Mantra 5, Shloka 24).
- **Items:** `m01`–`m37`, one per printed number. 37 items. Ids are permanent.
- **Types** (`work.json` → `types`): mantra, the ṛks 1–15 (मं॰ / Man.); phalaśruti, 16 (फल॰ / Phala.); śloka, 17–33, 35, 36 (श्लो॰ / Shl.); Gāyatrī mantra, 34 (गा॰ / Gay.); closing mantra, 37 (उ॰ / Cl., as the Śrī Rudram's: य एवं वेद, the Gāyatrī again and the śānti, which the page prints as one verse).
- **Topics** (ours): calling Lakshmi to the home (1); Phalashruti (16); verses in praise of Lakshmi (17); Closing (37).
- **Reading plans:** none.
