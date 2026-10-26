# Śrī Rudram — how the text is settled

**Source of truth:** the owner's printouts (PDF) of shlokam.org's two pages:
- https://shlokam.org/shloka/rudram-namakam.htm (89 pages)
- https://shlokam.org/shloka/rudram-chamakam.htm (47 pages)

The private copies are in `scriptures-data` at `hinduism/veda/yajurveda/krishna-yajurveda/samhita/shri-rudram/printouts/shlokam/`. Every page block has the Devanagari (with svaras), a transliteration (with accents), an English rendering and word glosses.

The printouts, not the live pages, are the source: the workspace cannot reach shlokam.org (the proxy refuses it), and the web-fetch tool only summarises a page and will not copy it.

## Method
1. **Extract.** `source/extract.py` reads the PDF text layer (PyMuPDF), classifies each line by type size and font (Devanagari 21.8 pt, transliteration, italic English, headings), and writes each block's Devanagari and transliteration lines to `source/<part>_raw.json`. The page's English and glosses are not kept in this repository.
2. **Mend the text layer.** The Devanagari text layer has systematic breaks that are not on the page. `source/rudram_text.py` → `norm_deva` mends them:
   - **Repeated svaras.** The same svara is often written twice: शि॒॒व → शि॒व, सर्वा᳚᳚ → सर्वा᳚. The page images show one.
   - **Repeated vowel signs.** A vowel sign is often repeated, with or without its svara: व्या॒ा॒धिने → व्या॒धिने, श्लोोक → श्लोक, ज्ञाात्र → ज्ञात्र, पृथि॒व्यांां → पृथि॒व्यां.
   - **Double visarga.** ःः → ः, as in प्रश्नःः and हरिःः.
   - **Dravidian short vowels.** The opening lines (गुरुभ्यॊ, ऒ३म्, हवामहॆ, ज्यॆष्ठराजं) and the प्रमुञ्च mantra use the short ॊ / ॆ / ऒ of a South-Indian Sanskrit encoding. Sanskrit has no short e or o, so they are written ो / े / ओ. The page's transliteration (o, e) agrees. The page image shows these glyphs.
   - **श्ड़्ण्व.** This is how the text layer renders शृण्व (śṛṇvan in the transliteration).
   - **Zero-width spaces.** Removed. The page puts one inside र्‌ष (वर्​ष, बर्​हिः, मर्​शनः) only to stop a ligature.
3. **Settle against two witnesses.** `source/settle.py` converts the page's own transliteration back to Devanagari and compares it with the mended text, part by part. It folds only conventions (visarga sandhi written as स्स, a line-final svara, ँ before व/य). Every remaining difference is checked against the page image and against the Taittirīya Saṃhitā (4.5 Namakam, 4.7 Chamakam); the corrections below are the result. After them, the only differences left are conventions:
   - च्छ / chCh;
   - the page's own spelling अर्ण॒वें᳚-ऽतरि॑क्षे, which the image confirms;
   - नमस्स / नमः स.
4. **Items.** One item per mantra (below). `t` is not the page's transliteration. It is made from the settled Devanagari, in the library's IAST convention (c for च, ṁ for anusvāra, e/o without macron, "," for a daṇḍa, ॥N॥), and it keeps the svaras as accents: ◌̍ for ॑, ◌̠ for ॒, ◌̎ for ᳚. So it always agrees with the Devanagari.

## Corrections (all in `source/settle.py` → `FIX`)
Most restore a reph (र्) that the PDF text layer drops. The page image and the page's transliteration both show it.

