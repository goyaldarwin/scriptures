# How to

Each procedure ends with the same three steps: **build, test, publish**.
```bash
python3 tools/site/build.py        # registers sources, checks the library, builds the site
python3 -m http.server 8000        # open http://localhost:8000 at phone size (390×844) and look
git add -A && git commit -m "…" && git push   # GitHub Pages updates in about a minute
```
If `build.py` prints `LIBRARY PROBLEM: …`, fix what it names. It never builds a broken library.

---

## Add a new meaning source (another translation or commentary)

1. Choose the id: `<lang>-<publisher or translator>`, e.g. `hi-swami-ramsukhdas` or `en-griffith`.
2. Turn the book into `{item id: [meaning, footnotes?]}`. Put the scripts and their intermediate files in `tools/works/<work>/meanings/<id>/` so the work can be redone. Match by the item ids in `library/<path>/work.json`, and check the verse text where possible, not by position alone. Copy the source's meanings faithfully (the owner's rule: copy what the owner gives; write our own, as `<lang>-scriptures`, only for verses no given source covers).
3. Write `library/<path>/meanings/<id>.json` in the format in `docs/LIBRARY.md` §3, with `id`, `lang`, `title` (bilingual) and `m`.
4. Build. The source appears under ☰ › More › Sources. The default stays as it was unless the new file has a lower `order`.
5. Note the edition and the permission status in the root `README.md` under "Sources and permissions".

## Add a new audio source (another reciter)

1. Choose the id: the reciter's name, e.g. `anup-jalota`. Create `tools/works/<work>/audio/<id>/`.
2. In it, write `source.json`:
   ```json
   {"id": "anup-jalota", "work": "hinduism/granth/tulsidas/ramcharitmanas", "type": "youtube", "lang": "hi",
    "title": {"hi": "अनूप जलोटा", "en": "Anup Jalota"}}
   ```
3. Write `recordings.json`, one entry per YouTube video in reading order: `{"yt": "<11-char video id>", "file": "<original download name>", "data": "<path of its copy in scriptures-data>", "dur": <seconds>, "order": <n>}`. First add the recording to the private repo `scriptures-data` at `<work path>/audio/<source id>/` (speech-quality copy + `.meta.json`, see its README). From a YouTube link, the owner does this on his computer with `uv run tools/fetch_youtube.py <work path> <source id> <link> --commit` there (it cannot run in a session or on GitHub's machines); then fill in the meta's Hindi title, `language`, `work_id`, `reciter`, `used_for` and `pipeline`. The video id is in the YouTube link (`watch?v=…`) and in the downloaded file name `[…]`.
4. Transcribe. **Preferred: in the cloud** — run the `transcribe` workflow of `scriptures-data` (Actions tab, or `gh api repos/goyaldarwin/scriptures-data/actions/workflows/transcribe.yml/dispatches -X POST -f ref=main -f inputs[source]=<this source folder> -f inputs[ids]=<ids> -f inputs[ref]=<branch>`): one GitHub machine per recording, about 7× faster than real time; then `python3 tools/audio/sync_transcripts.py <clone of scriptures-data>`. **Or locally** (hours; resumable), with `DATA_DIR=<clone of scriptures-data>` instead of `AUDIO_DIR`. If the faster-whisper model can't be downloaded (Hugging Face blocked), `tools/audio/transcribe_onnx.py` does the same with a Whisper model from GitHub (see its header): `AUDIO_DIR=<folder with the files> WHISPER_MODEL=<model folder> python3 tools/audio/transcribe.py tools/works/<work>/audio/<id> 0 2`, and the same with `1 2` in parallel. See `tools/audio/README.md`. Commit `transcripts/` as you go, because they are the expensive part.
5. Make the timings: `python3 tools/audio/make_timings.py tools/works/<work>/audio/<id>`. It prints, for each recording, the first and last verse it found. Check that these match the recording's day. If the speech recogniser missed a line and a verse starts at the wrong place, add its real start to `fixes.json` beside `source.json` (`{video id: {item id: seconds}}`) with the evidence in `fixes.md`, and run this step again. Never edit the generated timings by hand.
6. Build and test: tap ▶ on a day, then check that the highlighted verse follows the voice at the start, middle and end.

## Time a recording by ear (owner and helpers)
Use this when automatic timing is weak (kīrtan, chant) or a recording has no transcript.
1. Make a starting point: in `source.json` set `"estimate": true` (starts spread by text length) and `"draft": "<why>"`, run `make_timings.py`, build and push. A draft is heard only in Audio timing mode.
2. The owner opens the work, turns on ☰ › More › Audio timing, plays, and marks verses ("⏱ Starts now", "⏹ Ends now"); the light waits on guessed starts. Helpers do the same and send the owner a file ("Save as a file"); the owner opens it ("Open file") and checks each mark.
3. The owner taps "Send to the library": a GitHub issue "Timing: <path> / <source>"; the `timing` workflow applies it (owner's issues only) and closes it. With the publish switch on, the recording goes live and is marked checked.
4. To verify a send (the owner often asks): `gh api repos/goyaldarwin/scriptures/issues/<n>` and `/comments` (REST — GraphQL is unavailable), compare the issue's JSON with `library/<path>/audio/<source>.json` (each sent time exact), read `moved`, and check `gh api repos/goyaldarwin/scriptures/commits/main/check-runs`.
5. Never edit `owner.json` or the generated timings by hand; the issue is the record.

## Correct or remove a verse in a generated text
- Put the change in the work's generator (`text.txt`, `text_fixes.json`, `settle.py`'s `FIX` / `ITEM_FIX`), never only in a generated file — a regeneration undoes it. Diff the regenerated file against the previous one and explain every change.
- Item ids are permanent. A removed verse's id is not reused; re-point any topic that started at it; regenerate meanings and audio timings; record it in the work's `reconciliation.md`.
- A changed word: update both meanings (hi, en) and the work's glossary entry for that word.

## Add a new work (Ram Raksha Stotram, an Upanishad, Japji Sahib …)

1. Place it on the shelf at its REST-like address, `<tradition>/<genre>/<group…>/<work>` (`docs/LIBRARY.md` §1), reusing existing levels: e.g. a Hanumān Chālīsā goes to `hinduism/chalisa/hanuman/hanuman-chalisa`, the Kena Upaniṣad to `hinduism/veda/samaveda/upanishad/kena`, Japji Sahib to `sikhism/gurbani/guru-nanak-dev/japji-sahib`. Add the missing shelves to `library/index.json`, ending in `{"id", "work", "path", "title", "by", "edition", "desc"}`. The work id is the shelf id unless that is taken, and the tools go in `tools/works/<work id>/`.
2. Create `tools/works/<work>/` with the extraction scripts (from PDFs or other sources) and an `export.py` that writes `library/<path>/work.json` (`docs/LIBRARY.md` §2) with each verse's language, its meaning sources (§3), and new words into `glossary/<lang>.json` (§5). A new language needs its own entry first (below). Use `tools/works/ramcharitmanas/` as the model.
3. Choose the natural divisions for `parts`, the `topics`, and any `plans` (e.g. daily pāṭha). Ask the owner which plans they want. Pages follow the item's section `s`; use a name (e.g. `aarti`), not a number, unless sections are dohā numbers. Verse types the app doesn't know (viniyoga, dhyāna, pada, abhaṅga …) go in the work's `types` (`docs/LIBRARY.md` §2). Small models: `tools/works/ramraksha/` (a stotra from a video's on-screen text) and `tools/works/shirdi-sai-dhoop-aarti/` (a multilingual āratī from two printouts).
4. Add audio as above if there is a recording.
5. Build and test the shelf screen, the work's home, the reader, search, and bookmarks.

