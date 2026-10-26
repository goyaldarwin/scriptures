# Śrī Rudram (Namakam and Chamakam)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › संहिता › श्रीरुद्रम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/`, work id `shri-rudram`). The text is Taittirīya Saṃhitā 4.5 (Namakam) and 4.7 (Chamakam), with the opening and closing mantras that are recited with them.

## Sources
- **Text (source of truth).** The owner's printouts of shlokam.org's pages: [rudram-namakam.htm](https://shlokam.org/shloka/rudram-namakam.htm) and [rudram-chamakam.htm](https://shlokam.org/shloka/rudram-chamakam.htm). The Devanagari, with svaras, follows the printout exactly, except for the text-layer repairs and the two typo fixes listed in `reconciliation.md`. That file also records how the text is checked against the page's own transliteration, the page images and the Taittirīya Saṃhitā.
- **Private copies.** The printouts and the recordings are in `scriptures-data`, at `hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/printouts/shlokam/` and `…/audio/shlokam/`.
- **Meanings.** Written for this library, at the owner's request ("don't copy word for word; the meanings in these PDFs are too long; bring the context of Hinduism"). There is one short meaning per mantra in English (`en-scriptures`) and Hindi (`hi-scriptures`), both `order: 1`. They draw on:
  - the page's renderings and word glosses, read as a guide, never copied;
  - the traditional understanding (Sāyaṇa and Bhaṭṭa Bhāskara as commonly summarised, Rudra–Śiva, the Pañcākṣarī in the 8th anuvāka, and the Chamakam as the prayer for every blessing through the yajña).

  Longer context is in the footnotes. The page's English is not in this repository. Its Chamakam English is a summary per anuvāka.
- **Word meanings.** Also written for this library, informed by the page's glosses: 950 Sanskrit words (`glossary/g1–g5.json`), merged into `library/glossary/sa.json`. Glossary keys have no svaras, because the app ignores svara marks when it looks a word up. Five words whose shared entry carries another text's sense (तम्, कृष्ण, भव, न, पतये) have this work's sense in `glossary.json`.

## Files
- `source/extract.py <namakam.pdf> <chamakam.pdf> [private folder]` → `source/namakam_raw.json`, `chamakam_raw.json`: each page block's Devanagari and transliteration lines.
- `source/rudram_text.py`: mends the PDF text layer (`norm_deva`) and converts the page's transliteration back to Devanagari (`tr2deva`) as a second witness.
- `source/settle.py` → `text.json`: the settled text, one item per mantra, with the corrections (`FIX`); the exporter writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `meanings/namakam.json`, `chamakam.json`: our meanings, `{item id: {en, hi, fen?, fhi?}}`. `fen` and `fhi` are footnotes.
- `glossary/g1–g5.json`: word meanings, merged into `library/glossary/sa.json` (add-only). `glossary/work_sa.json` holds this work's own senses, written to `library/…/glossary.json`.
- `export.py` → `work.json`, `meanings/en-scriptures.json`, `meanings/hi-scriptures.json`, `glossary.json`; then run `python3 tools/site/build.py`.
- `audio/shlokam/`: `source.json` and `recordings.json` for the two shlokam.org recordings (YouTube `GbQM33333xs` Namakam, `0Gap1jjn2EM` Chamakam), their transcripts, and hand-checked starts (`fixes.json`, evidence in `fixes.md`). `python3 tools/audio/make_timings.py tools/works/shri-rudram/audio/shlokam` writes the timings. The source is a **draft** (`source.json` → `draft`): the automatic starts are not good enough, so it stays a draft until the owner checks the starts by ear in the app.

Rebuild: `python3 tools/works/shri-rudram/source/settle.py && python3 tools/works/shri-rudram/export.py && python3 tools/site/build.py`. Run `extract.py` again only if the printouts change.

## Structure
- **Parts:** नमकम् and चमकम्.
- **Sections (pages):** each anuvāka is a page (`nam-a01` … `nam-a11`, `cha-a01` … `cha-a11`). There are also an opening page (`nam-purva`), the hymn of names after anuvāka 1 (`nam-bhagavan`), the closing mantras and śānti (`nam-uttara`) and the Chamakam śānti (`cha-shanti`).
- **Items:** one per mantra, ids like `namakam.a08.m11` and `chamakam.a04.m12`, numbered `n` = "anuvāka.mantra" (8.11). The page's numbering stops at the anuvāka, so mantras are split as `reconciliation.md` describes. Ids are permanent.
  - Namakam: 178 items, of which 164 are mantras in anuvākas 1–11.
  - Chamakam: 167 items, of which 166 are mantras.
- **Types** (`work.json` → `types`):
  - mantra (मं॰ / Man.);
  - maṅgala mantra, the opening and inserted invocations (मङ्ग॰ / Maṅg.);
  - heading, the Taittirīya Saṃhitā heading (शी॰ / Hd.);
  - closing mantra (उ॰ / Cl.);
  - śānti mantra (शा॰ / Śā.).
- **Topics:** one per anuvāka, with a short theme (e.g. "Anuvāka 8 — Namaḥ Śivāya"), plus the opening, नमस्ते अस्तु भगवन्, the closing mantras and the Chamakam śānti.
- **Reading plans:** none. The Rudram is recited in one sitting.
