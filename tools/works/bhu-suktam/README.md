# Bhū Sūkta (भूसूक्तम्)

Shelf: हिन्दू धर्म › वेद › अथर्ववेद › संहिता › भूसूक्तम् (`library/hinduism/veda/atharvaveda/samhita/bhu-suktam/`, work id `bhu-suktam`). The text is shlokam.org's "Bhoomi Suktam": eighteen verses of the Atharvaveda's Pṛthivī Sūkta (12.1, the hymn to the Earth), numbered 1–18 as the page prints them.

**Why this shelf.** A Vedic text sits by its Veda and division (`docs/LIBRARY.md` §1), as the Śrī Rudram does. The page's text is the Atharvaveda's Pṛthivī Sūkta (its first verse, सत्यं बृहदृतमुग्रं दीक्षा तपो ब्रह्म यज्ञः पृथिवीं धारयन्ति, opens Atharvaveda 12.1; Hindupedia's "Bhusukta" names two Bhū Sūktas, Atharvaveda Saṃhitā 12.1 and Taittirīya Saṃhitā 1.5.3), so it goes on a new Saṃhitā shelf of the Atharvaveda, beside its Upaniṣads. The id `bhu-suktam` is the work's name in the Vaiṣṇava Pañca Sūkta, which is to be a work of its own that takes these verses.

**The text and the recording may differ.** The Bhū Sūkta of the Vaiṣṇava Pañca Sūkta is usually the Taittirīya one (Hindupedia: "the one from the Taittirīya Samhitā is better known of the two"); shlokam.org has only the Atharvaveda's. The recording is titled "Bhu Suktam", not "Bhoomi Suktam", and is short (164.5 s). If its transcript shows it sings the Taittirīya Bhū Sūkta, the text is to be taken from a written witness of that sūkta (sanskritdocuments.org, which the owner supplies) and the work moves to the Kṛṣṇa Yajurveda's shelf (moving a work keeps readers' places, `docs/LIBRARY.md` §1); the ids here are not yet published.

## Sources
- **Text (source of truth).** shlokam.org's page [Bhoomi Suktam](https://shlokam.org/shloka/bhoomi-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/atharvaveda/samhita/bhu-suktam/printouts/shlokam/bhoomi-suktam.html`. The page has no svaras, so neither does the text. The Devanagari follows the page exactly, except for the one correction in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Recording.** Soul Sadhana, YouTube `RBrq8UeM1N4` (164.5 s), whose downloaded file names it "Bhu Suktam Lyrics Meaning, Soul Sadhana". Audio source id `soul-sadhana`: `audio/soul-sadhana/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/bhu-suktam/audio/soul-sadhana/RBrq8UeM1N4.opus`. Not yet transcribed or timed (a draft). What it sings is known here only from its title; which Bhū Sūkta it sings, how much of it, in what order, and any opening, the transcript will show (above).
- **Meanings, word meanings, introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <bhoomi-suktam.html>` → `source/bhoomi-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two (the Śrī Rudram's and the Taittirīya Upaniṣad's method, with one helper for the six alike pages).
- `audio/soul-sadhana/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/bhu-suktam/source/settle.py && python3 tools/works/export.py bhu-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › one section (`sukta`) › mantras.
- **Numbering:** each mantra's `n` is the number the page prints at its end (॥१॥ … ॥१८॥), and it is cited by it (Mantra 12). These are the page's numbers, not the verse numbers of Atharvaveda 12.1.
- **Items:** `m01`–`m18` (type `mantra`). 18 items. Ids are permanent once published.
- **Types** (`work.json` → `types`): mantra (मं॰ / Man.).
- **Topics** (ours): truth, order and austerity uphold the Earth (1); the Earth is my mother, I her son (10).
- **Reading plans:** none.
