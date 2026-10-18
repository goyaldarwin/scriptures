# Tools

Everything used to make `library/` and the website. Run all commands from the repository root. Procedures are in `docs/HOW-TO.md`.

```
tools/
  site/                          the app (shared by every work)
    app.js                         all behaviour → app/app.js
    index_template.html            layout + styles → index.html, app/style.css
    library.py                     registers each work's sources and checks the whole library
    build.py                       runs library.py, then builds the website and dist/
  audio/                         audio sources (shared by every work)
    transcribe.py                  recordings → transcripts (Whisper speech recognition)
    align.py                       matches transcript lines to verses
    make_timings.py                transcripts → library/<work>/audio/<id>.json
  fonts/                         Noto Serif Devanagari, Literata, Gentium (transliteration subset)
  works/                         one folder per work: how its data was made
    ramcharitmanas/
      book/                        Gita Press PDFs → book/app_data.json (see its README)
      export.py                    app_data.json → library/tulsidas/ramcharitmanas/ (text + Gita Press meanings)
      audio/kamlesh-upadhyay/      source.json, recordings.json, transcripts/
    shirdi-sai-dhoop-aarti/
      text.txt                     the verse text (settled in reconciliation.md)
      meanings/hi.json, en.json    one meaning per verse
      glossary/mr|sa|hi.json       word meanings by language
      export.py                    → library/aarti/shirdi-sai/dhoop-aarti/ and library/glossary/
```

## Rebuild everything (Rāmacaritamānasa)
```bash
(cd tools/works/ramcharitmanas/book && python3 make_appdata.py)                 # book data (no PDFs needed)
python3 tools/works/ramcharitmanas/export.py                                     # → library/…/work.json, meanings/
python3 tools/audio/make_timings.py tools/works/ramcharitmanas/audio/kamlesh-upadhyay   # → library/…/audio/
python3 tools/site/build.py                                                      # check + website + dist/
```
Needs Python 3 with `numpy`. Transcription also needs `faster-whisper` and `ffmpeg`; reading the PDFs again needs `pymupdf` and `tesseract`; tests need `playwright`.
