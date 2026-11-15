# Nārāyaṇa Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/narayana-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/aranyaka/narayana-suktam/printouts/shlokam/narayana-suktam.html`). It gives 17 verse blocks, each with the Devanagari (with svaras), a transliteration (with accents), an English rendering and word glosses.

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The svaras are kept as the page has them (॑ ॒ ᳚). The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari, accents included (`shlokam.tr2deva`), and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / ōṃ, the ँ the Devanagari writes before य व ल (`वि॒श्वाक्षं॑-विँ॒श्वश॑म्भुवम्`, vi̠śvākṣa̍ṃ vi̠śvaśa̍mbhuvam), and a nasal before a consonant written as its class letter or as ṃ. All 34 lines agree letter for letter and svara for svara.
3. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: the first correction rests on the grammar; the others are settled on the independent witnesses (below).
4. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥, Pāṇini's spelling (the page's ओम् ॥ and ॐ are the sacred syllable), ꣳ (a Yajurveda text: the page's typed ग्ं), the ISO 15919 transliteration made from the verse, with the svaras as accents.

## Corrections (all in `source/settle.py` → `FIX`)

| Mantra | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 12 | नी॒लतो॑-यद॑मध्य॒स्था॒-द्वि॒ध्युल्ले॑खेव॒ | नी॒लतो॑-यद॑मध्य॒स्था॒-द्वि॒द्युल्ले॑खेव॒ | विद्युत् ("lightning", वि + द्युत्) has द; ध्यु is a misspelling. The page's joining of the words is kept. Both witnesses: विद्युल्लेखेव. |
| 2 | पुरु॑ष॒-स्तद्विश्व-मुप॑जीवति | पुरु॑ष॒-स्तद्विश्व॒-मुप॑जीवति | The anudātta before उप (úpa) is dropped; the accented Taittirīya Āraṇyaka: तद्विश्व॒मुप॑जीवति. |
| 6 | स॑मु॒द्रें-ऽतं॑ | स॑मु॒द्रे-ऽन्तं॑ | समुद्रे + अन्तम्: the anusvāra is on the wrong syllable. Āraṇyaka स॑मु॒द्रेन्त॑, Mahānārāyaṇa समुद्रेऽन्तं. |
| 7 | वि॑तस्या॒न्ते॒ | वि॑तस्त्या॒न्ते॒ | वितस्त्या, "by a span" (वितस्ति); वितस्या is no word. Both witnesses: वितस्त्या-. |
| 8 | शि॒लाभि॑स्तु | सि॒राभि॑स्तु | सिराभिः, "with veins (nāḍīs)", as both witnesses; शिला, "stone", has no sense around the heart. |
| 10 | र॒श्मय॑स्तस्य॒ सन्त॑ता । | र॒श्मय॑स्तस्य॒ सन्त॑ताः । | रश्मयः … सन्तताः (masculine plural): the visarga is dropped at the pause; the Mahānārāyaṇa: सन्तताः (the Āraṇyaka lacks the line). |
| 14 | ऋतग्ं स॒त्य | ऋ॒तग्ं स॒त्य | ऋतम् (ṛtám): the anudātta on ऋ is dropped; the accented Āraṇyaka: ऋ॒तꣳ. |

## Kept as the page has it
- **The Taittirīya recitation spellings:** -स्स, -न्न / -म्म / -ङ्क (the nasal joined to the next word with a hyphen), ग्ं, the ँ in विँ॒श्व… and व्याँ॒प्य, -ऽ for the avagraha (स॑मु॒द्रे-ऽन्तं॑, सो-ऽग्र॑भु॒क्).
- **Valid words, kept as printed:** व्य॒वस्थि॑तः after वह्नि॑शिखा (mantra 11), as Sanskrit Wikisource's accented Taittirīya Āraṇyaka also reads it; the page's line ends (। inside a mantra, ॥ where the page puts it).
- **ओम् ॥ before mantra 1:** printed on the page as the start of the sūkta; kept.
- **The order:** the śānti pāṭha, the sūkta, the Gāyatrī and the closing śānti, as the page gives them. The recording does not sing the śānti pāṭha (it stays, untimed) and opens with Puruṣa Sūkta mantra 17, धाता पुरस्ताद्यमुदाजहार…, which the reciters say before the Nārāyaṇa Sūkta: it is taken from the Puruṣa Sūkta (`[take purusha-suktam m17]`, its words and witness there), before mantra 1, under our topic "Opening".

## Structure (not on the page as such)
- **Numbering.** The page's Devanagari has no verse numbers; its blocks are numbered 1–17 in the HTML (`data-verse`). Block 1 is the śānti pāṭha, blocks 2–15 are mantras 1–14 (one block of two lines each, as the page divides them), block 16 the Gāyatrī, block 17 the closing śānti.
- **Sections:** `shanti` (block 1), `sukta` (the taken opening and mantras 1–14), `end` (Gāyatrī, closing śānti).
- **The closing ॐ शान्तिः शान्तिः शान्तिः** is an item of its own (type `shanti`), as the page gives it a block of its own; it is not a repeat of the opening सह नाववतु.

## Witnesses (`source/check.py`)
- **Sanskrit Wikisource, the Taittirīya Āraṇyaka with svaras** (`तैत्तिरीय-आरण्यकम्`, one page, no edition named; its private-use font characters read as `tools/works/sukta_witness.py` → `PUA`): the sūkta (its 6.11.1–6.12.1, TA 10), the Gāyatrī (its 6.1.6) and सह नाववतु (`source/witness/wikisource-ta.txt`). Compared letter for letter and svara for svara.
- **Sanskrit Wikisource, the Mahānārāyaṇa Upaniṣad** (`महानारायणोपनिषत्`, Āndhra recension, unaccented): anuvāka 13 and the first verse of 23, the Gāyatrī, the opening सह नाववतु (`source/witness/wikisource-mnu.txt`). The two are independent transcriptions of different recensions.
- **Settled on the witnesses:** the six corrections above (mantras 2, 6, 7, 8, 10, 14).
- **Kept, the recited text's own readings where both witnesses word otherwise** (each valid; the recording sings the page's, as far as its transcript shows): the ओम् before mantra 1 and the Gāyatrī; पर॒म-म्प॒दम् (both: परमं प्रभुम्); पर॑मान्नि॒त्यं (both: परमं नित्यं); जगत्स॒र्व॒म् (both: जगत्यस्मिन्); ज्वा॒ल॒मा॒लाकु॑ल-म्भा॒ती॒ (both: हृदयं तद्विजानीयात्); आपा॑दतल॒मस्त॑कः (both: -मस्तकम्); -मध्य॒स्था॒-द्वि॒द्यु- (both: मध्यस्था विद्यु-); स ब्रह्म॒ (both: स ब्रह्मा).
- **Kept against one witness:** the order of mantra 4's two lines (ज्योति first; both witnesses put ब्रह्म first, the Āraṇyaka without the ध्याता line, the Mahānārāyaṇa with नारायणः for नारायण-); व्य॒वस्थि॑तः (the Āraṇyaka; the Mahānārāyaṇa व्यवस्थिता); स हरिः and नमो नमः (the Mahānārāyaṇa; the Āraṇyaka lacks them); the तिर्यगूर्ध्व… line and भास्वत्यणूपमा (the Mahānārāyaṇa; the Āraṇyaka lacks the line and reads पीताभास्यात्तनूपमा); the Āraṇyaka's वितस्त्यान्तु for -न्ते.
- **The Mahānārāyaṇa's slips:** नारयणः, नीवारशूक्वत्, भास्वत्यणूपम.
- **Svaras the Āraṇyaka places otherwise, kept:** ना॒राय॒णपर॑-म्ब्र॒ह्म॒ (Āraṇyaka प॑रं), तत्त्व-न्ना॑ (त॒त्वं), अनन्त॒मव्यय॑- (अन॑न्त॒मव्य॑य-): the page's accentuation, not clearly wrong; the svaras are otherwise the same wherever the two spell the same words.

