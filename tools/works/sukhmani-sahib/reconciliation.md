# Sukhmani Sahib — how the text is settled

Source of truth: the owner's PDF, “Sukhmani Sahib with phonetic transliteration & English translation, Gurmukhi”
(K. Thind, 2003; 225 pages). Private copy: `scriptures-data/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/books/sant-singh-khalsa/sukhmani-sahib.pdf`.

## 1. Reading the PDF

The text layer is clean, and every line of the bani is printed as three lines in three fonts (`source/extract.py`):
the Gurmukhi in **GurbaniAkharThick** (a legacy font: ASCII letters drawn as Gurmukhi), then the transliteration
and the English translation in Tahoma, each sometimes wrapped. 2,018 printed lines; no OCR is needed.

The transliteration is told from the English by counting pada ends: the Gurmukhi ends each pada with `]`, the
transliteration with `.` (and a numbered line with `||n||`). On page 223 the transliteration's
`||6||` wraps onto a line of its own; the extractor waits for the `||n||` of a numbered line, so it is not taken as
the start of the English (“||6|| - these blessings come to one who…”).

## 2. Converting the Gurmukhi (`gurmukhi.py`)

A table maps every legacy character to Unicode and a class (letter, subjoined letter, vowel sign, sihari, nasal,
addak, visarga, punctuation). Letters are grouped into clusters; the legacy sihari `i`, typed before its letter,
is moved after the letter and its subjoined consonant (`ismrau` → ਸਿਮਰਉ, `AMimRq` → ਅੰਮ੍ਰਿਤ, `ik®pw` → ਕ੍ਰਿਪਾ);
marks are written in Unicode order (subjoined, vowel, nasal, addak); a vowel bearer with its sign becomes the
independent vowel (ੳ+ੁ → ਉ, ੲ+ਿ → ਇ, ਅ+ਾ → ਆ); the result is NFC. Unknown characters stop the conversion.