## Add a new language (for a work in Marathi, Gurmukhi, Braj …)
1. Add it to `library/glossary/languages.json`: ISO 639 code, bilingual name, script, fallback chain (e.g. Braj → Sanskrit), suffix rules and stems. Leave `suffixes` empty until you know the language's inflections; a wrong rule gives wrong roots.
2. Create `library/glossary/<code>.json` with the words of the work's verses (`docs/LIBRARY.md` §5). Write meanings for that language; do not copy Hindi or Awadhi senses because a spelling matches.
3. Set the work's `lang`, and give `l` to any verses in another language. For example, a Gurmukhi Japji Sahib uses `pa`, its Sanskrit-derived words can fall back to `sa`, and a Marathi āratī uses `mr`.
4. If the script is not Devanagari, check that the fonts cover it (`tools/fonts`, `tools/site/build.py`), and that `align.py` has a `key()` for it before aligning audio.
5. Build: the check refuses unknown languages, dictionaries without an entry in `languages.json`, and fallbacks to languages that don't exist.

## Fix a word or meaning in the Rāmacaritamānasa
- Verse text: add the fix to `tools/works/ramcharitmanas/book/text_fixes.json`, then run `(cd tools/works/ramcharitmanas/book && python3 make_appdata.py) && python3 tools/works/ramcharitmanas/export.py`.
- A Gita Press meaning: the same files and steps (see `tools/works/ramcharitmanas/book/README.md`).
- A word meaning: edit `library/glossary/<lang>.json` directly, in the language of the verse (`sa` for the ślokas and Sanskrit stutis, otherwise `awa`).

## Change the app
Edit `tools/site/app.js` (behaviour) or `tools/site/index_template.html` (layout and styles), then build and test. Check the playbook's list of past bugs.

## Try a change on claude.ai before publishing
Publish `dist/Scriptures-artifact.html` as an artifact. YouTube is blocked inside claude.ai artifacts, so test audio on the website.
