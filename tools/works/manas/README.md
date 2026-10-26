# श्रीरामचरितमानस (Śrī Rāmacaritamānasa)

Gosvāmī Tulasīdāsa's Rāmāyaṇa in Awadhi (`awa`, with Sanskrit `sa` ślokas and stutis), in the Gita Press (Gorakhpur) edition: seven kāṇḍas, every verse, with the 30-day and 9-day reading plans and the pārāyaṇa vidhi.

- **Text** (`text.txt`): made by `source/make.py` from the two Gita Press editions (`source/README.md`: every stage from the PDFs to `source/app_data.json`); every choice: `reconciliation.md`. `book.json` (made by `source/make.py`, included by `work.json`): the reading plans, the vidhi with the kathā-visarjana (`source/visarjan.json`, its source and readings in `source/visarjan.md`), and `renamed` / `split` for the joint caupāīs.
- **Meanings:** Gita Press's Hindi bhāvārtha and English translation (`meanings/hi/gitapress.json`, `meanings/en/gitapress.json`, made by `source/make.py`), shown first; ours (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`, `partial`: the Sundarakāṇḍa and the verses other works take). `topics.json`: our topic headings, shown by the Sundarakāṇḍa (the Mānas shows Gita Press's).
- **Recordings:** `audio/kamlesh-upadhyay/`: live; the starts the owner set by ear in `owner.json`.
- **Taken by:** the Sundarakāṇḍa (`tools/works/sundarkand/`) and Śrī Rāmacandra Kṛpālu, so a correction here reaches them at the next export.

Verse ids look like `bal.86.cau4`: kāṇḍa, dohā section, type, number. Verse types: `cau` (caupāī), `do` (dohā), `so` (sorathā), `cha` (chanda), `shloka`. The folder's format: `tools/works/README.md`.

## Sources (private repo `scriptures-data`)
- `hinduism/granth/tulsidas/ramcharitmanas/books/gitapress/hindi.pdf`, `english.pdf`: the two Gita Press editions read by `source/` (set `HINDI_PDF`, `ENGLISH_PDF` to these).
- `hinduism/granth/tulsidas/ramcharitmanas/books/visarjan-print/visarjan.jpg`: the owner's printed page of the Kathā-visarjana.
- `hinduism/granth/tulsidas/ramcharitmanas/audio/kamlesh-upadhyay/`: the recordings transcribed into `audio/kamlesh-upadhyay/transcripts/` (set `DATA_DIR` to the clone of `scriptures-data`; `recordings.json` → `data` names each file).
