# Śrī Sūkta — how the text is settled

**Source of truth:** shlokam.org's page <https://shlokam.org/shloka/sri-suktam.htm>, saved as HTML by the session from the URL the owner allowed (private copy in scriptures-data at `hinduism/veda/rigveda/samhita/shri-suktam/printouts/shlokam/sri-suktam.html`). It gives 37 verse blocks, each with the Devanagari (no svaras), a transliteration, an English rendering and word glosses; every block ends with its number (॥१॥ … ॥३७॥).

## Method
1. **Extract.** `source/extract.py` reads the page's HTML, never its rendered text (`tools/works/shlokam.py` → `page`): for each verse block (`div.verse-section`), the page's verse number, the Devanagari (`div.detail-sanskrit`) and the transliteration after it, split at `<br>`, zero-width spaces removed, empty lines dropped. The page's English is © shlokam.org and is not kept in this repository.
2. **Second witness.** `source/settle.py` converts the page's own transliteration back to Devanagari (`shlokam.tr2deva`) and compares it with the Devanagari line by line (`shlokam.compare`), folding only the two scripts' conventions: ॐ / oṃ, and a nasal before a consonant written as its class letter or as ṃ (दीपांकुराम् / dīpāṅkurām). All 79 lines agree letter for letter.
3. **Headings left out** (`HEADING`): फलश्रुतिः (the first line of block 16) and स्तोत्रम् (block 17) are the editor's headings, not recited. Our topics name these places.
4. **Corrections** (`FIX`). The transliteration is a copy of the page's own Devanagari, so it cannot expose a slip the two share: these rest on the grammar and on the page itself (its other verses, its Nīlā Sūkta page), each where the page is clearly wrong. The independent witnesses confirm them, but for the Gāyatrī's datives, undone (below).
5. **The writing standard** (docs/PLAYBOOK.md §3) applies at export: ॥ and compact verse numbers, Pāṇini's spelling (ॐ; a class nasal inside a word: the page's वरांकुशौ, दीपांकुराम्), the ISO 15919 transliteration made from the verse.

## Corrections (all in `source/settle.py` → `FIX`)

| Verse | Page (both scripts) | Text used | Why |
|---|---|---|---|
| 17 | पद्माक्षी (twice) | पद्माक्षि | The vocative, "O lotus-eyed", as the verse addresses the goddess (पद्मानने, …सम्भवे) and as the page writes पद्मदलायताक्षि in verse 24; पद्माक्षी is the nominative. |
| 22 | न च मात्सर्य न लोभो | न च मात्सर्यं न लोभो | मात्सर्यम् ("envy"), a subject like क्रोधः and लोभः beside it; मात्सर्य is a bare stem. |
| 30 | भजेहमाद्यां | भजेऽहमाद्यां | भजे + अहम्: the avagraha of the elided a is dropped on the page. |
| 30 | जगदीस्वरीं | जगदीश्वरीं | ईश्वरी ("sovereign"), with श. |
| 17 | पद्मासम्भवे | पद्मसम्भवे | "Lotus-born", the vocative, as both Wikisource texts (पद्मसंभवे) and the khila (padma-); पद्मा-, "born of Padmā", has no sense for Lakṣmī, who is Padmā. |
| 22 | भक्तानां श्रीसूक्तं जपेत्सदा | भक्तानां श्रीसूक्तं जपेत् | सदा makes the anuṣṭubh pāda ten syllables; the khila and Wikisource's first text end at जपेत् (its second text shares the page's सदा). |
| 30 | त्रिणेत्रां | त्रिनेत्रां | त्रिनेत्र, "three-eyed", as all three witnesses: no rule gives ण here. |
| 35 | पवमानं महियते | पवमानं महीयते | महीयते ("is honoured"), with ī; महियते is no word. |

## Kept as the page has it
- **Spacing inside compounds** (क्षीरसमुद्र राजतनयां, दासीभूतसमस्त देव वनितां, स्तनभर नमिता, बालार्क कोटि प्रतिभां, …): the page's spacing, which changes no letter, is kept.
- **Valid readings, kept as printed:** कां सोस्मितां (verse 4), पद्म ऊरु (verse 17), हस्त्यश्वादिगवे रथम् (verse 19), ईश्वरींग् (verse 9, the page's ग् before स as the reciters say it; the standard writes it ईश्वरीङ्ग्, as the page's transliteration īśvarīṅg).
- **The repetitions in verse 31** (नारायणि नमोऽस्तु ते, three times), as printed and recited.
- **The closing (verse 37)**: य एवं वेद, the Gāyatrī with ॐ, and the śānti, printed as one verse with one number, kept as one item (type `uttara`).

