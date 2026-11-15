# Taittirīya Upaniṣad (तैत्तिरीयोपनिषद्)

Shelf: हिन्दू धर्म › वेद › यजुर्वेद › कृष्ण यजुर्वेद › उपनिषद् › तैत्तिरीयोपनिषद् (`library/hinduism/veda/yajurveda/krishna-yajurveda/upanishad/taittiriya-upanishad/`, work id `taittiriya-upanishad`). The Upaniṣad of the Taittirīya śākhā of the Kṛṣṇa Yajurveda, in three vallīs: the Śīkṣāvallī (12 anuvākas), the Brahmānandavallī (9) and the Bhṛguvallī (10), 31 anuvākas in all.

## Sources
- **Text.** The shlokam.org page <https://shlokam.org/text/taittiriya-upanishad.htm>, the source the owner allowed. The private copy (the page's HTML, fetched 2026-11-14) is in scriptures-data at `<work path>/printouts/shlokam/taittiriya-upanishad.html`. The page gives the Devanagari and its own transliteration for every paragraph; it has no svaras, so neither does the text. The transliteration is the second witness of the Devanagari, line by line; five web witnesses are compared with every paragraph (`reconciliation.md`, "Witnesses"). Every correction, and why, is in `reconciliation.md`. The page's English translation and its headings are not in this repository.
- **Meanings.** Written for this library (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`), line by line, following Śaṅkara's reading, checked against his bhāṣya (IIT Kanpur's Sanskrit, with GRETIL's). Other readings and brief context are in the footnotes (`notes`). The English on the shlokam.org page and Swami Gambhirananda's translation (IIT Kanpur) were read only to check a reading; our meanings share no run of ten words with either (`tools/meanings/overlap.py`). The readings that were weighed are in `reconciliation.md`, "Meanings".
- **Word meanings.** Written for this library, in `library/glossary/sa.json`.
- **Introduction.** Not yet written.
- **Audio.** SMVedroad, "Taitiriya Upanishad Chant | तैत्तिरीय उपनिषद् गान | With Lyrics" (YouTube `YQ7K4wGDZlg`, 44 min 31 s), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `<work path>/audio/smvedroad/YQ7K4wGDZlg.opus`. Transcribed by Whisper (`audio/smvedroad/transcripts/`); every verse's start and end come from Meta's MMS forced aligner on the known text (`tools/audio/METHOD.md`; `mms/`, `aligned.json`, `aligned.md`): all 56 items have a start, not yet scored against starts set by ear. It sings the whole text in this order, with the vallīs' opening सह नाववतु and not the one the page prints again at their end. The to-check list is the verses the automatic checks flag (`check.json`); the owner's starts set by ear always win.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <the page's HTML>` → `source/taittiriya_raw.json`: each verse block's reference (vallī.anuvāka.paragraph, as the page numbers it), its Devanagari lines and its transliteration lines, split at the page's line breaks.
- `source/taittiriya_text.py`: the page's transliteration back to Devanagari (`tr2deva`), the second witness, and the key both are compared by.
- `source/witnesses.py <printouts folder of a scriptures-data clone>` → `source/witness/<site>.txt`: the five web witnesses (IIT Kanpur, upanishads.org.in, Wikisource, the Vedic Heritage Portal, GRETIL) in one format.
- `source/check.py`: compares every anuvāka of `text.txt` with every witness; the only differences allowed are the ones in `source/witness-readings.tsv` (`reconciliation.md`, "Witnesses").
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: our meanings, with footnotes (`notes`).
- `source/settle.py` → `text.txt`: compares the two scripts of every line (only the lines named in `WITNESS` may differ, all in how they write the pluta), applies the corrections (`FIX`), leaves out the page's headings, and writes the settled text, one item per paragraph, with the parts, sections and our topic headings. The export writes it by the library's standard and makes the transliteration (PLAYBOOK §3).

Rebuild: `python3 tools/works/taittiriya-upanishad/source/settle.py && python3 tools/works/export.py taittiriya-upanishad && python3 tools/site/build.py`. Run `extract.py` again only if the page changes.

## Structure
- **Hierarchy:** three vallīs (parts) › anuvākas (sections) › paragraphs (items).
- **Parts:** शीक्षावल्ली, ब्रह्मानन्दवल्ली, भृगुवल्ली (keys `1`, `2`, `3`). The Śīkṣāvallī is spelt as the page and its text spell it (इत्युक्तः शीक्षाध्यायः, इति शीक्षावल्ली समाप्ता).
- **Sections (pages):** each anuvāka is a page (`a1.1` … `a1.12`, `a2.1` … `a2.9`, `a3.1` … `a3.10`). The Brahmānanda- and Bhṛguvallī open with their śānti pāṭha on a page of its own (`shanti.2`, `shanti.3`), and each vallī ends with its closing words, on a page of its own (`iti.1`, `iti.2`, `iti.3`).
- **Items:** one per paragraph of an anuvāka, as the tradition numbers them and the page prints them, each ending with its number (॥१॥ … ॥६॥); an anuvāka's closing words (इति प्रथमोऽनुवाकः ॥) are the last line of its last paragraph. Ids are the citation (`1.3.2`, `3.10.6`), plus `shanti.2`, `shanti.3` and `iti.1` … `iti.3`. 56 items: 49 paragraphs (types `mantra`), the two anuvākas that are the Śīkṣāvallī's śānti pāṭhas (1.1, 1.12) and the two सह नाववतु that open vallīs 2 and 3 (type `shanti`), and three closing words (type `iti`). Ids are permanent.
- **Numbering:** a paragraph's `n` is its number within its anuvāka, as printed at its end; it is cited vallī.anuvāka.paragraph (`work.json` → `cite`: Mantra 1.3.2, Shanti Mantra 1.12.1). The śānti pāṭhas of vallīs 2 and 3 and the closing words have no number.
- **Types:** `mantra` (मं॰ / Man.), `shanti` (शा॰ / Shan.), `iti` (इति / Iti), as the other Upaniṣads.
- **Topics:** one per anuvāka with its theme, in our words, plus the śānti pāṭha of vallīs 2 and 3.
- **Reading plans:** none; the Upaniṣad is read in one or three sittings.

## Differences from the other Upaniṣads
- **The śānti pāṭhas of the vallīs.** The Śīkṣāvallī's are its own first and last anuvākas (शं नो मित्रः … वदिष्यामि and … अवादिषम्, two different texts), and the Brahmānanda- and Bhṛguvallī each open with सह नाववतु (`shanti.2`, `shanti.3`), as the page and the recording have them. The सह नाववतु the page prints again after the closing words of vallīs 2 and 3 is not an item: the SMVedroad recording does not sing it there (its transcript: इति आनन्दवल्ली समाप्ता is followed by अथ भृगुवल्ली, हरिः ॐ and the opening सह नाववतु of vallī 3; इति भृगुवल्ली समाप्ता by समाप्ता च तैत्तिरीयोपनिषत्, हरिः ॐ), and a śānti printed again at the end is not an item (PLAYBOOK §11, as the Kaṭha, Kena and Muṇḍaka).
- **Items are paragraphs of prose,** not metrical verses: the Taittirīya numbers its anuvākas' paragraphs (॥१॥ …), and the page prints one block per paragraph, so these are the items, cited at three levels as the Kaṭha's mantras are.
