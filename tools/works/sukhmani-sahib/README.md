# Sukhmani Sahib (Guru Arjan Dev Ji)

Shelf: सिख धर्म › गुरबाणी › गुरु अर्जन देव जी › सुखमनी साहिब (`library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/`,
work id `sukhmani-sahib`, language `pa`, Gurmukhi script). Sri Guru Granth Sahib, Ang 262–296.

## Source

The owner's PDF, “Sukhmani Sahib with phonetic transliteration & English translation, Gurmukhi” (K. Thind, 2003,
225 pages). It is private: `goyaldarwin/scriptures-data`, at
`sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/books/sant-singh-khalsa/sukhmani-sahib.pdf`. Every line of the bani
is printed as Gurmukhi (in a legacy font encoding), transliteration and English (Dr. Sant Singh Khalsa).

## Files

- `extract.py` — the PDF → `source/lines.json` (2,018 printed lines: legacy Gurmukhi, transliteration, English, page).
  Only needed again if the PDF changes: `python3 tools/works/sukhmani-sahib/extract.py <the PDF>`.
- `gurmukhi.py` — the legacy ASCII Gurmukhi encoding (GurbaniAkhar / AnmolLipi) → Unicode, with its mapping table.
- `check.py` — checks the conversion of every line against the PDF's own transliteration; optionally against two
  outside witnesses (see its header). `export.py` runs it first and stops if it fails.
- `structure.py` — printed lines → the 218 items (below), with structural checks.
- `meanings/hi.json`, `en.json`, `pa.json` — our Hindi, English and Punjabi meanings of every item, written for this
  library from the Gurmukhi (`tools/meanings/style.md` §12–13).
- `glossary/pa.json` — meanings of all 2,536 Gurmukhi words of the text, written for this library.
- `reconciliation.md` — how the text is settled: conversion decisions, check results, the one English fix.
- `export.py` — writes `work.json`, `meanings/hi-scriptures.json`, `en-scriptures.json` and `pa-scriptures.json`
  (ours, order 1; the English is checked to share no run of 10+ words with the PDF's), `meanings/en-sant-singh-khalsa.json`
  (the PDF's English, order 2, still selectable), and adds new words to `library/glossary/pa.json`. Then run
  `python3 tools/site/build.py`.
- `audio/parminder-singh/` — the recording (YouTube `KJ8D_ObQNzQ`), a **draft** (`source.json` → `draft`): kīrtan with
  long instrumental passages, so the automatic starts are not reliable. The owner marks the starts by ear in the app
  (`owner.json`, written by `tools/audio/apply_owner_timing.py`).

## Structure

Parts are the 24 Ashtapadis (अष्टपदी / Ashtapadi). Items, in reading order (ids are permanent):

| id | type | text |
|---|---|---|
| `a01.title` | heading | ਗਉੜੀ ਸੁਖਮਨੀ ਮਃ ੫ ॥ |
| `aNN.salok` | salok | ਸਲੋਕੁ ॥ + the salok (Ashtapadi 1: with ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥ and ਆਦਿ ਗੁਰਏ ਨਮਹ …) |
| `aNN.p1` | pauri 1 | ਅਸਟਪਦੀ ॥ + ten padas ॥੧॥ |
| `a01.rahao` | rahao | ਸੁਖਮਨੀ ਸੁਖ ਅੰਮ੍ਰਿਤ ਪ੍ਰਭ ਨਾਮੁ ॥ ਭਗਤ ਜਨਾ ਕੈ ਮਨਿ ਬਿਸ੍ਰਾਮ ॥ ਰਹਾਉ ॥ |
| `aNN.p2` … `aNN.p8` | pauri | ten padas each, the last ending ॥੮॥N॥ |

Each item is its own section (page) in the reader. Topics: two per Ashtapadi (starting at its Salok and at its first pauri), named by the first line of its
Salok and of its first pauri (the traditional way to cite Gurbani), in Devanagari letters for the Hindi interface
and in the PDF's transliteration for the English one. The transliteration is kept in each item's `t`, as printed.
