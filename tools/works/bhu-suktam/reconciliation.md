# Bhū Sūkta — how the text is settled

**Source of truth:** shlokam.org's page "Bhoomi Suktam", <https://shlokam.org/shloka/bhoomi-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/atharvaveda/samhita/bhu-suktam/printouts/shlokam/bhoomi-suktam.html`). It gives 18 verse blocks, each with the Devanagari (no svaras), a transliteration, an English rendering and word glosses; every block ends with its number (॥१॥ … ॥१८॥).

**Which text it is.** The Atharvaveda's Pṛthivī Sūkta (12.1), whose first verse begins सत्यं बृहदृतमुग्रं दीक्षा तपो ब्रह्म यज्ञः पृथिवीं धारयन्ति: eighteen of its verses. Hindupedia's article "Bhusukta" (<https://hindupedia.com/en/Bhusukta>) names two Bhū Sūktas, Atharvaveda Saṃhitā 12.1 and Taittirīya Saṃhitā 1.5.3, the latter the better known; the page is the former. Whether the recording sings this text is for its transcript to show (README).

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari (`shlokam.tr2deva`) and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions (a nasal before a consonant written as its class letter or as ṃ). All 41 lines agree letter for letter.
3. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: the one correction rests on the grammar and the page itself, where the page is clearly wrong. The check against independent witnesses is a later step.
4. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥ and compact verse numbers, Pāṇini's spelling (a class nasal inside a word: the page's असंबाधं, संबभूवुः), the ISO 15919 transliteration made from the verse.

## Corrections (all in `source/settle.py` → `FIX`)

| Verse | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 16 | …वाचो मधु पृथिवी धेहि मह्यम् | …वाचो मधु पृथिवि धेहि मह्यम् | The Earth is addressed (धेहि, "give"): the vocative पृथिवि, as the page writes it in verses 11, 12 and 15; पृथिवी is the nominative. |

## Kept as the page has it
- **Verse 16** is one line (ता नः प्रजाः सं दुह्रतां …). The page's Devanagari has an empty line before it (an empty `<br>` line); its transliteration has the one line only. The empty line is dropped.
- **The page's selection and its numbers** (1–18), not the hymn's own verse numbers.
- **Readings, as printed:** बध्यतो (verse 2), अजीतेऽहतो (verse 11): valid words, kept.

## Structure (not on the page as such)
- **Numbering.** Each mantra keeps the number the page prints (1–18).
- **Sections:** one, `sukta`.
