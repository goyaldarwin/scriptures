# Lessons: mistakes made once, the rule each became, and what guards it

From the history of `scriptures` (`git log`: every "fix", "the owner:" and owner report) and the previous audit (`docs/reviews/chalisa-aarti-namavali-audit.md`). One line each: what went wrong · the rule (PLAYBOOK §) · the guard. "None" is a test still to write (`docs/SWEEP.md` §E).

| What went wrong | Rule | Guard |
|---|---|---|
| A jukebox song played and counted as the whole video (the Lakṣmī āratī) | §8 a jukebox track has `start`/`end` | `library.py` (every time inside the stretch); `ux_test.py` (player start, end, length) |
| A name spelled as a printout had it (सायि for साई), then the same name spelled three ways in one chālīsā (साईं, साई, साँईं) and शिरडी beside शिर्डी | §2 a name takes its standard spelling, one spelling everywhere | `library.py` with `tools/text/names.json` |
| A shared dictionary entry spoke of one work ("here held by Śrī Rāma", "इस पदके कवि") and opened so in other works | §5 a shared entry names the work a sense belongs to | `library.py` (`CONTEXT`) |
| A shared entry gave only the inflected reading its first work needed (बिभ्यति "she fears", wrong in the Rāmāyaṇa's सर्वे बिभ्यति) | §5 an inflected form lists every reading | none: a check needs a grammar; read by hand (sweep §A5) |
| A hand start taken from a transcript segment's start, 3–13 s early on music or the line before | §8 a hand start is read in 5-s windows, quoted in `fixes.md` | `library.py` (every verse of a `fixes.json` named by its id in its `fixes.md`); whether the windows were read right is checked by ear (sweep §A7) |
| A verse the recording does not sing was given a guessed time (the Santoṣī Chālīsā's opening dohā) | §8 an unsung verse gets no time (`fill`) | `ux_test.py` (the light never sits on an untimed verse); none for the data |
| MMS took an āratī stanza's repeat; a verse kept from the transcript was a line early | §8 such starts are checked in windows | none (by ear, sweep §A7) |
| A hand start set at a transcript segment's edge, inside the verse before (Rāma Rakṣā 3 and 38) or in the verse's second line (Vālmīki 55.28, 30.35); to-check lists edited by hand drifted from their generator | §8 a hand start is read in windows; MMS's stands where it agrees | `regen_check.py` (`aligned.json` and `check.json` are what `mms_merge.py` makes; `aligned.md` beside them); the windows are read by hand (sweep §A7) |
| The player label, Resume, search and the reader took a verse's number from different places | §3 one number per verse, `c` | `cite.py` self-test; `ux_test.py` (every number the player shows finds its verse, per work) |
| "Back to …" showed another work's place | §6 it belongs to the work open | `ux_test.py` |
| ✓ Correct appeared only on a helper's mark, never on a verse the library lists to check | §8 ✓ on every verse still to check | `ux_test.py` (timing tests) |
| A test tapped a player button after a wait while real YouTube moved the light (CI) | §10 pin the verse as the tap begins | `ux_test.py` itself |
| An app.js with a syntax error shipped and the reader would not start | §10 the build refuses an app.js that does not parse | `build.py` |
| Readers with the old release cached saw a broken app after a release | §10 asset URLs carry a content hash | `smoke_test.py` (previous release's app.js on a split work) |
| A second element with the same id took the first one's tap | §10 an id is used once | `ux_test.py` (every element id used once, app-wide and per work) |
| A long compound ran off a phone screen | §7 nothing wider than the screen | `ux_test.py` (horizontal overflow) |
| The browser offered to translate the page | §10 `translate="no"` | `ux_test.py` |
| An āratī verse kept its printouts' commas | §3 no comma in an āratī | `library.py` |
| A marked (IAST) English title confused readers | §6 plain Indian English in titles | `library.py` |
| A doubts file was left for the owner | §2 decide; doubts settled before merge | the `check` workflow (a `docs/reviews/*-doubts.jsonl` that holds a line fails it) |
| An agent's note or instruction written into data | §2 only a helper's fix goes into data | `library.py` (`DOUBT`: TODO, re-gloss, "(record …", placeholder, and doubt wording, in our meanings and every dictionary) |
| A plain word marked `hard` (परे, बन्द) or an underline opening another word's entry (परे → परा) | §5 | `hard_words.py report --reach` (run by hand), app `hardKey` = `hard_key` (smoke test); none in the build |
| A hard entry kept after its meaning respelled the word (`kankhal` for Kanakhala) or its work was removed (नाथकर, कोया, nāmadeva) | §5 the key is the word as our meaning spells it | `library.py` (`check_hard`: an entry no meaning word reaches and no verse has) |
| An underline opened the shared sense where one work means another (the Śiva Purāṇa's "five Brahmans" opened "Brahman, the one supreme reality") | §5 a work's own sense in its glossary | none: read by hand (`hard_words.py report --reach`, sweep §A5) |
| A name spelled three ways in one work's English (Sadyojāta, Sadyaojāta, Sadyajāta) | §2 one name, one spelling | `library.py` for the names in `tools/text/names.json` only |
| A recording's last verse looped back on the same recording | §8 a recording covers every verse timed on it | `library.py`, `make_timings.py` |
| A setting shown where it does nothing | §7 a setting only where it does something | `library.py` (`lines`, `notes`); `ux_test.py` (Meaning per line) |
| An empty timing file broke a UX check (Durgā Saptaśatī before its transcript) | §8 a recording waits for its transcript | `regen_check.py` |
| A regenerated file undid a hand edit | §3 change data in its generator | `regen_check.py` |
| A transcribe run of 232 ids never started (concurrency group name too long) | §10 | none (workflow) |
| Our English wrote ṁ (the transliteration's letter) in some works and ṃ in others, so a hard entry keyed one way left the other un-underlined (hrīṃ, Narasiṃha, Kaṃsa) | style §5 IAST: ṃ | `library.py` (ṁ in our English or `en.json`) |
| The sacred syllable written Om and Oṃ in the same uses | style §5: Om | `library.py` (Oṃ in our English) |
| A source copy's stray character kept in a verse (@नाम; the Mahābhārata e-book's ‘ and “(भवेत्”) | §2 correct a clear slip | `library.py` (a bracket or quotation mark that does not close in its verse; a verse not in its language's script); other stray characters: the Unicode scan (sweep §A2), by hand |
| A draft's gloss kept its doubt ("text uncertain", "prob. for …") in the data, and a meaning followed the doubt instead of the book (7.2.35.25 "beyond Sadāśiva" for not beyond) | §2 decide; fix, don't annotate | `library.py` (`DOUBT`: in our meanings, the shared dictionaries and every work's glossary) |
| A work's glossary file drifted from its generator (words.py reads scriptures-data, so regen_check cannot run it) | §3 change data in its generator | none |