| Where | Text layer | Text used | Evidence |
|---|---|---|---|
| Namakam 1.10 (प्रमुञ्च) | प्रमुंच धन्वनस्त्वमुभयॊरार / नियॊज्याम् । याश्च तॆ हस्त इषवः परा ता भगवॊ वप । (no svaras) | प्रमु॑ञ्च॒ धन्व॑न॒स्त्वमु॒भयो॒रार्त्नि॑यो॒र्ज्याम् । याश्च॑ ते॒ हस्त॒ इष॑वः॒ परा॒ ता भ॑गवो वप ॥ | The page's Devanagari for this one mantra has no svaras and loses the reph of आर्त्नियोर्ज्याम्. Its transliteration (pramu̍ñcha̠ … ā̠rtni̍ yō̠rjyām … vapa ॥) has both, as does TS 4.5.1. The svaras and the closing ॥ follow the page's transliteration. |
| Namakam 2.10 | नमो॑ म॒न्त / णे॑ वाणि॒जाय॒ | नमो॑ म॒न्त्रिणे॑ वाणि॒जाय॒ | ्रि lost at a line break in the text layer; the image shows मन्त्रिणे |
| Namakam 4.13 | क॒मारे᳚भ्यश्च | क॒र्मारे᳚भ्यश्च | reph; ka̠rmārē̎bhyaścha |
| Namakam 5.2 | श॒वाय॑ | श॒र्वाय॑ | reph; śa̠rvāya |
| Namakam 9.12 | पणश॒द्या॑य | पर्णश॒द्या॑य | reph |
| Namakam 10.1 | मा भेमा-ऽरो॒ | मा भेर्मा-ऽरो॒ | reph; bhērmā |
| Namakam 10.3 | अ॒स / न्नना॑तुरम् | अ॒स्मिन्नना॑तुरम् | ्मि lost at a line break; a̠sminnanā̍turam |
| Namakam 10.5 | म्प्रि / या | म्प्रि॒या | the text layer loses the svara at a line break; pri̠yā |
| Namakam 11.2 | अ॒स / न्म॑ह॒त्य॑र्ण॒वें᳚ | अ॒स्मिन्म॑ह॒त्य॑र्ण॒वें᳚ | ्मि lost at a line break; image p. 76 |
| Namakam 11.2 | श्श॒वा अ॒धः | श्श॒र्वा अ॒धः | reph; image p. 76 |
| Namakam 11.7 | ती॒थानि॑ | ती॒र्थानि॑ | reph; image p. 78 |
| Namakam 11.10 | प्राची॒दश॑ … प्र॒तीची॒-दशो-दी॑ची॒- / दशो॒ध्वास् | प्राची॒र्दश॑ … प्र॒तीची॒-र्दशो-दी॑ची॒-र्दशो॒र्ध्वास् | reph ×4; image p. 78. The three page lines are re-broken at sense breaks; on the page the word व॒र्ष॒ breaks across two lines. |
| Closing 1 (त्र्यम्बकम्) | मृत्यो॑मुक्षीय | मृत्यो॑र्मुक्षीय | reph |
| Closing 2 | वि॒वेश॒ तस्म / रु॒द्राय॒ | वि॒वेश॒ तस्मै॑ रु॒द्राय॒ | ै॑ lost at a line break; tasmai̍ |
| Chamakam 1.1 | स॒जोष॑से॒माव॑धन्तु; द्यु॒म्नैवाजे॑भि॒ | स॒जोष॑से॒माव॑र्धन्तु; द्यु॒म्नैर्वाजे॑भि॒ | reph; image p. 2 |
| Chamakam 3.6 | ध॒ता च॑ | ध॒र्ता च॑ | reph |
| Chamakam 3.13 | दीघायु॒त्व | दीर्घायु॒त्व | reph |
| Chamakam 4.11 | पू॒ण … पू॒णत॑र | पू॒र्ण … पू॒र्णत॑र | reph |
| Chamakam 6.9 | त्वष्ठा॑ | त्वष्टा॑ | **The page itself** (Devanagari and transliteration, tvaṣṭhā) has ठ. The god is Tvaṣṭṛ, nominative त्वष्टा (TS 4.7.6), so this is a plain misspelling. |
| Chamakam 6.17, 11.15 | मू॒धा | मू॒र्धा | reph |
| Chamakam 8.8 | हवि॒धान॑ | हवि॒र्धान॑ | reph |
| Chamakam 9.1 | घ॒मश्च॑ मे॒-ऽकश्च॑ | घ॒र्मश्च॑ मे॒-ऽर्कश्च॑ | reph ×2 |
| Chamakam 10.2 | त्र्य॒वीच॑ मे | त्र्य॒वी च॑ मे | **the page itself** (Devanagari and transliteration) runs the two words together; च is the separate “and” of every line |
| Chamakam 11.9 | त्रय॑स / ग्ंशच्च | त्रय॑स्त्रिग्ंशच्च | ्त्रि lost at a line break; traya̍strigṃśachcha |
| Śānti | देव॒हू-मनु॑यज्ञ॒नी-बृह॒स्पति॑; पृथि॑विमात॒मा; हिग्ंसी॒मधु॑ | देव॒हू-र्मनु॑र्यज्ञ॒नी-र्बृह॒स्पति॑; पृथि॑विमात॒र्मा; हिग्ंसी॒र्मधु॑ | reph ×5; dēva̠hū-rmanu̍ryajña̠nī-rbṛha̠spati̍ … māta̠rmā … higṃsī̠rmadhu̍ |

