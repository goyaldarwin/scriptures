# Footnotes of the Gita Press English translation (452–453): extraction report

Output: `en_notes.json`, with 240 notes under 198 verse ids, each id `<kāṇḍa>.<sarga key>.<to>`, in reading order. All text comes from the PDF text layer (no OCR). Scripts are in `fn/` (`foot.py`, `notes.py`, `build.py`, `text.py`, plus `parse2.py`, a copy of `code/parse.py` that also records line offsets; its paragraphs match `book.json` exactly).

## How the notes were found
- **Footnote region:** on each page of the seven kāṇḍas (pp. 59–2303 within `parse.KANDA_PAGES`), this is every line below the last body line. Body lines are English in Nalandahel ≥ 10.3 pt, Sanskrit ≥ 13 pt, or headings. Notes are in Nalandatim 10 pt and Chanakya 10–12 pt. Rows at one baseline are joined left → across → right. The dotted elision fills (5.8–6.4 pt, pp. 82, 105, 209) are kept as "…". The stray "." glyphs in the Sanskrit of p. 184 are dropped. Page 71's last line (a body verse at 12.5 pt) is excluded.
- **Note start:** a note starts with `*`, `†`, `‡` or `N.` at the head of a row. A numbered row of Sanskrit inside a note does not start a new note. A row with no mark at the top of a page continues the previous note. There are four run-ons, at pp. 143, 298, 1303 and 1736, and each starts in lower case or inside a quotation.
- **Joining:** the lines are joined into one paragraph and the mark is removed. There are only six line-end hyphens, and each was checked:
  - kept: horse-sacrifice (89), snake-bite (184), Vāstu-Śānti (504, like Graha-Śānti in the same note), Kapiñjalādhikaraṇa-Nyāya (621) and left-like (1810, as printed)
  - removed: after-noon → afternoon (1705)
- **Sanskrit:** quotations are kept as `se_lines.json` decodes them. A few were spot-checked against the page images, but not every one.

## How marks were matched (page by page; the marks restart on each page)
| kind | notes | matching |
|---|---|---|
| `*` | 161 | `*` in a body line. The k-th `*` in reading order is matched to the k-th `*` note. The mark's character offset gives the paragraph. |
| numbers | 77 | Superscript digit lines (5.8–6.4 pt, sometimes "2 3" on one line) are matched by number. The host line is the body line just below the superscript in the same column. |
| `†`, `‡` | 2 | p. 1705 |

The body marks and the notes agree on every page except the cases listed below. The `•` after the verse numbers on pp. 659, 953, 1071 and 1148 are stray dots with no note (checked on p. 659); they are not marks. A mark printed straight after a verse number (e.g. "(165)*", p. 1206) is attached to the paragraph that number closes.

## Attached by position, by content or by special rule (check these)
- **p. 1220 → `sundara.4.2`:** no mark is printed (checked at 250 dpi). The note ("entry into a hostile city without passing through the gate") glosses the English of verses 1–2, so it is attached there by content. The position rule would give `sundara.4.3`.
- **p. 1326 → `sundara.35.19`:** the heading "We read in works on Physiognomy—" has a `*` but no mark in the text. It is kept as its own note, placed before notes 1–15, which all sit in the (17—19) paragraph.
- **pp. 1326–1327:** the footnotes are in two columns and were read column by column. Each numbered Sanskrit quotation is a separate note: 15 under `sundara.35.19` and 4 under `sundara.35.20`. "We have read in the Bālakāṇḍa—" is printed just above item 15 and is joined to it.
- **p. 1793 → `yuddha.76.7`:** eight numbered notes are printed as one run-on paragraph. They were split at "2." to "8." and each was matched to its own superscript. Their closing ":" is kept as printed.
- **p. 871 → `aranya.p1.1`:** the mark is on the heading "An Interpolated Canto*", so the note goes to the first paragraph of that canto.
- **p. 1923 → `yuddha.107.52`:** superscript 1 is on the Sanskrit of verse 51 (गगनं¹). It is attached to the English paragraph (51-52).
- **Mark lines that `parse.py` did not put into the English:** in these cases the paragraph was taken from the preceding English line, and each was checked by eye.
  - p. 650 (mix line, note 1) → `ayodhya.100.70`
  - p. 1557 (12 pt line) → `yuddha.28.4`
  - p. 1705 (`*`, `†` → `yuddha.63.7`; `‡` → `yuddha.63.9`), checked on the image

## Not settled / for the owner
- **p. 2151 (`uttara.38.17`, "in my coronation*"):** the mark is printed but the page has no footnote, and no note follows on the next pages. Nothing is attached.
- **Printed slips kept as printed:** "(l) morning" (1336), "IIwala" (1743), "thier" (647), "propositin" and "eights virtues" (1132), "dynsty" (2012), "Also know as" (2159), "Simhikā His six" (1743), "Sarhvartaka" and "Bhīṣma-Parva of, the" (1329), "Rāmāyaṇa-Śiromaṇi”construes" (496, no space), and "weeping/and" (1303).
- **p. 1475:** the note is only "roughly about 40 Kg." and starts in lower case. It has its own `*` and mark on the same page ("a maund*").
- **Not searched:** pp. 1170–1191 (between Kiṣkindhā and Sundara, outside `KANDA_PAGES`) and the front matter before p. 59.
- **A side finding about `parse.py`:** about 32 body English lines are missing from `book.json`'s English:
  - "mix" lines (English with Devanagari): pp. 139, 197, 201, 262, 343, 488, 614, 650 and others
  - Helvetica-first lines: pp. 201 and 1705 (the first two lines of p. 1705)
  - a 12 pt line: p. 1557
  - a 10.4 pt line: p. 2273
