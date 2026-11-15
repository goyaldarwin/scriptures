# Praśna Upaniṣad (प्रश्नोपनिषद्)

Shelf: हिन्दू धर्म › वेद › अथर्ववेद › उपनिषद् › प्रश्नोपनिषद् (`library/hinduism/veda/atharvaveda/upanishad/prashna-upanishad/`, work id `prashna-upanishad`). The Upaniṣad of the Atharvaveda in which six seekers put six questions to the sage Pippalāda: six praśnas, 67 mantras (16 + 13 + 12 + 11 + 7 + 8), with the śānti mantra भद्रं कर्णेभिः before them and each praśna's closing words after it.

## Sources
- **Text:** shlokam.org, "Prashnopanishad" (<https://shlokam.org/text/prashnopanishad.htm>), a page the owner allowed, saved as HTML. The private copy is in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/printouts/shlokam/prashnopanishad.html`. Its Devanagari is the base; its own transliteration, Śaṅkara's commentary as the page gives it, and five web texts check it: upanishads.org.in, Sanskrit Wikisource and the Vedic Heritage Portal (copies of the base's own text), IIT Kanpur's Heritage reader and GRETIL with Śaṅkara's bhāṣya (the independent witnesses); their raw downloads are in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/printouts/<site>/`. The page's slips are corrected where the grammar or the sense shows them and the witnesses give the right form. Every choice is in `reconciliation.md`. The page has no svara marks, so neither does the text.
- **Meanings:** written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, following Śaṅkara's reading, checked against his bhāṣya (IIT Kanpur's Sanskrit, with GRETIL's). Other readings and brief context are in the footnotes (`notes`). The English on the shlokam.org page (Swami Sivananda's and Max Müller's translations, S. Sitarama Sastri's translation of the bhāṣya) was read only to check a reading; our meanings share no run of ten words with it (`tools/meanings/overlap.py`). The readings that were weighed are in `reconciliation.md`.
- **Word meanings:** written for this library, in `library/glossary/sa.json`.
- **Audio:** SMVedroad, "Prashnopanishad Chant | With Lyrics" (YouTube `AtgMYxZFzKo`, 27 min 53 s), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/audio/smvedroad/AtgMYxZFzKo.opus`. Transcribed by Whisper (`audio/smvedroad/transcripts/`); every verse's start and end come from Meta's MMS forced aligner on the known text (`tools/audio/METHOD.md`; `mms/`, `aligned.json`, `aligned.md`): all 74 items have a start, not yet scored against starts set by ear. It sings the whole text in this order: the śānti from 1:00 (the transcript has no words before it), then the six praśnas, each with its closing words. What it adds is not a text and is left untimed: its announcement of each praśna (अथ प्रथमः प्रश्नः …) and समाप्ता च प्रश्नोपनिषत् after 6.iti; it does not sing the śānti again at the end. The to-check list is the 14 verses the automatic checks flag (`check.json`); the owner's starts set by ear always win.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <the saved page>` → `source/page_raw.json`: each verse block's Devanagari and transliteration lines, as the page has them (the page's English and commentary are not kept here).
- `source/settle.py` → `text.txt`: compares the page's Devanagari with its transliteration (it fails on a difference not listed), applies the corrections (`FIX`), makes each praśna's closing words an item, writes the mantra numbers, lays out the śānti as the Māṇḍūkya's (and checks it is the same), and writes the topics.
- `source/witnesses.py <printouts/ of the work in a scriptures-data clone>` → `source/witness/<site>.txt`: each web witness as a Devanagari text (GRETIL's IAST converted), divided by praśna, in `check.py`'s format.
- `source/check.py`: compares every praśna of `text.txt` with every witness word for word; it fails on a difference not listed in its `READING` (each settled in `reconciliation.md`).
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `text.txt`: the settled text, one verse per mantra, in Devanagari; the export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).

Rebuild: `python3 tools/works/prashna-upanishad/source/settle.py && python3 tools/works/prashna-upanishad/source/check.py && python3 tools/works/export.py prashna-upanishad && python3 tools/site/build.py`. Run `extract.py` again only if the saved page changes, and `witnesses.py` only if a witness's download does.

## Structure
- **Parts:** the six praśnas (प्रथम प्रश्न … षष्ठ प्रश्न, keys `1` … `6`).
- **Sections (pages):** one per praśna (`p1` … `p6`), plus `shanti` (the opening, in part 1).
- **Hierarchy:** six praśnas (parts) › one section each › mantras.
- **Items:** `shanti.1`; `1.1` … `6.8`; `1.iti` … `6.iti`. Ids are permanent.
- **Numbering:** a mantra's `n` is its number within its praśna, as the page prints it at its end (the page prints ॥ १.१॥; the text writes the mantra's own number, ॥१॥, as the Kaṭha does); it is cited praśna.mantra (`work.json` → `cite`: Mantra 3.5). The śānti and the closing words have none.
- **Types:** `shanti` (शा॰ / Shan.), `mantra` (मं॰ / Man.), `iti` (समापन (पुष्पिका) / Closing words (iti)), as the Māṇḍūkya's.
- **Topics:** the śānti pāṭha and one per praśna, with the praśna's question in our words.
- **Reading plans:** none; the Upaniṣad is read in one or two sittings.
