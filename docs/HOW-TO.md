# How to

Each procedure ends with the same three steps: **build, test, publish**.
```bash
python3 tools/site/build.py        # registers sources, checks the library, builds the site
python3 tools/site/regen_check.py  # library/ is exactly what the exporters make
python3 tools/site/smoke_test.py   # every work opens in a browser without script errors
python3 tools/site/ux_test.py      # navigation and reading, every work, at phone size
python3 -m http.server 8000        # open http://localhost:8000 at phone size (390×844) and look
git pull && git add -A && git commit -m "…" && git push   # GitHub Pages updates in about a minute
```
If `build.py` prints `LIBRARY PROBLEM: …`, fix what it names. It never builds a broken library. Large work (a new work, a change to shared code) goes on a branch and a pull request (`docs/START-HERE.md`). Always `git pull` first: the `timing` workflow also pushes to `main`.

---

## Add a new meaning source (another translation or commentary)

1. Choose the id: `<lang>-<publisher or translator>`, e.g. `hi-swami-ramsukhdas` or `en-griffith`.
2. Turn the book into `{item id: [meaning, footnotes?]}`. Put the scripts and their intermediate files in `tools/works/<work>/meanings/<id>/` so the work can be redone. Match by the item ids in `library/<path>/work.json`, and check the verse text where possible, not by position alone. Copy the source's meanings faithfully (`docs/LIBRARY.md` §3).
3. Write `library/<path>/meanings/<id>.json` in the format in `docs/LIBRARY.md` §3, with `id`, `lang`, `title` (bilingual), `m`, and optionally `order` and the line-by-line `p`.
4. Build. The source appears under ☰ › More › Sources. The default stays as it was unless the new file has a lower `order`.
5. Note the edition and the permission status in the root `README.md` under "Sources and permissions".

Our own meanings (`<lang>-scriptures`) follow `tools/meanings/style.md`; `tools/meanings/prepare.py` makes the batches to write, `apply_batches.py` merges them, and `overlap.py` checks them.

## Add a new audio source (another reciter)

1. Choose the id: the reciter's name, e.g. `anup-jalota`. Create `tools/works/<work>/audio/<id>/`.
2. In it, write `source.json`:
   ```json
   {"id": "anup-jalota", "work": "hinduism/granth/tulsidas/ramcharitmanas", "type": "youtube", "lang": "hi",
    "title": {"hi": "अनूप जलोटा", "en": "Anup Jalota"}}
   ```
   Optional fields (`order`, `draft`, `estimate`, `window`, `align`, `fill`, `anchor_min`) are described at the top of `tools/audio/make_timings.py` and `tools/audio/transcribe.py`.
3. Write `recordings.json`, one entry per YouTube video in reading order: `{"yt": "<11-char video id>", "file": "<original download name>", "data": "<path of its copy in scriptures-data>", "dur": <seconds>, "order": <n>}`. First add the recording to the private repo `scriptures-data` at `<work path>/audio/<source id>/` (speech-quality copy + `.meta.json`, see its README). The video id is in the YouTube link (`watch?v=…`) and in the downloaded file name `[…]`.
4. Transcribe (`tools/audio/README.md`).
   - **In the cloud (preferred):** run the `transcribe` workflow of `scriptures-data` (Actions tab, or `gh api repos/goyaldarwin/scriptures-data/actions/workflows/transcribe.yml/dispatches -X POST -f ref=main -f inputs[source]=<this source folder> -f inputs[ids]=<ids> -f inputs[ref]=<branch>`). It uses one GitHub machine per recording. Then run `python3 tools/audio/sync_transcripts.py <clone of scriptures-data>`.
   - **Locally** (hours; resumable): `DATA_DIR=<clone of scriptures-data> WHISPER_MODEL=<model folder> python3 tools/audio/transcribe.py tools/works/<work>/audio/<id> 0 2`, and the same with `1 2` in parallel.
   - **If the faster-whisper model can't be downloaded** (Hugging Face blocked): `python3 tools/audio/transcribe_onnx.py <audio file> <model folder> tools/works/<work>/audio/<id>/transcripts/<video id>.jsonl` with a Whisper model from GitHub (see the script's header), then mark it finished with an empty `<video id>.jsonl.done`.
   - Commit `transcripts/` as you go, because they are the expensive part.
5. Make the timings: `python3 tools/audio/make_timings.py tools/works/<work>/audio/<id>`. It prints, for each recording, the first and last verse it found. Check that these match the recording. If the speech recogniser missed a line and a verse starts at the wrong place, add its real start to `fixes.json` beside `source.json` (`{video id: {item id: seconds}}`) with the evidence in `fixes.md`, and run this step again. Never edit the generated timings by hand.
6. Build and test: tap ▶ on a reading, then check that the highlighted verse follows the voice at the start, middle and end.

