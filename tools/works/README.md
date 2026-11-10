# Works: one folder per work

Every work in the library has one folder here, named by its id (`tools/works/<id>/`; the id is permanent, `docs/LIBRARY.md`). One exporter makes the library from all of them:

```bash
python3 tools/works/export.py                  # every work, each after the works it takes verses from
python3 tools/works/export.py shiv-aarti       # one work (and the works it takes from)
python3 tools/audio/make_timings.py tools/works/<id>/audio/<source>   # a recording's timings
python3 tools/site/build.py
```

`tools/site/regen_check.py` makes the whole library again in an empty folder and fails on any difference, so nothing in `library/<path>/` is edited by hand.

## The folder

| File | What | Required |
|---|---|---|
| `work.json` | the manifest (below) | yes |
| `text.txt` | the verses (below) | yes |
| `README.md` | what the work is, where its text, meanings and recordings come from, its verse types | yes |
| `reconciliation.md` | the witnesses of the text and every choice made between them | yes |
| `meanings/<lang>/<source>.json` | one meaning source in one language (below) | |
| `commentary/<lang>/<source>.json` | one commentary, in the meaning format (below) | |
| `glossary/<lang>.json` | the work's own sense of a word whose shared entry (`library/glossary/<lang>.json`) carries another text's sense; for a big work loaded by part, also every word the shared dictionary lacks (loaded by part) | |
| `audio/<source>/` | one recording source (`tools/audio/README.md`) | |
| `topics.json` | our own topic headings `{first verse id: {hi, en}}`, for works that take this work's verses and show ours (`"topics": "ours"`) | |
| `source/` | the scripts and data that make `text.txt` (or a copied meaning) from the owner's sources, and their checks | |
| other `*.json` | data a `work.json` includes (`"include"`) | |

The build stops if a folder lacks a required file, or if a work on the shelf (`library/index.json`) has no folder.

