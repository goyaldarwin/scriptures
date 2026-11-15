# Durgā Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/durga-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/durga-suktam/printouts/shlokam/durga-suktam.html`). It gives 9 verse blocks, each with the Devanagari (with svaras, except the closing words and śānti), a transliteration (with accents), an English rendering and word glosses.

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The svaras are kept as the page has them (॑ ॒ ᳚). The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari, accents included (`shlokam.tr2deva`), and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / ōṃ, the ँ the Devanagari writes before य व ल (`ज्वल॒न्तीं-वैँ॑रोच॒नीम्`, jvala̠ntīṃ vai̍rōcha̠nīm), and a nasal before a consonant written as its class letter or as ṃ (the transliteration's tavē̎mdra for तवे᳚न्द्र). All 19 lines agree letter for letter and svara for svara.
3. **Heading left out** (`HEADING`): अथ दुर्गा सूक्तम्, the first line of block 1, is the editor's heading, as the Śrī Rudram's अथ श्रीरुद्रप्रश्नः; our topic names the place. Its pair at the end, इति दुर्गा सूक्तम्, is kept as the closing words (type `iti`), as the library keeps a work's closing words.
4. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: these rest on the grammar, each where the page is clearly wrong. The check against independent witnesses is a later step.
5. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥, Pāṇini's spelling (ओम् ॥ and ॐ are the sacred syllable), ꣳ (a Yajurveda text: the page's typed ग्ं), the ISO 15919 transliteration made from the verse, with the svaras as accents.

## Corrections (all in `source/settle.py` → `FIX`)

| Mantra | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 1 | सुनवाम॒ सोम॑ मरातीय॒तो | सुनवाम॒ सोम॑मरातीय॒तो | सोमम् + अरातीयतः: the space falls inside the word सोमम्, leaving मरातीयतो, no word. |
| 5 | पृ॒त॒ना॒ जित॒ग्ं॒ सह॑मानम् | पृ॒त॒ना॒जित॒ग्ं॒ सह॑मानम् | One compound, पृतनाजितम् ("victor in battles"), the object of हुवेम with सहमानम्, उग्रम्, अग्निम्; जितम् alone does not fit. |

## Kept as the page has it
- **The Taittirīya recitation spellings:** पर्-ष॒दति॑ and दु॑रि॒ता-ऽति॑पर्-षि (the page's way of writing the reph before ष), -स्स, -न्त / -ङ्क / -म्प (the nasal joined with a hyphen), थ्स (अ॒स्मान्थ्स्व॒स्तिभिः, पर॒माथ्स॒धस्था᳚त्), ग्ं, the ँ in वैँ॑रोच॒नीम्, सं॒वँसा॑नो and लोँ॒क, शंयोँः.
- **Valid words, kept as printed:** निद॑हाति॒ (mantra 1), सु॒तर॑सि (mantra 2), कन्यकु॒मारि॑ and दुर्गिः (the Gāyatrī).
- **The closing words and śānti** have no svaras on the page; kept so.

## Structure (not on the page as such)
- **Numbering.** The page's Devanagari has no verse numbers; its blocks are numbered 1–9 in the HTML (`data-verse`). Blocks 1–7 are mantras 1–7, block 8 the Gāyatrī; block 9 holds the closing words and the śānti, made two items (`iti`, `shanti.end`) as the library writes a work's closing words and its śānti.
- **Sections:** `sukta` (mantras 1–7), `end` (the Gāyatrī, the closing words, the śānti).
