# Book pipeline: Gita Press PDFs → `app_data.json`

The scripts run in this folder, which is also where they read and write their files. Only the first stage needs the PDFs. Every intermediate file is kept here, so any later stage can be rerun without them.

PDFs (not in the repository): `HINDI_PDF=…/hindi.pdf ENGLISH_PDF=…/english.pdf` (in `scriptures-data`, see `../README.md`). These are the owner's Gita Press editions: Hindi with bhāvārtha, and English with transliteration and translation.

| Stage | Scripts | Output |
|---|---|---|
| Hindi PDF: read the glyphs | `hi_trace.py` | `hi_trace.pkl` (large and not committed; rerun to make it), `hi_unmapped.json` |
| Hindi: decode the glyphs into Unicode | `hi_decode.py` (the glyph table); `glyph_sheets.py`, `glyph_render.py`, `glyph_check.py` to check it (they need the PDF's fonts saved as `font_16.ttf`, `font_19.ttf`) | `glyph_stats.json` |
| Hindi: pages → text → verses | `hi_pages.py`, `hi_parse.py`, `build_data.py` | `hi_text.json`, `hi_units_raw.json`, `hi_items.json` |
| Hindi: cross-check with OCR | `ocr.sh` (tesseract), `cmp_ocr.py`, `verify_ocr.py`, `crops.py` | `ocr1/`, `verify_ocr.json` |
| English PDF → verses | `en_extract2.py`, `en_units.py` | `en_rows.json`, `en_units.json` |
| Transliteration ↔ Devanagari | `tr2dev.py`, `verify.py` | `verify_tr.json` |
| Align Hindi and English | `align.py`, `build2.py` | `align_*.json`, `merged.json` |
| Topics (section headings) | `topics_prep.py` (reads the books' contents pages, `hi_toc.json` and `en_toc.json`; no script here makes them), `topics_final.py` (with `make_appdata_helpers.py`) | `topics_*.json`, `topic_starts_*.json`, `topics_final.json` |
| Word meanings | — | `gloss_final.json` (14,807 words) |
| English split per verse | `split/prep.py` → `split/chunk*.txt`, `split/groups.json` (made when a split is redone, not kept); the split points, judged by reading, in `split/out_*.json` (method in `split/SPEC.md`); `split/apply_lib.py`, `split/en_fix2.py`, `split/tr_fix.py` | applied inside `make_appdata.py` |
| Pārāyaṇa vidhi | `split/vidhi.py`, `split/vidhi_gloss.py` | applied inside `make_appdata.py` |
| **Final data** | `make_appdata.py` (applies `text_fixes.json`, topics, glossary, splits, vidhi) | **`app_data.json`** |

Text corrections go in `text_fixes.json`. Then run `python3 make_appdata.py` here and `python3 ../export.py`. Do not hand-edit `app_data.json`.

`gloss_final.json` is the Mānas's word list as it entered `library/glossary/`; `export.py` adds only the words the dictionaries lack. Correct word meanings in `library/glossary/<lang>.json`.
