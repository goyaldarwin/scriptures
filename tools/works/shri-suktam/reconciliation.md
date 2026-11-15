# Śrī Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/sri-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/rigveda/samhita/shri-suktam/printouts/shlokam/sri-suktam.html`). It gives 37 verse blocks, each with the Devanagari (no svaras), a transliteration, an English rendering and word glosses; every block ends with its number (॥१॥ … ॥३७॥).

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari (`shlokam.tr2deva`) and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / oṃ, and a nasal before a consonant written as its class letter or as ṃ (दीपांकुराम् / dīpāṅkurām). All 79 lines agree letter for letter.
3. **Headings left out** (`HEADING`): फलश्रुतिः (the first line of block 16) and स्तोत्रम् (block 17) are the editor's headings, not recited. Our topics name these places.
4. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: these rest on the grammar and on the page itself (its other verses, its Nīlā Sūkta page), each where the page is clearly wrong. The check against independent witnesses is a later step.
5. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥ and compact verse numbers, Pāṇini's spelling (ॐ; a class nasal inside a word: the page's वरांकुशौ, दीपांकुराम्), the ISO 15919 transliteration made from the verse.

## Corrections (all in `source/settle.py` → `FIX`)

| Verse | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 17 | पद्माक्षी (twice) | पद्माक्षि | The vocative, "O lotus-eyed", as the verse addresses the goddess (पद्मानने, …सम्भवे) and as the page writes पद्मदलायताक्षि in verse 24; पद्माक्षी is the nominative. |
| 22 | न च मात्सर्य न लोभो | न च मात्सर्यं न लोभो | मात्सर्यम् ("envy"), a subject like क्रोधः and लोभः beside it; मात्सर्य is a bare stem. |
| 30 | भजेहमाद्यां | भजेऽहमाद्यां | भजे + अहम्: the avagraha of the elided a is dropped on the page. |
| 30 | जगदीस्वरीं | जगदीश्वरीं | ईश्वरी ("sovereign"), with श. |
| 34 | महालक्ष्मी च विद्महे विष्णुपत्नी च धीमहि | महालक्ष्म्यै च विद्महे विष्णुपत्न्यै च धीमहि | A Gāyatrī names its deity in the dative, as the page's own verse 37 (महादेव्यै च विद्महे), its Nīlā Sūkta page (म॒हा॒दे॒व्यै च॑ वि॒द्महे॑ विष्णुप॒त्न्यै च॑ धीमहि) and its Nārāyaṇa and Durgā Gāyatrīs (नारायणाय, कात्यायनाय). |
| 37 | विष्णुपत्नी च धीमहि | विष्णुपत्न्यै च धीमहि | The same: the dative beside महादेव्यै in the same line. |
| 35 | पवमानं महियते | पवमानं महीयते | महीयते ("is honoured"), with ī; महियते is no word. |

## Kept as the page has it
- **Spacing inside compounds** (क्षीरसमुद्र राजतनयां, दासीभूतसमस्त देव वनितां, स्तनभर नमिता, बालार्क कोटि प्रतिभां, …): the page's spacing, which changes no letter, is kept.
- **Valid readings, kept as printed:** कां सोस्मितां (verse 4), पद्म ऊरु and पद्मासम्भवे (verse 17), हस्त्यश्वादिगवे रथम् (verse 19), ईश्वरींग् (verse 9, the page's ग् before स as the reciters say it; the standard writes it ईश्वरीङ्ग्, as the page's transliteration īśvarīṅg).
- **The repetitions in verse 31** (नारायणि नमोऽस्तु ते, three times), as printed and recited.
- **The closing (verse 37)**: य एवं वेद, the Gāyatrī with ॐ, and the śānti, printed as one verse with one number, kept as one item (type `uttara`).

## Structure (not on the page as such)
- **Numbering.** Each verse keeps the number the page prints (1–37).
- **Sections:** `sukta` (1–15, the fifteen ṛks the phalaśruti names: सूक्तं पञ्चदशर्चं), `phala` (16), `stotra` (17–37, under the page's heading स्तोत्रम्).
- **Types:** the ṛks 1–15 are mantras; 16 the phalaśruti; 34 the Gāyatrī; 37 the closing; the rest ślokas.
