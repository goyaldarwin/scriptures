# Sri Guru Granth Sahib

Shelf: सिख धर्म › गुरबाणी › श्री गुरु ग्रन्थ साहिब (`library/sikhism/gurbani/guru-granth-sahib/`, work id
`guru-granth-sahib`, language `pa`, Gurmukhi script). The whole Granth, 1,430 Angs, in its 51 parts; the Japji Sahib and
the Sukhmani Sahib are taken from their works. Loaded by part (`"load": "parts"`); word meanings are not written yet
(`"words": "partial"`). Meanings: ours in Punjabi and English (`meanings/pa/scriptures.json`, `meanings/en/scriptures.json`), written part by part (`docs/PLAYBOOK.md` §4; `docs/HOW-TO.md`); the copied Santhya and Shabdarth to come as second Punjabi meanings (`docs/ROADMAP.md`, item 0).

## Sources and permissions

- **The text: the Shabad OS database**, `@shabados/database` 4.8.7 on npm (`build/database.sqlite`; github.com/shabados/database),
  whose Sri Guru Granth Sahib is typed from the SGPC's 1,430-Ang edition. The Gurbani in it is marked public domain
  (Creative Commons Public Domain Mark 1.0); what the Shabad OS team made or arranged (its typing, line division,
  translations it compiled) is under Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0). Credited here, in the
  root `README.md` and in the app's edition line; the files made from it here are shared under the same licence.
- **Witnesses of the text** (scratch copies made by `tools/meanings/teeka.py fetch` from the owner's PDFs in the private
  `scriptures-data`, `reference/pa/commentaries/`, never committed): the Gurbani printed in Prof. Sahib Singh's Sri Guru
  Granth Darpan and in the Faridkot Teeka. `source/check.py` compares them word by word (`reconciliation.md`).
- **The Faridkot Teeka** (`commentary/pa/faridkot.json`): the commentary made at the Faridkot court by Nirmala scholars
  (1883–1905, public domain), as the Shabad OS database gives it (its translation source "Fareedkot Teeka", typed
  line by line, CC BY-SA 4.0 for the typing), copied as given.
