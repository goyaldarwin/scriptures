# श्रीरामचरितमानस (Śrī Rāmacaritamānasa)

Gosvāmī Tulasīdāsa's Rāmāyaṇa in Awadhi (`awa`, with Sanskrit `sa` ślokas and stutis), in the Gita Press (Gorakhpur) edition: seven kāṇḍas, every verse, with the 30-day and 9-day reading plans and the pārāyaṇa vidhi.

- **Text** (`text.txt`): made by `source/make.py` from the two Gita Press editions (`source/README.md`: every stage from the PDFs to `source/app_data.json`); every choice: `reconciliation.md`. `book.json` (made by `source/make.py`, included by `work.json`): the reading plans, the vidhi with the kathā-visarjana (`source/visarjan.json`, its source and readings in `source/visarjan.md`), and `renamed` / `split` for the joint caupāīs.
- **Meanings:** Gita Press's Hindi bhāvārtha and English translation (`meanings/hi/gitapress.json`, `meanings/en/gitapress.json`, made by `source/make.py`), shown first; ours (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`, every verse, one piece per verse line). `topics.json`: our topic headings, shown by the Sundarakāṇḍa (the Mānas shows Gita Press's).
- **Recordings:** `audio/kamlesh-upadhyay/`: live; the starts the owner set by ear in `owner.json`.
- **Taken by:** the Sundarakāṇḍa (`tools/works/sundarkand/`) and Śrī Rāmacandra Kṛpālu, so a correction here reaches them at the next export.

Verse ids look like `bal.86.cau4`: kāṇḍa, dohā section, type, number. Verse types: `cau` (caupāī), `do` (dohā), `so` (sorathā), `cha` (chanda), `shloka`. The folder's format: `tools/works/README.md`.

## Sources (private repo `scriptures-data`)
- `hinduism/granth/tulsidas/ramcharitmanas/books/gitapress/hindi.pdf`, `english.pdf`: the two Gita Press editions read by `source/` (set `HINDI_PDF`, `ENGLISH_PDF` to these).
- `hinduism/granth/tulsidas/ramcharitmanas/books/visarjan-print/visarjan.jpg`: the owner's printed page of the Kathā-visarjana.
- `hinduism/granth/tulsidas/ramcharitmanas/audio/kamlesh-upadhyay/`: the recordings transcribed into `audio/kamlesh-upadhyay/transcripts/` (set `DATA_DIR` to the clone of `scriptures-data`; `recordings.json` → `data` names each file).

## Structure
- **Hierarchy:** seven kāṇḍas (parts) › dohā sections › verses. A section is a dohā with the caupāīs, chhandas and ślokas before it ("Dohā 2" = the caupāīs before dohā 2 and dohā 2); the opening ślokas and sorathās of a kāṇḍa are section `0`, the closing ślokas of the Uttara-kāṇḍa the section `end` ("Closing", `work.json` → `sections`).
- **Numbering:** (`work.json` → `cite`) a verse's `n` is its number in its section as Gita Press prints it (a caupāī's number the app shows at its end); a verse is cited dohā.verse ("Verse 106.3", a chhanda "Chhand 10.1"), a dohā or sorathā by its own number ("Doha 106", "Doha 3क"), the ślokas of section 0 and `end` by theirs ("Shloka 1"). Where Gita Press numbers a second run of chhandas under one dohā from 1 again, `cite.repeat` lists it (Araṇya 20, Laṅkā 101).
- **Types:** `cau`, `do`, `so`, `cha`, `shloka`. **Topics:** Gita Press's headings. **Reading plans:** the 30-day Māsa-pārāyaṇa and the 9-day Navāhna (`book.json`).

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- The text itself: Bal Kand 34, the date and place it was begun (our text, from the Gita Press edition).
- Wikipedia, "Ramcharitmanas" (https://en.wikipedia.org/wiki/Ramcharitmanas): Awadhi, structure and metres, the three dialogues, its relation to Valmiki, Ramlila and the parayans, UNESCO 2024.
