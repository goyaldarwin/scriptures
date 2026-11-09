# श्रीशिवमहापुराण (Shri Shiv Mahapuran)

Shelf: हिन्दू धर्म › पुराण › महापुराण › श्रीशिवमहापुराण (`library/hinduism/purana/mahapurana/shiva/`, work id `shiva-purana`). The Śrī Śivamahāpurāṇa of Maharṣi Vedavyāsa in its seven saṃhitās and 457 adhyāyas, with the Śivapurāṇa Māhātmya (seven adhyāyas) that Gita Press prints before it: 24,676 verses and passages, in Sanskrit (`sa`), each adhyāya closing with its इति words.

| Part | Adhyāyas | Verses |
|---|---|---|
| Māhātmya | 7 | 373 |
| Vidyeśvara-saṃhitā | 25 | 1,541 |
| Rudra-saṃhitā, Sṛṣṭi-khaṇḍa | 20 | 1,222 |
| Rudra-saṃhitā, Satī-khaṇḍa | 43 | 2,313 |
| Rudra-saṃhitā, Pārvatī-khaṇḍa | 55 | 2,704 |
| Rudra-saṃhitā, Kumāra-khaṇḍa | 20 | 1,080 |
| Rudra-saṃhitā, Yuddha-khaṇḍa | 59 | 2,956 |
| Śatarudra-saṃhitā | 42 | 2,189 |
| Koṭirudra-saṃhitā | 43 | 2,189 |
| Umā-saṃhitā | 51 | 2,694 |
| Kailāsa-saṃhitā | 23 | 1,287 |
| Vāyavīya-saṃhitā, Pūrva-khaṇḍa | 35 | 1,765 |
| Vāyavīya-saṃhitā, Uttara-khaṇḍa | 41 | 2,363 |

## Sources
- **Text:** the owner's copy of sanskritdocuments.org's *Śrīśivamahāpurāṇam* (a JSON of its twelve pages: 464 chapters, Devanagari and IAST), in `scriptures-data` at `printouts/sanskritdocuments/shiva-purana.json`. It follows the Gita Press edition (code 2223, *Śrīśivamahāpurāṇa, mūla saṃskṛta śloka–hindī vyākhyāsahita*, and its second part, code 2224) verse for verse: its numbering, its speaker lines, its readings. `source/make_text.py` makes `text.txt` from it; `source/corrections.json` holds every choice made on it, each with its reason.
- **The printed witnesses**, in `scriptures-data` at `books/gitapress/`: `shiv-1.pdf`, the owner's scan of Gita Press code 2223 (the Māhātmya, the Vidyeśvara- and the Rudra-saṃhitā, Sanskrit with Hindi), and `kalyan-2018-uttarardh.pdf`, his scan of Kalyan's *Śrīśivamahāpurāṇāṅka* (January 2018: the Śatarudra- to the Vāyavīya-saṃhitā in Hindi only, with the verse numbers). Both are page images without a text layer; their Hindi is read by OCR, the owner's choice for these scans (below).
- **Web witnesses** (the owner asked for web lookups wherever the copy is in doubt): wisdomlib.org's *Shiva Purana [sanskrit]*, which follows the Gita Press numbering, for a verse the copy drops; Gita Press's abridged Hindi published online (gurujimaharaj.com, mahashivpuran.wordpress.com) for a Hindi word under an ink blot (`reconciliation.md`).
- **English meaning** (`meanings/en/scriptures.json`, ours, "English meaning — Scriptures"): the owner's drafts, written from each verse, in `scriptures-data` at `meaning-records/en-scriptures/shiva-purana-drafts.json`, brought to `tools/meanings/style.md`: implied words written into the sentence, speech without quotation marks, "!" only where the verse exclaims, British spelling; each verse that opens with a speaker's line begins "X said:" from one table of the 320 speaker lines; the closing words translated in one pattern ("Thus ends the fifth adhyāya, named …, in …"). The owner's choice: they stand until a reviewed meaning replaces them (`docs/PLAYBOOK.md` §4).
- **Word meanings** (`glossary/sa.json`, English only): the drafts' word-by-word glosses, lined up with the words as the verse prints them and gathered per word by `source/words.py`; a word the shared dictionary has is left to it. Hindi, root and grammar are not written yet (`work.json` → `"words": "partial"`).
- **Hindi meaning** (`meanings/hi/gitapress.json`, copied, "Gita Press — Hindi translation"): Gita Press's Hindi, the Māhātmya to the Yuddha-khaṇḍa from code 2223 and the rest from Kalyan 2018, read from the owner's scans by OCR (the owner's choice for these scans, which have no text layer; recorded in each scan's `.meta.json`): two passes merged, every word they read differently or the word list lacks read by eye on its printed line, and then every paragraph proofread against its page (`source/hindi/README.md`). Each paragraph sits under the last verse its mark names. Not yet carried: the books' footnotes (`reconciliation.md`).

