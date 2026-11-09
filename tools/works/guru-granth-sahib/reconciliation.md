# Sri Guru Granth Sahib — how the text is settled

Source of truth: the Shabad OS database, `@shabados/database` 4.8.7 on npm (its Sri Guru Granth Sahib, typed from the
SGPC's 1,430-Ang edition). Witnesses: the Gurbani printed in Prof. Sahib Singh's Sri Guru Granth Darpan and in the
Faridkot Teeka (the owner's PDFs in the private `scriptures-data`, `reference/pa/commentaries/`). No OCR.

## 1. Reading the database (`source/shabados.py`)

The database's Granth lines are kept in `source/shabados.tsv` exactly as it types them. Its 60,555 lines of the Granth (source 1) are in the common legacy ASCII Gurmukhi encoding, converted with
the Sukhmani Sahib's converter (`tools/works/sukhmani-sahib/source/gurmukhi.py`; its decisions:
`tools/works/sukhmani-sahib/reconciliation.md` §2), then by the writing standard (`tools/text/standard.py`: ॥ with no
space inside a number mark). Every line converts; the characters used are the 35 letters, the vowel signs, tippi, bindi,
visarga, the pairin ਰ ਹ ਵ, ੑ (udaat, the half ਹ), ੵ (yakash), ੴ and the Gurmukhi digits.

## 2. What is left out of the database's lines

- **The vishraams** `;` `.` `,` (76,737 pause marks added for reading aloud; the Granth does not print them), as in the
  Japji Sahib's check.
- **The spacer `Ø`** (111 places): a blank glyph the legacy fonts put under a bindi or tippi before a bihari (ˆØI); the
  letter is written with its bihari and nasal in Unicode order (ਪਾਈਂ). A tippi with a bihari (ਥਿਤੀੰ) is written bihari
  first, as every vowel sign comes before its nasal sign in this library.
- **The small numerals under some headings** (36 headings: ਗਉੜੀ₂ ਮਹਲਾ ੫ ॥, ਆਸਾ ਮਹਲਾ ੫ ਪੰਚਪਦੇ₃ ॥, ਗਉੜੀ ਕਬੀਰ ਜੀ ਤਿਪਦੇ₁₅ ॥):
  the Granth prints them small under a word of the heading, as the count of the shabads of that kind that follow (the
  Darpan's own note at Ang 356: "ਲਫ਼ਜ਼ 'ਪੰਚਪਦੇ' ਦਾ ਹੇਠਲਾ ਅੰਕ … ਦੱਸਦਾ ਹੈ ਕਿ ਇਹ ਸ਼ਬਦ ਗਿਣਤੀ ਵਿਚ …"). They are not read
  as part of the heading, Unicode has no small Gurmukhi numerals, and written full-size in the line they would read as
  part of it (ਗਉੜੀ ੨ ਮਹਲਾ ੫); so the heading is written without them. The Faridkot Teeka prints these headings without
  them; the Darpan sets them as small glyphs in some.

## 3. The text against its witnesses (`source/check.py`, every difference in `source/differences.tsv`)

The whole Granth, 399,248 words (the taken Japji and Sukhmani included, from the database's lines), was compared word
by word with each witness's Gurbani (the method: `source/check.py`'s docstring):

| | words of the text compared | words differing | of them |
|---|---|---|---|
| Darpan | 375,593 (94.1%) | 316 | 266 word division · 25 signs set in another order · 7 signs the font drops · 18 words its font sets otherwise |
| Faridkot Teeka | 366,511 (91.8%) | 315 | 249 word division · 7 font · 59 readings of its own |

The rest of each witness is its commentary, or lines the conversion could not tell from it (Darpan: the Gurbani set in
the visual-order font; Faridkot: lines ending in ॥ that convert cleanly), and is not counted.

Decisions (PLAYBOOK §2: the base edition stays unless its reading is clearly an error that the witnesses correct):

- **One correction, Ang 608** (Sorath Mahala 5, `608.1`): the database has ਕਿਸੁ ਹਉ ਜਾਚੀ **ਕਿਸੁ** ਆਰਾਧੀ ਜਾ ਸਭੁ ਕੋ ਕੀਤਾ ਹੋਸੀ ॥;
  the Darpan, the Faridkot Teeka and srigranth.org (the SGPC text, checked online) all have ਕਿਸ ਆਰਾਧੀ, without the aunkar
  (the only place both witnesses agree against the text). The text has ਕਿਸ (`make.py` → `FIX`).
- **Word division** (515 places, 203 of them the same in both witnesses): the witnesses divide some compounds the
  database prints as one word, almost all ਗੁਰਸਬਦੀ / ਗੁਰਸਬਦੁ / ਗੁਰਸਬਦ (ਗੁਰ ਸਬਦੀ) and ਵਡਭਾਗ (ਵਡ ਭਾਗ). The Granth is written
  without spaces between words (larivaar); the division is each edition's, and the base edition's is kept throughout
  (the Japji and Sukhmani follow it too).
- **The Darpan's font** (50 places): its Gurbani font has no glyph for some signs and draws others in another order
  (a yakash ੵ under ਰ, ਈਂ split, ਲੁੰ, the hora with an aunkar, small numerals as stray letters); after these are allowed
  for, it reads with the text everywhere but Ang 608.
- **The Faridkot Teeka's own readings** (59 places: ਨਾ/ਨ, ਸਤਗੁਰ/ਸਤਿਗੁਰ, ਦੇਵਲ/ਦੇਵੇਂ, ਹਰਨਾਕਸ/ਹਰਨਾਖਸ, ਅਪਨੇ/ਅਪੁਨੇ, ਰੰਗ/ਰੰਗਿ …):
  one witness alone, the Darpan reading with the text; the text is kept.

## 4. Verses (`source/make.py`)

The database's 5,549 units are its display units, not always the Granth's shabads. A verse here is one shabad, or one
pauri or salok of a composition (README.md, "Structure"); the choices:

- A heading the database puts at the end of the unit before its shabad (Sarang, Ang 1230; Bilaval, Ang 829) goes to its
  shabad; a unit of headings only (ਰਾਗੁ ਆਸਾ ਮਹਲਾ ੩ ਪਟੀ ॥) joins the verse after it.
- Four chhants the database cuts into their stanzas and saloks (ਡਖਣੇ) are one verse each again, as the Granth numbers
  them: Sri Raag `80.1`, Vadhans `577.1`, Jaitsri `704.1`, Ramkali `926.1`.
- Banis the database keeps whole although the Granth numbers each pauri or salok are cut at every number: Kabir's
  Bavan Akhri and Thiti (Gauri), the two Pattis (Asa), the Thiti Mahala 1 (Bilaval), the Anand and the Dakhni Oankar
  (Ramkali), the Gatha, the Phunhe and the Saloks Varan te Vadhik; so are the units holding two or more pauris of the
  Sidh Gosht and units of two saloks. A rahao after a pauri's number is a verse of its own (type rahao, as in the
  Sukhmani Sahib): 7 of them.
- The Bara Mahas (Majh Mahala 5, Tukhari Mahala 1), the Ruti (Ramkali) and the Vaar of Balvand and Satta keep one verse
  per stanza, as the database has them.
- The Japji Sahib (`[take japji-sahib mool .. salok.close]`) and the Sukhmani Sahib (`[take sukhmani-sahib a01.title ..
  a24.p8]`) are taken from their works. Their lines equal the database's (`check.py` proves it on every run): the
  Sukhmani's 2,027 lines exactly, the Japji's but for its Mool Mantar, which the Japji prints on four lines.

Result: 5,767 verses of this text's own (2,928 shabads, 1,751 saloks, 841 pauris, 97 stanzas, 143 swayyas, 7 rahaos) and
260 taken, 60,555 lines in all (58,143 of its own).

## 5. The Faridkot Teeka (`source/faridkot.py` → `commentary/pa/faridkot.json`)

Copied as the database gives it, line by line (5,766 verses of this work, and every verse of the Japji Sahib and the
Sukhmani Sahib in their own works, so the taken verses carry it too). Changed only where the database's typing broke:
a private-use code for a hora (U+F02B, 16 places → ੋ) and for a bindi (U+F02E, 8 → ਂ), one stray (U+F02C) and a
zero-width non-joiner dropped, the addak typed as ~ before its letter (~ → ੱ, 7) and one word left in the legacy
encoding (qMU → ਤੂੰ). Its paragraph mark ☬ is a line break; its footnotes (_¹_ …) are the verse's notes.

## 6. Writers and Angs (`source/make.py` → `views.json`)

- **A verse's writer** is the database's writer of its unit (every verse's units have one writer; the taken Japji and
  Sukhmani Sahib, the database's Guru Nanak Dev Ji and Guru Arjan Dev Ji). Where a verse's own heading names a Mahala and
  the database names a Bhagat, the heading is the Granth's word and wins: `326.1` (ਗਉੜੀ ਕਬੀਰ ਜੀ ਕੀ ਨਾਲਿ ਰਲਾਇ ਲਿਖਿਆ ਮਹਲਾ ੫,
  the database's Bhagat Kabir Ji), `1136.3` (ਭੈਰਉ ਮਹਲਾ ੫, Bhagat Kabir Ji) and `1253.3` (ਸਾਰੰਗ ਮਹਲਾ ੫ ਸੂਰਦਾਸ, Bhagat
  Surdas Ji) are Guru Arjan Dev Ji's. A vaar's heading names the vaar's writer, not its saloks', so it does not count
  (the Vaars of Sri Raag, Bihagra, Vadhans, Maru, Sarang and Malar open with another Guru's salok).
- **The Raagmala** (`1429.13`) is in no writer's list: the Granth names no writer for it; the database's "Poet Alam" is
  an attribution, not the text's.
- **Names:** the database's, in Gurmukhi as it types them; in English its plain spelling (Guru Amar Das Ji and Guru Ram
  Das Ji in two words, Bhagat Bhikhan, Bhatt Jalap, Bhatt Kirat); in Hindi the same names in Devanagari. Four groups:
  the Gurus (by Mahala; Guru Tegh Bahadur Ji is Mahala 9), the Bhagats, the Bhatts, and Satta and Balwand with Baba
  Sundar.
- **An Ang** opens at the verse its first line is in, from the database's Ang of every line (the taken banis' lines
  matched one by one with the database's, as `check.py` proves them equal).