## Time a recording by ear (owner and helpers)
Use this when automatic timing is weak (kīrtan, chant) or a recording has no transcript.
1. Make a starting point: in `source.json` set `"estimate": true` (starts spread by text length) and `"draft": "<why>"`, run `make_timings.py`, build and push. A draft plays only while Audio timing is on.
2. The owner opens the work, turns on ☰ › More › Audio timing, plays, and marks verses ("⏱ Starts now", "⏹ Ends now"); the light waits on guessed starts. Helpers do the same and send the owner a file ("Save timings as a file"); the owner opens it ("Open a file") and checks each mark.
3. The owner taps "Send to the library (GitHub)": this opens a GitHub issue "Timing: <path> / <source>". The `timing` workflow applies it (issues from the owner's accounts only: `goyaldarwin`, `darwingoyal`) and closes it. For a draft, the switch "This recording is checked: publish it for everyone" goes with the send: the recording goes live and is marked checked.
4. To verify a send: `gh api repos/goyaldarwin/scriptures/issues/<n>` and `/comments` (REST; GraphQL is unavailable), compare the issue's JSON with `library/<path>/audio/<source>.json` (each sent time exact), read `moved`, and check `gh api repos/goyaldarwin/scriptures/commits/main/check-runs`.
5. Never edit `owner.json` or the generated timings by hand; the issue is the record.

## Correct or remove a verse in a generated text
- Put the change in the work's generator (`text.txt`, `text_fixes.json`, `settle.py`'s `FIX` / `ITEM_FIX`), never only in a generated file: a regeneration undoes it. Diff the regenerated file against the previous one and explain every change.
- Item ids are permanent. A removed verse's id is not reused; re-point any topic that started at it; regenerate meanings and audio timings; record it in the work's `reconciliation.md`.
- A changed word: update every meaning of the verse and the work's glossary entry for that word.

## Add a new work (an Upanishad, Japji Sahib …)

1. Place it on the shelf at its address, `<tradition>/<genre>/<group…>/<work>` (`docs/LIBRARY.md` §1), reusing existing levels: e.g. a Hanumān Chālīsā goes to `hinduism/chalisa/hanuman/hanuman-chalisa`, the Kena Upaniṣad to `hinduism/veda/samaveda/upanishad/kena`, Japji Sahib to `sikhism/gurbani/guru-nanak-dev/japji-sahib`. Add the missing shelves to `library/index.json`, ending in `{"id", "work", "path", "title", "by", "edition", "desc"}` (and `salute` if the work has its own). The work id is the shelf id unless that is taken, and the tools go in `tools/works/<work id>/`.
2. Create `tools/works/<work>/` with the extraction scripts (from PDFs or other sources), a `reconciliation.md` (the source and every choice), a `README.md`, and an `export.py` that writes `library/<path>/work.json` through `jsonio.dump_library` (it applies the writing standard, PLAYBOOK §3, and makes the transliteration) (`docs/LIBRARY.md` §2) with each verse's language, its meaning sources (§3), and new words into `glossary/<lang>.json` (§5). A new language needs its own entry first (below).
3. Choose the natural divisions for `parts`, the `topics`, and any `plans` (e.g. daily pāṭha). Ask the owner which plans they want. Pages follow the item's section `s`; use a name (e.g. `aarti`), not a number, unless sections are dohā numbers. Verse types the app doesn't know (viniyoga, dhyāna, pada, abhaṅga …) go in the work's `types` (`docs/LIBRARY.md` §2).
4. Models: `tools/works/katha-upanishad/` (a Sanskrit text from a book, checked against witnesses), `tools/works/aartis/` (short texts from printouts, one exporter for several works), `tools/works/shirdi-sai-dhoop-aarti/` (a multilingual āratī from two printouts), `tools/works/sukhmani-sahib/` (Gurmukhi, line-by-line meanings).
5. Add audio as above if there is a recording.
6. Build and test the shelf screen, the work's home, the reader, search, and bookmarks.

## Add a new language (for a work in Marathi, Gurmukhi, Braj …)
1. Add it to `library/glossary/languages.json`: ISO 639 code, bilingual name, script, fallback chain (e.g. Braj → Sanskrit), suffix rules and stems. Leave `suffixes` empty until you know the language's inflections; a wrong rule gives wrong roots. Add a `meaning` block only if meanings will be written in it (`docs/LIBRARY.md` §5).
2. Create `library/glossary/<code>.json` with the words of the work's verses (`docs/LIBRARY.md` §5). Write meanings for that language; do not copy Hindi or Awadhi senses because a spelling matches.
3. Set the work's `lang`, and give `l` to any verses in another language. For example, a Gurmukhi Japji Sahib uses `pa`, and a Marathi āratī uses `mr`.
4. If the script is not Devanagari or Gurmukhi, add a font (`tools/fonts`, registered in `tools/site/build.py`) and teach `key()` in `tools/audio/align.py` to read it before aligning audio.
5. Build: the check refuses unknown languages, dictionaries without an entry in `languages.json`, and fallbacks to languages that don't exist.

## Fix a word or meaning in the Rāmacaritamānasa
- Verse text: add the fix to `tools/works/ramcharitmanas/book/text_fixes.json`, then run `(cd tools/works/ramcharitmanas/book && python3 make_appdata.py) && python3 tools/works/ramcharitmanas/export.py && python3 tools/works/sundarkand/export.py && python3 tools/works/aartis/export.py`.
- A Gita Press meaning: the same files and steps (see `tools/works/ramcharitmanas/book/README.md`).
- Our own meaning: `tools/works/ramcharitmanas/meanings/hi.json` or `en.json`, then the same export.
- A word meaning: edit `library/glossary/<lang>.json` directly, in the language of the verse (`sa` for the ślokas and Sanskrit stutis, otherwise `awa`).

## Change the app
Edit `tools/site/app.js` (behaviour) or `tools/site/index_template.html` (layout and styles), then build and test. Read `docs/PLAYBOOK.md` §7 (the app) first.

## Try a change on claude.ai before publishing
Publish `dist/Scriptures-artifact.html` as an artifact. YouTube is blocked inside claude.ai artifacts, so test audio on the website.
