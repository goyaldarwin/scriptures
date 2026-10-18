# Śrī Rāmacaritamānasa (Gita Press, Gorakhpur)

- `book/`: the Hindi and English Gita Press editions → `book/app_data.json`. See `book/README.md` for every stage.
- `export.py`: `app_data.json` → `library/hindu/granth/tulsidas/ramcharitmanas/` (`work.json`, `meanings/hi-gitapress.json`, `meanings/en-gitapress.json`) and new words into `library/glossary/sa.json` / `awa.json`, by the language of each verse.
- `audio/kamlesh-upadhyay/`: the inputs for the audio source. See `tools/audio/README.md`.

Item ids look like `bal.86.cau4`: kāṇḍa, dohā section, type, number. They are permanent.

## Sources (private repo `scriptures-data`)
- `hindu/granth/tulsidas/ramcharitmanas/books/gitapress/hindi.pdf`, `english.pdf`: the two Gita Press editions read by `book/` (set `HINDI_PDF`, `ENGLISH_PDF` to these).
- `hindu/granth/tulsidas/ramcharitmanas/audio/kamlesh-upadhyay/`: the recordings transcribed into `audio/kamlesh-upadhyay/transcripts/` (set `AUDIO_DIR` to this folder).
