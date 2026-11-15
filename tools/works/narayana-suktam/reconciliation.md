# Nārāyaṇa Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/narayana-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/printouts/shlokam/narayana-suktam.html`). It gives 17 verse blocks, each with the Devanagari (with svaras), a transliteration (with accents), an English rendering and word glosses.

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The svaras are kept as the page has them (॑ ॒ ᳚). The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari, accents included (`shlokam.tr2deva`), and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / ōṃ, the ँ the Devanagari writes before य व ल (`वि॒श्वाक्षं॑-विँ॒श्वश॑म्भुवम्`, vi̠śvākṣa̍ṃ vi̠śvaśa̍mbhuvam), and a nasal before a consonant written as its class letter or as ṃ. All 34 lines agree letter for letter and svara for svara.
3. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: the correction rests on the grammar, where the page is clearly wrong. The check against independent witnesses is a later step.
4. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥, Pāṇini's spelling (the page's ओम् ॥ and ॐ are the sacred syllable), ꣳ (a Yajurveda text: the page's typed ग्ं), the ISO 15919 transliteration made from the verse, with the svaras as accents.

## Corrections (all in `source/settle.py` → `FIX`)

| Mantra | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 12 | नी॒लतो॑-यद॑मध्य॒स्था॒-द्वि॒ध्युल्ले॑खेव॒ | नी॒लतो॑-यद॑मध्य॒स्था॒-द्वि॒द्युल्ले॑खेव॒ | विद्युत् ("lightning", वि + द्युत्) has द; ध्यु is a misspelling. The page's joining of the words is kept. |

## Kept as the page has it
- **The Taittirīya recitation spellings:** -स्स, -न्न / -म्म / -ङ्क (the nasal joined to the next word with a hyphen), ग्ं, the ँ in विँ॒श्व… and व्याँ॒प्य, -ऽ for the avagraha (स॑मु॒द्रें-ऽतं॑, सो-ऽग्र॑भु॒क्).
- **Valid words, kept as printed:** शि॒लाभि॑स्तु (mantra 8); व्य॒वस्थि॑तः after वह्नि॑शिखा (mantra 11), as Sanskrit Wikisource's accented Taittirīya Āraṇyaka also reads it; the page's line ends (। inside a mantra, ॥ where the page puts it).
- **ओम् ॥ before mantra 1:** printed on the page as the start of the sūkta; kept.
- **The order:** the śānti pāṭha, the sūkta, the Gāyatrī and the closing śānti, as the page gives them.

## Structure (not on the page as such)
- **Numbering.** The page's Devanagari has no verse numbers; its blocks are numbered 1–17 in the HTML (`data-verse`). Block 1 is the śānti pāṭha, blocks 2–15 are mantras 1–14 (one block of two lines each, as the page divides them), block 16 the Gāyatrī, block 17 the closing śānti.
- **Sections:** `shanti` (block 1), `sukta` (mantras 1–14), `end` (Gāyatrī, closing śānti).
- **The closing ॐ शान्तिः शान्तिः शान्तिः** is an item of its own (type `shanti`), as the page gives it a block of its own; it is not a repeat of the opening सह नाववतु.
