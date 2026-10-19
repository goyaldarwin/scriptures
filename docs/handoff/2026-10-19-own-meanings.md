# Handoff: write our own meanings where we use others' copyrighted ones

Written 2026-10-19 at the end of a long session, for a fresh session. Paste the prompt below into the new session.

---

## Prompt

> You are continuing work on Darwin Goyal's (`goyaldarwin`) personal, ad-free scriptures library. Live at https://scriptures.craadle.org (GitHub Pages from `main` of the public repo `goyaldarwin/scriptures`), and wrapped as an Android app ("Sunderkand & Ramcharitmanas", package `org.craadle.scriptures.hinduism`, published by the owner's company Craadle; currently in Play internal testing, about to go to production).
>
> **First:** clone `github.com/goyaldarwin/scriptures` and read, in this order: `CLAUDE.md`, `docs/START-HERE.md`, `docs/PLAYBOOK.md`, `docs/HOW-TO.md` ("Add a meaning source"), `docs/LIBRARY.md`, then this file, `docs/handoff/2026-10-19-own-meanings.md`. The private repo `goyaldarwin/scriptures-data` holds raw sources (book PDFs, printouts); it stays private, and its raw files are never copied into the public repo.
>
> **The task:** wherever the library shows meanings that are someone else's copyright, add our own meanings as a new, selectable source, written for this library, so that the app can later drop the copyrighted sources and be free of copyright risk. Details, scope, rules and the plan are in this file. Start with the pilot (the Sundarakāṇḍa), show the owner samples, and only then do the rest.

---

## Why

The app is going public on Google Play. Several meaning sources are other publishers' copyright, included so far "for personal study" with permission pending (see `README.md` → "Sources and permissions"). A store app is far more visible than a website; a complaint can get the app removed and mark the developer account. The owner's decision (2026-10-19): write our own Hindi and English meanings for every place where we rely on such a source; keep both side by side in the app for a while; once he has checked ours and is satisfied, readers will see only ours, while the old sources stay in the repository.

## Scope: what is someone else's, and what we write

