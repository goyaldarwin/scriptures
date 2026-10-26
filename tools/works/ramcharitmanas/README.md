# Śrī Rāmacaritamānasa (Gita Press, Gorakhpur)

- `book/`: the Hindi and English Gita Press editions → `book/app_data.json`. See `book/README.md` for every stage.
- `export.py`: `app_data.json` → `library/hinduism/granth/tulsidas/ramcharitmanas/` (`work.json`, `meanings/hi-gitapress.json`, `meanings/en-gitapress.json`, `meanings/hi-scriptures.json`, `meanings/en-scriptures.json`) and new words into `library/glossary/sa.json` / `awa.json`, by the language of each verse.
- `meanings/`: our own meanings (`hi.json`, `en.json`, written to `tools/meanings/style.md`) → the sources `hi-scriptures` and `en-scriptures`; `topics.json`: our own topic headings, used by the Sundarakāṇḍa work (the Mānas shows Gita Press's headings).
- `visarjan.json`: the Kathā-visarjana page (text, meanings and word meanings), read by `export.py`. Its source and readings: `visarjan.md`.
- `audio/kamlesh-upadhyay/`: the inputs for the audio source (`recordings.json`, `transcripts/`, and `owner.json`, the starts the owner set by ear). See `tools/audio/README.md`.

Item ids look like `bal.86.cau4`: kāṇḍa, dohā section, type, number. They are permanent.

## Sources (private repo `scriptures-data`)
- `hinduism/granth/tulsidas/ramcharitmanas/books/gitapress/hindi.pdf`, `english.pdf`: the two Gita Press editions read by `book/` (set `HINDI_PDF`, `ENGLISH_PDF` to these).
- `hinduism/granth/tulsidas/ramcharitmanas/books/visarjan-print/visarjan.jpg`: the owner's printed page of the Kathā-visarjana.
- `hinduism/granth/tulsidas/ramcharitmanas/audio/kamlesh-upadhyay/`: the recordings transcribed into `audio/kamlesh-upadhyay/transcripts/` (set `DATA_DIR` to the clone of `scriptures-data`; `recordings.json` → `data` names each file).
