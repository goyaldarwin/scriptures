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
2. Turn the book into `{item id: [meaning, footnotes?]}`. Put the scripts and their intermediate files in `tools/works/<work>/meanings/<id>/` so the work can be redone. Match by the item ids in `library/<path>/work.json`, and check the verse text where possible, not by position alone.
3. Write `library/<path>/meanings/<id>.json` in the format in `docs/LIBRARY.md` §3, with `id`, `lang`, `title` (bilingual) and `m`.
4. Build. The source appears in the reader under Settings → Sources. The default stays as it was unless the new file has a lower `order`.
5. Note the edition and the permission status in the root `README.md` under "Sources and permissions".

## Add a new audio source (another reciter)

1. Choose the id: the reciter's name, e.g. `anup-jalota`. Create `tools/works/<work>/audio/<id>/`.
2. In it, write `source.json`:
   ```json
   {"id": "anup-jalota", "work": "tulsidas/ramcharitmanas", "type": "youtube", "lang": "hi",
    "title": {"hi": "अनूप जलोटा", "en": "Anup Jalota"}}
   ```
3. Write `recordings.json`, one entry per YouTube video in reading order: `{"yt": "<11-char video id>", "file": "<audio file name>", "dur": <seconds>, "order": <n>}`. The video id is in the YouTube link (`watch?v=…`) and in the downloaded file name `[…]`.
4. Transcribe (hours; resumable): `AUDIO_DIR=<folder with the files> WHISPER_MODEL=<model folder> python3 tools/audio/transcribe.py tools/works/<work>/audio/<id> 0 2`, and the same with `1 2` in parallel. See `tools/audio/README.md`. Commit `transcripts/` as you go, because they are the expensive part.
5. Make the timings: `python3 tools/audio/make_timings.py tools/works/<work>/audio/<id>`. It prints, for each recording, the first and last verse it found. Check that these match the recording's day.
6. Build and test: tap ▶ on a day, then check that the highlighted verse follows the voice at the start, middle and end.

## Add a new work (Ram Raksha Stotram, an Upanishad, Japji Sahib …)

1. Place it on the shelf: edit `library/index.json` and add shelves as deep as needed (e.g. Ved › Sāmaveda › Upaniṣad › Kena), ending in `{"id", "work", "path", "title", "by", "edition", "desc"}`. The `path` mirrors the shelf, e.g. `ved/samaveda/upanishad/kena`.
2. Create `tools/works/<work>/` with the extraction scripts (from PDFs or other sources) and an `export.py` that writes `library/<path>/work.json` (`docs/LIBRARY.md` §2), its meaning sources (§3), and new words into `gloss.json` (§5). Use `tools/works/ramcharitmanas/` as the model.
3. Choose the natural divisions for `parts`, the `topics`, and any `plans` (e.g. daily pāṭha). Ask the owner which plans they want.
4. Add audio as above if there is a recording.
5. Build and test the shelf screen, the work's home, the reader, search, and bookmarks.

## Fix a word or meaning in the Rāmacaritamānasa
- Verse text: add the fix to `tools/works/ramcharitmanas/book/text_fixes.json`, then run `(cd tools/works/ramcharitmanas/book && python3 make_appdata.py) && python3 tools/works/ramcharitmanas/export.py`.
- A Gita Press meaning: the same files and steps (see `tools/works/ramcharitmanas/book/README.md`).
- A word meaning: edit `library/gloss.json` directly.

## Change the app
Edit `tools/site/app.js` (behaviour) or `tools/site/index_template.html` (layout and styles), then build and test. Check the playbook's list of past bugs.

## Try a change on claude.ai before publishing
Publish `dist/Scriptures-artifact.html` as an artifact. YouTube is blocked inside claude.ai artifacts, so test audio on the website.
