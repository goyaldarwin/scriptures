# Nīlā Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/neela-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/samhita/neela-suktam/printouts/shlokam/neela-suktam.html`). It gives 5 verse blocks, each with the Devanagari (with svaras), a transliteration (with accents), an English rendering and word glosses.

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The svaras are kept as the page has them (॑ ॒ ᳚). The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari, accents included (`shlokam.tr2deva`; its ḻ is ळ), and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / ōṃ, the ँ the Devanagari writes before य व ल, and a nasal before a consonant written as its class letter or as ṃ. All 9 lines agree letter for letter and svara for svara.
3. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: these rest on the grammar and on the page itself, each where the page is clearly wrong. The check against independent witnesses is a later step.
4. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥, Pāṇini's spelling (ओं and ॐ are the sacred syllable), ꣳ (a Yajurveda text: the page's typed ग्ं), the ISO 15919 transliteration made from the verse, with the svaras as accents.

## Corrections (all in `source/settle.py` → `FIX`)
Four are spaces missing between words that make no sandhi with each other, so that two words read as one; the fifth is a misspelt word.

| Mantra | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 1 | पय॑स्वती॒रन्ति॒राशा॑नो अस्तु | पय॑स्वती॒ रन्ति॒राशा॑ नो अस्तु | पयस्वती, रन्तिः आशा, नः: no sandhi joins पयस्वती to रन्ति, or आशा to नः. |
| 1 | -ऽस्येशा॑ना॒सह॑सो॒या म॒नोता᳚ | -ऽस्येशा॑ना॒ सह॑सो॒ या म॒नोता᳚ | ईशाना, सहसः, या: three words; nothing joins them. |
| 2 | वा॒युस्स॑न्धुवा॒नावाता॑ | वा॒युस्स॑न्धुवा॒ना वाता॑ | सन्धुवानाः वाताः: the visarga drops before व, leaving two words. |
| 2 | दि॒वोध॒रुणः॑ | दि॒वो ध॒रुणः॑ | दिवः धरुणः ("the support of heaven"): two words. |
| 2 | अ॒स्येश्या॑ना॒ जग॑तो॒ | अ॒स्येशा॑ना॒ जग॑तो॒ | ईशाना ("ruling"), as the same phrase in mantra 1 (अ॒स्येशा॑ना॒); ईश्याना is no word. |

## Kept as the page has it
- **The Taittirīya recitation spellings:** ओ-ङ्गृ॒णा॒हि॒ (ॐ joined to गृणाहि), -र्मात॒रिश्वा (the reph joined with a hyphen), ग्ं, the ँ in विँष्णु॑प॒त्नी, -ऽ for the avagraha, ळ in नीळा.
- **The accents as printed:** सुत॒र॑सि (the invocation) beside the Durgā Sūkta page's सु॒तर॑सि, विँष्णु॑प॒त्नी: the svaras are the page's.
- **The invocation and the Gāyatrī,** which are not in Taittirīya Saṃhitā 4.4.12, are kept as the page gives them, the invocation as a maṅgala mantra (the Śrī Rudram's type for its invocations).

## Structure (not on the page as such)
- **Numbering.** The page's Devanagari has no verse numbers; its blocks are numbered 1–5 in the HTML (`data-verse`). Block 1 is the invocation, blocks 2–3 are mantras 1–2 (as the page divides the passage), block 4 the Gāyatrī, block 5 the śānti.
- **Sections:** `sukta` (the invocation and mantras 1–2), `end` (the Gāyatrī, the śānti).
