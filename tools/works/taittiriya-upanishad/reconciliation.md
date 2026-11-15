# Taittirīya Upaniṣad — how the text is settled

**Source of truth:** the shlokam.org page <https://shlokam.org/text/taittiriya-upanishad.htm>, allowed by the owner. Its HTML (fetched 2026-11-14) is in scriptures-data at `hinduism/veda/yajurveda/krishna-yajurveda/upanishad/taittiriya-upanishad/printouts/shlokam/taittiriya-upanishad.html`. It has 54 verse blocks, numbered vallī.anuvāka.paragraph (2.0.x and 3.0.x for the openings of vallīs 2 and 3). Each block has the Devanagari (`div.detail-sanskrit`), the page's transliteration (the `div.detail-text` after it), a colloquial spelling and an English translation. There are no svaras.

## Method
1. **Extract.** `source/extract.py` parses the HTML (not the rendered page): each block's Devanagari and transliteration, split at `<br>`, zero-width spaces removed. Only these two are kept; the page's English is not in this repository.
2. **Two witnesses.** `source/settle.py` turns the transliteration back into Devanagari (`source/taittiriya_text.py`) and compares every line, letters only. The two agree in every line but nine, and those differ only in how they write the sāman's pluta and one anusvāra (the transliteration's hāāāvu, ṛtāāāsya, '''ham for हा३वु, ऋता३स्य, ऽ३हम; ahaṃśloka for अहꣳश्लोक; adhilokam adhi- with a space): `WITNESS` names them, and settle.py stops if any other line differs. The two scripts come from one edition, so their agreement shows the extraction is right, not that the edition is: a slip they share is corrected below where the grammar, the sense or the Upaniṣad's own parallel lines show it is wrong (PLAYBOOK §2).
3. **Headings left out.** 21 blocks open with an editor's title (प्रथमा शीक्षावल्ली, संहितोपासनम्, व्याहृत्युपासनम् …; `HEADING` in settle.py). They are not the Upaniṣad's words and are not recited; our own topic headings stand in their place.
4. **The library's standard** (PLAYBOOK §3) is applied by the exporter: ꣳ before श ष स ह र (a Yajurveda text), a word-final ं before a vowel as म् (2.8.3 शतं आजानजानां → शतम् आजानजानां), the class nasal, ॥ and compact numbers (॥१॥), and the ISO 15919 transliteration made from the verse.

## Corrections (source/settle.py → FIX)

| Where | Page (both scripts) | Text | Why |
|---|---|---|---|
| 1.3.1 | आकाशः सन्धिः वायुः सन्धानम् | आकाशः सन्धिः । वायुः सन्धानम् | The daṇḍa is in the page's transliteration (sandhiḥ. vāyuḥ) and between every other pair of the list. |
| 1.3.1 | उपनिषदम् व्याख्यास्यामः | उपनिषदं व्याख्यास्यामः | A word-final m before a consonant is the anusvāra (Pāṇini 8.3.23; PLAYBOOK §3), as everywhere else on the page. |
| 1.3.2 | अथाधिजौतिषम् | अथाधिज्यौतिषम् | A dropped य: the same paragraph closes इत्यधिज्यौतिषम्, and 1.3.1 lists अधिज्यौतिषम्. |
| 1.3.4 | इतीमामहासꣳहिताः | इतीमा महासꣳहिताः | A missing space: इमाः महासंहिताः, as the next line writes एता महासꣳहिता. |
| 1.3.4 | वे`द | वेद | A stray accent mark (both scripts). |
| 1.5.1 | सर्वेलोक महीयन्ते | सर्वे लोका महीयन्ते | सर्वे needs the plural लोकाः (लोका before म); the page itself has सर्वे वेदा and सर्वे प्राण… in the next two paragraphs. |
| 1.5.2 | सर्वेवेदा | सर्वे वेदा | A missing space. |
| 1.5.3 | सर्वे प्राण महीयन्ते | सर्वे प्राणा महीयन्ते | The plural प्राणाः, as सर्वे वेदा. |
| 1.5.3 | चतस्रश्चतुर्ध | चतस्रश्चतुर्धा | The adverb चतुर्धा, "fourfold"; चतुर्ध is no word here. |
| 1.5.3 | सर्वेऽस्मैदेवा | सर्वेऽस्मै देवा | A missing space (अस्मै देवाः). |
| 1.6.1 | एषोऽन्तहृदय | एषोऽन्तर्हृदय | अन्तः + हृदय: the र् is dropped. |
| 1.7.1 | पाङ्क्तग् स्पृणोतीति | पाङ्क्तꣳ स्पृणोतीति | The page writes the anusvāra before a sibilant as ꣳ (gͫ) everywhere else; here only the g of it is left. |
| 1.8.1 | ॐꣳशोमिति | ओꣳशोमिति | ॐ already holds the nasal; with ꣳ after it the nasal is written twice. The syllable is ओꣳ (om̐ before श). |
| 1.9.1 | सत्यवचा राथी तरः | सत्यवचा राथीतरः | One name, Rāthītara (as पौरुशिष्टिः and नाको मौद्गल्यः after it). |
| 1.10.1 | सुमेध अमृतोक्षितः | सुमेधा अमृतोक्षितः | The predicate of (अहम्) अस्मि is the nominative सुमेधाः, सुमेधा before a vowel; सुमेध is no nominative. |
| 1.11.1 | आचार्योन्तेवासिनम् | आचार्योऽन्तेवासिनम् | आचार्यः + अन्तेवासिनम्: the avagraha is dropped. |
| 1.11.2 | त्वयोपास्यानि ।नो | त्वयोपास्यानि । नो | Spacing. |
| 1.11.4 | इत्येकादशऽनुवाकः | इत्येकादशोऽनुवाकः | एकादशः + अनुवाकः, as every other anuvāka closes. |
| 2.1.1 | ओषधीभ्योन्नम् | ओषधीभ्योऽन्नम् | ओषधीभ्यः + अन्नम्: the avagraha is dropped. |
| 2.6.1 | कश्चन गच्छती | कश्चन गच्छती३ । | The question's pluta, as its pair कश्चित्समश्नुता३ उ: गच्छती with a long ई is the plutated गच्छति, whose ३ is dropped; the daṇḍa closes the question as every line does. |
| 2.6.1 | बहुस्यां | बहु स्यां | Two words, "may I be many". |
| 2.7.1 | तदात्मान स्वयमकुरुत | तदात्मानꣳ स्वयमकुरुत | The accusative आत्मानम्, ꣳ before स; आत्मान is no form. |
| 2.7.1 | तत्वेव | तत्त्वेव | तत् + तु + एव. |
| 2.9.1 | आत्मान स्पृणुते (twice) | आत्मानꣳ स्पृणुते | As 2.7.1. |
| 3.2.1 | भुतानि | भूतानि | A typing slip; भूतानि in 3.1, 3.3–3.6. |
| 3.6.1 | आनन्दाध्येव | आनन्दाद्ध्येव | As अन्नाद्ध्येव, प्राणाद्ध्येव, विज्ञानाद्ध्येव (आनन्दात् + हि + एव). |
| 3.10.1 | एदद्वा | एतद्वा | As एतद्वै in the two lines before. |
| 3.10.1 | अन्ततोऽस्मा अन्न राध्यते | अन्नꣳ राध्यते | As अन्नꣳराध्यते in the lines before. |
| 3.10.5 | इमाँल्लोकन्कामान्नी | इमाँल्लोकान्कामान्नी | The accusative plural लोकान्, as इमान्. |
| 3.10.5 | हा ३ वु हा ३ वु हा ३ वु | हा३वु हा३वु हा३वु | The pluta mark joined to its syllable, as the page writes ऋता३स्य and समश्नुता३. |
| 3.10.6 | अहमन्नादोऽ३हमन्नादोऽ३अहमन्नादः | अहमन्नादोऽ३हमन्नादोऽ३हमन्नादः | The second repetition written as the first: the avagraha already stands for the elided अ. |
| 3.10.6 | मा३अऽवाः | मा३ऽवाः | The same: मा + अवाः, the अ elided and marked by ऽ. |
| 3.10.6 | ॥ ॐ शान्तिः शान्तिः शान्तिः ॥ (3.10.6) | ॐ शान्तिः शान्तिः शान्तिः ॥ | Written as the page's other śānti pāṭhas. |
| every सह नाववतु | तेजस्विनावधीतमस्तु (2.0.1, 2.9.1, 3.0.1) | तेजस्वि नावधीतमस्तु | तेजस्वि नौ अधीतम्: the page itself divides the words so in the closing śānti of 3.10.6, and the library's Kaṭha writes it so. One śānti pāṭha, one spelling. |

## Kept as the page has it
- **शीक्षा** with a long ī (ॐ शीक्षां व्याख्यास्यामः, इत्युक्तः शीक्षाध्यायः, शीक्षावल्ली): the page's spelling in the text and the closing words alike, a valid Vedic form; the part's title follows it.
- Words written together that the grammar allows either way: अनुकृतिर्हस्म, अप्योश्रावयेत्याश्रावयन्ति, आमायन्तु, प्रमाभाहि प्रमापद्यस्व, भूरिविश्रुवम्, य एषस्तन, प्राचीन योग्योपास्व, ओमितीदꣳसर्वम्, इदꣳसर्वम्, प्रवचनꣳसन्धानम्.
- उपास्व (1.6.2), a valid form of the imperative of उप + आस्.
- कदाचनेति (2.4.1) beside कुतश्चनेति (2.9.1): the Upaniṣad has both.
- The pluta in the sāman of 3.10.6 (ऋता३स्य, ना३भाइ, मा३ऽवाः, अदन्तमा३द्मि, अभ्यभवा३म्) and the page's ऽ३ order in अहमन्नादोऽ३हम्.

## Structure (not on the page as such)
- **ब्रह्मविदाप्नोति परम् is the first paragraph of anuvāka 2.1.** The page prints it as a block of its own (2.0.2, under the heading उपनिषत्सारसङ्ग्रहः, with no number) and starts 2.1 at तस्माद्वा एतस्मादात्मन; the anuvāka's one number, ॥१॥, closes तदप्येष श्लोको भवति after both. The tradition reads them as one paragraph, the first of the Brahmānandavallī's first anuvāka, so item 2.1.1 holds both, the page's 2.0.2 first.
- **The anuvāka's closing words** (इति प्रथमोऽनुवाकः ॥) stand on their own line at the end of its last paragraph; the page sometimes runs them on after the number.
- **The vallīs' closing words** (॥ इति शीक्षावल्ली समाप्ता ॥ …) are items of type `iti`, and the सह नाववतु the page prints after those of vallīs 2 and 3 are items of type `shanti` (`shanti.2.end`, `shanti.3.end`), as the page places them (README, "Differences from the other Upaniṣads").

## Open
- None. A second edition (sanskritdocuments.org) joins `source/witness/` when the owner supplies its printout; it is a check, and every reading above is settled without it.
