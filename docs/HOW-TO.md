# How to

Each procedure ends with the same three steps: **build, test, publish**.
```bash
python3 tools/site/check.py        # every check below, side by side (about 5 minutes); --fast: the first three only (about 20 s)
  # tools/site/build.py          registers sources, checks the library, builds the site
  # tools/site/regen_check.py    the text generators make the committed texts; library/ is exactly what the exporters and make_timings.py make
  # tools/site/history_check.py  no work or verse id that readers' data points at has disappeared
  # tools/site/smoke_test.py     every work opens in a browser without script errors
  # tools/site/ux_test.py        navigation and reading, every work, at phone size (in shards: --shard K/N)
python3 -m http.server 8000        # open http://localhost:8000 at phone size (390×844) and look
git pull && git add -A && git commit -m "…" && git push   # GitHub Pages updates in about a minute
```
A work's files are in `tools/works/<work>/` (the format: `tools/works/README.md`); `python3 tools/works/export.py <work>` writes it into `library/`. After a change to a work's text, make its recordings' timings again too (`python3 tools/audio/make_timings.py tools/works/<work>/audio/<source>`, then the same for any work whose recording takes from it, `source.json` → `take`): the starts not set by ear are spread by verse length, and `regen_check.py` fails on a stale timing file.

If `build.py` prints `LIBRARY PROBLEM: …`, fix what it names. It never builds a broken library. Large work (a new work, a change to shared code) goes on a branch and a pull request (`docs/PLAYBOOK.md` §10). Always `git pull` first: the `timing` workflow also pushes to `main`.

---

## Add a new meaning source (another translation)

1. Choose the source's name: the publisher or translator, e.g. `swami-ramsukhdas` or `griffith`; its library id is `<lang>-<name>`.
2. Write `tools/works/<work>/meanings/<lang>/<name>.json` (`tools/works/README.md` → meanings): `title` (bilingual), `order`, `"copied": true`, `m` {verse id: meaning, or a list of one piece per line}, and `notes` for footnotes. Match by the verse ids in `text.txt`, and check the verse text where possible, not by position alone. Copy the source's meanings faithfully (`docs/LIBRARY.md` §3). When a script makes the file from a book, keep the script and its intermediate files in `tools/works/<work>/source/` so it can be redone.
3. Export the work and build. The source appears under ☰ › More settings › Sources. The default stays as it was unless the new file has a lower `order`.
4. Note the edition and the permission status in the root `README.md` under "Sources and permissions".

## Add a commentary

A commentary explains the verse (a guru's or ācārya's ṭīkā, a bhāṣya); a translation, however free, is a meaning source (above).
1. Keep the owner's copy in `scriptures-data` at the work's path, under `books/<publisher>/` or `printouts/<site>/`, with its `.meta.json`.
2. Name it after its author or publisher (`shridhara`, `ramsukhdas`); its library id is `<lang>-<name>`, in the language it is written in (`sa` for a Sanskrit ṭīkā).
3. Write `tools/works/<work>/commentary/<lang>/<name>.json` in the meaning format (`tools/works/README.md` → commentary): `title` (bilingual), `order`, `"copied": true`, `m` {verse id: the commentary on it}, `notes` for its footnotes. A commentary on several verses sits under the last of them. Make it with a script in `tools/works/<work>/source/` when it comes from a book, and record every choice in `reconciliation.md`.
4. Export the work and build. ☰ › More settings › Sources then shows "Commentary" for this work (Off by default).
5. Record the edition and permission status in the work's `README.md` under "Sources and permissions".

Our own meanings (`meanings/<lang>/scriptures.json`) follow `tools/meanings/style.md`; `tools/meanings/prepare.py --work <work>` makes the batches to write, `apply_batches.py --work <work>` merges them, and the export checks them against the copied sources (`overlap.py`).

## Write our own meanings for a kāṇḍa of the Mānas

The rules are `tools/meanings/style.md` (above all §1) and `docs/PLAYBOOK.md` §4; each step has its brief in `tools/meanings/briefs/`, and every step reads its brief, `style.md` and the owner-approved Sundarakāṇḍa samples (the `sundar.` entries of `tools/works/manas/meanings/hi/scriptures.json` and `en/scriptures.json`) first.

