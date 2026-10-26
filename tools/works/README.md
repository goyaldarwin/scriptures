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
| `glossary/<lang>.json` | the work's own sense of a word whose shared entry (`library/glossary/<lang>.json`) carries another text's sense | |
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
- `numbers`: ours end with the verse's number, `"verse"` (the number the verse ends with) or `"n"` (its `n`, for works whose verses carry none in their lines).
- `partial`: our source need not cover every verse (otherwise the export stops on a missing one).
- `m`: a string, or a list of one piece per verse line (read line by line in the app).
- Ours may not share a run of 10 or more words with a copied source in the same language (`tools/meanings/overlap.py`).
- Written with `tools/jsonio.py` → `dump_meanings` (settings first, one verse per line).

## Start a new work

1. Make `tools/works/<id>/` with `work.json`, `text.txt`, `README.md` and `reconciliation.md` (copy them from a work like it: `shiv-aarti` for a short hymn, `katha-upanishad` for a text settled from a book).
2. Add the work to the shelf, `library/index.json`.
3. Write the meanings, add the missing words to `library/glossary/<lang>.json`, then export, build and run the checks (`docs/HOW-TO.md` → "Add a new work").
