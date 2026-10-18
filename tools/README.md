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
    transcribe_onnx.py             the same with a Whisper model from GitHub, when the usual model can't be downloaded
    align.py                       matches transcript lines to verses
    make_timings.py                transcripts → library/<work>/audio/<id>.json
    sync_transcripts.py            copies transcripts made in the cloud (private repo) into tools/works/…/transcripts/
  fonts/                         Noto Serif Devanagari, Literata, Gentium (transliteration subset)
  works/                         one folder per work: how its data was made
    ramcharitmanas/
      book/                        Gita Press PDFs → book/app_data.json (see its README)
      export.py                    app_data.json → library/hinduism/granth/tulsidas/ramcharitmanas/ (text + Gita Press meanings)
      audio/kamlesh-upadhyay/      source.json, recordings.json, transcripts/
    ramraksha/
      source/                      the video's text (video_text.tsv), the Hindi web page and its cleaned meanings
      export.py                    source/ → library/hinduism/stotra/rama/ramraksha/ (text, English + Hindi meanings, new Sanskrit words)
      glossary_sa.json             the stotra's word meanings, merged into library/glossary/sa.json
      audio/vande-guru-paramparaam/ source.json, recordings.json, fixes.json + fixes.md, transcripts/
    shirdi-sai-dhoop-aarti/
      text.txt                     the verse text (settled in reconciliation.md)
      meanings/hi.json, en.json    one meaning per verse
      glossary/mr|sa|hi.json       word meanings by language
      export.py                    → library/hinduism/aarti/shirdi-sai/dhoop-aarti/ and library/glossary/
    shri-rudram/
      source/                      the shlokam.org printouts (PDF) → *_raw.json (extract.py) → ../text.json (settle.py; reconciliation.md)
      meanings/namakam|chamakam.json  our English and Hindi meaning per mantra
      glossary/g*.json, work_sa.json  word meanings (→ library/glossary/sa.json) and this work's own senses
      export.py                    → library/hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/
      audio/shlokam/               source.json, recordings.json (transcripts come from the cloud)
    sundarkand/                  the Sundarakāṇḍa as a work of its own (see its README)
      export.py                    part 1 GENERATED from the Mānas's work.json + Gita Press meanings (same ids, sections,
                                   text, topics); parts 2–3 (Hanumān Chālīsā, āratī) from text.txt → library/hinduism/granth/tulsidas/sundarkand/
      check.py                     checks that part 1 is identical to the Mānas's Sundara-kāṇḍa
      text.txt, reconciliation.md  the Chālīsā and āratī text, and how it was settled from the web sources
      translit.py                  their transliteration, in the Mānas's style
      meanings/hi.json, en.json    our own meanings for the Chālīsā and āratī (→ hi-scriptures, en-scriptures)
      glossary/awa|hi.json         their word meanings, merged into library/glossary/
      audio/ashwin-pathak/         source.json, recordings.json, transcripts (cloud) → timings
    isha-upanishad/
      text.json                    the text (from the shlokam.org printout; settled in reconciliation.md), check.py verifies it
      meanings/hi.json, en.json    one meaning per mantra, written for this library
      glossary_sa.json             word meanings, merged into library/glossary/sa.json
      export.py                    → library/hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/
      audio/smvedroad/             source.json, recordings.json, fixes.json/md (timed)
      audio/smvedroad/             source.json, recordings.json (not timed yet)
    sukhmani-sahib/
      extract.py                   the owner's PDF → source/lines.json (legacy Gurmukhi, transliteration, English per printed line)
      gurmukhi.py                  legacy ASCII Gurmukhi font encoding (GurbaniAkhar) → Unicode Gurmukhi
      check.py                     checks every converted line (transliteration skeletons; optional external witnesses)
      structure.py                 printed lines → items (24 Ashtapadis: salok, pauris, rahao)
      meanings/hi.json, glossary/pa.json   Hindi meaning per item and Gurmukhi word meanings, written for this library
      export.py                    → library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/ and library/glossary/pa.json
```

## Rebuild everything (Rāmacaritamānasa)
```bash
(cd tools/works/ramcharitmanas/book && python3 make_appdata.py)                 # book data (no PDFs needed)
python3 tools/works/ramcharitmanas/export.py                                     # → library/…/work.json, meanings/
python3 tools/audio/make_timings.py tools/works/ramcharitmanas/audio/kamlesh-upadhyay   # → library/…/audio/
python3 tools/works/sundarkand/export.py                                         # the standalone Sundarakāṇḍa takes the Mānas's corrections
python3 tools/site/build.py                                                      # check + website + dist/
```
Needs Python 3 with `numpy`. Transcription also needs `faster-whisper` and `ffmpeg`; reading the PDFs again needs `pymupdf` and `tesseract`; tests need `playwright`.
