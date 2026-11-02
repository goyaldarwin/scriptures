# Śrīmad Vālmīki Rāmāyaṇa

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
- **Witnesses of the text** (`reconciliation.md`): the owner's scrapes of the IIT Kanpur / Rashtriya Sanskrit Vidyapeetha, Tirupati site (valmiki.gitasupersite.in) and of valmikiramayan.net (sanskritdocuments.org copy), both Bāla to Yuddha, in `scriptures-data` at `printouts/iitk/` and `printouts/valmikiramayan-net/`. Their Sanskrit is in `source/witness/`; their translations and word meanings are kept private and only used to check.

## Ids and structure
- A verse is `<kāṇḍa>.<sarga>.<verse>` with the book's numbers (`bala.1.1`, `sundara.15.30`); a later addition's sarga is `p1`, `p2` (`aranya.p1.3`, `uttara.p2.10`). Parts are the kāṇḍas; a section (page) is a sarga (`bala.1`).
- The verse number ends the verse's last line (॥१॥). Long-metre verses keep the book's line per pāda.
- The English is Gita Press's, under the verse it translates; where the book translates several verses together (its mark `(19—22)`), the meaning sits under the last of them, with the mark as printed.

## How it is made
```bash
S=tools/works/valmiki-ramayana/source
python3 $S/extract.py <scriptures-data>/hinduism/granth/valmiki/ramayana/books/gitapress/sanskrit-english.pdf   # → spans
python3 $S/build_lines.py $S <spans> <lines>          # every line decoded, well-formedness checked
python3 $S/parse.py <lines> <book>                    # kāṇḍa → sarga → verses and English paragraphs
python3 $S/run_wit.py $S <book> <iitk scrape> <diffs> iitk   # and the same for valmikiramayan.net (vr)
python3 $S/settle.py <book> $S/review/corrections.final.json …   # the text and the copied English
```
`reconciliation.md` lists every difference from the book and why.
