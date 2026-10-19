# Sundarakāṇḍa (standalone work, with the Hanumān Chālīsā and āratī)

Shelf: हिन्दू धर्म › ग्रन्थ › गोस्वामी तुलसीदास › सुन्दरकाण्ड (`library/hinduism/granth/tulsidas/sundarkand/`, work id `sundarkand`), next to the Śrī Rāmacaritamānasa.

The Sundarakāṇḍa is the most often recited part of the Mānas, so it is also a work of its own, read in one sitting and followed, as it usually is in practice, by the Śrī Hanumān Chālīsā and the āratī "आरती कीजै हनुमान लला की". It has five parts: प्रारम्भिक वन्दना (the opening prayers sung in the recording), किष्किन्धाकाण्ड (अन्तिम अंश) (the lead-in from Kiṣkindhā dohā 29), सुन्दरकाण्ड, श्रीहनुमानचालीसा, आरती. It has no reading plans.

## Part 0: the opening prayers

What Pt. Ashwin Kumar Pathak's recording sings before the text: ॐ श्री परमात्मने नमः, the Gaṇeśa ślokas वक्रतुण्ड… and विघ्नेश्वराय…, ॐ again, and the Mānas's sorathā प्रनवउँ पवनकुमार (`bal.17.so17`, pulled from the Mānas by `[manas bal.17.so17]` in `text.txt`, so it is the Mānas's own, with its Gita Press meanings). Section `mangal`, items `mangal.mantra1`, `mangal.shloka1`, `mangal.shloka2`, `mangal.mantra2`, `bal.17.so17`. Sources and choices: `reconciliation.md`. `work.json` → `prepended` (5) keeps readers' older saved places on the same verse (`docs/LIBRARY.md`).

## Parts 1 and 2 are generated from the Mānas, never copied by hand

`export.py` reads `library/hinduism/granth/tulsidas/ramcharitmanas/work.json` and takes every item of the Mānas's Sundara-kāṇḍa part with everything it has: the same ids (`sundar.12.cau3`), sections `s` (dohā numbers, so pages are labelled "Dohā 12" as in the Mānas), types, numbers, verse lines, transliteration and language (`sa` for the three opening ślokas). It takes that part's topics, and the Gita Press Hindi and English meanings of those items from the Mānas's `meanings/hi-gitapress.json` and `en-gitapress.json`, under the same source ids and titles. The Mānas has no closing colophon item for the kāṇḍa, so there is none here either.

**So a correction to the Mānas reaches the Sundarakāṇḍa on the next rebuild.** Fix the Mānas as usual (`docs/HOW-TO.md` → "Fix a word or meaning in the Rāmacaritamānasa"), then run:
```bash
python3 tools/works/ramcharitmanas/export.py
python3 tools/works/sundarkand/export.py
python3 tools/works/sundarkand/check.py     # the Sundarakāṇḍa items, topics and Gita Press meanings equal the Mānas's
python3 tools/site/build.py
```
Never edit `library/hinduism/granth/tulsidas/sundarkand/` by hand. The Mānas itself is not touched: this work only reads it.

Readers' bookmarks, notes and progress are stored per work id, so those made in the Sundarakāṇḍa stay separate from those made in the Mānas, even though the item ids are the same.

## Parts 3 and 4: the Hanumān Chālīsā and the āratī

- `text.txt`: their verse text, section by section. `reconciliation.md` records the sources and every choice.
  - Chālīsā (language `awa`, Tulasīdāsa's Awadhi): the two opening dohās (`chalisa.do1`, `do2`), the 40 caupāīs (`chalisa.cau1`–`cau40`, one item per numbered line, following the usual numbering 1–40 in which each line of two half-lines is one caupāī), and the closing dohā (`chalisa.do3`). Types `do` and `cau` are the Mānas's own. Sections: `chalisa-do`, `chalisa-cau`, `chalisa-ant`.
  - Āratī (language `hi`): the refrain (`aarti.tek`, type `tek` = टेक) and six stanzas of two lines each (`aarti.pad1`–`pad6`, type `pad`). Both types are declared in `work.json` → `types`. In singing, the refrain is repeated after every stanza; the text shows it once.
- `translit.py`: the Roman transliteration of these verses, in the Mānas's own style (checked against the Mānas: `python3 tools/works/sundarkand/translit.py --check`).
- `meanings/hi.json`, `en.json`: one meaning per verse, written for this library, because the owner gave no source for these two texts → sources `hi-scriptures` and `en-scriptures` (`order: 2`). A reader who has Gita Press selected sees them for these verses, tagged with the source's name, because Gita Press does not cover them.
- `glossary/awa.json`, `hi.json`: the word meanings of the Chālīsā (Awadhi) and the āratī (Hindi) that the shared dictionaries did not have yet. The exporter adds them to `library/glossary/<lang>.json` and never changes an existing word. It stops if any word of any verse has no meaning in its language or its fallback (Sanskrit).

## Audio

`audio/ashwin-pathak/`: Pt. Ashwin Kumar Pathak's recording (YouTube `QjSpUgnEPLU`), not transcribed or timed yet. Follow `docs/HOW-TO.md` → "Add a new audio source". When it is transcribed, compare the Chālīsā and āratī as sung with `text.txt` (see the open points in `reconciliation.md`).
