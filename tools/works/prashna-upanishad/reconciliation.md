# Praśna Upaniṣad — how the text is settled

**Source of truth:** shlokam.org, "Prashnopanishad" (<https://shlokam.org/text/prashnopanishad.htm>), a page the owner allowed, saved as HTML (private copy in scriptures-data at `hinduism/veda/atharvaveda/upanishad/prashna-upanishad/printouts/shlokam/prashnopanishad.html`). It gives the śānti mantra and the six praśnas, mantra by mantra, in Devanagari without svaras, each with the page's transliteration, English and Śaṅkara's commentary in S. Sitarama Sastri's English. Each praśna's closing words are printed as the last line of its last mantra.

**Witnesses:**
- **The page's own transliteration.** `source/settle.py` converts it back to Devanagari and compares it with the page's Devanagari word by word. They agree in every word of all 68 blocks: the transliteration is made from the same Devanagari, so it confirms the page's encoding (no letter is lost or broken in the HTML), and its slips are the Devanagari's slips too. It is not an independent edition, so it never outvotes the grammar.
- **Śaṅkara's commentary as the page gives it** (English): it renders the words it explains, and confirms the reading where a slip leaves a non-word (below).
- **The Māṇḍūkya's settled śānti** (`tools/works/mandukya-upanishad/`): the same śānti mantra of the Atharvaveda's Upaniṣads.

The library's writing standard (docs/PLAYBOOK.md §3) applies: ॥ and compact verse numbers, Pāṇini's spelling, the ISO 15919 transliteration made from the verse, ं for ꣳ outside the Yajurveda.

## The text as read
- **Zero-width characters.** The page puts a joiner inside श‍ृ (शृणुयाम in the śānti; शृणोति, अनुशृणोति in 4.2 and 4.5); `settle.py` removes it, as the Māṇḍūkya does, and removes any zero-width space.
- **Numbers.** The page ends each mantra ॥ १.१॥ (praśna.mantra). The text ends it with the mantra's own number, ॥१॥, and cites it praśna.mantra (`work.json` → `cite`), as the Kaṭha does.
- **Closing words.** The page prints इति प्रश्नोपनिषदि प्रथमः प्रश्नः ॥ (… षष्ठः प्रश्नः) as the last line of each praśna's last mantra. Each is an item of its own, `1.iti` … `6.iti`, of type `iti`, in its praśna's section; the words are the page's.
- **Line breaks** are the page's, but two: 5.5 breaks अभि-ध्यायीत across two lines (the text keeps the word whole: पुरुषमभिध्यायीत at the end of the first line); 6.4 prints its number on a line of its own (it joins the line before).
- **ꣳ** in तुष्टुवांसस् (śānti) and यजूंषि (2.6): the page writes ꣳ, the Yajurveda's sign; this is the Atharvaveda, so ं.

## The śānti mantra
The page's śānti is the Māṇḍūkya's settled śānti (भद्रं कर्णेभिः … with the four स्वस्ति lines), word for word, but for one slip: स्थिरैरङ्गैस्तुष्**त**ुवाꣳसस्, a non-word (after ष the dental त becomes ट, Pāṇini 8.4.41; the verb is stu, तुष्टुवांसः), here as in its transliteration (tuṣtuvā-); the text has तुष्टुवांसस्, as the Māṇḍūkya. The page's eight short lines are laid out in the Māṇḍūkya's five, and यदायुः ends with । as there, so the two Upaniṣads show the same mantra the same way; `settle.py` checks that the two are equal.

## Corrections (all in `source/settle.py` → `FIX`)
Each is a slip of the page (a non-word, a broken form or a broken sandhi), shown by the grammar or the sense and confirmed where noted by Śaṅkara's commentary on the page.

| Mantra | The page | The text | Why |
|---|---|---|---|
| 1.3 | भगवन् कुते ह वा | भगवन् कुतो ह वा | कुते is no word; the question is "whence" (कुतः, before ह: कुतो), as the commentary renders it |
| 1.12 | शुक्लः प्रणस्तस्माद् | शुक्लः प्राणस्तस्माद् | प्रण is no word; the pair of the praśna is रयि and प्राण (the dark half is रयि, the bright half प्राण), as the commentary explains it |
| 2.4 | तस्मिंष्च | तस्मिंश्च | ष्च is no Sanskrit cluster: स् before च is श् (8.4.40), as तस्मिंश्च earlier in the same mantra |
| 2.4 | प्रातिष्टन्त | प्रातिष्ठन्त | the root is स्था (प्रतिष्ठ-), as प्रतिष्ठमाने and प्रतिष्ठन्ते in the same mantra |
| 2.4 | वाङ्मनष्चक्षुः | वाङ्मनश्चक्षुः | as तस्मिंश्च; the page writes वाङ्मनश्चक्षुः itself in 2.2 |
| 2.11 | प्राणैकर्षरत्ता | प्राणैकर्षिरत्ता | एकर्षि (the fire of the Ātharvaṇas) + अत्ता; एकर्षरत्ता is a broken form; the commentary names Ekarshi |
| 3.1 | कौशल्यश्चाश्वलायनः | कौसल्यश्चाश्वलायनः | one name, one spelling: the page writes कौसल्य in 1.1 and 6.1, and the commentary Kausalya |
| 3.4 | सम्रादेवाधिकृतान् | सम्राडेवाधिकृतान् | सम्राज् before a vowel is सम्राड् (8.2.36, 8.2.39); सम्राद् is no form of it; the commentary: the sovereign |
| 3.4 | एतन् ग्रामानोतान् ग्रामान् | एतान् ग्रामानेतान् ग्रामान् | the king's words "these villages, those villages": एतान् twice (accusative plural of एतद्, agreeing with ग्रामान्); एतन् and ओतान् are no forms; the commentary: "these villages and those" |
| 3.11 | तदेषः श्लोकः | तदेष श्लोकः | एषः drops its visarga before a consonant (6.1.132); the page writes तदेष श्लोकः in 1.10, 4.10 and 6.5 |
| 4.7 | स यथा सोभ्य | स यथा सोम्य | सोभ्य is no word; the address is सोम्य, as the page writes it in 4.10, 4.11 and 6.2; the commentary: good-looking youth |
| 4.7 | वसोवृक्षं | वासोवृक्षं | वास (dwelling) + वृक्ष: the tree the birds live in; वसो- is no stem here; the commentary: the tree meant for their abode |
| 4.8 | यादौ च गन्तव्यं च | पादौ च गन्तव्यं च | the organs are listed with their objects: हस्तौ … पादौ च गन्तव्यं च (the feet and what is walked to); यादौ is no word; the commentary: feet and what must be reached |
| 5.4 | विभुतिमनुभूय | विभूतिमनुभूय | विभूति (greatness, glory), with the long ū of the root भू; the commentary: having enjoyed greatness |
| 6.2 | यस्मिन्नताः षोडशकलाः | यस्मिन्नेताः षोडशकलाः | एताः (these) agreeing with षोडशकलाः; नताः does not fit the sense; the commentary: of whom these sixteen kalās are born |
| 6.6 | यथ मा वो मृत्युः | यथा मा वो मृत्युः | यथ is no word; यथा मा … परिव्यथाः "so that death may not trouble you"; the commentary: so that death may not harm you |

## Kept as the page has it
Where the page's reading is a valid form, it stays, though some printed editions differ:
- सौर्यायणी (1.1) and सौर्यायणि (4.1): both forms of the patronymic; each as printed.
- तान्ह स ऋषिरुवाच (1.2), उदयन्यत्प्राचीं (1.6): words joined in writing, as the page joins them.
- मनोकृतेनायात्यस्मिञ्शरीरे (3.3): मनोकृतेन is the Upaniṣad's own (Vedic) form, which the commentary explains as "by the act of the mind"; ञ्श, not ञ्छ (छ for श after न् is optional, 8.3.31 with 8.4.63).
- प्रातिष्ठते (3.5), नेयायते (4.2), मातरिश्व (2.11), परमऋषिभ्यो (6.8): Vedic forms, as printed.
- सर्व एवोत्क्रामन्ते … सर्व एवोत्क्रमन्ते (2.4): both forms of the verb, as printed.
- अन्योन्यसक्ताः अनविप्रयुक्ताः (5.6): the visarga kept before the vowel at the pāda's end, as printed.
- पुरिशयं (5.5): as printed.

## Divisions
The page divides the text into six "chapters", the six praśnas; they are the six parts, each one section. The topics are the śānti pāṭha and one per praśna, under our own names (the question each praśna answers). The page's mantra numbers, restarting in each praśna, are the text's.