## Word meanings
Every word has an entry in the shared dictionary (`library/glossary/sa.json`), checked in Monier-Williams and Apte. Sāyaṇa's commentary is not at hand here, so where a reading is open the dictionaries and the grammar decide, and no sense is put to any commentator. A word the recitation joins with a hyphen (the Taittirīya way) is one key, its words in `p`.
- **नारायणपरः** (4, 5), written as one word: "Nārāyaṇa the supreme" first, "devoted to Nārāyaṇa" second (पर at the end of a compound).
- **निष्ट्या** (7): निष्टि, "the joint of the neck" (Monier-Williams, from the Taittirīya Āraṇyaka's scholiast), ablative निष्ट्याः before व.
- **भाती** (8): Monier-Williams gives भाती as a feminine of the present participle of √भा; the entry also gives "shines".
- **अणीयोर्ध्वा** (11): अणीयः ("most subtle") + ऊर्ध्वा ("rising upward").

## Meanings
`meanings/hi/scriptures.json` and `meanings/en/scriptures.json` rest on the mantra's words, their grammar and Monier-Williams and Apte; no reading is put to any commentator. Where the words allow more than one reading:

| Mantra | Settled reading | Why |
|---|---|---|
| m01, m02, m03, m06 | the accusatives with no verb close with "on him we meditate" (उनका हम ध्यान करते हैं) | the sūkta goes on to the heart as the seat of meditation (m07–m13); the same verb supplied in all four |
| m02 | परमान्नित्यम्: परमात् + नित्यम्, "beyond even the highest, eternal" | त् becomes न् before न्; परमम् + नित्यम् would print परमन्नित्यम् |
| m03 | आत्मेश्वरम्: "the ruler of all selves" | beside पतिं विश्वस्य; Monier-Williams' "master of one's self" is said of a person |
| m04, m05 | नारायणपरः …: "Nārāyaṇa is the supreme light …", परः "supreme" throughout | the lines are parallel (नारायणः परः); "devoted to Nārāyaṇa" would break the parallel |
| m06 | समुद्रेऽन्तम्: "the goal in the ocean of worldly existence" | अन्त, "end, limit" (Monier-Williams), as our word meaning |
| m13 | स ब्रह्म: Brahmā; "he is Brahman" in the footnote | a list of gods (Śiva, Hari, Indra) |
