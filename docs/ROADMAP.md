# Roadmap: keeping the library sustainable

The owner's priorities, in order: **accuracy**, then unambiguity, clarity, consistency and structure. This page lists what protects them and what should come next. When an item is done, move it to "In place" with one line on how it works.

## In place
- **One hierarchy everywhere.** A work's address (`<tradition>/<genre>/<group…>/<work>`) is the folder in `library/` and in the private `scriptures-data`, and the shelf in the app from the genre down (the app shows no tradition). `build.py` refuses a path that doesn't match the shelf.
- **Permanent ids.** Work ids, item ids and source ids never change, so readers' bookmarks, notes and progress survive any reorganisation (`renamed` in `work.json` moves them when a verse is split).
- **Checks before anything goes live.**
  - `build.py` checks the library: sources, item ids, line-by-line meanings, plans, languages, dictionaries, a meaning for every word of every verse, paths and the store apps' shelves. It also refuses an `app.js` that doesn't parse.
  - `regen_check.py` makes the library again in an empty folder (`tools/works/export.py`, `make_timings.py`) and fails if `library/` differs from it, so a hand edit to generated data, or a generator changed without regenerating, is caught.
  - `smoke_test.py` opens every work in a browser; `ux_test.py` checks navigation and reading at phone size.
  - GitHub Actions (`check.yml`) runs them all on every pull request and every push to `main`. It also fails if the committed website differs from what the build makes.
- **Sources separated from results.** Raw books, printouts and recordings live privately in `scriptures-data`, each with a `.meta.json` (origin, checksum, rights, what it feeds). The public repo holds only what is built from them, plus every script.
- **One folder per work, one format, one exporter.** `tools/works/<work id>/` holds the work's manifest, text, meanings per language, recordings and source scripts (`tools/works/README.md`); `build.py` refuses a work without its folder and required files.
- **Generated, never hand-copied.** A work that reuses another's text, like the Sundarakāṇḍa from the Mānas, takes its verses by id (`[take …]` in `text.txt`), and `regen_check.py` keeps the two identical.
- **Parallel work without collisions.**
  - Branches and pull requests.
  - Shared code goes to `main` first, on its own.
  - Shared files are written one entry per line, so additions from different branches merge.
  - Transcription runs in the cloud, one machine per recording.
- **Audio times set by ear, safely.** The app's Audio timing mode sends the owner's times as a GitHub issue; the `timing` workflow applies them to `owner.json`. The order rule that places the other verses around them is the same in the app and the builder (`tools/audio/order.py`), and `ux_test.py` checks that they agree.
- **Copying is checked.** `tools/meanings/overlap.py` stops any meaning of ours that shares 10 or more words in a row with a copyrighted one.
- **The hard words of our meanings can be tapped.** Every work's hard Hindi and English meaning words have an entry (`"hard": true`, `docs/LIBRARY.md` §5), written from the dictionaries and reviewed; `tools/meanings/hard_words.py report --reach` shows what the app underlines, and every word sense left open was settled from the dictionaries (Monier-Williams, Apte, Platts) and the Gurbani commentaries (`tools/meanings/platts.py`, `teeka.py`), so `docs/reviews/dictionary-doubts.jsonl` holds only new doubts.
- **Rules are written down.** `docs/PLAYBOOK.md` holds preferences and rules, `docs/LIBRARY.md` the format, and `docs/HOW-TO.md` the procedures. Git holds the history.

