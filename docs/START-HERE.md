# Start here: resuming this project

This repository holds everything about the project: the website, the data, every script used to make the data, and the owner's preferences. If the original Claude session is lost, a new session can continue from here.

## Prompt to paste in a new session

> Clone github.com/goyaldarwin/scriptures and read `docs/START-HERE.md`, `docs/PLAYBOOK.md`, `docs/HOW-TO.md` and `docs/LIBRARY.md` before doing anything. Then: **[the task]**. Follow the playbook. Gita Press books are the source of truth. Test at phone size (390×844) with screenshots. Commit and push when done, and tell me in plain words what changed.

## Owner and standards
- Owner: Darwin Goyal (GitHub `goyaldarwin`).
- Accuracy first: the Gita Press books are the only source of truth. Fix discrepancies in the data directly, without notes or annotations. Do not mention AI anywhere in the app.
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
- Pending: a permission letter to Gita Press for the meanings.
