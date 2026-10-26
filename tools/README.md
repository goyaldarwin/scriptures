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
    regen_check.py                 library/ must be exactly what the works' exporters make
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
    prepare.py, apply_batches.py   batches of verses for writers and reviewers → a work's meaning files
    overlap.py                     no sentence copied from a copyrighted meaning
    versenum.py                    the verse number at the end of each of our meanings
    sanskrit_dict.py               Monier-Williams and Apte look-ups
  store/                         the store apps (docs/APPS.md): icons, screenshots, listing check
  fonts/                         Noto Serif Devanagari and Gurmukhi, Tiro Devanagari Sanskrit (svaras), Literata, Gentium (transliteration subset)
  jsonio.py                      writes library files: shared ones one entry per line; a work's through the standard
  text/standard.py               the writing standard for verses (PLAYBOOK §3): ॥, Pāṇini's spelling for Sanskrit, ISO 15919
  works/                         one folder per work: how its data is made (each has a README.md)
    ramcharitmanas/
      book/                        Gita Press PDFs → book/app_data.json (see its README)
      meanings/                    our own meanings (hi.json, en.json) and topic headings (topics.json)
      visarjan.json                the Kathā-visarjana page
      export.py                    → library/hinduism/granth/tulsidas/ramcharitmanas/ (text, Gita Press and our meanings)
      audio/kamlesh-upadhyay/      source.json, recordings.json, owner.json, transcripts/
    sundarkand/                  the Sundarakāṇḍa as a work of its own
      export.py                    parts 1–2 (the close of the Kiṣkindhā-kāṇḍa, the Sundara-kāṇḍa) GENERATED from the Mānas's
                                   work.json and meanings (same ids, sections, text, topics); parts 0, 3, 4 (opening prayers,
                                   Hanumān Chālīsā, āratī) from text.txt → library/hinduism/granth/tulsidas/sundarkand/
      check.py                     checks that the Mānas part is identical to the Mānas's Sundara-kāṇḍa
      text.txt, reconciliation.md  the added texts, and how they were settled from the web sources
      meanings/hi.json, en.json    our own meanings for the added texts
      glossary/awa|hi|sa.json      their word meanings, merged into library/glossary/
      audio/ashwin-pathak/         source.json, recordings.json, fixes.json + fixes.md, transcripts/
    ramraksha/
      source/                      the video's text (video_text.tsv), the Hindi web page and its cleaned meanings
      meanings/hi.json, en.json    our own meanings
      export.py                    source/ → library/hinduism/stotra/rama/ramraksha/ (text, meanings, new Sanskrit words)
      glossary_sa.json             the stotra's word meanings, merged into library/glossary/sa.json
      audio/vande-guru-paramparaam/ source.json, recordings.json, fixes.json + fixes.md, transcripts/
    aartis/                      the Hindu āratīs, one work each, one exporter (see its README)
      <work>/                      text.txt, meanings/, reconciliation.md, senses.json, audio/
      glossary/awa|bra|hi.json     their word meanings, merged into library/glossary/
      export.py                    → library/hinduism/aarti/<deity>/<work>/ (after the Mānas and Sundarakāṇḍa exports)
    shirdi-sai-dhoop-aarti/
      text.txt                     the verse text (settled in reconciliation.md)
      meanings/                    hi.json, en.json (ours), en-shirdisaibabakripa.json (the printout's English)
      glossary/mr|sa|hi.json       word meanings by language
      export.py                    → library/hinduism/aarti/shirdi-sai/dhoop-aarti/ and library/glossary/
      audio/pramod-medhi-times/    the live recording, timed by ear (owner.json)
    shri-rudram/
      source/                      the shlokam.org printouts → *_raw.json (extract.py) → ../text.json (settle.py; reconciliation.md)
      meanings/namakam|chamakam.json  our English and Hindi meaning per mantra
      glossary/                    word meanings (→ library/glossary/sa.json) and this work's own senses
      export.py                    → library/hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/
      audio/shlokam/               source.json, recordings.json, fixes.json + fixes.md, transcripts/ (a draft)
    katha-upanishad/
      source/                      the book's IAST → pdf_raw.json (extract.py) → ../text.json (settle.py); witness/
      check.py                     checks the text against its transliteration and the witnesses
      meanings/, glossary/         our meanings; word meanings by vallī
      export.py                    → library/hinduism/veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad/
      audio/smvedroad/             source.json, recordings.json, fixes.json + fixes.md, transcripts/
    isha-upanishad/
      text.json                    the text (from the shlokam.org printout; settled in reconciliation.md), check.py verifies it
      meanings/hi.json, en.json    our meanings
      glossary_sa.json             word meanings, merged into library/glossary/sa.json
      export.py                    → library/hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/
      audio/smvedroad/             source.json, recordings.json, fixes.json + fixes.md, transcripts/
    mandukya-upanishad/
      text.txt                     the text (settled in reconciliation.md)
      meanings/hi.json, en.json    our meanings
      glossary_sa.json             word meanings, merged into library/glossary/sa.json
      export.py                    → library/hinduism/veda/atharvaveda/upanishad/mandukya-upanishad/
      audio/smvedroad/             source.json, recordings.json, fixes.json + fixes.md, transcripts/
    sukhmani-sahib/
      extract.py                   the owner's PDF → source/lines.json (legacy Gurmukhi, transliteration, English per printed line)
      gurmukhi.py                  legacy ASCII Gurmukhi font encoding (GurbaniAkhar) → Unicode Gurmukhi
      check.py                     checks every converted line (transliteration skeletons; optional external witnesses)
      structure.py                 printed lines → items (24 Ashtapadis: salok, pauris, rahao)
      meanings/hi|en|pa.json       our meanings, line by line
      glossary/pa.json             Gurmukhi word meanings
      export.py                    → library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/ and library/glossary/pa.json
      audio/parminder-singh/       source.json, recordings.json, owner.json, transcripts/ (a draft)
```

## Rebuild everything (Rāmacaritamānasa)
```bash
(cd tools/works/ramcharitmanas/book && python3 make_appdata.py)                 # book data (no PDFs needed)
python3 tools/works/ramcharitmanas/export.py                                     # → library/…/work.json, meanings/
python3 tools/audio/make_timings.py tools/works/ramcharitmanas/audio/kamlesh-upadhyay   # → library/…/audio/
python3 tools/works/sundarkand/export.py                                         # the standalone Sundarakāṇḍa takes the Mānas's corrections
python3 tools/works/aartis/export.py                                             # the Hanumān āratī and the Mānas verses in the Rāma stuti
python3 tools/site/build.py                                                      # check + website + dist/
```
Needs Python 3 with `numpy` and Node.js (`build.py` checks that `app.js` parses). Transcription also needs `faster-whisper` and `ffmpeg`; reading the PDFs again needs `pymupdf` and `tesseract`; the tests, icons and screenshots need `playwright`.
