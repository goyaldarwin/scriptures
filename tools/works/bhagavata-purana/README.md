# श्रीमद्भागवतमहापुराण (Shrimad Bhagavat Mahapuran)

Shelf: हिन्दू धर्म › पुराण › महापुराण › श्रीमद्भागवतमहापुराण (`library/hinduism/purana/mahapurana/bhagavata/`, work id `bhagavata-purana`). The Śrīmad Bhāgavata Mahāpurāṇa of Maharṣi Vedavyāsa in its twelve skandhas and 335 adhyāyas, as printed by Gita Press, Gorakhpur, with the Śrīmad Bhāgavata Māhātmya of the Padma Purāṇa (six adhyāyas) that the book prints before it: 14,603 numbered verses and prose passages, in Sanskrit (`sa`).

| Part | Adhyāyas | Verses |
|---|---|---|
| Māhātmya | 6 | 504 |
| Skandha 1 | 19 | 809 |
| Skandha 2 | 10 | 391 |
| Skandha 3 | 33 | 1,411 |
| Skandha 4 | 31 | 1,445 |
| Skandha 5 | 26 | 668 |
| Skandha 6 | 19 | 851 |
| Skandha 7 | 15 | 750 |
| Skandha 8 | 24 | 931 |
| Skandha 9 | 24 | 964 |
| Skandha 10 | 90 | 3,946 |
| Skandha 11 | 31 | 1,367 |
| Skandha 12 | 13 | 566 |

