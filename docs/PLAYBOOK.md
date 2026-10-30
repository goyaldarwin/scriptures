# Playbook: the owner's preferences and the project's rules

Every rule here is current. When the owner states a new preference, or a lesson changes how we work, change the rule here in the same commit as the change. Do not add dates, "was / used to / superseded" notes or stories: git keeps the history. Where a rule has a reason, the reason is given in the present tense.

Contents: 1 Working with the owner · 2 Sources and accuracy · 3 Texts · 4 Meanings · 5 Word meanings · 6 The library · 7 The app · 8 Audio · 9 Apps and store · 10 Engineering · 11 Extraction techniques

---

## 1. Working with the owner
- **Accuracy over speed.** Then unambiguity, clarity, consistency and structure. The owner "loves and admires consistency".
- **Plain words.** Say what changed, what to check, and one next step. The owner reads on his phone.
- **Never leave him looking at "processing":** send a short progress line (what is happening, what is done, roughly how long the rest takes).
- **Ask only when a decision is really his.** Otherwise pick the sensible option and say so.
- **Show it working:** test at phone size (390×844) and look at the screenshots before saying it is done.
- **Be honest about limits:** what the session cannot reach (most websites, Hugging Face, YouTube), what runs on the workspace (speech recognition does not use Claude usage; Claude's own reading and writing does), and that background jobs stop after 2 hours.
- **The owner shares files himself** (book PDFs, printouts, screenshots, a recording's audio file with the YouTube id at the end of its name). Nobody else is ever asked to upload anything.
- Only the owner's repositories for this project are read or changed (`goyaldarwin/scriptures`, `goyaldarwin/scriptures-data`).

## 2. Sources and accuracy
- **Never write a scripture text from memory.** Each work's text comes from the source the owner gave for it (a book, a printout, a video's on-screen text, a web page he allows), named in the work's README.
- **Fix, don't annotate.** A discrepancy is fixed in the data, never shown in the app (no "पाठभेद" tags, no variant markers, no notes about accuracy). Every fix is recorded in the work's `reconciliation.md`: what the source has, what the text has, why.
- **Correct a source only where it is clearly wrong:** a typing slip, a broken word, a missing space, a sense that does not fit, broken Sanskrit. Otherwise keep its words.
- **One witness:** keep its words; mark each correction **open** in `reconciliation.md`, and ask for a second witness (a printed copy) to settle it.
- **Two witnesses:** the one the owner prefers is the base, the other checks it. Where several witnesses disagree, follow the majority and say so.
- **Widely available texts** (a Chālīsā, an āratī) may come from two or three good web sources when the owner says so; reconcile word by word.
- **Spelling in Tulasīdāsa's works** follows the Gita Press house style of our Mānas (ए not ये; ब/स forms; joined compounds; no hyphens); where sources disagree on a word, the metre decides.
- **A verse that belongs to a bigger work is taken from it by id, never retyped** (`[manas bal.17.so17]` in a `text.txt`), so a correction there reaches every copy, and a check proves the copy is equal.
- **Never route around a blocked site or a copyright limit.** From these sessions the shell reaches GitHub and little else; the fetch tool returns summaries, not whole pages. Ask the owner for the page as a PDF (into `scriptures-data`), or to allow the site.
- **`goyaldarwin/scriptures-data` is private, always.** Its raw files are never copied here; only what the build makes from them.
- **Reference books** (dictionaries, commentaries) are used to check facts, never copied (`tools/meanings/style.md` §11).

## 3. Texts
- **The verse and its number are the core of each work.** Item ids are permanent: bookmarks, notes, progress and audio times point at them. A removed verse's id is never reused; a renamed one goes in `work.json` → `renamed`.
- **Change a text in its generator** (`text.txt`, `settle.py`, the exporter), never only in a generated file: a regeneration undoes it. Before committing a regenerated file, diff it against the previous one and explain every change.
- **Removing a verse:** drop it in the generator, re-point any topic that started at it, regenerate meanings and audio.
- **Verses put before a work's text** (an opening a recording sings) need `work.json` → `prepended`, so older saved places move forward once.
- **One caupāī per item** in the Mānas: where Gita Press prints two or three as one, they are separate items; the joint meaning sits under the last part.
- **Pages follow the book's own sections, never topics.** A topic starting mid-section shows its heading inside the page, before its verse. Chaupāīs belong to the dohā that follows them ("Dohā 2" = the chaupāīs before dohā 2 and dohā 2).
- **Opening verses are named by type and number** ("Śloka 1–7", "Sorathā 5"), never "Dohā 0" or "Invocation".
- **A work declares its own verse types** in `work.json` → `types` (name and short tag); the app knows the Mānas's (चौपाई, दोहा, सोरठा, छंद, श्लोक).
- **How verses are written: one standard for every work**, applied by `tools/text/standard.py` when an exporter writes (`jsonio.dump_library`), and checked by the build (a verse or transliteration that differs fails it). A source file keeps its printed form; the published text follows the standard:
  - **॥ is one character** (U+0965), never two daṇḍas, in verses and meanings alike. **Verse numbers are compact** (`॥१॥`) so they never wrap away from the line; Devanagari digits in Hindi, Latin in English. Marks like आ॰ / ध्रु॰ use the abbreviation sign ॰ (U+0970), never a zero.
  - **Sanskrit follows Pāṇini** (the owner): ॐ for the sacred syllable (the pluta ओ३म् stays as printed); inside a word, a nasal before a stop is written as that stop's own nasal letter (सङ्कल्प, पञ्च, दण्ड, अन्त, कम्प), never the dot; a word-final m is म् at a pause (before । or ॥) and before a vowel, ं only before a consonant; the avagraha ऽ marks an elided a (it cannot be added by rule: `avagraha_candidates` lists places to check by eye against the source).
  - **ꣳ in the Yajurveda's texts** (shelf path under `veda/yajurveda/`): the anusvāra before श ष स ह र is ꣳ, as the Yajurveda recites it; elsewhere it is ं.
  - **The transliteration is ISO 15919**, made from the verse, never typed: r̥ is ऋ and ṛ is ड़; ṁ anusvāra, m̐ candrabindu, ḥ visarga, ’ avagraha, gͫ ꣳ; Vedic accents on their vowel (◌̍ udātta, ◌̠ anudātta, ◌̎ double svarita). A daṇḍa is ",", a line ending in ॥ ends with ".", a number is ` ॥N॥`. Gurmukhi is transliterated the same way, letter for letter (each letter is its Devanagari twin; tippi and bindi ṁ, addak doubles the consonant, ੴ ik oaṅkār). An i or u vowel after an a is ï ü (गउ gaü), never to be read as ai, au.
  - **Words are looked up by their spelling folded** (`fold`: class nasal, ꣳ and final म् as ं), so the dictionaries need one entry for गङ्गा and गंगा; the app's `fold()` is the same rule (the smoke test compares them).
- **Every verse has a language** (`l` on the item, else the work's `lang`), and every language is in `library/glossary/languages.json`. A text in a new language brings its own language and dictionary (Braj: `bra`), never a near language's.
- **Vedic accents** (svaras) are kept in the text; the app strips them only when looking a word up.
- **Each āratī is its own work**, on its deity's shelf (`hinduism/aarti/<deity>/<work>`), even when several come from one page. **The refrain (टेक) is shown once**; the "॥ ॐ जय शिव… ॥" cues after each stanza and the closing repeat are left out.
- **A popular part of a big work can be a work of its own** (the Sundarakāṇḍa beside the Mānas): it is generated from the big work and never written into it; its own additions (opening prayers, Chālīsā, āratī) come from its own `text.txt`.
- **The verses follow the order of the owner's recording** (the owner: "re-order the verses to suit the recording"): where it sings them in another order than the source, the text takes the recording's order and `reconciliation.md` says so. A verse of the source that the recording leaves out stays in the text, untimed.
- **A recording's opening that is not in the book is added as text too, and timed**, so the reader sees what is being sung (the Sundarakāṇḍa's opening prayers).
- **The closing verse is "समापन (पुष्पिका)" / "Closing words (iti)"**, not "colophon".

## 4. Meanings
- **Our own meanings, everywhere.** Where a meaning source is someone else's copyright, we write our own Hindi and English (and Punjabi for Gurbani) **from the original verse, never by rewording a translation**. They are sources `hi-scriptures`, `en-scriptures`, `pa-scriptures`, titled "भावार्थ — शास्त्र" / "Hindi meaning — Scriptures" (and the matching English and Punjabi titles); the app never mentions AI.
- **Which source a reader sees first** is the source's `order`. Ours is first in every work except the Rāmacaritamānasa, where Gita Press stays first until the owner says otherwise. Other sources stay selectable under ☰ › More settings › Sources.
- **For Sanskrit texts, our meanings are concise and grounded in tradition:** one to three sentences per verse, following the traditional reading (Śaṅkara for the Upaniṣads, Sāyaṇa for Vedic hymns), other readings briefly in a footnote. The owner: "Use your own intelligence… Don't copy word for word… Bring the context of Hinduism."
- **Line by line.** The owner: "whatever our line in the verse, its meaning below it wherever present." Our meanings are stored one piece per verse line (`p`); a line whose sense cannot stand alone gives its piece to the next line. Sources without pieces show the whole meaning after the verse. Each line sits on its own meaning as one pair, with no ॰ between them; a short faint saffron dash parts one pair from the next, so the full-width rule under the verse is the only long line and clearly ends it, as in a verse with its meaning whole.
- **The verse number ends the meaning**, added by the exporter from the verse (`tools/meanings/versenum.py`), never typed into a meaning file.
- **Copying is checked:** no run of 10 or more words shared with a copyrighted meaning; runs of 6–9 are read (`tools/meanings/overlap.py`). A same-language meaning (our Punjabi beside a Punjabi commentary) also gets a side-by-side copy audit, because the checker misses a sentence-by-sentence paraphrase.
- **A doubt of reading** goes in `docs/reviews/<work>-doubts.jsonl` for the owner; the meaning gives the plain reading. Before following Gita Press on a doubt, check Monier-Williams or Apte, the grammar, and an independent translation (Growse): most web meanings copy Gita Press.
- **A publisher's meaning that we show is kept as printed:** only extraction breaks and plain typos are fixed.
- **Style** (names, epithets, recurring terms, honorifics, Hindi joined postpositions, English with IAST names): `tools/meanings/style.md`.
- **Headings (topics):** our own wording where a work shows our meanings by default (the Sundarakāṇḍa: `tools/works/manas/topics.json`); the Mānas keeps Gita Press's while Gita Press is its default. A heading or meaning the owner has already approved (the Sundarakāṇḍa and its Kiṣkindhā lead-in) is changed only to fix an error or a copy; a new batch never rewrites it for taste.
- **The Mānas, kāṇḍa by kāṇḍa:** batches of about 50 verses (`prepare.py`) go to a writer, then an independent reviewer, then a separate copy auditor who reads every line beside Gita Press and rewrites any sentence that follows theirs with words swapped; the auditor's rewrite wins over the reviewer's fix. Then `apply_batches.py`, a consistency pass over the kāṇḍa (names, speech openings, refrains, headings) and the word issues into the dictionary; one branch and pull request per kāṇḍa; doubts in `docs/reviews/<date>-manas-<kāṇḍa>-doubts.jsonl`.

## 5. Word meanings
- **They are for learning:** "these are the tiny steps someone is taking to learn Sanskrit… we cannot afford mistakes." Every word of every verse has a meaning; meaning, root (`r`), grammar (`g`) and parts (`p`) agree.
- **One dictionary per language** (`library/glossary/<lang>.json`), never merged: the same spelling means different things in different languages (या, परे, ते, करि, हर). Lookups follow the language's fallback chain.
- **A word with several senses lists them all** ("जाओ / जिसे, जिसके"); the verse's meaning uses only the one its context needs. A sense that fits only one work goes in that work's own `glossary.json`.
- **`library/glossary/*.json` are the master copies:** exporters only add new words, never overwrite. A correction is made there directly, with the reason in the commit message.
- **Checked in trusted dictionaries** (`tools/meanings/style.md` §11): Monier-Williams and Apte for Sanskrit; Platts first for Awadhi and Braj; the Hindī Śabdasāgara; McGregor read on its page images (its OCR is unreliable); Mahan Kosh for Punjabi.
- Open questions about words are in `docs/reviews/dictionary-doubts.jsonl`.

## 6. The library
- **One website** (https://scriptures.craadle.org, published from `main`), installable on the phone; no ads, ever.
- **A shelf hierarchy, tradition first:** `<tradition>/<genre>/<group…>/<work>` (`hinduism/granth/tulsidas/ramcharitmanas`, `hinduism/stotra/rama/ramraksha`, `hinduism/veda/yajurveda/krishna-yajurveda/upanishad/katha-upanishad`, `sikhism/gurbani/guru-arjan-dev/sukhmani-sahib`). Reuse levels; think of the whole future library when adding one. A work's id is permanent; its place on the shelf may change.
- **Every work gets the same experience:** its natural divisions, plans, bookmarks, notes, progress, search, audio and sources.
- **A work's home:** "Continue ›" beside "▶ Play all" on one line; then its parts (or, for a single-part work, its sections) and its plans, each with ▶. A work without plans shows no plan switch. Tapping a part opens it directly.
- **Plans** (30-day Māsa-pārāyaṇa, 9-day Navāhna): a day opens at its **start**; "Continue" is the separate way back to where you were. Before the first day and after the last, a plan lists what is read then (`before` / `after` in `work.json`): the Mānas shows "Pārāyaṇa vidhi", the days, "Śrī Rāmāyaṇajī kī Āratī" and "Kathā-visarjana". The part list does not show them. Each day says how long it takes to hear ("≈ 1 h 22 min"), and so does the button to the next day at a day's end, so a reader can choose by the time they have: from the recording chosen, at the speed set, from the start of its first verse to the end of its last, pauses included.
- **The Pārāyaṇa vidhi** is one structured page of steps (Āvāhana → Pradhāna pūjā → Viniyoga → Ācamana and Prāṇāyāma → Karanyāsa → Aṅganyāsa → Dhyāna), each mantra on a card with its meaning; beginner guidance (what it means, what to do) is in its own boxes; every word on a vidhi page has a word meaning.
- **Text and meanings are separate:** the verse is the core; Hindi, English and Punjabi meanings and audio are selectable sources; word meanings are fixed and shared.
- **On the library page, each shelf shows two works**, the ones used most recently on this phone first, then "+N".
- **Under a work's title: the author, and the parent text where there is one** (`work.json` → `by`, `from`) — never the publisher.
- **The greeting** (॥ जय श्रीराम ॥, ੴ …, `salute` in `library/index.json`) shows only when a work is opened from the library or the tour, for at least 1.5 s; never on start, refresh or Back.
- **A new reader starts in English** (interface and English meaning).
- **Personal data stays on the phone** (localStorage `manas.personal.v1`): one reader per device; "Save my file" / "Open a file" on Bookmarks & notes.

## 7. The app
**Consistency**
- **One word for one thing**, in every label, toast, tour step and help line: verse / पद (never "text" for a verse); work / ग्रन्थ; meaning / अर्थ (never "translation"); note, bookmark, file, recording, section, library, shelf; play / सुनें (never "listen" or "hear"); letters / अक्षर (only for size); Audio timing / ऑडियोका समय. A new thing gets one word, added here.
- **Each setting has one place**, and the same control looks the same everywhere.
- **One interface language at a time**, headings, labels and numbers included.

**Header and menus**
- **One header on every page.** Left: the way back only (breadcrumbs on the library, shortened to one row; "‹ Library" on a work; ‹ in the reader). Right: A− / A+, the language or meaning capsule, search, ☰.
- **Language and meaning are one choice.** On the library and work pages, हिं · En sets the interface and the meaning together. In the reader the capsule holds the meaning switches, शब्द (word meanings) and 📖 (recitation mode); turning English on makes the interface English, only Hindi makes it Hindi. A work with a third meaning language (ਪੰ) shows two of them in the capsule, chosen under More › Sources.
- **Recitation mode (📖)** hides every meaning and remembers which were on; turning a meaning on ends it.
- **One ☰ sheet everywhere:** Bookmarks & notes (in a work), Dark theme (on = dark), Share the app (the owner: one short line and one link, `<site>/get`, through the phone's share sheet; `/get` sends an Android phone to the store app, `library/apps.json` → `store`, anything else to the website; chat apps show a card: the name, the library's contents in Hindi then English, and the wide picture `tools/store/icons/share-card.png` made by `make_icons.py`), Take the tour, More settings (the owner's name for it; और सेटिंग). **More settings** holds the rare things: Transliteration, Sources, Audio timing, Privacy. While Audio timing is on, its switch and "Clear adjustments" also show at the top of ☰. Nothing in ☰ repeats the header.
- **The ⋮ menu of a verse:** Play from here · Write a note · Copy verse and meaning · Improve verse or meaning. Items are short commands without "the".

**Reader**
- **Reading comes first:** simple, clear, nothing pulls attention from the verse. Light theme by default.
- **The verse** is bold and centred; its meanings are centred under it, full width; with Hindi and English both on, English is lighter. Word meanings under a verse stay left-aligned. Footnotes are content and sit under their verse.
- **The verse type is a heading** ("॥ चौपाई ॥", in saffron) where the type changes, never a corner tag.
- **The verse's corners never touch its words:** ▶ (saffron, filled) top left; bookmark (blue, filled saffron once set) top right; ⋮ (blue) bottom right; ↶ (saffron, timing mode only) bottom left.
- **Continuous scrolling** through a part or a day; at the end, one button to the next.
- **The lit verse's highlight** never crosses the previous verse's rule.
- **The footer shows where you are:** the verse range ("Dohā 29–30 ▾") and the part or day. A tap opens the section picker: tapping a part or day at the top only lists its sections; nothing opens until a section is tapped.
- **Nothing is wider than the screen**, even with the phone's text zoom; headings and the transliteration grow with A− / A+.
- **Vedic accents must be unmistakable:** a verse with svaras is set in Tiro Devanagari Sanskrit.

**Playing**
- **▶ on every part, every plan day and every verse;** "Play all" on a work's home. Playing is hands-free: the verse being recited stays at the top, the page follows it, meanings follow the switches, the screen stays on. A verse taller than the screen is followed inside too: when the line being recited (guessed from the time spent in the verse, shared among its lines by length) runs under the player, it comes up just below the bar, with its meaning when line by line — once for each line, so the reader can still scroll back by hand.
- **Playing ends where its button says:** ▶ on a part or day, and "Play from here", end with what is open ("<part> finished" and "▶ Play on"); "Play all" ends with "Recitation complete". The end message names no deity.
- **A touch or scroll never pauses the following;** when the lit verse is off screen, a pill "↑ Go to <verse>" brings it back.
- **The playing speed** (0.5–2×, YouTube's own) is a button in the player bar; ✕ is alone in its top-right corner.
- **The player never shows a recording's own title:** it shows the verse and the reading, then the reciter.

**Tour and navigation**
- **The tour is done, not read:** a welcome card, then the reader is taken into the Sundarakāṇḍa and asked to do each thing for real, with that spot lit (open the text, tap a word, drag the drawer down, A+, A−, switch a meaning, recitation mode, a bookmark, ▶). Every step after the first has "‹ Back"; "Skip" at every step; after ▶ plays 5 s, the library opens with "Tour complete — we hope you enjoy the app!". It is in every ☰ as "Take the tour".
- **Back retraces exactly, and a refresh stays on the same page** (every page and shelf is a browser-history entry). "‹ Library" opens the library itself.
- **Drawers close by dragging them down.** Buttons on a page stand 10 px apart.
- **Bookmarks & notes** lists fold under their headings (the fold is remembered); each bookmark has its own ✕.
- **Search forgives spelling** (the owner: one should not have to try a few spellings). The text and what is typed are folded to one sound key: in Devanagari (and Gurmukhi, read as Devanagari, so Hindi letters find the Sukhmani Sahib) ि/ी, ु/ू, ब/व, श/ष/स, ण/न, ृ/रि, ै/अइ, ौ/अउ, a nasal before a consonant, ँ ं ़ ् and Vedic accents count as one; in Roman letters long vowels, aspiration, sh/s, ch/c, v/w/b, f/p, z/j, a nasal before a consonant and a word's final a; in both, a word's final u (तनु धनु धामु, काजु). A verse is found by what was typed with spaces ignored and about one letter in six allowed to differ (Tulsīdās's ऐसेउ for "aise", काजु for काज), or by most of its words in any order; the closest comes first, then meanings, then the looser matches. A Roman-letter search shows the verse itself.
- **Offline:** a work opened once is readable offline with its meanings; library files are fetched fresh when online (2.5 s wait) and from the phone's copy when not.

## 8. Audio
- **Recordings play from YouTube;** the library stores only verse times. The player stays visible at YouTube's minimum (200×200): no hidden audio, it breaks YouTube's terms.
- **The pipeline:** the owner's audio file → a speech-quality copy in `scriptures-data` → `source.json` + `recordings.json` → transcription (the `transcribe` workflow of scriptures-data, or `tools/audio/transcribe_onnx.py` with the Whisper model from GitHub) → `tools/audio/make_timings.py`. Steps: `docs/HOW-TO.md`.
- **A verse the recording does not sing gets no time:** no start is guessed for it (`source.json` → `"fill": 0` when every other verse is heard), so the light stays on the verse being sung.
- **Check the timings against the transcript before publishing:** the first and last verse of each recording, and boundaries inside long breaths. In āratīs the alignment often matches the refrain to a later repeat. A hand-checked start goes in `fixes.json` with its evidence in `fixes.md`.
- **A recording that stops before the text ends** (a jaikāra after the last verse) gets `from` / `to` in `recordings.json` and `"align": "anchors"`.
- **The highlight must never sit on words that are not being sung:** a recording of another version is a draft until the owner chooses the text; a recording of a different composition is not timed to our text.
- **Timing by ear** (☰ › More settings › Audio timing): off by default and off again 12 hours after last use; never carried by a personal file. Under each verse: "− ⏱ Starts now +   − ⏹ Ends now +", the times and whose they are, "Until next" once an end is set; ↶ Undo in the verse's corner; the step (0.1 / 0.25 / 0.5 / 1 s) is a saffron chip in the player bar, and beside it the filled saffron "Next ▸ N", both on their own line under ✕ (the owner: ✕ one line up, so they never cover the video); on a phone under 390 px, where ⏮ ▶ ⏭ 1× do not fit beside the 200-px video, 1× moves up beside ✕ (wider phones keep it after ⏭) (the owner: one tap to the next verse still to check, after the one playing, round to the first, and it plays it; hidden when none is left). You mark the verse you look at, never the lit one; a mark never scrolls the page.
- **The light waits for you:** it never moves to a verse whose start is only a guess; a set end moves it to the next verse at once. "Ends now" gives the next unset verse that end as its start. Each − / + previews 2 s while nothing is playing.
- **One order rule, in one place:** `tools/audio/order.py` and `buildAudio` in `app.js` are the same rule, so what the phone shows is what will be published; the UX test proves they agree on every recording.
- **Sending:** "Send to the library" opens a GitHub issue; the `timing` workflow (issues from the owner's accounts only: `goyaldarwin`, `darwingoyal`) applies it and fails if any other verse would change. Owner times win over everything. A live recording takes each send at once; a draft goes live with the "checked: publish it for everyone" switch.
- **A recording covers every verse timed on it:** its `first`..`last` in the timings includes the verses the owner set after its last matched one (`make_timings.py`, the app, and a build check), so at a recording's end the player never goes back to a verse on the same recording (a loop).
- **Helpers** save their marks as a file; the owner opens it and checks each mark before it is sent.
- **Verifying a send:** compare the issue's JSON with `library/<path>/audio/<source>.json` (each sent time exact), read `moved`, and check the deploy run succeeded.

## 9. Apps and store
- **One app per tradition** (the Hindu app also shows the Sukhmani Sahib), published by the owner's corporation, in every country except mainland China; Android first, iPhone when the owner asks. The app shows the website, so content never waits for an app update. Details: `docs/APPS.md`.
- **Store pictures come from the real app** (`tools/store/screenshots.py`): a light, warm background, and only verses whose meanings are our own.
- Support email: support@craadle.org.

## 10. Engineering
- **One repository holds everything** for the website: the data, every script and expensive intermediate (transcripts, extracted text), and the docs, so a new session can continue. Shared code in `tools/site`, `tools/audio`, `tools/meanings`, `tools/works/export.py`; generated files are never edited by hand.
- **One folder per work, one format** (`tools/works/README.md`): `tools/works/<work id>/` holds `work.json`, `text.txt`, `README.md`, `reconciliation.md`, `meanings/<lang>/<source>.json` (any number of sources per language), `audio/<source>/` (any number of recordings), the work's own word senses in `glossary/<lang>.json`, and the scripts that make its text in `source/`. One exporter makes every work; a work that repeats another's verses takes them by id (`[take <work> …]`), never by copy. When a work needs something the format lacks, the format grows for every work (the exporter and `tools/works/README.md` together), not a script of its own.
- **Shared code goes first, on its own pull request;** check `docs/LIBRARY.md` and the app for an existing feature before writing one.
- **`build.py` refuses an inconsistent library** and an `app.js` that does not parse. Before every commit: build, `regen_check.py` (library/ equals what `tools/works/export.py` and `make_timings.py` make, in an empty folder), `history_check.py` (no work or verse id that readers' data points at has gone), `smoke_test.py`, `ux_test.py`; gate on their exit codes, never on a grep of their output. After merging, check that the `check` run on `main` is green (failed checks are annotations: `gh api repos/goyaldarwin/scriptures/check-runs/<job id>/annotations`).
- **A test that touches the player starts from a quiet player** (`stopAudio(); ytOK = false`). On the CI runner YouTube loads for real and moves the lit verse at any moment, so a test that taps a player button pins the verse as the tap begins and reads the result right after the app's handler (click listeners, removed afterwards), never after a wait. Tests that sample live data exclude verses set by ear; the timing tests clear the published marks in memory first, so they never depend on how far the owner has marked a recording.
- **Everything that broke gets a test** in the same change as its fix: a button is tapped the way a finger does (Playwright's `click`, which refuses a hidden or covered element), not called from code.
- **Releases must not break phones with the old version cached:** asset URLs carry a content hash; the service worker revalidates; think of readers on the previous release when moving a data file.
- **The page is never machine-translated** (the owner: no "Translate this page?" bar): `translate="no"` on `<html>` and `<meta name="google" content="notranslate">`; the app has its own Hindi and English.
- **An element id is used once** in the page: `$('#id')` binds the first, so a second element with the same id takes the first one's tap away (`ux_test.py` checks it).
- **A handler that calls a function with optional arguments is wrapped** (`() => f()`), so the click event is never passed as an argument.
- **A scripted docs edit asserts its anchor first:** `str.replace` silently does nothing when the anchor is missing.
- **Merging:** large work (a new work, a shared-code change) on a branch and pull request, merged by the session once the tests pass; a small fix the owner asks for may go to `main` after the same tests. Always `git pull` first: the `timing` workflow pushes to `main`.
- **GitHub Actions minutes:** jobs in the public repo are free; jobs in the private `scriptures-data` (transcription, experiments) use the owner's 2,000 included minutes a month, and more is billed. Before a private-repo run, estimate its minutes (jobs × hours each); ask the owner first when it is large (the whole-Mānas MMS run took about 2,350).
- **This environment:** never `pkill -f` or `kill $(pgrep -f …)` (they kill the session's own shell; kill by PID). GitHub GraphQL is unavailable; use the REST API (`gh api …`). Hugging Face is blocked; the Whisper model comes from GitHub (`tools/audio/transcribe_onnx.py`). Tesseract `hin`/`mar`/`san` install with apt.

## 11. Extraction techniques
- **Gita Press Hindi PDFs** have a broken text layer: decode from glyph ids (PyMuPDF `get_texttrace()`) with a glyph → Unicode map (pre-base ि, reph combinations, conjuncts, nukta forms, empty placeholder glyphs; after a halant a zero-advance space means ZWNJ, between consonants a missing ्). Cross-check with Tesseract `hin` OCR of the page images (agreement well above 95%; every disagreement read by eye).
- **Gita Press English PDFs** mix fonts: Devanagari in a legacy 8-bit font (Chanakya/Kruti style), transliteration in a custom encoding (å=ā, ∂=ī …). Convert, then check by turning the transliteration back into Devanagari and diffing.
- **Footnotes run across pages** (one starting lowercase continues the previous) and restart their marks per page: match notes to marks in order. A note is one paragraph: its printed lines are joined (a new note starts with its mark); a line-end hyphen stays in a hyphenated word (forty-eight) and goes where the printer split a word (expand-ing), each such hyphen decided by hand (`tools/works/manas/source/make.py`).
- **Web-page printouts** often have a broken Devanagari text layer: OCR the page images, or read the text layer by position (`pdftotext -bbox`) where an overlay hides lines.
- **A book whose Devanagari is in a legacy font** can still be the source through its IAST layer, converted letter for letter and checked against another witness.
- **A śānti mantra printed again at the end of an Upaniṣad is not an item:** the work ends with its last verse (the Kaṭha ends with 2.3.18).
- **A video's on-screen text** can be the source when the owner says so: crop the subtitle band at full width, transcribe line by line with the frame number; repeated screenshots of a line are one line. Where the video's Devanagari and its transliteration disagree, follow the correct one.
