# Japji Sahib (Guru Nanak Dev Ji)

Shelf: सिख धर्म › गुरबाणी › गुरु नानक देव जी › जपुजी साहिब (`library/sikhism/gurbani/guru-nanak-dev/japji-sahib/`,
work id `japji-sahib`, language `pa`, Gurmukhi script). Sri Guru Granth Sahib, Ang 1–8.

## Source

The owner's PDF, SikhNet's “1 - Japji [Gurmukhi]” (37 pages, Gurmukhi only, in a legacy font encoding). It is private:
`goyaldarwin/scriptures-data`, at `sikhism/gurbani/guru-nanak-dev/japji-sahib/books/sikhnet/japji.pdf`. The text agrees
word for word with the Shabad OS database and with the owner's earlier study sheet (`reconciliation.md`).

## Files

The folder's format: `tools/works/README.md`.

- `source/extract.py` — the PDF → `source/pdf.txt` (its text layer, one printed line per line). Only needed again if the
  PDF changes: `python3 tools/works/japji-sahib/source/extract.py <the PDF>`.
- `source/make.py` — `pdf.txt` → `text.txt`: converts the legacy Gurmukhi with the Sukhmani Sahib's converter
  (`tools/works/sukhmani-sahib/source/gurmukhi.py`), one line per pada, the structure checked; topics named by first lines.
- `source/check.py` — the checks of `reconciliation.md` (structure always; the witnesses when given).
- `meanings/en/scriptures.json`, `meanings/hi/scriptures.json`, `meanings/pa/scriptures.json` — our English, Hindi and
  Punjabi meanings, written for this library from the Gurmukhi line by line (`tools/meanings/style.md` §12–13), each with
  notes that explain terms, allusions and readings (the owner asked for meanings that are elaborate as well as accurate).
  They were checked against Prof. Sahib Singh's Darpan and the Faridkot Teeka, and against the translations of Sant Singh
  Khalsa and Manmohan Singh (English) and Manmohan Singh, Prof. Sahib Singh and the Faridkot Teeka (Punjabi), with no
  run of 10 or more words in common (`tools/meanings/overlap.py`).
- The meanings of the Japji's Gurmukhi words are in `library/glossary/pa.json`.
- `audio/nirvair-khalsa-jatha-uk/` — the recording (YouTube `wbuM4eyIBDM`, 16 minutes), published for review (`source.json` → `review`): sung with a harmonium between lines, so the starts come from the 6-second-window transcript's anchor alignment (step 1 of `tools/audio/METHOD.md`), seven of them hand-checked (`fixes.md`); every start is on the to-check list until the owner sets it by ear. MMS (steps 2–5) is used once the owner has set 20–30 starts to score it on.

Rebuild: `python3 tools/works/japji-sahib/source/make.py && python3 tools/works/export.py japji-sahib && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the whole bani) › each item its own section › the item.
- **Numbering:** a pauri's `n` is the number it ends with (॥੧॥ … ॥੩੮॥); the two saloks end with ॥੧॥ and are told apart
  by their section names (Opening Salok, Closing Salok). The Mool Mantar and the title have no number.

| id | type | text |
|---|---|---|
| `mool` | mool (Mool Mantar) | ੴ ਸਤਿ ਨਾਮੁ ਕਰਤਾ ਪੁਰਖੁ … ਗੁਰ ਪ੍ਰਸਾਦਿ ॥ (four lines, as the PDF prints them) |
| `jap` | heading | ॥ ਜਪੁ ॥ |
| `salok.open` | salok 1 | ਆਦਿ ਸਚੁ ਜੁਗਾਦਿ ਸਚੁ ॥ ਹੈ ਭੀ ਸਚੁ ਨਾਨਕ ਹੋਸੀ ਭੀ ਸਚੁ ॥੧॥ |
| `p1` … `p38` | pauri 1–38 | the 38 pauris |
| `salok.close` | salok 1 | ਸਲੋਕੁ ॥ ਪਵਣੁ ਗੁਰੂ ਪਾਣੀ ਪਿਤਾ … ਕੇਤੀ ਛੁਟੀ ਨਾਲਿ ॥੧॥ |

Topics: the Mool Mantar, then one per salok and pauri, named by its first line (the traditional way to cite Gurbani), in
Devanagari letters for the Hindi interface and in its ISO 15919 transliteration for the English one.

## Introduction
The readers' introduction (`intro` in `library/index.json`) states only what these support:
- Wikipedia, "Japji Sahib" (https://en.wikipedia.org/wiki/Japji_Sahib): by Guru Nanak; opens the Guru Granth Sahib; the
  name Jap (japa) and the honorifics; the essence of Sikhism, the Granth its expansion; Mool Mantar, 38 pauris in different
  metres, a final salok by Guru Angad; the themes (purification, Hukam, listening and faith, God formless and beyond
  description); the first bani of Nitnem, for individual meditative recitation; recited in gurdwaras morning and evening,
  at the Khalsa initiation and at cremation.
- The text itself: Ang 1–8, the opening salok, Suniai and Mannai, the five khands.
