# The sweep: a correctness and consistency audit of every work, the app and both repositories

This is the prompt for a full audit session. Start a session on `goyaldarwin/scriptures` (it attaches `goyaldarwin/scriptures-data`) and say: **"Run docs/SWEEP.md."** It may take several sessions. Each one picks up from the checklists already written in `docs/reviews/sweep/` and goes on.

Your job: find and fix every error and inconsistency in the library, the app and the two repositories. That includes the kinds of error the owner has reported, and every other instance of each kind. Then publish the fixes and report in plain words. Accuracy comes first, then unambiguity, clarity, consistency and structure. Never assume a check passed: check it against the source and in the app.

---

## 0. Before anything

1. Read, in full: `CLAUDE.md`, `docs/START-HERE.md`, `docs/PLAYBOOK.md`, `docs/HOW-TO.md`, `docs/LIBRARY.md`, `docs/WORKS.md`, `tools/works/README.md`, `tools/audio/METHOD.md`, `tools/meanings/style.md`, and `docs/reviews/chalisa-aarti-namavali-audit.md`. The last is the previous audit, and it shows the kinds of error to expect. Follow every rule in these files. Where two of them disagree, that is a finding (§D).
2. Run `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check` before you read any meaning.
3. Run `git pull` in both repositories. Then read `git log` for the whole history of `scriptures` (`git log --stat`, and the messages in full). Each "fix", "the owner:" or "never again" is a mistake that was made once. Collect them in `docs/reviews/sweep/lessons.md`, one line each: what went wrong, the rule it became (PLAYBOOK section), and whether a test now guards it. That list drives §E (tests) and tells you where the same mistake is likely to repeat.
4. Make the inventory (start from `docs/WORKS.md`, which the build makes: every work's levels, verse types, citation, meanings and recordings, and what is not yet the same in every work): every work in `library/index.json` and `tools/works/*`, with its religion and shelf, language(s), parts and sections, verse count, meaning sources per language, word dictionaries, recordings and their sources, and its sources in scriptures-data. Write it to `docs/reviews/sweep/inventory.md`. A work in one place and not the other, an orphan folder, or a recording with no source is a finding.
5. Create a task list: one item per area below, then one per work.

**Hard rules, from CLAUDE.md and the PLAYBOOK:**
- Never write a scripture text, a meaning or a word sense from memory. Texts come from the owner's sources in scriptures-data, or from web sources he allows. Every textual choice goes in the work's `reconciliation.md`.
- Never route around a blocked site or a copyright limit.
- scriptures-data is private, always. Never copy its raw files into the public repository.
- Change data in its generator (`text.txt`, `settle.py`, an exporter, `fixes.json`), never in a generated file. Diff every regenerated file before you commit it.
- Audio timings follow `tools/audio/METHOD.md`. A start set by hand is checked with `tools/audio/windows.py` and goes in `fixes.json`, with the windows it was read from quoted in `fixes.md`.
- Run `python3 tools/site/check.py` before every commit. Run `git pull` before every push. Files state the current state only: no change logs. A new rule or lesson goes into `docs/PLAYBOOK.md` in the same commit as the change it comes from.
- Do not use `pkill -f`. GitHub GraphQL is not available, so use `gh api` (REST).
- **Helpers (subagents) may read in breadth, but you verify every fix yourself** against its source before it goes in. Apply only the fix, never the helper's note or instruction. A helper's finding that changes a reading `reconciliation.md` already settled is rejected unless the source shows it. Never import or re-run a script that writes files just to reuse a variable from it.
- **Decide; do not leave doubts for the owner.** Settle each doubt from the witnesses, the grammar, the metre and the dictionaries, and record the decision. Ask the owner only when a decision is really his: a name's spelling, a version of a text, a UX choice he has not made.

---

## A. Every work, one by one

For each work, write `docs/reviews/sweep/<work id>.md`: what was read, what was found and what became of it (fixed / settled and recorded / not taken, with the reason). Go shelf by shelf, starting with the newest works.

### A1. Sources and placement
- Every source named in the work's README and `reconciliation.md` exists in **scriptures-data** (book PDFs and page images, printouts, witness texts, audio files, transcripts), at the path given. List missing ones. Do not fetch replacements unless the owner allows that site.
- The work sits on the right shelf: religion › tradition or deity › kind › work, as `docs/LIBRARY.md` defines it (`hinduism/aarti/<deity>/<work>`, `sikhism/gurbani/…`). Its group, title, `by` and `from` are right and spelled as its siblings spell them. `index.json`, `work.json` and the work's README agree.
- **Religion and tradition are clearly classified in both repositories,** even though the app shows no religion. Folder trees in `library/`, `tools/works/` (or its index) and scriptures-data follow one scheme. Write that scheme down in `docs/LIBRARY.md` and `scriptures-data/README.md`, and move anything that breaks it (with `renamed`/`removed.json` where ids or paths are public).

### A2. Text against its sources (accuracy)
- Compare the text word by word against the base witness, then the other witnesses. Every difference is either fixed or recorded in `reconciliation.md` with its reason. Look for typing slips, broken words, missing or extra spaces in names (राम सागर / रामसागर: keep a split only where both printed witnesses split it), dropped signs, and OCR confusions.
- Names take their standard spelling, not a printout's slip. The owner's ruling: साई, not सायि. Look for the whole class: शिर्डी/षिर्डी, -माई/-मायि, जन्मे/जन्में, and every other name that is spelled two ways in the library.
- **Accents and Vedic marks** (§7 of the owner's list): every Vedic text keeps its svaras as the source prints them, and the transliteration shows them as `docs/PLAYBOOK.md` §3 says. Check that the same mark is the same Unicode character everywhere: no look-alikes, NFC, ꣳ only in the Yajurveda, the avagraha used where the source has it, ॥ as one character, compact verse numbers. Any non-Vedic text with an accent mark is a finding.
- The standard of `tools/text/standard.py` holds: Pāṇini's nasals in Sanskrit, ॐ, no commas in āratīs, ISO 15919 transliteration made from the verse.
- In an āratī: the refrain is shown once, the text follows the recording's version, and a stanza the recording leaves out stays in the text untimed.

### A3. Numbering and hierarchy (owner's 1, 2, 4, 5)
- Every work is part › section › verse. Write down, for each work, what its levels are in its own tradition, and check that the data follows them. Examples: the Mānas groups by dohā and chaupāī (Doha 106 = the chaupāīs before dohā 106 and the dohā); the Kaṭha by adhyāya.vallī.mantra; Gurbani by Ang and place; a Chālīsā by dohā / chaupāī / closing dohā; a Nāmāvalī by name number. Put this table in `docs/LIBRARY.md`.
- Each verse's `n` and citation `c` come from one rule (`work.json` → `cite`, `tools/text/cite.py`). The number printed at the verse's end is its own. No two verses of one type are cited alike in one place.
- **One source of truth for a verse's number** (owner's 2 and 5). The number in the reader, in the player bar, in the YouTube playback text, in Resume, in Go to / Back to, in bookmarks, in notes and in the number search must all be the exporter's `c`, and nothing computed on the side. Trace each place in `app.js` and show that it reads `c`. Then test it in the browser on at least the Mānas, the Kaṭha, the Gītā, a Gurbani bāṇī, the Vālmīki Rāmāyaṇa, a Chālīsā, an āratī and a Nāmāvalī.
- **Search by the number being played** (owner's 3): typing the number shown in the player (10.2, 2.1.1, 106.3, Ang 14.2, …) finds that verse in every work. Add a test for each citation style.
- Section names: a section that restarts the numbering has a name. Opening verses are named by type and number, never "Dohā 0" or "Invocation".

### A4. Meanings (owner's 8)
- Every verse has our Hindi and English meaning, where the work has them. Each one says what the verse says: names, who speaks to whom, nothing added, nothing missing. The language follows `tools/meanings/style.md`: names in IAST, the same name spelled the same way throughout, joined postpositions in Hindi.
- **Find where an agent's note or instruction was written into data**: a sentence in English inside a Hindi meaning or a verse; "(record …)", "should", "re-gloss", "here" or "this āratī" in a data file; a placeholder. Search for these patterns across the whole library.
- Each meaning source has a title and an `order`. Ours comes first. A copied source is kept as printed. Run the copy check (`tools/meanings/overlap.py`) against every copyrighted source.
- The meaning split per line (`p`) matches the verse's lines.

### A5. Word meanings: verse words and hard words of the meanings (owner's 9, and checks 1 and 3)
- Every word of every verse has an entry. Meaning, root, grammar and parts agree with each other and with the verse's sense. Check against Monier-Williams and Apte for Sanskrit, Platts for Awadhi and Braj, the Śabdasāgara, and Mahan Kosh.
- **One dictionary per language, shared, with work-specific overrides** (`library/glossary/<lang>.json`, and the work's own `glossary/<lang>.json` for a sense only that work needs). A shared entry never says "here" or "this āratī". It gives the general senses, and a sense that belongs to one work names that work. Find every shared entry that breaks this.
- **Hard words in all works** (check 1): each underlined word of a meaning opens its own entry, never another word's. परे must not open परा; जाये must not open जाया; a plural is read as its own singular. Only hard words are underlined: a plain word (परे, बन्द, जाये) is never marked `hard`. Every hard entry is reached by a word that actually occurs in some meaning. Run `tools/meanings/hard_words.py` report on every work and read its output.
- Languages are kept apart: a Hindi meaning's words are looked up in Hindi, the English meaning's words in English, and a verse's words in the verse's language with its fallback chain. An Awadhi verse that falls back to a Sanskrit entry ("होता → होतृ") is a finding.

### A6. Language of every verse (owner's 10)
- Every verse has a language: `l` on the item, else the work's `lang`. Check that the language is right: a Sanskrit śloka inside a Hindi work, a Braj pad, a Gurmukhi line. Every language is in `library/glossary/languages.json` with its own dictionary. Write down how this is managed and where it is checked, and add a test if none exists.

### A7. Audio (owner's 6 and 8; the previous audit's biggest class)
For **every** recording of every work:
- The recording plays its own stretch: a song inside a jukebox has `start`/`end` in `recordings.json`, and a part of a longer recording uses `take`, `from` or `to`.
- In the app (phone size, a real browser), the player starts at the work's first sung verse, stops at the end of its track, and shows the track's length.
- Hear a sample of verses with `tools/audio/windows.py`: the first, the last, about every tenth, every verse in `check.json`, and every hand start in `fixes.json`. The last 5-s window that still begins with a line's first words is at that line's start; the first window that does not is after it.
  - A hand start that is really a transcript segment's start, early on music or the line before, is wrong.
  - In an āratī, MMS often takes a stanza's repeat.
  - A verse kept from the transcript (MMS unsure) is often a line early.
  - A verse the recording does not sing must be untimed (the Santoṣī Chālīsā's opening dohā). It must not be back-filled.
- Fix through `fixes.json`, with the windows in `fixes.md`, then run `make_timings.py`, diff the result, and listen to the fixed verses in the app.
- `aligned.md` holds the scoring figures where the owner has set starts by ear.
- **Audio timing (by ear) works the same way in every work and every recording,** not only in the Mānas: timing mode, ⏱ Starts now / ⏹ Ends now, ✓ Correct, Next ▸, the check list, the flags and the `timing` workflow. Test it on one recording of each kind: a whole video, a jukebox track, a taken recording, and a recording of a split work.

### A8. Storage consistency (owner's 8 and 14)
Every work is stored the same way, as `tools/works/README.md` and `docs/LIBRARY.md` describe:
- the text, with its `reconciliation.md` and README;
- `meanings/<lang>/<source>.json` for each source and language;
- `glossary/<lang>.json`;
- `audio/<source>/` with `source.json`, `recordings.json`, `fixes.json` / `fixes.md`, `aligned.json` / `aligned.md`, `check.json` and transcripts.

Any work that does it differently is listed. It is either brought into line, or the difference is documented with its reason.

---

## B. The app (owner's 6, 11, 12, 13)

Test at phone size (390×844, and 360) in a real browser, in Hindi and in English, light and dark. Look at the screenshots before you say anything works.

- **Every flow and screen:** the shelves, a work's page, ⓘ About, the reader, sections and topics, the verse menu ⋮, the word sheet, meanings (whole / per line), footnotes and commentary, search (text, number, word), bookmarks, notes and corrections, Resume, Go to / Back to, the player (play, ⏮ ⏭, speed, recitation follow, sleep/stop, background tab), timing mode, Review timing flags, the To-check list, Send to the library, the settings, share, the install and store pages, offline use and split works. Each must do what the PLAYBOOK says, the same way in every work.
- **Every setting** under ☰ and ☰ › More settings: switch it, see it take effect, reload, and see it kept. A setting is never shown where it does nothing.
- **The overlay capsules** (owner's 13): list every capsule and toast. That means the white ones and the black ones, and each saffron chip and button (Next ▸, the ±step chip, the timing chips, the flags, the toasts). Write down what each colour means (for example: white for information about the verse or work, black for transient system messages). Make every use follow that meaning, with the same shape, size, position, timing and dismiss behaviour. Put the rule in the PLAYBOOK, §7.
- **Saffron headers in āratīs, Chālīsās and other texts** (check 6): section headings and topic headings (`@topic`), their wording, their language pair, their capitalisation and transliteration style, where they appear and how they look. They should be consistent within a shelf and across shelves. Chālīsās should have the same set: the opening dohā(s), chaupāī groups by topic, the closing dohā. Āratīs should follow one convention. Write the convention down.
- The jukebox and track behaviour, and the hard-word underlines, in several works.

## C. Speed of build and test (owner's 18)
- Time each step of `tools/site/check.py` (build, regen_check, history_check, smoke_test, ux_test shards) and of CI. Find the slow parts: regen_check re-exporting everything, browser tests opening 174 works, YouTube loads that the sandbox refuses, fixed `wait_for_timeout`s.
- Make them faster without losing coverage:
  - regenerate and check only the works a change touches, with the full run in CI;
  - cache what does not change;
  - wait on a condition rather than a timeout;
  - split work across shards by measured time;
  - give a data-only change a quicker path.
- Record the before and after times in `tools/site/README.md`, and keep `check.py`'s rule that a commit is checked before it is made.

## D. Instructions, scripts and documentation (owner's 16, 17, 21)
- Every procedure in `docs/HOW-TO.md`, `tools/*/README.md` and `METHOD.md` matches the code. Run each command as written on a scratch branch. A step that no longer works, a flag that does not exist, a file the code no longer reads, or a figure that is out of date is a finding.
- Every docstring and comment in `app.js`, `make_timings.py`, `library.py`, `export.py` and the other tools says what the code now does. The format in `docs/LIBRARY.md` matches what `library.py` checks and what the app reads, field for field.
- The PLAYBOOK's principles are unambiguous and do not contradict each other or the docs. Each rule is applied in every work, and each rule that can be checked by code is checked by code (§E).
- **Adding a work** (owner's 14): walk through adding one of each kind (a Chālīsā, a Sanskrit stotra with accents, a Gurbani bāṇī, a split work, a work with two recordings, one of them a jukebox track). Each should be a short, clear and identical procedure. Write it as one checklist in `docs/HOW-TO.md`. Where it needs hand steps that a script could do, write the script.

## E. Tests (owner's 19)
- Use `lessons.md` from step 0.3: every past mistake should have a test that fails if it comes back. List those without one and write them. Examples:
  - the number search for each citation style;
  - one source of truth for numbers;
  - jukebox start, end and length;
  - an unsung verse left untimed;
  - a shared entry with "here";
  - an agent's note in data;
  - a plain word marked hard;
  - a hand start without windows in `fixes.md`;
  - a doubts file left behind;
  - a name spelled two ways;
  - a work that breaks the storage layout;
  - a setting that does nothing;
  - a capsule that breaks the colour rule.
- Prefer a build check (`library.py`) for a data rule, and a UX test for a behaviour.

## F. What else? (owner's 20)
Think about what has not been listed and look for it. For example:
- Every id and path is permanent, or renamed through `renamed`/`removed.json`.
- Saved places, bookmarks, notes and owner timings still point at existing verses.
- Unicode: zero-width joiners, look-alike letters, NFC.
- Fonts render every character used (Gurmukhi, Vedic marks).
- Accessibility: labels, contrast, tap sizes.
- Hindi and English UI strings are complete and consistent.
- The service worker and offline cache are not stale.
- `apps.json` and the store pages are right.
- Privacy page; licences and attributions of copied sources.
- Recordings whose YouTube video is gone or region-locked (check through the owner).
- Transcript files committed but unused.
- Large files that slow the site.
- Error handling when a part or meaning fails to load.
- What a new reader sees on first open.

---

## Working method
- **Small pull requests, one subject each.** A fix to shared code (the app, a tool, the build) goes first on its own pull request, with its test; data fixes follow, one shelf or one class at a time. Each pull request needs `check.py` passing, green CI and a merge. Then check the live site (scriptures.craadle.org) at phone size in a browser. If no browser is connected, say so and check the deployed files and the Pages run instead.
- Write every lesson and new rule into `docs/PLAYBOOK.md` in the same commit as the change.
- Keep `docs/reviews/sweep/` up to date as you go, so a later session can continue from it. Delete any doubts file once it is settled.
- **Report to the owner in plain words** when a stage is done and at the end: what was wrong, what you fixed, what you could not settle and why, and one next step. Keep it short; he reads on his phone.
