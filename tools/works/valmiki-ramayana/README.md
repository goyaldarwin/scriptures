# Śrīmad Vālmīki Rāmāyaṇa (Shrimad Valmiki Ramayan)

The Ādikāvya of Maharṣi Vālmīki in its seven kāṇḍas, as printed by Gita Press, Gorakhpur: 23,701 verses in 645 sargas and 3 later additions (प्रक्षिप्त सर्ग, one in the Araṇya-kāṇḍa after sarga 56, two in the Uttara-kāṇḍa after sarga 59), kept where the book prints them.

| Kāṇḍa | Sargas | Verses |
|---|---|---|
| Bāla | 77 | 2,270 |
| Ayodhyā | 119 | 4,304 |
| Araṇya | 75 + 1 | 2,473 |
| Kiṣkindhā | 67 | 2,462 |
| Sundara | 68 | 2,865 |
| Yuddha | 128 | 5,788 |
| Uttara | 111 + 2 | 3,539 |

## Sources
- **Text and English meaning:** the owner's Gita Press *Śrīmad Vālmīki-Rāmāyaṇa, with Sanskrit text and English translation* (codes 452–453, revised edition, parts I–II), in `scriptures-data` at `books/gitapress/sanskrit-english.pdf`. The text is read from the book's text layer, never by OCR (the owner's rule): the Devanagari is set in the legacy Chanakya font, whose 171 codes are mapped to Unicode in `source/chanakya.py` (each code read from the shape of the glyph in the font embedded in the PDF, `source/glyphsheet.py`, and confirmed by the words it occurs in); the English is in the Nalanda fonts, whose diacritics are mapped in `source/english.py`.
- **Hindi meaning:** the owner's Gita Press *Śrīmad Vālmīkīya Rāmāyaṇa*, Hindi translation only (code 77), in `scriptures-data` at `books/gitapress/hindi.pdf`, read from its glyph ids (the font is Noto Sans Devanagari; its text layer maps the conjuncts to wrong characters).
- **Witnesses of the text** (`reconciliation.md`): the owner's scrapes of the IIT Kanpur / Rashtriya Sanskrit Vidyapeetha, Tirupati site (valmiki.gitasupersite.in) and of valmikiramayan.net (sanskritdocuments.org copy), both Bāla to Yuddha, in `scriptures-data` at `printouts/iitk/` and `printouts/valmikiramayan-net/`. Their Sanskrit is in `source/witness/`; their verse translations are kept private and only used to check.
- **Word meanings** (`glossary/sa.json`, the senses shown when a word of a verse is tapped): the English is the witnesses' word-by-word gloss copied as they give it: IIT Kanpur's, else valmikiramayan.net's, the one that fits the verse where they differ, ours only where neither glosses the word or a part of it. Where each entry's English comes from is in `source/words/src.json`. The Hindi, the root (`r`), the grammar (`g`) and the parts of a joined word (`p`) are ours, each checked in Monier-Williams and Apte. They are written per kāṇḍa from word packets (`source/words/packets.py`: every new word with up to three of its verses and the witnesses' glosses of those verses) by the brief `source/words/BRIEF.md`, then merged by `source/words/merge.py`.

## Sources and permissions
All the sources are the owner's copies, used for personal study: the Gita Press books (Sanskrit text, English and Hindi meanings, shown as printed) and the two websites' word-by-word glosses (shown as given in the word meanings). No permission has been requested from Gita Press, IIT Kanpur / Rashtriya Sanskrit Vidyapeetha, Tirupati, or valmikiramayan.net.

## Structure
- **Hierarchy:** seven kāṇḍas (parts: Bal Kand … Uttar Kand) › sargas (sections `bala.1` … , numbered: `work.json` → `cite.sec` names them "Sarga" / "सर्ग") › verses. The three later additions (प्रक्षिप्त सर्ग) are sections of their own where the book prints them, with names (`work.json` → `sections`): `aranya.p1` after Araṇya 56, `uttara.p1` and `uttara.p2` after Uttara 59 ("Interpolated sarga 1").
- **Numbering:** a verse's id is `<kāṇḍa>.<sarga>.<verse>` with the book's numbers (`bala.1.1`, `sundara.15.30`, `aranya.p1.3`); its `n` is its number in the sarga, the number that ends its last line (॥३०॥). It is cited sarga.verse within its kāṇḍa (`work.json` → `cite`: "Shloka 15.30" in the player, Resume and search; its place "Sarga 15 · Shloka 30"); a verse of an interpolated sarga by its own number, the sarga's name beside it. In search, "15.30" finds that verse in each kāṇḍa and "15" (or "Sarga 15") opens Sarga 15 of each. Long-metre verses keep the book's line per pāda.
- **Types:** `shloka`. **Topics:** the book's Hindi and English sarga titles. **Meanings:** Gita Press's English under the verse it translates; where the book translates several verses together (its mark `(19—22)`), the meaning sits under the last of them, with the mark as printed. **Loading:** by kāṇḍa (`"load": "parts"`). **Reading plans:** none yet.

## How it is made
```bash
S=tools/works/valmiki-ramayana/source
python3 $S/extract.py <scriptures-data>/hinduism/granth/valmiki/ramayana/books/gitapress/sanskrit-english.pdf   # → spans
python3 $S/build_lines.py $S <spans> <lines>          # every line decoded, well-formedness checked
python3 $S/parse.py <lines> <book>                    # kāṇḍa → sarga → verses and English paragraphs
python3 $S/run_wit.py $S <book> <iitk scrape> <diffs> iitk   # and the same for valmikiramayan.net (vr)
python3 $S/settle.py <book> $S/review/corrections.final.json <verses> <english>   # the settled verses and the copied English
python3 $S/plain_en.py                                # the headings' English in plain spelling (Shri Ram, Lakshman), in text.txt
```
`text.txt` was assembled once from `settle.py`'s verses and the two books' sarga titles; no script in the repository writes it, so `text.txt` is the work's source from here on, every change to it recorded in `reconciliation.md`.
`reconciliation.md` lists every difference from the book and why.
