# Kena Upaniṣad (केनोपनिषद्)

Shelf: हिन्दू धर्म › वेद › सामवेद › उपनिषद् › केनोपनिषद् (`library/hinduism/veda/samaveda/upanishad/kena-upanishad/`, work id `kena-upanishad`). The Upaniṣad of the Talavakara śākhā of the Sāmaveda (the book: the ninth chapter of its Talavakara branch), named from its first word, *kena*, "by whom?": four khaṇḍas, 34 mantras (8 + 5 + 12 + 9), verse in khaṇḍas 1–2 and prose in 3–4, with the Sāmaveda's śānti mantra आप्यायन्तु before them and the closing words of each khaṇḍa.

## Sources
- **Text.** The owner's book: Swami Gurubhaktananda, *Kena Upanishad — Know That Alone as Brahman* (The Sandeepany Experience, Text 38; Chinmaya International Foundation, chinfo.org). The private copy is in scriptures-data at `<work path>/books/sandeepany/kena-upanishad-gurubhaktananda.pdf`. It is the same series and typesetting as the Kaṭha's book: its Devanagari is set in a legacy font (BRH Devanagari) whose text layer cannot be read, so the text is taken from the book's **IAST transliteration** (decoded with the Kaṭha's map of the font's Latin-1 symbols: `source/extract.py`) and converted letter for letter to Devanagari (`source/settle.py`). Where the transliteration has a slip, the book's own Devanagari, read by eye, and the witnesses settle it. The result is checked against three Devanagari witnesses (`source/check.py`, `source/witness/`): upanishads.org.in (one page per mantra), Sanskrit Wikisource's केनोपनिषद् (a copy of sanskritdocuments.org's text) and IIT Kanpur's Heritage reader. Every decision is in `reconciliation.md`.
- **Audio.** SMVedroad, "Ken upanishad Chant | केनोपनिषद् गान | With Lyrics" (YouTube `wng4v0SS8hA`, 647 s), in `audio/smvedroad/` (`source.json`, `recordings.json`). The private copy is in scriptures-data at `<work path>/audio/smvedroad/`. Transcribed by Whisper (`audio/smvedroad/transcripts/`); every verse's start and end come from Meta's MMS forced aligner on the known text (`tools/audio/METHOD.md`; `mms/`, `aligned.json`, `aligned.md`): all 39 items have a start, not yet scored against starts set by ear. It sings the whole text in this order: the śānti from 0:58 (the transcript has no words before it), the four khaṇḍas, each with its closing words, the fourth's sung as इति चतुर्थः खण्डः, केनोपनिषत् समाप्ता. What it adds is not a text and is left untimed: its announcement of a khaṇḍa (अथ चतुर्थः खण्डः) and the हरिः ॐ it ends with; it does not sing the śānti again at the end. The to-check list is the 10 verses the automatic checks flag (`check.json`); the owner's starts set by ear always win.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <the PDF>` → `source/pdf_raw.json`: each mantra's transliteration lines, decoded, the śānti mantra's, and each khaṇḍa's closing words (needs PyMuPDF).
- `source/settle.py` → `text.txt`: the settled text in Devanagari, with the topics; the export writes it by the library's standard and makes the transliteration (PLAYBOOK §3). Its `iast2deva` is the Kaṭha's, with the pluta ३ this text has.
- `source/witness/*.txt`: Devanagari witnesses (verses separated by blank lines, `# 2` naming a khaṇḍa, `# end` before the closing śānti), each made from the raw download kept in scriptures-data under `<work path>/printouts/<site>/`.
- `source/check.py`: every witness must spell the same words as `text.txt`, khaṇḍa by khaṇḍa (only the differences in `reconciliation.md` are allowed). Run it after any change to the text.

Rebuild: `python3 tools/works/kena-upanishad/source/settle.py && python3 tools/works/kena-upanishad/source/check.py && python3 tools/works/export.py kena-upanishad && python3 tools/site/build.py`. Run `extract.py` again only if the PDF changes.

## Structure
- **Parts:** the four khaṇḍas, प्रथम खण्ड … चतुर्थ खण्ड (keys `1` … `4`).
- **Sections (pages):** one per khaṇḍa (`k1` … `k4`), plus `shanti` (opening).
- **Hierarchy:** four khaṇḍas (parts, each one page) › mantras.
- **Items:** `shanti.1`; `1.1` … `4.9`; the closing words `1.iti` … `4.iti` (the fourth's with the Upaniṣad's own, इति केनोपनिषत्).
- **Numbering:** a mantra's `n` is its number within the khaṇḍa, as the book prints it at its end; it is cited khaṇḍa.mantra (`work.json` → `cite`: Mantra 1.3, in the reader's places, the player and search), as the Praśna's praśna.mantra. The book counts eight mantras in khaṇḍa 1 (its "Chapter 1, 8 Verses"), printing 1.3 in two halves (1.3.1, 1.3.2) that are one mantra here; Wikisource and IIT Kanpur count nine there (`reconciliation.md`). Ids are permanent.
- **Types:** `shanti` (शा॰ / Shan.), `mantra` (मं॰ / Man.) and `iti` (समापन (पुष्पिका) / Closing words (iti)).
- **Topics:** one per khaṇḍa with its theme, plus the śānti pāṭha.
- **Reading plans:** none; the Upaniṣad is read in one sitting.
- **The closing śānti:** the book prints the śānti only before the text and ends with इति केनोपनिषत् and ॐ तत् सत्; the work ends with 4.iti (PLAYBOOK §11: a śānti mantra repeated at the end is not an item).
