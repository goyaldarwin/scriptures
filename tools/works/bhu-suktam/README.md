# Bhū Sūkta (भूसूक्तम्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › संहिता › भूसूक्तम् (`library/hinduism/veda/yajurveda/krishna-yajurveda/samhita/bhu-suktam/`, work id `bhu-suktam`). The text is the Taittirīya Saṃhitā's Bhū Sūkta, 1.5.3.1–2 (भूमिर्भूम्ना द्यौर्वरिणा … इह मादयन्ताम्): seven ṛks, the Bhū Sūkta of the Vaiṣṇava Pañca Sūkta, as the recording sings it.

**Why this shelf.** A Vedic text sits by its Veda, śākhā and division (`docs/LIBRARY.md` §1), as the Śrī Rudram sits at `…/krishna-yajurveda/samhita/`: the sūkta is the Taittirīya Saṃhitā's, so it sits beside the Śrī Rudram and the Nīlā Sūkta. Hindupedia's "Bhusukta" names two Bhū Sūktas, Atharvaveda 12.1 (the Pṛthivī Sūkta, the only one on shlokam.org) and Taittirīya Saṃhitā 1.5.3, the better known; the recording sings the Taittirīya one (its transcript), and a written witness of it is at hand, so the text is that one (`reconciliation.md`). The Vaiṣṇava Pañca Sūkta (Puruṣa, Nārāyaṇa, Śrī, Bhū, Nīlā) is to be a work of its own that takes these verses.

## Sources
- **Text (source of truth).** Sanskrit Wikisource's Taittirīya Saṃhitā, kāṇḍas 1–4, with svaras ([तैत्तिरीयसंहिता-१-४](https://sa.wikisource.org/wiki/तैत्तिरीयसंहिता-१-४), no edition named), its raw wikitext in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/samhita/bhu-suktam/printouts/wikisource/तैत्तिरीयसंहिता-१-४.wiki.txt`. The words and svaras follow the page exactly; the recording's ॐ and closing śānti are added (`reconciliation.md`).
- **Not used:** shlokam.org's page "Bhoomi Suktam" (Atharvaveda 12.1, eighteen verses), kept in scriptures-data at `…/bhu-suktam/printouts/shlokam/`: it is not the sūkta the recording sings.
- **Recording.** Soul Sadhana, YouTube `RBrq8UeM1N4` (164.5 s), whose downloaded file names it "Bhu Suktam Lyrics Meaning, Soul Sadhana". Audio source id `soul-sadhana`: `audio/soul-sadhana/` (`source.json`, `recordings.json`); the private speech-quality copy is in scriptures-data at `…/bhu-suktam/audio/soul-sadhana/RBrq8UeM1N4.opus`. Transcribed (`transcripts/`), not yet timed (a draft). It sings ॐ, the seven ṛks and the śānti.
- **Word meanings:** every word, in the shared dictionary (`library/glossary/sa.json`; the readings decided: `reconciliation.md`, "Word meanings").
- **Meanings.** Written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, from the mantra's words, their grammar and Monier-Williams and Apte; no reading is put to any commentator (Sāyaṇa's commentary is not at hand). Brief context and well-known second readings are in the footnotes (`notes`); the readings decided are in `reconciliation.md`, "Meanings". No published English of this text is at hand to audit our meanings against (shlokam.org's Bhoomi Suktam English is the Atharvaveda's hymn, another text), so its batches have the review and the dictionary check without a copy audit (`apply_batches.py --steps review,dict`).
- **Introduction:** not written yet.

## Files
The folder's format: `tools/works/README.md`.
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `source/extract.py <dir>` → `source/ts-1.5.3_raw.txt`: the passage from the page's raw wikitext (its private-use font characters read as `tools/works/sukta_witness.py` → `PUA` says). Run it again only if the page changes.
- `source/settle.py` → `text.txt`: one item per ṛk, its lines at the page's daṇḍas, the recording's ॐ and closing śānti, our topic headings; `tools/site/regen_check.py` runs it. The export writes it by the library's standard (ꣳ, a Yajurveda text) and makes the transliteration (PLAYBOOK §3).
- `source/witnesses.py <dir>` → `source/witness/wikisource-ts.txt`, and `source/check.py`: proves the text keeps the page's words and svaras (`tools/works/sukta_witness.py`, shared by the six Sūktas).
- `audio/soul-sadhana/`: `source.json`, `recordings.json`, `transcripts/`.

Rebuild: `python3 tools/works/bhu-suktam/source/settle.py && python3 tools/works/export.py bhu-suktam && python3 tools/site/build.py`.

## Structure
- **Hierarchy:** one part (the sūkta) › two sections (`sukta`: the seven ṛks; `end`: the śānti) › items.
- **Numbering:** the page prints no numbers within the passage; each ṛk's `n` is its place, 1–7, as the page ends each with ।।, and it is cited by it (Mantra 5).
- **Items:** `m01`–`m07` (type `mantra`), `shanti.end` (type `shanti`). 8 items. Ids are permanent once published.
- **Types** (`work.json` → `types`): mantra (मं॰ / Man.), śānti mantra (शा॰ / Shan.).
- **Topics** (ours): Earth, sky and mid-air; the fire laid down (1); kindling again the fire scattered in anger (5); Shanti Paath.
- **Reading plans:** none.