## Sources
- **Text and Hindi meaning:** the owner's Gita Press *Śrīmad Bhāgavata Mahāpurāṇa, saral Hindī vyākhyā sahit*, parts 1–2 (codes 26–27: skandhas 1–8 with the Māhātmya, and 9–12), in `scriptures-data` at `books/gitapress/bhag-1.pdf` and `books/gitapress/bhag-2.pdf`. They are calibre prints of the e-book, Devanagari in embedded subsets of Noto Sans Devanagari Regular and Bold version 1.05 (googlefonts/noto-fonts, tag `v2015-09-29-license-adobe`), whose text layer drops most conjuncts. The text is read from the glyph ids, never by OCR (`source/decode.py`): every glyph's outline equals the official font's, every run of glyphs is decoded by matching the glyph sequences of 6.6 million syllables shaped with the official fonts (HarfBuzz), and every decoded run is shaped again and compared with the PDF's glyphs. Every run decodes; the only runs that do not shape back are the e-book's ई drawn as इ with a hook (21), which decode to ई.
- **Witnesses** for the six verses the e-book leaves out (10.33.17–22): vedabase.io (ŚB 10.33.16–18 there) and wisdomlib.org's Bhāgavata Purāṇa [sanskrit] (10.33.20–22), as `reconciliation.md` records. The owner asked for web lookups wherever the book is in doubt.
- **Meanings:** Gita Press's Hindi (`meanings/hi/gitapress.json`), copied as printed. No English meaning yet.
- **Word meanings:** not written yet (`work.json` → `"words": "partial"`, the owner's choice: the work goes live with its verses and Hindi meanings first).

## Sources and permissions
The Gita Press books are the owner's copies, used for personal study; the text and the Hindi are shown as printed. No permission has been requested from Gita Press.

## Audio
`audio/sanskrit-parayan/`: the whole Bhāgavata recited in Sanskrit, the Māhātmya first, in 30 YouTube recordings (48 hours; the reciter is not named in the owner's files). Transcribed with Whisper on GitHub (`transcribe` workflow), matched to the text by anchors (`"align": "anchors"`). Each recording starts where the one before it ends; `recordings.json` → `from` and `to` give those bounds, each recording begins at its first verse heard among a run of matched verses, and the alignment caches keep only the matches inside its bounds. 14,309 of the 14,945 items have a start; the rest (the first verses of some recordings, much of the Sanskrit prose of Skandha 5, which the recogniser hears poorly), and 12.13.19–23 at the end of the last recording, which after 12.13 goes on with matter not in this text. A draft (`source.json` → `draft`) until the owner has checked the starts by ear.

## Structure
- **Hierarchy:** thirteen parts (the Māhātmya, then Skandh 1 … Skandh 12) › adhyāyas (sections `m.1` … `m.6`, `1.1` … `12.13`; numbered: `work.json` → `cite.sec` names them "Adhyay" / "अध्याय") › verses.
- **Numbering:** a verse's id is `<skandha>.<adhyāya>.<verse>` with the book's numbers (`1.1.1`, `10.33.17`); in the Māhātmya `m.<adhyāya>.<verse>`. Its `n` is the number that ends it (॥१७॥). A verse of a skandha is cited skandha.adhyāya.verse (`work.json` → `cite`: "Shloka 10.33.17"); a verse of the Māhātmya (type `mshloka`) adhyāya.verse within the Māhātmya ("Shloka 3.12"). The Māhātmya's opening verse (कृष्णं नारायणं वन्दे, `m.1.0`) and each adhyāya's closing words (`<adhyāya>.iti`) have no number and are named by their type.
- **Types:** `shloka`; `mshloka` (a śloka of the Māhātmya); `gadya` (the Sanskrit prose, set in bold in the book: most of Skandha 5 and a few passages elsewhere; one item per numbered passage); `iti` (the closing words of each adhyāya). A speaker's line (श्रीशुक उवाच, सूत उवाच) is the first line of the verse it opens, as the book prints it above that verse.
- **Lines:** one line per half-verse for anuṣṭubh, one per pāda for longer metres; the e-book's narrow column wraps a long pāda in two, and those two are one line here.
- **Topics:** the book's Hindi adhyāya titles; the English is their plain English (`source/topics_en.tsv`). **Meanings:** each of the book's Hindi paragraphs sits under the last verse its mark names (॥ ३२-३३ ॥ under 33), every mark kept as printed. **Loading:** by part (`"load": "parts"`).
- **Reading plan:** Saptāha (7 days), its days ending where the book's saptāha method (पारायण-विधि, from the Padma Purāṇa's verse मनुकर्दमसंवादपर्यन्तं प्रथमेऽहनि …) ends them: Manu and Kardama's dialogue (3.22), Bharata's story (5.14), the end of Skandha 7 (7.15), Śrī Kṛṣṇa's birth (10.3), Rukmiṇī's marriage (10.54), the Haṁsa teaching (11.13), the rest (12.13). The Māhātmya is read on the first day.

## How it is made
```bash
S=tools/works/bhagavata-purana/source
D=<clone of scriptures-data>/hinduism/purana/mahapurana/bhagavata/books/gitapress
python3 $S/fonts.py                                   # the official Noto Sans Devanagari 1.05 Regular and Bold (from GitHub)
python3 $S/fontcheck.py $D/bhag-1.pdf; python3 $S/fontcheck.py $D/bhag-2.pdf   # every embedded glyph equals the official font's
python3 $S/survey.py                                  # the glyph-sequence table (table.pkl, not kept: 400 MB)
python3 $S/runall.py $D/bhag-1.pdf p1.pkl && python3 $S/runall.py $D/bhag-2.pdf p2.pkl   # every page decoded and shaped back
python3 $S/survey2.py && python3 $S/survey3.py        # the table grown by the conjuncts the first pass found, the font's other characters
python3 $S/runall.py $D/bhag-1.pdf p1.pkl && python3 $S/runall.py $D/bhag-2.pdf p2.pkl   # again: now every run decodes
python3 $S/lines.py                                   # → lines.json: every line with its position, size, weight
python3 $S/parse.py && python3 $S/verses.py && python3 $S/hindi.py   # → book2.json: parts › adhyāyas › verses, Hindi paragraphs
python3 $S/notes.py                                   # the book's notes (* † ‡) paired with their marks; anything left over → notes_unpaired.json
python3 $S/make_text.py tools/works/bhagavata-purana   # text.txt and meanings/hi/gitapress.json (with the notes)
```
The steps read the owner's PDFs from `scriptures-data`, so `regen_check.py` cannot run them: after changing a script, run them and diff `text.txt`. Corrections of the book are in `source/corrections.json` and `source/missing.json`; the sequence repairs are made by `verses.py` and `hindi.py` and logged. `reconciliation.md` lists every difference from the book and why.