## Kept as the page has it
- **Readings or spacing that differ from some TS editions.** These stay as printed: हिर॑ण्य बाहवे (TS हिर॑ण्यबाहवे); पाग्ं स॒व्या॑य (पांस॒व्या॑य); आनिर् ह॒तेभ्यो; भुव॑ना वि॒वेश॒ (भुव॑नाऽऽवि॒वेश॑); स्वगाका॒रश्च॑ without the svara on स्व; परि॑णो; [शङ्क॒राय॑] in square brackets. The doubt here is about spacing or a single accent, not the words, so the page is followed.
- **The page's sandhi spellings.** These are the recitation forms of the Taittirīya tradition: -ञ्च, -म्पत॑ये, नम॒-स्स, ग्ं, the ँ in विँश्वा, येँ᳚, सं॒विँच्च and त्र्यम्बकं-यँजामहे, and अर्ण॒वें᳚-ऽतरि॑क्षे.
- **The pluta.** ओ३म् is kept with its pluta ३.

## Structure (not on the page as such)
- **Numbering.** The page numbers only the end of each anuvāka (॥१॥ … ॥११॥) and gives no mantra numbers. Each anuvāka is split into its mantras:
  - **Anuvākas of ṛks** (Namakam 1, 10 and 11.1–11.3): a ṛk per item, as the page's own blocks divide them.
  - **The other anuvākas:** one item per line, as the page prints them. Each line is one नमो … नमो or … च मे unit.
  - **Namakam 11.4–11.10:** in the one block, each "ये …" line is its own item, then the refrain तेषाग्ं …, then the closing prose.
  - **Chamakam 1.1:** the opening ṛk अग्ना॑विष्णो … is one item.
  - Mantras are numbered within the anuvāka (`n` = "anuvāka.mantra", e.g. 8.11).
- **The parts the page has outside TS 4.5 / 4.7** are placed in their own sections:
  - **Opening:** अथ श्रीरुद्रप्रश्नः (the heading, used as the topic), गुरुभ्यो नमः, गणानां त्वा, the TS heading, ओ-न्नमो भगवते रुद्राय. The page shows the last of these under its "1st Anuvaka" label, but it is an invocation, not part of TS 4.5.1.
  - **After anuvāka 1:** श्री शम्भवे नमः and नमस्ते अस्तु भगवन्….
  - **After anuvāka 11:** the closing mantras (त्र्यम्बकम् … ओ-न्नमो भगवते रुद्राय विष्णवे …) and सदाशिवोम् / शान्ति.
  - **Chamakam:** its śānti mantra.

## Two more misprints in the printout's Devanagari

The printout's own transliteration and the standard Taittirīya Saṃhitā agree against its Devanagari in two places; the Devanagari is corrected, as with त्वष्टा above:
- Namakam 3.12: printed "नमो-ऽस्स॑द्भ्यो॒ विद्य॑द्भ्यश्च" → **नमो-ऽस्य॑द्भ्यो॒ विध्य॑द्भ्यश्च** (transliteration "'syadbhyo viddhyadbhyaśca"; TS 4.5.3 अस्यद्भ्यो विध्यद्भ्यश्च, "to those who shoot and to those who pierce", from अस् and व्यध्).
- Chamakam 8.2: printed "दिष्णि॑याश्च" → **धिष्णि॑याश्च** (transliteration "dhiṣṇiyāśca"; TS 4.7.8 धिष्णियाः, the side-altars).

Kept as printed, because the printout's transliteration agrees: "मृत्यु॑र्मे पा॒हि" (Namakam closing), "मनु॒राय॑जे" (Namakam 10).
Meaning: Chamakam 8.4 स्वरवः are the svarus, chips cut from the sacrificial post (Sāyaṇa: यूपशकलाः), not "wooden pegs".

## "श्री शम्भवे नमः" left out
The printout has "श्री शम्भ॑वे॒ नमः॑ ॥" before "नमस्ते अस्तु भगवन्"; it is not recited, and the owner asked for it to be left out. `source/settle.py` leaves it out; the opening mantras are numbered 1–4.

## The closing mantras in the recording's order
The owner: "In Namakam, the ending verses are jumbled up and don't match the order in the recording", and chose the recording's order. The printout lists त्र्यम्बकं (u1), यो रुद्रो (u2), तमु ष्टुहि (u3), यक्ष्वामहे (u4), अयं मे हस्तो (u5), ये ते सहस्रम् (u6), मृत्यवे स्वाहा (u7), ओं नमो भगवते रुद्राय विष्णवे (u8). Shlokam's recording (GbQM33333xs) sings u1 u2 u6 u7 u8 and then u3 u4 u5 before the śānti (transcript, 1170–1253 s; the प्राणानां ग्रन्थिरसि line is part of u8 and is sung before ओं नमो भगवते). `source/settle.py` (ORDER_FIX) moves u3–u5 after u8; the ids stay, the numbers 1–8 follow the recording's order. The text of each mantra is unchanged.