- **The introduction** (`intro` in `library/index.json`): Wikipedia, "Guru Granth Sahib"
  (https://en.wikipedia.org/wiki/Guru_Granth_Sahib), only what it states: the central scripture of Sikhism, regarded as
  the final, sovereign and eternal Guru after the ten human Gurus, so affirmed by Guru Gobind Singh in 1708; the first
  rendition, the Adi Granth, compiled by Guru Arjan and completed in 1604, Bhai Gurdas his scribe, installed in the
  Golden Temple; the hymns of Guru Tegh Bahadur added by Guru Gobind Singh (the Damdama bir); composed mainly by six
  Gurus (Nanak, Angad, Amar Das, Ram Das, Arjan, Tegh Bahadur), with hymns of Bhakti sants, two Muslim saint poets and
  the Bhatts; written in the Gurmukhi script in several languages; 1,430 Angs, arranged mainly by 31 raags, opening with
  the Mul Mantar, Japji, So Dar and Sohila and closing with the Mundavani and the Raagmala; the focal point of every
  gurdwara, on a raised throne, read by a granthi, approached with head covered and shoes off. The text itself gives the
  parts and the counts.

## Files

The folder's format: `tools/works/README.md`. The database itself (158 MB) is not in this repository: its Granth lines
are, in `source/shabados.tsv`, so the text is made and checked here (`tools/site/regen_check.py` runs `make.py`). The
database's npm package is kept in the private `scriptures-data` (`sikhism/gurbani/guru-granth-sahib/printouts/shabados/`, with its `.meta.json`), or
`npm install @shabados/database@4.8.7`; give its `build/database.sqlite` with `--db` to make the extract again or the
commentary.

- `source/shabados.tsv` — the database's 60,555 Granth lines as it types them (legacy ASCII), with their unit, section,
  writer, line id, Ang, line and type (`python3 source/shabados.py --extract --db DB`).
- `source/shabados.py` — reads the extract (or the database): its Granth lines (legacy ASCII Gurmukhi) → Unicode with the Sukhmani Sahib's
  converter (`tools/works/sukhmani-sahib/source/gurmukhi.py`) and the writing standard; the vishraam marks, the spacer and
  the small numerals under some headings are left out (`reconciliation.md` §2).
- `source/make.py` — the database → `text.txt` (the verses, parts, sections, topics, the two taken banis) and `views.json`
  (the writers and the Angs).
- `source/check.py` — the checks of `reconciliation.md`: the structure, the taken banis equal to the database, and the
  text word by word against the Darpan and the Faridkot Teeka.
- `source/faridkot.py` — the database's Faridkot Teeka → `commentary/pa/faridkot.json`.
- `commentary/pa/faridkot.json` — the Faridkot Teeka, line by line (`"copied": true`).

- `source/differences.tsv` — every word of the text a witness gives otherwise, with its decision (`check.py --record`).

Rebuild: `python3 tools/works/guru-granth-sahib/source/make.py && python3 tools/works/guru-granth-sahib/source/faridkot.py --db DB && python3 tools/works/export.py guru-granth-sahib && python3 tools/site/build.py`.

## Structure

- **Hierarchy:** part (the 51 parts of the Granth: Jap, So Dar, So Purakh, Sohila, the 31 raags from Sri Raag to Raag
  Jaijavanti, then Salok Sahaskriti, Gatha, Phunhe, Chaubole, Salok Kabir Ji, Salok Farid Ji, the six Swayye, Salok Varan
  te Vadhik, Salok Mahala 9, Mundavani Mahala 5, Raagmala) › section (the Ang a verse begins on, "Ang 14") › verse.
  The taken Japji and Sukhmani keep their own sections, named in `work.json` → `sections`.
- **A verse** is one shabad, or one pauri or salok of a composition, its lines (pangtis) as the Granth prints them, each
  ending with ॥ (or its number mark). Headings (ਸਿਰੀਰਾਗੁ ਮਹਲਾ ੧ ॥, ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥) are lines of the verse they head.
  Types: shabad, salok, pauri, rahao (the rahao of a bani cut into pauris: Patti, Oankar, Thiti, Sidh Gosht), pad (a stanza
  of the Bara Mahas, the Ruti, the Gatha, the Phunhe, the Chaubole), swayya; and those of the Japji (mool, heading).
- **Ids:** `<Ang>.<k>`: the Ang the verse begins on and its place among this text's own verses beginning there (`14.1`,
  `14.2`, the So Dar `8.1`); taken verses keep their ids (`mool`, `p1`, `a01.p1`). Permanent.
- **Numbering:** a verse is cited by its Ang and its place on it (`cite`: `by` sec.n, `sec` Ang): "Shabad 14.2",
  "Pauri 917.2". The numbers at a verse's end (॥੪॥੧॥੩੪॥: its stanzas, its place in its group of shabads, in its raag)
  stay as printed but are not its citation, because they restart with each Guru, each kind of composition and each vaar
  (`cite.mark` "none"). The Japji and the Sukhmani keep their own citations (Pauri 5, Pauri 1.8).
- **Views** (`views.json`, made by `make.py`, joined to the manifest by `include`): beside its parts the Granth is
  classified by **writer** (the Gurus, the Bhagats, the Bhatts, Satta and Balwand and Baba Sundar; each writer's verses
  in the Granth's order, read on their own) and by **Ang** (for each of the 1,430 Angs, the verse its first line is in).
  How a writer is settled: `reconciliation.md` §6.
- **Topics:** every shabad, and every salok and swayya of the closing compositions, by its first line (as the Japji's);
  a composition (a vaar, a bani of pauris or stanzas) once, at its start, by its heading line.

## Introduction
`intro` in `library/index.json`, from Wikipedia's "Guru Granth Sahib" (above); it states only what that article and the
text support.
