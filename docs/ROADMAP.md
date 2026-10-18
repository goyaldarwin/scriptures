# Roadmap: keeping the library sustainable

The owner's priorities, in order: **accuracy**, then unambiguity, clarity, consistency and structure. This page lists what is in place to protect them and what should come next. Keep it current: when an item is done, move it to "In place" with one line on how it works.

## In place
- **One hierarchy everywhere.** A work's address (`<tradition>/<genre>/<group…>/<work>`) is the shelf in the app, the folder in `library/`, and the folder in the private `scriptures-data`. `build.py` refuses a path that doesn't match the shelf.
- **Permanent ids.** Work ids, item ids and source ids never change, so readers' bookmarks, notes and progress survive any reorganisation.
- **Checks before anything goes live.**
  - `build.py` checks the library: sources, item ids, plans, languages, dictionaries and paths. It also refuses an `app.js` that doesn't parse.
  - `smoke_test.py` opens every work in a browser.
  - GitHub Actions (`check.yml`) runs both on every pull request and every push. It also fails if the committed website differs from what the build makes.
- **Sources separated from results.** Raw books, printouts and recordings live privately in `scriptures-data`, each with a `.meta.json` (origin, checksum, rights, what it feeds). The public repo holds only what is built from them, plus every script.
- **Generated, never hand-copied.** A work that reuses another's text, like the Sundarakāṇḍa from the Mānas, is generated from it on every build, with a check that the two are identical.
- **Parallel work without collisions.**
  - Branches and pull requests.
  - Shared code goes to `main` first, on its own.
  - Shared files are written one entry per line, so additions from different branches merge.
  - Transcription runs in the cloud, one machine per recording.
- **Audio times set by ear, safely.** The app's Audio timing mode sends the owner's times as a GitHub issue; the `timing` workflow applies them to `owner.json` and refuses any change beyond the verses sent and their re-placed neighbours. The light waits on guessed starts; the same ordering rule runs in the app and the builder.
- **Decisions are written down.** `docs/PLAYBOOK.md` holds preferences and lessons, `docs/LIBRARY.md` the format, and `docs/HOW-TO.md` the procedures.

## Next (highest value first)
1. **Check the private repo too.** Add a `check.yml` in `scriptures-data`:
   - every file has a `.meta.json`;
   - every checksum matches;
   - every path is a work in the public library;
   - every public `recordings.json` → `data` exists.
2. **Make each audio source's state visible.** Add a table per recording (transcribed / timed / verses covered / hand fixes), generated into `docs/AUDIO-STATUS.md`, so "what's left?" is answered by a file, not by memory.
3. **Run the whole audio chain with one command.** A single command per source: transcribe in the cloud, wait, sync, time, build, open a pull request.
4. **Settle the dictionary doubts.** The full review (2026-10-18) corrected 879 entries across sa, awa, mr and pa (the Rudram's and Sukhmani's words included); the doubts left are in `docs/reviews/2026-10-18-dictionary-doubts.jsonl`, to settle one by one with the owner.
   - List words whose dictionary sense was written for one work but appears in another.
   - Review them per language.
   - Move work-specific senses into that work's `glossary.json`.
5. **Settle uncertain readings with the owner's printed copy.** Where a text came from the web (Chālīsā, āratī), compare it with a Gita Press print when the owner provides one. Record the outcome in the work's `reconciliation.md`.
6. **Check audio against what is sung.** After timing, read each verse's transcript segment against its text, and flag verses where the reciter's wording differs. This catches both text errors and timing errors.
7. **Release notes.** A short `CHANGELOG.md` entry per merged pull request (what readers will notice), so the owner can see what changed without reading commits.
8. **Finish the drafts by ear.** The owner marks the Śrī Rudram and the Sukhmani Sahib in Settings › Audio timing and publishes each from there (see the playbook, "Audio timing by ear"). Helpers can mark too and send the owner a file.
9. **Player buttons for timing** (offered to the owner, not built): "⏹ End" and "⏱ Next starts" beside play/pause, so marking needs no scrolling.
