# The library: format reference

Step-by-step procedures are in `docs/HOW-TO.md`. This page defines the files the website reads. A work's files are made from its folder, `tools/works/<work id>/`, whose format is in `tools/works/README.md`; only the shelf (`index.json`), `removed.json`, `apps.json` and the dictionaries (`glossary/`) are edited here.

All scriptures live under `library/` as JSON. The website reads only these files, so a new work needs no change to the app code if it follows this format. Every visible label carries both languages: `{"hi": "…", "en": "…"}`.

## 1. The shelf: `library/index.json` — a REST-like hierarchy

Every work has an address, read from the general to the specific like a REST path:

```
<tradition> / <genre> / <group> [/ <group> …] / <work>
```

| Level | What it is | Ids in use or planned |
|---|---|---|
| tradition | the faith | `hinduism` (हिन्दू धर्म), `sikhism` (सिख धर्म); later `jain`, `bauddh` … |
| genre | the kind of text, as a reader looks for it | Hindu: `granth` (epics, scriptures), `stotra`, `aarti`, `chalisa`, `bhajan`, `veda`, `purana` … · Sikh: `gurbani` … |
| group(s) | whatever groups works naturally inside that genre (one or more levels) | `granth`: the author (`tulsidas`, `valmiki`, `vyasa`) · `stotra`, `aarti`, `chalisa`: the deity or saint (`rama`, `hanuman`, `vishnu`, `shiva`, `ganga`, `shirdi-sai`) · `veda`: the Veda, its śākhā where there are two (`yajurveda/krishna-yajurveda`, `yajurveda/shukla-yajurveda`), then the division `samhita` / `brahmana` / `aranyaka` / `upanishad` · `gurbani`: the Guru (`guru-arjan-dev`, `guru-nanak-dev`) |
| work | the text you open | `ramcharitmanas`, `ramraksha`, `dhoop-aarti`, `katha-upanishad`, `sukhmani-sahib` |

Examples:

```
hinduism/granth/tulsidas/ramcharitmanas
hinduism/stotra/rama/ramraksha
hinduism/aarti/shirdi-sai/dhoop-aarti
hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram
hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad
hinduism/veda/atharvaveda/upanishad/mandukya-upanishad
sikhism/gurbani/guru-arjan-dev/sukhmani-sahib
hinduism/veda/samaveda/upanishad/kena          (planned)
sikhism/gurbani/guru-nanak-dev/japji-sahib     (planned)
```

Rules (`tools/site/build.py` checks them):
- **The path is the chain of ids.** A work's `path` must be exactly the ids of the shelves above it, followed by its own id, and the files live in `library/<path>/`. The library screen shows two levels at a time: a shelf's sub-shelves as headings, with their contents listed under them.
- **At least three levels** (tradition / genre / work). Add a group level when the genre will hold works of more than one author or deity, which is almost always.
- **Ids** are lowercase ASCII with hyphens, in common romanised spelling without diacritics (`ramraksha`, `shirdi-sai`, `hanuman-chalisa`). Titles carry the proper Devanagari and diacritics.
- **Before adding a level, reuse an existing one.** Look at `index.json` first: a new Hanumān stotra goes under `hinduism/stotra/hanuman/`, not a new `hanumaan/`. A new genre or tradition is a deliberate decision; say so in the pull request.
- **Every shelf has a bilingual `title`**, plus an optional `desc` (one line, shown under it).

The work node itself:
```json
{"id": "ramcharitmanas", "work": "manas", "path": "hinduism/granth/tulsidas/ramcharitmanas",
 "title": {…}, "by": {…}, "edition": {…}, "desc": {…}, "salute": "॥ जय श्रीराम ॥"}
```
- `work` is the work's **permanent id**. Readers' bookmarks, notes, progress and choices are stored under it, so it never changes, even if the work moves on the shelf. It must be unique across the library. For a new work, use the same value as its shelf `id` unless that is already taken. The tools folder is `tools/works/<work id>/`.
- `by`, `edition` (optional, bilingual): shown in the library and searched.
- `salute` (optional): the salutation on the opening screen while the work loads. Without it the app shows ॥ ॐ श्री परमात्मने नमः ॥.
- Moving a work to another shelf is safe: change `path`, move the folder, and nothing readers saved is lost.

