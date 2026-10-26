# Tools

Everything used to make `library/` and the website. Run all commands from the repository root. Procedures are in `docs/HOW-TO.md`.

```
tools/
  site/                          the app (shared by every work)
    app.js                         all behaviour → app/app.js
    index_template.html            layout + styles → index.html, app/style.css
    library.py                     registers each work's sources and checks the whole library
    build.py                       runs library.py, then builds the website and dist/
    privacy.html                   the privacy policy → privacy.html
    regen_check.py                 library/ must be exactly what tools/works/export.py and make_timings.py make
    smoke_test.py, ux_test.py      every work in a browser; navigation and reading at phone size
    fixtures/                      data only the tests use (its README)
  audio/                         audio sources (shared by every work; see audio/README.md)
    transcribe.py                  recordings → transcripts (Whisper speech recognition)
    transcribe_onnx.py             the same with a Whisper model from GitHub, when the usual model can't be downloaded
    sync_transcripts.py            copies transcripts made in the cloud (private repo) into tools/works/…/transcripts/
    align.py                       matches transcript lines to verses
    make_timings.py                transcripts → library/<work>/audio/<id>.json
    order.py                       the order rule for times set by ear (the same rule as the app's)
    apply_owner_timing.py          a "Timing:" issue from the app → the source's owner.json (run by the timing workflow)
  meanings/                      our own meanings (style.md)
    prepare.py, apply_batches.py   batches of verses for writers and reviewers → a work's meanings/<lang>/scriptures.json
    overlap.py                     no sentence copied from a copyrighted meaning
    versenum.py                    the verse number at the end of each of our meanings
    sanskrit_dict.py               Monier-Williams and Apte look-ups
  store/                         the store apps (docs/APPS.md): icons, screenshots, listing check
  fonts/                         Noto Serif Devanagari and Gurmukhi, Tiro Devanagari Sanskrit (svaras), Literata, Gentium (transliteration subset)
  jsonio.py                      writes library files: shared ones one entry per line; a work's through the standard
  text/standard.py               the writing standard for verses (PLAYBOOK §3): ॥, Pāṇini's spelling for Sanskrit, ISO 15919
  works/                         one folder per work, named by its id; the format: works/README.md
    export.py                      every work folder → library/<path>/ (work.json, meanings/, glossary.json)
    textfile.py                    the format of text.txt; source scripts write it with textfile.write
    <work>/                        work.json, text.txt, README.md, reconciliation.md, meanings/<lang>/<source>.json,
                                   glossary/<lang>.json (the work's own senses), audio/<source>/, source/ (scripts that
                                   make the text from the owner's books and pages, and their checks)
```

## Rebuild everything
```bash
(cd tools/works/manas/source && python3 make_appdata.py && python3 make.py)    # the Mānas from its book data (no PDFs needed)
python3 tools/works/export.py                                                  # every work → library/
for s in tools/works/*/audio/*/; do grep -q '"take"' $s/source.json || python3 tools/audio/make_timings.py $s; done   # timings
for s in tools/works/*/audio/*/; do grep -q '"take"' $s/source.json && python3 tools/audio/make_timings.py $s; done   # then those taken from them
python3 tools/site/build.py                                                    # check + website + dist/
```
`python3 tools/site/regen_check.py` does the same into an empty folder and compares it with `library/`.
Needs Python 3 with `numpy` and Node.js (`build.py` checks that `app.js` parses). Transcription also needs `faster-whisper` and `ffmpeg`; reading the PDFs again needs `pymupdf` and `tesseract`; the tests, icons and screenshots need `playwright`.
