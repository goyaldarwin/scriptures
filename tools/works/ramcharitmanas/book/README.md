# Book pipeline: Gita Press PDFs → `app_data.json`

The scripts run in this folder, which is also where they read and write their files. Only the first stage needs the PDFs. Every intermediate file is kept here, so any later stage can be rerun without them.

PDFs (not in the repository): `HINDI_PDF=…/Hindi.pdf ENGLISH_PDF=…/English.pdf`. These are the owner's Gita Press editions: Hindi with bhāvārtha, and English with transliteration and translation.

| Stage | Scripts | Output |
|---|---|---|
| Hindi PDF: read the glyphs | `hi_trace.py` | `hi_trace.pkl` (large and not committed; rerun to make it) |
| Hindi: decode the glyphs into Unicode | `hi_decode.py`, `glyph_sheets.py`, `glyph_render.py`, `glyph_check.py` | `hi_unmapped.json`, `glyph_stats.json` |
| Hindi: pages → text → verses | `hi_pages.py`, `hi_parse.py`, `build_data.py` | `hi_text.json`, `hi_toc.json`, `hi_units_raw.json`, `hi_items.json` |
| Hindi: cross-check with OCR | `ocr.sh` (tesseract), `cmp_ocr.py`, `verify_ocr.py`, `crops.py` | `ocr1/`, `verify_ocr.json` |
| English PDF → verses | `en_extract.py`, `en_extract2.py`, `en_parse.py`, `en_units.py` | `en_rows.json`, `en_lines.json`, `en_toc.json`, `en_units.json` |
| Transliteration ↔ Devanagari | `tr2dev.py`, `verify.py` | `verify_tr.json` |
| Align Hindi and English | `align.py`, `build2.py`, `variants.py` | `align_*.json`, `merged.json`, `variants.json` |
| Topics (section headings) | `topics_prep.py`, `topics_final.py` | `topics_*.json`, `topic_starts_*.json`, `topics_final.json` |
| Word meanings | glossary batches `gloss_in_*`/`gloss_out_*`, `gloss2_*` | `gloss_final.json` (14,807 words) |
| English split per verse | `split/prep.py` → `split/out_*.json`; `split/apply_lib.py`, `split/en_fix2.py`, `split/tr_fix.py`; spec in `split/SPEC.md` | applied inside `make_appdata.py` |
| Pārāyaṇa vidhi | `split/vidhi.py`, `split/vidhi_gloss.py` | applied inside `make_appdata.py` |
| **Final data** | `make_appdata.py`, `make_appdata_helpers.py` (applies `text_fixes.json`, topics, glossary, splits, vidhi) | **`app_data.json`** |
| Report | `make_report.py` | |

Text corrections go in `text_fixes.json`. Then run `python3 make_appdata.py` here and `python3 ../export.py`. Do not hand-edit `app_data.json`.

`gloss_final.json` was the starting point of `library/gloss.json`. Correct word meanings in `library/gloss.json` now.
