# श्रीमद्भगवद्गीता (Shrimad Bhagavad Gita)

Shelf: हिन्दू धर्म › ग्रन्थ › महर्षि वेदव्यास › श्रीमद्भगवद्गीता (`library/hinduism/granth/vyasa/bhagavad-gita/`, work id `bhagavad-gita`). The dialogue of Śrī Kṛṣṇa and Arjuna in the Bhīṣma-parva of the Mahābhārata, as Sañjaya tells it to Dhṛtarāṣṭra: 18 adhyāyas, 701 ślokas, in Sanskrit (`sa`), each adhyāya closing with its colophon (ॐ तत्सदिति …); before them, as an opening part, the nine verses of the Gītā Dhyānam (ॐ पार्थाय प्रतिबोधितां …), which the recordings chant first.

| Adhyāya | Ślokas | Adhyāya | Ślokas | Adhyāya | Ślokas |
|---|---|---|---|---|---|
| 1 अर्जुनविषादयोग | 47 | 7 ज्ञानविज्ञानयोग | 30 | 13 क्षेत्रक्षेत्रज्ञविभागयोग | 35 |
| 2 साङ्ख्ययोग | 72 | 8 अक्षरब्रह्मयोग | 28 | 14 गुणत्रयविभागयोग | 27 |
| 3 कर्मयोग | 43 | 9 राजविद्याराजगुह्ययोग | 34 | 15 पुरुषोत्तमयोग | 20 |
| 4 ज्ञानकर्मसंन्यासयोग | 42 | 10 विभूतियोग | 42 | 16 दैवासुरसम्पद्विभागयोग | 24 |
| 5 संन्यासयोग | 29 | 11 विश्वरूपदर्शनयोग | 55 | 17 श्रद्धात्रयविभागयोग | 28 |
| 6 आत्मसंयमयोग | 47 | 12 भक्तियोग | 20 | 18 मोक्षसंन्यासयोग | 78 |

