# Praśna Upaniṣad (प्रश्नोपनिषद्)

Shelf: हिन्दू धर्म › वेद › अथर्ववेद › उपनिषद् › प्रश्नोपनिषद् (`library/hinduism/veda/atharvaveda/upanishad/prashna-upanishad/`, work id `prashna-upanishad`). The Upaniṣad of the Atharvaveda in which six seekers put six questions to the sage Pippalāda: six praśnas, 67 mantras (16 + 13 + 12 + 11 + 7 + 8), with the śānti mantra भद्रं कर्णेभिः before them and each praśna's closing words after it.

## Sources
- **Text:** shlokam.org, "Prashnopanishad" (<https://shlokam.org/text/prashnopanishad.htm>), a page the owner allowed, saved as HTML. The private copy is in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/printouts/shlokam/prashnopanishad.html`. Its Devanagari is the base; its own transliteration, Śaṅkara's commentary as the page gives it, and five web texts check it: upanishads.org.in, Sanskrit Wikisource and the Vedic Heritage Portal (copies of the base's own text), IIT Kanpur's Heritage reader and GRETIL with Śaṅkara's bhāṣya (the independent witnesses); their raw downloads are in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/printouts/<site>/`. The page's slips are corrected where the grammar or the sense shows them and the witnesses give the right form. Every choice is in `reconciliation.md`. The page has no svara marks, so neither does the text.
- **Meanings:** not written yet.
- **Word meanings:** not written yet.
- **Audio:** SMVedroad, "Prashnopanishad Chant | With Lyrics" (YouTube `AtgMYxZFzKo`, 27 min 53 s), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/audio/smvedroad/AtgMYxZFzKo.opus`. Not transcribed or timed yet. The video's title and description name the Upaniṣad, the singers and the channel's other Upaniṣads, and say nothing of its order or of an opening; whether it chants the whole text, in the page's order, and what it sings before 1.1 and after 6.8 is read from its transcript when it is timed (an opening it sings that the text lacks is added then, from a written witness).

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <the saved page>` → `source/page_raw.json`: each verse block's Devanagari and transliteration lines, as the page has them (the page's English and commentary are not kept here).
- `source/settle.py` → `text.txt`: compares the page's Devanagari with its transliteration (it fails on a difference not listed), applies the corrections (`FIX`), makes each praśna's closing words an item, writes the mantra numbers, lays out the śānti as the Māṇḍūkya's (and checks it is the same), and writes the topics.
- `source/witnesses.py <printouts/ of the work in a scriptures-data clone>` → `source/witness/<site>.txt`: each web witness as a Devanagari text (GRETIL's IAST converted), divided by praśna, in `check.py`'s format.
- `source/check.py`: compares every praśna of `text.txt` with every witness word for word; it fails on a difference not listed in its `READING` (each settled in `reconciliation.md`).
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