| Work | Copyrighted source now shown | Items | What to write |
|---|---|---|---|
| Śrī Rāmacaritamānasa (`library/hinduism/granth/tulsidas/ramcharitmanas`) | `hi-gitapress` (Hanumānprasād Poddār's bhāvārtha), `en-gitapress` | 6,157 verses (6,103 Awadhi, 54 Sanskrit), 7 kāṇḍas: Bāla 1,947 · Ayodhyā 1,647 · Araṇya 355 · Kiṣkindhā 193 · Sundara 343 · Laṅkā 800 · Uttara 872 | Hindi **and** English for every verse |
| — its topic headings (`work.json` → `topics`, 218, Hindi and English) | Gita Press's section headings | 218 | our own short headings (check with the owner first: he may prefer to keep them, as they are brief descriptive labels) |
| — its pārāyaṇa vidhi (`work.json` → `vidhi`, `vg`), the Rāmāyaṇajī kī āratī and the Kathā-visarjana pages | Gita Press's instructional prose | a few pages | our own wording of the instructions; the mantras and stutis themselves are traditional texts and stay |
| Sundarakāṇḍa (`library/hinduism/granth/tulsidas/sundarkand`) | the same Gita Press meanings, **generated from the Mānas** by `tools/works/sundarkand/export.py` | 343 + 11 lead-in + 1 (bal.17.so17) | nothing separately: write them in the Mānas, then extend the Sundarakāṇḍa exporter to carry the new Mānas sources too (its own `hi-scriptures`/`en-scriptures` for the Chālīsā, āratī and opening prayers already exist and stay) |
| Śrī Rāma Rakṣā Stotram (`library/hinduism/stotra/rama/ramraksha`) | `hi-stuti-chalisa-sangrah` (40), `en-vande-guru-paramparaam` (42) | 42 | Hindi and English |
| Shirdi Dhūpa Āratī | `en-shirdisaibabakripa` (62) | — | **nothing to write**: our own `en-scriptures` already covers all 64; only the switch-off later applies |
| Sukhmani Sahib | `en-sant-singh-khalsa` (218) | 218 | English (our Hindi `hi-scriptures` already exists) |
| Īśāvāsya Upaniṣad, Śrī Rudram, Chālīsā, āratī | already our own | — | nothing |

Also note for the owner (do not change without asking): the Rāma Rakṣā's verse text and transliteration follow a YouTube video's on-screen text (the stotra itself is public domain), and the Sukhmani Sahib's transliteration comes from K. Thind's PDF. The risk there is small, but name it.

## The most important rule: write from the original, not from the translation

Copyright protects **wording**, not meaning. A meaning that paraphrases Gita Press sentence by sentence is still derived from Gita Press and does not remove the risk. So:

1. **Read the verse itself** (Awadhi / Sanskrit / Gurmukhi, with our word meanings in `library/glossary/<lang>.json` and the verse's context in the kāṇḍa: who is speaking, to whom, what just happened), and write the meaning from that.
2. Use the existing source **only to check understanding** — a hard word, an allusion, who "he" refers to, a name. Facts and interpretation are free to use; sentences, phrasing, sentence order, distinctive word choices and the publisher's added explanations in brackets are not.
3. **Never** open the old meaning and reword it. Write first, then compare: if ours reads like a reworded copy, write it again.
4. **Check mechanically** before committing: a script that flags any run of 6 or more consecutive words (after normalising punctuation) shared between our meaning and the copyrighted one, for every verse. Short shared phrases that are simply the natural words ("श्रीरामजी", "said Hanumān") are fine; long ones mean rewrite. Keep the script in the repository (`tools/meanings/overlap.py`) and run it in the export.
5. Do not try to "beat" the original by adding commentary. A meaning states what the verse says, faithfully, clearly, in context — nothing invented, nothing left out. Where the verse is genuinely ambiguous or traditions differ, give the plain reading and note the doubt in a review file for the owner (see below), not in the meaning.

## Quality: what a good meaning is here

- **Accuracy first** (the project's first rule), then unambiguity, clarity, consistency.
- **Context of the work:** the Mānas is a devotional epic told in nested dialogues (Śiva to Pārvatī, Kākabhuśuṇḍi to Garuḍa, Yājñavalkya to Bharadvāja, Tulasīdāsa to the reader). Keep the speaker clear. Keep the devotional register: honorifics (श्रीरामजी, श्रीसीताजी, हनुमान्‌जी; "Śrī Rāma", "Sītā"), respectful verbs. Translate the bhakti vocabulary consistently.
- **Hindi:** natural modern Hindi in the house style already used in our own Hindi meanings (`tools/works/sundarkand/meanings/hi.json`, `tools/works/sukhmani-sahib/meanings/hi.json`, Rudram, Īśa). Gita Press joins postpositions (श्रीरामजीको); follow whatever our own existing meanings do, and settle it once with the owner in the pilot.
- **English:** plain, dignified English with IAST for names (Śrī Rāma, Hanumān, Rāvaṇa, Ayodhyā), as in our other English meanings. No archaic "thee/thou".
- **A style sheet first:** before writing, make `tools/meanings/style.md` — how each recurring name, epithet and term is rendered in Hindi and English (Raghunātha, Raghupati, Kosalādhīśa…; bhakti, māyā, dharma, satsaṅga…), verse-number handling (do not copy Gita Press's trailing ।।१७।।), punctuation. Every batch follows it, so 12,000 meanings read as one voice.
- **Length:** about as long as the verse needs. A caupāī gets one or two sentences; a long chhanda more. No filler.
- **Sanskrit ślokas** in the Mānas (54) and the Rāma Rakṣā: translate the Sanskrit directly.
- **Sukhmani Sahib English:** write from the Gurmukhi with our own Hindi meaning and Gurmukhi word meanings as aids; keep Sikh terms as the community uses them (Naam, Waheguru, Gurmukh, Simran…) — put them in the style sheet.

## How it fits the app (no app change needed to add a source)

- A work's meaning sources are files `library/<work>/meanings/<id>.json`: `{"id", "lang": "hi"|"en", "order": n, "title": {"hi", "en"}, "m": {item id: [meaning text]}}`. `build.py` finds them and registers them in `work.json` → `sources`; the reader picks one per language in Settings › Sources. A reader whose chosen source lacks a verse sees the next source by `order`, tagged with its name. See `docs/LIBRARY.md` and `docs/HOW-TO.md`.
- Our own sources are conventionally `hi-scriptures` / `en-scriptures`, titled "भावार्थ — शास्त्र" / "English meaning — Scriptures" (the Sundarakāṇḍa, Dhūpa Āratī, Sukhmani Sahib already have them).
- **The source's name — ask the owner first.** The playbook says "Do not mention AI anywhere in the app", but on 2026-10-19 the owner said the new source should be named as auto-generated, with the AI as the source. Ask him which title he wants (for example "भावार्थ — शास्त्र" / "Meaning — Scriptures", or one that says it was written with AI), and record the answer in `docs/PLAYBOOK.md`.
- Keep the text of our meanings in the tools folder (like `tools/works/<work>/meanings/hi.json`, `en.json`), written by the work's `export.py` into the library, never hand-edited in `library/`. For the Mānas, `tools/works/ramcharitmanas/export.py` builds from `book/app_data.json`; add our files beside it, e.g. `tools/works/ramcharitmanas/meanings/hi.json`, `en.json` (one entry per item id), and have `export.py` write `meanings/hi-scriptures.json`, `en-scriptures.json`. Check that every item has both, exactly once, and nothing extra (the Sundarakāṇḍa exporter shows how).
- **Sundarakāṇḍa:** `tools/works/sundarkand/export.py` copies the Mānas's Gita Press sources for parts 1–2 and `bal.17.so17`; extend it to copy the new Mānas sources too, merged with its own `hi-scriptures`/`en-scriptures` for the Chālīsā, āratī and opening prayers (one source per language, not two with the same id), and extend `check.py` to prove the copies equal the Mānas's.
- **Do not change the Mānas's text, ids or Gita Press files.** The Mānas is the owner's most important work; the new sources only add files.

## Rolling out: side by side, then ours only

1. **Now:** add ours as a second source (`order` after Gita Press), so readers and the owner can switch between them in Settings › Sources. The app is still in internal testing, so this is the "test" phase the owner wants.
2. **The owner reviews** (samples per kāṇḍa, then whatever he wants).
3. **Then, on his word only:** readers see only ours. Do this with a small, general switch rather than deleting files: e.g. a `"retired": true` field in a meaning file that `build.py` honours by not registering the source (so it stays in the repository but nobody sees it), and readers who had chosen it fall back to ours. This applies to the website and the app alike (the app shows the website). Write it as its own small shared-code change with a UX test, and record it in `docs/LIBRARY.md` and the playbook. Update `README.md` → "Sources and permissions" to say what is shown and what is only kept.

## Plan of work

1. **Read** the docs listed in the prompt. Run the three tests once to see a green baseline.
2. **Style sheet** (`tools/meanings/style.md`) and the **overlap checker** (`tools/meanings/overlap.py`).
3. **Pilot: the Sundarakāṇḍa's 343 verses + the 11 Kiṣkindhā lead-in verses + bal.17.so17** (written in the Mānas files, carried to the Sundarakāṇḍa). Show the owner 15–20 verses side by side with Gita Press (a short page or table: verse, ours, theirs) and ask: tone, length, joined or separate postpositions, honorifics, the source's name. Adjust the style sheet. Ship the pilot (Sundarakāṇḍa work + Mānas Sundara-kāṇḍa) once he is happy.
4. **The rest of the Mānas**, kāṇḍa by kāṇḍa, Hindi and English together. It is large (about 12,000 meanings): split into batches (e.g. one dohā-group of ~50 items), and use parallel subagents if available, each given the style sheet, the kāṇḍa's context, the batch's verses with word meanings, and the rule "write from the original". Every batch goes through the overlap checker and a second-pass review (by a separate agent that did not write it) for accuracy against the verse. Commit per kāṇḍa, on a branch, tests green, merge.
5. **Rāma Rakṣā** (Hindi + English, 42) and **Sukhmani Sahib English** (218).
6. **Topics and the vidhi prose** — after asking the owner (step 3 is a good moment).
7. **Doubts file:** `docs/reviews/<date>-meaning-doubts.jsonl`, one line per verse where the reading is uncertain or traditions differ: `{"id", "issue", "our reading", "alternatives"}`. The owner decides.
8. Report to the owner in plain words after each step: what changed, what to check, one next step.

## Ways of working (from CLAUDE.md and the playbook — the essentials)

- Accuracy above all. Never write a **scripture text** from memory (the verses come from the owner's sources); meanings are ours, but they must be faithful to the verse.
- Never route around a blocked site or a copyright limit.
- Before every commit: `python3 tools/site/build.py && python3 tools/site/smoke_test.py && python3 tools/site/ux_test.py`; diff regenerated data before committing it. `git pull` before pushing (a workflow also pushes to `main`).
- Large work on a branch `work/<name>` with a pull request; merge it yourself once the tests pass (the owner has delegated merging).
- Record every new owner preference or lesson in `docs/PLAYBOOK.md` in the same commit.
- No `pkill -f` (it kills the session's own shell). GitHub GraphQL is unavailable: use `gh api` (REST).
- Reply to the owner in plain words: what changed, what to check, one next step. He reads on his phone.