## Sources
- **Text:** the owner's copy of sanskritdocuments.org's *Śrīmadbhagavadgītā* (https://sanskritdocuments.org/doc_giitaa/bhagvadnew.html: a JSON of the page, 701 verses in Devanagari and IAST with their speaker lines, the page's variant readings and each chapter's colophon), in `scriptures-data` at `printouts/sanskritdocuments/bhagavad-gita.json`. `source/make_text.py` makes `text.txt` from it; `source/corrections.json` holds every change, each with its reason (`reconciliation.md`). The page counts 701 verses: adhyāya 13 opens with Arjuna's question (प्रकृतिं पुरुषं चैव …) as verse 1.
- **Gītā Dhyānam:** the owner's printout of shlokam.org's "Gita Dhyanam" (https://shlokam.org/shloka/gita-dhyanam.htm), in `scriptures-data` at `printouts/shlokam/gita-dhyanam.pdf`, typed into `source/dhyana.txt` (`reconciliation.md`). Its meaning and word meanings are ours (`meanings/`, `source/words_ours.json`); shlokam.org's translation is not used.
- **Witness:** the Sanskrit of the public-domain dataset github.com/gita/gita (`data/verse.json`, 701 verses; a copy in `scriptures-data` at `printouts/gita-gita/verse.json`), compared word for word with the base (`reconciliation.md`).
- **Guide and check:** the owner's *Bhagavad-gītā As It Is* in Hindi (The Bhaktivedanta Book Trust; © BBT), in `scriptures-data` at `books/bbt/hindi.pdf`, for checking our word meanings and meanings. Its text layer is in a broken font mapping (ि read as ठ, थ as र् …), so it is read on its page images; it is copyrighted, so it checks facts and is never copied.
- **Hindi and English meaning** (`meanings/hi/scriptures.json`, `meanings/en/scriptures.json`, ours, "भावार्थ — शास्त्र" / "English meaning — Scriptures", shown first): reviewed meanings of every verse, one piece per verse line ("Meaning per line"), following Śaṅkara's reading with other well-known readings in footnotes. Each batch was written from the verse, its word meanings and Monier-Williams and Apte, starting from the owner's drafts, then reviewed, copy-audited against Besant and Telang (no run of ten words in common) and checked again against the verse, and the whole work made consistent (`docs/HOW-TO.md`, "Write our own meanings for a Sanskrit work"); the readings settled on the way are in `reconciliation.md`.
- **English meanings copied:** Annie Besant, *The Bhagavad-Gita*, 4th edition, 1922 (`meanings/en/besant.json`, "Annie Besant — English meaning"), and K. T. Telang, *The Bhagavadgîtâ*, Sacred Books of the East vol. 8, 1882 (`meanings/en/telang.json`, "K. T. Telang — English meaning"), both public domain, from the owner's copy, as given. Telang often renders several verses in one passage (1.4–6, 1.26–31 …): it sits under the last of them, as the Mānas's joint meanings do.
- **Word meanings** (`glossary/sa.json`, the work's own; Hindi and English): the drafts' word-by-word glosses, lined up with the words as the verse prints them and gathered per word by `source/words.py`; a word the shared dictionary has is left to it (four of its entries gained the Gītā's sense: देव, का, श्रेयो, तमः). The speakers' lines and the colophons have our own entries (`source/words_ours.json`). Root and grammar are not written yet.

## Sources and permissions
The Sanskrit text is public domain (sanskritdocuments.org: for personal study and research). Besant (1922) and Telang (1882) are public domain. The Bhaktivedanta Book Trust's book is the owner's copy, used only to check facts; nothing of it is published. No permission has been requested from sanskritdocuments.org.

## Structure
- **Hierarchy:** the Gītā Dhyānam (part and section `dhyana`, marked ॐ, nine verses of type `dhyana`, cited "Dhyan N"), then eighteen parts, the adhyāyas (keys `1` … `18`, each marked with its number in the list of parts and named by its yoga) › one section each, the adhyāya (`1` … `18`, labelled "Adhyay N" / "अध्याय N" in `work.json` → `sections`) › ślokas.
- **Numbering:** a verse's id is adhyāya.śloka (`2.47`), its `n` the number that ends it (॥४७॥); it is cited adhyāya.śloka (`work.json` → `cite`: `["part", "n"]`, "Shloka 2.47"), as the Gītā is always cited.
- **Items without a number:** each adhyāya's colophon (ॐ तत्सदिति …, type `iti`, `<adhyāya>.iti`), its last item.
- **Types:** `dhyana` (the Dhyānam's verses); `shloka`; `iti` (the colophon). A speaker's line (श्रीभगवानुवाच, अर्जुन उवाच, सञ्जय उवाच, धृतराष्ट्र उवाच) is the first line of the verse it opens, as the book prints it above the verse; at 1.21 and 1.28 it stands in the middle of the śloka, where Arjuna's words begin.
- **Lines:** one per half-śloka (anuṣṭubh), one per pāda (triṣṭubh), as the copy has them.
- **Topics:** none; each adhyāya is one page.

## How it is made
```bash
J=<clone of scriptures-data>/hinduism/granth/vyasa/bhagavad-gita/printouts/sanskritdocuments/bhagavad-gita.json
python3 tools/works/bhagavad-gita/source/make_text.py $J     # text.txt
python3 tools/works/bhagavad-gita/source/meanings.py $J      # meanings/
python3 tools/works/bhagavad-gita/source/words.py $J         # glossary/sa.json
python3 tools/works/export.py bhagavad-gita
```
They read the owner's copy from `scriptures-data`, so `regen_check.py` cannot run them: after changing a script or one of its data files, run it and diff what it writes.

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- The text itself: the Gita Dhyanam, the eighteen adhyāyas and their closing words naming each a yoga, the 701 ślokas with adhyāya 13 opening on Arjuna's question (`reconciliation.md`), the eleventh adhyāya's name.
- Wikipedia, "Bhagavad Gita" (https://en.wikipedia.org/wiki/Bhagavad_Gita, read through its mirrors): its place in the Bhīṣma-parva (chapters 23–40 of book 6), about 700 verses, Sañjaya's divine sight from Vyāsa and his telling to Dhṛtarāṣṭra, its ascription to Vyāsa, its themes (dharma, karma yoga, knowledge, meditation, bhakti), the Prasthānatrayī and the commentaries.