0. **Dictionaries:** `python3 tools/meanings/sanskrit_dict.py fetch`, then `check`. They live outside the repository, so a new machine or cloud session never has them; nothing below runs without them (`prepare.py` and `apply_batches.py` refuse).
1. **Batches:** `python3 tools/meanings/prepare.py <scratch folder> <first id> <last id> --work manas --size 50`, the scratch folder outside the repository (e.g. `/home/claude/work/bal/`), the ids the kāṇḍa's first and last (`library/hinduism/granth/tulsidas/ramcharitmanas/work.json`; the Bāla-kāṇḍa is `bal.0.shloka1` to `bal.361.so361`, 1,957 verses). It writes `batch-NN.md` (verses, transliteration, word meanings, context) and `batch-NN.ids`, and marks a verse that already has our meaning ALREADY WRITTEN (an owner-approved one, such as the Sundarakāṇḍa's opening prayer `bal.17.so17`, stays as it is).
2. **For every batch, in this order, each step by its own agent** (the session launches them with its agent tool, many batches in parallel; each is told its brief, the scratch folder and its batch number, writes only into the scratch folder, names any helper file with the kāṇḍa and batch, and never edits the repository; a step whose agent stopped without its output file is run again):
   1. writer — `manas-writer.md`: the whole draft from the verse, its word meanings, the dictionaries and its context in the work overall and in the nearby verses, before opening any published meaning;
   2. reviewer — `manas-reviewer.md` → `batch-NN.review.jsonl`;
   3. copy audit — `manas-copy-auditor.md` → `batch-NN.audit.jsonl` (rewords wording only, never sense);
   4. accuracy and dictionary check — `manas-accuracy-checker.md` → `batch-NN.dict.jsonl` (every reworded piece read against the verse again).

   Each later step's fix wins over an earlier one for the same piece (writer < review < audit < accuracy check).