## Structure (not on the page as such)
- **Numbering.** Each verse keeps the number the page prints (1–37).
- **Sections:** `sukta` (1–15, the fifteen ṛks the phalaśruti names: सूक्तं पञ्चदशर्चं), `phala` (16), `stotra` (17–37, under the page's heading स्तोत्रम्).
- **Types:** the ṛks 1–15 are mantras; 16 the phalaśruti; 34 the Gāyatrī; 37 the closing; the rest ślokas.

## Witnesses (`source/check.py`)
- **Sanskrit Wikisource, श्रीसूक्तम्**, two texts on one page (no edition named): the first, 27 verses (`source/witness/wikisource-1.txt`: our 1–22, 24 in another wording, 32–35), and the second, headed अन्यः पाठः, 36 verses in our order (`wikisource-2.txt`); compared separately, as they differ.
- **GRETIL, Ṛgveda khilāni** (Scheftelowitz, *Die Apokryphen des Ṛgveda*, Breslau 1906, from a Kashmir manuscript): khila 2.6 has our ṛks 1–15 and, as its own verses or as variants, our 16–26 and 29–36 (`gretil-khila.txt`), its IAST made Devanagari with the Kaṭha Upaniṣad's converter after its "."-divided vowels are joined by sandhi (`source/witnesses.py`).
- **The Gāyatrī (34, and the closing 37): the page's nominatives stay.** महालक्ष्मी च विद्महे विष्णुपत्नी च धीमहि is the khila's own reading (mahā.lakṣmī.ca.vidmahe.viṣṇu.patnī.ca.dhīmahi) and Wikisource's first text's; only its second text has महालक्ष्म्यै / विष्णुपत्न्यै. A reading the scholarly edition and a second witness share is not clearly wrong, whatever the grammar of later Gāyatrīs, and the recording sings the nominatives (its transcript: …लक्ष्मी च विद्महे … पत्नी च धीमहि). Verse 37's विष्णुपत्नी च धीमहि, which no witness has, keeps the page's form too.
- **Confirmed:** पद्माक्षि (17: both Wikisource texts; the khila padmākṣī), मात्सर्यं (22: the khila, Wikisource 2), भजेऽहम् (30: the khila; Wikisource 2 भजेहम्), जगदीश्वरीं (30: all), महीयते (35: all).
- **Settled on them:** पद्मसम्भवे (17), जपेत् without सदा (22), त्रिनेत्रां (30), in the table above.
- **Kept against all three:** पूरुषानहम् (15; the witnesses पुरुषान्: a valid Vedic form), ईश्वरीङ्ग् (9, the reciters' ग्).
- **The khila's own recension, not the recited text** (each listed in `source/check.py`): प्रमोदिनीम् (3), कांस्यस्मि तां हिरण्यप्रवाराम् … पद्मेस्थिताम् (4), तं पद्मनेमिम् … वृणोमि (5), कीर्तिं वृद्धिम् (7), क्षुत्पिपासामला (8), स्रवन्तु … चिक्लीता … गृहे (12), पक्वां … पुष्टाम् and सूर्याम् / चन्द्राम् exchanged (13, 14), दास्यो without अश्वान् (15), पद्मोरू … संहवे तं मे भजसि (17), अश्वदायै … (18), करोतु मे (19), धनमुत्सृजे (20), its shorter 24, श्रीर्लक्ष्मीः (29), वरां कुशा … वहन्ती … ताम् (30), शरधये … गौरी and no repeats (31), शुभगन्ध (32), लक्ष्मीं प्रियसखीम् (33), श्रीवर्चस्वम् … शुभमानम् … धान्यं धनम् (35), दारिद्र्यम् (36), and मम आवह for म आवह (1, 13, 14).
- **Wikisource's first text, its own wording and slips:** ॐ before verse 1, हिरण्यवर्णाम, आद्रां (4), प्रादुर्भुतो सुराष्ट्रे, -ऋध्दिं (7, 8), क्षुत्पपासा, जेष्ठां अलक्ष्मीं, सर्वानिर्णुद, गृहात (8), ईश्वरिं (9), श्रेयतां (10), स्रजन्तु सिग्धानि (12), पुष्टि (13), यष्टीं … लक्ष्मी (14), जुहुयाादाज्यम्, पञ्चदशर्च (16), पद्मउरू … तन्मे भजसि पद्मक्षि (17), अश्वदायै … लभतां (18), पुत्रपौत्रं … हस्ताश्वादि … करोतु मे (19), वसु … वरूणं … धनमस्तु मे (20), वृतहा (21), मात्सर्य (22), its 24 (पद्मानने पद्मविपत्रे … संनिधस्त्वं), धवलतरांसुक (32), देवी माधवी … लक्ष्मीं प्रियसखीं (33), श्रीवर्चस्वम् … आविधाच्छोभमानम् … धान्यं धनम् (35).
- **Wikisource's second text:** its सदा (22), (विष्णु) beside विश्व (24), साधके for साधिके (31), its datives (34).

## Word meanings
Every word has an entry in the shared dictionary (`library/glossary/sa.json`), checked in Monier-Williams and Apte. Sāyaṇa's commentary is not at hand here, so where a reading is open the dictionaries and the grammar decide, and no sense is put to any commentator. A word the recitation joins with a hyphen (the Taittirīya way) is one key, its words in `p`.
- **कां** (4): both readings, the interrogative "whom (indescribable)" first, then क "Brahman" (Monier-Williams). **सोस्मितां**: the sense from स्मित, "smiling"; the form is not split into parts.
- **मायान्तरायाश्च बाह्या अलक्ष्मीः** (6): मायाः अन्तराः याः च बाह्याः, "the illusions, the misfortunes within and without".
- **चिक्लीत** (12): not in Monier-Williams; the vocative of a name, its sense from Apte's चिक्लिद, "moisture" (√क्लिद्). **कर्दम** (11): the name, and "mud, clay".
- **Words the page prints apart inside a compound** (पद्म ऊरु, पुत्रपौत्र धनं, गम्भीरा वर्तनाभिः, स्तनभर नमिता, क्षीरसमुद्र राजतनयां, …): the first word's entry gives its own sense as the compound's first member; the last word's gives the whole compound's sense in brackets.
- **पुरुषान्** / **पूरुषान्** (2, 15) and the Gāyatrī's nominatives (34, 37) are glossed as printed.

## Meanings
`meanings/hi/scriptures.json` and `meanings/en/scriptures.json` rest on the mantra's words, their grammar and Monier-Williams and Apte; no reading is put to any commentator. Where the words allow more than one reading:

| Mantra | Settled reading | Why |
|---|---|---|
| m01 | हरिणीम्: "like a doe" | Monier-Williams' and Apte's first sense; हिरण्यवर्णाम् already gives the hue |
| m04 | कां: "her who is bliss" | क, "joy" (Monier-Williams); the interrogative leaves the sentence without a frame |
| m06 | मायान्तरायाश्च बाह्या अलक्ष्मीः: "the illusions within and the misfortunes without" | मायाः अन्तराः याः च बाह्याः, as our word meanings split it |
| m13 | पुष्करिणीम्: "like a lotus pool" | Monier-Williams' first, Ṛgvedic sense; m14 has करिणी for the elephant |
| m14 | यः left unrendered; करिणी "a she-elephant", यष्टि "a staff to lean on" | a masculine relative with no referent in the line; the refrain as in m13; Monier-Williams' यष्टि, "any support" |
| m20 | वरुणं धनमश्नुते: "wealth reaches Varuṇa" | वरुणम् accusative, धनम् nominative |
| m21 | the subject of ददातु is Indra (वृत्रहा), carried over | no other subject is in the words |
| m23 | अव ब्रह्म द्विषो जहि: "protect the Veda, strike down those who hate" | the words as printed apart: अव "protect", ब्रह्म "the Veda"; अव … जहि with ब्रह्मद्विषः ("strike down the haters of the sacred word") is also grammatical, but the text does not join the compound |
| m33 | क्षमाम्: "forbearance itself" | Monier-Williams' and Apte's first sense; "the earth" is their later one |
| m35 | पवमानम् the subject of both verbs: "the purifying Pavamāna is glorified; may it bestow …" | पवमानम् neuter nominative; no other subject is in the words |