Words go in the shared dictionaries, `library/glossary/<lang>.json`, edited directly; the build checks that every word of every verse has a meaning there (or in the work's `glossary/`).

## `work.json`

```json
{
 "id": "shiv-aarti",
 "path": "hinduism/aarti/shiva/shiv-aarti",
 "lang": "hi",
 "title": {"hi": "…", "en": "…"},
 "by": {"hi": "…", "en": "…"},
 "edition": {"hi": "…", "en": "…"},
 "parts": {"name": {"hi": "आरती", "en": "Āratī"}, "list": [{"key": "aarti", "hi": "…", "en": "…"}]},
 "types": {"tek": {"name": {"hi": "टेक", "en": "Refrain (ṭeka)"}, "short": {"hi": "टेक", "en": "Tek"}}}
}
```

- `id` equals the folder's name; `path` is the work's place on the shelf (`library/<path>/`); `lang` the language of its verses (an ISO 639 code in `library/glossary/languages.json`).
- `title`, `by`, `edition`, `from` (shown under the title), `colophon`: bilingual labels.
- `parts.list[].key`: the name `text.txt` uses for a part (`@part aarti`); it is not written to the library.
- `types`: the work's verse types; the Mānas's own (`cau`, `do`, `so`, `cha`, `shloka`) need no entry.
- `cite`: how a verse is cited, part › section › verse (`docs/LIBRARY.md` §2, `tools/text/cite.py`): declare it when a verse's own number restarts in each section or part (the Mānas by dohā, the Kaṭha adhyāya.vallī.mantra, the Śrī Rudram anuvāka.mantra, the Sukhmani Sahib ashtapadi.pauri); `n` in `text.txt` is always the verse's own number, as printed. Without it a verse is cited by its own number, and the build refuses two verses of one type cited alike in one part: give the sections names (`sections`) or declare `cite`.
- `load: "parts"`: a big work (the Vālmīki Rāmāyaṇa) is written for loading one part at a time: each meaning source as a header and `meanings/<lang>-<src>/<part index>.json`, and the work's own senses as `glossary/<part index>.json` (`docs/LIBRARY.md` §2, §3, §5). The phone fetches a part's meanings and word senses only when it opens that part. Use it when a work's meanings would make a phone fetch more than a few MB at once; the verses stay one `work.json`.
- `verses: "parts"` (with `load: "parts"`): a work whose verses alone are tens of MB (the Mahābhārata) has them by part too: `work.json` keeps every item without its lines (`"v": []`), and each part's lines and transliteration are `verses/<part index>.json` (`docs/LIBRARY.md` §2). The exporter writes them; every tool reads the work whole with `tools/jsonio.py` → `read_work`.
- `sections`: a label for each `@section` id, `{"bala.1": {"hi": "सर्ग १", "en": "Sarga 1"}}`, shown wherever the app names a section (footer, section picker, home, a verse's place). Every id must be a section of the text.
- `prepended`, `removed`, `renamed`, `split`: keep readers' saved places when verses are added before the first, removed or split (`docs/LIBRARY.md`).
- `include`: other files in the folder whose keys join the manifest (the Mānas's `book.json`: reading plans, vidhi).
- `topics: "ours"`: a run taken from another work shows that work's `topics.json` headings instead of its own.

Every other key is copied into `library/<path>/work.json` as it is.

## `text.txt`

```
# a comment
@part aarti                         the part the following verses belong to (a key of parts.list)
@section aarti                      the section (page) the following verses belong to
@lang sa                            the language of the following verses (until the next @lang)
@topic हिन्दी नाम | English name     a topic heading that starts at the next verse
[aarti.pad1 pad 1]                  a verse: id, type, number (the number is left out when it has none) …
पहली पंक्ति ।                        … and its lines, one per line
दूसरी पंक्ति ॥१॥
[take manas bal.17.so17]            a verse of another work, unchanged; it joins this part and section
[take sundarkand aarti.tek .. aarti.pad6]   a run of another work's verses, with their sections and topics
```

- A verse id is permanent: readers' bookmarks, notes and timings are stored by it.
- A taken verse keeps its id, lines, transliteration and language; its meanings come from the same source of the work it comes from (a meaning file with no `m`), and so can its recording (`audio/<source>/source.json` → `"take": "<work id>"`). A correction made in the source work reaches every work that takes from it at the next export.
- A run brings the topics inside it (and the topic it starts in); a `@topic` just before a run names the run's start instead.
- A text made by a script from a book or a page is written with `tools/works/textfile.py` (`write`), so it reads like a typed one, and says at its top which script makes it.

## `meanings/<lang>/<source>.json`

```json
{
"about": "where the meaning comes from (not shown)",
"title": {"hi": "…", "en": "…"},
"order": 1,
"numbers": "verse",
"m": {
"aarti.pad1": "the meaning",
"aarti.pad2": ["the first line's meaning", "the second line's meaning"]
},
"notes": {
"aarti.pad1": ["a footnote"]
}
}
```

- The source `scriptures` is ours, written for this library (`tools/meanings/style.md`); any other name is a source we copy, marked `"copied": true`. Its library id is `<lang>-<source>`.
- `title`: optional for ours (the exporter's default per language), required for a copied source.
- `order`: the source readers see first has the lowest.
- `numbers` (required on our own meanings): they end with the verse's number, `"verse"` (the number the verse ends with) or `"cite"` (its citation, `tools/text/cite.py`: the Kaṭha's mantra 1.1.1, whose verse ends ॥१॥, and the Śrī Rudram, whose mantras print none).
- `partial`: our source need not cover every verse (otherwise the export stops on a missing one).
- `m`: a string, or a list of one piece per verse line (read line by line in the app).
- `notes`: a verse's footnotes, `[footnote, …]`; they show under the meaning they belong to (the reader can hide them: ☰ › More settings › Footnotes).
- Ours may not share a run of 10 or more words with a copied source in the same language (`tools/meanings/overlap.py`).
- Written with `tools/jsonio.py` → `dump_meanings` (settings first, one verse per line).

## `commentary/<lang>/<source>.json`

A commentary explains the verses (a guru's ṭīkā, a bhāṣya); a translation is a meaning. Same format and rules as a meaning source (a list in `m` is the commentary line by line: the reader shows each line's piece as its own paragraph), with three differences: `lang` may be any language of `library/glossary/languages.json` (a Sanskrit ṭīkā is `sa`); there is no `numbers` and no `partial` (a commentary need not cover every verse); and our own (`scriptures`) has no default title. Its library id is `<lang>-<source>`, written to `library/<path>/commentary/` (`docs/LIBRARY.md` §3). A work may have any number; the reader sees none until one is chosen.

## Start a new work

1. Make `tools/works/<id>/` with `work.json`, `text.txt`, `README.md` and `reconciliation.md` (copy them from a work like it: `shiv-aarti` for a short hymn, `katha-upanishad` for a text settled from a book).
2. Add the work to the shelf, `library/index.json`.
3. Write the meanings, add the missing words to `library/glossary/<lang>.json`, then export, build and run the checks (`docs/HOW-TO.md` → "Add a new work").
4. Read the work's row in `docs/WORKS.md` (the build writes it) beside the works like it: the same levels, the same verse types and names, a citation with every level its book uses, our meanings line by line, every word with a meaning, each recording timed by MMS. Anything that differs is either fixed or said in the work's README with its reason.
5. While working on it, `python3 tools/site/check.py --works <id>` runs the build, the regeneration check (only what changed), the history check, the smoke test and the work's own UX checks; the full `check.py` before the pull request.
