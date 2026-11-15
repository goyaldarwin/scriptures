# Aitareya Upaniṣad (ऐतरेयोपनिषद्)

Shelf: हिन्दू धर्म › वेद › ऋग्वेद › उपनिषद् › ऐतरेयोपनिषद् (`library/hinduism/veda/rigveda/upanishad/aitareya-upanishad/`, work id `aitareya-upanishad`). The Upaniṣad of the Ṛgveda's Aitareya Āraṇyaka, in prose: three adhyāyas, the first of three khaṇḍas, 33 mantras (4 + 5 + 14, 6, 4), with the Ṛgveda's śānti mantra वाङ् मे मनसि before them.

## Sources
- **Text.** The owner's book: Swami Gurubhaktananda, *Aitareya Upanishad* (The Sandeepany Experience, Text 34; web edition 2019, chinfo.org), the Kaṭha's series and typesetting. The private copy is in scriptures-data at `<work path>/books/sandeepany/aitareya-upanishad-gurubhaktananda.pdf`. As for the Kaṭha, its Devanagari is in a legacy font, so the text is taken from the book's **IAST transliteration** (`source/extract.py`, with the Kaṭha's decoding of the font's symbols) and converted letter for letter to Devanagari (`source/settle.py`, with the Kaṭha's `iast2deva`). The result is checked against three Devanagari witnesses (`source/check.py`, `source/witness/`): the owner's printout of sanskritdocuments.org (all 33 mantras and the śānti, read on its page images), upanishads.org.in (Sri Aurobindo's text, one page per mantra) and IIT Kanpur's Heritage reader. The slips in the book's transliteration are corrected, each where the book's own word-by-word, the grammar or the text's own parallel lines show the right form and witnesses have it; many of them are shared by sanskritdocuments.org, which prints the same edition. Every decision is in `reconciliation.md`.
- **Meanings.** Written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), one piece per verse line, following Śaṅkara's reading, other readings and brief context in the footnotes (`notes`); written, reviewed, copy-audited and checked again against the verse by separate agents (`docs/HOW-TO.md`, "Write our own meanings for a Sanskrit work"). The book's English is read only for the copy audit (it shares no run of ten words with ours); it is not in this repository. The readings settled: `reconciliation.md`, "Meanings".
- **Word meanings.** Written for this library, in `library/glossary/sa.json`, with this work's own senses in `glossary/sa.json`.
- **Introduction:** not written yet.
- **Audio.** SMVedroad, “Aitariya Upanishad Chant | ऐत्तरेय उपनिषद् गान | With Lyrics” (YouTube `Qd8l9Am5JRU`, 19 min), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `<work path>/audio/smvedroad/`. Its title and description name no structure (the description lists the channel's other Upaniṣad recordings), so whether it chants the śānti before the text or after it, and every mantra, is read from its transcript when it is timed. Not transcribed or timed yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <the PDF>` → `source/pdf_raw.json`: each mantra's transliteration lines, decoded (and the śānti's). Needs PyMuPDF: the book sets the Devanagari and the transliteration side by side, so the transliteration is read by its font (BRH Latin).
- `source/settle.py` → `text.txt`: the settled text, one verse per mantra, in Devanagari, with the topics; the export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).
- `source/witnesses.py <printouts folder>` → `source/witness/upanishads-org.txt`, `source/witness/iitk.txt`, from the raw downloads in scriptures-data; `source/witness/sanskritdocuments-full.txt` is the printout read on its page images (its text layer scrambles the vowel signs).
- `source/check.py`: every witness verse must have the same letters as `text.txt` (only the differences in `reconciliation.md` are allowed). Run it after any change to the text.

Rebuild: `python3 tools/works/aitareya-upanishad/source/settle.py && python3 tools/works/aitareya-upanishad/source/check.py && python3 tools/works/export.py aitareya-upanishad && python3 tools/site/build.py`. Run `extract.py` again only if the PDF changes.

## Structure
- **Parts:** प्रथम अध्याय, द्वितीय अध्याय, तृतीय अध्याय.
- **Sections (pages):** the five khaṇḍas (`k1.1`, `k1.2`, `k1.3`, `k2.1`, `k3.1`), plus `shanti` (opening).
- **Hierarchy:** three adhyāyas (parts) › khaṇḍas (sections: three in the first, one each in the second and third) › mantras.
- **Items:** `shanti.1`; `1.1.1` … `3.1.4`.
- **Numbering:** a mantra's `n` is its number within the khaṇḍa (॥१॥); it is cited adhyāya.khaṇḍa.mantra, the standard numbering (`work.json` → `cite`: Mantra 1.3.12), as the Kaṭha is. The book numbers its own six "chapters" (1–3 the first adhyāya's khaṇḍas, 4 and 5 the second and third adhyāyas, 6 the śānti) and splits 3.1.3 in two ("5.3A", "5.3B"); its numbers are not used.
- **Types:** `shanti` (शा॰ / Śā.) and `mantra` (मं॰ / Man.).
- **Topics:** one per khaṇḍa with its theme, plus the śānti pāṭha.
- **The śānti:** the book prints it once, after 3.1.4, as its chapter 6; here it opens the work, as in the library's other Upaniṣads and in sanskritdocuments.org, and is not repeated at the end (PLAYBOOK §11).
- **Reading plans:** none; the Upaniṣad is read in one sitting.
