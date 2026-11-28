# Lavan (Guru Ram Das Ji)

Shelf: सिख धर्म › गुरबाणी › गुरु राम दास जी › लावां (`library/sikhism/gurbani/guru-ram-das/lavan/`, work id `lavan`, language `pa`, Gurmukhi script). Sri Guru Granth Sahib,
Raag Suhi, Ang 773–774: 1 shabad, taken from the Granth's work unchanged (`text.txt` → `[take guru-granth-sahib 773.2 .. 773.2]`), so
its text, meanings, commentary and recordings' timings are the Granth's, and a correction there reaches this work at
the next export (`docs/PLAYBOOK.md` §3, "A verse that belongs to a bigger work is taken from it by id").

- **Text:** the Granth's, from the Shabad OS database (`tools/works/guru-granth-sahib/README.md`, "Sources and
  permissions"; CC BY-SA 4.0 for the typing, credited in the edition line); its first and last lines checked against
  the Granth's data (`reconciliation.md`).
- **Meanings:** `meanings/pa/scriptures.json` and `meanings/en/scriptures.json` take the Granth's own (`pa-scriptures`,
  `en-scriptures`). The Granth has none for Raag Suhi yet: the export writes no meaning source until it has (`docs/PLAYBOOK.md` §6, "A bani taken from the Granth"), and the reader shows no meaning switch; they join at the export after the Granth's Raag Suhi is written.
- **Commentary:** `commentary/pa/faridkot.json` takes the Granth's Faridkot Teeka.
- **Recordings:** Sehaj Path Kirtan (the default, as in the Granth); Bhai Pishora Singh Ji (Sahaj Paath); Kirtan (Shabad Guru and the others); each `audio/<source>/source.json` takes the Granth's timings (`"take"`), so a start set by ear on
  the Granth's recording reaches this work (`tools/audio/apply_owner_timing.py` makes the works that take it again).
- **Word meanings:** the Granth's are not all written (`"words": "partial"`, as the Granth).
- **Introduction:** none yet; About this work shows the shelf's line (`desc`). An introduction is written once its facts
  are confirmed online (`docs/PLAYBOOK.md` §6, "About a work").

The folder's format: `tools/works/README.md`.

## Structure
- **Hierarchy:** one part (Lavan) › sections, the Ang each verse begins on ("Ang 773", `work.json` → `sections`, as the
  Granth names them) › the verse: 1 shabad, as the Granth divides them (`tools/works/guru-granth-sahib/reconciliation.md` §4).
- **Numbering:** the Granth's: a verse keeps its id and its citation, the Ang it begins on and its place among the verses
  beginning there ("Shabad 773.2"). The part's line counts its verses by type, in the bani's own words (1 shabad).
- **Topics:** the Granth's headings for these verses. **Reading plans:** none.
