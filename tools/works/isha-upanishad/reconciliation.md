# Īśāvāsya Upaniṣad — how the text is settled

**Source of truth:** the owner's printout of <https://shlokam.org/text/isha-upanishad.htm> (41 pages; private copy in scriptures-data at `hinduism/veda/yajurveda/shukla-yajurveda/upanishad/isha-upanishad/printouts/shlokam/isha-upanishad.pdf`). It gives the śānti mantra and mantras 1–18 in Devanagari with a transliteration, and no svara (accent) marks.

**Checked against:** the standard text, Vājasaneyi Saṃhitā 40 in the Kāṇva recension as commonly chanted (18 mantras). Where the printout and the standard text differ, the second witness is sanskritdocuments.org, *Īśāvāsyopaniṣat with Śāṅkarabhāṣya*: <https://sanskritdocuments.org/doc_upanishhat/IshAvAsyopanishadshAnkarabhAShya.html>.

## How it is read
- The printout's Devanagari **text layer is broken**. It drops every र् (repha and र् in conjuncts: पूणम् for पूर्णम्, सवम् for सर्वम्, तीत्वा for तीर्त्वा), doubles some vowel signs (देेवा, शुश्रुुम) and splits words at line ends. So the Devanagari is read from the **page images** (rendered at 200 dpi, each verse checked by eye).
- The printout's **transliteration layer is clean**. `check.py` converts it to Devanagari and compares it with `text.json` word for word. The only differences it allows are the corrections below. It also checks that our own transliteration (`t`) spells the same text as our Devanagari (`v`).
- The library's writing standard (docs/PLAYBOOK.md §3) applies: ॥ and compact verse numbers (`॥१॥`), Pāṇini's spelling, ꣳ (a Yajurveda text), the ISO 15919 transliteration made from the verse. The printout's `|` after ओं is a daṇḍa (।).

## Corrections to the printout

| Item | Printout | Settled | Why |
|---|---|---|---|
| m08 | स्ययम्भूर्याथातथ्यतो… (*syayambhūr*) | स्वयम्भूर्याथातथ्यतो… (*svayambhūr*) | A typo, in both scripts. The printout's own word list has स्वयम्भूः (*svayambhūḥ*), as do the standard text and sanskritdocuments.org. |
| m08 | …अस्नाविरंशुद्धम् अपापविद्धम् | …अस्नाविरं शुद्धमपापविद्धम् | शुद्धम् + अपापविद्धम् must join (म् before a vowel), as in the standard text and sanskritdocuments.org (…अस्नाविरꣳशुद्धमपापविद्धम्). The space falls after the anusvāra, as in Gita Press and most printings. This changes no letter, and it lets the line fit a phone screen. |
| m09 | ततो भूय इव ते तमोय उ विद्यायां रताः | …ते तमो य उ विद्यायां रताः | A missing space: तमः + ये + उ → तमो य उ. Mantra 12 of the same printout, the standard text and sanskritdocuments.org all have तमो य उ. |
| m16 | …व्यूह रश्मीन्समूह । / तेजः यत्ते रूपं… | …व्यूह रश्मीन्समूह तेजः । / यत्ते रूपं… | The printout misplaces the daṇḍa (and line break). तेजः is the object of समूह (“gather in your light”), and the printout's own translation reads it that way (“gather up thy burning light”). The standard text and sanskritdocuments.org (“…व्यूह रश्मीन् समूह तेजः । यत्ते रूपं…”) put the daṇḍa after तेजः, which is also why तेजः keeps its visarga. |
| shanti.1 | two lines ending …पूर्णमेवावशिष्यते ॥ | a third line ओं शान्तिः शान्तिः शान्तिः ॥ | The printout's word-by-word list for this mantra ends with ॐ शान्तिः शान्तिः शान्तिः, and the mantra is always recited with it. It is written ओं, like the first line. |

## Kept as printed (valid forms, not errors)
- अन्धन्तमः (m09) beside अन्धं तमः (m12): the same words, with the anusvāra written as a nasal. Both are standard.
- सम्भूति / संभूति, असम्भूतिम् / असंभवात्: the printout mixes the two spellings of the nasal; kept as printed.
- ओं (in the śānti mantra and m17) rather than ॐ: kept as printed in the verse lines.
- m14 संभूत्यामृतमश्नुते: kept. Śaṅkara reads it as असम्भूत्या (the अ lost in sandhi); the meaning notes this.
- The printout gives the śānti mantra once, at the start; it does not repeat it at the end, so neither does the text here.

## Meanings
At the owner's instruction for the Sanskrit texts, the meanings are not copied from the printout. `meanings/en.json` and `meanings/hi.json` are written for this library: one to three sentences per mantra, following Śaṅkara's reading, with other readings (Viśiṣṭādvaita, Sri Aurobindo) briefly in the footnotes. The printout's section headings (“Verses 1-2: Cosmos and Renunciation”, “3-8: The Nature of Atman”, “9-14: Vidya and Avidya”, “15-18: Closing Prayers”) are the topics, reworded. Its commentary (Śaṅkara's bhāṣya in M. Hiriyanna's 1911 translation) informed the meanings and is not reproduced.