3. **Apply:** `python3 tools/meanings/apply_batches.py <scratch folder> --work manas --doubts docs/reviews/manas-<kāṇḍa>-doubts.jsonl` on a branch `manas-meanings-<kāṇḍa>` (one doubts file per kāṇḍa). It applies the writer's files and then the three steps' fixes, refuses a batch that missed a step (`--steps` names the steps required, all three by default), appends the doubts, and gathers every word issue into `<scratch folder>/words-to-settle.jsonl`. Check that no entry outside the kāṇḍa changed.
4. **Consistency pass** over the kāṇḍa — `manas-consistency.md`.
5. **Dictionary:** each issue of `words-to-settle.jsonl` that is clearly right for the word goes into `library/glossary/<lang>.json` as an added sense (old senses stay: other verses use them); the rest into `docs/reviews/dictionary-doubts.jsonl`.
6. **Copy check of the whole file:** `python3 tools/meanings/overlap.py tools/works/manas/meanings/hi/scriptures.json library/hinduism/granth/tulsidas/ramcharitmanas/meanings/hi-gitapress.json` and `python3 tools/meanings/overlap.py tools/works/manas/meanings/en/scriptures.json library/hinduism/granth/tulsidas/ramcharitmanas/meanings/en-gitapress.json`, 0 runs of 10+ for both.
7. `python3 tools/works/export.py`, then every check of `CLAUDE.md`; diff the regenerated data; one pull request per kāṇḍa. Before it merges, the session settles every doubt the writer or reviewer recorded (`docs/PLAYBOOK.md` §2): it applies the decision and removes the doubt from its file (`docs/reviews/README.md`).

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
   - **In the cloud (preferred):** run the `transcribe` workflow of this repository (Actions tab, or `gh api repos/goyaldarwin/scriptures/actions/workflows/transcribe.yml/dispatches -X POST -f ref=main -f inputs[source]=<this source folder> -f inputs[ids]=<ids> -f inputs[ref]=<branch>`; at most 256 ids a run). It uses one GitHub machine per recording, free because this repository is public: each job fetches only its own recording from `scriptures-data` with the read-only token in the secret `DATA_TOKEN` (a fine-grained token of the owner's, Contents: read on `scriptures-data` only; when it expires the jobs fail at that step, and the owner makes a new one), and commits only the transcript to the branch `ref`. `git pull` the branch afterwards.
   - **In the private repo:** the `transcribe` workflow of `scriptures-data` does the same on the owner's included minutes (`docs/PLAYBOOK.md` §10); then run `python3 tools/audio/sync_transcripts.py <clone of scriptures-data>`.
   - **Locally** (hours; resumable): `DATA_DIR=<clone of scriptures-data> WHISPER_MODEL=<model folder> python3 tools/audio/transcribe.py tools/works/<work>/audio/<id> 0 2`, and the same with `1 2` in parallel.
   - **If the faster-whisper model can't be downloaded** (Hugging Face blocked), or the private repo's Actions cannot run (GitHub billing): `python3 tools/audio/transcribe_onnx.py <audio file> <model folder> tools/works/<work>/audio/<id>/transcripts/<video id>.jsonl` with a Whisper model from GitHub (see the script's header), then mark it finished with an empty `<video id>.jsonl.done`.
   - Commit `transcripts/` as you go, because they are the expensive part.
5. Make the timings: `python3 tools/audio/make_timings.py tools/works/<work>/audio/<id>`. It prints, for each recording, the first and last verse it found. Check that these match the recording. If the speech recogniser missed a line and a verse starts at the wrong place, add its real start to `fixes.json` beside `source.json` (`{video id: {item id: seconds}}`) with the evidence in `fixes.md`, and run this step again. Never edit the generated timings by hand.
6. Build and test: tap ▶ on a reading, then check that the highlighted verse follows the voice at the start, middle and end.

## Time a recording by ear (owner and helpers)
Use this when automatic timing is weak (kīrtan, chant) or a recording has no transcript.
1. Make a starting point: in `source.json` set `"estimate": true` (starts spread by text length) and `"draft": "<why>"`, run `make_timings.py`, build and push. A draft plays only while Audio timing is on.
2. The owner opens the work, turns on ☰ › More settings › Audio timing, plays, and marks verses ("⏱ Starts now", "⏹ Ends now"); the light waits on guessed starts. "Next ▸" in the player bar goes to the next verse still to check and plays it. Helpers do the same and send the owner a file ("Save timings as a file"); the owner opens it ("Open a file") and checks each mark.
3. The owner taps "Publish changes": this opens a GitHub issue "Timing: <path> / <source>". The `timing` workflow applies it (issues from the owner's accounts only: `goyaldarwin`, `darwingoyal`) and closes it. For a draft, the switch "This recording is checked: publish it for everyone" goes with the send: the recording goes live and is marked checked.
4. To verify a send: `gh api repos/goyaldarwin/scriptures/issues/<n>` and `/comments` (REST; GraphQL is unavailable), compare the issue's JSON with `library/<path>/audio/<source>.json` (each sent time exact), read `moved`, and check `gh api repos/goyaldarwin/scriptures/commits/main/check-runs`.
5. Never edit `owner.json` or the generated timings by hand; the issue is the record.

## OCR a scanned book (only where the owner has chosen OCR for it)
`docs/PLAYBOOK.md` §11 ("No OCR") is the rule. Where the owner chooses OCR for a scan without a text layer (the work's `README.md` and the scan's `.meta.json` in `scriptures-data` say so), the OCR runs on GitHub, free here: the `ocr` workflow (Actions tab, or `gh api repos/goyaldarwin/scriptures/actions/workflows/ocr.yml/dispatches -X POST -f ref=main -f inputs[script]=<the work's OCR script> -f inputs[data]=<the PDF's path in scriptures-data> -f inputs[layout]=<layout> -f inputs[ranges]=13-60,61-110 -f inputs[out]=<folder> -f inputs[ref]=<branch>`; at most 256 ranges a run, 14 jobs at once). Each job fetches only that PDF with `DATA_TOKEN` and commits only the OCR text to the branch `ref`. The text is a draft: every word the work's checks flag is read by eye on the page image before it is used (`tools/works/shiva-purana/source/hindi/`).

## Correct or remove a verse in a generated text
- Put the change where the work's text is made (`text.txt`, or, when a script in `source/` makes it, that script's corrections: the Mānas's `text_fixes.json`, `settle.py`'s `FIX` / `ITEM_FIX`), never only in `library/`: a regeneration undoes it. Diff the regenerated file against the previous one and explain every change.
- Item ids are permanent. A removed verse's id is not reused; re-point any topic that started at it; regenerate meanings and audio timings; record it in the work's `reconciliation.md`.
- A changed word: update every meaning of the verse and the work's glossary entry for that word.

## Add a new work (an Upanishad, Japji Sahib …)

1. Place it on the shelf at its address, `<tradition>/<genre>/<group…>/<work>` (`docs/LIBRARY.md` §1), reusing existing levels: e.g. a Hanumān Chālīsā goes to `hinduism/chalisa/hanuman/hanuman-chalisa`, the Kena Upaniṣad to `hinduism/veda/samaveda/upanishad/kena`, Japji Sahib to `sikhism/gurbani/guru-nanak-dev/japji-sahib`. Add the missing shelves to `library/index.json`, ending in `{"id", "work", "path", "title", "by", "edition", "desc"}` (and `salute` if the work has its own). The work id is the shelf id unless that is taken.
2. Create `tools/works/<work id>/` (`tools/works/README.md`): `work.json` (the manifest, with the work's `path`), `text.txt` (the verses, with each verse's language), `README.md`, `reconciliation.md` (the source and every choice), the meanings in `meanings/<lang>/`, and any scripts that make the text from PDFs or pages in `source/`. Add the new words to `library/glossary/<lang>.json` (`docs/LIBRARY.md` §5). `python3 tools/works/export.py <work id>` writes it through the writing standard (PLAYBOOK §3) and makes the transliteration. A new language needs its own entry first (below).
3. Choose the natural divisions for `parts`, the `topics`, and any `plans` (e.g. daily pāṭha). Ask the owner which plans they want. Pages follow the item's section `s`; use a name (e.g. `aarti`), not a number, unless sections are dohā numbers. Verse types the app doesn't know (viniyoga, dhyāna, pada, abhaṅga …) go in the work's `types` (`docs/LIBRARY.md` §2).
   **Write down the hierarchy and its numbering** (part › section › verse) in the work's `README.md`, and give each verse in `text.txt` its own number as the book prints it (`[1.1.1 mantra 1]`, never the full `1.1.1`). If numbers restart in each section or part, say how a verse is cited in `work.json` → `cite` (`docs/LIBRARY.md` §2: the Kaṭha `{"by": ["part", "sec", "n"]}`), or name the sections (`sections`) when they are separate compositions (the Dhūpa Āratī). The build refuses a number printed at a verse's end that is not its `n`, and two verses cited alike.
4. Models: `tools/works/katha-upanishad/` (a Sanskrit text from a book, checked against witnesses), `tools/works/shiv-aarti/` (a short text from printouts and pages), `tools/works/shirdi-sai-dhoop-aarti/` (a multilingual āratī from two printouts), `tools/works/sukhmani-sahib/` (Gurmukhi, line-by-line meanings), `tools/works/sundarkand/` (a work that takes its verses from another).
5. Add audio as above if there is a recording.
6. Give the hard words of its meanings an entry (`docs/LIBRARY.md` §5, "hard"): `python3 tools/meanings/hard_words.py candidates OUT` lists the words of every meaning without one; a writer chooses the hard ones and writes each entry from the dictionaries (`tools/meanings/style.md` §11), a reviewer checks them against their places, then `hard_words.py apply OUT/*.out.json` and `hard_words.py report --reach` (every key reaches only its own word). A sense nobody can confirm goes to `docs/reviews/dictionary-doubts.jsonl`, not to a reader.
7. Build and test the shelf screen, the work's home, the reader, search, and bookmarks.

## Add a new language (for a work in Marathi, Gurmukhi, Braj …)
1. Add it to `library/glossary/languages.json`: ISO 639 code, bilingual name, script, fallback chain (e.g. Braj → Sanskrit), suffix rules and stems. Leave `suffixes` empty until you know the language's inflections; a wrong rule gives wrong roots. Add a `meaning` block only if meanings will be written in it (`docs/LIBRARY.md` §5).
2. Create `library/glossary/<code>.json` with the words of the work's verses (`docs/LIBRARY.md` §5). Write meanings for that language; do not copy Hindi or Awadhi senses because a spelling matches.
3. Set the work's `lang`, and give `l` to any verses in another language. For example, a Gurmukhi Japji Sahib uses `pa`, and a Marathi āratī uses `mr`.
4. If the script is not Devanagari or Gurmukhi, add a font (`tools/fonts`, registered in `tools/site/build.py`) and teach `key()` in `tools/audio/align.py` to read it before aligning audio.
5. Build: the check refuses unknown languages, dictionaries without an entry in `languages.json`, and fallbacks to languages that don't exist.

## Fix a word or meaning in the Rāmacaritamānasa
- Verse text: add the fix to `tools/works/manas/source/text_fixes.json` (and the witness to `reconciliation.md`), then run `(cd tools/works/manas/source && python3 make_appdata.py && python3 make.py) && python3 tools/works/export.py`. The works that take its verses follow (the Sundarakāṇḍa, Śrī Rāmacandra Kṛpālu, and through the Sundarakāṇḍa the Hanumān āratī); make the recordings' timings again (top of this page).
- A Gita Press meaning: the same files and steps (see `tools/works/manas/source/README.md`).
- Our own meaning: `tools/works/manas/meanings/hi/scriptures.json` or `en/scriptures.json`, then `python3 tools/works/export.py`.
- A word meaning: edit `library/glossary/<lang>.json` directly, in the language of the verse (`sa` for the ślokas and Sanskrit stutis, otherwise `awa`).

## Change the app
Edit `tools/site/app.js` (behaviour) or `tools/site/index_template.html` (layout and styles), then build and test. Read `docs/PLAYBOOK.md` §7 (the app) first.

## Try a change on claude.ai before publishing
Publish `dist/Scriptures-artifact.html` as an artifact. YouTube is blocked inside claude.ai artifacts, so test audio on the website.
