# Kirtan Sohila (Guru Nanak Dev Ji, Guru Ram Das Ji, Guru Arjan Dev Ji)

Shelf: सिख धर्म › गुरबाणी › कीर्तन सोहिला, beside Sri Guru Granth Sahib: a bani of several Gurus (docs/PLAYBOOK.md §6) (`library/sikhism/gurbani/kirtan-sohila/`, work id `kirtan-sohila`, language `pa`, Gurmukhi script). Sri Guru Granth Sahib,
Sohila, Ang 12–13: 5 shabads, taken from the Granth's work unchanged (`text.txt` → `[take guru-granth-sahib 12.3 .. 13.3]`), so
its text, meanings, commentary and recordings' timings are the Granth's, and a correction there reaches this work at
the next export (`docs/PLAYBOOK.md` §3, "A verse that belongs to a bigger work is taken from it by id").

- **Text:** the Granth's, from the Shabad OS database (`tools/works/guru-granth-sahib/README.md`, "Sources and
  permissions"; CC BY-SA 4.0 for the typing, credited in the edition line); its first and last lines checked against
  the Granth's data (`reconciliation.md`).
- **Meanings:** `meanings/pa/scriptures.json` and `meanings/en/scriptures.json` take the Granth's own (`pa-scriptures`,
  `en-scriptures`). Every verse has them.
- **Commentary:** `commentary/pa/faridkot.json` takes the Granth's Faridkot Teeka.
- **Recordings:** Sehaj Path Kirtan (the default, as in the Granth); Bhai Pishora Singh Ji (Sahaj Paath); each `audio/<source>/source.json` takes the Granth's timings (`"take"`), so a start set by ear on
  the Granth's recording reaches this work (`tools/audio/apply_owner_timing.py` makes the works that take it again).
- **Word meanings:** the Granth's are not all written (`"words": "partial"`, as the Granth).
- **Introduction:** none yet; About this work shows the shelf's line (`desc`). An introduction is written once its facts
  are confirmed online (`docs/PLAYBOOK.md` §6, "About a work").

The folder's format: `tools/works/README.md`.

## Structure
- **Hierarchy:** one part (Kirtan Sohila) › sections, the Ang each verse begins on ("Ang 12", `work.json` → `sections`, as the
  Granth names them) › verses: 5 shabads, as the Granth divides them (`tools/works/guru-granth-sahib/reconciliation.md` §4).
- **Numbering:** the Granth's: a verse keeps its id and its citation, the Ang it begins on and its place among the verses
  beginning there ("Shabad 12.3"). The part's line counts its verses by type, in the bani's own words (5 shabads).
- **Topics:** the Granth's headings for these verses. **Reading plans:** none.
