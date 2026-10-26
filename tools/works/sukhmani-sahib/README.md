# Sukhmani Sahib (Guru Arjan Dev Ji)

Shelf: सिख धर्म › गुरबाणी › गुरु अर्जन देव जी › सुखमनी साहिब (`library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/`,
work id `sukhmani-sahib`, language `pa`, Gurmukhi script). Sri Guru Granth Sahib, Ang 262–296.

## Source

The owner's PDF, “Sukhmani Sahib with phonetic transliteration & English translation, Gurmukhi” (K. Thind, 2003,
225 pages). It is private: `goyaldarwin/scriptures-data`, at
`sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/books/sant-singh-khalsa/sukhmani-sahib.pdf`. Every line of the bani
is printed as Gurmukhi (in a legacy font encoding), transliteration and English (Dr. Sant Singh Khalsa).

## Files

The folder's format: `tools/works/README.md`.

- `source/extract.py` — the PDF → `source/lines.json` (2,018 printed lines: legacy Gurmukhi, transliteration, English, page).
  Only needed again if the PDF changes: `python3 tools/works/sukhmani-sahib/source/extract.py <the PDF>`.
- `source/gurmukhi.py` — the legacy ASCII Gurmukhi encoding (GurbaniAkhar / AnmolLipi) → Unicode, with its mapping table.
- `source/check.py` — checks the conversion of every line against the PDF's own transliteration; optionally against two
  outside witnesses (see its header).
- `source/structure.py` — printed lines → the 218 verses (below), with structural checks.
- `source/make.py` — runs both checks, then writes `text.txt` (with the parts and topics) and
  `meanings/en/sant-singh-khalsa.json` (the PDF's English, copied, `order: 2`, still selectable).
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`, `meanings/pa/scriptures.json` — our Hindi, English and
  Punjabi meanings of every verse, written for this library from the Gurmukhi (`tools/meanings/style.md` §12–13); ours
  are the default, and the export checks that our English shares no run of 10+ words with the PDF's.
- The meanings of all 2,536 Gurmukhi words of the text, written for this library, are in `library/glossary/pa.json`.
- `reconciliation.md` — how the text is settled: conversion decisions, check results, the one English fix.
- `audio/parminder-singh/` — the recording (YouTube `KJ8D_ObQNzQ`), published for review (`source.json` → `review`): kīrtan
  with long instrumental passages, so the automatic starts are only partly confirmed. Readers hear it; every start not yet
  set by ear is listed for the owner to check in timing mode (`owner.json`, written by `tools/audio/apply_owner_timing.py`).

Rebuild: `python3 tools/works/sukhmani-sahib/source/make.py && python3 tools/works/export.py sukhmani-sahib && python3 tools/site/build.py`.

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
and in its ISO 15919 transliteration for the English one. Each item's `t` is the ISO 15919 transliteration of its
Gurmukhi, made by the writing standard (`tools/text/standard.py`); the PDF's own phonetic transliteration is used only by
`source/check.py`, as a witness of the conversion.
