# श्रीविष्णुसहस्रनामस्तोत्रम् (Śrī Viṣṇu Sahasranāma Stotram)

Shelf: हिन्दू धर्म › नामावलि › भगवान विष्णु › श्रीविष्णुसहस्रनामस्तोत्रम् (`library/hinduism/namavali/vishnu/vishnu-sahasranama/`,
work id `vishnu-sahasranama`). The thousand names of Viṣṇu that Bhīṣma teaches Yudhiṣṭhira in the Mahābhārata,
Anuśāsana-parva (chapter 149 in the Gita Press edition), in Sanskrit (`sa`), as it is recited: the opening prayers, the
pūrva-pīṭhikā, the viniyoga and nyāsas, the dhyāna, the 108 ślokas of names, the uttara-pīṭhikā (phalaśruti), the closing
words and the closing ślokas. Both recordings end with the uttara-pīṭhikā; the nyāsas, the closing words and the closing
ślokas stay untimed.

## Sources
- **Text** (`text.txt`): the owner's base, vishnusahasranamam.in, *विष्णु सहस्रनाम (सहस्त्रनाम) संपूर्ण पाठ* (Sandeep
  Bhandari, updated 4 October 2026), printed to PDF by the owner (private copy outside this repository; pages 3–23 are
  the stotra). Its text layer splits conjuncts, so every line was read against the printed page. Only the stotra's own
  text is taken: the page's Hindi meanings, notes and menus are left out. Checked against the owner's second witness, a
  roman transliteration of the stotra (no diacritics), and, for doubtful readings, against sanskritdocuments.org's
  edition and the Mahābhārata's critical text. Every change from the base and every source used: `reconciliation.md`.
- **Recordings** (not yet timed; what each recites and in what order: `reconciliation.md`):
  - `ms-subbulakshmi` (the default): M. S. Subbulakshmi, YouTube `0tubv1OKDjg` (29:51); the text follows its order;
  - `vande-guru-paramparaam`: Vande Guru Paramparaam, “Vishnu Sahasranamam” (Ishaan Pai; YouTube `A4D-Zf-HJLI`, 30 minutes).
- **Meanings, word meanings:** none yet.

## Structure
- **Hierarchy:** one part › nine sections (pages) › the verse.
  - `mangala` (Opening Prayers): `mangala.sh1`–`sh6` (śloka 1–6) and `mangala.mantra` (ॐ नमो विष्णवे प्रभविष्णवे);
  - `purva` (Purva Peethika): `purva.sh7`–`sh22`; the base numbers the opening prayers and the pūrva-pīṭhikā as one run,
    ॥१॥–॥२२॥, so the pūrva-pīṭhikā starts at śloka 7;
  - `nyasa` (Viniyoga and Nyas): `viniyoga` (type `viniyoga`), `nyasa.rishyadi`, `nyasa.kara`, `nyasa.anga` (type
    `nyasa`: the ṛṣyādi-, kara- and ṣaḍaṅga-nyāsa) and `sankalpa` (type `sankalpa`);
  - `dhyana` (Dhyanam): `dhyana.dh1`–`dh7` (type `dhyana`, numbered 1–7 as printed), with `dhyana.mantra`
    (ॐ नमो भगवते वासुदेवाय, type `mantra`) after the second, which both recordings recite;
  - `stotra` (Stotra): `stotra.harih` (॥ हरिः ॐ ॥, type `mantra`) and `stotra.sh1`–`sh108`;
  - `uttara` (Uttara Peethika): `uttara.sh1`–`sh33`;
  - `iti` (Closing words): `iti`;
  - `upasamhara` (Closing Shlokas): `upasamhara.sh1`–`sh11`; `paryaya` (Alternative Closing Shlokas): `paryaya.sh1`–`sh13`.
- **Numbering:** a verse's `n` is its printed number; the numbers restart in each section, and every section has a name
  (`work.json` → `sections`), so a verse is cited by its own number within its section (“Stotra · Shloka 5”,
  “Uttara Peethika · Shloka 5”); no `cite` rule is needed. The base prints the closing ślokas without numbers; they are
  numbered 1–11 and 1–13 here so that each can be cited (`reconciliation.md`).
- **Speakers:** a speaker line (श्रीवैशम्पायन उवाच, युधिष्ठिर उवाच, भीष्म उवाच …) is the first line of the verse it introduces,
  as the Bhagavad Gītā and the Durgā Saptaśatī write them; the viniyoga opens with श्रीवेदव्यास उवाच.
- **Refrains:** the line the recitation adds after ślokas 107 and 108 and after uttara-pīṭhikā 22, 24, 25, 27 and 28
  (सर्वप्रहरणायुध ॐ नम इति …) is the last line of its verse, as the base prints it.
- **Verse types:** मन्त्र (`mantra`), विनियोग (`viniyoga`), न्यास (`nyasa`), सङ्कल्प (`sankalpa`), ध्यान (`dhyana`), श्लोक
  (`shloka`), समापन (`iti`).
- **Topics:** one per section, as the sections are named (the closing words have none). Item ids are permanent.

The folder's format: `tools/works/README.md`.