## Next (highest value first)
0. **The whole Sri Guru Granth Sahib, with Punjabi meanings only** (the owner's choices; branch `guru-granth-sahib`). The sources are in `scriptures-data` at `sikhism/gurbani/guru-granth-sahib/books/` (`shabdarth/`, `santhya/`, each with its OCR in `ocr/`).
   - **Text:** the Shabad OS database (`@shabados/database` on npm, CC BY-SA, credited), checked word for word against the Gurbani printed in the Darpan and the Faridkot Teeka (`tools/meanings/teeka.py fetch`), every difference in `reconciliation.md`. Parts are the 51 sections of the Granth (the opening banis, the 31 raags, the closing compositions); **one verse is one shabad** (or pauri, salok), its lines as the Granth prints them; ids by the Ang it starts on (`14.1`, the first shabad starting on Ang 14), permanent. The Japji and Sukhmani Sahib are taken from their works (`[take japji-sahib mool .. salok.close]`, `[take sukhmani-sahib a01.title .. a24.p8]`). `load: "parts"`; `words: "partial"` until Punjabi word meanings are written.
   - **Meanings, Punjabi only (no Hindi, no English):** `meanings/pa/santhya.json`, Bhai Vir Singh's Santhya (Ang 1 to about 607), copied, the default meaning there (`order` 1; the owner); `meanings/pa/shabdarth.json`, the Shabdarth (SGPC 1936–41, mainly Teja Singh), copied: its line meanings line by line, its padarth word meanings as notes, the meaning of the whole Granth (`order` 2: the default from Ang 608, where the Santhya ends, through the app's filling in from a work's other source of the same language, and the second meaning of Ang 1–607); `commentary/pa/faridkot.json`, the Faridkot Teeka (from the Shabad OS database, typed, line by line).
   - **Accuracy of the OCR (the owner's choice, "two-witness check"):** the 1936–41 print's OCR is compared word by word with the 2009–12 reprint's; every disagreement is settled on the page image of the 1936–41 print (the 1939 volume a third witness where it covers the page); the Santhya's doubtful words are read on its page images (pothi 6 has a second scan). Ang by Ang, a batch goes live when it is settled; the rest stays out (`partial`).
   - **Order:** the text and the Faridkot commentary first (no OCR; in place: `tools/works/guru-granth-sahib/`), then the Santhya batch by batch from Ang 1 to its end (about Ang 607), then the Shabdarth from Ang 608 to 1430 (so the whole Granth has a Punjabi meaning), then the Shabdarth for Ang 1–607.
1. **Our own meanings for the rest of the Rāmacaritamānasa.** Ours cover every kāṇḍa but the Bāla-kāṇḍa; Gita Press is still the only meaning of the Bāla-kāṇḍa (about 1,960 verses, Hindi and English), of the Mānas's topic headings and of its pārāyaṇa vidhi prose (the mantras stay). Write them as for the Sundarakāṇḍa: from the verse, never from the translation (`tools/meanings/style.md`), in batches, by `docs/HOW-TO.md` → "Write our own meanings for a kāṇḍa of the Mānas" (`prepare.py`, then for each batch a writer, a reviewer, a copy audit and an accuracy check, then `apply_batches.py`), each checked by `overlap.py`, one piece per verse line; kāṇḍa by kāṇḍa on a branch. Then, on the owner's word only, readers see only ours: a small switch (e.g. `"retired": true` in a meaning file, honoured by `build.py`), not deleted files.
2. **Check the private repo too.** Add a `check.yml` in `scriptures-data`:
   - every file has a `.meta.json`;
   - every checksum matches;
   - every path is a work in the public library;
   - every public `recordings.json` → `data` exists.
3. **Make each audio source's state visible.** Generate a table per recording (transcribed / timed / verses covered / hand fixes / verses to check) from the data, so "what's left?" is answered by a file, not by memory.
4. **Run the whole audio chain with one command.** A single command per source: transcribe in the cloud, wait, sync, time, build, open a pull request.
5. **Settle uncertain readings with the owner's printed copy.** Where a text came from the web (Chālīsā, āratīs), compare it with a Gita Press print when the owner provides one. Record the outcome in the work's `reconciliation.md`.
6. **Check audio against what is sung.** After timing, read each verse's transcript segment against its text, and flag verses where the reciter's wording differs. This catches both text errors and timing errors.
7. **Finish the timings by ear.** The Sukhmani Sahib recording is published with every start not yet set by ear listed to check; the owner checks them under ☰ › More settings › Audio timing (`docs/HOW-TO.md` → "Time a recording by ear"). Helpers can mark too and send the owner a file. The Mānas recording still has verses to check, and one dohā (`aranya.46.do46ख`) without a time.
8. **Player buttons for timing** (offered to the owner): "⏹ End" and "⏱ Next starts" beside play/pause, so marking needs no scrolling.
9. **Punjabi word meanings.** Fill in `pa` in `library/glossary/pa.json` (`docs/design/languages.md` §2).
10. **The Android app** (`docs/APPS.md`): the content-rights decision, then the Play release. The iPhone app is parked.
