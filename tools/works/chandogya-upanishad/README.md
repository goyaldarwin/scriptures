# Chāndogya Upaniṣad (छान्दोग्योपनिषद्)

Shelf: हिन्दू धर्म › वेद › सामवेद › उपनिषद् › छान्दोग्योपनिषद् (`library/hinduism/veda/samaveda/upanishad/chandogya-upanishad/`, work id `chandogya-upanishad`). The Upaniṣad of the Sāmaveda: eight adhyāyas (prapāṭhakas) of 13, 24, 19, 17, 24, 16, 26 and 15 khaṇḍas, 629 mantras (104 + 82 + 95 + 78 + 88 + 69 + 51 + 62), with the Sāmaveda's śānti mantra आप्यायन्तु ममाङ्गानि before them; the work ends with 8.15.1.

## Sources
- **Text.** <https://shlokam.org/text/chandogya-upanishad.htm>, the page the owner allowed, fetched on 2026-11-14. The private copy is in scriptures-data at `hinduism/veda/samaveda/upanishad/chandogya-upanishad/printouts/shlokam/chandogya-upanishad.html`. Its Devanagari is the base; its own transliteration is read back into Devanagari as a check of it (`source/settle.py`). The page has no svara marks, so neither does the text. Every correction, and why, is in `reconciliation.md`. Four web witnesses check it word by word: IIT Kanpur Heritage, upanishads.org.in, Sanskrit Wikisource and GRETIL (`reconciliation.md`, "Witnesses"); their raw downloads are in scriptures-data at `hinduism/veda/samaveda/upanishad/chandogya-upanishad/printouts/<site>/`.
- **Meanings, word meanings, introduction.** Not written yet.
- **Audio.** Himalaya Swamyji (YouTube channel `UC9iJNpZ9slWLKV_sc70atDQ`), “Chandogya Adyaayam 1 … 8 — Chanting with telugu script”: eight videos, one per adhyāya, in `audio/himalaya-swamyji/` (`source.json`, `recordings.json` in adhyāya order: `OhCjI726VAk` 2449 s, `k3aTyQeXJW4` 2258 s, `Mc1Q13Fnrt4` 2059 s, `hb70MYF1N70` 2081 s, `foAEXZosBfM` 2318 s, `jCHUgtLF9Cg` 1785 s, `a_9YayMp_H0` 2182 s, `x6yyfqQfZI4` 2254 s; 4 h 50 min in all). The private copies are in scriptures-data at `hinduism/veda/samaveda/upanishad/chandogya-upanishad/audio/himalaya-swamyji/<adhyāya>_<YouTube id>.opus`. The descriptions credit the chanting to Poojya Sree Surya Bhaskarendra Saraswathi Swamy (Uttarakashi), say each video chants its whole adhyāya in Sanskrit with the Telugu script on screen, and name no opening or closing prayer; whether a video sings the śānti mantra, or anything before or after its adhyāya, is settled from its transcript when it is timed. Not transcribed or timed yet.

## Files
The folder's format: `tools/works/README.md`.
- `source/extract.py <the page>` → `source/chandogya_raw.json`: each block of the page (its place, its Devanagari lines and its transliteration lines), with zero-width spaces removed. The page's English and word glosses are not read.
- `source/settle.py` → `text.txt`: the settled text, one verse per mantra, with the parts, sections and topics; it first compares the page's Devanagari with its transliteration, block by block, and stops on a difference that is not listed. The export writes the text by the library's standard and makes the transliteration (PLAYBOOK §3).
- `source/witnesses.py <the work's printouts/ in a scriptures-data clone>` → `source/witness/{iitk,upanishads-org,wikisource,gretil}.txt`: each witness's mantras in Devanagari (GRETIL's IAST read into Devanagari), by khaṇḍa.
- `source/check.py` compares every khaṇḍa of `text.txt` with every witness and fails on a difference that `source/witness-readings.tsv` (each witness's own readings) and `reconciliation.md` do not record.

Rebuild: `python3 tools/works/chandogya-upanishad/source/settle.py && python3 tools/works/chandogya-upanishad/source/check.py && python3 tools/works/export.py chandogya-upanishad && python3 tools/site/build.py`. Run `extract.py` again only if the page changes.

## Structure
- **Parts:** the eight adhyāyas (प्रथम … अष्टम अध्याय; Adhyay 1 … 8).
- **Sections (pages):** the khaṇḍas, `k<adhyāya>.<khaṇḍa>` (`k1.1` … `k8.15`), named “Khand N” (`work.json` → `cite.sec`), plus `shanti` (opening).
- **Hierarchy:** eight adhyāyas (parts) › 154 khaṇḍas (sections) › mantras.
- **Items:** `shanti.1`; `1.1.1` … `8.15.1`, 630 in all.
- **Numbering:** a mantra's `n` is its number within the khaṇḍa, which it ends with (॥१॥); it is cited adhyāya.khaṇḍa.mantra, the standard numbering, as the Kaṭha is (`work.json` → `cite`: Mantra 6.8.7). The page prints each mantra's full number (॥ ६.८.७ ॥); the text keeps the mantra's own. Ids are permanent.
- **Types:** `shanti` (शा॰ / Shan.) and `mantra` (मं॰ / Man.).
- **Topics:** 38, our own headings at each teaching (the Udgītha, the honey teaching, Śāṇḍilya, Satyakāma, the five fires, tat tvam asi, Nārada and Sanatkumāra, the small space in the heart, Indra and Virocana …), plus the śānti pāṭha.
- **Closing lines:** the page's ॥ इति प्रथमः खण्डः ॥ after each khaṇḍa and ॥ इति प्रथमोऽध्यायः ॥ after adhyāyas 1–7 are not items: the sections and parts already name them, and the page has none after adhyāya 8. The page gives the śānti mantra once, at the start (PLAYBOOK §11).
- **Loading:** the whole work at once (no `"load": "parts"`): its verses are about 0.4 MB, and its meanings in two languages will be of the Bhagavad Gītā's order (701 verses, 2 MB with four meaning sources, loaded whole), far under the several MB per part that makes a work load by part (PLAYBOOK §10).
- **Reading plans:** none.
