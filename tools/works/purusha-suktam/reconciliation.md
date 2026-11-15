# Puruṣa Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/purusha-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/purusha-suktam/printouts/shlokam/purusha-suktam.html`). It gives 25 verse blocks, each with the Devanagari (with svaras), a transliteration (with accents), an English rendering and word glosses.

**Which text it is.** The page's blocks 1–18 and 19–24 are the same mantras, in the same order, as the two anuvākas Sanskrit Wikisource gives as Taittirīya Āraṇyaka 3.12 and 3.13 (its unaccented prapāṭhaka 3, `तैत्तिरीयारण्यकम्(विस्वर)/प्रपाठकः ३`, the second tagged उत्तरनारायणः), and that page is the independent witness every word is checked against (below).

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed (the page puts one inside र्‌ष, as in स॒हस्र॑शीर्​षा॒, only to stop a ligature), empty lines dropped. The svaras are kept as the page has them (॑ ॒ ᳚). The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari, accents included (`shlokam.tr2deva`), and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / ōṃ, the ँ the Devanagari writes before य व ल (`तं-यँ॒ज्ञ`, taṃ ya̠jña), and a nasal before a consonant written as its class letter or as ṃ. Every other line agrees letter for letter and svara for svara. The two lines that differ (`WITNESS`):
   - mantra 18, line 2: महि॒मानः॑ सचन्ते in Devanagari, mahi̠māna̍-ssachantē in the transliteration. The same words: visarga before स written as ः or as -स्स, both of which the page uses. The Devanagari is kept.
   - block 25, line 1: the heading शान्ति मन्त्रः, which the transliteration gives in English ("Shanti Mantra"). The heading is left out (below).
3. **Headings left out** (`HEADING`): उत्तरनारायणम् (the first line of block 19) and शान्ति मन्त्रः (block 25) are the editor's headings, not recited. Our topics name these places.
4. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: these rest on the grammar, each where the page is clearly wrong, and the witness confirms every one (below).
5. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥, Pāṇini's spelling, ꣳ (a Yajurveda text: the page's typed ग्ं), the ISO 15919 transliteration made from the verse, with the svaras as accents.

## Corrections (all in `source/settle.py` → `FIX`)

| Mantra | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 2 | उ॒तामृ॑त॒त्व स्येशा॑नः | उ॒तामृ॑त॒त्वस्येशा॑नः | A space inside one word, अमृतत्वस्य ("of immortality"). |
| 6 | श॒रध्ध॒विः | श॒रद्ध॒विः | शरद् + हविः gives द्ध; ध्ध (two aspirates) is no Sanskrit spelling. |
| 12 | क॒ति॒था व्य॑कल्पयन्न् | क॒ति॒धा व्य॑कल्पयन्न् | कतिधा, "in how many ways", the question the next line answers; कतिथा is no word. |
| 16 | …अ॒भि॒वद॒न्॒, यदा-ऽऽस्ते᳚ | …अ॒भि॒वद॒न्॒ यदा-ऽऽस्ते᳚ | A stray comma inside the pāda; the page uses none elsewhere. |

## Kept as the page has it
- **The Taittirīya recitation spellings:** -स्स for visarga before स, -ञ्ज / -म्प / -न्द (the nasal joined to the next word with a hyphen), थ्स (य॒ज्ञाथ्स॑र्व॒हुतः॑, for त्स), ग्ं, the ँ in विँ॒श्वतो॑ and यँ॒ज्ञम्, -ऽ for the avagraha and -ऽऽ where a long ā is joined (पादो᳚-ऽस्ये॒हा-ऽऽभ॑वा॒त्), the doubled final न्न् (व्य॑कल्पयन्न्, अ॑कल्पयन्न्).
- **प॒शूग्-स्ताग्-श्च॑क्रे** (mantra 9): written as the page writes it.
- **The order:** the sūkta, the Uttaranārāyaṇa, then the śānti pāṭha, as the page gives them; the recording also sings the śānti pāṭha before the sūkta (its transcript), so the text opens with it too (`shanti.1`, the page's own words, the same as `shanti.end`).

## Structure (not on the page as such)
- **Numbering.** The page's Devanagari has no verse numbers; its blocks are numbered 1–25 in the HTML (`data-verse`). Mantras keep that number (1–24), running on through the Uttaranārāyaṇa; the śānti pāṭha (block 25) is unnumbered.
- **Sections:** `shanti` (the opening śānti pāṭha), `purusha` (1–18, TA 3.12), `uttara` (19–24, TA 3.13), `end` (the closing śānti pāṭha).
- **The śānti pāṭha's first line** holds eight short phrases on the page; it is written two to a line, as they pair in sense (तच्छं योरावृणीमहे । गातुं यज्ञाय ।, …), with ॐ शान्तिः… as the last line.

## Witnesses (`source/check.py`)
- **Sanskrit Wikisource, Taittirīya Āraṇyaka (unaccented), prapāṭhaka 3** (`तैत्तिरीयारण्यकम्(विस्वर)/प्रपाठकः ३`, no edition named): anuvākas 3.12 and 3.13 and the prapāṭhaka's closing śānti, against mantras 1–24 and both śāntis (`source/witness/wikisource-ta.txt`). It has no svaras, so the page's svaras have no witness.
- **Not used:** Wikisource's separate page पुरुषसूक्तम् (the Ṛgveda's sixteen-verse order, typed with S for ऽ and slips, by one contributor); Wikisource's accented Taittirīya Āraṇyaka lacks prapāṭhaka 3; GRETIL has no Taittirīya Āraṇyaka.
- **Agreement.** Every word of the 24 mantras and the śānti agrees, the Taittirīya spellings and the anusvāra's writing aside (`tools/works/sukta_witness.py`). The four corrections are the witness's readings: अमृतत्वस्येशानः, शरद्धविः, कतिधा, and no comma.
- **The witness's one slip:** mantra 17, तमेवं विद्वानमृतं इह भवति, where its own mantra 20 and the page read अमृत इह (अमृतः इह): the page stays.
