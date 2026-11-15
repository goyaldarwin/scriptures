# Puruṣa Sūkta (पुरुषसूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › आरण्यक › पुरुषसूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/purusha-suktam/`, work id `purusha-suktam`). The text is the Taittirīya Āraṇyaka's Puruṣa Sūkta: anuvāka 3.12 (eighteen mantras) and the Uttaranārāyaṇa, 3.13 (six), with the śānti pāṭha तच्छं योरावृणीमहे.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram sits at `…/krishna-yajurveda/samhita/`. This is the Āraṇyaka's form of the sūkta, not the Ṛgveda's (10.90): the page has the Uttaranārāyaṇa, which it heads उत्तरनारायणम्, and Sanskrit Wikisource's Taittirīya Āraṇyaka has the same eighteen mantras as its anuvāka 3.12 and the six as 3.13, tagged उत्तरनारायणः (`reconciliation.md`). So it goes on a new Āraṇyaka shelf of the Kṛṣṇa Yajurveda, beside the Nārāyaṇa and Durgā Sūktas, all three of the Taittirīya Āraṇyaka, and the Yajurveda's writing of the anusvāra (ꣳ) applies. The Vaiṣṇava Pañca Sūkta (Puruṣa, Nārāyaṇa, Śrī, Bhū, Nīlā) is to be a work of its own that takes these verses (`[take purusha-suktam …]`, as the Sundarakāṇḍa takes the Mānas's), so the grouping does not move any sūkta from its Veda.

## Sources
- **Text (source of truth).** shlokam.org's page [Purusha Suktam](https://shlokam.org/shloka/purusha-suktam.htm), saved as HTML. The private copy is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/purusha-suktam/printouts/shlokam/purusha-suktam.html`. The Devanagari, with its svaras, follows the page exactly, except for its two headings and the four corrections in `reconciliation.md`; the page's own transliteration is the second witness of every line.
- **Recording.** Sri Sathya Sai Official, YouTube `TngWQ6zweBc` (498.9 s), whose downloaded file names it "Full Purusha Suktam With Lyrics, Ancient Vedic Chants In Sanskrit, Powerful Mantra". `audio/sri-sathya-sai/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/purusha-suktam/audio/sri-sathya-sai/TngWQ6zweBc.opus`. Not yet transcribed or timed (a draft). What it sings is known here only from its title ("Full": the whole sūkta); whether it sings the Uttaranārāyaṇa and the śānti pāṭha, in what order, and any opening the page lacks, the transcript will show; an opening it sings is then added as text from a written witness (PLAYBOOK §3).
- **Meanings, word meanings, introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <purusha-suktam.html>` → `source/purusha-suktam_raw.json`: the page's verse blocks (Devanagari and transliteration). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: the settled text, with the corrections (`FIX`), the page's headings left out (`HEADING`), the lines where the page's two scripts differ (`WITNESS`), the sections and our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `tools/works/shlokam.py`, shared by the six Sūktas: reads a shlokam.org page's HTML, converts its transliteration to Devanagari and compares the two. The Śrī Rudram (from PDF printouts) and the Taittirīya Upaniṣad have helpers of their own doing the same; the Sūktas share one because their pages are alike.
- `audio/sri-sathya-sai/`: `source.json`, `recordings.json`.

Rebuild: `python3 tools/works/purusha-suktam/source/settle.py && python3 tools/works/export.py purusha-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › three sections (`purusha`: mantras 1–18, TA 3.12; `uttara`: mantras 19–24, the Uttaranārāyaṇa, TA 3.13; `shanti`: the śānti pāṭha) › mantras.
- **Numbering:** the page prints no numbers; a mantra's `n` is the page's own verse number (1–24, running on through the Uttaranārāyaṇa), and it is cited by it (Mantra 19). The śānti pāṭha has none.
- **Items:** `m01`–`m24` (type `mantra`), one per ṛk as the page divides them (`m24`, ह्रीश्च ते, is the anuvāka's closing prose in three lines), and `shanti.end` (type `shanti`, तच्छं योः, which the page gives after the sūkta). 25 items. Ids are permanent.
- **Types** (`work.json` → `types`): mantra (मं॰ / Man.), śānti mantra (शा॰ / Shan.).
- **Topics** (ours): the Person of a thousand heads (1), the sacrifice of the Person and creation (6), knowing the Person (16), Uttara Narayana (19), Shanti Paath.
- **Reading plans:** none; the sūkta is recited in one sitting.
