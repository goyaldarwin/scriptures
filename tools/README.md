# Tools

Everything used to make `library/` and the website. Run all commands from the repository root. Procedures are in `docs/HOW-TO.md`.

```
tools/
  site/                          the app (shared by every work)
    app.js                         all behaviour → app/app.js
    index_template.html            layout + styles → index.html, app/style.css
    library.py                     registers each work's sources and checks the whole library
    build.py                       runs library.py and catalogue.py, then builds the website and dist/
    catalogue.py                   docs/WORKS.md: every work's structure, numbering, sources and recordings, made from the library
    privacy.html                   the privacy policy → privacy.html
    check.py                       every check before a commit, side by side (build, then regen, history, smoke, UX in shards)
    regen_check.py                 the text generators make the committed texts; library/ is exactly what export.py and make_timings.py make
                                   (only the works changed since its last pass here; --full: every work, as the CI)
    history_check.py               no work or verse id that readers' data points at has disappeared
    smoke_test.py, ux_test.py      every work in a browser; navigation and reading at phone size
    fixtures/                      data only the tests use (its README)
  audio/                         audio sources (shared by every work; see audio/README.md)
    transcribe.py                  recordings → transcripts (Whisper speech recognition)
    transcribe_onnx.py             the same with a Whisper model from GitHub, when the usual model can't be downloaded
    sync_transcripts.py            copies transcripts made in the cloud (private repo) into tools/works/…/transcripts/
    align.py                       matches transcript lines to verses
    make_timings.py                transcripts → library/<path>/audio/<id>.json
    order.py                       the order rule for times set by ear (the same rule as the app's)
    apply_owner_timing.py          a "Timing:" issue from the app → the source's owner.json (run by the timing workflow)
  meanings/                      our own meanings (style.md)
    prepare.py, apply_batches.py   batches of verses for writers and reviewers → a work's meanings/<lang>/scriptures.json
    gurbani_prepare.py             batches of Sri Guru Granth Sahib with the published translations line by line (scratch, private)
    overlap.py                     no sentence copied from a copyrighted meaning
    platts.py                      look a Hindi, Awadhi or Braj word up in Platts (read from the private copy in scriptures-data)
    teeka.py                       search Prof. Sahib Singh's Darpan and the Faridkot Teeka for a Gurbani word (private copies, converted to Unicode)
    hard_words.py                  the hard words of our meanings: candidates for a writer, apply written entries, report what the app underlines
    versenum.py                    the verse number at the end of each of our meanings
    sanskrit_dict.py               Monier-Williams and Apte look-ups
  store/                         the store apps (docs/APPS.md): icons, screenshots, listing check
  fonts/                         Noto Serif Devanagari and Gurmukhi, Tiro Devanagari Sanskrit (svaras), Literata, Gentium Book Plus (the transliteration's letters only, `subset_gentium.py`; OFL, `gentium-LICENSE.txt`)
  jsonio.py                      writes library files: shared ones one entry per line; a work's through the standard
  text/standard.py               the writing standard for verses (PLAYBOOK §3): ॥, Pāṇini's spelling for Sanskrit, ISO 15919
  text/cite.py                   a verse's number as cited (work.json → cite): the one source of every number the app shows or finds
  text/names.json                a name's one spelling and its variants, on the shelves where it holds (checked by site/library.py)
  sweep/inventory.py             the sweep's inventory (docs/SWEEP.md, step 0.4): every work, its sources here and in scriptures-data
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
`python3 tools/site/regen_check.py` does the same into an empty folder and compares it with `library/` (`--full` for every work; without it, only the works whose inputs or outputs changed since its last pass on this machine).
Needs Python 3 with `numpy` and Node.js (`build.py` checks that `app.js` parses). Transcription also needs `faster-whisper` and `ffmpeg`; reading the PDFs again needs `pymupdf` and `tesseract`; the tests, icons and screenshots need `playwright`.