**The private sources** (books, printouts, recordings) of a work are in `goyaldarwin/scriptures-data` at the same `<path>`, under `<kind>/<source-id>/`, with metadata per file.

## 2. A work: `library/<path>/work.json`

| Field | Meaning |
|---|---|
| `id` | same as `work` in the shelf |
| `lang` | the language most of its verses are in (a code from `glossary/languages.json`, e.g. `awa`) |
| `title`, `by`, `edition`, `colophon` | bilingual labels. `edition` names the edition or source (found by the library search; not shown under the title) |
| `from` | optional, bilingual: the parent text or context, shown under the title after the author (`by · from`), e.g. the Sundarakāṇḍa's “Śrī Rāmacaritamānasa”, the Sukhmani Sahib's “Sri Guru Granth Sahib, Ang 262–296”. Never a publisher. |
| `parts` | the top division: `{"name": {"hi":"काण्ड","en":"Kāṇḍa"}, "list": [{"hi":…,"en":…}, …]}` |
| `items` | every verse, in reading order (below) |
| `topics` | section headings: `[{"id": <first item id>, "hi": …, "en": …}]` |
| `plans` | reading plans: `[{"id":"M","name":…,"long":…,"unit":…,"before":["vidhi"],"after":["aarti"],"n":30,"end":[<last item id of each day>]}]`. `before` / `after` (optional; the pūrvāṅga and uttarāṅga) name pages listed before the first day and after the last: `vidhi` (the procedure in `vidhi.hi/en`), `aarti` (`vidhi.aarti`) and `visarjan` (`vidhi.visarjan`: `{title, when, verses: [{v: [lines], hi, en}]}`, recited at the end of a pārāyaṇa). `build.py` refuses a page the work lacks. |
| `types` | optional: the work's own verse types, `{"viniyoga": {"name": {hi,en}, "short": {hi,en}}}`. `name` is the full label (headers, search, ranges), `short` the tag at the left of the verse's first line. They add to or replace the built-in Mānas types (`cau`, `do`, `so`, `cha`, `shloka`) while the work is open. |
| `renamed`, `split` | optional: `renamed` maps an old item id to its new one. In the Mānas, the 16 joint caupāīs Gita Press prints as one (`bal.6.cau3-5`) are one item per caupāī (`bal.6.cau3`, `cau4`, `cau5`), and each old id maps to the first part. The app moves readers' notes, bookmarks, timing marks and place on an old id to the new one (a meaning correction goes to the last part, where the joint Gita Press meaning is); `make_timings.py` reads old ids in its caches the same way. `split`: `[position, items added]` pairs, used to move a place saved as a position only (no id). |
| `removed` | optional: ids of verses taken out on purpose (the Kaṭha's closing śānti `shanti.2`); an id is never used again. `tools/site/history_check.py` fails when a verse id of the previous version is gone and is neither here nor in `renamed`; a work gone from the shelf must be in `library/removed.json` → `works`. |
| `prepended` | optional: the number of opening verses that a place saved as a position only (no id) does not count. The app moves such a place forward by this many, once (`fixLast` in `tools/site/app.js`). The Sundarakāṇḍa has `5` (its opening prayers). Places, bookmarks, notes and audio times kept by id never need this. |
| `vidhi`, `vg` | optional: recitation procedure (pārāyaṇa vidhi) and its word meanings |
| `glossary` | **generated**: `true` when the work has its own `glossary.json` (§5) |
| `sources` | **generated by `tools/site/build.py`**, never edited: the meaning and audio sources found in the work's `meanings/` and `audio/` folders, `{"hi":[…], "en":[…], "au":[…]}`, plus a list for any other meaning language the work has (`"pa"`). |

An item: `{"id": "bal.86.cau4", "p": 0, "s": "86", "y": "cau", "n": "4", "v": [verse lines, in the work's script], "t": [transliteration lines]}`
- `l` (only when it differs from the work's `lang`): the verse's language. In the Mānas, `sa` marks the ślokas and the Sanskrit stutis; every other verse is `awa`.
- `p`: index into `parts.list`. `s`: the section (book page heading, e.g. the dohā number the item belongs to). `y`: type (`shloka`, `cau`, `do`, `so`, `cha`, or one of the work's `types`). A numeric `s` is shown as “Dohā N” (the Mānas); other works use non-numeric sections (e.g. `sh4`), which are labelled by their verses. `n`: the number printed in the book.
- `v` (the verse) and its number are the core of the work. Meanings are never stored here.
- `v` and `t` are written by the standard (`docs/PLAYBOOK.md` §3, `tools/text/standard.py`): `t` is the ISO 15919 transliteration of `v` (Devanagari and Gurmukhi).

## 3. A meaning source: `library/<path>/meanings/<id>.json`

```json
{"id": "hi-gitapress", "lang": "hi", "order": 1,
 "title": {"hi": "गीताप्रेस — भावार्थ (हनुमानप्रसाद पोद्दार)", "en": "Gita Press — Hindi bhāvārtha (Hanumānprasād Poddār)"},
 "m": {"bal.0.shloka1": ["meaning text", ["footnote", "…"]]}}
```
- `id` = the file name. Name it `<lang>-<publisher or translator>`, lowercase with hyphens, e.g. `en-gitapress`, `hi-swami-ramsukhdas`.
- `lang` is a meaning language: one with a `meaning` block in `glossary/languages.json` (`hi`, `en` and `pa`; §5). Adding a meaning language is one entry there; the app needs no change. A work with a third meaning language shows two of them in the reader's header (by default ਪੰ · En in an English app, ਪੰ · हिं in a Hindi one; the reader chooses the pair in ☰ › More › Sources › "Meanings in the bar").
- `order` (optional): the lowest is the default for new readers. Without it, sources sort by id.
- `p` (optional): the meaning **line by line**, `{item id: [one piece per verse line]}`. The reader shows each piece under its line. A piece is `""` where a line has no meaning of its own (a heading line such as ਸਲੋਕੁ ॥), and at least one piece is not empty. The list has exactly as many pieces as the verse has lines, and the item also has its whole meaning in `m` (used for search, copy and a reader's own correction). A source without `p` is shown whole after the verse. `tools/site/library.py` checks it.
- `m` maps item ids to `[meaning, footnotes]`. The footnotes list is optional. A source may cover only some verses. A verse the reader's chosen source doesn't cover is filled in from the work's other sources of the same language, in `order`, with a small tag naming that source.

**Where meanings come from (the owner's rules; `docs/PLAYBOOK.md` §4):**
1. **A publisher's meaning is copied faithfully** from the source the owner gives (a book, a web page, a video's on-screen text). Fix only plain typos and broken text layers, and list the fixes in the work's `reconciliation.md`.
2. **Our own meanings** are written from the verse, never by rewording a translation (`tools/meanings/style.md`). They are separate sources named `<lang>-scriptures` (titled "भावार्थ — शास्त्र" / "Hindi meaning — Scriptures", and the matching English and Punjabi titles), so readers can tell them apart.
3. Name every other source after its publisher, translator or channel, and record its edition and permission status in the root `README.md` → "Sources and permissions".

## 4. An audio source: `library/<path>/audio/<id>.json`

```json
{"id": "kamlesh-upadhyay", "type": "youtube", "title": {"hi": "पं. कमलेश उपाध्याय “हरिपुरी”", "en": "Pt. Kamlesh Upadhyay “Haripuri”"},
 "tracks": [{"yt": "nieT_-RsShc", "dur": 9109.9, "first": "bal.0.shloka1", "last": "bal.55.do55"}],
 "at": {"bal.0.shloka1": [0, 42.12]}}
```
- `id` = the file name: the reciter's name, lowercase with hyphens.
- `title` is what readers see while it plays. The player never shows the YouTube video's own title; it shows the reading (kāṇḍa or plan day), the verse and this title.
- `tracks` are YouTube videos in reading order. `at` maps each item to `[track index, start second]`.
- `order` (optional): the lowest is the default recording. Without it, sources sort by id.
- This file is generated by `tools/audio/make_timings.py`. Do not edit it by hand. Its inputs live in `tools/works/<work>/audio/<id>/`: `source.json`, `recordings.json`, `transcripts/`, and optionally `owner.json`, `fixes.json` and `fixes.md`.
- `at` maps a verse id to `[track, start]` or `[track, start, end]` (seconds). The end is given only where it was set by ear (a refrain, kīrtan or music follows the verse); the app uses it only to stop: playing one verse, or at the last verse of a reading. Continuous playing ignores it.
- `"draft": "<reason>"` marks a recording whose timings are not checked yet: the app plays it only while ☰ › More › Audio timing is on.
- (in the source's `tools/works/<work>/audio/<id>/source.json` only) `"review": "<why>"`: published for everyone, while every start not yet set by ear stays in `check` for the owner to review in timing mode.
- `check` (starts only estimated, listed to be checked by ear), `guess` (starts only guessed by text length, re-guessed around the owner's times), `own` (verses with an owner time: used exactly as given, and the app treats them as set), `moved` (verses placed again by the order rule around the owner's times) and `raw` (`{verse: start}`: the start each moved verse had before the rule — the app applies the rule from it, so what it shows is what the next send publishes). The rule itself is `tools/audio/order.py`, the same as the app's `buildAudio`.
- More inputs: `owner.json` (`{video: {verse: seconds or [start, end]}}`) holds the times the owner set by ear in the app; they are used exactly as given and win over `fixes.json` and the automatic timing. It is written by `tools/audio/apply_owner_timing.py` from a "Timing:" GitHub issue (`.github/workflows/timing.yml`), never by hand.
- `fixes.json` = `{video id: {item id: seconds}}`: hand-checked starts for lines the speech recogniser missed. They win over the automatic match. Put the evidence for each fix (the transcript segment, or what is heard) in `fixes.md`.

## 5. Word meanings: `library/glossary/`

Each language has its own dictionary, because the same spelling can mean different things in different languages. For example, या is "who (fem.)" in Sanskrit but "this" in Awadhi, and परे is "in the other (world)" in Sanskrit but "fell" in Awadhi.

```
library/glossary/
  languages.json   every language used by any verse
  sa.json          Sanskrit
  awa.json         Awadhi
  mr.json Marathi · hi.json Hindi · bra.json Braj · pa.json Punjabi (Gurmukhi script; Gurbani)
```

`languages.json`:
```json
{"awa": {"name": {"hi": "अवधी", "en": "Awadhi"}, "script": "Deva", "fallback": ["sa"],
         "suffixes": ["हिं", "न्ह", "…"], "stems": ["", "ा", "ी", "ु"]},
 "pa":  {"name": {"hi": "पंजाबी (गुरमुखी)", "en": "Punjabi (Gurmukhi)"}, "script": "Guru", "fallback": [],
         "meaning": {"short": "ਪੰ", "name": {"hi": "पंजाबी", "en": "Punjabi", "pa": "ਪੰਜਾਬੀ"}, "order": 3}}}
```
The file lists every language of a verse, and every language a meaning is written in (`en` too, with script `Latn`).
- Codes are ISO 639: `sa`, `awa`, `hi`, `mr`, `pa`, `bra` … Script codes are ISO 15924: `Deva`, `Guru` …
- Scripts the site supports: Devanagari and Gurmukhi (fonts in `tools/fonts`, registered in `tools/site/build.py`; Gurmukhi digits ੦–੯ work like Devanagari ones). The audio matcher reads Gurmukhi by mapping it onto Devanagari (`tools/audio/align.py` → `gur2dev`). A new script needs a font and a key mapping first.
- `fallback`: where to look next when a word isn't in this language's dictionary. Awadhi borrows Sanskrit words, so `awa` → `sa`. Sanskrit has no fallback, so a Sanskrit verse never shows an Awadhi sense.
- `suffixes` / `stems`: how to find the root of an inflected word (रामहि → राम). These are per language, because each language inflects differently.
- `meaning` (optional): makes it a meaning language, one a meaning source can be written in (§3). `short` is its switch in the reader's header (हिं, En, ਪੰ), `name` its bilingual name (it may add its own, `pa`), `order` its place among the meaning layers.

Dictionary keys are written **without Vedic accent marks** (svara: U+0951–0954, U+1CD0–1CFF, U+A8E0–A8F1); the app removes them from a tapped word before looking it up, so a text keeps its svaras and still finds its meanings. Exporters must strip them the same way when they collect words.

A dictionary (`<lang>.json`): `{"राम": {"hi": "भगवान श्रीराम", "en": "Lord Rama", "g": "grammar", "r": "root", "p": [["part", "meaning"]]}}`. Every entry has `hi` or `en`. An entry may also carry `"pa"`, its Punjabi meaning: the app shows it in the word sheet, and in the word list while the ਪੰ layer is on. No entry has one yet.

**How a tapped word is looked up:**
1. The verse's language comes from the item's `l`, otherwise the work's `lang`.
2. For that language, then each fallback in turn, the app checks:
   - the reader's own meaning, saved on their device as `<lang>:<word>`;
   - the work's own sense, from `<work>/glossary.json` if it has one;
   - the shared dictionary for that language.
3. If nothing matches exactly, it tries the suffix rules of each language in the chain.
The word sheet shows which language's meaning it is showing.

**A work's own senses** (optional), `library/<path>/glossary.json`: `{"sa": {"word": {…}}, "awa": {…}}`, made from the work's `tools/works/<work>/glossary/<lang>.json`. Use it when a word means something particular in one work. Never use it for a general correction; that belongs in the shared dictionary.

**Maintenance:** the files in `glossary/` are the master copies, so correct a word there directly. A work's exporter files each new word by the language of the verses it occurs in, and only adds words that aren't there yet. A word that occurs in two languages is added to both, so check that each sense fits its language.

## Rules that keep it consistent
- Ids: lowercase letters, digits and hyphens. A work's `work` id and an item's `id` are permanent, because readers' bookmarks, notes and progress point at them.
- A source's file name is its `id`. `tools/site/build.py` refuses to build if they differ, if an item id is unknown, if a word of a verse has no meaning in its language or a fallback, if a timing is outside its recording, if a line-by-line meaning does not match the verse's lines, or if a plan's days are out of order.
- The verse text (`work.json`) never contains meanings, and a source never contains verse text.
- Every verse has a language, and every language has an entry in `languages.json`. A new language means a new dictionary file; never mix languages in one dictionary.
- Every label shown to readers is bilingual: `{"hi", "en"}`.
- Generated files (`index.html`, `app/`, `work.json` → `sources`/`glossary`, `audio/*.json`, and every file `tools/works/export.py` writes) are rebuilt, never edited. `tools/site/regen_check.py` fails on any hand edit.
- Files that many works add to are written **one entry per line, sorted** (`tools/jsonio.py`): `glossary/<lang>.json` and `index.json`. `build.py` re-writes them in that form, so two branches that add different words usually merge without conflict. If two branches add words that sort next to each other, git asks; keep both lines.