## Sources and permissions
The Gita Press books and the copy of sanskritdocuments.org's text are the owner's, used for personal study; sanskritdocuments.org's pages are for personal study and research, and the Sanskrit text is public domain. No permission has been requested from Gita Press or sanskritdocuments.org.

## Structure
- **Hierarchy:** thirteen parts (the Māhātmya; the Vidyeśvara-saṃhitā; the Rudra-saṃhitā's five khaṇḍas; the Śatarudra-, Koṭirudra-, Umā- and Kailāsa-saṃhitā; the Vāyavīya-saṃhitā's two khaṇḍas) › adhyāyas (sections `m.1` … `m.7`, `1.1` … `1.25`, `2.1.1` … `2.5.59`, `3.1` … `6.23`, `7.1.1` … `7.2.41`; numbered: `work.json` → `cite.sec` names them "Adhyay" / "अध्याय") › verses. The part keys (`1`, `2.1` … `2.5`, `3` … `6`, `7.1`, `7.2`) are the copy's and wisdomlib's numbers for the books, and the mark beside each part in the list of parts.
- **Numbering:** a verse's id is its adhyāya's section and its number as the book prints it (`1.1.5`, `2.3.27.12`, `7.2.4.30`); in the Māhātmya `m.<adhyāya>.<verse>`. Its `n` is the number that ends it (॥५॥). A verse is cited part.adhyāya.verse (`work.json` → `cite`: "Shloka 2.3.27.12", "Shloka 1.1.5"); a verse of the Māhātmya (type `mshloka`) adhyāya.verse within the Māhātmya ("Shloka 3.12").
- **Items without a number:** an adhyāya's opening maṅgala-śloka (`1.1.0`, `3.1.0`), a prose passage before an adhyāya's first verse (`2.5.49.0`, Śukra's namaskāra; `6.19.0`, the list of mahāvākyas), and each adhyāya's closing words (`<adhyāya>.iti`). They are named by their type.
- **Types:** `shloka`; `mshloka` (a śloka of the Māhātmya); `gadya` (prose); `iti` (the closing words of each adhyāya). A speaker's line (सूत उवाच, ब्रह्मोवाच) is the first line of the verse it opens, as the book prints it above that verse.
- **Lines:** one line per half-verse for anuṣṭubh, one per pāda for longer metres, as the copy has them.
- **Topics:** one heading per adhyāya, ours (`docs/PLAYBOOK.md` §4: the work shows our meanings first), in Hindi and plain English, written from the adhyāya's own title (the …नाम of its closing words) and its opening verses: `source/topics.json`, read by `make_text.py`. **Loading:** by part (`"load": "parts"`).

## How it is made
```bash
D=<clone of scriptures-data>/hinduism/purana/mahapurana/shiva
python3 tools/works/shiva-purana/source/make_text.py $D/printouts/sanskritdocuments/shiva-purana.json tools/works/shiva-purana
python3 tools/works/shiva-purana/source/words.py <clone of scriptures-data>/hinduism/purana/mahapurana/shiva/meaning-records/en-scriptures/shiva-purana-drafts.json
```
They read the owner's copy from `scriptures-data`, so `regen_check.py` cannot run them: after changing a script or `corrections.json`, run it and diff `text.txt` (and `glossary/sa.json`). It stops on any verse number out of sequence, any unnumbered lines it cannot place and any id used twice. `reconciliation.md` lists every difference from the copy and why.

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- The text itself: 1.1.1–3 (the sages' sacrifice at Prayāga, where the Gaṅgā meets the Yamunā, and Sūta, Vyāsa's disciple), the seven saṃhitās and the Rudra-saṃhitā's five khaṇḍas, the topics (the linga and Śiva's teaching of Om and the pañcākṣara in the Vidyeśvara; Satī, Pārvatī's tapas and marriage, Kārttikeya, Gaṇeśa, Tripura in the Rudra; the avatāras in the Śatarudra; the twelve jyotirliṅgas and Śivarātri in the Koṭirudra), the Māhātmya's colophons (स्कान्दे महापुराणे) and topics (Devarāja, Cañculā, Binduga, the way to hear it).
- Wikipedia, "Shiva Purana" (https://en.wikipedia.org/wiki/Shiva_Purana, and its mirrors): one of the eighteen Mahāpurāṇas and Shaiva literature; its claim to have had 100,000 verses in twelve saṃhitās, abridged by Vyāsa; the seven-saṃhitā recension; hindupedia.com, "Śivapurāṇa": 24,000 verses in seven saṃhitās.
