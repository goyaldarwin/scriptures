# Start here: resuming this project

This repository holds everything about the project: the website, the data, every script used to make the data, and the owner's preferences. If the original Claude session is lost, a new session can continue from here.

## Prompt to paste in a new session

> Clone github.com/goyaldarwin/scriptures and read `docs/START-HERE.md`, `docs/PLAYBOOK.md`, `docs/HOW-TO.md` and `docs/LIBRARY.md` before doing anything. Then: **[the task]**. Follow the playbook. Each work’s source of truth is the source I gave for it (see its README). Test at phone size (390×844) with screenshots. Commit and push when done, and tell me in plain words what changed.

## Two repositories, one hierarchy
| Repository | Visibility | What it holds |
|---|---|---|
| `goyaldarwin/scriptures` (this one) | public | the website, the library data made from the sources (text, meanings, word meanings, verse timings), every script and intermediate file, and the docs |
| `goyaldarwin/scriptures-data` | **private, always** | the raw sources that aren't ours to publish: books, printouts, screenshots, recordings, each with a `<file>.meta.json` (see its README) |

Both use the same address for a work, the shelf path the reader sees: `hinduism/granth/tulsidas/ramcharitmanas` is `library/hinduism/granth/tulsidas/ramcharitmanas/` here and `hinduism/granth/tulsidas/ramcharitmanas/` there. Under a work, the private repo groups files as `<kind>/<source-id>/<file>` (`books/gitapress/hindi.pdf`, `audio/kamlesh-upadhyay/…`). The source id is the same one used here for the meaning or audio source made from it. Never copy anything from the private repo into this one except what the build produces from it.

## Working rules for every session
- **Never push to `main` directly.** `main` is the live website, so every push to it is published.
  - Create a branch (`work/<short-name>`, e.g. `work/sai-aarti`), commit there, push the branch, and open a pull request.
  - The owner merges it after testing.
- **Start from the latest `main`** (`git fetch origin main`), and rebase onto it before opening the pull request. Several sessions may work at once.
- **Run `python3 tools/site/build.py` and then `python3 tools/site/smoke_test.py` before every commit.** The smoke test opens every work in a real browser and fails on any script error.
- **Run `python3 tools/site/build.py` before every commit.** It checks the library and refuses to build if anything is inconsistent. Commit the generated files it produces.
- **Shared code goes first, on its own.** If a work needs something new in the app or the shared tools (`tools/site/`, `tools/audio/`, `tools/jsonio.py`), make that change as its own small pull request first, say why, and build the work on top of it after it is merged. Before writing shared code, check `docs/LIBRARY.md` and the app for a feature that already does it. Two sessions once built the same feature (work-defined verse types) in two different ways, and the pull requests collided.
- **Touch only what your task needs.** A new work adds its own folders: `library/<path>/` and `tools/works/<work>/`. It edits shared files only to add to them: `library/index.json` (one new entry on the shelf), and `library/glossary/languages.json` plus a new `<lang>.json`. Changes to `tools/site/` or `tools/audio/` affect every work, so call them out in the pull request.
- **Ask the owner for the sources** (book PDFs, recording links) instead of guessing. Accuracy comes before speed.

## Owner and standards
- Owner: Darwin Goyal (GitHub `goyaldarwin`).
- **Accuracy comes first, then unambiguity, clarity, consistency and structure.**
  - Each work's source of truth is the source the owner gave for it: the Gita Press books for the Rāmacaritamānasa, a video's on-screen text, a web page, a PDF. That source is named in the work's README.
  - Fix discrepancies in the data directly, and record each fix in the work's `reconciliation.md`, not in the app. Do not mention AI anywhere in the app.
- **Getting a source's text:** the web-fetch tool returns summaries, not whole pages, and most websites are blocked from the shell. For a web page, ask the owner to print it to PDF and add it to `scriptures-data` under `printouts/<site>/`, or to allow the site for the session. Never write a text from memory.
- `docs/PLAYBOOK.md` records every preference and lesson. Keep adding to it whenever the owner states a new preference or a lesson is learned.

## How the pieces fit

```
Gita Press PDFs ─ tools/works/ramcharitmanas/book ─► app_data.json ─ export.py ─► library/…/work.json, meanings/
YouTube recordings ─ tools/audio/transcribe.py ─► transcripts ─ make_timings.py ─► library/…/audio/
library/ ─ tools/site/build.py (checks everything first) ─► index.html, app/, sw.js  +  dist/ (offline file, claude.ai file)
```

- The verse text and its number are the core of each work. Hindi meaning, English meaning and audio are interchangeable sources that the reader picks in Settings. Word meanings (`glossary/<lang>.json`) are fixed and shared, one dictionary per language. Each verse is looked up in its own language: Awadhi for most of the Mānas, Sanskrit for its ślokas and Sanskrit stutis.
- The app is the same for every work: the shelf screen, the work's home (divisions and plans with ▶), and a continuous-scroll reader with a section picker at the bottom. Bookmarks, notes, progress and hands-free recitation are built in.
- Readers' personal data stays in their browser (localStorage, key `manas.personal.v1`; v2 format with keys prefixed by work id).

## Common tasks
See `docs/HOW-TO.md`: add a meaning source, add a reciter, add a work, fix text, change the app, publish.

## Status (October 2026)
- Śrī Rāmacaritamānasa: the full text, Hindi and English meanings, glossary, topics, plans and vidhi are complete.
- Audio (Pt. Kamlesh Upadhyay): days 1–10 and 15–17 are timed. 11–14 and 18–30 still need transcribing (`tools/audio/README.md`). There is no recording for day 26.
- Śrī Rāma Rakṣā Stotram (Stotras shelf): text, English and Hindi meanings, word meanings and audio (Vande Guru Paramparaam) are complete.
- Pending: a permission letter to Gita Press for the meanings.
