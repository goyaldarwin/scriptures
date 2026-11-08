# Japji Sahib — how the text is settled

Source of truth: the owner's PDF, SikhNet's “1 - Japji [Gurmukhi]” (37 pages, Gurmukhi only). Private copy:
`scriptures-data/sikhism/gurbani/guru-nanak-dev/japji-sahib/books/sikhnet/japji.pdf`.

## 1. Reading the PDF

The text layer is clean (`source/extract.py` → `source/pdf.txt`, 488 printed lines on pages 2–37; page 1 is a cover).
The Gurmukhi is in **GurbaniAkharHeavy**, the common legacy encoding (ASCII letters drawn as Gurmukhi), converted with
the Sukhmani Sahib's converter, `tools/works/sukhmani-sahib/source/gurmukhi.py` (its decisions:
`tools/works/sukhmani-sahib/reconciliation.md` §2). `µ` (a tippi form, in ਅਨੰਤ, ਅਨੰਦੁ) is in its table. No OCR.

## 2. Lines

The PDF wraps long padas over two printed lines and sets short ones two to a line; `source/make.py` undoes the layout,
so that each line of `text.txt` is one pada, ending with ॥ (or ॥N॥). The Mool Mantar has no ॥ inside: it keeps the
four lines the PDF prints (ੴ ਸਤਿ ਨਾਮੁ ਕਰਤਾ ਪੁਰਖੁ / ਨਿਰਭਉ ਨਿਰਵੈਰੁ / ਅਕਾਲ ਮੂਰਤਿ ਅਜੂਨੀ ਸੈਭੰ / ਗੁਰ ਪ੍ਰਸਾਦਿ ॥).

## 3. The one difference from the PDF

- **॥ ਜਪੁ ॥** — the PDF prints the title as “ਜਪੁ ॥”, without the opening ॥. Sri Guru Granth Sahib (Ang 1) prints
  ॥ ਜਪੁ ॥, and so do both witnesses below (the Shabad OS database, the owner's study sheet); `make.py` writes ॥ ਜਪੁ ॥.

## 4. Checks (`source/check.py`)

1. **Structure and conversion** (always): 42 items (Mool Mantar, ॥ ਜਪੁ ॥, the opening salok ending ॥੧॥, pauris
   1–38 each ending with its own number, the closing salok ending ॥੧॥), 388 lines; every line is Gurmukhi, with no
   bare vowel bearer.
2. **Witnesses** (scratch copies, not committed):
   - **The Shabad OS database** (`@shabados/database` 4.8.7 on npm; its bani “Jap Ji Sahib”, Ang 1–8), vishraam marks
     `; . ,` removed, compared word by word: **2,536 words each, 0 differences**; ॥ marks 426 each (the same division
     into padas).
   - **`gurmukhi-utils` 3.2.2** (Shabad OS's own ASCII→Unicode converter, run with node) on every printed line of the
     PDF: **488 of 488 lines identical** to `gurmukhi.py`'s output.
   - **The owner's earlier study sheet** (`scriptures-data/…/japji-sahib/meaning-records/en-scriptures/study-sheet.md`,
     Unicode Gurmukhi typed independently of this PDF): **2,536 words each, 0 differences**.

Run: `python3 tools/works/japji-sahib/source/check.py --shabados <database.sqlite> --gurmukhi-utils <package dir> --md <study-sheet.md>`.
