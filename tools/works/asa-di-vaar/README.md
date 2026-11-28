# Asa Di Vaar (Guru Nanak Dev Ji)

Shelf: सिख धर्म › गुरबाणी › गुरु नानक देव जी › आसा दी वार (`library/sikhism/gurbani/guru-nanak-dev/asa-di-vaar/`, work id `asa-di-vaar`, language `pa`, Gurmukhi script). Sri Guru Granth Sahib,
Raag Asa, Ang 462–475: 60 saloks, 24 pauris, 1 rahao, taken from the Granth's work unchanged (`text.txt` → `[take guru-granth-sahib 462.1 .. 475.5]`), so
its text, meanings, commentary and recordings' timings are the Granth's, and a correction there reaches this work at
the next export (`docs/PLAYBOOK.md` §3, "A verse that belongs to a bigger work is taken from it by id").

- **Text:** the Granth's, from the Shabad OS database (`tools/works/guru-granth-sahib/README.md`, "Sources and
  permissions"; CC BY-SA 4.0 for the typing, credited in the edition line); its first and last lines checked against
  the Granth's data (`reconciliation.md`).
- **Meanings:** `meanings/pa/scriptures.json` and `meanings/en/scriptures.json` take the Granth's own (`pa-scriptures`,
  `en-scriptures`). Every verse has them.
- **Commentary:** `commentary/pa/faridkot.json` takes the Granth's Faridkot Teeka.
- **Recordings:** Sehaj Path Kirtan (the default, as in the Granth); Bhai Pishora Singh Ji (Sahaj Paath), 32 of its 85 verses not sung there; Kirtan (Shabad Guru and the others), 5 of its 85 verses not sung there; each `audio/<source>/source.json` takes the Granth's timings (`"take"`), so a start set by ear on
  the Granth's recording reaches this work (`tools/audio/apply_owner_timing.py` makes the works that take it again).
- **Word meanings:** the Granth's are not all written (`"words": "partial"`, as the Granth).
- **Introduction:** none yet; About this work shows the shelf's line (`desc`). An introduction is written once its facts
  are confirmed online (`docs/PLAYBOOK.md` §6, "About a work").

The folder's format: `tools/works/README.md`.

## Structure
- **Hierarchy:** one part (Asa Di Vaar) › sections, the Ang each verse begins on ("Ang 462", `work.json` → `sections`, as the
  Granth names them) › verses: 60 saloks, 24 pauris, 1 rahao, as the Granth divides them (`tools/works/guru-granth-sahib/reconciliation.md` §4).
- **Numbering:** the Granth's: a verse keeps its id and its citation, the Ang it begins on and its place among the verses
  beginning there ("Salok 462.1"). The part's line counts its verses by type, in the bani's own words (60 saloks, 24 pauris, 1 rahao).
- **Topics:** the Granth's headings for these verses. **Reading plans:** none.