Characters that occur in this PDF: the 35 letters used, `w I u U y Y o O W` (W = ਾਂ), `i`, `M µ` (tippi), `R ®`
(pairin rara), `@` (half haha), `´` (half yayya), `Í` (pairin vava), `ü` (aunkar under a pairin), `E` (ਓ), `\`
(ਞ), `Ú` (visarga, in ਮਃ), `]`, `<>`, digits. Not occurring but mapped: nukta letters (S ^ Z z & L), bindi `N`,
addak, the other pairin letters.

Two code-point decisions, following the Gurbani databases (SikhiToTheMax/BaniDB, Shabad OS) rather than a
generic ੍ + letter:
- `´` → **ੵ U+0A75 (yakash)**: ਸੁਧਾਖੵਰ, ਆਖੵਰ, ਬਖੵਾਨੁ, ਨਖੵਤ੍ਰ, ਜਖੵ, ਅਧਾਖੵਰੁ, ਅਖੵਓ.
- `@` → **ੑ U+0A51 (udaat)**, the small half-ਹ under ਮ in ਤੁਮੑਾਰੀ, ਤੁਮੑਰੀ, ਤੁਮੑਾਰੋ (3 words). `H`, the full pairin
  haha, stays ੍ਹ.
The Noto Serif Gurmukhi font of the site has both signs (checked in its cmap and on screen).

## 3. Checks (`source/check.py`)

1. **Conversion**: all 2,018 lines convert; no unknown character, no bare vowel bearer, nothing outside Gurmukhi,
   digits, ॥ and spaces.
2. **Consonant skeleton against the PDF's own transliteration**: each line's Gurmukhi and its printed
   transliteration are reduced to their consonants by place of articulation and compared, allowing a tippi/bindi
   to read as n, m or nothing, a doubled consonant, and “bh/rh/kh …” for a letter + ਹ (ਕਬਹੂ kabhoo,
   ਪਰਹਰੈ parharai), ਞ = nj. **2,018 of 2,018 lines agree.**
3. **Independent witnesses** (run with `--shabados` and `--gurmukhi-utils`; scratch copies, not committed):
   - The Shabad OS database (`@shabados/database` 4.8.7 on npm, which stores Gurbani in the same ASCII
     encoding): its Sukhmani Sahib bani, with its vishraam marks `; .` removed, compared word by word with the
     PDF: **12,391 words each, 0 differences**. The PDF's Gurmukhi is letter-perfect against it.
   - `gurmukhi-utils` 3.2.2 (Shabad OS's own ASCII→Unicode converter, run with node): **2,018 of 2,018 lines
     identical** to `gurmukhi.py`'s output.
4. **Known lines** (checked by eye against the standard Unicode Gurbani text): ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ ॥ ·
   ਗਉੜੀ ਸੁਖਮਨੀ ਮਃ ੫ ॥ · ਸੁਖਮਨੀ ਸੁਖ ਅੰਮ੍ਰਿਤ ਪ੍ਰਭ ਨਾਮੁ ॥ ਭਗਤ ਜਨਾ ਕੈ ਮਨਿ ਬਿਸ੍ਰਾਮ ॥ ਰਹਾਉ ॥ · ਆਦਿ ਗੁਰਏ ਨਮਹ ॥ ·
   ਬੇਦ ਪੁਰਾਨ ਸਿੰਮ੍ਰਿਤਿ ਸੁਧਾਖੵਰ ॥ · ਟੂਟੀ ਗਾਢਨਹਾਰ ਗੋੁਪਾਲ ॥ (hora and aunkar together, as printed) ·
   ਨਾਨਕ ਇਹ ਗੁਣਿ ਨਾਮੁ ਸੁਖਮਨੀ ॥੮॥੨੪॥.
   Web pages (searchgurbani.com, sikhsamridhi.com, api.banidb.com) are not used for spot checks: their
   Gurbani is rendered by JavaScript, and the workspace's network proxy refuses direct downloads. The
   Shabad OS database above serves instead.

## Skeleton exceptions

None: every line agrees (the check fails on any line not listed here).

## 4. Structure (`source/structure.py`)

Checked by the code: 24 Ashtapadis; each has one Salok and eight pauris numbered ॥੧॥ … ॥੮॥, the last ending
॥੮॥n॥ with its Ashtapadi's number; every pauri has ten padas (plus the heading ਅਸਟਪਦੀ ॥ in pauri 1). The title
ਗਉੜੀ ਸੁਖਮਨੀ ਮਃ ੫ ॥ and the Rahaa-o couplet (after pauri 1 of Ashtapadi 1) are their own items. 218 items.
Where the PDF prints two padas on one line (9 places, e.g. ਜਿਉ ਮਹਾ ਉਦਿਆਨ ਮਹਿ ਮਾਰਗੁ ਪਾਵੈ ॥ ਤਿਉ ਸਾਧੂ ਸੰਗਿ ਮਿਲਿ
ਜੋਤਿ ਪ੍ਰਗਟਾਵੈ ॥), the verse and its transliteration are split into one line per pada.
The salok's own ॥੧॥ is kept in the text, but the item is labelled “Salok” without a number, so that each
Ashtapadi does not show a “Salok 1”.

## 5. English (Dr. Sant Singh Khalsa)

Copied from the PDF; the lines of an item are joined into one paragraph in order (the reader shows a meaning as
one paragraph). Checked word by word against the same translation in the Shabad OS database (translation source
“Dr. Sant Singh Khalsa”): 18,755 words, 67 differences, all of them the PDF's own presentation (“Shalok:” where
the database has “Salok:”, its leading “- ” before a continuing sentence, capitals at the database's line
starts) except one extraction break, fixed: **“obtai n” → “obtain”** (Ashtapadi 15, pauri 5). Nothing else is
changed.

## 6. Our meanings and word meanings

The PDF has no Hindi, no Punjabi and no word meanings, so they are written for this library (`hi-scriptures`,
`pa-scriptures`; `library/glossary/pa.json`): 218 of 218 items and 2,536 of 2,536 distinct words. Our English
(`en-scriptures`, the default) is also written for this library from the Gurmukhi; the PDF's English stays
selectable (order 2), and the export stops if ours shares a run of 10 or more words with it.

### Readings settled with the commentaries

Our Hindi, English and Punjabi give one reading of every line. Where a line can be read more than one way, the
grammar decides, then Prof. Sahib Singh's Darpan and the Faridkot Teeka (read to check the reading only; our wording
is our own and the overlap check runs against the Darpan). Where both commentaries, or the grammar and one of them,
agree with our reading, it stands. These lines take the reading below:

| Line | Reading | Why |
|---|---|---|
| a01.p1 ਕੀਨੇ ਰਾਮ ਨਾਮ ਇਕ ਆਖੵਰ | the Vedas, Puranas and Simritis hold the one word of the Name the purest | ਸੁਧਾਖੵਰ is the predicate of ਕੀਨੇ; the Darpan |
| a01.rahao ਮਨਿ ਬਿਸ੍ਰਾਮ | it dwells in the devotees' minds | ਬਿਸ੍ਰਾਮ = abode (Darpan's gloss) |
| a02.salok ਨਾਨਕ ਕੇ … ਸਾਥ | O God, in Nanak's (the Guru's) company I have come to your refuge | no verb for "stay"; the Darpan |
| a04.p6 ਨਾਨਕ ਤੁਮਰੀ ਕਿਰਪਾ ਤਰੈ | a statement: Nanak crosses over by your grace alone | ਤਰੈ indicative; our Hindi |
| a04.p7 ਦ੍ਰਿੜੁ ਕਰਿ ਮਾਨੈ | he takes it all (his house of sand, Maya's games) to be lasting | the next line: death never comes to mind |
| a06.p5 ਨੀਕੀ ਜਾਤਿ | good birth | the Darpan: a good (human) birth; not caste |
| a07.p1 ਸਭੁ ਹੋਤ ਨਿਬੇਰਾ | everything is settled | ਸਭੁ; the Darpan |
| a07.p3 ਪਰਮਾਨੰਦਾ; ਬਨਿ ਆਈ | God, the supreme bliss; a deep bond of love forms between the Saadh and God | the Darpan |
| a07.p8 ਉਪਮਾ | likeness: the Saadh can be likened only to the all-pervading Lord | fits ਸਾਧ ਪ੍ਰਭ ਭੇਦੁ ਨ in line 10; the Darpan |
| a08.p1 ਪਾਵਕ ਕਾ ਸਹਜ ਸੁਭਾਉ | fire's nature to burn away all impurity | the stanza's theme (untainted); the Darpan |
| a10.p1 ਕਬਿ ਕਾਬਿ ਬੀਚਾਰਹਿ | poets reflect on poetry | both commentaries |
| a10.p2, a15.p3, a16.p6, a17.p7, a22.p4 | second person, causative, ਕਰਮੁ = grace, singular, a relative clause | the Gurmukhi's grammar (our Hindi aligned) |
| a02.p7, a16.p8, a21.p5 | through the Lord's glory; one (not I) is struck with awe; says Nanak, you alone know | the three languages on the English's reading |
| a11.salok ਮਹੀਅਲਿ | the space between earth and sky | ਮਹੀ + ਤਲਿ |
| a11.p8 ਬਸਹਿ | plural | the verb; the Darpan |
| a12.p5 ਮਾਇਆ ਪਾਛੈ ਪਾਵੈ | he keeps storing up Maya | the Darpan |
| a12.p8 ਸਚੁ … ਸਭੁ ਕੀਨਾ | all that he has made is true | the Darpan |
| a13.p7 ਜੈਸਾ ਭਾਵੈ | as one's inclination is, so one becomes | the next line: past deeds cannot be erased; the Darpan |
| a14.p3 ਹਰਿ ਮੁਖੀ | the eminent ones who utter the Lord | ਮੁਖੀ with the plural ਬੋਲਹਿ; the Darpan |
| a14.p7 ਕ੍ਰਿਪਾ ਕਰਹਿ | God bestows grace | both commentaries |
| a15.p5 ਮਨ ਮੋਲਿ | at the price of your mind | ਮੋਲਿ; the Darpan |
| a16.p7 ਅਵਰ ਨ ਬੂਝਿ | know that no other takes thought for it | ਬੂਝਿ imperative after ਜਿਸ ਕੀ ਸ੍ਰਿਸਟਿ ਸੁ ਕਰਣੈਹਾਰੁ; the Darpan |
| a18.p3 ਗੁਰ ਕਾ ਮਨੁ ਮਾਨੈ | one with whom the Guru's mind is wholly satisfied | both commentaries |
| a18.p7 ਜਪਿ ਨਾਮੁ | by repeating the Name (stability is found) | parallel to ਸੁਨਿ in line 10; the Darpan |
| a19.p4 ਤਤੁ ਬੀਚਾਰੁ ਕਹੈ ਜਨੁ ਸਾਚਾ | one who speaks reflection on the Essence is the true servant | both commentaries |
| a20.p5 ਨਾਮੁ … ਗੁਨਤਾਸੁ | the Naam is the treasure of virtues | ਗੁਨਤਾਸੁ beside ਨਾਮੁ; the Darpan |
| a21.p8 ਜਹ ਅਬਿਗਤੁ ਭਗਤੁ ਤਹ ਆਪਿ | where the Unmanifest is, there is his devotee; where the devotee, there he is | ਅਬਿਗਤੁ is nominative; the Darpan |
| a24.p6 ਗੁਰ ਨਾਨਕ ਨਾਮ ਬਚਨ | O Nanak, the Guru's word and the Naam | ਗੁਰ with ਬਚਨ, ਨਾਨਕ the signature; the Darpan |
| a24.salok | first person: I have worshipped, I have found | our Hindi; Faridkot |

ਨਾਨਕ in the last line follows `tools/meanings/style.md` §12.
