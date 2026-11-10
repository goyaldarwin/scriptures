# Audit of the Chālīsā, Āratī and Nāmāvalī shelves

Every work and recording that the pull request adding these shelves brought in was read again, work by work, for six kinds of error: A spelling and names, B the text against its sources, C the audio, D meanings against the verse, E word meanings (the verse's words and the underlined words of our meanings), F shelves and titles. Each work below lists what was read and found (the reviewer's checklist), then every finding: **fixed** (checked against the source before it was applied), **fixed by hand** (the reviewer's fix was not right as given; the right one was made), **covered** (fixed where the shared dictionary entry was rewritten as a general one), or **not taken** (with the reason). Every fix is in the data; the readings decided are in each work's `reconciliation.md`, the audio starts in each recording's `fixes.md`.

The owner's two reports and their classes: the Sathya Sai name is साई everywhere (text, titles, meanings, word entries, shelf, README, reconciliation); every song inside a jukebox has its own start and end, so the player starts at its first verse, stops at its end and shows its own length.

## Jai Ahoi Mata (`ahoi-aarti`)
- Witnesses read: Aarti Mala page image i-335 (base); Drik Panchang ahoi-mata-aarti.html (whole text). Randhir i-189/190 not a witness (per reconciliation).
- Verses compared: 8 (tek + 7 stanzas), word by word; every difference is in reconciliation.md.
- Meanings read: 8 hi / 8 en. Words read: ~110 verse words + 9 underlined.
- Title/shelf: work.json title, index.json entry (ahoi group) checked.
- A: no errors. B: text matches base with recorded corrections. D: meanings match verses. E: 2 (ले sense; कर grammar). F: fine.
- Findings:
  - E `aarti.pad4`: ले in 'कर ले' (does, manages to do) opens only 'लेकर / taking, carrying', a sense that cannot fit this line. — **fixed**
  - E `aarti.pad4`: The shared entry कर has g=संज्ञा for all its senses, though the sense used here (कर न सके, कर ले) is a verb; — **fixed by hand**

## Jai Ambe Gauri (`ambe-aarti`)
- Witnesses read: Randhir book page images i-176, i-177 (base); Drik Panchang ambe-mata-aarti.html (whole). Aarti Mala i-336 not reopened (used only for noted variants).
- Verses compared: 13 (tek + 12), word by word; the three recording-led lines (st. 2, 4, 12) confirmed word for word in Drik Panchang.
- Meanings read: 13 hi / 13 en. Words read: ~180 verse words + ~30 underlined.
- Title/shelf: work.json and index.json (durga group) checked.
- A: none. B: none (all differences recorded). D: none. E: 3 (श्यामा no Goddess sense; श्रीमालकेतु guess stated as fact; Hari underline about the Mānas). F: none.
- Findings:
  - E `aarti.tek`: श्यामा in 'मैया जय श्यामा गौरी' (the dark Goddess, Durgā/Kālī) opens a shared entry with no sense for the Goddess: — **covered**
  - E `aarti.pad11`: The verse word श्रीमालकेतु (and the Hindi meaning's underlined श्रीमालकेतुमें) opens 'माँका एक धाम / a seat of the Mother', a guess stated as fact; — **fixed**
  - E `aarti.tek`: The English meaning's underlined 'Hari' opens an entry about the Mānas ('in the Mānas also Śrī Rāma'), which is beside the point in a Durgā āratī. — **covered**
- Recording `anuradha-paudwal` (YouTube sd31yGqZFlA): plays start 900.46 s, end 1349.9 s. Starts heard in 5-s windows: 8 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: none.

## Barambar Pranam Maiya Barambar Pranam (`annapurna-aarti`)
- Witnesses read: Randhir book page image i-244 (base); Drik Panchang annapurna-mata-aarti.html (whole). Aarti Mala i-337 not used for readings (per reconciliation).
- Verses compared: 6 (tek + 5), word by word: all match the book; differences only standard ones, recorded.
- Meanings read: 6 hi / 6 en. Words read: ~95 verse words + ~25 underlined.
- Title/shelf: work.json and index.json (annapurna group) checked.
- A: none. B: none. D: 1 (low: 'beside you' added in pad2; the Hindi 'आपके आगे' would change with it). E: 2 (देवियों underline opens vocative देवि; देव falls back to a Sanskrit entry). F: none.
- Findings:
  - E `aarti.pad4`: In the Hindi meaning, देवियों ('goddesses') is underlined and opens the entry देवि 'हे देवी! (आदरणीय स्त्री या रानीका सम्बोधन) / O lady, O queen (respectful address)', a vocative that cannot fit; — **fixed**
  - E `aarti.pad4`: The verse word देव ('gods', in 'देवी देव', a Hindi line) has no Hindi entry and falls back to the Sanskrit entry 'हे देव! / देव, प्रकाशमान देव (‘इति’ से पहले देवः)' with grammar 'संज्ञा, पुंलिंग / सम्बोधन एकवचन' and an ' — **fixed**
  - D `aarti.pad2`: 'आपके आगे' / 'beside you' is added to 'कहाँ कृष्ण कहाँ राम'; — **not taken: the rhetorical question (कहाँ कृष्ण कहाँ राम) is a comparison with her; the meaning keeps it**

## Shri Annapurna Chalisa (`annapurna-chalisa`)
- Witnesses read: book page images i-240, i-241, i-242, i-243 (pp. 241–244; zoomed crops of doubtful lines: cau7 अग्नि, cau20–25, cau29–31, cau32 चण्डि); Drik Panchang printout annapurna-mata-chalisa.html (drik.py).
- Verses compared: 42 (2 dohās, 40 chaupāīs), every line against the book and Drik; every difference found is in reconciliation.md.
- Meanings read: 42 hi / 42 en, plus every underlined word's entry.
- Words read: all verse words of 42 verses (about 330 tokens), each entry checked against its line.
- Title / shelf: work.json title hi/en, by; library/index.json entry (chalisa › annapurna) against sibling chālīsās.
- A (spelling, names): no error found in text, meanings or titles.
- B (text vs witnesses): text agrees with the book line by line except the corrections recorded in reconciliation.md; nothing unrecorded.
- D (meanings): hi and en agree and follow each verse; nothing to report.
- E (word meanings): 6 findings: shared en entries girijā, bhavānī (Mānas-only gloss); awa मोहे, अभय, होहिं, पावा lack the sense the line needs.
- F (title, shelf): consistent with siblings; nothing to report.
- Findings:
  - E `chalisa.cau9`: The English meaning's underlined 'Girijā' (also cau27, cau33) opens the shared en entry that says Pārvatī is the one 'to whom Śiva tells the Mānas': — **covered**
  - E `chalisa.cau22`: The English meaning's underlined 'Bhavānī' opens the shared en entry 'to whom Śiva tells the Mānas', a Mānas-only gloss that misleads here (Bhavānī answering Brahmā). — **covered**
  - E `chalisa.cau29`: मोहे in 'करमँह अपर पाश मन मोहे' is 'enchants (the mind)', present; — **fixed**
  - E `chalisa.cau1`: अभय in 'वर-अरु अभय भाव' is the gift of fearlessness (abhaya, with vara: — **fixed**
  - E `chalisa.cau25`: होहिं in 'शंभुनाथ पुनि होहिं हमारा' is optative ('may (he) be mine again', as the meanings say: — **fixed**
  - E `chalisa.cau7`: पावा in 'सहि नहि पावा' is the auxiliary 'could (not bear)'; — **fixed**

## Jai Ho Gangaram Baba (`baba-gangaram-aarti`)
- Witnesses read: Randhir book page images i-170, i-171 (base; धरे in st. 5 checked on a zoomed crop); Drik Panchang baba-gangaram-aarti.html (whole).
- Verses compared: 8 (tek + 7), word by word: text = book in every word.
- Meanings read: 8 hi / 8 en. Words read: ~135 verse words + ~15 underlined.
- Title/shelf: work.json and index.json (baba-gangaram group) checked.
- A: 1 (Gaṅgārāma in the Jhunjhunu entry). B: none. D: none. E: 3 (Bābā underline says Sāī Bābā; देव and शोक fall back to Sanskrit entries). F: none.
- Findings:
  - E `aarti.tek`: The English meaning's underlined 'Bābā' (in aarti.tek and aarti.pad6) opens a shared entry ending 'here Sāī Bābā of Shirdi'; — **covered**
  - A `aarti.pad3`: The English underline entry for Jhunjhunu spells the saint 'Bābā Gaṅgārāma', while the work and its own entry spell him 'Gaṅgārām' (one name spelt one way). — **fixed**
  - E `aarti.pad7`: The verse word देव ('god', in 'थे देव बड़े बलवान') has no Hindi entry and falls back to the Sanskrit one ('हे देव! / देव, प्रकाशमान देव (‘इति’ से पहले देवः)', g 'सम्बोधन एकवचन'), whose note and grammar are for Sanskrit v — **fixed**
  - E `aarti.pad3`: शोक has no Hindi entry and opens the Sanskrit one, whose grammar 'प्रथमा एकवचन (शोकः, संधिमें विसर्गका लोप)' describes a Sanskrit sandhi that is not in this Hindi line. — **fixed**

## Shri Baba Gangaram Chalisa (`baba-gangaram-chalisa`)
- Witnesses read: book page images i-166, i-167, i-168, i-169, i-170 (pp. 167–171; zoomed crop of cau31–35, निशातन confirmed as printed); Drik Panchang printout shri-baba-gangaram-chalisa.html (drik.py).
- Verses compared: 43 (3 dohās, 40 chaupāīs), every line against the book and Drik; text equals the book except the recorded quotation marks; Drik's spelling differences are recorded.
- Meanings read: 43 hi / 43 en, with every underlined word's entry.
- Words read: all verse words of 43 verses (about 360 tokens).
- Title / shelf: work.json title hi/en; library/index.json (chalisa › baba-gangaram) against siblings.
- A (spelling, names): 3 findings: Gaṅgārām / Gaṅgārāma in two glossary entries (the work's own, and shared hi गंगाराम); 'Dasharā' not IAST.
- B (text vs witnesses): nothing unrecorded.
- D (meanings): 1 low-confidence finding (cau7 टारो read as a statement though glossed and used as an imperative).
- E (word meanings): 7 findings: en bābā ('here Sāī Bābā'), en māyā (Mānas note), hi ब्रह्म ('here Paraśurāma'), hi महावीर (poet sense missing in the hi glossary), hi पंचदेव (temple sense), awa जनहित ('(her)'), awa हीन.
- F (title, shelf): consistent; nothing to report.
- Findings:
  - E `chalisa.do2`: The English meanings underline 'Bābā' (do2, cau4, cau6, cau17, cau20, cau21, cau22, cau26, cau31), and the shared en entry says 'here Sāī Bābā of Shirdi': — **covered**
  - E `chalisa.cau15`: The English meaning underlines 'māyā', whose shared en entry ends 'In the Mānas, Sītā is the Lord's māyā': — **covered**
  - E `chalisa.cau32`: The Hindi meaning underlines ब्रह्म (as 'पूर्ण ब्रह्म'); — **fixed**
  - E `chalisa.cau40`: The Hindi meaning underlines महावीरने, and the entry it opens (shared hi) gives 'great hero / Hanumān / Mahāvīra the Tīrthaṅkara', none of which is meant: — **fixed**
  - E `chalisa.cau38`: In cau38 पंचदेव is the Pañcadeva temple ('पंचदेव मन्दिर विख्याता'), but the Hindi meaning's underlined पंचदेव opens the shared hi entry with only 'the five deities' (the en side has a temple entry, the awa verse word has — **fixed**
  - A `chalisa.cau35`: The work's hi glossary entry for the underlined दशहराको spells the festival 'Gaṅgā Dasharā' in English: — **fixed**
  - A `chalisa.cau7`: The work's hi glossary entry झुंझनूं (underlined in cau7, cau31, cau35) spells the name 'Bābā Gaṅgārām’s' (no final a, curly apostrophe) where every meaning and the en entries of this work spell Gaṅgārāma. — **fixed**
  - A `chalisa.do2`: The shared hi entry गंगाराम (underlined in the Hindi meanings of do2, cau1, cau16, cau20, cau25, cau29, cau32, cau39, cau40, do3) gives the English 'Bābā Gaṅgārām', unlike this work's English meanings and en entry (Gaṅgā — **fixed**
  - E `chalisa.cau10`: जनहित (cau10, cau14) is about Bābā Gaṅgārāma (and in cau14 the gods), but the shared entry's English says 'for the good of (her) people', a feminine left from a goddess's work. — **fixed**
  - E `chalisa.cau8`: हीन in 'दीन हीन' is 'lowly, destitute' (the meanings: — **fixed**
  - D `chalisa.cau7`: टारो is glossed imperative ('टालो, दूर करो', आज्ञार्थक) and the work's other prayers use imperatives (हरौ, करो, करहु), but both meanings make it a statement ('आप … टालते हैं', 'you avert'). — **fixed by hand**

## Jai Jai Shri Badrinath (`badrinath-aarti`)
- Witnesses read: Drik Panchang lord-badarinatha-aarti.html (base, only witness; whole). The book does not have it (per reconciliation).
- Verses compared: 6 (tek + 5): equal to Drik except the recorded मेध→मेघ and the standard.
- Meanings read: 6 hi / 6 en. Words read: ~85 verse words + ~20 underlined.
- Title/shelf: work.json and index.json (vishnu group) checked.
- A: 2 (Badrīnātha for Badarīnātha in meaning and entries). B: none. D: none. E: none new (श्यामा's sense 3 is this work's own; see ambe-aarti finding, which keeps it). F: none.
- Findings:
  - A `aarti.tek`: The name is spelt 'Badrīnātha' in the English meaning and both glossary entries, a mix of the modern short form (Badrī) and the Sanskrit ending; — **fixed**
  - A `glossary`: Same spelling in the dictionary entries: — **fixed**

## Jai Jai Shri Baglamukhi Mata (`bagalamukhi-aarti`)
- Witnesses read: Randhir book page image i-254 (base); Drik Panchang bagalamukhi-mata-aarti.html (whole).
- Verses compared: 12 (tek + 10 stanzas + dohā), word by word: equal to the book in every word.
- Meanings read: 12 hi / 12 en. Words read: ~140 verse words + ~15 underlined.
- Title/shelf: work.json and index.json (bagalamukhi group, sibling chalisa) checked.
- A: none. B: none. D: none. E: none. F: 1 (Bagalamukhi vs Baglamukhi in the English title; same change in index.json title and text.txt @topic).
- Findings:
  - F `title`: The English title spells the goddess 'Bagalamukhi', while the same work's 'by', its shelf group ('Mother Baglamukhi'), its shelf description ('The aarti of Mother Baglamukhi') and the sibling Chalisa ('Shri Baglamukhi Ch — **fixed by hand**

## Shri Baglamukhi Chalisa (`bagalamukhi-chalisa`)
- Witnesses read: book page images i-250, i-251, i-252, i-253 (pp. 251–254); Drik Panchang printout bagalamukhi-mata-chalisa.html (drik.py).
- Verses compared: 43 (3 dohās, 40 chaupāīs), line by line; text equals the book but for the recorded गुग्गुल (cau26); Drik's three variants recorded.
- Meanings read: 43 hi / 43 en, with every underlined word's entry.
- Words read: all verse words of 43 verses (about 390 tokens).
- Title / shelf: work.json title/by; library/index.json chalisa and aarti groups for Bagalāmukhī.
- A (spelling, names): 1 finding (Haripur/Haridwar vs Haripura/Haridvāra in the work's hi glossary).
- B (text vs witnesses): nothing unrecorded.
- D (meanings): hi and en agree and follow the verses; nothing to report.
- E (word meanings): 2 findings (awa नसाई intransitive only; awa धरे past only, and cau13's underlined धरे).
- F (title, shelf): 1 low finding (Baglamukhi vs Bagalamukhi between this shelf and the sibling āratī's title).
- Findings:
  - A `chalisa.do2`: The work's hi glossary entry हरिपुर (underlined in the Hindi meaning) spells the places 'Haripur' and 'Haridwar' in English, while the English meaning and the work's en entries write Haripura and Haridvāra (IAST, as styl — **fixed**
  - E `chalisa.cau34`: नसाई in 'अल्पकाल महँ रिपुहिं नसाई' is transitive, 'destroys (the enemies)', with रिपुहिं as its object, as both meanings read it; — **fixed**
  - E `chalisa.cau38`: धरे in 'धरे ध्यान होवै कल्याना' is 'holding (meditation)', a participle ('ध्यान धरनेसे', 'Meditating'); — **fixed**
  - F `shelf`: The deity is spelt Baglamukhi in this work's English title, the shelf group (Mother Baglamukhi) and both descs, but Bagalamukhi in the sibling āratī's English title (Jai Jai Shri Bagalamukhi Mata) on the same deity's āra — **fixed by hand**

## Bajrang Baan (`bajrang-baan`)
- Witnesses read: book page images i-027 (heading, opening dohā, cau1–2), i-028, i-029 (zoomed: ह्रीं/हुँ line), i-030 (pp. 28–31); Drik Panchang printout shri-bajarang-baan.html (drik.py).
- Verses compared: 37 (2 dohās, 35 chaupāīs), line by line; text equals the book but for the three recorded corrections (गिरि, परौं, हनु); every Drik difference is in the reconciliation's kept list.
- Meanings read: 37 hi / 37 en, with every underlined word's entry.
- Words read: all verse words of 37 verses (about 400 tokens).
- Title / shelf: work.json title/by; library/index.json (chalisa › hanuman) against siblings.
- A (spelling, names): 1 low finding (Añjanā in the word entry vs Añjanī in the meanings).
- B (text vs witnesses): nothing unrecorded.
- D (meanings): 1 low-confidence finding, given for hi and en (cau23 अग्नि बैताल read as 'fire, vetālas').
- E (word meanings): 1 finding, in two files (Laṅkinī entries say a fist where the verse says a kick).
- F (title, shelf): consistent with the Hanumān shelf; nothing to report.
- Findings:
  - E `chalisa.cau4`: The underlined Laṅkinī entries say Hanumān struck her with his fist (hi: — **fixed**
  - E `chalisa.cau4`: Same as above for the English meaning's underlined Laṅkinī: — **fixed**
  - D `chalisa.cau23`: 'अग्नि बैताल' stands in a list of spirits Hanumān is asked to kill (इन्हें मारु, cau24); — **fixed**
  - D `chalisa.cau23`: English of the same: — **fixed**
  - A `chalisa.cau21`: Hanumān's mother is Añjanī in the meanings (अंजनीकुमार, 'son of Añjanī') and in the underlined entries, but the verse word अन्जनि opens an entry naming her 'माता अंजना / Mother Añjanā': — **fixed**

## Om Jai Hanumat Veera (`balaji-aarti`)
- Witnesses read: Randhir book page image i-115 (base; damaged स्·ीव, ल·क confirmed); Drik Panchang shri-balaji-aarti.html (whole). Aarti Mala i-320 not reopened (its variants are only listed, not used).
- Verses compared: 9 (tek + 8), word by word: equal to the book, with the two damaged letters filled from Drik as recorded.
- Meanings read: 9 hi / 9 en. Words read: ~140 verse words + ~20 underlined.
- Title/shelf: work.json and index.json (hanuman group) checked.
- A: none. B: none. D: none. E: 1 (English underline 'Indra' gives the god, not the poet). F: none.
- Findings:
  - E `aarti.pad8`: In the English meaning 'says Indra', Indra is the poet who signs the āratī, but the underlined 'Indra' opens only the shared entry 'Indra, king of the gods and lord of heaven, who wields the thunderbolt', which tells the — **fixed**

## Shri Balaji Chalisa (`balaji-chalisa`)
- Witnesses read: book page images i-111, i-112, i-113 (zoomed: cau23–26, अंजनी), i-114 (pp. 112–115); Drik Panchang printout shri-balaji-chalisa.html (drik.py).
- Verses compared: 43 (3 dohās, 40 chaupāīs), line by line; text equals the book (only the recorded ॥ and comma); Drik's differences (भाग, अरु, उध्दार, dohā split) recorded.
- Meanings read: 43 hi / 43 en, with every underlined word's entry.
- Words read: all verse words of 43 verses (about 370 tokens).
- Title / shelf: work.json title/by; library/index.json (chalisa › hanuman) against siblings.
- A (spelling, names): 2 low findings (Añjanā vs Añjanī; मेंहदीपुर vs मेहंदीपुर within the work).
- B (text vs witnesses): nothing unrecorded.
- D (meanings): hi and en agree and follow the verses (readings in reconciliation.md checked); nothing to report.
- E (word meanings): 2 findings (hi पुरी 'city' underlined for the Purī family; en bābā 'here Sāī Bābā', shared with baba-gangaram-chalisa).
- F (title, shelf): consistent; nothing to report.
- Findings:
  - E `chalisa.cau17`: The Hindi meaning underlines पुरी in 'पुरी परिवार आपकी सेवा करता है' (the Purī family, the line of Mahant Gaṇeśapurī), but the shared hi entry gives only 'नगरी / city', which cannot fit; — **fixed**
  - E `chalisa.cau20`: The English meaning underlines 'Bābā' (cau20, cau26), here Bālājī (Hanumān), and the shared en entry says 'here Sāī Bābā of Shirdi'. — **covered**
  - A `chalisa.cau24`: Hanumān's mother is 'माता अंजनी' / 'Mother Añjanī' in the meanings and the underlined entries, but the verse word अंजनी opens 'माता अंजना / Añjanā (Hanumān's mother)': — **fixed**
  - A `chalisa.do2`: The Hindi spelling of Mehandipur differs within the work: — **fixed**

## Shri Banke Bihari Teri Aarti Gaun (`banke-bihari-aarti`)
- Witnesses read: Drik Panchang shri-banke-bihari-aarti.html (base, only witness; whole). Book OCR searched for the āratī: not present (confirms reconciliation).
- Verses compared: 6 (tek + 5), word by word: equal to Drik except the recorded कुन्ज→कुञ्ज.
- Meanings read: 6 hi / 6 en. Words read: ~95 verse words + ~30 underlined.
- Title/shelf: work.json and index.json (krishna group) checked.
- A: none. B: none. D: none. E: 2 (low: Hari underline with Mānas note; मोहन entry duplicate sense). F: none.
- Findings:
  - E `aarti.pad3`: The English meaning's underlined "Hari's" opens the shared entry 'Hari, a name of Viṣṇu; — **covered**
  - E `aarti.pad4`: The shared entry मोहन lists the mohanbhog sense twice (two near-identical senses), so the word sheet shows a duplicate. — **fixed**

## Jai Bhairav Deva (`batuk-bhairav-aarti`)
- Witnesses read: Randhir book page image i-072 (base); Drik Panchang batuka-bhairava-aarti.html (whole). Aarti Mala i-321 not reopened (its variants listed only).
- Verses compared: 7 (tek + 6), word by word: equal to the book in every word.
- Meanings read: 7 hi / 7 en. Words read: ~100 verse words + ~15 underlined.
- Title/shelf: work.json and index.json (bhairava group) checked.
- A: none. B: none. D: 1 (low: pad4 meaning supplies 'offerings'). E: 2 (Deva underline Upaniṣad note; भयहारी feminine only). F: none.
- Findings:
  - D `aarti.pad4`: The meaning adds a noun the verse does not have: — **not taken: records a doubt instead of deciding; the meaning stays**
  - E `aarti.tek`: The English meaning's underlined 'Deva' (in 'Bhairava Deva') opens 'a god, a shining one; — **covered**
  - E `aarti.pad2`: भयहारी (said of Bhairava, masculine) opens 'भय हरनेवाली' (feminine only); — **fixed**

## Shri Batuk Bhairav Chalisa (`batuk-bhairav-chalisa`)
- Witnesses read: book page images i-068, i-069, i-070, i-071 (pp. 69–72), each line compared; Drik Panchang printout (drik.py) line by line; OCR used only as a finding aid.
- Verses compared: 44 (4 dohās, 40 chaupāīs), all against the images and Drik; every difference is in reconciliation.md.
- Meanings read: 44 hi / 44 en (no per-line pieces in this work).
- Words read: 414 verse-word entries, 117 underlined meaning-word entries.
- Title / shelf checked: work.json title, `by`, sections; library/index.json entry (Bhairav shelf; desc en repeats the title, like most sibling chālīsās).
- A (spelling, names): 1 low (hard entries spell 'Baṭuk Bhairav' against the work's 'Baṭuka Bhairava').
- B (text against witnesses): none. Text matches the book; भजूं, the one correction, is recorded.
- D (meanings): 1 low (वारे in cau32 has no word in either meaning; finding given as two edits, hi and en).
- E (word meanings): 5. Shared hard entries carry other works' notes: उमा (Mānas), Bābā (Sāī Bābā), Digambara (Sāī Bābā), बैजनाथ (only 'a place'). The तेश entry guesses ईश. Cakranātha's sense differs between two entries (low).
- F (title, shelf): none.
- Findings:
  - E `chalisa.cau11`: Underlined उमाको in the Hindi meaning opens the shared hard entry for उमा, which speaks of the Mānas ("मानसमें शिवजी उन्हें रामकथा सुनाते हैं"); — **covered**
  - E `chalisa.cau26`: Underlined 'Bābā' in the English meaning (Bhairoṃ Bābā) opens the shared entry that says 'here Sāī Bābā of Shirdi': — **covered**
  - E `chalisa.cau10`: Underlined 'Digambara' in the English meaning opens the shared entry 'a name of Dattātreya, here of Sāī Bābā as Datta': — **covered**
  - E `chalisa.cau8`: Underlined बैजनाथ in the Hindi meaning (हे प्रभु बैजनाथ!) opens the shared hard entry 'एक तीर्थस्थान / a place of pilgrimage'; — **fixed**
  - E `chalisa.cau6`: The shared awa entry for तेश glosses it as ईश 'lord' with root ईश, a guess: — **fixed**
  - D `chalisa.cau32`: The meanings leave वारे untranslated: — **fixed**
  - D `chalisa.cau32`: English half of the same fix (वारे). — **fixed**
  - A `glossary`: Hard entries spell the name 'Baṭuk Bhairav' (no final a) while the work's meanings and other entries use 'Baṭuka Bhairava'. — **fixed**
  - E `chalisa.cau12`: The underlined English hard entry gives Cakranātha as 'lord of the circle' while the verse word's entry gives 'lord of the discus': — **fixed**

## Jai Jai Bhagirath Nandini (`bhagirath-nandini-aarti`)
- Witnesses read: Drik Panchang ganga-bhagiratha-nandini-aarti.html (base, only witness; whole). No book copy (none found in scriptures-data; no Vinaya Patrikā source there either).
- Verses compared: 6 (tek + 5), quarter by quarter: equal to Drik except the recorded line break in st. 3, न्→ं, commas.
- Meanings read: 6 hi / 6 en. Words read: ~60 verse words (many compounds) + ~25 underlined.
- Title/shelf: work.json and index.json (ganga group) checked.
- A: none. B: none. D: none. E: none. F: 1 (low: Bhagirathanandini spelling in the plain title).
- Findings:
  - F `title`: The English title 'Jai Jai Bhagirathanandini' keeps the inherent a after Bhagirath (a Sanskrit-style transliteration), while plain Indian English drops it (Bhagirath, as in the work's own id bhagirath-nandini-aarti and a — **fixed by hand**

## Suno Ji Bhairav Ladile (`bhairav-aarti`)
- Witnesses read: Randhir book page images i-066, i-067 (base); Drik Panchang shri-bhairava-aarti.html (whole).
- Verses compared: 6 (tek + 5; 28 half-lines), word by word: equal to the book in every word.
- Meanings read: 6 hi / 6 en. Words read: ~150 verse words + ~15 underlined.
- Title/shelf: work.json and index.json (bhairava group) checked.
- A: 3 (Sarkāra/Sarkār; Mehandīpur in an entry). B: none. D: none. E: none. F: none.
- Findings:
  - A `aarti.pad4`: सरकार is spelt two ways in one place: — **fixed**
  - A `glossary`: The en entry 'sarkāra' spells the place 'Mehandīpur' (long ī), while the work, the Bālājī āratī and every other entry write Mehandipur. — **fixed**
  - A `glossary`: The hi entry प्रेतराज gives the English 'Pretarāja Sarkāra', against 'Pretarāja Sarkār' in the en entries (same name, two spellings). — **fixed**

## Shri Bhairav Chalisa (`bhairav-chalisa`)
- Witnesses read: book page images i-063, i-064, i-065, i-066 (pp. 64–67), each line compared; Drik Panchang printout line by line.
- Verses compared: 39 (2 dohās, 37 chaupāīs); every difference is in reconciliation.md (अहहु correction; the kept list).
- Meanings read: 39 hi / 39 en.
- Words read: 351 verse-word entries, 80 underlined meaning-word entries.
- Title / shelf checked: work.json; library/index.json (Bhairav shelf).
- A: none.
- B: none.
- D: none. Meanings match their verses; the readings settled in cau14, cau27 and cau28 are followed.
- E: 8. Shared hard entries are wrong for this work: श्याम ('here Khāṭū Śyāmajī'), Girijā (Mānas), Digambara (Sāī Bābā), girdle (verb only, where the meaning uses the noun), जगदीश (Viṣṇu). Shared awa entries: आराती (only 'of Tripura'), चतुर्भुज ('Vishnu form'). Cakranātha (low).
- F: none.
- Findings:
  - E `chalisa.cau1`: Underlined श्याम (cau1 'आपका वर्ण श्याम है', cau17 'श्याम वर्णकी') opens the shared hard entry whose second sense says '(यहाँ खाटूश्यामजी) / (here Khāṭū Śyāmajī)': — **covered**
  - E `chalisa.cau3`: Underlined 'Girijā' in the English meaning opens the shared entry '... — **covered**
  - E `chalisa.cau21`: Underlined 'Digambara' in the English meaning opens the shared entry 'a name of Dattātreya, here of Sāī Bābā as Datta': — **covered**
  - E `chalisa.cau8`: Underlined 'girdle' in the English meaning ('the girdle and its little bells') is a noun, the waist ornament करधनी, but the shared entry gives only the verb 'to encircle' (चारों ओरसे घेरना). — **covered**
  - E `chalisa.cau37`: Underlined जगदीश in the Hindi meaning ('हे जगदीश!', said to Bhairava) opens the shared hard entry 'जगत्‌के स्वामी (भगवान विष्णु) / Lord of the universe (Viṣṇu)': — **covered**
  - E `chalisa.cau14`: The shared awa entry for आराती gives only 'enemy (of Tripura = Shiva)' in English; — **fixed**
  - E `chalisa.cau10`: The shared awa entry for चतुर्भुज says 'चार भुजाओं वाला (विष्णु रूप) / four-armed (Vishnu form)'; — **covered**
  - E `chalisa.cau21`: The underlined English hard entry gives Cakranātha as 'lord of the circle' while the verse word's entry gives 'lord of the discus'. — **fixed**

## Pitu Matu Sahayak Swami Sakha (`brahma-aarti`)
- Witnesses read: Randhir book page image i-052 (base); Drik Panchang shri-brahma-aarti.html (whole). Atul's Song A Day (web, named in reconciliation for निर्गुण→दुर्गुण) not reopened.
- Verses compared: 5 stanzas (20 half-lines), word by word: equal to the book except the recorded दुर्गुण and line division.
- Meanings read: 5 hi / 5 en. Words read: ~95 verse words + ~10 underlined.
- Title/shelf: work.json and index.json (brahma group) checked.
- A: none. B: none. D: none. E: 4 (प्रताप verse word lacks the poet sense; मातु vocative only; छिन grammar; Mahārāja underline Sāī note). Hari underline (Mānas note) as in ambe-aarti. F: none.
- Findings:
  - E `aarti.pad5`: The verse word प्रताप in 'तुम सों प्रभु पाय प्रताप हरि' is the poet's name (our meanings: — **fixed**
  - E `aarti.pad1`: मातु in 'पितु मातु सहायक स्वामी सखा' is 'mother' in a list (our meanings: — **covered**
  - E `aarti.pad3`: छिन in 'छिन ही छिन' ('moment by moment') is a noun, but the shared entry's grammar is only 'क्रिया' and its first sense is the verb 'be snatched away'; — **fixed**
  - E `aarti.pad4`: The English underline 'Mahārāja' opens 'great king; — **covered**

## Shri Brahma Chalisa (`brahma-chalisa`)
- Witnesses read: book page images i-047, i-048, i-049, i-050, i-051 (pp. 48–52), each line compared; i-049's last line was enlarged to check one word. Drik Panchang printout line by line; OCR diffed word by word as a finding aid.
- Verses compared: 55 (2 dohās, 53 chaupāīs).
- Meanings read: 55 hi / 55 en.
- Words read: 518 verse-word entries, 67 underlined meaning-word entries.
- Title / shelf checked: work.json; library/index.json (Brahma shelf).
- B: 2 entries for one issue. The book prints भैटहु in cau29 and our text has भैंटहु; reconciliation.md wrongly says the book has भैंटहु. The fix records the correction.
- A: 1 low (Puṣkar / Puṣkara).
- D: none. Meanings match their verses; cau20, cau40 and cau46 follow their settled readings.
- E: 2. The ब्रह्म hard entry says 'here Paraśurāma'; the awa entry for चतुर्भुज says 'Vishnu form', but here the form is Brahmā's.
- F: none.
- Findings:
  - B `chalisa.cau29`: The book prints भैटहु (no anusvāra), not भैंटहु: — **fixed by hand**
  - B `chalisa.cau29`: Same point, the 'kept' list: — **fixed by hand**
  - E `chalisa.cau22`: Underlined ब्रह्म in the Hindi meanings (cau22, cau24, cau39, cau40, cau44) opens the shared hard entry whose second sense ends '(here Paraśurāma)' / 'ब्राह्मणरूपमें परशुरामजी': — **covered**
  - E `chalisa.cau2`: The shared awa entry for चतुर्भुज says '(विष्णु रूप) / (Vishnu form)'; — **covered**
  - A `chalisa.cau52`: The place is Puṣkara in the English meaning and in the verse word's entry, but the underlined Hindi hard entry spells it 'Puṣkar'. — **fixed**

## Jai Ambe Brahmacharini Mata (`brahmacharini-aarti`)
- Witnesses read: Drik Panchang devi-brahmacharini-aarti.html (base, only witness; whole). Book OCR searched: no copy (confirms reconciliation). The two web pages named for रुद्राक्ष not reopened (rudrākṣa is plainly right for रद्रक्षा).
- Verses compared: 5 stanzas (20 lines), word by word: equal to Drik except रद्रक्षा→रुद्राक्ष (recorded).
- Meanings read: 5 hi / 5 en (pad2→pad3 run-on sentence checked). Words read: ~110 verse words + ~15 underlined.
- Title/shelf: work.json and index.json (durga group) checked.
- A: none. B: none. D: none. E: 1 (low: ब्रह्म entry 'here Paraśurāma'). F: none.
- Findings:
  - E `aarti.pad2`: The shared entry ब्रह्म (opened by 'ब्रह्म मन्त्र') says in English 'a brāhmaṇa (here Paraśurāma)'; — **covered**

## Om Jai Brihaspati Deva (`brihaspati-aarti`)
- Witnesses read: Aarti Mala image i-357 (read); Drik Panchang weekdays-guruwar-aarti.html; README and reconciliation.md read.
- Verses compared word by word against the witness(es): 7 (refrain and every stanza).
- Meanings read (hi/en): 7/7; underlined words in meanings checked.
- Verse words read (entries checked): about 73.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 2.
- Findings:
  - E `aarti.pad3`: आकर ("having come", आकर द्वार खड़े) has the shared entry's grammar संज्ञा only, though the sense used here is the conjunctive participle आ करके; — **fixed**
  - E `aarti.tek`: छिन in छिन छिन भोग लगाऊं is the noun "moment" (the entry's second sense), but the entry's only grammar label is क्रिया. — **fixed**

## Jai Maa Chandraghanta Sukh Dham (`chandraghanta-aarti`)
- Witnesses read: Drik Panchang devi-chandraghanta-aarti.html (only witness; book has none); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 5 (refrain and every stanza).
- Meanings read (hi/en): 5/5; underlined words in meanings checked.
- Verse words read (entries checked): about 78.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 1.
- Findings:
  - E `aarti.pad5`: The English meaning's underlined Bhavānī opens the shared entry "Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas": — **fixed**

## Om Jai Chitragupt Hare (`chitragupta-aarti`)
- Witnesses read: Drik Panchang lord-chitragupta-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 11 (refrain and every stanza).
- Meanings read (hi/en): 11/11; underlined words in meanings checked.
- Verse words read (entries checked): about 150.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 1.
- Findings:
  - E `aarti.pad2`: मातु in मातु इरावती दक्षिणा / वाम अङ्ग साजै is "Mother (Irāvatī)", the subject of साजै, not an address; — **covered**

## Jai Dhanvantari Deva (`dhanvantari-aarti`)
- Witnesses read: Drik Panchang lord-dhanvantari-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 7 (refrain and every stanza).
- Meanings read (hi/en): 7/7; underlined words in meanings checked.
- Verse words read (entries checked): about 80.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 0.
- Findings: none.

## Ambe Tu Hai Jagdambe Kali (`durga-aarti`)
- Witnesses read: book image i-206 (base); Aarti Mala image i-339; Drik Panchang durga-mata-aarti.html; README and reconciliation.md read.
- Verses compared word by word against the witness(es): 4 (refrain and every stanza).
- Meanings read (hi/en): 4/4; underlined words in meanings checked.
- Verse words read (entries checked): about 100.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 2.
- Findings:
  - D `aarti.tek`: English "Bhāratī (Sarasvatī) sings your glories alone" can be read as "Bhāratī alone sings"; — **fixed**
  - E `aarti.tek`: दुर्गे (जय दुर्गे, vocative "O Durgā") falls through to the Sanskrit entry whose only grammar is सप्तमी एकवचन and whose first sense is "on a high, hard place"; — **fixed**
- Recording `anuradha-paudwal` (YouTube OQ5K_GILwzQ): plays the whole video. Starts heard in 5-s windows: 4 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): aarti.tek. Starts set from the windows: aarti.pad1, aarti.pad2, aarti.pad3.

## Shri Durga Chalisa (`durga-chalisa`)
- Witnesses read: book page images i-172, i-173, i-174, i-175 (pp. 173–176), each line compared; Drik Panchang printout line by line; Chalisa Mala OCR (i-404 to i-406) for the four recording readings. Each of the four (कालिका, अमरपुरी अरु बासव लोका, यश ×2) is in Drik Panchang word for word, and in Chalisa Mala too. Audio not checked (class C is the lead's).
- Verses compared: 42 (41 chaupāīs, 1 dohā); every difference is recorded.
- Meanings read: 42 hi / 42 en.
- Words read: 406 verse-word entries, 75 underlined meaning-word entries.
- Title / shelf checked: work.json; library/index.json (Durga shelf).
- A: 1 low (Hiṅglāj / Hiṅgalāja).
- B: none.
- D: 1 low. Who Lāṅgura vīra is differs between the word entry (Hanumān) and the meanings and hard entries.
- E: 2. The Tārā hard entry gives only Vāli's wife, but the verse means the Mahāvidyā. The Bhavānī entry has a Mānas note.
- F: none.
- Findings:
  - E `chalisa.cau16`: Underlined 'Tārā' in the English meaning ('Tārā who carries the world across', the Mahāvidyā) opens the shared hard entry 'Tārā, Vāli's wife, mother of Aṅgada': — **covered**
  - E `chalisa.cau14`: Underlined 'Bhavānī' in the English meanings (cau14, cau17, cau33, cau37, cau41) opens the shared entry '... — **covered**
  - A `chalisa.cau14`: The shrine is Hiṅgalāja in the English meaning and its English hard entry, but the underlined Hindi hard entry spells it 'Hiṅglāj'. — **fixed**
  - D `chalisa.cau17`: Who लांगुर वीर is differs within the work: — **fixed**
- Recording `bhaktidhaam` (YouTube lCwPg0LRRjk): plays start 1479.26 s, end 1790.53 s. Starts heard in 5-s windows: 8 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: chalisa.cau17, chalisa.cau33.

## Om Jai Ekadashi (`ekadashi-aarti`)
- Witnesses read: Drik Panchang ekadashi-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 15 (refrain and every stanza).
- Meanings read (hi/en): 15/15; underlined words in meanings checked.
- Verse words read (entries checked): about 210.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 5.
- Findings:
  - F `shelf`: The shelf description says the āratī is of Bhagwan Vishnu, but the āratī is of Ekādaśī Mātā (ॐ जय एकादशी … जय एकादशी माता; — **fixed**
  - E `aarti.pad10`: English meaning underlines Indirā (the Ekādaśī of Āśvina kṛṣṇa) and opens the shared entry 'Indirā, Lakṣmī, the wife of Viṣṇu': — **fixed**
  - E `aarti.pad11`: English meaning underlines Ramā (Ramā Ekādaśī of Kārttika) and opens the shared entry 'Ramā, Lakṣmī, the wife of Viṣṇu; — **fixed**
  - E `aarti.pad8`: English meaning underlines Yoginī (Yoginī Ekādaśī of Āṣāḍha) and opens the shared entry 'a yoginī, a fierce female spirit attending the Goddess, haunting the battlefield': — **fixed**
  - A `glossary`: Three shared English entries this work underlines write 'ekādaśī' in lower case, while every other Ekādaśī entry and our meanings write 'Ekādaśī'. — **fixed by hand**

## Aarti Gajbadan Vinayak Ki (`gajvadan-vinayak-aarti`)
- Witnesses read: Drik Panchang gajavadan-vinayaka-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 4 (refrain and every stanza).
- Meanings read (hi/en): 4/4; underlined words in meanings checked.
- Verse words read (entries checked): about 45.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 0.
- Findings: none.

## Jai Ganesh Jai Ganesh Jai Ganesh Deva (`ganesh-aarti`)
- Witnesses read: book image i-010; Drik Panchang jay-ganesh-aarti.html; README and reconciliation.md read.
- Verses compared word by word against the witness(es): 6 (refrain and every stanza).
- Meanings read (hi/en): 6/6; underlined words in meanings checked.
- Verse words read (entries checked): about 75.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 1.
- Findings:
  - B `aarti.pad4`: Stanza 4 (दीनन की लाज …) stands before the poet's stanza, as the book orders it, but Drik Panchang prints its bracketed variant after the सूर श्याम stanza; — **fixed**
- Recording `anuradha-paudwal` (YouTube oWo6hMlex5M): plays the whole video. Starts heard in 5-s windows: 7 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: aarti.pad2, aarti.pad3, aarti.pad1.

## Shri Ganesh Chalisa (`ganesha-chalisa`)
- Witnesses read: book page images i-006, i-007, i-008, i-009 (pp. 7–10), each line compared; Drik Panchang printout line by line; Chalisa Mala OCR (i-366, i-367) for cau38 (शक्ति भक्ति) and do3 (अपने). Both readings are in Drik and Chalisa Mala as the reconciliation says. Audio not checked (C).
- Verses compared: 41 (3 dohās, 38 chaupāīs); every difference is recorded.
- Meanings read: 41 hi / 41 en.
- Words read: 417 verse-word entries, 90 underlined meaning-word entries.
- Title / shelf checked: work.json; library/index.json. Its desc en is the transliterated opening, unlike most siblings' (which repeat the title), but the Hanumān Chālīsā does the same, so it is not flagged.
- A: none.
- B: none.
- D: 1 low (do3: the English reads the year as 1010; the Hindi leaves सहस्र-दश unread).
- E: 2. Shared hard entries Girijā (en) and उमा (hi) carry Mānas notes.
- F: none.
- Findings:
  - E `chalisa.do1`: Underlined 'Girijā' in the English meanings (do1, cau22, cau26) opens the shared entry '... — **covered**
  - E `chalisa.cau19`: Underlined उमाजी in the Hindi meanings (cau19, cau24) opens the shared hard entry for उमा, which says 'मानसमें शिवजी उन्हें रामकथा सुनाते हैं / to whom Śiva tells the Rāma story in the Mānas': — **covered**
  - D `chalisa.do3`: Hindi and English differ on the year: — **fixed**
- Recording `anuradha-paudwal` (YouTube oHHniScYJzo): plays the whole video. Starts heard in 5-s windows: 21 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): chalisa.cau3, chalisa.cau4, chalisa.cau8, chalisa.cau27, chalisa.cau28, chalisa.cau30. Starts set from the windows: chalisa.cau20.

## Shri Ganga Chalisa (`ganga-chalisa`)
- Witnesses read: book page images i-255, i-256, i-257, i-258 (pp. 256–259); Drik Panchang ganga-mata-chalisa.html (via drik.py).
- Verses compared: 43 (3 dohās, 40 chaupāīs), every line against the book images; the 4 recorded corrections confirmed against book and Drik.
- Meanings read: 43 hi / 43 en.
- Words read: all verse words (~400 tokens) and every underlined word in both meanings.
- Title (work.json) and shelf (library/index.json, group ganga) checked.
- A: 2 findings (Sundardās vs Sundaradāsa in shared entries).
- B: none; text equals the book line for line apart from the 4 recorded corrections.
- D: 1 low-confidence (cau16 'वर्ष पर्यन्त' rendered 'for years').
- E: 4 findings (hi बन्द entry 'bows' for 'closed'; Mandākinī = Citrakūṭa river, hi and en; वागीसा 'Brahmā / giver').
- F: none.
- Findings:
  - E `chalisa.cau35`: In the Hindi meaning 'नरकके किवाड़ बन्द हो गये हैं' the word बन्द (closed) is underlined, and the shared Hindi entry it opens says 'वन्दना करते हैं, प्रणाम करते हैं / bows, offers praise' — a wrong sense for every use of — **covered**
  - E `chalisa.cau19`: Underlined मन्दाकिनी (Hindi meaning, cau19 and cau22) and Mandākinī (English meaning) open the shared entries for the river at Citrakūṭa; — **fixed**
  - E `chalisa.cau19`: English side of the same: — **fixed**
  - E `chalisa.cau40`: The verse word वागीसा opens 'वाणीके स्वामी, ब्रह्मा (यहाँ: — **fixed**
  - A `chalisa.cau39`: The poet's name is spelt Sundaradāsa in our English meaning, README and the English-meaning entry, but 'Sundardās' in the verse-word entry (awa) and in the English line of the Hindi-meaning entry for सुन्दरदास. — **covered**
  - A `chalisa.cau39`: Same spelling issue in the Hindi-meaning entry's English line (Sundardās for Sundaradāsa). — **covered**
  - D `chalisa.cau16`: 'वर्ष पर्यन्त' is literally 'for a year' (up to a year); — **not taken: वर्ष पर्यन्त is read as "for years" (the Purāṇic story); low confidence, kept**

## Om Jai Gangadhar (`gangadhar-aarti`)
- Witnesses read: Drik Panchang lord-gangadhara-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 9 (refrain and every stanza).
- Meanings read (hi/en): 9/9; underlined words in meanings checked.
- Verse words read (entries checked): about 230.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 3.
- Findings:
  - E `aarti.pad2`: The Hindi meaning's गहनोंसे ("with ornaments") is underlined and opens the entry for गहन, 'deep, hard to fathom': — **fixed**
  - E `aarti.tek`: The English meaning's underlined Girijā (tek: — **fixed**
  - E `aarti.tek`: मां in the Sanskrit त्वं मां पालय ("protect me") opens the hi entry with r=माता, g=संज्ञा (first sense माँ, माता); — **fixed**
- Recording `bhajan-aur-aarti` (YouTube Zn78FYVwbZM): plays the whole video. Starts heard in 5-s windows: 8 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: none.

## Ganpati Ki Seva Mangal Meva (`ganpati-seva-aarti`)
- Witnesses read: Drik Panchang ganapati-seva-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 10 (refrain and every stanza).
- Meanings read (hi/en): 10/10; underlined words in meanings checked.
- Verse words read (entries checked): about 165.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 1.
- Findings:
  - E `aarti.pad8`: सर्व in the Hindi line ताके कारज सर्व सरैं ("all his works") has no hi entry and falls to the Sanskrit one, whose grammar 'प्रथमा, एकवचन (सर्वः; — **fixed**

## Aarti Shri Gaiya Maiya Ki (`gau-mata-aarti`)
- Witnesses read: Aarti Mala image i-342 (base); Drik Panchang gau-mata-aarti.html; README and reconciliation.md read.
- Verses compared word by word against the witness(es): 5 (refrain and every stanza).
- Meanings read (hi/en): 5/5; underlined words in meanings checked.
- Verse words read (entries checked): about 95.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 1.
- Findings:
  - E `aarti.pad2`: शोक in the Hindi list रोग शोक संकट परित्राता has no hi entry and falls to the Sanskrit one, whose grammar 'प्रथमा एकवचन (शोकः, संधिमें विसर्गका लोप)' is wrong for a Hindi noun in a list. — **fixed**

## Jayati Jai Gayatri Mata (`gayatri-aarti`)
- Witnesses read: book image i-200 (base); Drik Panchang gayatri-mata-aarti.html; README and reconciliation.md read.
- Verses compared word by word against the witness(es): 11 (refrain and every stanza).
- Meanings read (hi/en): 11/11; underlined words in meanings checked.
- Verse words read (entries checked): about 190.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 1.
- Findings:
  - A `glossary`: Shared Sanskrit entries this work's verse words open give names without IAST (style.md §5): — **fixed by hand**

## Shri Gayatri Chalisa (`gayatri-chalisa`)
- Witnesses read: book page images i-196, i-197, i-198, i-199 (pp. 197–200); reconciliation's Drik Panchang differences taken as recorded.
- Verses compared: 43 (3 dohās, 40 chaupāīs), every line against the book images; the one recorded correction (cau20 ह्वै जाई) confirmed on i-198.
- Meanings read: 43 hi / 43 en.
- Words read: all verse words (~380 tokens, ~300 distinct entries) and every underlined word in both meanings.
- Title (work.json) and shelf (library/index.json, group gayatri) checked.
- A: none.
- B: none; text equals the book apart from the recorded correction.
- D: none.
- E: 3 (shared en 'bhavānī' Mānas clause; sa अविद्या '(the pleasant)'; en 'māyā' Mānas note, low).
- F: none.
- Findings:
  - E `chalisa.cau14`: Underlined 'Bhavānī' in the English meaning (cau14, cau33) opens the shared entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas' (Hindi line likewise). — **covered**
  - E `chalisa.cau13`: The verse word अविद्या (आलस पाप अविद्या नासै) falls back to the Sanskrit shared entry 'अविद्या (प्रेय, अज्ञान) / ignorance (the pleasant)'. — **fixed**
  - E `chalisa.cau7`: Underlined 'māyā' (English meaning) opens a shared entry ending 'In the Mānas, Sītā is the Lord's māyā' — a Mānas note in a Gāyatrī chālīsā where māyā is 'the wondrous māyā of the Formless'. — **covered**

## Jai Jai Giridhari Prabhu (`giridhari-aarti`)
- Witnesses read: Drik Panchang lord-giridhari-aarti.html (only witness); README and reconciliation.md read.
- Verses compared word by word against the witness(es): 10 (refrain and every stanza).
- Meanings read (hi/en): 10/10; underlined words in meanings checked.
- Verse words read (entries checked): about 100.
- Title (work.json hi/en) and shelf entry (library/index.json title, desc, deity group) checked.
- Findings: 3.
- Findings:
  - E `aarti.pad9`: The English meaning's underlined Nārāyaṇa (the poet naming himself: — **fixed**
  - E `glossary`: The shared English entry for 'lapwing' is stored under the truncated key "lapw" (found only because the matcher strips -ing from lapwing); — **fixed**
  - E `aarti.pad6`: The shared entry मोहन lists the mohanbhog sense twice (two near-identical senses), which the word sheet shows as a duplicate. — **fixed**

## Om Jai Jai Jai Giriraj (`giriraj-aarti`)
- Witnesses read: book page images i-138, i-139 (pp. 139–140); Drik Panchang shri-giriraj-aarti.html (drik.py).
- Verses compared: 8 (refrain + 7 stanzas), word by word against the book and Drik: identical apart from recorded standard changes.
- Meanings read: 8 hi / 8 en (and underlined entries).
- Words read: all verse words of 8 verses (~100 tokens) with their entries.
- Title / shelf: work.json and library/index.json checked.
- A (spelling/names): no error found.
- B (text): matches book and Drik; nothing unrecorded.
- D (meanings): 1 low (stanza 2 line 1 split into two clauses, plural stones).
- E (words): 2 (shared श्याम entry says "here Khāṭū Śyāmajī"; अप्सरा is a pool's name here, entry only "celestial dancer").
- F (title/shelf): no error (desc "The aarti of Bhagwan Shri Krishna" matches the Krishna shelf siblings).
- Findings:
  - E `aarti.pad2`: The shared entry of श्याम says 'here Khāṭū Śyāmajī' (यहाँ खाटूश्यामजी). — **covered**
  - E `aarti.pad4`: अप्सरा here is the name of a pool, Apsarā Kuṇḍa at Govardhana (our meanings: — **fixed by hand**
  - D `aarti.pad2`: The meaning splits the first line into two statements (your form is beautiful; — **fixed by hand**

## Shri Giriraj Chalisa (`giriraj-chalisa`)
- Witnesses read: book page images i-134, i-135, i-136, i-137, i-138 (pp. 135–139); Drik Panchang shri-giriraj-chalisa.html (via drik.py), line by line.
- Verses compared: 44 (4 dohās, 40 chaupāīs) against book and Drik; the 4 recorded corrections confirmed (पखवारे i-136, पढ़ावें i-137, quotes i-137, चालिसा i-138); no unrecorded difference (book गौलोक in cau8 = Drik, kept).
- Meanings read: 44 hi / 44 en.
- Words read: all verse words (~420 tokens) and every underlined word in both meanings.
- Title (work.json) and shelf (library/index.json, group krishna) checked.
- A: none.
- B: none.
- D: none.
- E: 3 (hi underlined श्याम = Khāṭū Śyāma, work-own fix and shared note; en underlined Bihārī = Kṛṣṇa for the poet's name).
- F: none.
- Findings:
  - E `chalisa.cau37`: In the Hindi meaning 'कवि श्याम कहते हैं' the underlined श्याम opens the shared entry 'साँवला … / श्याम, श्रीकृष्ण (यहाँ खाटूश्यामजी)' — here श्याम is the poet (Śyāma Bihārī), and the shared entry's 'यहाँ खाटूश्यामजी' is — **fixed**
  - E `chalisa.cau37`: The shared Hindi-meaning entry श्याम carries a work-specific note '(यहाँ खाटूश्यामजी)' / '(here Khāṭū Śyāmajī)', which is wrong in every work but the Khāṭū Śyāma one; — **covered**
  - E `chalisa.do4`: In the English meaning 'Śyāma Bihārī is in your refuge' the underlined 'Bihārī' opens the shared entry 'Bihārī, he who roams at play, Kṛṣṇa (Bāṅke Bihārī, Kuñja Bihārī)'; — **fixed**

## Jai Bhagavad Gite (`gita-aarti`)
- Witnesses read: Drik Panchang bhagavad-gita-aarti.html (base, only witness; drik.py). Book OCR searched (गीते, सुपुनीते, कामासक्ति): the book has no copy, as the reconciliation says.
- Verses compared: 7 (refrain + 6 stanzas), word by word against Drik: identical apart from recorded standard changes.
- Meanings read: 7 hi / 7 en, with underlined entries.
- Words read: all verse words of 7 verses (~80 tokens).
- Title / shelf: work.json and library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found.
- E: 2 (shared en 'hari' entry speaks of the Mānas; shared ब्रह्म entry says "here Paraśurāma").
- F: no error found.
- Findings:
  - E `aarti.tek`: The underlined English word Hari (in the refrain and stanzas 4, 5, 6) opens the shared entry 'Hari, a name of Viṣṇu; — **covered**
  - E `aarti.pad1`: The underlined ब्रह्मकी (hi meaning) opens the shared ब्रह्म entry whose English second sense says 'a brāhmaṇa (here Paraśurāma)'. — **covered**

## Shri Gita Chalisa (`gita-chalisa`)
- Witnesses read: Drik Panchang gita-chalisa.html (the base; via drik.py), line by line. The book has no copy (none to read).
- Verses compared: 40 chaupāīs against Drik; the 2 recorded corrections (श्रद्घा → श्रद्धा, सामान → समान) confirmed; no other difference.
- Meanings read: 40 hi / 40 en.
- Words read: all verse words (~360 tokens) and every underlined word in both meanings.
- Title (work.json) and shelf (library/index.json, group gita) checked.
- A: none.
- B: none.
- D: none.
- E: 5 (shared hi ब्रह्म 'here Paraśurāma'; राखे and बिसारे past-only for present verbs; तुमसे, उनसे senses, low).
- F: none.
- Findings:
  - E `chalisa.cau19`: Underlined ब्रह्म in the Hindi meanings (cau19 'पूर्ण ब्रह्म', cau31 'सगुण ब्रह्मका') opens a shared entry whose English second sense reads 'a brāhmaṇa (here Paraśurāma)' — a 'here' from one āratī, false in this and ever — **fixed**
  - E `chalisa.cau24`: राखे in 'मन इन्द्रिय अपने वश राखे' is present ('keeps', like चाखे in the same line, glossed 'tastes'); — **fixed**
  - E `chalisa.cau17`: बिसारे in 'लज्जा भय रु बिसारे मान' is present ('forgets', in a run of present verbs: — **fixed**
  - E `chalisa.cau6`: तुमसे in 'तुमसे दूजा मन नहीं भावे' means 'than you / other than you'; — **fixed**
  - E `chalisa.cau36`: उनसे in 'उनसे करता मैं अति प्यार' is 'them' (the object of love, Hindi से with प्यार करना); — **fixed**

## Shri Gopal Chalisa (`gopal-chalisa`)
- Witnesses read: book page images i-042, i-043, i-044, i-045, i-046 (pp. 43–47); Drik Panchang differences as recorded in reconciliation.md (only its slips रुप, अम्बरीय).
- Verses compared: 44 (2 dohās, 41 chaupāīs, 1 chhanda) against the book images; the one recorded change (quotes round जयरामदेव, i-045) confirmed; no unrecorded difference.
- Meanings read: 44 hi / 44 en.
- Words read: all verse words (~440 tokens) and every underlined word in both meanings.
- Title (work.json) and shelf (library/index.json, group krishna) checked.
- A: 1 low (non-IAST names in shared verse-word entries: Ajamila, Ambarisha, Kaitabha, Narada).
- B: none.
- D: none.
- E: 1 (cau37 Hindi 'छूट जाये' underlined as जाया 'born of / wife').
- F: none.
- Findings:
  - E `chalisa.cau37`: In the Hindi meaning '…संसारकी आशा छूट जाये' the verb जाये is underlined and opens the shared entry जाया 'जन्मा हुआ, पुत्र … / पत्नी' — 'born of, son / wife'. — **not taken: the underline is fixed in the app instead (जाये has an entry of its own)**
  - A `chalisa.cau34`: Verse-word entries give names without IAST, unlike our English meaning and the other entries of this work: — **fixed**

## Jai Gorakh Deva (`gorakhnath-aarti`)
- Witnesses read: book page images i-098, i-099 (pp. 99–100); Drik Panchang shri-gorakha-aarti.html (drik.py).
- Verses compared: 9 (refrain + 8 stanzas), word by word against book and Drik: identical apart from recorded standard changes.
- Meanings read: 9 hi / 9 en, with underlined entries.
- Words read: all verse words of 9 verses (~120 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found.
- E: 3 (न्यारे entry lacks 'apart'; विनवत entry feminine only; en 'māyā' entry speaks of the Mānas and Sītā).
- F: no error found.
- Findings:
  - E `aarti.pad5`: न्यारे (verse word, and underlined in the Hindi meaning 'सबसे न्यारे हैं') opens only 'निराले, अनोखे / rare, special'. — **fixed**
  - E `aarti.pad8`: विनवत (the poet 'बाल त्रिलोकी', a male child, prays) opens a shared entry whose Hindi is feminine only: — **fixed**
  - E `aarti.pad4`: The underlined English word Māyā opens the shared entry ending 'In the Mānas, Sītā is the Lord's māyā'. — **covered**

## Shri Gorakh Chalisa (`gorakhnath-chalisa`)
- Witnesses read: book page images i-094, i-095, i-096, i-097, i-098 (pp. 95–99, whole text); Drik Panchang `shri-gorakha-chalisa.html` (whole text, via drik.py). InstaAstro not opened (only cited for cau17/do3, both settled on the book).
- Verses compared: 44 of 44 (4 dohās, 40 chaupāīs), word by word against the book and Drik.
- Meanings read: 44 hi, 44 en.
- Words read: every verse word (about 470 tokens) and every underlined meaning word (review.py --words).
- Title / shelf: work.json title, by; library/index.json chalisa › gorakhnath entry (title, desc, group) checked against siblings.
- A: Nāth / Nātha spelt both ways in shared en entries (6); Gorakhanātha vs Gorakhnāth in verse-word entries (3); Gopīcanda vs Gopīcand; तारा "Tara (Bali's wife)"; Shiva, Kamadeva (2), Maya without IAST. 15 findings.
- B: text agrees with the book line for line; every Drik difference is recorded in reconciliation.md. No findings.
- D: meanings say what the verses say; hi and en agree. No findings.
- E: misleading underlined entries (girijā Mānas note, māyā Mānas note, ब्रह्म "here Paraśurāma", नाद, विभूति, रसोंके→रसा); प्रकाशी feminine tag; सिद्धि lacks the yogic sense. 8 findings.
- F: title and shelf entry consistent with the text and siblings. No findings.
- Findings:
  - E `chalisa.do1`: The underlined 'Girijā' in the English meaning opens a shared entry that says she is the one 'to whom Śiva tells the Mānas': — **covered**
  - E `chalisa.cau27`: The underlined 'māyā' in the English meaning opens a shared entry ending 'In the Mānas, Sītā is the Lord's māyā', which has nothing to do with the yogīs perceiving Gorakhnāth's māyā and misleads here. — **covered**
  - E `chalisa.cau12`: The underlined ब्रह्म / ब्रह्मके in the Hindi meanings (cau12, cau13) opens a shared entry whose English second sense says 'a brāhmaṇa (here Paraśurāma)': — **covered**
  - E `chalisa.cau9`: Hindi meaning 'गलेमें नाद शोभा पाता है' uses नाद for the Nātha yogī's horn-whistle (as the English 'the nāda, the yogī's horn' and the verse word's own awa entry say), but the underlined नाद opens the shared entry 'ध्वनि — **covered**
  - E `chalisa.cau23`: The Hindi meaning's 'रसोंके' is underlined and opens the entry for रसा, 'शोरबा, तरी (जो भातपर डाली जाती है) / gravy, sauce (poured over rice)': — **fixed**
  - E `chalisa.do3`: Hindi meaning 'अंगोंपर अपार विभूति है' uses विभूति for the sacred ash (English: — **covered**
  - A `chalisa.cau29`: Shared word entry तारा (cau29, cau31) gives 'Tara (Bali's wife)': — **covered**
  - A `glossary`: Shared English hard-word entry 'alakh' spells the order 'Nāth', while this work's meaning (do4 'the Nātha salutation'), its own glossary ('the Nāthas'), and the shared entries ādeś, गोरख, गोरखनाथ, गोरक्ष, नाद, गोपीचन्द,  — **fixed**
  - A `glossary`: Shared English hard-word entry 'nirañjan' spells the order 'Nāth', while this work's meaning (do4 'the Nātha salutation'), its own glossary ('the Nāthas'), and the shared entries ādeś, गोरख, गोरखनाथ, गोरक्ष, नाद, गोपीचन् — **fixed**
  - A `glossary`: Shared English hard-word entry 'gorakh' spells the order 'Nāth', while this work's meaning (do4 'the Nātha salutation'), its own glossary ('the Nāthas'), and the shared entries ādeś, गोरख, गोरखनाथ, गोरक्ष, नाद, गोपीचन्द, — **fixed**
  - A `glossary`: Shared English hard-word entry 'gorakha' spells the order 'Nāth', while this work's meaning (do4 'the Nātha salutation'), its own glossary ('the Nāthas'), and the shared entries ādeś, गोरख, गोरखनाथ, गोरक्ष, नाद, गोपीचन्द — **fixed**
  - A `glossary`: Shared English hard-word entry 'gorakhnāth' spells the order 'Nāth', while this work's meaning (do4 'the Nātha salutation'), its own glossary ('the Nāthas'), and the shared entries ādeś, गोरख, गोरखनाथ, गोरक्ष, नाद, गोपीच — **fixed**
  - A `glossary`: Shared English hard-word entry 'gorakṣa' spells the order 'Nāth', while this work's meaning (do4 'the Nātha salutation'), its own glossary ('the Nāthas'), and the shared entries ādeś, गोरख, गोरखनाथ, गोरक्ष, नाद, गोपीचन्द — **fixed**
  - A `glossary`: Verse word गोरख (awa shared) names him 'Gorakhanātha', while every meaning and hard-word entry of the work (and the shelf's 'Gorakhnath') say 'Gorakhnāth': — **fixed**
  - A `glossary`: Verse word गोरखनाथ (awa shared) names him 'Gorakhanātha', while every meaning and hard-word entry of the work (and the shelf's 'Gorakhnath') say 'Gorakhnāth': — **fixed**
  - A `glossary`: Verse word गोरक्ष (awa shared) names him 'Gorakhanātha', while every meaning and hard-word entry of the work (and the shelf's 'Gorakhnath') say 'Gorakhnāth': — **fixed**
  - A `chalisa.cau31`: Verse word गोपीचन्द gives 'King Gopīcanda', while the meaning (hi/en) and both hard-word entries say 'Gopīcand'. — **fixed**
  - A `chalisa.do4`: Shared word entry हर (cau17, do4) has 'Shiva' without IAST beside 'O Hara (Śiva)!' in the same entry. — **covered**
  - A `chalisa.cau15`: Shared word entry मार has 'Kamadeva' without IAST (Kāmadeva). — **fixed**
  - A `chalisa.cau3`: Shared word entry कामा has 'Kamadeva' without IAST (Kāmadeva). — **fixed**
  - A `chalisa.cau27`: Shared word entry माया gives 'illusion, Maya' (no IAST; — **fixed**
  - E `chalisa.cau1`: Word प्रकाशी (cau1 'गुरु देव प्रकाशी', cau12 'गोरख नाथ सकल प्रकाशी') is used of Gorakhnāth, but its grammar says 'विशेषण, स्त्रीलिंग'; — **fixed**
  - E `chalisa.cau23`: Word सिद्धि (cau19 'सिद्धि बढ़े', cau23 'सिद्धि देवो') is the yogic power, as our meanings say ('siddhi', underlined to 'a supernatural power gained by yoga'), but the verse-word entry gives only 'accomplishment / Siddhi — **covered**

## Shri Govardhan Maharaj (`govardhan-aarti`)
- Witnesses read: Drik Panchang shri-govardhan-aarti.html (base, only witness; drik.py). Book OCR searched (गोवर्धन महाराज, चकलेश्वर): not in the book, as recorded.
- Verses compared: 6 (refrain + 5 stanzas) word by word against Drik: identical apart from recorded standard changes.
- Meanings read: 6 hi / 6 en, with underlined entries.
- Words read: all verse words of 6 verses (~60 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found.
- E: no error found (shared 'mahārāja' en entry's example "as for Sāī Bābā" is an example, not wrong).
- F: no error found.
- Findings: none.

## Shri Hanuman Chalisa (`hanuman-chalisa`)
- Text taken by id from the Sundarakāṇḍa work (`[take sundarkand chalisa.do1 .. chalisa.do3]`); its reconciliation (tools/works/sundarkand/reconciliation.md) read.
- Witnesses read: book page images i-021, i-022, i-023, i-024 (pp. 22–25, whole text; i-025 checked as the next work); Drik Panchang `shree-hanuman-chalisa.html` (whole text).
- Verses compared: 43 of 43 (3 dohās, 40 chaupāīs) against the book and Drik for word-level differences (Mānas spelling choices of the Sundarakāṇḍa table not re-flagged).
- Meanings read: 43 hi, 43 en (whole and per line).
- Words read: every verse word (about 460 tokens) and every underlined meaning word.
- Title / shelf: work.json title, by; library/index.json chalisa › hanuman entry beside Bajrang Baan and Balaji.
- A: 25 verse-word entries spell names without IAST (Hanuman, Rama, Sita, Lakshmana, Lanka, Shiva, Tulsidas …); अंजनि Añjanā vs Añjanī; Cālīsā vs Chālīsā. 27 findings.
- B: word differences from the book (do2 देउ, cau33 भावै, cau37 जय, cau38 शत/छूटहिं) unrecorded; reconciliation's image number off by one. 2 findings.
- D: cau6 hi अंश vs en "born of"; cau16 en adds "great". 2 findings (low).
- E: दीन (cau31) has no "gave" sense; सम्हारो tagged imperative. 2 findings.
- F: shelf desc.en is the opening words, unlike its siblings. 1 finding (low).
- Findings:
  - E `chalisa.cau31`: In 'अस बर दीन जानकी माता' दीन is the verb 'gave' (दीन्ह; — **fixed**
  - E `chalisa.cau23`: 'आपन तेज सम्हारो आपै' is a statement ('you alone can contain your own splendour', as both meanings say), but the word entry gives only the imperative 'सँभालो' with g=आज्ञार्थक, which misleads a learner. — **fixed**
  - A `chalisa.cau1`: Verse word हनुमान (awa shared) spells the name without IAST ("Hanuman"), while the work's meanings and its other entries write "Hanumān": — **fixed**
  - A `chalisa.cau25`: Verse word हनुमत (awa shared) spells the name without IAST ("Hanuman"), while the work's meanings and its other entries write "Hanumān": — **fixed**
  - A `chalisa.do2`: Verse word पवनकुमार (awa shared) spells the name without IAST ("Hanuman"), while the work's meanings and its other entries write "Hanumān, son of the Wind": — **fixed**
  - A `chalisa.cau2`: Verse word पवनसुत (awa shared) spells the name without IAST ("Hanuman, son of the Wind"), while the work's meanings and its other entries write "Hanumān, son of the Wind": — **fixed**
  - A `chalisa.do3`: Verse word पवनतनय (awa shared) spells the name without IAST ("Hanuman (son of Wind)"), while the work's meanings and its other entries write "Hanumān (son of the Wind)": — **fixed**
  - A `chalisa.cau1`: Verse word कपीस (awa shared) spells the name without IAST ("lord of monkeys (Sugriva / Hanuman)"), while the work's meanings and its other entries write "lord of monkeys (Sugrīva / Hanumān)": — **fixed**
  - A `chalisa.cau2`: Verse word राम (awa shared) spells the name without IAST ("Lord Rama /), while the work's meanings and its other entries write "Lord Rāma /: — **fixed**
  - A `chalisa.do1`: Verse word रघुबर (awa shared) spells the name without IAST ("Rama, best of the Raghus"), while the work's meanings and its other entries write "Rāma, best of the Raghus": — **fixed**
  - A `chalisa.cau12`: Verse word रघुपति (awa shared) spells the name without IAST ("Rama, lord of the Raghus"), while the work's meanings and its other entries write "Rāma, lord of the Raghus": — **fixed**
  - A `chalisa.cau10`: Verse word रामचंद्र (awa shared) spells the name without IAST ("Shri Ramachandra"), while the work's meanings and its other entries write "Śrī Rāmacandra": — **fixed**
  - A `chalisa.cau11`: Verse word श्रीरघुबीर (awa shared) spells the name without IAST ("Shri Rama"), while the work's meanings and its other entries write "Śrī Rāma, hero of the Raghus": — **fixed**
  - A `chalisa.cau8`: Verse word लखन (awa shared) spells the name without IAST ("Lakshmana /), while the work's meanings and its other entries write "Lakṣmaṇa /: — **fixed**
  - A `chalisa.cau8`: Verse word सीता (awa shared) spells the name without IAST ("Sita, Rama's consort"), while the work's meanings and its other entries write "Sītā, Rāma's consort": — **fixed**
  - A `chalisa.cau9`: Verse word लंक (awa shared) spells the name without IAST ("Lanka"), while the work's meanings and its other entries write "Laṅkā": — **fixed**
  - A `chalisa.cau14`: Verse word ब्रह्मादि (awa shared) spells the name without IAST ("Brahma and others"), while the work's meanings and its other entries write "Brahmā and the others": — **fixed**
  - A `chalisa.cau14`: Verse word नारद (awa shared) spells the name without IAST ("sage Narada"), while the work's meanings and its other entries write "the sage Nārada": — **fixed**
  - A `chalisa.cau14`: Verse word सारद (awa shared) spells the name without IAST ("Sarasvati /), while the work's meanings and its other entries write "Sarasvatī /: — **fixed**
  - A `chalisa.cau14`: Verse word अहीसा (awa shared) spells the name without IAST ("Shesha (lord of serpents)"), while the work's meanings and its other entries write "Śeṣa (lord of serpents)": — **fixed**
  - A `chalisa.cau13`: Verse word श्रीपति (awa shared) spells the name without IAST ("consort of Lakshmi"), while the work's meanings and its other entries write "consort of Lakṣmī": — **fixed**
  - A `chalisa.cau17`: Verse word बिभीषन (awa shared) spells the name without IAST ("Vibhishana, Ravana's brother"), while the work's meanings and its other entries write "Vibhīṣaṇa, Rāvaṇa's brother": — **fixed**
  - A `chalisa.cau31`: Verse word जानकी (awa shared) spells the name without IAST ("Janaki (Sita)"), while the work's meanings and its other entries write "Jānakī (Sītā)": — **fixed**
  - A `chalisa.cau39`: Verse word गौरीसा (awa shared) spells the name without IAST ("Shiva (Gauri's lord)"), while the work's meanings and its other entries write "Śiva (Gaurī's lord)": — **fixed**
  - A `chalisa.cau40`: Verse word तुलसीदास (awa shared) spells the name without IAST ("Tulsidas, the poet"), while the work's meanings and its other entries write "Tulasīdāsa, the poet": — **fixed**
  - A `chalisa.cau40`: Verse word हरि (awa shared) spells the name without IAST ("Lord Hari (Vishnu)), while the work's meanings and its other entries write "Lord Hari (Viṣṇu): — **fixed**
  - A `chalisa.cau6`: Verse word संकर (awa shared) spells the name without IAST ("Lord Shiva /), while the work's meanings and its other entries write "Lord Śiva /: — **fixed**
  - A `chalisa.cau2`: Verse word अंजनि names her 'अंजना / Añjanā', while both meanings and both hard-word entries of the same verse say 'अंजनी / Añjanī': — **fixed**
  - A `chalisa.cau39`: Hard-word entry हनुमानचालीसा writes 'Hanumān Cālīsā', while the English meaning of the same verse and the shared entry chālīsā write 'Chālīsā'. — **fixed**
  - D `chalisa.cau6`: Hindi and English give संकर सुवन two different senses: — **not taken: the owner-approved Sundarakāṇḍa meaning; अंश and "born of" are both the tradition’s**
  - D `chalisa.cau16`: English adds 'great' (the verse has only उपकार, 'a favour'); — **fixed**
  - B `chalisa.cau33`: The book (base witness of the Chālīsā shelf, named in this work's reconciliation.md) differs from our text in words the Sundarakāṇḍa reconciliation never lists: — **fixed by hand**
  - F `shelf`: The shelf description's English is the opening words ('Shri Guru Charan Saroj Raj'), while its siblings on the Hanumān shelf (Bajrang Baan, Shri Balaji Chalisa) and nearly every chālīsā give the title as the English desc — **fixed**
  - B `chalisa.do1`: reconciliation.md points to the book's Chālīsā as 'image i-022 …', but it begins on i-021 (book p. — **fixed**
- Recording `ashwin-pathak`: its verses are taken from the Sundarakāṇḍa's recording (`source.json` "take"); the track starts at its first verse and ends where the Sundarakāṇḍa's next verse starts.

## Har Har Har Mahadev (`har-har-mahadev-aarti`)
- Witnesses read: Drik Panchang mahadev-aarti.html (base, only witness; drik.py). Book OCR searched (औढरदानी, त्रिमूर्ति, विवसन, शशिधर, कालातीत, अतिदीन): only chance hits in other texts; not in the book, as recorded.
- Verses compared: 12 (refrain + 11 stanzas) word by word against Drik: identical apart from recorded standard changes.
- Meanings read: 12 hi / 12 en, with underlined entries.
- Words read: all verse words of 12 verses (~120 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found.
- E: 1 (परे in the Hindi meanings underlined with the entry of परा 'supreme').
- F: no error found.
- Findings:
  - E `aarti.pad2`: In the Hindi meanings of stanzas 2 (twice: — **covered**

## Jagjanani Jai Jai (`jagjanani-aarti`)
- Witnesses read: Drik Panchang shri-jagajanani-aarti.html (base, only witness; drik.py). docs/reviews/jagjanani-aarti-doubts.jsonl read.
- Verses compared: 14 (refrain + 13 stanzas) word by word against Drik: identical apart from recorded standard changes.
- Meanings read: 14 hi / 14 en, with underlined entries.
- Words read: all verse words of 14 verses (~150 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: 1 low (two doubts left open in the doubts file, against PLAYBOOK §2).
- D: no error found.
- E: 3 (उमा entry speaks of the Mānas; en 'hari' entry speaks of the Mānas; परे underlined with the entry of परा).
- F: no error found.
- Findings:
  - E `aarti.pad4`: The verse word उमा, and उमा underlined in the Hindi meaning, open the shared entry 'पार्वतीजी, शिवजीकी पत्नी; — **covered**
  - E `aarti.pad3`: The underlined English word Hari (Hari who sustains) opens the shared entry 'Hari, a name of Viṣṇu; — **covered**
  - E `aarti.pad2`: परे ('beyond') in the Hindi meanings of stanza 2 ('इन्द्रियोंसे परे') and stanza 10 ('कालसे परे') is underlined and opens the entry of परा, 'परम, सबसे ऊँची / supreme, highest': — **covered**
  - B `aarti.pad8`: Two readings are left open in docs/reviews/jagjanani-aarti-doubts.jsonl (pad8 सरुपा, 'open doubt' also in reconciliation.md; — **fixed by hand**
- Recording `anuradha-paudwal` (YouTube faxIif-3F8o): plays start 1100.85 s, end 1853.38 s. Starts heard in 5-s windows: 13 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): aarti.pad7. Starts set from the windows: none.

## Jai Jai Jaharveer Hare (`jaharveer-aarti`)
- Witnesses read: book page images i-104, i-105 (pp. 105–106); Drik Panchang shri-jaharveer-aarti.html (drik.py).
- Verses compared: 8 (refrain + 7 stanzas) word by word against book and Drik: identical to the book apart from recorded standard changes; Drik's विघ्न recorded.
- Meanings read: 8 hi / 8 en, with underlined entries.
- Words read: all verse words of 8 verses (~150 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found (Rāṇā in the en entries for Jevar/Bāchal is supported by the Jāharvīr Chālīsā's जेवर राना).
- B: no unrecorded difference.
- D: no error found.
- E: 1 (en 'hari' entry speaks of the Mānas).
- F: no error found.
- Findings:
  - E `aarti.tek`: The underlined English word Hari (twice in the refrain: — **covered**

## Shri Jaharveer Chalisa (`jaharveer-chalisa`)
- Witnesses read: book page images i-100, i-101, i-102, i-103, i-104 (pp. 101–105, whole text); Drik Panchang `shri-jaharveer-chalisa.html` (whole text).
- Verses compared: 55 of 55 (2 dohās, 53 chaupāīs), word by word against the book and Drik.
- Meanings read: 55 hi, 55 en.
- Words read: every verse word (about 520 tokens, 330 distinct entries) and every underlined meaning word, including the work's own glossary (hi, en).
- Title / shelf: work.json title, by, sections; library/index.json chalisa › jaharveer entry and the aarti shelf's group title.
- A: verse-word entries name the people in another spelling than the meanings (Gogā, Jāharavīra, Jevara, Bāchala, Kāchala, Arjana, Sarjana, Anaṅgapāla, Cauhāna, Siriyala, kotwal, guggula, Magha, Tulsidas): 18; चौहान "Cauhān"; Saṅgaladīpa vs Saṅgaldīp. 20 findings. (The shared Gorakh / Nāth spellings found in gorakhnath-chalisa recur here; not filed twice.)
- B: text agrees with the book line for line; every Drik difference is recorded. No findings.
- D: meanings say what the verses say; hi and en agree. No findings.
- E: underlined नरसिंह (Viṣṇu's avatāra) and लीला / Līlā ("divine play") for the paṇḍit and the horse; work en "līlī" contradicts work hi "लीली"; Rāṇā entry names the Kṛṣṇa Chālīsā; Hari entry names the Mānas; roots of शस्त्र, पाना, सारी. 8 findings.
- F: title and shelf consistent. No findings.
- Findings:
  - E `chalisa.cau39`: The Hindi meaning's 'नरसिंह पण्डित' is underlined and opens the shared entry for Viṣṇu's man-lion incarnation ('Narasiṁha … who burst from a pillar to save Prahlāda'); — **fixed**
  - E `chalisa.cau39`: In cau39 'लीला घोड़ा' is Līlā the horse, but the underlined लीला (Hindi meaning) opens 'भगवान्‌के खेल-जैसे काम … क्रीड़ा' and the underlined Līlā (English meaning) opens 'divine play; — **fixed**
  - E `chalisa.cau37`: The work's own English entry for Līlī calls her 'the mare of Gūgā (Jāharvīr)', but in the story (cau37–39) Līlī is the mare who bore Līlā, the horse that became Gūgā's; — **fixed**
  - E `chalisa.cau12`: The underlined 'Rāṇā' (Rāṇā Jevar) opens a shared entry whose second half is about another work ('in the Kṛṣṇa Chālīsā, the Rāṇā who sent Mīrā a snake'), which misleads in the Jāharvīr Chālīsā. — **fixed**
  - E `chalisa.cau7`: The underlined 'Hari' (Gūgā, 'a devotee of Hari') opens a shared entry tied to the Mānas ('in the Mānas also Śrī Rāma'): — **covered**
  - A `chalisa.do2`: Hard-word entry चौहान gives 'Cauhān', while the English meaning and the en entry chauhān write 'Chauhān': — **fixed**
  - A `chalisa.cau42`: The work's own Hindi hard-word entry spells the land 'Saṅgaladīpa', while the English meaning and the English entry write 'Saṅgaldīp'. — **fixed**
  - A `chalisa.do2`: Verse word गूगा (awa shared) spells the name "Gogā (Jāharavīra)", while this work's meanings and hard-word entries write "Gūgā (Gogā, Jāharvīr)": — **fixed**
  - A `chalisa.cau5`: Verse word गूगावीर (awa shared) spells the name "Gogā the hero (Jāharavīra)", while this work's meanings and hard-word entries write "Gūgā the hero (Jāharvīr)": — **fixed**
  - A `chalisa.cau1`: Verse word जाहर (awa shared) spells the name "Jāhara (Gogā)", while this work's meanings and hard-word entries write "Jāhar (Gūgā)": — **fixed**
  - A `chalisa.cau2`: Verse word जाहरवीर (awa shared) spells the name "Jāharavīra Gogā (a folk deity)", while this work's meanings and hard-word entries write "Jāharvīr Gūgā (Gogājī, a folk deity)": — **fixed**
  - A `chalisa.do1`: Verse word जेवर (awa shared) spells the name "King Jevara (the father of Gogā)", while this work's meanings and hard-word entries write "King Jevar (the father of Gūgā)": — **fixed**
  - A `chalisa.cau41`: Verse word जेवरराव (awa shared) spells the name "Rāva Jevara (the father of Gogā)", while this work's meanings and hard-word entries write "Jevar Rāv (the father of Gūgā)": — **fixed**
  - A `chalisa.cau12`: Verse word बाछल (awa shared) spells the name "Queen Bāchala (the mother of Gogā)", while this work's meanings and hard-word entries write "Queen Bāchal (the mother of Gūgā)": — **fixed**
  - A `chalisa.do1`: Verse word बाछला (awa shared) spells the name "Queen Bāchala (the mother of Gogā)", while this work's meanings and hard-word entries write "Queen Bāchal (the mother of Gūgā)": — **fixed**
  - A `chalisa.cau33`: Verse word काछल (awa shared) spells the name "Kāchala (Bāchala's sister)", while this work's meanings and hard-word entries write "Kāchal (Bāchal's sister)": — **fixed**
  - A `chalisa.cau44`: Verse word अरजन (awa shared) spells the name "Arjana (Kāchala's son)", while this work's meanings and hard-word entries write "Arjan (Kāchal's son)": — **fixed**
  - A `chalisa.cau44`: Verse word सरजन (awa shared) spells the name "Sarjana (Kāchala's son)", while this work's meanings and hard-word entries write "Sarjan (Kāchal's son)": — **fixed**
  - A `chalisa.do2`: Verse word अनंगपाल (awa shared) spells the name "King Anaṅgapāla (Tomara king of Delhi)", while this work's meanings and hard-word entries write "King Anaṅgpāl (Tomara king of Delhi)": — **fixed**
  - A `chalisa.do2`: Verse word चौहान (awa shared) spells the name "the Cauhāna Rajput clan", while this work's meanings and hard-word entries write "the Chauhān Rajput clan": — **fixed**
  - A `chalisa.cau11`: Verse word श्रीयल (awa shared) spells the name "Queen Siriyala (Gogā's wife)", while this work's meanings and hard-word entries write "Queen Śrīyal (Siriyal, Gūgā's wife)": — **fixed**
  - A `chalisa.cau39`: Verse word भज्जु (awa shared) spells the name "Bhajjū (the kotwal)", while this work's meanings and hard-word entries write "Bhajjū (the kotwāl)": — **fixed**
  - A `chalisa.cau35`: Verse word गूगल (awa shared) spells the name "guggula (the blessed grain given as prasāda)", while this work's meanings and hard-word entries write "guggal (the blessed grain given as prasāda)": — **fixed**
  - A `chalisa.cau23`: Verse word माघ (awa shared) spells the name "month of Magha", while this work's meanings and hard-word entries write "the month of Māgha": — **fixed**
  - A `chalisa.cau4`: Verse word तुलसी (awa shared) spells the name "Tulsidas (the poet) / tulsi plant, while this work's meanings and hard-word entries write "Tulasīdāsa (the poet) / the tulasī plant: — **fixed**
  - E `chalisa.cau47`: Word शस्त्र gives its root as 'सस्त्र' (a tadbhava spelling), not the Sanskrit शस्त्र it is; — **fixed**
  - E `chalisa.cau20`: In 'सन्तान पाना मुश्किल नाई' पाना is the verb 'to obtain' (the entry's third sense), but the entry gives the root 'पान' only, which misleads. — **fixed**
  - E `chalisa.cau9`: In 'पूरन हुई कामना सारी' (and cau46 'बागड़ सारी') सारी is the adjective 'all', but the entry gives root साड़ी and g=संज्ञा only. — **fixed**

## Jai Shani Deva (`jai-shani-deva-aarti`)
- Witnesses read: Drik Panchang weekdays-shaniwar-aarti.html (base, only witness; first of its two āratīs; drik.py).
- Verses compared: 4 (refrain + 3 stanzas, 22 lines) word by word against Drik: identical apart from the recorded comma/line-end changes and करू → करूं (recorded).
- Meanings read: 4 hi / 4 en, with underlined entries.
- Words read: all verse words of 4 verses (~90 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found.
- E: 2 (underlined Nala opens the monkey Nala's entry, not King Nala; en 'deva' entry's Upaniṣad note, low).
- F: no error found.
- Findings:
  - E `aarti.pad1`: The underlined English word Nala ('King Nala came under Śani's period') opens the shared entry for the monkey Nala of Śrī Rāma's army, who built the bridge to Laṅkā: — **covered**
  - E `aarti.tek`: The underlined English word Deva (in 'Śani Deva', refrain twice-thrice and stanza 3) opens the shared entry 'a god, a shining one; — **covered**

## Aarti Kijai Shri Janak Lali Ki (`janaki-aarti`)
- Witnesses read: Drik Panchang janaki-mata-aarti.html (base, only witness; drik.py). Book OCR searched (जनक लली, हरिचन्द): no copy.
- Verses compared: 4 (refrain + 3 stanzas) word by word against Drik: identical apart from recorded changes (comma, सुमन्गल → सुमंगल, वन्धन → बन्धन).
- Meanings read: 4 hi / 4 en, with underlined entries.
- Words read: all verse words of 4 verses (~45 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found.
- E: no error found.
- F: no error found.
- Findings: none.

## Jai Janakinatha Jai Shri Raghunatha (`janakinath-aarti`)
- Witnesses read: Drik Panchang shri-janakinatha-aarti.html (base, only witness; drik.py). Book OCR searched (जानकीनाथा, मनीराम): no copy.
- Verses compared: 6 (refrain + 5 stanzas) word by word against Drik: identical apart from recorded changes (commas, प्रभु!).
- Meanings read: 6 hi / 6 en, with underlined entries.
- Words read: all verse words of 6 verses (~75 tokens).
- Title / shelf: work.json, library/index.json checked (the part name and topic are the shortened "जय जानकीनाथा", as in several sibling āratīs).
- A: no error found (कौसल्या in the meanings for the verse's कौशल्या follows the library's Mānas spelling).
- B: no unrecorded difference.
- D: no error found.
- E: no error found.
- F: no error found.
- Findings: none.

## Shish Gang Ardhang Parvati (`kailashvasi-aarti`)
- Witnesses read: Drik Panchang lord-kailasavasi-aarti.html (base, only witness; drik.py). Book OCR searched (कैलासी, सुखरासी, लक्षासी): hits i-064, i-183, i-429 are other texts; no copy.
- Verses compared: 10 stanzas (40 lines) word by word against Drik: identical apart from recorded standard changes.
- Meanings read: 10 hi / 10 en, with underlined entries.
- Words read: all verse words of 10 verses (~190 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: 1 low (न्ग/न्ज kept from Drik, while janaki-aarti corrects the same habit; title affected).
- B: no unrecorded difference.
- D: no error found.
- E: 1 (underlined 'Kalpa' in 'Kalpa trees' opens the 'age of the world' sense).
- F: see A (title spelling follows the text).
- Findings:
  - E `aarti.pad4`: In the English meaning 'Kalpa trees and pārijāta trees', the underlined word Kalpa opens the shared entry 'a kalpa, an age of the world: — **covered**
  - A `aarti.pad1`: The text keeps Drik Panchang's typing of the class nasal as न् (अर्धन्ग, भृन्गी, गुन्जा-सी), which also puts न्ग into the title (शीश गंग अर्धन्ग पार्वती), next to गंग written with the anusvāra in the same line and भृंगी  — **not taken: the base’s spelling kept (a Hindi āratī, not Sanskrit; Pāṇini’s nasal rule is for Sanskrit)**

## Kalaratri Jai Jai Mahakali (`kalaratri-aarti`)
- Witnesses read: Drik Panchang devi-kalaratri-aarti.html (base, only witness; drik.py).
- Verses compared: 5 stanzas (20 lines) word by word against Drik: identical apart from recorded line-end/numbering changes.
- Meanings read: 5 hi / 5 en, with underlined entries.
- Words read: all verse words of 5 verses (~90 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: no unrecorded difference.
- D: no error found (stanza 4: Hindi 'रक्तदन्ता और अन्नपूर्णा यदि कृपा करें' is the honorific plural; English reads one goddess — consistent with the verse's करे).
- E: no error found.
- F: no error found.
- Findings: none.

## Shri Kali Chalisa (`kali-chalisa`)
- Witnesses read: book page images i-201, i-202, i-203, i-204, i-205 (pp. 202–206, whole text); Drik Panchang `kali-mata-chalisa.html` (whole text).
- Verses compared: 57 of 57 (3 dohās, 54 chaupāīs), word by word against the book and Drik.
- Meanings read: 57 hi, 57 en.
- Words read: every verse word (about 560 tokens, about 400 distinct entries) and every underlined meaning word, with the work's own glossary.
- Title / shelf: work.json title, by, sections; library/index.json chalisa › kali beside Mahakali.
- A: 11 verse-word entries spell names without IAST (Bhavani, Ambika, Uma, Girija, Kali, Durga, Parvati, Sati/Shiva, Shesha, mridanga, Ganga). 11 findings.
- B: text agrees with the book line for line; every Drik difference and every correction is recorded. No findings.
- D: meanings say what the verses say; hi and en agree. No findings.
- E: Mānas notes in उमा (hi), Bhavānī, Girijā, Māyā, Satī; Tārā opens only Vāli's wife; स्मृति opens only the smṛti books; girdle only the verb; योगिनी / yoginī lack the Goddess-as-yoginī sense. 10 findings. (The ब्रह्म "here Paraśurāma" entry, filed under gorakhnath-chalisa, is underlined here too, cau13.)
- F: title and shelf consistent. No findings.
- Findings:
  - E `chalisa.cau3`: The underlined उमा in the Hindi meaning (a name of Kālī in a list of the Goddess's names) opens a shared entry ending 'मानसमें शिवजी उन्हें रामकथा सुनाते हैं / to whom Śiva tells the Rāma story in the Mānas': — **covered**
  - E `chalisa.cau5`: The underlined 'Bhavānī' (cau5, cau35, cau48) opens a shared entry ending 'to whom Śiva tells the Mānas': — **covered**
  - E `chalisa.cau4`: The underlined 'Girijā' opens the shared entry with the Mānas note 'to whom Śiva tells the Mānas' (same entry and fix as in gorakhnath-chalisa do1). — **covered**
  - E `chalisa.cau3`: The underlined 'Māyā' (here a name of the Goddess) opens the shared entry ending 'In the Mānas, Sītā is the Lord's māyā' (same entry and fix as in gorakhnath-chalisa cau27). — **covered**
  - E `chalisa.cau9`: In cau9 ('तारा भुवनेश्वरी'), cau42 ('माँ तारा') and do3 ('जय तारा') Tārā is the goddess, one of the ten Mahāvidyās, but the underlined 'Tārā' opens only 'Tārā, Vāli's wife, mother of Aṅgada', a sense that cannot fit. — **covered**
  - E `chalisa.cau17`: In 'पुष्टि तुष्टि धृति स्मृति' the Goddess is memory (English: — **fixed**
  - E `chalisa.cau28`: 'At your waist are girdle-bells' uses girdle as a noun (a waist-band), but the underlined 'girdle' opens only the verb 'to encircle, to surround like a belt'. — **covered**
  - E `chalisa.cau15`: In cau15 ('मेघस्वना तपस्विनि योगिनी') yoginī is a name of the Goddess herself beside 'the ascetic', but the underlined योगिनी (Hindi) and yoginī (English) open only 'a fearsome female attendant of Durgā, seen on battlefi — **covered**
  - E `chalisa.cau5`: The underlined 'Satī' opens a shared entry ending 'Śiva calls Pārvatī by this name', a note from the Mānas's dialogue that has no place in a list of Kālī's names. — **covered**
  - A `chalisa.cau5`: Verse word भवानी (awa shared) spells the name without IAST ("Bhavani (Parvati)"), while the work's meanings write "Bhavānī (Pārvatī)": — **covered**
  - A `chalisa.cau3`: Verse word अंबिका (awa shared) spells the name without IAST ("Ambika (name of Parvati)"), while the work's meanings write "Ambikā (a name of Pārvatī)": — **fixed**
  - A `chalisa.cau3`: Verse word उमा (awa shared) spells the name without IAST ("Uma (Parvati)"), while the work's meanings write "Umā (Pārvatī)": — **fixed**
  - A `chalisa.cau4`: Verse word गिरिजा (awa shared) spells the name without IAST ("Girija (Parvati)"), while the work's meanings write "Girijā (Pārvatī)": — **fixed**
  - A `chalisa.cau8`: Verse word कालिका (awa shared) spells the name without IAST ("Goddess Kali"), while the work's meanings write "the goddess Kālī": — **fixed**
  - A `chalisa.cau4`: Verse word दुर्गा (awa shared) spells the name without IAST ("Durga /), while the work's meanings write "Durgā /: — **fixed**
  - A `chalisa.cau2`: Verse word जगदंबा (awa shared) spells the name without IAST ("mother of the world (Parvati)"), while the work's meanings write "mother of the world (Pārvatī)": — **covered**
  - A `chalisa.cau5`: Verse word सती (awa shared) spells the name without IAST ("Sati, Shiva's consort / chaste wife"), while the work's meanings write "Satī, Śiva's consort / chaste wife": — **covered**
  - A `chalisa.cau51`: Verse word अनंत (awa shared) spells the name without IAST ("endless / Shesha / the Lord"), while the work's meanings write "endless / Śeṣa / the Lord": — **fixed**
  - A `chalisa.cau30`: Verse word मृदंग (awa shared) spells the name without IAST ("mridanga drum"), while the work's meanings write "mṛdaṅga drum": — **fixed**
  - A `chalisa.cau27`: Verse word गंगा (awa shared) spells the name without IAST ("the Ganga"), while the work's meanings write "the Gaṅgā": — **fixed**
  - E `chalisa.cau15`: English half of the योगिनी finding above: — **covered**

## Jai Jai Ambe Jai Katyayani (`katyayani-aarti`)
- Witnesses read: Drik Panchang devi-katyayani-aarti.html (base, only witness; drik.py). docs/reviews/katyayani-aarti-doubts.jsonl looked for (absent). DNA Hindi (named for a doubt) not reachable here; not needed for any finding.
- Verses compared: 5 stanzas (20 lines) word by word against Drik: identical apart from recorded changes (छुडाने → छुड़ाने, line ends, numbers).
- Meanings read: 5 hi / 5 en, with underlined entries.
- Words read: all verse words of 5 verses (~85 tokens).
- Title / shelf: work.json, library/index.json checked.
- A: no error found.
- B: 1 (reconciliation.md still calls कही an open doubt in a doubts file that does not exist; settled below).
- D: no error found.
- E: 1 (भण्डारोंको underlined with the entry of भण्डारा 'communal feast').
- F: no error found.
- Findings:
  - E `aarti.pad5`: In the Hindi meaning 'भण्डारोंको भरपूर कर देंगी' (storehouses, as the English 'fill the storehouses' and the verse word भण्डारे = 'भण्डार, खजाने / storehouses' have it), the underline on भण्डारोंको opens the entry of भण् — **not taken: the underline is fixed in the app instead (भण्डारोंको is read as भण्डार)**
  - B `aarti.pad2`: reconciliation.md contradicts itself: — **fixed by hand**

## Om Jai Shri Shyam Hare (`khatu-shyam-aarti`)
- Witnesses read: Book i-155 (image read); Drik Panchang shyam-baba-aarti.html (drik.py).
- Verses compared against the witnesses: 7 of 7 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 7/7, en 7/7 (no per-line pieces in this work).
- Verse words read: 97 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 26.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 1 finding(s): aarti.tek (medium)
- F (title, shelf): no finding
- Findings:
  - E `aarti.tek`: The English meaning underlines 'Hari' (Śrī Śyāma Hari); — **covered**

## Shri Shyam Chalisa (`khatu-shyam-chalisa`)
- Witnesses read: book page images i-151, i-152, i-153, i-154 (pp. 152–155, whole text); Drik Panchang `shri-shyam-chalisa.html` (whole text).
- Verses compared: 42 of 42 (2 dohās, 40 chaupāīs), word by word against the book and Drik.
- Meanings read: 42 hi, 42 en.
- Words read: every verse word (about 420 tokens, about 330 distinct entries) and every underlined meaning word, with the work's own glossary.
- Title / shelf: work.json title (the book's running head; its heading "श्री श्याम (खाटू) चालीसा" noted in README), by, sections; library/index.json chalisa › khatu-shyam and the aarti shelf's group.
- A: Śyām vs Śyāma (2); Kaṁsa vs Kaṃsa; 10 verse-word entries without IAST (Ajamila, Shiva ×2, Rama, Narasimha, Prahlada, Maya, Vishnu, Sadan, Lakshmi). 13 findings. (हरि, हर, सती, नारद entries filed under other works recur here.)
- B: text agrees with the book line for line; every Drik difference and correction is recorded. No findings.
- D: meanings say what the verses say; hi and en agree. No findings.
- E: underlined भीमके opens only "terrible"; Mukunda "here of Śrī Rāma" for Bāla Mukunda; भाले (भोले-भाले) opens "forehead / spear"; root of भाले. 4 findings. (Māyā and Hari entries with Mānas notes, filed under gorakhnath and jaharveer, are underlined here too: cau14, cau8.)
- F: title and shelf consistent. No findings.
- Findings:
  - E `chalisa.cau3`: In the Hindi meaning 'वे भीमके सुपुत्र हैं … कहीं वे भीमके पौत्र' the underlined भीमके (twice) opens 'भयंकर, डरावना / terrible, fearsome': — **covered**
  - E `chalisa.cau8`: The underlined 'Mukunda' in 'Śrī Bāla Mukunda' (the child Kṛṣṇa) opens a shared entry that says 'here of Śrī Rāma': — **covered**
  - E `chalisa.cau33`: In the Hindi meaning '… मनके गोरे और भोले-भाले हैं' the underlined भाले opens the entry for भाला, 'भाल, माथा / भाला, बरछा / the forehead / a spear', a suffix-stripping match that cannot fit (भोले-भाले: — **fixed**
  - E `chalisa.cau33`: Verse word भाले (in भोले भाले, 'guileless') gives the root भाला, which is 'spear'; — **fixed**
  - A `chalisa.cau5`: Hard-word entry बर्बरीक ends 'worshipped as Khāṭū Śyām', while the English meanings and the entries khāṭū, बर्बरीक (verse word) and श्याम write 'Śyāma'. — **fixed**
  - A `chalisa.cau36`: The work's own hard entry खाटू writes 'Khāṭū Śyām'; — **fixed**
  - A `chalisa.cau11`: Hard-word entry कंस writes 'Kaṁsa' (ṁ), while the English meaning of the same verse and the verse word कंस write 'Kaṃsa' (ṃ, the IAST the library's English uses). — **fixed**
  - A `chalisa.cau24`: Verse word अजामिल (awa shared) spells the name "Ajamila (a sinful Brahmin saved)", while the work's meanings write "Ajāmila (a sinful Brahmin saved)": — **covered**
  - A `chalisa.cau14`: Verse word ईसा (awa shared) spells the name "Lord (Shiva) / the Lord", while the work's meanings write "Lord (Śiva) / the Lord": — **fixed**
  - A `chalisa.cau9`: Verse word खरारी (awa shared) spells the name "slayer of Khara (Rama)", while the work's meanings write "slayer of Khara (Rāma)": — **fixed**
  - A `chalisa.cau10`: Verse word नरहरि (awa shared) spells the name "Narasimha (man-lion)", while the work's meanings write "Narasiṃha (man-lion)": — **fixed**
  - A `chalisa.cau10`: Verse word प्रहलाद (awa shared) spells the name "Prahlada, the devotee", while the work's meanings write "Prahlāda, the devotee": — **fixed**
  - A `chalisa.cau14`: Verse word मायापति (awa shared) spells the name "Lord of Maya", while the work's meanings write "Lord of māyā": — **fixed**
  - A `chalisa.cau8`: Verse word मुकुंदा (awa shared) spells the name "Mukunda (Vishnu), giver of liberation", while the work's meanings write "Mukunda (Viṣṇu), giver of liberation": — **fixed**
  - A `chalisa.cau24`: Verse word सदन (awa shared) spells the name "abode / Sadan (Sadanā the butcher, a devotee)", while the work's meanings write "abode / Sadana (Sadana the butcher, a devotee)": — **fixed**
  - A `chalisa.cau8`: Verse word श्री (awa shared) spells the name "Lakshmi /, while the work's meanings write "Lakṣmī /: — **fixed**
  - A `chalisa.cau16`: Verse word महेश (sa shared) spells the name "Lord Shiva", while the work's meanings write "Lord Śiva": — **fixed**

## Shri Krishna Chalisa (`krishna-chalisa`)
- Witnesses read: book page images i-032, i-033, i-034, i-035 (pp. 33–36), every line; Drik Panchang `shree-krishna-chalisa.html` (via drik.py) for the differences listed in reconciliation.md.
- Verses compared: 43 (3 dohās, 40 chaupāīs) against the book image, word by word. Every difference from the book is in reconciliation.md (घुँघराले, कागासुर, भारथ, क्षमहु बेगि, नवनिधि, चारि).
- Meanings read: 43 hi, 43 en (no per-line pieces in this work).
- Words read: every verse word of 43 verses (about 420 tokens) and every underlined word in hi/en meanings.
- Title/shelf: work.json title hi/en, library/index.json entry (Bhagwan Shri Krishna group, desc = opening line) checked.
- A: one spelling clash (Kākāsura in the verse-word entry vs Kāgāsura everywhere else), low.
- B: text matches the book image line for line; no unrecorded difference.
- D: meanings match their verses; nothing found.
- E: 8 findings: underlined श्याम (Khāṭū Śyāma "here"), मधुवन/Madhuvana (Sugrīva's grove), भीम (adjective, not Bhīma), सुन्दरदास (Kakarā poet of the Gaṅgā Chālīsā), Vidura (bananas vs greens, low); verse words धारो (no imperative), दे (no absolutive), लायो (root).
- F: title and shelf right; nothing found.
- Findings:
  - E `chalisa.do1, chalisa.cau28`: The underlined श्याम in our Hindi meaning opens the shared hard-word entry whose Kṛṣṇa sense says '(यहाँ खाटूश्यामजी)' / '(here Khāṭū Śyāmajī)': — **fixed by hand**
  - E `chalisa.cau13`: The underlined मधुवन (hi) and Madhuvana (en) open the shared entries for Sugrīva's grove in the Rāmāyaṇa, where the monkeys ate the fruit; — **fixed by hand**
  - E `chalisa.cau24`: The underlined भीमको in our Hindi meaning ('आपने भीमको तिनका चीरकर संहारका संकेत दिया') opens the shared entry भीम 'भयंकर, डरावना / terrible, fearsome', an adjective; — **covered**
  - E `chalisa.cau38`: The underlined सुन्दरदासने opens the shared entry सुन्दरदास, written for the Gaṅgā Chālīsā ('ककरा ग्राम ऋषि दुर्वासा । सुन्दरदास गंगा कर दासा'): — **fixed**
  - E `chalisa.cau4`: Verse word धारो has only the past sense 'धारण किया / held, kept' (g भूतकाल), but here it is an imperative ('पुनि ... — **fixed**
  - E `chalisa.cau18`: Verse word दे (in 'चरणचिन्ह दे निर्भय कीन्हें') has only the imperative 'दे / give, let' (g आज्ञार्थ); — **fixed**
  - E `chalisa.cau22`: Verse word लायो has the right sense 'ले आये / brought (back)' but its root is only लगाना, which is wrong for this sense (root लाना). — **fixed**
  - E `chalisa.cau27`: The underlined Vidura's (en) opens the shared entry saying Vidura is the one 'at whose house Kṛṣṇa ate bananas'; — **fixed**
  - A `chalisa.cau12`: The verse word कागासुर's English gives the demon as 'Kākāsura', while the verse, our English meaning and the underlined entries spell him Kāgāsura: — **fixed**

## Aarti Shri Krishna Kanhaiya Ki (`krishna-kanhaiya-aarti`)
- Witnesses read: Drik Panchang shri-krishna-kanhaiya-aarti.html (only witness).
- Verses compared against the witnesses: 6 of 6 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 6/6, en 6/6 (no per-line pieces in this work).
- Verse words read: 94 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 45.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): no finding
- F (title, shelf): no finding
- Findings: none.

## Om Jai Yaksha Kuber Hare (`kuber-aarti`)
- Witnesses read: Drik Panchang lord-kubera-aarti.html (only witness).
- Verses compared against the witnesses: 8 of 8 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 8/8, en 8/8 (no per-line pieces in this work).
- Verse words read: 150 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 32.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 4 finding(s): aarti.pad2 (medium), aarti.pad2 (medium), aarti.pad6 (medium), aarti.pad4 (low)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad2`: योगिनी (योगिनी मंगल गावैं: — **covered**
  - E `aarti.pad2`: The English meaning underlines 'yoginīs'; — **covered**
  - E `aarti.pad6`: जोत (घी की जोत जले: — **fixed**
  - E `aarti.pad4`: The shared entry for मोहन lists the mohanbhog sense twice in different wording (a duplicated sense). — **covered**

## Shri Kuber Chalisa (`kuber-chalisa`)
- Witnesses read: Drik Panchang `shri-kubera-chalisa.html` (via drik.py), the base; the book has no Kubera Chālīsā (README, reconciliation.md). Compared by script, line by line, after removing punctuation.
- Verses compared: 48 (4 dohās, 44 chaupāīs). The only differences from Drik (ढेर, चढ़ा दे) are both in reconciliation.md.
- Meanings read: 48 hi, 48 en.
- Words read: every verse word of 48 verses (about 560 tokens) and every underlined word.
- Title/shelf: work.json title, library/index.json entry (group Kuber, desc = opening line) checked.
- A: Viśravā / Viśravas in one work's English, low.
- B: text equals Drik Panchang except the two recorded corrections; nothing found.
- D: meanings match their verses; nothing found.
- E: 5 findings: underlined भीम (adjective, not Bhīma), underlined मानस (no Mānas Parivāra sense in Hindi); roots of चढ़ा, उठा, मिटा (low).
- F: title and shelf right; nothing found.
- Findings:
  - E `chalisa.cau18`: The underlined भीम in our Hindi meaning ('जैसे पुरुषोंमें भीम बलवान् हैं') opens the shared hard-word entry 'भयंकर, डरावना / terrible, fearsome', an adjective; — **covered**
  - E `chalisa.cau44`: The underlined मानस in our Hindi meaning ('मानस परिवारने कुबेरजीकी कीर्ति गायी है') opens the shared hard-word entry (the Mānasa lake; — **fixed**
  - E `chalisa.cau31`: Verse word चढ़ा (in 'और चढ़ा दे', raise higher) has the sense right but the root only चढ़ना (to climb); — **fixed**
  - E `chalisa.cau31`: Verse word उठा (in 'पुनः उठा दे', lift up again) has root उठना and grammar भूतकाल only; — **fixed**
  - E `chalisa.cau33`: Verse word मिटा (in 'भूख कुबेर मिटा दे') has root मिटना and grammar भूतकाल only; — **fixed**
  - A `chalisa.cau8`: Kubera's father is spelt two ways in the work's English: — **fixed**

## Aarti Kunj Bihari Ki (`kunj-bihari-aarti`)
- Witnesses read: Drik Panchang kunj-bihari-aarti.html (only witness); audio not checked (class C skipped).
- Verses compared against the witnesses: 5 of 5 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 5/5, en 5/5 (no per-line pieces in this work).
- Verse words read: 127 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 31.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 1 finding(s): aarti.pad3 (medium)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad3`: ते in जहां ते / स्मरन ते is the Braj-Hindi postposition 'from, by', but the entry the app opens is the Sanskrit dictionary's (sa.json), whose root and grammar give only the Sanskrit pronoun (युष्मद् / तद्); — **covered**
- Recording `kumar-vishu` (YouTube rI-DXgiHALU): plays start 1542.34 s, end 1818.82 s. Starts heard in 5-s windows: 6 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: aarti.pad1, aarti.pad3.

## Kushmanda Jai Jag Sukhdani (`kushmanda-aarti`)
- Witnesses read: Drik Panchang devi-kushmanda-aarti.html (only saved witness; Aaj Tak/InstaAstro cited from web, not opened).
- Verses compared against the witnesses: 5 of 5 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 5/5, en 5/5 (no per-line pieces in this work).
- Verse words read: 94 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 8.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 3 finding(s): aarti.pad5 (high), aarti.pad3 (medium), aarti.pad3 (low)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad5`: भर in 'मेरे तुम भण्डारे भर दो' means 'fill' (भर दो: — **fixed**
  - E `aarti.pad3`: दो in 'पूर्ण कर दो' / 'भर दो' is the verb 'give, please do'; — **fixed**
  - E `aarti.pad3`: कर in 'पूर्ण कर दो' / 'पूरे कर दो' is the verb करना; — **fixed**

## Om Jai Lakshmi Mata (`lakshmi-aarti`)
- Witnesses read: Book i-189, i-190 (images read); Aarti Mala i-347 (image read); Drik Panchang lakshmi-mata-aarti.html; every changed word checked to be in the witness the reconciliation names.
- Verses compared against the witnesses: 8 of 8 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 8/8, en 8/8 (no per-line pieces in this work).
- Verse words read: 113 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 20.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 2 finding(s): aarti.pad1 (high), aarti.pad6 (medium)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad1`: उमा (verse word, and underlined in our Hindi meaning 'आप ही उमा, रमा और ब्रह्माणी हैं') opens the shared entry '...; — **fixed**
  - E `aarti.pad6`: जाता in 'क्षीरोदधि जाता' is the participle 'born' (Sanskrit जात, from जन्), and the entry lists that sense, but its root is only जाना ('to go') and grammar only वर्तमान, which is wrong for that sense and misleads a learn — **fixed**
- Recording `anuradha-paudwal` (YouTube sd31yGqZFlA): plays start 1998.25 s, end 2330.25 s. Starts heard in 5-s windows: 6 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: aarti.tek.

## Shri Lakshmi Chalisa (`lakshmi-chalisa`)
- Witnesses read: book page images i-182, i-183, i-184, i-185 (pp. 183–186), every line; Drik Panchang `lakshmi-mata-chalisa.html` (via drik.py) for the two corrections (त्रिविध ताप, तन में) and the order of "केहि प्रकार".
- Verses compared: 44 (1 dohā + 1 sorathā opening, 39 chaupāīs, 2 closing dohās) against the book image word by word. The only differences (cau21, cau38) are in reconciliation.md and confirmed in Drik.
- Meanings read: 44 hi, 44 en.
- Words read: every verse word of 44 verses (about 470 tokens) and every underlined word.
- Title/shelf: work.json title, library/index.json entry (Mother Lakshmi group, desc = opening line) checked.
- A: nothing found (Lakṣmī, Viṣṇu, Jagadambā/Jagadambikā consistent).
- B: text matches the book except the two recorded corrections; nothing found.
- D: meanings match their verses; nothing found.
- E: 6 findings: underlined भवानी / Bhavānī open the Pārvatī (and Mānas) entries where Lakṣmī is meant (hi, en); verse words भवानी and जगदम्बा name only Pārvatī; पै lacks "on"; करके root (low).
- F: title and shelf right; nothing found.
- Findings:
  - E `chalisa.cau6, chalisa.cau32`: The underlined भवानी in our Hindi meanings ('हे जगज्जननी भवानी!', 'हे लक्ष्मी भवानी!') opens the shared hard-word entry 'शिवजीकी पत्नी, पार्वतीजी'; — **fixed**
  - E `chalisa.cau6, chalisa.cau32`: The underlined Bhavānī in our English meanings ('be gracious, Bhavānī, Mother of the world'; — **fixed**
  - E `chalisa.cau6, chalisa.cau32`: Verse word भवानी has only 'पार्वतीजी / Bhavani (Parvati)'; — **covered**
  - E `chalisa.cau3`: Verse word जगदम्बा (folded to जगदंबा) is glossed 'जगत की माता (पार्वती) / mother of the world (Parvati)'; — **covered**
  - E `chalisa.do3`: Verse word पै in 'मातु लक्ष्मी दास पै करहु दया की कोर' is the postposition 'on, upon' (our meaning: — **fixed**
  - E `chalisa.cau39`: Verse word करके (in 'रूप चतुर्भुज करके धारण', having taken) has root करकना and grammar भूतकाल only, which belong to the senses 'चुभे / खटके'; — **fixed**

## Jai Lakshmi-Vishno (`lakshmi-narayan-aarti`)
- Witnesses read: Drik Panchang shri-lakshminarayana-aarti.html (only witness).
- Verses compared against the witnesses: 8 of 8 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 8/8, en 8/8 (no per-line pieces in this work).
- Verse words read: 84 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 41.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 2 finding(s): aarti.pad5 (high), aarti.pad2 (medium)
- F (title, shelf): 1 finding(s): shelf (low)
- Findings:
  - E `aarti.pad5`: परमानन्द (परमानन्द बिधाता: — **covered**
  - E `aarti.pad2`: गरुड़ (underlined in our Hindi meaning) and Garuḍa (underlined in our English) open entries ending 'मानसमें उन्होंने काकभुशुण्डिजीसे रामकथा सुनी' / 'in the Mānas he hears the Rāma story from Kākabhuśuṇḍi': — **fixed by hand**
  - F `shelf`: The shelf description calls this 'the aarti of Bhagwan Vishnu', but the āratī is of Lakṣmī-Nārāyaṇa together (every stanza alternates Lakṣmī and Viṣṇu; — **fixed by hand**

## Jai Sharanam Varanam Namo Namah (`lalita-aarti`)
- Witnesses read: Book i-281 (image read); Drik Panchang lalita-mata-aarti.html.
- Verses compared against the witnesses: 5 of 5 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 5/5, en 5/5 (no per-line pieces in this work).
- Verse words read: 81 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 39.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 2 finding(s): aarti.pad1 (medium), aarti.tek (low)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad1`: राजेश्वरि is glossed 'रानियोंकी रानी' (queen of queens), but राज + ईश्वरी is 'sovereign (mistress) of kings / of the realm', as its own parts (राज: — **fixed**
  - E `aarti.tek`: The English meanings underline 'salutations' (16 times in this work) as a hard word; — **fixed**

## Shri Lalita Chalisa (`lalita-chalisa`)
- Witnesses read: book page images i-277, i-278, i-279, i-280 (pp. 278–281), every line; Drik Panchang `lalita-mata-chalisa.html` (via drik.py) for तव (cau1, cau28), cau19, cau23 (तब in both witnesses) and the closing dohā.
- Verses compared: 49 (48 chaupāīs, 1 closing dohā) against the book image word by word. Every difference (तव ×2, two exclamation marks, सहस्रार) is in reconciliation.md.
- Meanings read: 49 hi, 49 en.
- Words read: every verse word of 49 verses (about 520 tokens) and every underlined word.
- Title/shelf: work.json title, library/index.json entry (Mother Lalita group, desc = opening line) checked.
- A: nothing found.
- B: text matches the book except the recorded corrections; cau23 तब kept as both witnesses print it (recorded); nothing found.
- D: meanings match their verses; nothing found.
- E: 5 findings: underlined Tārā opens Vāli's wife (high); त्रिपुरप्यारी entry gives the rejected "beloved of Śiva" and lacks the meaning's sense; चक्र lacks the Śrīcakra / yogic cakra sense; होता falls back to Sanskrit hotṛ; underlined उमा carries a Mānas note (low).
- F: title and shelf right; nothing found.
- Findings:
  - E `chalisa.cau8`: The underlined Tārā in our English meaning ('Dhūmāvatī, Bagalā, Bhairavī, Tārā, Bhuvaneśvarī and Kamalā are your unfolding') opens the shared entry 'Tārā, Vāli's wife, mother of Aṅgada'; — **fixed**
  - E `chalisa.cau19`: Verse word त्रिपुरप्यारी gives first 'त्रिपुर (शिवजी)की प्यारी / beloved of Tripura (Śiva)', the reading reconciliation.md rejects ("Śiva is Tripurāri, not त्रिपुर"), and lacks the reading our meanings take, 'beloved of  — **fixed**
  - E `chalisa.cau5`: Verse word चक्र in 'चक्र स्वामिनी' (our meaning: — **fixed**
  - E `chalisa.cau23`: Verse word होता (in 'होता तब सेवा अनुरागी', 'becomes') has no Awadhi entry and falls back to the Sanskrit one, whose root is होतृ (the priest) and grammar प्रथमा एकवचन: — **fixed**
  - E `chalisa.cau37`: The underlined उमा in our Hindi meaning ('आप हैमवती, उमा और ब्रह्माणी हैं') opens the shared entry that adds 'मानसमें शिवजी उन्हें रामकथा सुनाते हैं', a Mānas note with no place in a Lalitā Chālīsā, where Umā is a name o — **fixed**

## Jai Mahagauri Jagat Ki Maya (`mahagauri-aarti`)
- Witnesses read: Drik Panchang devi-mahagauri-aarti.html (only saved witness; Aaj Tak cited from web, not opened).
- Verses compared against the witnesses: 5 of 5 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 5/5, en 5/5 (no per-line pieces in this work).
- Verse words read: 110 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 29.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): 1 finding(s): aarti.pad1 (medium)
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 3 finding(s): aarti.pad1 (high), aarti.pad1 (medium), aarti.pad5 (low)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad1`: उमा (verse word, and underlined in our Hindi meaning 'हे उमा, भवानी!') opens the shared entry with 'मानसमें शिवजी उन्हें रामकथा सुनाते हैं' / '...to whom Śiva tells the Rāma story in the Mānas': — **fixed**
  - E `aarti.pad1`: Our English meaning underlines 'Bhavānī' and 'māyā'; — **fixed**
  - A `aarti.pad1`: The English meaning writes the place as 'Kankhal' (plain spelling) beside 'Haridvāra' (IAST) in the same sentence; — **fixed**
  - E `aarti.pad5`: सोच in 'सोच तुम क्या रहे हो' is the verb stem (सोचना, 'think'); — **fixed**

## Mangal Ki Seva Sun Meri Deva (`mahakali-aarti`)
- Witnesses read: Book i-211, i-212, i-213 (images read); Drik Panchang mahakali-mata-aarti.html (drik.py; its differences match the reconciliation); Aarti Mala i-344–i-346 not re-opened (used only for the stanza division and two readings).
- Verses compared against the witnesses: 8 of 8 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 8/8, en 8/8 (no per-line pieces in this work).
- Verse words read: 235 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 40.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): 2 finding(s): aarti.pad4 (medium), aarti.pad4 (low)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad4`: Our English meaning underlines 'Bhavānī' (pad4, pad6, pad7); — **fixed**
  - E `aarti.pad4`: वारी in 'आदित वारी' is the noun 'day (of the week)' (आदित वारी: — **fixed**

## Shri Mahakali Chalisa (`mahakali-chalisa`)
- Witnesses read: book page images i-207, i-208, i-209, i-210, i-211 (pp. 208–212), every line; Drik Panchang `mahakali-mata-chalisa.html` (via drik.py) for the two corrections (ब्योम, धूम्र) and the kept readings (महाकराली, मारद, नलिनबिलोचनि, वासिनि).
- Verses compared: 46 (3 opening dohās, 42 chaupāīs, 1 closing dohā) against the book image word by word. Both differences (cau20, cau22) are in reconciliation.md and confirmed in Drik.
- Meanings read: 46 hi, 46 en.
- Words read: every verse word of 46 verses (about 470 tokens) and every underlined word.
- Title/shelf: work.json title, library/index.json entry (Mother Kali group, desc = opening line) checked.
- A: nothing found.
- B: text matches the book except the two recorded corrections; nothing found.
- D: meanings match their verses; nothing found.
- E: 6 findings: underlined Tārā opens Vāli's wife (high); underlined सिद्धि / Siddhi (the poet) open only "supernatural power" (hi, en; high); जगदम्बा entry names Pārvatī (low); शिरो grammar (low); सुन्दरी lacks the Mahāvidyā sense (low).
- F: title and shelf right; nothing found.
- Findings:
  - E `chalisa.do2, chalisa.cau6`: The underlined Tārā in our English meanings ('Victory to Tārā, victory to Kālikā, victory to the host of the ten Mahāvidyās'; — **fixed by hand**
  - E `chalisa.do2, chalisa.cau12, chalisa.cau35`: The underlined सिद्धि / सिद्धिकी in our Hindi meanings, where it is the poet's name ('हिन्दके एक कवि सिद्धि', 'कवि सिद्धिकी पुरातन माता', 'ब्रह्माण्डकी और कवि सिद्धिकी माता'), opens the shared entry with only 'अलौकिक शक् — **fixed**
  - E `chalisa.do2, chalisa.cau12, chalisa.cau35`: The underlined Siddhi in our English meanings, the poet's name ('Siddhi, a poet of Hind'; — **fixed by hand**
  - E `chalisa.cau4, chalisa.cau38`: Verse word जगदम्बा (folded to जगदंबा) is glossed 'जगत की माता (पार्वती) / mother of the world (Parvati)'; — **covered**
  - E `chalisa.cau3`: Verse word शिरो in 'शिरो मालिका' (a garland of heads, शिरोमालिका) has grammar 'द्वितीया एकवचन (संधिमें शिरः → शिरो)', an accusative; — **fixed**
  - E `chalisa.cau6`: Verse word सुन्दरी (folded to सुंदरी) has only 'सुंदर स्त्री / beautiful woman', while our English meaning and the work's own underlined entry read it as the Mahāvidyā Sundarī (Tripurasundarī) in a list of goddesses ('Tā — **fixed**

## Shri Mahalakshmi Chalisa (`mahalakshmi-chalisa`)
- Witnesses read: book page images i-186, i-187, i-188, i-189 (pp. 187–190); Drik Panchang printout `mahalakshmi-mata-chalisa.html` (via drik.py).
- Verses compared: 42 (2 dohā + 40 chaupāī), every line against the book images and Drik; all differences found are recorded in reconciliation.md.
- Meanings read: 42 hi / 42 en.
- Words read: every verse word (about 330 tokens) and every underlined meaning word.
- Title/shelf checked: work.json title and by; library/index.json entry (lakshmi group, desc = opening line; en desc = title as on 53 sibling chālīsās).
- A (spelling, names): no errors found (Mahālakṣmī, Viṣṇu, Śeṣa, Śiva consistent).
- B (text vs witnesses): text matches the book; the four corrections and the kept readings are recorded; no unrecorded difference.
- D (meanings): no errors found; hi and en agree verse by verse.
- E (word meanings): 6 findings (Bhavānī en/hi hard entries and awa word entry name Pārvatī/the Mānas for Mahālakṣmī; Govinda hard entry contradicts poet's-name reading; तत्त्व hard entry lacks "element"; बिलोक lacks "having seen").
- F (title, shelf): no errors found.
- Findings:
  - E `chalisa.cau2`: The underlined 'Bhavānī' in the English meaning (cau2, cau10) opens the shared en entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas'. — **covered**
  - E `chalisa.cau2`: The underlined 'भवानी' in the Hindi meaning (cau2, cau10) opens 'शिवजीकी पत्नी, पार्वतीजी'; — **covered**
  - E `chalisa.cau2`: Verse word भवानी (cau2, cau10) opens the shared awa entry 'पार्वतीजी / Bhavani (Parvati)'; — **fixed**
  - E `chalisa.cau40`: The underlined 'Govinda' in the English meaning of cau40 opens 'Govinda, a name of Kṛṣṇa (Viṣṇu); — **covered**
  - E `chalisa.cau11`: The underlined 'तत्त्वोंसे' in the Hindi meaning ('पाँच तत्त्वोंसे सृष्टि रची') opens the shared hard entry 'असली सार, सत्य; — **covered**
  - E `chalisa.cau14`: Verse word बिलोक opens 'देखता है / looks' (finite present), but in 'छवि बिलोक सुरमुनि नरनारी करे…' it is the absolutive 'having seen', as the meaning renders it ('छवि देखकर' / 'Seeing your beauty'). — **fixed**

## Jai Mahavir Prabho (`mahavir-aarti`)
- Witnesses read: Book i-144 (image read); Drik Panchang shri-mahavir-aarti.html.
- Verses compared against the witnesses: 7 of 7 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 7/7, en 7/7 (no per-line pieces in this work).
- Verse words read: 75 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 19.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): no finding
- B (text vs witnesses): 1 finding(s): aarti.pad1 (low)
- D (meanings vs verses): no finding
- E (word meanings): no finding
- F (title, shelf): no finding
- Findings:
  - B `aarti.pad1`: जन्में (with anusvāra) is not a Hindi form: — **fixed by hand**

## Shri Mahavir (Tirthankar) Chalisa (`mahavir-chalisa`)
- Witnesses read: book page images i-140, i-141, i-142, i-143 (pp. 141–144); Drik Panchang printout `shri-mahavir-chalisa.html`.
- Verses compared: 40 (2 dohā + 36 chaupāī + 2 sorathā), every line against the book images and Drik; the only differences (quotation marks around चन्द्र; Drik भग for भाग) are recorded.
- Meanings read: 40 hi / 40 en.
- Words read: every verse word (about 330 tokens) and every underlined meaning word.
- Title/shelf checked: work.json title/by; library/index.json (mahavir group, desc = opening line).
- A (spelling, names): 3 findings, low (split पर ×2 against §4; Cāṁdanapura with ISO ṁ instead of IAST).
- B (text vs witnesses): no errors found.
- D (meanings): no errors found (cau5 तमसे and cau7 वीर रण राग readings are recorded with reasons).
- E (word meanings): 4 findings (digambara en hard entry about Sāī Bābā; Siddha en/hi hard entries lack the Jaina sense; अतिशय hi hard entry lacks "miracle"). Not flagged: जोधराज awa entry "(जयपुरके) एक दीवान" could not be verified either way on the web (low).
- F (title, shelf): no errors found.
- Findings:
  - E `chalisa.cau4`: The underlined 'digambara' in the English meaning opens the shared en entry "'clad in the sky', naked; — **covered**
  - E `chalisa.do1`: The underlined 'Siddhas' in the English meaning of do1 opens 'the Siddhas, perfected ones: — **covered**
  - E `chalisa.do1`: The underlined 'सिद्धोंको' in the Hindi meaning of do1 opens 'योग और तपसे सिद्धियाँ पाये हुए महात्मा; — **covered**
  - E `chalisa.cau20`: The underlined 'अतिशय' in the Hindi meaning ('टीलेमें अतिशय (चमत्कार) दिखलाया') opens 'बहुत अधिक, अत्यन्त / exceeding, very great' (an adjective); — **covered**
  - A `chalisa.cau29`: Hindi house style (style.md §4, postpositions joined): — **fixed**
  - A `chalisa.cau34`: Hindi house style (style.md §4, postpositions joined to pronouns): — **fixed**
  - A `chalisa.cau19`: 'Cāṁdanapura' uses the ISO 15919 letter ṁ; — **not taken: kept Cāṁdanapura: the app matches a word of a meaning to its entry by its letters, and m̐ breaks the match**

## Mangal Murti Jai Jai Hanumanta (`mangal-murti-hanuman-aarti`)
- Witnesses read: Drik Panchang weekdays-mangalwar-aarti.html (only witness).
- Verses compared against the witnesses: 12 of 12 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 12/12, en 12/12 (no per-line pieces in this work).
- Verse words read: 201 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 30.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): 2 finding(s): aarti.pad3 (low), aarti.pad9 (low)
- B (text vs witnesses): no finding: text matches the witnesses; every difference is in reconciliation.md
- D (meanings vs verses): no finding
- E (word meanings): no finding
- F (title, shelf): no finding
- Findings:
  - A `aarti.pad3`: Hanumān's mother is 'अंजनी' / 'Añjanī' in our Hindi and English meaning (and in their underlined entries), but the verse word अंजनि opens 'माता अंजना' / 'Mother Añjanā': — **fixed**
  - A `aarti.pad9`: The entry for दहन (दारिद्र दहन) writes 'जलाने वाले' apart; — **fixed**

## Shri Ganesh Chalisa (`mangalmay-ganesha-chalisa`)
- Witnesses read: Drik Panchang printout `shree-ganesha-chalisa.html` (the only witness; the book does not print this chālīsā: OCR of all book images searched for मंगलमय/करिवर/डासना/षडानन, hits are only the other Gaṇeśa Chālīsā and āratīs).
- Verses compared: 42 (2 dohā + 40 chaupāī) against Drik, word by word; every difference is in reconciliation.md's table.
- Meanings read: 42 hi / 42 en.
- Words read: every verse word (about 380 tokens) and every underlined meaning word.
- Title/shelf checked: work.json title/by; library/index.json (ganesha group).
- A (spelling, names): 10 low findings, all one kind (split पर in Hindi meanings against §4).
- B (text vs witnesses): no errors found.
- D (meanings): 1 finding (cau37 hi and en differ on how the earth was circled).
- E (word meanings): 2 findings (hi hard entry गौरीश = Śiva contradicts the settled reading; साई entry still marked "(?) / पाठ अस्पष्ट" though settled).
- F (title, shelf): 1 finding (English desc repeats the title, so two identical "Shri Ganesh Chalisa" rows on one shelf).
- Findings:
  - E `chalisa.cau40`: The underlined 'गौरीश' in the Hindi meaning ('उनके साथी आप हैं, हे गौरीश!') opens the shared hi entry 'गौरीके स्वामी, शिवजी', contradicting the work's settled reading (Gaurīśa here addresses Gaṇeśa; — **fixed**
  - E `chalisa.cau33`: Verse word साई opens an entry marked as a guess: — **fixed**
  - D `chalisa.cau37`: Hindi and English differ: — **fixed**
  - F `shelf`: Two works on the Gaṇeśa shelf now have the same title 'Shri Ganesh Chalisa'; — **fixed**
  - A `chalisa.cau4`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau5`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau6`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau12`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau14`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau19`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau21`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau35`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau38`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau39`: Hindi house style (style.md §4: — **fixed**

## Shri Narasimha Chalisa (`narasimha-chalisa`)
- Witnesses read: Drik Panchang printout `narasimha-chalisa.html` (the only witness; book OCR searched for नरसिंह/नृसिंह: the only hit, i-405, is the Durgā Chālīsā's line about the Narasiṃha form).
- Verses compared: 44 (4 dohā + 40 chaupāī) against Drik word by word; the four changes are in reconciliation.md's table; no unrecorded difference.
- Meanings read: 44 hi / 44 en.
- Words read: every verse word (about 400 tokens) and every underlined meaning word.
- Title/shelf checked: work.json title/by (by भगवान नृसिंह is the same on the two Narasiṃha āratīs); library/index.json (narasimha group).
- A (spelling, names): 3 low findings (Narasiṁha / Nṛsiṃha spellings in hard entries beside the work's Narasiṃha; split पर).
- B (text vs witnesses): text matches Drik; 1 finding in reconciliation.md (points to a doubts file that does not exist, contradicting its own "Readings settled").
- D (meanings): no errors found.
- E (word meanings): 3 findings (आगमें falsely underlined as आगम; शिव in cau40 has no "auspicious" sense; रहे has only a past-tense sense).
- F (title, shelf): no errors found.
- Findings:
  - E `chalisa.cau8`: The Hindi meaning's 'आगमें' ('प्रचण्ड आगमें जलाया', in the fire) is underlined as the hard word 'आगम' and opens 'आगम, तन्त्रशास्त्र / आना, आगमन' (the Āgamas / arrival): — **fixed**
  - E `chalisa.cau40`: Verse word शिव (in 'शिव स्वरूप है शरण तुम्हारी') opens only 'भगवान शिव / Lord Śiva', but the work reads शिव here as 'auspicious, blessing' (reconciliation 'Readings settled' cau40, MW śiva; — **fixed**
  - B `reconciliation`: reconciliation.md says the परसाया doubt 'is in docs/reviews/narasimha-chalisa-doubts.jsonl', but that file does not exist and the same file's 'Readings settled' says the reading is settled (cau7). — **fixed**
  - A `glossary`: The Hindi meanings' underlined नरसिंह (do1, cau1, cau2, cau24, cau26, cau31, cau36, do4) opens an entry whose English spells the name 'Narasiṁha' (ISO ṁ), while this work's English meanings and the sibling hard entry श्र — **fixed**
  - A `glossary`: The underlined 'प्रह्लाद' (cau6, cau10, cau16) opens an entry whose English calls the Lord 'Nṛsiṃha', a third spelling beside the work's 'Narasiṃha' (and the en 'prahlāda' hard entry's 'Narasiṁha'). — **covered**
  - E `chalisa.cau35`: Verse word रहे opens only 'रहे / remained, were (भूतकाल बहुवचन)', but in 'सो नर रहे तुम्हारा प्यारा' (cau35) and 'उस घर आनन्द रहे' (do4) it is present/subjunctive singular ('remains', as the meanings render it). — **fixed**
  - A `chalisa.cau24`: Hindi house style (style.md §4, postpositions joined to pronouns): — **fixed**

## Om Jai Jagadanandi (`narmada-aarti`)
- Witnesses read: Book i-264 (image read); Drik Panchang narmada-mata-aarti.html.
- Verses compared against the witnesses: 7 of 7 (text.txt line by line; reconciliation table checked).
- Meanings read: hi 7/7, en 7/7 (no per-line pieces in this work).
- Verse words read: 116 (entries opened by review.py --words; NONE/POSSIBLE: 0). Underlined meaning words read: 44.
- Title (work.json, library work.json) and shelf entry (library/index.json: title, desc, deity group) checked against siblings.
- A (spelling, names): 1 finding(s): aarti.pad5 (medium)
- B (text vs witnesses): 1 finding(s): aarti.pad4 (medium)
- D (meanings vs verses): 1 finding(s): aarti.pad4 (low)
- E (word meanings): 1 finding(s): aarti.pad5 (medium)
- F (title, shelf): no finding
- Findings:
  - E `aarti.pad5`: जोती in 'घाटन घाट कोटी रतन जोती' is the noun 'light' (ज्योति); — **fixed**
  - A `aarti.pad5`: The place is 'Amarakaṇṭaka' in our English meaning and in the verse word's entry (अमरकंठ), but the entry the Hindi meaning's underline opens (अमरकण्टकमें) spells it 'Amarkaṇṭak': — **fixed**
  - D `aarti.pad4`: 'भव मेटन्ती' (she wipes away bhava, worldly existence, i.e. — **fixed**
  - B `aarti.pad4`: Unrecorded difference: — **fixed by hand**

## Shri Narmada Chalisa (`narmada-chalisa`)
- Witnesses read: book page images i-260, i-261, i-262, i-263 (pp. 261–264); Drik Panchang printout `narmada-mata-chalisa.html`; MW (sanskrit_dict.py) for सोमोद्भवा.
- Verses compared: 43 (3 dohā + 40 chaupāī), every line against the book images and Drik; the one correction and the kept readings are recorded.
- Meanings read: 43 hi / 43 en.
- Words read: every verse word (about 380 tokens) and every underlined meaning word.
- Title/shelf checked: work.json title/by; library/index.json (narmada group, desc = opening line).
- A (spelling, names): 8 low findings (Amarkaṇṭak / Kankhal in hard entries against the work's Amarakaṇṭaka / Kanakhala; split पर ×6).
- B (text vs witnesses): text matches the book; 1 finding (cau22 समोद्भवा read as सोमोद्भवा in the meanings, unrecorded; metre and MW support सोमोद्भवा).
- D (meanings): no errors found.
- E (word meanings): 2 findings (भवानी as Narmadā's epithet has only the Pārvatī sense; en hard entry Sarasvatī lacks the river).
- F (title, shelf): no errors found.
- Findings:
  - B `chalisa.cau22`: The verse reads समोद्भवा (as both witnesses print it), but our meanings read it as सोमोद्भवा ('born of the moon', a name of the Narmadā) and the word entry's root is सोमोद्भवा. — **fixed**
  - E `chalisa.cau1`: Verse word भवानी in 'नर्मदा भवानी' (cau1, cau3) opens only 'पार्वतीजी / Bhavani (Parvati)', and the underlined Bhavānī in the meanings opens the hi entry 'शिवजीकी पत्नी, पार्वतीजी' and the en entry '…to whom Śiva tells t — **fixed**
  - E `chalisa.cau17`: The underlined 'Sarasvatī' in the English meanings of cau17 ('at Kurukṣetra the glory of the Sarasvatī') and cau28 ('The Sarasvatī gives it in three days') opens only 'Sarasvatī, the goddess of speech and learning'; — **covered**
  - A `chalisa.cau2`: One place, two spellings: — **fixed**
  - A `chalisa.cau17`: One place, two spellings: — **fixed**
  - A `chalisa.do2`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau5`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau10`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau32`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau33`: Hindi house style (style.md §4: — **fixed**
  - A `chalisa.cau36`: Hindi house style (style.md §4: — **fixed**

## Om Jai Narsingh Hare (`narsingh-aarti`)
- Witnesses read: Drik Panchang om-jai-narsingh-hare.html (only witness; book has none); reconciliation.md and README read.
- Verses compared: 4 (refrain + 3 stanzas), every line against the witness(es).
- Meanings read: 4 hi / 4 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 4 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues (Narasiṁha, Hari, Brahmā, Śiva consistent).
- B: text = Drik word for word; दुस्यु→दस्यु recorded in reconciliation.
- C: skipped (audio checked by the lead).
- D: meanings match verses; hi/en agree.
- E: all verse words have fitting entries; no NONE/POSSIBLE.
- F: title, by, shelf (Bhagwan Narasimha group) consistent.
- Findings: none.

## Aarti Kijai Narsingh Kunwar Ki (`narsingh-kunwar-aarti`)
- Witnesses read: Drik Panchang aarti-kijai-narsingh-kunwarki.html (only witness); reconciliation.md and README read.
- Verses compared: 4 (refrain + 3 stanzas), every line against the witness(es).
- Meanings read: 4 hi / 4 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 4 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: 1 low (Prahlāda entry 'Nṛsiṃha'/'He' vs work's Narasiṁha).
- B: text = Drik; all line changes recorded.
- C: skipped (audio checked by the lead).
- D: meanings match (readings settled in reconciliation followed).
- E: entries fit; तुलसी sa entry 'Tulsidas/tulsi' non-IAST (reported under ram-raghuvir-aarti).
- F: title/shelf fine.
- Findings:
  - A `aarti.pad1`: The underlined/verse-word entry for प्रह्लाद (shared, hard) spells the avatar 'Nṛsiṃha' (ṃ) and uses a capital 'He' for the Lord, while this work's meanings spell him 'Narasiṁha' (ṁ) and style.md §5 keeps pronouns for th — **fixed**

## Aarti Kijai Shri Natvar Ji Ki (`natvar-aarti`)
- Witnesses read: Drik Panchang lord-natavara-aarti.html (only witness); reconciliation.md and README read.
- Verses compared: 6 (refrain + 5 stanzas), every line against the witness(es).
- Meanings read: 6 hi / 6 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 6 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = Drik; comma removal and order recorded.
- C: skipped (audio checked by the lead).
- D: meanings match; pad4 अघ reading as recorded.
- E: 2 (underlined परे opens परा 'supreme' — medium; 'upholder' entry's '(dharma)' — low).
- F: fine.
- Findings:
  - E `aarti.pad3`: In the Hindi meaning 'गुणोंसे परे' (beyond the guṇas) the word परे is underlined, but the app opens the entry for परा ('परम, सबसे ऊँची' / 'supreme, highest'), a sense that does not fit. — **fixed**
  - E `aarti.pad3`: The English meaning's 'upholder' (of the whole universe) is underlined with the shared hard entry 'one who supports and keeps up (dharma)' / '(धर्मको) धारण करने…'; — **fixed**

## Shri Navagraha Chalisa (`navagraha-chalisa`)
- Witnesses read: book page images i-078, i-079, i-080, i-081, i-082 (pp. 79–83); Drik Panchang printout (drik.py); Chalisa Mala OCR i-401–i-403 for cau31/cau34 only.
- Verses compared: 44 of 44 (4 dohās, 40 chaupāīs) against the book images; Drik checked against the reconciliation's list.
- Meanings read: 44 hi / 44 en (whole; no per-line pieces).
- Words read: every verse word (~330) and every underlined meaning word.
- Title / shelf: work.json title, parts, sections; library/index.json entry (navagraha group, desc) checked.
- A: one finding (Sundaradāsa / Sundardās in the drawers); names otherwise consistent.
- B: no unrecorded difference; text matches the book line for line (सैहिंकेय is in all three witnesses, kept).
- D: meanings match the verses; no finding.
- E: सोम (hi, en) drawers lack the Moon; Tārā (en) drawer is Vāli's wife; जीव / Jīva drawers lack the name of Bṛhaspati; शिखी lacks Rāhu's sense in cau30; अघमन part gloss and वप्र root unrecorded (low).
- F: title and shelf consistent with siblings; no finding.
- Findings:
  - E `chalisa.do2, chalisa.cau7`: The Hindi meaning underlines सोम (here the Moon: — **covered**
  - E `chalisa.do2, chalisa.cau7`: The English meaning underlines Soma ('Śaśi and Soma, the Moon'; — **covered**
  - E `chalisa.cau15`: The English meaning 'O son of Tārā' underlines Tārā, whose shared entry is 'Tārā, Vāli's wife, mother of Aṅgada'. — **covered**
  - E `chalisa.cau19`: Both meanings underline जीव / Jīva, used here as a name of Bṛhaspati ('जीव और बृहस्पति आपके नाम हैं'), but the hi and en drawers give only 'living being; — **covered**
  - E `chalisa.cau19`: Same as above for the English drawer jīva. — **covered**
  - E `chalisa.cau30`: In cau30 शिखी is one of Rāhu's names ('शिखी आदि बहु नाम तुम्हारा', addressed to Rāhu; — **fixed**
  - A `chalisa.cau37, chalisa.do4`: The poet is 'Sundaradāsa' in our English meanings and the en drawer, but the hi underline drawer (सुन्दरदास, shown from the Hindi meaning) and the verse-word entry सुन्दरदास give the English 'Sundardās': — **covered**
  - A `chalisa.do4`: Same spelling mismatch in the awa verse-word entry सुन्दरदास (shared; — **covered**
  - E `chalisa.cau34`: अघमन is split अघ + मन with मन glossed 'मर्दन करनेवाला' (crusher); — **not taken: no reading to record: the meaning gives अघमन as "crusher of sin", as the line reads**
  - E `chalisa.cau26`: The work's own awa entry for वप्र gives root 'बभ्रु' and says it is Babhru of Śani's ten names; — **not taken: the identification with बभ्रु is a guess: the entry now says only "a name of Śani"**

## Om Jai Parshudhari (`parashuram-aarti`)
- Witnesses read: Book i-149, i-150 (pp. 150–151) read on images; Drik shri-parashurama-aarti.html; reconciliation.md and README read.
- Verses compared: 8 (refrain + 7 stanzas), every line against the witness(es).
- Meanings read: 8 hi / 8 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 8 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = book and Drik word for word; quotation marks removal recorded.
- C: skipped (audio checked by the lead).
- D: meanings match verses.
- E: 1 high (नर-सिंह opens Narasiṁha-avatar entry; meaning is 'lion among men').
- F: fine.
- Findings:
  - E `aarti.pad1`: The verse word नर-सिंह (जमदग्नी सुत नर-सिंह) opens the shared entry for the avatar Narasiṁha ('Viṣṇu's man-lion incarnation, who burst from a pillar to save Prahlāda'), but here it is Paraśurāma praised as 'a lion among  — **fixed**

## Shri Parshuram Chalisa (`parashurama-chalisa`)
- Witnesses read: book page images i-145, i-146, i-147, i-148, i-149 (pp. 146–150; the āratī on i-149 not part of this work); Drik Panchang per the reconciliation's list.
- Verses compared: 44 of 44 (3 dohās, 40 chaupāīs, 1 śloka) against the book images.
- Meanings read: 44 hi / 44 en (whole).
- Words read: every verse word (~330) and every underlined meaning word.
- Title / shelf: work.json title, parts, sections; library/index.json (parashurama group "Bhagwan Parshuram", desc) checked.
- A: no finding (names consistent: Paraśurāma, Jamadagni, Reṇukā, Bhṛgu, Kārtavīrya).
- B: no unrecorded difference; both changes (सहस्र in cau19 and the śloka) recorded.
- D: cau35 'भाई!' address with 'आपने/you' makes the brother the giver; cau7 Hindi 'अर्थात्' gloss.
- E: पूर्णेन्दु hi drawer says 'this āratī'; 'girdle' en drawer has only the verb sense.
- F: title and shelf consistent with siblings; no finding.
- Findings:
  - D `chalisa.cau35`: The meaning takes भाई as an address to the listener (as reconciliation.md settles) but then keeps Paraśurāma in the second person: — **fixed**
  - D `chalisa.cau35`: Same in English. — **fixed**
  - D `chalisa.cau7`: The Hindi meaning adds a gloss with 'अर्थात्' ('सुखभावमें, अर्थात् चौथे घरमें'), the 'that is to say' that style.md §2 rules out; — **fixed**
  - E `chalisa.cau40`: The Hindi meaning underlines पूर्णेन्दु, whose drawer says 'पूर्णेन्दु, इस आरतीके कवि' / 'the poet of this āratī': — **fixed**
  - E `chalisa.cau11`: The English meaning underlines 'girdle' (a noun: — **covered**

## Jai Parvati Mata (`parvati-aarti`)
- Witnesses read: Book i-249 (p. 250) read on image; Drik parvati-mata-aarti.html; Aarti Mala i-348 only via reconciliation (not reopened: its readings are not in the text except as recorded); reconciliation.md and README read.
- Verses compared: 8 (refrain + 7 stanzas), every line against the witness(es).
- Meanings read: 8 hi / 8 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 8 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = book with recorded changes (देववधू, सहस्र, pad5 line 2 = Drik's line as written); no unrecorded difference.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: 1 low (ता falls to sa pronoun entry with तद् grammar).
- F: fine.
- Findings:
  - E `aarti.pad2`: The verse word ता (in 'नृत्य करत ता था', the dance syllables) opens the Sanskrit shared entry whose root and grammar are those of the pronoun तद् ('द्वितीया बहुवचन स्त्रीलिंग (ताः)'); — **fixed**
- Recording `anuradha-paudwal` (YouTube faxIif-3F8o): plays start 1860.15 s, end 2363.96 s. Starts heard in 5-s windows: 7 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): aarti.pad1, aarti.pad2, aarti.pad3. Starts set from the windows: none.

## Shri Parvati Chalisa (`parvati-chalisa`)
- Witnesses read: book page images i-245, i-246, i-247, i-248 (pp. 246–249); Drik Panchang differences as listed in reconciliation.md.
- Verses compared: 42 of 42 (2 dohās, 40 chaupāīs) against the book images.
- Meanings read: 42 hi / 42 en (whole).
- Words read: every verse word (~300) and every underlined meaning word.
- Title / shelf: work.json title and by ("माँ पार्वती" / "Mother Parvati"); library/index.json parvati group and desc checked.
- A: no finding (Pārvatī, Śiva, Śeṣa, Kārttikeya, Gaṅgā, Nārada, Umā consistent).
- B: no unrecorded difference; the two dropped exclamation marks recorded; पहआयी kept and recorded.
- D: meanings match the verses; no finding.
- E: 'girdle' en drawer has only the verb sense (cau6; shared with parashurama-chalisa).
- F: title and shelf consistent; no finding.
- Findings:
  - E `chalisa.cau6`: The English meaning underlines 'girdle' as a noun ('a divine girdle sways at your waist'), but the shared en entry gives only the verb 'to encircle, to surround like a belt' (same entry as in parashurama-chalisa cau11; — **covered**

## Jayati Mangalagar (`pavansut-hanuman-aarti`)
- Witnesses read: Drik shri-pavanasuta-hanuman-aarti.html (only witness); reconciliation.md and README read.
- Verses compared: 5 (5 stanzas), every line against the witness(es).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 5 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: 1 medium (पुरारी sa entry 'Shiva').
- B: text = Drik; शाषी→शाखी recorded.
- C: skipped (audio checked by the lead).
- D: 1 medium (कौशला-कुशल… word entry direction contradicts meaning).
- E: 1 high (en 'Tulasī's' underlined opens the tulasī-plant entry).
- F: fine.
- Findings:
  - E `aarti.pad5`: In the English meaning 'the Rāma-city of Tulasī's mind', 'Tulasī's' is underlined and opens the entry for the tulasī plant ('the tulasī, the holy basil, dear to Viṣṇu'); — **fixed**
  - D `aarti.pad4`: The word entry for कौशला-कुशल-कल्याणभाषी says he told of Kosala's welfare ('who told of the welfare and well-being of Kosala (Ayodhyā)'), but our meanings (hi and en) say he told Kosala of Śrī Rāma's welfare ('कोसल देशको — **fixed**
  - A `aarti.pad1`: The verse word पुरारी opens the shared Sanskrit entry whose English is 'Shiva (foe of Tripura)', without IAST, while the work (and style.md §5) spells Śiva. — **fixed**

## Jai Jai Pitarji Maharaj (`pitar-aarti`)
- Witnesses read: Book i-165 (p. 166) read on image; Drik shri-pitar-aarti.html; reconciliation.md and README read.
- Verses compared: 5 (refrain + 4 stanzas), every line against the witness(es).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 5 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = book = Drik word for word.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: 2 (Bābā entry 'here Sāī Bābā of Shirdi' — high; Mahārāja 'as for Sāī Bābā' — low).
- F: 1 low (shelf hi desc पितरकी → पितरोंकी).
- Findings:
  - E `aarti.tek`: In the English meaning 'I have come to your refuge, Bābā', the underlined Bābā opens the shared hard entry ending 'here Sāī Bābā of Shirdi' / 'यहाँ शिरडीके साईं बाबा'. — **covered**
  - E `aarti.tek`: The underlined 'Mahārāja' (Pitarjī Mahārāja) opens the shared entry 'great king; — **covered**
  - F `shelf`: The shelf description in Hindi reads 'पितरकी आरती' (singular oblique), while the English is 'The aarti of Pitars (the ancestors)' (plural) and the āratī addresses the ancestors as a group; — **fixed**

## Shri Pitar Chalisa (`pitar-chalisa`)
- Witnesses read: book page images i-161, i-162 (with crops of cau8, cau9, cau15), i-163, i-164, i-165 (pp. 162–166); Drik Panchang printout in full (drik.py).
- Verses compared: 45 of 45 (5 dohās, 40 chaupāīs) against the book images and Drik.
- Meanings read: 45 hi / 45 en (whole).
- Words read: every verse word (~380) and every underlined meaning word.
- Title / shelf: work.json title and by; library/index.json pitar group ("Pitars (the ancestors)") and desc checked.
- A: झुंझुनूँ (Hindi meanings and drawers) against the verse's झुंझुनू (3 verses + the work glossary key).
- B: no unrecorded difference; cau8 and cau22 changes recorded (दीन्हा / लीन्हा in cau9 checked on a crop: the book has them).
- D: meanings match the verses; no finding.
- E: सिद्धि lacks the 'supernatural power' sense (cau32–33); स्वयं lacks 'own' (do3); नारा root (low).
- F: title and shelf consistent; no finding.
- Findings:
  - A `chalisa.cau8`: The town is spelt झुंझुनू in the verse text (book i-162, i-164, i-165; — **fixed**
  - A `chalisa.do4`: Same spelling (झुंझुनूँ for the verse's झुंझुनू) in the Hindi meaning. — **fixed**
  - A `chalisa.do5`: Same spelling in the Hindi meaning. — **fixed**
  - A `glossary`: With the meanings spelt झुंझुनू, the work's own hi underline entry must be re-keyed (and its text matched), or the underline drawer is lost. — **fixed**
  - E `chalisa.cau32, chalisa.cau33`: सिद्धि is glossed only 'accomplishment / Siddhi (the poet's name)'; — **covered**
  - E `chalisa.do3`: In 'तीरथ और स्वयं ग्राम' स्वयं means one's own (our meanings: — **fixed**
  - E `chalisa.cau19`: नारा in 'धर्म जाति का नहीं है नारा' is 'slogan' (the entry's second sense), but the entry's root is नाला for both senses; — **fixed**

## Aarti Pretraj Ki Kijai (`pretraj-aarti`)
- Witnesses read: Book i-110 (p. 112) read on image; Drik shri-pretraj-aarti.html; reconciliation.md and README read.
- Verses compared: 6 (refrain + 5 stanzas), every line against the witness(es).
- Meanings read: 6 hi / 6 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 6 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = book = Drik; कृपाल kept as recorded.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: 1 high (Bābā entry 'here Sāī Bābā'; here Bābā = Bālājī).
- F: 1 medium (English title 'Keejai' vs library-wide 'Kijai').
- Findings:
  - E `aarti.pad3`: In the English meaning ('You are obedient to Bābā … Put the petition to Bābā') the underlined Bābā opens the shared entry ending 'here Sāī Bābā of Shirdi'; — **covered**
  - F `title`: The English title spells कीजै as 'Keejai', while every sibling āratī title in the library spells it 'Kijai' (Aarti Kijai Hanuman Lala Ki, Aarti Kijai Shri Raghuvar Ji Ki, Aarti Kijai Narsingh Kunwar Ki, Aarti Kijai Shri  — **fixed by hand**

## Shri Pretraj Chalisa (`pretraj-chalisa`)
- Witnesses read: book page images i-106, i-107, i-108, i-109 (pp. 107–110), with crops of cau10, cau23, cau24 (मेंहदीपुर, अरज); Drik Panchang differences as in reconciliation.md.
- Verses compared: 44 of 44 (4 dohās, 40 chaupāīs) against the book images.
- Meanings read: 44 hi / 44 en (whole).
- Words read: every verse word (~350) and every underlined meaning word.
- Title / shelf: work.json title and by ("प्रेतराज सरकार" / "Pretraj Sarkar"); library/index.json pretraj group and desc checked.
- A: Sarakāra / Sarkār / Sarkāra in meaning and drawers; मेहंदीपुर in the awa प्रेतराज entry; Sukharām in the hi drawer.
- B: no unrecorded difference; text matches the book line for line.
- D: meanings match the verses (cau22, cau30, do4 readings as recorded); no finding.
- E: cau28 'Gaṇeśa' underlined in 'Mahant Gaṇeśa Purī' opens the god; verse word गणेश lacks the name sense.
- F: title and shelf consistent; no finding.
- Findings:
  - E `chalisa.cau28`: The English meaning 'The ascetic Mahant Gaṇeśa Purī' splits the mahant's name, so 'Gaṇeśa' is underlined and opens the drawer of the god Gaṇeśa ('the elephant-headed god, son of Śiva and Pārvatī'); — **fixed**
  - E `chalisa.cau28`: English drawer for the one-word name (new work-own entry, so the name stays underlined and opens the mahant, not the god). — **fixed**
  - E `chalisa.cau28`: The verse word गणेश (in 'महन्त गणेश पुरी') opens only 'गणेशजी / Gaṇeśa', the god; — **fixed**
  - A `chalisa.do2`: सरकार of 'प्रेतराज सरकार' is spelt three ways in one work: — **covered**
  - A `chalisa.do2`: Same: — **covered**
  - A `chalisa.do2`: Same: — **covered**
  - A `chalisa.cau1 (word प्रेतराज)`: The verse-word entry प्रेतराज spells the place मेहंदीपुर; — **covered**
  - A `chalisa.do4`: The poet is 'Sukharāma' in the English meaning, the en drawer and the awa entry, but the hi drawer सुखराम (opened from the Hindi meaning) gives the English 'Sukharām'. — **fixed**

## Jai Purushottam Deva (`purushottam-aarti`)
- Witnesses read: Drik lord-purushottam-aarti.html (only witness); reconciliation.md and README read.
- Verses compared: 8 (refrain + 7 stanzas), every line against the witness(es).
- Meanings read: 8 hi / 8 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 8 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: 1 low (work glossary 'brahmin' vs meaning 'brāhmaṇa').
- B: text = Drik word for word.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: entries fit (work glossary keys with ने work for the underline).
- F: fine.
- Findings:
  - A `aarti.pad4`: The work's own hard entry for Sudeva (underlined in the Hindi meaning) calls him 'a brahmin devotee', while the English meaning of the same verse and the work's English glossary entry say 'brāhmaṇa'; — **fixed**

## Shri Radha Chalisa (`radha-chalisa`)
- Witnesses read: book page images i-220, i-221, i-222, i-223 (pp. 221–224); Drik Panchang `printouts/drikpanchang/shri-radha-chalisa.html` (via drik.py); README, reconciliation.md, work.json, text.txt, work glossary.
- Verses compared: 43 of 43 (2 opening dohās, 40 chaupāīs, closing dohā), each line against the book image and Drik.
- Meanings read: 43 hi / 43 en.
- Words read: 404 verse-word entries, 125 underlined meaning-word entries.
- Title / shelf: work.json title and by; library/index.json entry (group श्रीराधा / Shri Radha, desc = opening line; en desc = title as on all sibling chālīsās).
- A: 2 findings (low): awa उमा English without IAST; hard entry बनवारी spelt Banvārī against Banavārī in our meanings.
- B: no finding. Every difference from the book is in reconciliation.md (वृन्दाविपिन, वृषभानु, the restored cau8–9 from Drik, बदना, युत, सादर, भजिहैं, तिहारी, the space in श्रीराधा सर्वेश्वरी); the Drik variants are listed as kept.
- D: no finding. Hindi and English agree verse by verse; cau40 reading is recorded in reconciliation.md.
- E: 8 findings: श्याम (hi hard entry "here Khāṭū Śyāmajī", and sa entry used for the verse word), उमा (Mānas note), Hari (Mānas note), विलास (no "play" sense), उचारे (past only), उजारी (root/grammar), ब्रह्मानी (en "Brahmani").
- F: no finding.
- Findings:
  - E `chalisa.cau2`: The underlined श्याम in our Hindi meanings (cau2, cau4, cau7, cau9, cau29) opens the shared hard entry 'श्याम, श्रीकृष्ण (यहाँ खाटूश्यामजी)' / 'Śyāma, Kṛṣṇa (here Khāṭū Śyāmajī)'. — **covered**
  - E `chalisa.cau2`: The verse word श्याम (cau2, cau4, cau7, cau9, cau29) has no awa entry and falls back to sa shared 'साँवला / श्यामसुन्दर श्रीकृष्ण (खाटूश्यामजी)' / 'dark-hued / Śyāma, Kṛṣṇa (Khāṭū Śyāma)': — **fixed**
  - E `chalisa.cau16`: The underlined उमा in the Hindi meaning opens the shared hard entry about the Mānas ('मानसमें शिवजी उन्हें रामकथा सुनाते हैं' / 'to whom Śiva tells the Rāma story in the Mānas'), which misleads in the Rādhā Chālīsā (the  — **fixed**
  - E `chalisa.cau35`: The underlined 'Hari' in the English meaning opens the shared entry 'Hari, a name of Viṣṇu; — **fixed**
  - E `chalisa.cau3`: The underlined विलास (in 'रासमें विलास करनेवाली') opens the shared entry 'सुख-भोग, ठाट-बाट, ऐश्वर्यका आनन्द' / 'luxury, pleasures, splendour', which has no sense of play/sport that the line needs (रास विलासिनि: — **fixed**
  - E `chalisa.cau8`: उचारे is glossed 'कहे / uttered', grammar भूतकाल; — **fixed**
  - E `chalisa.cau19`: उजारी: — **fixed**
  - E `chalisa.cau16`: ब्रह्मानी's English is only 'Brahmani' (no IAST, no sense), while its Hindi gives 'सरस्वती / ब्रह्मा की शक्ति' and the meaning uses Brahmāṇī. — **fixed**
  - A `chalisa.cau16`: The verse word उमा's English is 'Uma (Parvati)' without IAST, unlike the work's 'Umās' and the hard entry 'Umā (Pārvatī)'. — **fixed**
  - A `chalisa.cau19`: The underlined बनवारी (Hindi meaning) opens a hard entry whose English spells the name 'Banvārī', while our English meaning and the en hard entry spell it 'Banavārī'. — **fixed**

## Aarti Kijai Shri Raghuvar Ji Ki (`raghuvar-aarti`)
- Witnesses read: Book i-015 (p. 16) read on image; Drik shri-raghuvar-aarti.html; reconciliation.md and README read.
- Verses compared: 5 (refrain + 4 stanzas), every line against the witness(es).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 5 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = book; पुरूषोतम→पुरुषोतम and stanza grouping recorded.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: entries fit (अवन्ह 'protector' unsure but not contradicted).
- F: fine.
- Findings: none.

## Shri Ram Chalisa (`ram-chalisa`)
- Witnesses read: book page images i-011, i-012, i-013, i-014 (pp. 12–15); Drik Panchang `printouts/drikpanchang/shree-rama-chalisa.html` (via drik.py); README, reconciliation.md, work.json, text.txt, work glossary, audio fixes.md (for the one sung reading).
- Verses compared: 48 of 48 (46 chaupāīs, 2 closing dohās), each line against the book image and Drik; book order kept as recorded (Drik orders two blocks differently).
- Meanings read: 48 hi / 48 en.
- Words read: 478 verse-word entries, 60 underlined meaning-word entries.
- Title / shelf: work.json title and by; library/index.json entry (group श्रीराम / Shri Ram; desc = first half of cau1).
- A: no finding.
- B: no finding. The three book misprints (हदय ×2, शंरव्र) are recorded; cau39 हमरे is word for word in Drik ("तुम ही हो हमरे तन-मन धन"); every other Drik variant is in the kept list.
- D: no finding. The four settled readings (cau32, cau41, cau46, do1) are recorded with reasons; Hindi and English agree.
- E: 5 findings: हरिदास verse word glossed only "servant of Hari" though the work reads it as the poet's name; hard entry ब्रह्म ("here Paraśurāma"); पाहीं, जीते, ताकी (root/grammar or tense that misleads here).
- F: no finding.
- Findings:
  - E `chalisa.cau46`: The verse word हरिदास (cau46 and closing do1) opens only the shared awa entry 'भगवान का भक्त' / 'servant of Hari', while the work reads हरिदास as the poet's name (reconciliation.md 'Readings settled'; — **fixed**
  - E `chalisa.cau28`: The underlined ब्रह्म in the Hindi meaning (निर्गुण … ब्रह्म) opens the shared hard entry whose English second sense reads 'a brāhmaṇa (here Paraśurāma)': — **covered**
  - E `chalisa.cau3`: पाहीं in 'ब्रह्मा इन्द्र पार नहिं पाहीं' (also cau10) means 'पाते हैं' (from पाना); — **fixed**
  - E `chalisa.cau19`: जीते in 'ताते रण जीते नहिं कोई' is 'can (no one) win / defeat him', present-potential, as our meanings say ('कोई नहीं जीत सकता' / 'no one can win'); — **fixed**
  - E `chalisa.cau27`: ताकी in 'ताकी मुक्ति अवसि हो जावै' is 'उसकी' (his); — **fixed**
- Recording `bhaktidhaam` (YouTube lCwPg0LRRjk): plays start 2710.89 s, end 3026.76 s. Starts heard in 5-s windows: 26 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): chalisa.cau1, chalisa.cau2, chalisa.cau3, chalisa.cau30, chalisa.cau31, chalisa.cau32. Starts set from the windows: chalisa.cau17, chalisa.cau29, chalisa.cau11, chalisa.cau13.

## Bandaun Raghupati Karuna Nidhan (`ram-raghupati-aarti`)
- Witnesses read: Drik shri-rama-raghupati-aarti.html (only witness); reconciliation.md and README read.
- Verses compared: 9 (9 stanzas), every line against the witness(es).
- Meanings read: 9 hi / 9 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 9 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: no issues.
- B: text = Drik with recorded nasal/space normalisations.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: entries fit.
- F: fine.
- Findings: none.

## Aisi Aarti Ram Raghubir Ki Karahi Man (`ram-raghuvir-aarti`)
- Witnesses read: Drik shri-rama-raghuvira-aarti.html (only witness); reconciliation.md and README read.
- Verses compared: 6 (refrain + 5 stanzas), every line against the witness(es).
- Meanings read: 6 hi / 6 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 6 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: 1 medium (तुलसी sa entry 'Tulsidas … tulsi plant', non-IAST).
- B: text = Drik; रुप→रूप, सन्शय→संशय, commas recorded.
- C: skipped (audio checked by the lead).
- D: meanings match.
- E: entries fit apart from the तुलसी spelling.
- F: 1 low (part/topic 'Aisi Aarti Ram Raghubir Ki' vs title '… Karahi Man').
- Findings:
  - A `aarti.pad5`: The verse word तुलसी (दास तुलसी) opens the shared Sanskrit entry whose English is 'Tulsidas (the poet) / tulsi plant / Mother Tulasī…': — **covered**
  - F `title`: The work's title is 'ऐसी आरती राम रघुबीर की करहि मन' / 'Aisi Aarti Ram Raghubir Ki Karahi Man' (work.json title, shelf), but its one part and its topic are 'ऐसी आरती राम रघुबीर की' / 'Aisi Aarti Ram Raghubir Ki'; — **fixed by hand**

## Om Jai Shri Ramade (`ramdev-aarti`)
- Witnesses read: Book i-160 (p. 161) read on image; Drik shri-ramdev-aarti.html; reconciliation.md and README read.
- Verses compared: 5 (refrain + 4 stanzas), every line against the witness(es).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: every verse word of all 5 verses (review.py --words), and every underlined word in both meanings.
- Title/shelf checked: work.json title, by, parts, text.txt @topic, library/index.json entry and group.
- A: 1 low (मेनादे entry 'Mainādē' with ē).
- B: text = book = Drik word for word.
- C: skipped (audio checked by the lead).
- D: meanings match (भाण as a name, as recorded).
- E: entries fit.
- F: fine.
- Findings:
  - A `aarti.tek`: The shared entry for मेनादे gives the variant 'Mainādē' with ē, a letter not used in IAST (the library's English uses IAST; — **fixed**

## Shri Ramdev Chalisa (`ramdev-chalisa`)
- Witnesses read: book page images i-156, i-157, i-158, i-159 (pp. 157–160); Drik Panchang `printouts/drikpanchang/shri-ramdev-chalisa.html` (via drik.py); README, reconciliation.md, work.json, text.txt, work glossaries (hi, en).
- Verses compared: 42 of 42 (2 opening dohās, 40 chaupāīs), each line against the book image and Drik.
- Meanings read: 42 hi / 42 en.
- Words read: 390 verse-word entries, 103 underlined meaning-word entries.
- Title / shelf: work.json title and by; library/index.json entry (group बाबा रामदेव / Baba Ramdev; desc = first line of do1).
- A: 13 findings: the shared awa entries for the work's names spell them Rāmadeva, Ajamala, Ratanā, Pungal, Vijayasiṃha, Suganā, Bohitā, Vīramadeva, Haṛabūjī, Harajī against the meanings' Rāmdev, Ajmal, Ratnā, Puṅgal, Vijaysiṃh, Sugnā, Bauhit, Vīram, Harbū, Harjī; the work hard entries Pugal/Ratanā, Haḍbūjī, paracā.
- B: no finding. Text equals the book line for line ("No change from the book"); the Drik differences are in the kept list.
- D: no finding. Hindi and English agree; the three settled readings (cau8, cau19, cau28) are recorded.
- E: 8 findings: hard entries that give the wrong word or sense here: भैरव (Śiva's form, not the demon), नाड़ी (body channel, not the pond), लीले / Līlā (divine play, not the horse, hi and en), māyā (Mānas note); हर in "हर जी" lacks the name; सुने (past only), गाऊँ (root गाँव).
- F: no finding.
- Findings:
  - E `chalisa.cau9`: The underlined भैरव in the Hindi meaning ('आपने भैरव (राक्षस)को मारा') opens the shared hard entry 'भैरव, शिवजीका उग्र रूप, काशीके कोतवाल' / 'Bhairava, the fierce form of Śiva, guardian of Kāśī'. — **fixed by hand**
  - E `chalisa.cau18`: The underlined नाड़ी in the Hindi meanings of cau18 ('प्यारी नाड़ी (छोटा तालाब) रच दी') and cau24 ('सूखी नाड़ीमें पानी कर दिया') opens the shared hard entry 'शरीरकी नस (नली), जिसमें प्राण चलता है' / 'a channel (nāḍī) of  — **fixed by hand**
  - E `chalisa.cau34`: Līlā/लीले here is Rāmdev's horse (the blue horse, लीला घोड़ा), as both meanings say ('लीले घोड़ेपर', 'mounted on Līlā') and the verse-word entry लीले says. — **fixed by hand**
  - E `chalisa.cau34`: Same as the previous finding, Hindi side: — **fixed**
  - E `chalisa.cau1`: The underlined 'māyā' in the English meaning opens the shared entry ending 'In the Mānas, Sītā is the Lord's māyā', which does not belong in the Rāmdev Chālīsā. — **fixed**
  - A `chalisa.cau10`: The work's own hard entry पुंगल spells the place 'Pugal' (no macron) and the devotee 'Ratanā', while the work's en hard entries and English meaning use 'Pūgal' and 'Ratnā'. — **fixed**
  - A `chalisa.cau22`: The work's hard entry हड़बूजीने romanises ड़ as ḍ ('Haḍbūjī'); — **fixed**
  - A `chalisa.cau20`: The underlined जाम्भोजीने hard entry writes the miracle 'paracā', while the work's other entries and meanings write 'parcā'. — **fixed**
  - A `chalisa.do1`: The verse word रामदेव (do1, cau1) is glossed 'Bābā Rāmadeva', while every meaning and hard entry of the work (and its title) has Rāmdev. — **fixed**
  - A `chalisa.do2`: The verse word अजमल (do2, cau1) is glossed 'Ajamala (Rāmadeva's father)'; — **fixed**
  - A `chalisa.cau10`: The verse word रतना is glossed 'Ratanā … Rāmadeva … Pungal'; — **fixed**
  - A `chalisa.cau10`: The verse word पुंगल is glossed 'Pungal'; — **fixed**
  - A `chalisa.cau11`: The verse word विजयसिंह is glossed 'Vijayasiṃha'; — **fixed**
  - A `chalisa.cau12`: The verse word सुगना is glossed 'Suganā (Rāmadeva's sister)'; — **fixed**
  - A `chalisa.cau13`: The verse word बौहित is glossed only as 'बोहिता / Bohitā', a different spelling of the name from the verse and from our meanings and hard entries (बौहित / Bauhit). — **fixed**
  - A `chalisa.cau15`: The verse word वीरम is glossed 'Vīramadeva (Rāmadeva's…)'; — **fixed**
  - A `chalisa.cau22`: The verse word हरबू is glossed 'Haṛabūjī … Rāmadeva'; — **fixed**
  - A `chalisa.cau24`: The verse word हरजी is glossed 'Harajī … Rāmadeva'; — **fixed**
  - E `chalisa.cau23`: In 'परच्या सत्रह हर जी पाया' the words हर जी are the name Harjī (हरजी in cau24; — **covered**
  - E `chalisa.cau36`: सुने in 'यह चालीसा सुने सुनावे' is present ('whoever hears', as both meanings say); — **fixed**
  - E `chalisa.cau38`: गाऊँ ('क्या गुण तब गाऊँ', I sing) has the fitting sense listed second, but its root is given as गाँव (village), which misleads here. — **fixed**

## Jai Shri Rani Sati Maiya (`rani-sati-aarti`)
- Witnesses read: Book i-286, i-287 (pp. 287–288); Drik Panchang shri-rani-sati-aarti.html.
- Verses compared: 8 (every line of text.txt against the witness(es)).
- Meanings read: 8 hi / 8 en (whole; no per-line pieces in this work).
- Words read: 112 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 3.
- Result per class: A: 'Satī' en underline wrong person (E); one separated पर (low). B: every line matches book and Drik; changes (करो, सप्त, line splits) recorded. D: hi/en agree; no clause missing. E: Satī underline; कलश lacks temple sense (low). F: title, by, shelf (rani-sati, 'राणी सतीकी आरती') fine.
- Findings:
  - E `aarti.tek`: The underlined 'Satī' in the English meanings (tek 'Śrī Rāṇī Satī'; — **fixed**
  - A `aarti.pad5`: Hindi meaning writes the postposition apart, 'हृदय-पटल पर', against the house style of joined postpositions (style.md §4; — **fixed**
  - E `aarti.pad2`: कलश (कंचन कलश धरे, the temple's golden kalaśas) has only 'घड़ा / pot, jar'; — **fixed**

## Shri Rani Sati Chalisa (`rani-sati-chalisa`)
- Witnesses read: book page images i-282, i-283, i-284, i-285, i-286 (pp. 283–287; closing dohā on i-286); Drik Panchang `printouts/drikpanchang/shri-rani-sati-chalisa.html` (via drik.py); README, reconciliation.md, work.json, text.txt, work glossaries (hi, en). For the Rāṇājī entry: Wikipedia "Rani Sati" (web).
- Verses compared: 43 of 43 (2 opening dohās, 40 chaupāīs, closing dohā), each line against the book image and Drik.
- Meanings read: 43 hi / 43 en.
- Words read: 421 verse-word entries, 96 underlined meaning-word entries.
- Title / shelf: work.json title and by; library/index.json entry (group राणी सती / Rani Sati; desc = first line of do1).
- A: 9 findings: four work hard entries write रानी / Rānī Satī against राणी / Rāṇī everywhere else; shared awa names Gursāmal, Tandhan Dās, Jālīrām, Dokwa against the meanings' Gurasāmala, Tanadhanadāsa, Jālīrāma, Ḍokavā; Bāṃsal (ṃ for candrabindu).
- B: no finding. The book's slips (भवान, सुन्दरर, मु से, the comma, the quotes and "(मैं)" in cau40) are recorded; other Drik variants are in the kept lists.
- D: no finding. Hindi and English agree; the three settled readings (do2, cau28, cau34) are recorded.
- E: 7 findings: en hard entry Satī (Dakṣa's daughter, not Rāṇī Satī), Bhavānī (Mānas note), Rāṇājī ("a ruler", against the legend's loyal servant and the shared entry), Vikrama (notes on other works); shared awa सती (no sense for a satī / Rāṇī Satī), दुहाई (oath only), लेनी.
- F: no finding.
- Findings:
  - E `chalisa.cau8`: The underlined 'Satī' in the English meanings (do1, cau1, cau8, cau11, cau13, cau22, cau24, cau31, cau32) opens the shared entry 'Satī, Dakṣa's daughter and Śiva's wife, born again as Pārvatī; — **fixed by hand**
  - E `chalisa.cau1`: The underlined 'Bhavānī' in the English meaning ('Śrī Satī Bhavānī') opens the shared entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas': — **fixed by hand**
  - E `chalisa.cau13`: The work's hard entry for Rāṇājī says he was 'a Rāṇā (a ruler)'. — **fixed**
  - E `chalisa.cau1`: The verse word सती (do1, cau1, cau8, cau11, cau13, cau22, cau24, cau31, cau32) is glossed 'शिवपत्नी सतीजी / पतिव्रता' / 'Sati, Shiva's consort / chaste wife': — **covered**
  - E `chalisa.cau32`: दुहाई in 'श्री राणी सती की फिरी दुहाई' is the proclamation of her name spreading abroad (our meanings: — **fixed**
  - E `chalisa.cau38`: लेनी in 'भक्तन की आपत्ति हर लेनी' is 'she who takes away' (हर लेनी = हर लेनेवाली, parallel to देनी 'देने वाली' in the same line); — **fixed**
  - E `chalisa.cau14`: The underlined 'Vikrama' in the English meaning opens the shared entry whose second sense is 'King Vikrama (Vikramāditya), on whom Śani set his foot, and whose figurines the Viśvakarmā Chālīsā praises': — **fixed**
  - A `chalisa.cau8`: The work's hard entry गुरसामलजीका says 'रानी सतीके' / 'Rānī Satī', against राणी सती / Rāṇī Satī everywhere else in the work (title, verse, meanings, other entries). — **fixed**
  - A `chalisa.cau10`: The work's hard entry जालीरामजीके says 'रानी सतीके' / 'Rānī Satī' against राणी सती / Rāṇī Satī. — **fixed**
  - A `chalisa.cau8`: The work's hard entry डोकवामें says 'रानी सतीका' in Hindi (its English has Rāṇī Satī). — **fixed**
  - A `chalisa.cau9`: The work's hard entry तनधनदासजीको says 'रानी सतीके' in Hindi (its English has Rāṇī Satī). — **fixed**
  - A `chalisa.cau8`: The verse word गुरसामलजी is glossed 'Gursāmal', while our English meaning and hard entries have Gurasāmala. — **fixed**
  - A `chalisa.cau9`: The verse words तनधन and दास are glossed 'Tandhan Dās', while our English meaning and hard entries have Tanadhanadāsa. — **fixed**
  - A `chalisa.cau10`: The verse word जालीराम is glossed 'Jālīrām', while our English meaning and hard entries have Jālīrāma. — **fixed**
  - A `chalisa.cau8`: The verse word डोकवा is glossed 'Dokwa', while our English meaning and hard entries have Ḍokavā. — **fixed**
  - A `chalisa.cau18`: The work's hard entry बाँसल romanises the candrabindu as ṃ ('Bāṃsal'); — **fixed**

## Namu Tero Aarti Majanu Murare (`ravidas-aarti`)
- Witnesses read: Book i-093 (p. 94); Drik Panchang shri-ravidas-aarti.html.
- Verses compared: 5 (every line of text.txt against the witness(es)).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: 96 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 4.
- Result per class: A: one separated 'आप पर' (low). B: text = book except भजनु→मजनु (recorded with SGGS Ang 694); stanza grouping recorded. D: hi/en agree. E: किया (=क्या) glossed 'did' (high); Hari Mānas note; वरतणि root बरतन. F: title/shelf fine (by Guru Ravidas = book heading).
- Findings:
  - E `aarti.pad3`: In तेरो कियो तुझ ही किया अरपउ the second किया is 'क्या' (what): — **fixed**
  - E `aarti.tek`: The underlined 'Hari' in the English meanings (tek, pad4) opens the shared entry 'Hari, a name of Viṣṇu; — **fixed**
  - E `aarti.pad4`: वरतणि (बरताव, 'practice, way of life') gives its root as बरतन, which is the word for a vessel/utensil; — **fixed**
  - A `aarti.pad3`: Hindi meaning writes 'आप पर' apart, against the house style of joined postpositions with pronouns too (style.md §4: — **fixed**

## Shri Ravidas Chalisa (`ravidas-chalisa`)
- Witnesses read: book page images i-089, i-090, i-091, i-092 (pp. 90–93); Drik Panchang `printouts/drikpanchang/shri-ravidas-chalisa.html` (via drik.py); README, reconciliation.md, work.json, text.txt, work glossaries (hi, en, awa).
- Verses compared: 44 of 44 (2 opening dohās, 40 chaupāīs, 2 closing dohās), each line against the book image and Drik.
- Meanings read: 44 hi / 44 en.
- Words read: 432 verse-word entries, 82 underlined meaning-word entries.
- Title / shelf: work.json title and by; library/index.json entry (group गुरु रविदास / Guru Ravidas; desc = first line of do1).
- A: 10 findings: the saint is "Ravidās" in nine work hard entries and the shared hi hard entry, against "Ravidāsa" in all our English meanings and the awa verse-word entry; "Sadnā" against the meanings' "Sadanā"; "Sant" against "Saint".
- B: no finding. The one change (अरु मान) is recorded; the Drik variants are in the kept list; the text equals the book otherwise.
- D: no finding. Hindi and English agree; the cau10 reading is settled in reconciliation.md.
- E: 2 findings: Hari (Mānas note in the en hard entry), दिखाओ (imperative only where the line is past). (The shared ताकी entry, do4, is the same issue already reported under ram-chalisa.)
- F: no finding.
- Findings:
  - E `chalisa.cau1`: The underlined 'Hari' in the English meanings (cau1 'devotees of Hari', cau4, do4) opens the shared entry 'Hari, a name of Viṣṇu; — **fixed**
  - E `chalisa.cau27`: दिखाओ in 'जन्म जनेऊ आप दिखाओ' is past ('you showed', as both meanings say: — **fixed**
  - A `chalisa.cau31`: The work's hard entry सदना spells the name 'Sadnā' (three times) and the saint 'Ravidās', while our English meaning (cau31, cau32), the en hard entry and the awa verse-word entry have 'Sadanā' and 'Ravidāsa'. — **fixed**
  - A `chalisa.cau2`: The work's hard entry कर्मा says 'Sant Ravidās', against 'Saint' in the work's other entries and 'Ravidāsa' in our meanings. — **fixed**
  - A `chalisa.cau3`: The work's hard entry माडुर spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau39`: The work's hard entry योगावतीने spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau2`: The work's hard entry राहूजी spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau2`: The work's en hard entry karmā spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau3`: The work's en hard entry māḍur spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau2`: The work's en hard entry rāhū spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau39`: The work's en hard entry yogāvatī spells the saint 'Ravidās'. — **fixed**
  - A `chalisa.cau1`: The shared hard entry रविदास, opened by every रविदासजी- in our Hindi meanings (do1, cau1, cau11, cau13, cau14, cau16, cau26, cau36, do3), spells the saint 'Ravidās (Raidās)' against 'Ravidāsa' in our English meanings and — **fixed**

## Shri Sai Chalisa (`sai-chalisa`)
- Witnesses read: book page images i-116 … i-132 (all 204 lines, line by line); Drik Panchang `shirdi-sai/sai-chalisa/printouts/drikpanchang/sai-baba-chalisa.html` (diffed word by word against text.txt); reconciliation.md and README read. Chalisa Mala (i-383 … i-391) not opened: the reconciliation calls it a copy of Drik's text, and no reading rests on it alone.
- Verses compared: 102 of 102 (204 lines) against the book and Drik.
- Meanings read: 102 Hindi, 102 English, with every underlined word.
- Words read: every verse word (about 1,900 tokens, about 900 distinct entries).
- Title/shelf: work.json title and by, library/index.json shelf `shirdi-sai` and the entry's desc checked (desc = first line; matches the text).
- A: Hindi meanings write शिरडी (11 times) against the text's and the library's शिर्डी. IAST in English is consistent (Sāī, Bābā, Śirḍī, Kāśīrāma).
- B: text.txt matches the book on every line; the 7 corrections are recorded with sound reasons. A few Drik slips are not listed (low).
- D: meanings match their verses; no clause missing or added found.
- E: 5 wrong underlined entries (काशी, परे→परा, अगर, बन्द, विभूति), 1 weak (प्रकृति); verse-word entries: साई "(?)", लिये, पलक, बढ़ा, धरकर, होता (Sanskrit fallback), जाकर / अयोध्या root, निर्भय.
- F: title, shelf and desc are fine; nothing found.
- Findings:
  - A `meanings (hi), 11 places: cau1, cau7, cau8, cau30, cau35, cau42, cau65, cau69, cau79, cau80, cau91`: The Hindi meanings spell the village शिरडी throughout, while the verse text (every verse except 1), the work's topic heading (शिर्डीमें) and the library's standard spelling (brief: — **fixed by hand**
  - E `chalisa.cau38, chalisa.cau52`: In both meanings काशी / Kāśī is the devotee Kāśīrāma, but the word is underlined and opens the entry for the city of Kāśī (Vārāṇasī, Śiva's city, 'where death brings liberation'): — **fixed by hand**
  - E `chalisa.cau55`: In the Hindi meaning 'भेद-भावसे परे' (beyond) the app underlines परे and opens the entry परा 'परम, सबसे ऊँची' (supreme): — **fixed by hand**
  - E `chalisa.cau76, chalisa.cau102`: अगर ('if') in the Hindi meanings is underlined and opens the shared hard entry 'एक सुगन्धित लकड़ी, अगरु / agarwood': — **fixed by hand**
  - E `chalisa.cau83`: In the Hindi meaning 'सारा खेल बन्द करके' (shut down) the app underlines बन्द and opens the shared hard entry 'वन्दना करते हैं, प्रणाम करते हैं / bows, offers praise' (r वन्दना): — **fixed by hand**
  - E `chalisa.cau98, chalisa.cau99`: विभूति in the Hindi meanings is Bābā's sacred ash (udī), but the underlined entry gives only 'ऐश्वर्य, महिमा, बड़ाई / glory, greatness, splendour', which cannot fit 'विभूति देकर', 'विभूतिमें … शक्ति', 'मस्तक पर धारण'. — **fixed**
  - E `chalisa.cau95`: 'प्रकृतिकी छटा' is the beauty of nature (the garden), but the underlined entry gives Prakṛti as 'जगत्‌का मूल कारण (मूल प्रकृति)', the philosophical primal cause; — **fixed**
  - E `chalisa.cau4, cau30, cau66, cau93 (word साई)`: The verse word साई opens the shared entry whose first sense is 'वही (सोई) — पाठ अस्पष्ट / that very (?)' with r=सोई, g=सर्वनाम: — **fixed**
  - E `chalisa.cau51`: लिये in 'भक्त के लिये' means 'for', but its entry gives only 'लिये (बुलाई = बुला लिये) / (called them) all together', r=लेना, g=भूतकाल: — **covered**
  - E `chalisa.cau41`: पलक in 'किसी पलक में' means 'in some moment' (पलक = पल, the twinkling of an eye), as our meanings take it; — **fixed**
  - E `chalisa.cau57`: बढ़ा in 'प्यार बढ़ा दिन-दिन दूना' is intransitive 'grew' (बढ़ना); — **fixed**
  - E `chalisa.cau20`: धरकर in 'चरणों में धरकर के शीश' is 'placing, laying (the head)'; — **fixed by hand**
  - E `chalisa.cau23`: होता in 'होता है उद्धार' has no awa entry and falls back to the Sanskrit one: — **covered**
  - E `chalisa.cau12`: जाकर ('having gone') opens an entry with r=जो and g=सर्वनाम (for the sense 'जिसका'); — **fixed by hand**
  - E `chalisa.cau3`: अयोध्या (the city) opens an entry whose first sense, root and grammar are for the poet Ayodhyādāsa (r=अयोध्यादास). — **fixed by hand**
  - E `chalisa.cau101`: निर्भय here is the poet's name (reconciliation.md, 'Readings settled': — **fixed**
  - B `reconciliation`: Some differences from Drik Panchang are not recorded in reconciliation.md (all are Drik slips or spacing; — **fixed**

## Aarti Shri Sai Guruvar Ki (`sai-guruvar-aarti`)
- Witnesses read: Book i-133 (p. 134); Aarti Mala i-330; Drik Panchang sai-baba-aarti.html.
- Verses compared: 6 (every line of text.txt against the witness(es)).
- Meanings read: 6 hi / 6 en (whole; no per-line pieces in this work).
- Words read: 118 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 4.
- Result per class: A: two separated postpositions (low); Sāī vs Sāīṁdāsa (low). B: text = book; कर added from Drik (recorded); Aarti Mala claims checked on image. D: hi/en agree. E: shared परमानन्द says 'poet of this āratī'. F: title/shelf fine.
- Findings:
  - E `aarti.tek`: The verse word परमानन्द (परमानन्द सदा सुरवर की, 'ever supreme bliss') opens a shared entry whose first sense is 'परमानन्ददास (परमानन्द स्वामी), इस आरतीके कवि / Paramānanda (Svāmī), the poet of this āratī'. — **fixed**
  - A `aarti.pad2`: Hindi meaning writes 'शरीर पर' apart, against the house style of joined postpositions (style.md §4). — **fixed**
  - A `aarti.pad3`: Hindi meaning writes 'उस पर' apart, against the house style (style.md §4: — **fixed**
  - A `aarti.pad5`: English spells साईं as 'Sāī' everywhere (tek, pad3, pad5, and 169 times across the library) but the poet's name as 'Sāīṁdāsa' (meaning and the work's own en entry): — **fixed**

## Jai Santoshi Mata (`santoshi-aarti`)
- Witnesses read: Book i-239 (p. 240); Aarti Mala i-358; Drik Panchang santoshi-mata-aarti.html and weekdays-shukrawar-aarti.html.
- Verses compared: 12 (every line of text.txt against the witness(es)).
- Meanings read: 12 hi / 12 en (whole; no per-line pieces in this work).
- Words read: 156 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 0.
- Result per class: A: none. B: every recording-driven word (pad3, pad5, pad8–11, tek सेवक) found in the named witness (Drik or Aarti Mala image) word for word; book corrections (संतोषी, चीर, प्रिय) recorded. D: hi/en agree. E: all entries fit. F: fine.
- Findings: none.
- Recording `anuradha-paudwal` (YouTube LCYAyR6EmDI): plays the whole video. Starts heard in 5-s windows: 8 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): aarti.tek. Starts set from the windows: aarti.pad5, aarti.pad11.

## Shri Santoshi Maa Chalisa (`santoshi-chalisa`)
- Witnesses read: book page images i-235 … i-238 (all of it, line by line); Drik Panchang `santoshi/santoshi-chalisa/printouts/drikpanchang/santoshi-mata-chalisa.html` (diffed word by word); README and reconciliation.md read. Audio not checked (class C, the lead's).
- Verses compared: 42 of 42 (2 dohās, 40 chaupāīs).
- Meanings read: 42 Hindi, 42 English, with every underlined word.
- Words read: every verse word (about 330 tokens).
- Title/shelf: work.json title/by, library/index.json shelf `santoshi` and the entry's desc (= the opening dohā's first half-line, as the book has it).
- A: names consistent (संतोषी माँ / Mother Santoṣī, Śāradā, Ṛddhi, Siddhi, Girijā, Bhavānī); nothing found.
- B: text.txt matches the book on every line; the two corrections and every Drik difference are recorded.
- D: meanings match their verses; nothing found.
- E: व्याकुलयारी's entry contradicts the settled reading; shared en entries for Girijā, Bhavānī, māyā carry Mānas notes; मां falls back to Sanskrit 'me'; तरनी lacks its sense here; पाता root (low).
- F: title, by, shelf, desc fine.
- Findings:
  - E `chalisa.cau25 (word व्याकुलयारी)`: The word entry contradicts the reading settled in reconciliation.md and used by both meanings. — **fixed**
  - E `chalisa.cau12, chalisa.cau13, chalisa.cau18 (underlined Girijā, Bhavānī, māyā)`: The English meanings' underlined Girijā, Bhavānī and māyā open shared entries written for the Mānas: — **fixed by hand**
  - E `chalisa.do1, chalisa.cau1 (word मां)`: मां (the book's spelling) has no awa entry and falls back to the Sanskrit one: — **fixed**
  - E `chalisa.cau22 (word तरनी)`: तरनी in 'भव भय तरनी' is 'she who carries (one) across', as both meanings take it ('पार उतारनेवाली', 'carry one across'); — **fixed**
  - E `chalisa.cau23 (word पाता)`: पाता ('obtains') opens an entry whose root and grammar are for 'पत्ते, leaves' (r=पत्ता, g=संज्ञा); — **fixed by hand**
- Recording `bhaktidhaam` (YouTube lCwPg0LRRjk): plays start 1790.55 s, end 2108.6 s. Starts heard in 5-s windows: 25 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): chalisa.cau10, chalisa.cau11, chalisa.cau12. Starts set from the windows: chalisa.cau23, chalisa.cau33.

## Jai Saraswati Mata (`saraswati-aarti`)
- Witnesses read: Drik Panchang saraswati-mata-aarti.html (only witness); book/booklets checked by OCR grep: Aarti Mala i-350 is a different Sarasvatī āratī.
- Verses compared: 7 (every line of text.txt against the witness(es)).
- Meanings read: 7 hi / 7 en (whole; no per-line pieces in this work).
- Words read: 90 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 0.
- Result per class: A: none. B: text = Drik; closing repeat dropped (recorded). D: hi/en agree (Mantharā/Rāvaṇa line read as Sarasvatī's doing; consistent). E: all have a fitting sense. F: fine.
- Findings: none.
- Recording `anuradha-paudwal` (YouTube faxIif-3F8o): plays start 590.73 s, end 1097.0 s. Starts heard in 5-s windows: 7 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): aarti.pad1, aarti.pad2, aarti.pad3, aarti.pad4. Starts set from the windows: aarti.pad5, aarti.tek.

## Shri Saraswati Chalisa (`saraswati-chalisa`)
- Witnesses read: book page images i-191 … i-194 (every line; cau23 फेरेऊ checked on a zoomed crop); Chalisa Mala i-424 (last page: the split राम सागर and cau39); Drik Panchang `saraswati/saraswati-chalisa/printouts/drikpanchang/saraswati-mata-chalisa.html` (diffed word by word: another version, its differences recorded in reconciliation.md); README and reconciliation.md read.
- Verses compared: 43 of 43 (4 dohās, 39 chaupāīs).
- Meanings read: 43 Hindi, 43 English, with every underlined word.
- Words read: every verse word (about 380 tokens).
- Title/shelf: work.json title/by, library/index.json shelf `saraswati` and the entry's desc (= the first dohā's first half, as the text has it).
- A: names consistent in the meanings (Sarasvatī, Vālmīki, Rāmasāgara, Kālidāsa); the shared hi entry सूरदास spells the poet Sūrdās against our Sūradāsa (low).
- B: text.txt matches the book except the 6 recorded corrections; Drik differences recorded. The name split in do4 (राम सागर, as the book and Chalisa Mala print it) leaves सागर glossed 'ocean' (low).
- D: cau29 adds 'whenever trouble comes' (low); the rest matches the verses.
- E: Bhavānī's shared en entry has a Mānas note (cau11, cau39); वधे falls back to the Sanskrit locative.
- F: title, by, shelf, desc fine.
- Findings:
  - E `chalisa.cau11, chalisa.cau39 (underlined Bhavānī)`: The English meanings' underlined Bhavānī opens the shared entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas': — **covered**
  - E `chalisa.cau22 (word वधे)`: वधे ('slew') has no awa entry and falls back to the Sanskrit one, shown with g=सप्तमी, एकवचन ('on the slaying'); — **fixed**
  - D `chalisa.cau29`: Both meanings add a clause the verse does not have: — **not taken: जब जब implies "when (in need)"; the proposed wording is worse**
  - E `chalisa.do4 (word सागर)`: In the last dohā the poet's name is printed split, राम सागर (the book i-194 line 12 and Chalisa Mala i-424 both split it; — **not taken: both printed witnesses split राम सागर in this dohā; kept as printed**
  - A `chalisa.cau9 (underlined सूरदास)`: The Hindi meaning's underlined सूरदास opens a shared entry whose English spells the poet 'Sūrdās' and his work 'Sūrsāgar', while our English meaning (and the en entry sūradāsa) spell him Sūradāsa: — **fixed**

## Shri Sathya Sai Ashtottara Shatanamavali (`sathya-sai-ashtottara`)
- Witnesses read: the owner's base PDF (scriptures-data/hinduism/namavali/sathya-sai/sathya-sai-ashtottara/printouts/bhaktibharat/sathya-sai-108-names.pdf), pages 1–5 rendered and read as images (page 2 also at 250 dpi around names 17–19), plus both text layers (PyMuPDF, pdftotext). The second witness (sathyasai.org *108 Mirrors*) is not in scriptures-data and was not opened; no claim rests on it.
- Verses compared: 109 of 109 (108 names + iti). Every name compared against the base programmatically (spaces ignored) and the spaces checked against the page images: they match except name 18 (finding) and the recorded changes (55, iti, the split conjuncts).
- Meanings read: 109 hi / 109 en.
- Words read: every verse word of every item (about 545 tokens; ॐ, श्री, सायि, नमः are the same in every name) and every underlined word of the meanings (salutation(s), Bābā, dharma, renounce, स्वरूप, युक्त, शिर्डी/Shirdi, भरद्वाज/Bharadvāja, वात्सल्य, अन्तरात्मा, विहार, forlorn, अव्यक्त/unmanifest, Gītā, सिद्धि, कर्म/karma, पुरातन, परे→परा, संकल्प, purifier, साधक, अनुग्रह, तत्त्व, yogīs). No NONE or POSSIBLE entries.
- Title and shelf checked: work.json title/by/parts/sections/types, library/index.json shelf entry (title, by, desc, deity group 'Shri Sathya Sai Baba'), the topic line.
- A: Dvārakāmāyi (en) vs द्वारकामाई (hi) in name 32; the two Shirdi hard entries spell शिरडी/शिर्डी, साईं/साईबाबा and Maharashtra/Mahārāṣṭra differently (low); श्री's English 'Lakshmi' without IAST (low). (सायि → साई not reported, as instructed.)
- B: one unrecorded difference: name 18 printed as one word पर्तिक्षेत्रनिवासिने, our text splits it. Everything else matches the base or is recorded.
- D: meanings match their names, hi and en agree; nothing found.
- E: three underlines misfit: Bābā ('here Sāī Bābā of Shirdi') in 1 and 108; Bharadvāja/भरद्वाज (Mānas entry) in 21; परे opening परा ('supreme') in 84, 85. Verse-word entries all fit.
- F: the 'by' line names Sathya Sai Baba as author of his own names (low; may be the lead's convention).
- Findings:
  - B `nama.n18`: Name 18 is split into two words (पर्ति क्षेत्रनिवासिने); — **fixed by hand**
  - E `nama.n1`: The underlined English word 'Bābā' (names 1 and 108) opens the shared entry that says 'here Sāī Bābā of Shirdi' / 'यहाँ शिरडीके साईं बाबा'. — **fixed by hand**
  - E `nama.n21`: The underlined Bharadvāja in name 21's English meaning opens the Mānas entry ('the great sage of Prayāga, whose hermitage Śrī Rāma visited on his way to the forest'). — **fixed by hand**
  - E `nama.n21`: Hindi side of the same: — **fixed by hand**
  - E `nama.n84`: In the Hindi meanings of names 84 and 85 the word परे ('beyond': — **fixed by hand**
  - A `nama.n32`: English and Hindi spell the mosque differently: — **fixed by hand**
  - A `glossary`: The two hard entries for Shirdi that this work's meanings open spell the place and the saint differently: — **fixed by hand**
  - A `glossary`: The shared word entry for श्री, shown under every one of the 108 names, gives the English 'Lakshmi / glory / honorific', without IAST; — **fixed by hand**
  - F `title`: The work's 'by' (author) line, shown in the library and searched, names Bhagavān Śrī Sathya Sai Baba, the one the names praise, as the author of his own 108 names. — **not taken: by names the deity on these shelves (every āratī and chālīsā: the deity), as the Dhūpa Āratī**
- Recording `ashtotrashat-namavali` (YouTube mLBceWHiVZA): plays the whole video. Starts heard in 5-s windows: 37 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: none.

## Jai Lakshmi Ramana (`satyanarayan-aarti`)
- Witnesses read: Aarti Mala i-329 (base); Drik Panchang shree-satyanarayan-aarti.html; not in the ५१ book (OCR grep).
- Verses compared: 9 (every line of text.txt against the witness(es)).
- Meanings read: 9 hi / 9 en (whole; no per-line pieces in this work).
- Words read: 115 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 1.
- Result per class: A: none. B: text = Aarti Mala image; कहत निरंजन→करत निराजन recorded with Drik. D: hi/en agree. E: प्रभुजी grammar vocative only (low). F: fine (vishnu shelf).
- Findings:
  - E `aarti.pad4`: प्रभुजी in सो फल भोग्यो प्रभुजी फिर स्तुति कीनी is read by our meanings as the object of the praise ('फिर प्रभुकी स्तुति की' / 'then sang the Lord's praise'), but its shared entry gives the grammar only as 'संज्ञा (सम्बो — **fixed**
- Recording `anuradha-paudwal` (YouTube sd31yGqZFlA): plays start 1634.38 s, end 1997.91 s. Starts heard in 5-s windows: 8 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): aarti.tek, aarti.pad2. Starts set from the windows: none.

## Shailputri Maa Bail Asvar (`shailputri-aarti`)
- Witnesses read: Drik Panchang devi-shailputri-aarti.html (only witness).
- Verses compared: 5 (every line of text.txt against the witness(es)).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: 98 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 3.
- Result per class: A: none. B: text = Drik. D: hi/en agree. E: उमा (Mānas note, high), किशोरी (Rādhā/Sītā senses), Bhavānī en (Mānas note). F: fine (durga shelf).
- Findings:
  - E `aarti.pad2`: उमा (verse word in पार्वती तू उमा कहलावे, and underlined in our Hindi meaning 'आप उमा कहलाती हैं') opens the shared entry 'पार्वतीजी, शिवजीकी पत्नी; — **fixed**
  - E `aarti.pad5`: किशोरी in जय गिरराज किशोरी अम्बे (Pārvatī, the mountain king's young daughter; — **fixed**
  - E `aarti.pad1`: The underlined 'Bhavānī' in the English meaning ('You are Bhavānī, beloved of Śiva') opens the shared entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas': — **fixed**

## Hari Om Shri Shakambhar Amba Ji Ki Aarti Kijo (`shakambhari-aarti`)
- Witnesses read: Book i-276 (p. 277); Drik Panchang shakambhari-mata-aarti.html; Aarti Mala i-351 per reconciliation (not used for readings).
- Verses compared: 5 (every line of text.txt against the witness(es)).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: 78 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 3.
- Result per class: A: none. B: text = book; line splits as the book's commas. D: hi/en agree. E: Bhavānī, Māyā, Hari en underlines carry Mānas notes. F: title/part differ (pattern shared with other works), fine.
- Findings:
  - E `aarti.pad1`: The underlined 'Bhavānī' in the English meaning ('the all-complete, primal Bhavānī') opens the shared entry '…to whom Śiva tells the Mānas': — **fixed by hand**
  - E `aarti.pad2`: The underlined 'Māyā' in the English meaning ('You are of auspicious form, and Māyā', a name of the Goddess) opens the shared entry ending 'In the Mānas, Sītā is the Lord's māyā': — **fixed**
  - E `aarti.tek`: The underlined 'Hari' in the English meaning ('Hari Om', the invocation) opens 'Hari, a name of Viṣṇu; — **fixed**

## Shri Shakambhari Chalisa (`shakambhari-chalisa`)
- Witnesses read: book page images i-271 … i-275 (every line, including the repeated line on i-274); Drik Panchang `shakambhari/shakambhari-chalisa/printouts/drikpanchang/shakambhari-mata-chalisa.html` (diffed word by word; every difference is recorded); README and reconciliation.md read.
- Verses compared: 50 of 50 (4 dohās, 46 chaupāīs).
- Meanings read: 50 Hindi, 50 English, with every underlined word.
- Words read: every verse word (about 430 tokens).
- Title/shelf: work.json title/by, library/index.json shelf `shakambhari` and the entry's desc (= the first dohā's first line, as the text has it).
- A: the work's hi glossary has 'Cālīsā' and 'Bhūrā Dev' against Chālīsā / Bhūrā Deva everywhere else.
- B: text.txt matches the book; the two corrections (the doubled line, नें) and every Drik difference are recorded; nothing found.
- D: meanings match their verses (the settled readings of cau4, 10, 27, 28, 43 are followed); nothing found.
- E: प्रसाद (part of the poet's name) glossed only 'grace'; shared ब्रह्म entry says 'here Paraśurāma'; सफल lacks the sense the meaning uses (low); शोक falls back to Sanskrit grammar (low).
- F: title, by, shelf, desc fine.
- Findings:
  - E `chalisa.cau39 (word प्रसाद)`: In 'कान्ता प्रसाद जगाधरी वासी' प्रसाद is the second half of the poet's name Kāntāprasāda (both meanings read it so), but tapped it opens only 'कृपा, प्रसाद / grace, favour'. — **fixed**
  - E `chalisa.cau1, chalisa.cau6 (underlined ब्रह्म)`: The Hindi meanings' ब्रह्म (Brahman) opens the shared hard entry whose second English sense reads 'a brāhmaṇa (here Paraśurāma)': — **fixed**
  - A `glossary (work hi.json: कान्त, भूरा)`: The work's own Hindi-side glossary spells two names differently from the rest of the work: — **fixed by hand**
  - E `chalisa.cau31 (word सफल)`: Both meanings read 'कोढ़ी काया सफल बनाती' as making the leper's body whole (hi 'निरोग बनाती हैं', en 'make a leper's body whole'), but the word's entry gives only 'सफल / फलोंसे भरा' (fruitful / laden with fruit): — **fixed**
  - E `chalisa.cau27, chalisa.cau43 (word शोक)`: शोक has no awa entry and falls back to the Sanskrit one, shown with g=प्रथमा एकवचन (शोकः, संधिमें विसर्गका लोप): — **fixed**

## Shri Shani Chalisa (`shani-chalisa`)
- Witnesses read: book page images i-058 … i-061 (every line); Drik Panchang `shani/shani-chalisa/printouts/drikpanchang/shani-dev-chalisa.html` (diffed word by word; every difference is recorded); the one recording-led reading (cau35 मंगल कारी) checked in Drik Panchang word for word (Drik line: 'स्वर्ण सर्वसुख मंगल कारी'); README and reconciliation.md read. Audio itself not checked (class C, the lead's). Chalisa Mala not opened (a copy of Drik's text, no reading rests on it).
- Verses compared: 43 of 43 (3 dohās, 40 chaupāīs).
- Meanings read: 43 Hindi, 43 English, with every underlined word.
- Words read: every verse word (about 390 tokens).
- Title/shelf: work.json title/by, library/index.json shelf `shani` (beside shanishchar-chalisa, same title, told apart by desc) and the entry's desc (= the first dohā's first line).
- A: names consistent (Śanideva, Chāyānandana, Koṇastha, Sauri, Rāmasundara Prabhudāsa); nothing found.
- B: text.txt matches the book except the recorded corrections; the recording-led word is in Drik Panchang as written; nothing found.
- D: cau37 meaning reads नशि as 'destroying', the word sheet as 'sinews' (low); the rest matches the verses and the settled readings.
- E: en underlined Nala opens the monkey Nala (high); Girijā's shared en entry has a Mānas note; कारी root (low).
- F: title, by, shelf, desc fine.
- Findings:
  - E `chalisa.cau20 (underlined Nala, en)`: In the English meaning Nala is King Nala of Niṣadha (Śani's period over him, the roasted fish), but the underlined Nala opens the shared en entry for the monkey Nala of Rāma's army who built the bridge to Laṅkā: — **fixed by hand**
  - E `chalisa.do1 (underlined Girijā, en)`: The English meaning's underlined Girijā (Gaṇeśa, son of Girijā) opens the shared entry 'Girijā, Pārvatī, daughter of the mountain king, to whom Śiva tells the Mānas': — **covered**
  - D `chalisa.cau37`: The meanings and the word sheet read नशि differently. — **fixed by hand**
  - E `chalisa.cau35 (word कारी)`: कारी in 'मंगल कारी' ('bringing blessing') opens an entry whose root and grammar are for काली 'black' (r=काला, g=विशेषण (स्त्रीलिंग)); — **fixed by hand**
- Recording `bhaktidhaam` (YouTube lCwPg0LRRjk): plays start 2109.07 s, end 2710.08 s. Starts heard in 5-s windows: 16 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): chalisa.cau17. Starts set from the windows: none.

## Jai Jai Jai Shri Shani Dev (`shanidev-aarti`)
- Witnesses read: Book i-057 (p. 58); Drik Panchang shri-shanidev-aarti.html; transcript checked only for the recorded tek change.
- Verses compared: 5 (every line of text.txt against the witness(es)).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: 64 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 5.
- Result per class: A: separated सिर पर / आप पर (low). B: text = book except tek line 2 (सूरज के पुत्र प्रभु, in Drik, recorded). D: en adds 'jewelled' (low). E: छाया (Chāyā) and धार (wearing) have no fitting sense (high); Deva en Upaniṣad note (low). F: fine.
- Findings:
  - E `aarti.tek`: छाया in प्रभु छाया महतारी is Chāyā, Sūrya's wife and Śani's mother (our meanings: — **fixed**
  - E `aarti.pad1`: धार in नीलाम्बर धार नाथ is 'wearing' (धारण करके; — **fixed**
  - D `aarti.pad2`: English adds 'jewelled' to the crown: — **fixed**
  - A `aarti.pad2`: Hindi meaning writes 'सिर पर' and 'आप पर' apart, against the house style of joined postpositions (style.md §4); — **fixed**
  - E `aarti.tek`: The underlined 'Deva' in the English meaning ('Śrī Śani Deva') opens the shared entry 'a god, a shining one; — **fixed**
- Recording `chand-kumar` (YouTube JtJ4P0302FY): plays the whole video. Starts heard in 5-s windows: 4 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: aarti.tek, aarti.pad1, aarti.pad2, aarti.pad3.

## Shri Shani Chalisa (`shanishchar-chalisa`)
- Witnesses read: book page images i-053, i-054, i-055, i-056 (every line); Drik Panchang `shani/shanishchar-chalisa/printouts/drikpanchang/shani-dev-chalisa.html`.
- Verses compared: 43 (do1, so1, cau1–39, do2, do3) against the book; Drik read alongside.
- Meanings read: 43 hi / 43 en, with every underlined word.
- Words read: 448 verse-word entries (no NONE, no POSSIBLE).
- Title / shelf: work.json title and by; library/index.json shelf entry (Shani Dev, desc = opening line) checked against the sibling shani-chalisa.
- A (spelling/names): no error found (शनिश्चर/शनीश्चर vary in the verse as printed; meanings use शनीश्चर / Śanīścara consistently).
- B (text): text matches the book line for line; the two corrections are recorded. 1 low-confidence: the reading of तोर as तीर is not recorded.
- D (meanings): no error found.
- E (words): 4: बार lacks the weekday sense; English hard entry Sarasvatī lacks the river; Vimala and Lalitā entries contradict the closing dohās.
- F (title/shelf): no error found.
- Findings:
  - E `chalisa.cau12`: बार in 'बार शनीचर' (cau12, cau20) means the weekday (वार: — **fixed**
  - E `chalisa.cau17`: The underlined English 'Sarasvatī' opens an entry that gives only the goddess of speech and learning, but here our meaning speaks of the river ('the pure stream of the Sarasvatī'). — **covered**
  - E `chalisa.do2`: The underlined 'Vimala' entry calls Vimala 'the poet of this Chālīsā, who names himself in it', but the dohā says Vimala prepared the pāṭha (कीन्हौं विमल तैयार), as our meaning and README say; — **fixed**
  - E `chalisa.do3`: The work's ललिता entry calls Lalitā 'the poet of this chālīsā' (इस चालीसाके रचयिता कवि); — **fixed**
  - B `chalisa.cau16`: तोर in 'सरयू तोर सहित अनुरागा' is read as तीर ('bank'; — **fixed**

## Jayati Jayati Jag Nivas (`shankar-aarti`)
- Witnesses read: Drik Panchang lord-shankara-aarti.html (only witness).
- Verses compared: 8 (every line of text.txt against the witness(es)).
- Meanings read: 8 hi / 8 en (whole; no per-line pieces in this work).
- Words read: 85 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 3.
- Result per class: A: none. B: text = Drik. D: tek en 'Śiva' for verse/hi 'शंकर'. E: underlined परे matched to परा (wrong word); māyā en Mānas note. F: fine (shiva shelf).
- Findings:
  - D `aarti.tek`: The verse names शंकर; — **fixed**
  - E `aarti.pad5`: In the Hindi meaning ('वे कलाओंसे परे होकर भी…', 'beyond the kalās') the word परे is underlined and opens the entry for परा: — **not taken: the underline of परे is fixed in the app instead (a word with an entry of its own is that word)**
  - E `aarti.pad4`: The underlined 'māyā' in the English meaning ('dispel the delusion of māyā') opens the shared entry ending 'In the Mānas, Sītā is the Lord's māyā': — **fixed**

## Maiya Sharda Tore Darbar Aarti Nit Gaun (`sharda-aarti`)
- Witnesses read: Book i-269, i-270 (pp. 270–271); Drik Panchang sharda-mata-aarti.html.
- Verses compared: 8 (every line of text.txt against the witness(es)).
- Meanings read: 8 hi / 8 en (whole; no per-line pieces in this work).
- Words read: 98 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 0.
- Result per class: A: none. B: text = book's second printing with recorded slips (दीया, सुनाऊँ). D: hi/en agree (subjunctive गाऊँ/I sing noted, not flagged). E: all fit. F: fine.
- Findings: none.

## Shri Sharda Chalisa (`sharda-chalisa`)
- Witnesses read: book page images i-265, i-266, i-267, i-268 (every line); Drik Panchang `sharda/sharda-chalisa/printouts/drikpanchang/sharda-mata-chalisa.html` (compared word by word with a script).
- Verses compared: 43 (do1, cau1–40, do2, do3).
- Meanings read: 43 hi / 43 en, with every underlined word.
- Words read: 394 verse-word entries (no NONE, no POSSIBLE).
- Title / shelf: work.json title and by; library/index.json (Mother Sharda shelf, desc = opening line).
- A (spelling/names): 1 low (Sūrdās vs Sūradāsa in the hi hard entry).
- B (text): text matches the book; Drik differences all recorded. 1: reconciliation cites a doubts file that does not exist.
- D (meanings): 1 low (cau14 मुण्डी reading not recorded).
- E (words): 10: दो, कल्याणा, अभय, चतुर्भुज, अनुमाना, अविद्या (sa fallback), Trikūṭa hi/en (Laṅkā), Bhavānī (Mānas), Māyā (Mānas).
- F (title/shelf): no error found.
- Findings:
  - E `chalisa.cau3`: दो in 'दो सहस्र बर्षहि अनुमाना' is the number two, but the shared entry gives only the imperative 'दीजिये / give'. — **fixed**
  - E `chalisa.cau30`: कल्याणा in 'होई सकल विधि अति कल्याणा' (cau30) and 'शारद मातु करहिं कल्याणा' (cau36) is the noun 'welfare, good'; — **fixed**
  - E `chalisa.cau5`: The underlined त्रिकूट (hi) and Trikūṭa (en) open entries saying it is the mountain on which Laṅkā stands; — **fixed by hand**
  - E `chalisa.cau5`: Same as the English: — **fixed**
  - E `chalisa.cau13`: The underlined English 'Bhavānī' (cau13, cau28) opens an entry that says Bhavānī is Pārvatī 'to whom Śiva tells the Mānas': — **covered**
  - E `chalisa.cau18`: The underlined English 'Māyā' / 'māyā' opens an entry ending 'In the Mānas, Sītā is the Lord's māyā', which misleads in a hymn where Śāradā herself is addressed as the world's Māyā. — **fixed**
  - E `chalisa.do2`: अविद्या falls back to the Sanskrit entry 'अविद्या (प्रेय, अज्ञान) / ignorance (the pleasant)', a gloss made for the Kaṭha Upaniṣad (preyas); — **covered**
  - E `chalisa.cau9`: अभय in 'वीणा पुस्तक अभय धारिणी' is a noun, the gesture (or boon) of fearlessness she holds, as our meanings say; — **covered**
  - E `chalisa.cau2`: चतुर्भुज (cau2, cau6) describes Śāradā's four-armed form, but the shared entry reads 'four-armed (Vishnu form)', which misleads here. — **covered**
  - E `chalisa.cau3`: अनुमाना in 'दो सहस्र बर्षहि अनुमाना' means 'by reckoning, about' (as our meanings: — **fixed**
  - D `chalisa.cau14`: 'रक्त बीज काटा रण मुण्डी' is read as 'wearing her garland of heads she cut down Raktabīja' (work entry मुण्डी = she who wears a garland of heads). — **not taken: the work glossary’s reading (मुण्डी: wearing the garland of heads) kept**
  - A `chalisa.cau15`: The Hindi hard entry सूरदास gives the English 'Sūrdās … the Sūrsāgar', while our English meaning and its own hard entry spell him 'Sūradāsa' (one name, two spellings in the work). — **fixed**
  - B `chalisa.cau7`: reconciliation.md calls शचि 'an open doubt in docs/reviews/sharda-chalisa-doubts.jsonl', but that file does not exist and the same document settles the reading under 'Readings settled'. — **fixed**

## Jai Shitala Mata (`shitala-aarti`)
- Witnesses read: Book i-218, i-219 (pp. 219–220); Drik Panchang shitala-mata-aarti.html.
- Verses compared: 11 (every line of text.txt against the witness(es)).
- Meanings read: 11 hi / 11 en (whole; no per-line pieces in this work).
- Words read: 149 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 3.
- Result per class: A: none. B: text = book; line handling recorded. D: hi/en agree. E: Nārāyaṇa en underline = Viṣṇu not the poet (high); मातु vocative only; बाला entry says 'here Kṛṣṇa' (low). F: fine.
- Findings:
  - E `aarti.pad10`: In दास नारायण कर जोरी the name is the poet's signature (README; — **fixed**
  - E `aarti.pad5`: मातु in भक्तन को सुख देती मातु पिता भ्राता is 'mother' (you are their mother, father and brother; — **fixed**
  - E `aarti.pad9`: बाला (उत्पत्ति बाला बिनाशन) opens a shared entry whose second sense says 'बालक, किशोर (यहाँ श्रीकृष्ण) / the boy, the lad (here Kṛṣṇa)': — **fixed**

## Shri Shitala Chalisa (`shitala-chalisa`)
- Witnesses read: book page images i-214, i-215, i-216, i-217 (every line); Drik Panchang `shitala/shitala-chalisa/printouts/drikpanchang/shitala-mata-chalisa.html` (compared word by word with a script).
- Verses compared: 41 (do1, do2, cau1–39). Every difference from Drik is in reconciliation.md; the book's two slips (त्रलोक्य, मोर मोर) are corrected and recorded.
- Meanings read: 41 hi / 41 en, with every underlined word.
- Words read: 359 verse-word entries (no NONE, no POSSIBLE).
- Title / shelf: work.json title and by; library/index.json (Mother Shitala shelf, desc = opening line).
- A (spelling/names): 4: Śeḍhalā vs Śeṛhalā; Maṃdalā vs Mandalā (meaning, en and hi hard entries).
- B (text): no error found.
- D (meanings): no error found.
- E (words): 6: khara (demon entry for the donkey), लिये, जाहि, औषधि, Bhavānī (Mānas; same shared fix as sharda), वैशाख underlined as the month (low).
- F (title/shelf): no error found.
- Findings:
  - E `chalisa.cau27`: The underlined English 'khara' opens the shared entry for Khara the demon who fought Śrī Rāma with Dūṣaṇa; — **fixed**
  - E `chalisa.cau13`: लिये in 'करमें लिये मार्जनी सूपा' means 'took / holding (in the hand)'; — **covered**
  - E `chalisa.cau28`: जाहि in 'जाहि सकल दुख दूर पराई' is the verb 'go' (जाहिं: — **fixed**
  - E `chalisa.cau29`: औषधि in 'ताकर मंत्र न औषधि कोई' means medicine, remedy; — **fixed**
  - E `chalisa.cau1`: The underlined English 'Bhavānī' (cau1, cau5) opens the shared entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas', which misleads in this Śītalā Chālīsā (the same shared entry flagged in sharda-chalisa; — **covered**
  - A `chalisa.cau25`: शेढ़ला is spelt two ways in English in this work: — **fixed**
  - A `chalisa.cau25`: मंदला is 'Maṃdalā' in our English meaning and hard entries but 'Mandalā' in the verse-word entry; — **fixed**
  - A `chalisa.cau25`: With the meaning's 'Mandalā', the work's English hard entry (key and gloss) and the Hindi hard entry's English must follow. — **fixed**
  - A `chalisa.cau25`: The Hindi hard entry मंदला gives the English 'Maṃdalā'; — **fixed**
  - E `chalisa.cau27`: In the Hindi meaning 'वैशाख-सुनन्दन' (a name of the donkey), the underlined वैशाख opens 'वैशाख मास (अप्रैल–मई)', the month, which misleads; — **fixed**

## Shri Shiv Chalisa (`shiv-chalisa`)
- Witnesses read: book page images i-016, i-017, i-018, i-019 (every line); Drik Panchang `shiva/shiv-chalisa/printouts/drikpanchang/shiva-chalisa.html` (compared word by word with a script). Audio skipped (lead); the reconciliation changes no word for the recording.
- Verses compared: 44 (do1, cau1–41, do2, do3). Every Drik difference is in the reconciliation's list (ॠ/ऋ typing aside); the one correction (कि → की) is recorded.
- Meanings read: 44 hi / 44 en, with every underlined word.
- Words read: 426 verse-word entries (no NONE, no POSSIBLE).
- Title / shelf: work.json title and by; library/index.json (Bhagwan Shiv chalisa shelf, desc = opening line).
- A (spelling/names): 1 low (Śiva Cālīsā vs Chālīsā in a hard entry).
- B (text): no error found.
- D (meanings): no error found.
- E (words): 3: जगदीश as Viṣṇu, Girijā (Mānas clause), तपहिं (locative only).
- F (title/shelf): no error found.
- Findings:
  - E `chalisa.do2`: In the Hindi meaning 'हे जगदीश!' addresses Śiva, but the underlined जगदीश opens 'जगत्‌के स्वामी (भगवान विष्णु)' / 'Lord of the universe (Viṣṇu)', which misleads in the Śiva Chālīsā. — **fixed**
  - E `chalisa.do1`: The underlined English 'Girijā' (do1, cau1) opens the shared entry '… Pārvatī, daughter of the mountain king, to whom Śiva tells the Mānas': — **covered**
  - E `chalisa.cau14`: तपहिं in 'किया तपहिं भागीरथ भारी' is the object of किया (Bhagīratha did great penance), as our meanings read it; — **fixed**
  - A `chalisa.cau41`: The poet's hard entries spell the work two ways in English: — **fixed**
- Recording `bhaktidhaam` (YouTube lCwPg0LRRjk): plays start 0.1 s, end 393.51 s. Starts heard in 5-s windows: 16 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: chalisa.cau13, chalisa.cau33.

## Jai Siddhidatri Maa Tu Siddhi Ki Data (`siddhidatri-aarti`)
- Witnesses read: Drik Panchang devi-siddhidatri-aarti.html (only witness).
- Verses compared: 5 (every line of text.txt against the witness(es)).
- Meanings read: 5 hi / 5 en (whole; no per-line pieces in this work).
- Words read: 136 verse-word entries, plus every underlined word in both meanings; NONE/POSSIBLE: 0.
- Title (work.json hi/en), parts, by, and shelf entry (library/index.json title, desc, deity group) checked against siblings.
- Findings: 1.
- Result per class: A: none. B: text = Drik. D: hi/en agree. E: māyā en Mānas note. F: fine (durga shelf).
- Findings:
  - E `aarti.pad4`: The underlined 'māyā' in the English meaning ('this māyā of yours', the Goddess's own) opens the shared entry ending 'In the Mānas, Sītā is the Lord's māyā': — **fixed**

## Aarti Shri Janak Dulari Ki (`sita-aarti`)
- Witnesses read: Drik Panchang printout `hinduism/aarti/sita/sita-aarti/printouts/drikpanchang/sita-mata-aarti.html` (drik.py); book OCR searched for the āratī (दुलारी etc.): not in the book, as the reconciliation says.
- Verses compared: 4 (tek + 3 stanzas), line by line against Drik; both corrections (दीनोद्धारिणि, शिरोमणि) recorded.
- Meanings read: 4 hi / 4 en.
- Words read: 66 verse words + 6 underlined.
- Title/shelf: work.json and library/index.json (sita group, "माता सीताकी आरती") checked.
- A: no error in text or meanings; one shared word entry without IAST (listed under E).
- B: text matches Drik word for word apart from the two recorded corrections and the standard.
- D: meanings match the verses; hi and en agree.
- E: 1 finding (सीता sa entry English not in IAST).
- F: no finding.
- Findings:
  - E `aarti.pad1`: The shared Sanskrit entry for सीता (the word the app opens for सीता in 'सीता मैया') gives its English without IAST, unlike the house style and the sibling entry राम ('Śrī Rāma'): — **fixed**

## Gao Gao Ri Priyapritam Ki Aarti Gao (`sitaram-aarti`)
- Witnesses read: Drik Panchang `hinduism/aarti/rama/sitaram-aarti/printouts/drikpanchang/shri-sitarama-aarti.html`; book OCR searched (प्रीतम, प्रियाप्रीतम): not in the book.
- Verses compared: 5 (tek + 4 stanzas); matches Drik apart from the recorded सिंगार, दंपति and the standard.
- Meanings read: 5 hi / 5 en.
- Words read: 79 verse words + 12 underlined.
- Title/shelf: work.json, library/index.json (rama group) checked.
- A: no misspelling found.
- B: no unrecorded difference.
- D: meanings match the verses.
- E: 3 findings (underlined रामेश्वर hi and en open the Śiva-liṅga entry; साज lacks the 'finery' sense, low).
- F: 2 findings (shelf desc says Shri Ram only; README points to a doubts file that does not exist and calls the reading unsettled).
- Findings:
  - E `aarti.pad4`: In the Hindi meaning the underlined रामेश्वर (the addressee, the poet of the āratī as reconciliation.md settles it) opens the shared entry for the Śiva-liṅga and holy place Rāmeśvara, which misleads here. — **fixed**
  - E `aarti.pad4`: In the English meaning the underlined 'Rāmeśvara' (the poet addressed) opens the shared en entry for the Śiva liṅga Śrī Rāma set up on the seashore, which misleads here. — **fixed**
  - F `shelf`: The shelf description says the āratī is Śrī Rāma's alone, but it is the āratī of the couple, Sītā and Rāma (प्रियाप्रीतम; — **fixed**
  - F `title`: README.md says the reading of रामेस्वर 'is not settled (docs/reviews/sitaram-aarti-doubts.jsonl)', but that file does not exist and reconciliation.md ('Readings settled') settles it as the poet's name; — **fixed**
  - E `aarti.pad1`: The word साज (shared entry, also underlined in the Hindi meaning 'साज-शृंगार') gives 'सामान, तैयारी / सजना, शोभा देना'; — **fixed**

## Jai Teri Ho Skand Mata (`skandamata-aarti`)
- Witnesses read: Drik Panchang `hinduism/aarti/durga/skandamata-aarti/printouts/drikpanchang/devi-skandamata-aarti.html`; book OCR searched (स्कन्द/स्कंद): no copy of this āratī. DNA Hindi / Boldsky are named only for doubtful readings (not opened; the three corrections they support are clear on the base's own evidence).
- Verses compared: 5 stanzas; matches Drik apart from the three recorded corrections (मैं, कहीं, खण्डा) and the standard.
- Meanings read: 5 hi / 5 en.
- Words read: 104 verse words + 4 underlined.
- Title/shelf: work.json, library/index.json (durga group, desc as its Navadurgā siblings) checked.
- A: no finding.
- B: no unrecorded difference.
- D: meanings match the verses (pad4 reading settled in reconciliation).
- E: 1 finding (जोत grammar given only as क्रिया).
- F: no finding.
- Findings:
  - E `aarti.pad2`: The shared entry for जोत (तेरी जोत जलाता रहूँ मैं: — **fixed**

## Jai Kashyap Nandan (`surya-aarti`)
- Witnesses read: book page image i-332 (Aarti Mala, "सूर्य देव जी की आरती"), Drik Panchang `surya-deva-aarti.html` (drik.py).
- Verses compared: 7 (tek + 6 stanzas), every line against i-332 and Drik; all differences (तिमिर, सुकर्म, करुणा, hyphens, line splits) recorded.
- Meanings read: 7 hi / 7 en.
- Words read: 58 verse words + 11 underlined.
- Title/shelf: work.json, library/index.json (surya group) checked.
- A: 1 low finding (Savitā in the meaning vs Savitṛ in the entries).
- B: no unrecorded difference.
- D: meanings match the verses.
- E: 1 finding (shared en entry 'aditi' runs the Kaṭha sense into the mother-of-gods sense).
- F: no finding.
- Findings:
  - E `aarti.tek`: The underlined 'Aditi' in the English meaning opens a shared entry that runs two different things together as one sense: — **covered**
  - A `aarti.pad3`: The English meaning names the god 'Savitā', while the word entries the app opens for सविता in this very verse (and the underlined सविता of the Hindi meaning) give 'Savitṛ'; — **fixed**

## Shri Surya Chalisa (`surya-chalisa`)
- Witnesses read: book page images i-073, i-074, i-075, i-076 (every line); Drik Panchang `surya/surya-chalisa/printouts/drikpanchang/surya-deva-chalisa.html` (compared word by word with a script).
- Verses compared: 42 (do1, cau1–40, do2). The book's slips (सहस्त्र, छन, बढतु, वांस, रहम, बीज, सुतजग, धन्य-२, मध, the printed numbers) are corrected and recorded; every Drik difference is in the reconciliation (spacing variants aside).
- Meanings read: 42 hi / 42 en, with every underlined word.
- Words read: 391 verse-word entries (no NONE, no POSSIBLE).
- Title / shelf: work.json title and by; library/index.json (Bhagwan Surya chalisa shelf, desc = opening line).
- A (spelling/names): 1 low (suvarṇaretā glossed two ways).
- B (text): no error found.
- D (meanings): no error found.
- E (words): 11: hard entries give another sense than the Sun's name or the month used here: Arka (en), अरुण (hi), हंस (hi, Kaṭha gloss), मधु/madhu (month Caitra missing), हिरण्यगर्भ/हिरण्यगर्भाय/hiraṇyagarbha (Brahmā only), Hari (Mānas clause, low), Tvaṣṭā/Varuṇa/Mitra (low).
- F (title/shelf): no error found.
- Findings:
  - E `chalisa.cau9`: The underlined English 'Arka' (cau9, cau18) opens an entry with only 'the arka plant (madar) / in the Rudram, the sacred fire of a great rite': — **covered**
  - E `chalisa.cau6`: The underlined Hindi अरुण (cau6 'अरुणके समान मनोहर सारथी', cau9 and cau37 where Aruṇa is a name of the Sun) opens a hard entry that says only 'लाल, उगते सूर्य-जैसा / red, ruddy as the dawn'; — **covered**
  - E `chalisa.cau2`: The underlined Hindi हंस (cau2 in the list of the Sun's names, cau25 'कमरमें हंस … रहते हैं') opens 'हंस पक्षी / (कठोपनिषद्‌में) गतिशील आत्मा, सूर्यरूपमें', a Kaṭha Upaniṣad gloss; — **covered**
  - E `chalisa.cau37`: The underlined Hindi मधु opens 'शहद / वसन्त ऋतु / मधु असुर / मीठा', and the English 'Madhu' (if underlined) 'the spring season … / a demon': — **covered**
  - E `chalisa.cau37`: English hard entry 'madhu': — **covered**
  - E `chalisa.cau37`: (English side of the same entry) the English gloss of 'madhu' needs the month too. — **covered**
  - E `chalisa.cau4`: The underlined हिरण्यगर्भ (cau4) and हिरण्यगर्भाय (cau10) open Hindi hard entries saying only 'ब्रह्मा, सृष्टिमें सबसे पहले प्रकट हुए'; — **covered**
  - E `chalisa.cau10`: Same as cau4, for the dative form हिरण्यगर्भाय (Hindi hard entry). — **fixed**
  - E `chalisa.cau4`: English hard entry 'hiraṇyagarbha' (en cau4, cau10): — **fixed**
  - E `chalisa.cau3`: The underlined English 'Hari' opens 'Hari, a name of Viṣṇu; — **fixed**
  - E `chalisa.cau23`: In the armour (cau23) Tvaṣṭā, Varuṇa and Mitra are names of the Sun (the verse-word entry त्वष्टावरुण says 'सूर्यके दो नाम'), but the underlined hard entries give only the craftsman of the gods, the god of the waters, an — **fixed**
  - A `chalisa.cau22`: The English hard entry suvarṇaretā glosses the name two ways: — **fixed**

## Jai Jai Tulsi Mata (`tulsi-aarti`)
- Witnesses read: book page image i-229 (p. 230, "आरती श्री तुलसी जी की"); Drik Panchang readings as listed in reconciliation.md (the book is base).
- Verses compared: 6 (tek + 5 stanzas), every line against i-229; the three corrections (रोगों, बहु, वर्ण) recorded; no other difference.
- Meanings read: 6 hi / 6 en.
- Words read: 104 verse words + 11 underlined.
- Title/shelf: work.json, library/index.json (tulsi group) checked.
- A: 1 finding (shared sa entry तुलसी: Tulsidas / tulsi not in IAST).
- B: no unrecorded difference.
- D: meanings match the verses (pad1 योग reading is in docs/reviews/tulsi-aarti-doubts.jsonl, still listed as open).
- E: 2 findings (श्याम shared entry says 'here Khāṭū Śyāmajī'; 'hari' en entry carries a Mānas note in the same sense, low).
- F: no finding.
- Findings:
  - E `aarti.pad5`: The shared entry for श्याम (श्याम वर्ण कुमारी: — **covered**
  - A `aarti.tek`: The shared Sanskrit entry for तुलसी (the word the app opens for तुलसी माता) spells two of its three senses without IAST, beside 'Tulasī' in the third: — **covered**
  - E `aarti.pad3`: The underlined 'Hari' (pad3 "Hari's", pad5 'Hari') opens a shared English entry that joins a Mānas-only note into the one sense: — **covered**
- Recording `anuradha-paudwal` (YouTube faxIif-3F8o): plays start 2365.12 s, end 2827.16 s. Starts heard in 5-s windows: 6 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: aarti.tek, aarti.pad5.

## Shri Tulsi Chalisa (`tulsi-chalisa`)
- Witnesses: Drik Panchang tulasi-mata-chalisa.html (base; read with drik.py, compared word by word with text.txt); the book has no Tulasī Chālīsā (no page images apply).
- Verses compared: 46 (6 dohās, 40 chaupāīs). Only differences from Drik: the three recorded in reconciliation.md (बिराजिनी, संग्रामा, प्रयाग).
- Meanings read: 46 hi / 46 en (whole), with every underlined word (106).
- Words read: 492 verse words (no NONE, no POSSIBLE).
- Title / shelf: work.json and library/index.json (Tulsi Mata › Shri Tulsi Chalisa, desc = opening half) checked.
- A: 2 findings (cau5 non-honorific उसके; Sukharām/Sukharāma in a hard entry).
- B: no findings (text = Drik Panchang except the 3 recorded corrections).
- D: no separate findings (meanings match verses; settled readings followed).
- E: 14 findings (सुदामा verse + hard entry; द्वन्द्व hard entry; विचारे; सुन्दर as poet's name; तुलसीदास ×3 (awa, hi, en); आशिय "(?)"; राधे vocative; होही person; कन्त grammar; है; en 'tulasī' plant-only entry).
- F: no findings.
- Findings:
  - E `chalisa.cau10`: The verse word सुदामा opens the shared entry for Kṛṣṇa's poor friend Sudāmā; — **fixed by hand**
  - E `chalisa.cau10`: The underlined सुदामा in our Hindi meaning opens the shared hard entry 'श्रीकृष्णके निर्धन ब्राह्मण मित्र / Kṛṣṇa's poor brahmin friend', which is a different Sudāmā; — **fixed by hand**
  - E `chalisa.cau17`: The underlined द्वन्द्व in the Hindi meaning ('घोर द्वन्द्व करते हुए', combat) opens a shared hard entry giving only 'pairs of opposites (joy and sorrow…)', a sense that cannot fit a fight. — **fixed**
  - E `chalisa.cau27`: विचारे in 'दियो श्राप बिना विचारे' (cursed without thinking) has only the shared sense 'विचारकर (रचा) / devised', which does not fit; — **fixed**
  - E `chalisa.cau38`: सुन्दर here is the poet's name (the reconciliation and both meanings: — **fixed by hand**
  - E `chalisa.do6`: तुलसीदास in the last dohā is Sukharāma, 'son/servant of Tulasī', naming himself (our meanings: — **fixed**
  - E `chalisa.do6`: The underlined तुलसीदासने in the Hindi meaning opens the shared hard entry 'गोस्वामी तुलसीदास', but the meaning makes Tulasīdāsa a name of Sukharāma ('तुलसीके पुत्र सुखरामने — तुलसीदासने —'); — **fixed**
  - E `chalisa.do6`: The underlined 'Tulasīdāsa' in the English meaning opens the shared entry 'the poet-saint who wrote the Rāmacaritamānasa', which contradicts the meaning (Tulasīdāsa = Sukharāma, son of Tulasī). — **fixed**
  - E `chalisa.do4`: आशिय opens an entry marked as a guess: — **fixed**
  - E `chalisa.cau11`: राधे is the subject here ('Rādhā could not bear to see'), but its only entry is the vocative 'हे राधा / O Rādhā', g=संबोधन, which misleads. — **fixed**
  - E `chalisa.cau40`: होही 'होही सुख' is said of the men and women who recite (they become happy), but the entry gives 'होता (है) / (you) become', g=मध्यम पुरुष (second person): — **fixed**
  - E `chalisa.cau4`: कन्त ('कन्त मम होहू', be my husband) is not an address here, but the shared entry (folded कंत) has g=संबोधन. — **fixed**
  - E `chalisa.cau3`: है in 'जब प्रसन्न है दर्शन दीन्ह्यो' stands for ह्वै 'having become (pleased)', as both meanings read it ('प्रसन्न होकर', 'well pleased'); — **fixed**
  - A `chalisa.cau5`: Hindi meaning refers to the goddess Tulasī with the non-honorific उसके, while the work elsewhere uses the honorific for her in narration (cau14 'हुईं', cau15 'उनका जन्म', cau16 'उनके पतिका'). — **fixed**
  - A `glossary`: The shared Hindi hard entry सुखराम gives the English 'Sukharām', while our English meaning and en.json spell the poet 'Sukharāma'. — **fixed**
  - E `chalisa.do1`: The underlined 'Tulasī' in the English meanings (used throughout for the goddess: — **covered**

## Jai Vaishnavi Mata (`vaishno-devi-aarti`)
- Witnesses read: book page image i-353 (Aarti Mala, "श्री वैष्णो जी की आरती"), Drik Panchang `vaishno-mata-aarti.html` (drik.py).
- Verses compared: 8 (tek + 7 stanzas), every half-line against i-353 and Drik; all corrections and the two lines taken from Drik (pad6, pad7 lines 3–4) recorded; kept spellings as listed.
- Meanings read: 8 hi / 8 en.
- Words read: 107 verse words + 13 underlined.
- Title/shelf: work.json, library/index.json (vaishno-devi group) checked.
- A: 1 finding (sa गंगा entry 'the Ganga' without IAST).
- B: no unrecorded difference.
- D: meanings match the verses.
- E: no further finding.
- F: no finding.
- Findings:
  - A `aarti.pad1`: The shared entry for गंगा (गंगा बहती चरनन) gives 'the Ganga' without IAST, while the meaning of this verse says 'the Gaṅgā' (style.md §5). — **fixed**

## Shri Vaishno Devi Chalisa (`vaishno-devi-chalisa`)
- Witnesses: the book, page images i-230, i-231, i-232, i-233 (read on the images); Drik Panchang vaishno-mata-chalisa.html (drik.py, word-by-word diff).
- Verses compared: 42 (2 dohās, 40 chaupāīs). Text = book except नमो, शर्मा quotes, पोषण, all recorded; Drik's differences all listed in reconciliation.md.
- Meanings read: 42 hi / 42 en, with every underlined word (99).
- Words read: 373 verse words (no NONE, no POSSIBLE).
- Title / shelf: work.json and library/index.json (Mother Vaishno Devi › Shri Vaishno Devi Chalisa) checked.
- A: 4 findings (Kaul Kandolī / Kaul-Kandaulī, Nagrota / Nagaroṭā, Trikuṭa in a hard entry, Lāṅgur / Lāṅgura).
- B: no findings.
- D: no findings.
- E: 7 findings (त्रिकूट hi + en hard entries give Laṅkā's Trikūṭa; श्रीधर hi + en hard entries give Viṣṇu, not the devotee; भैरों hard entry lacks the yogī; देवियों → vocative देवि; सोने 'सोने ने').
- F: no findings.
- Findings:
  - E `chalisa.do1`: The underlined त्रिकूट in the Hindi meaning ('त्रिकूट पर्वत आपका धाम है', the Jammu hill of Vaiṣṇo Devī) opens the shared hard entry for the Laṅkā Trikūṭa: — **fixed by hand**
  - E `chalisa.do1`: The underlined 'Trikūṭa' in the English meaning ('whose home is Mount Trikūṭa') opens the shared entry 'the three-peaked mountain on which Laṅkā stands', the wrong mountain. — **fixed by hand**
  - E `chalisa.cau18`: The underlined श्रीधरके (cau18) and श्रीधरने (cau34) open the shared hard entry 'लक्ष्मीको धारण करनेवाले (विष्णु) / bearer of Śrī (Viṣṇu)', but here Śrīdhara is the devotee (भक्त श्रीधर) who held the feast; — **fixed by hand**
  - E `chalisa.cau18`: The underlined 'Śrīdhara' in the English meanings (cau18 'her devotee Śrīdhara', cau34 'The devotee Śrīdhara') opens the shared entry "Śrīdhara, 'who holds Śrī (Lakṣmī)': — **fixed**
  - E `chalisa.cau14`: The underlined भैरों in the Hindi meanings of the Bhairoṁ story (cau14 'योगी भैरों', cau20, cau23, cau27, cau29) opens the shared hard entry 'भैरों, भैरव — शिवजीका उग्र रूप', but in this story he is the yogī Bhairoṁ Nāth — **covered**
  - E `chalisa.cau3`: In 'देवियों और देवताओंने' the plain word देवियों (goddesses) is underlined and opens the hard entry देवि: — **fixed**
  - E `chalisa.cau37`: सोने (सोने का छत्र, a golden canopy) opens the shared entry hi 'सोने ने' (an ergative form, 'by gold'), which is wrong Hindi for the word and does not fit. — **fixed**
  - A `chalisa.cau16`: The work's own hard entry कंदौली spells the place 'Kaul Kandolī' in English, while our English meaning and the work's en.json have 'Kaul-Kandaulī'. — **fixed**
  - A `chalisa.cau14`: The work's own hard entry नगरोटा gives the English 'Nagrota', while our English meaning has 'Nagaroṭā' (and the work's en.json 'Nagaroṭā (Nagrota)'); — **fixed**
  - A `chalisa.cau1`: The shared hard entries for वैष्णो spell the hill 'Trikuṭa' (en) in hi.json, a form found nowhere in the work (the English meanings have Trikūṭa, do1, and Trikuṭā, cau7, as the verses do). — **fixed**
  - A `chalisa.cau26`: The attendant hero is 'Lāṅgura' in our English meaning and en.json, but 'Lāṅgur' in the English of the shared Hindi hard entry लांगुर. — **fixed**

## Sun Meri Devi Parvatvasini (`vindhyeshwari-aarti`)
- Witnesses read: book page image i-181 (p. 182), Aarti Mala image i-334, Drik Panchang `vindhyeshwari-mata-aarti.html` (drik.py).
- Verses compared: 5 (tek + 4 stanzas), every half-line against i-181, i-334 and Drik; the bracketed (तेरा) and Drik's missing तेरे recorded.
- Meanings read: 5 hi / 5 en.
- Words read: 70 verse words + 16 underlined.
- Title/shelf: work.json, library/index.json (vindhyeshwari group) checked.
- A: no finding.
- B: no unrecorded difference.
- D: meanings match the verses (pad3 सवाया settled in reconciliation).
- E: 2 findings (sa मध्ये entry '(in the heart)'; मोहन entry repeats the mohanbhog sense).
- F: no finding.
- Findings:
  - E `aarti.pad3`: The shared Sanskrit entry for मध्ये (सत्युग त्रेता द्वापर मध्ये: — **fixed**
  - E `aarti.pad4`: The shared entry for मोहन lists the mohanbhog sense twice (third and fourth senses say the same thing), and its grammar names only two classes for four senses. — **covered**

## Shri Vindhyeshwari Chalisa (`vindhyeshwari-chalisa`)
- Witnesses: the book, page images i-178, i-179, i-180, i-181 (read on the images); Drik Panchang vindhyeshwari-mata-chalisa.html (drik.py, word-by-word diff); Chalisa Mala not reopened (used by the work only as a check; both recorded corrections are also in Drik).
- Verses compared: 39 (1 dohā, 38 chaupāīs). Text = book except चौसट्ठी, मन लाई (recorded); every Drik difference is in the reconciliation's kept list.
- Meanings read: 39 hi / 39 en, with every underlined word (72).
- Words read: 378 verse words (no NONE, no POSSIBLE).
- Title / shelf: work.json and library/index.json (Mother Vindhyeshwari › Shri Vindhyeshwari Chalisa) checked.
- A: 1 finding (Hiṅglāj / Hiṅgalāja).
- B: no findings.
- D: no findings.
- E: 8 findings (मानहुँ 'as if' for the imperative; ज्वाला lacks the name; उमा hard entry with the Mānas note; en Bhavānī with the Mānas note; देवियाँ → vocative देवि; सेवी 'servants' for 'served'; मोचन; सुमिरे tense).
- F: no findings.
- Findings:
  - E `chalisa.cau37`: मानहुँ in 'यह जनि अचरज मानहुँ भाई' is the imperative 'consider, take (it)' (do not take this as a wonder), as both meanings read it; — **fixed**
  - E `chalisa.cau10`: ज्वाला here is a name of the Goddess (Jvālā, in a list उमा माधवी चण्डी ज्वाला; — **fixed**
  - E `chalisa.cau10`: The underlined उमा in the Hindi meaning opens the shared hard entry 'पार्वतीजी, शिवजीकी पत्नी; — **fixed by hand**
  - E `chalisa.cau1`: The underlined 'Bhavānī' in the English meanings (cau1, cau5, cau19, cau33, cau38: — **fixed**
  - E `chalisa.cau15`: The plain word देवियाँ in the Hindi meaning ('आप चौंसठ देवियाँ हैं') is underlined and opens the hard entry देवि: — **fixed**
  - E `chalisa.cau3`: सेवी in 'सन्त असुर सुर सेवी' is said of the Goddess: — **fixed**
  - E `chalisa.cau25`: मोचन in 'निश्चय ऋण मोचन होई जाई' is the noun 'release' (release from debt comes about), as the meanings have it; — **fixed**
  - E `chalisa.cau30`: सुमिरे in 'निश्चय देविहिं सुमिरे सोई' is 'should remember' (optative), as the meanings read it ('स्मरण करे', 'should remember'); — **fixed**
  - A `chalisa.cau11`: The shrine is 'Hiṅgalāja' in our English meaning and en.json, but 'Hiṅglāj' in the English of the shared Hindi hard entry हिंगलाज. — **fixed**

## Shri Vishnu Chalisa (`vishnu-chalisa`)
- Witnesses: the book, page images i-037, i-038, i-039, i-040 (read on the images); Drik Panchang shri-vishnu-chalisa.html (drik.py, word-by-word diff). Audio not checked (class C, the lead's).
- Verses compared: 41 (1 dohā, 40 chaupāīs). Text = book except मत्स्य (recorded) and cau30 निज, the recording's reading, confirmed word for word in Drik Panchang; Drik's other differences (भगवान, भाँति, करहुँ) are recorded.
- Meanings read: 41 hi / 41 en, with every underlined word (58).
- Words read: 381 verse words (no NONE, no POSSIBLE).
- Title / shelf: work.json and library/index.json (Bhagwan Vishnu › Shri Vishnu Chalisa) checked.
- A: no findings.
- B: no findings.
- D: no findings.
- E: no findings (entries fit; settled readings अमिलख, बनाया, हार पार have matching senses).
- F: no findings.
- Findings: none.
- Recording `bhaktidhaam` (YouTube lCwPg0LRRjk): plays start 1149.61 s, end 1478.89 s. Starts heard in 5-s windows: 14 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): chalisa.cau16. Starts set from the windows: none.

## Shri Vishnu Sahasranamam (`vishnu-sahasranama`)
- Witnesses read: the owner's base PDF (scriptures-data/.../printouts/vishnusahasranamam-in/vishnu-sahasranama.pdf), its text layer in full (pdftotext and PyMuPDF), pages 3–23 rendered; page 11 read as an image (stotra 36–46, where the site header hides stotra 41's second line). The owner's second witness (english-transliteration/vishnusahasranama.pdf) checked at stotra 41 and 48. sanskritdocuments.org and the critical edition were not re-opened: the base matches our text except where reconciliation.md records a change, so no reading needed them.
- Verses compared: 203 of 203 items (mangala 7, purva 16, viniyoga/nyāsa/saṅkalpa 5, dhyāna 8, stotra 109, uttara 33, iti 1, upasaṃhāra 11, paryāya 13), by a token diff of the whole base stotra against text.txt (nasals folded): every difference is a recorded change, a recorded heading/speaker-dash removal, or a recorded text-layer split (the 'SPACE' list matches reconciliation.md's list of mended splits).
- Meanings read: 203 hi / 203 en, all, against their verses; the names in brackets in hi and en compared automatically for the stotra.
- Words read: 1,866 verse-word lookups (1,546 distinct entries), scanned for NONE/POSSIBLE/(?) (none), case/ending agreement, other-work senses, and an overlap test of each entry against its verse's English meaning (210 low-overlap cases read by hand; all fit). All 340 distinct underlined words of the meanings read with their entries.
- Title and shelf checked: work.json (title, by, edition, parts, sections, types), library/index.json shelf entry (title, by, edition, desc, deity group), topics.
- A: 'Sattra' (en) for the verse's सत्रं in stotra 48.
- B: no wrong text; one unrecorded fact: stotra 41 line 2 is hidden by the site header on the printed page and comes from the text layer (low).
- D: meanings are accurate and hi/en agree; two low points: 'veiled by ignorance' (Saṃvṛta, 25) wording; the refrain's इति rendered after 107/108 but not after uttara 22–28.
- E: the main problem. The names in brackets in our meanings are underlined and open shared hard entries written for other works: 59 misfits (Gada a monkey of Rāma's army, Guha the Niṣāda chief, Jayanta the crow, Kālanemi Rāvaṇa's rākṣasa, Suṣeṇa the Laṅkā physician, Siddhārtha/Vardhamāna Mahāvīra, Vikrama the era/king, Paramā/परमा an Ekādaśī, पवित्रा an Ekādaśī, धरणीधर 'the poet of this āratī', बभ्रु Śani, पुनर्वसु a nakṣatra, सर्ग a chapter, स्मृति law-books, कपि a monkey, पगोंसे → पगा 'soaked', परे → परा 'supreme' in six verses, Dakṣa, Nahuṣa, Gopati, Arka, Śatrughna, अनन्तरूप Lakṣmaṇa, and others). Each has a proposed work-own glossary entry. Verse-word entries themselves fit.
- F: README still says 'Meanings, word meanings: none yet' (low). Title, by and shelf entry are right.
- Findings:
  - E `stotra.sh81`: The underlined English word 'gada' in our meaning ("the elder brother of Gada (Gadāgraja)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh41`: The underlined English word 'guha' in our meaning ("the one who hides himself by his māyā (Guha)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh85`: The underlined English word 'jayanta' in our meaning ("the victorious (Jayanta)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh69`: The underlined English word 'kālanemi' in our meaning ("the slayer of Kālanemi (Kālaneminihā)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh58`: The underlined English word 'suṣeṇa' in our meaning ("the one with a splendid army (Suṣeṇa)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh27`: The underlined English word 'siddhārtha' in our meaning ("he whose every aim is accomplished (Siddhārtha)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh28`: The underlined English word 'vardhamāna' in our meaning ("who grows as the world (Vardhamāna)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh9`: The underlined English word 'vikrama' in our meaning ("he who strode across the worlds (Vikrama)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh2`: The underlined English word 'paramā' in our meaning ("the highest goal of the liberated (Muktānāṃ Paramā Gatiḥ)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh23`: The underlined English word 'nimiṣa' in our meaning ("he whose eyes are closed in yogic sleep (Nimiṣa)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh34`: The underlined English word 'nahuṣa' in our meaning ("he who binds all by māyā (Nahuṣa)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh45 (also sh98)`: The underlined English word 'dakṣa' in our meaning ("the skilful (Dakṣa)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh85`: The underlined English word 'arka' in our meaning ("the sun (Arka)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh37`: The underlined English word 'aśoka' in our meaning ("the sorrowless (Aśoka)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh53, stotra.sh63`: The underlined English word 'gopati' in our meaning ("the lord of the cows (Gopati)" (53), "the lord of the earth (Gopati)" (63)) opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh26`: The underlined English word 'jahnu' in our meaning ("he who draws all beings into himself at the dissolution (Jahnu)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh18, stotra.sh78`: The underlined English word 'madhu' in our meaning ("sweet as honey (Madhu)" (18), "born in the line of Madhu (Mādhava)" (78)) opens a shared hard entry that does not fit: — **fixed by hand**
  - E `dhyana.dh1, stotra.sh55`: The underlined English word 'mukunda' in our meaning ("may Mukunda purify us", "the giver of liberation (Mukunda)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `viniyoga, stotra.sh107, stotra.sh108`: The underlined English word 'śārṅga' in our meaning ("he whose bow is Śārṅga", "the bow Śārṅga") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh44`: The underlined English word 'śatrughna' in our meaning ("the slayer of the enemies of the gods (Śatrughna)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh32`: The underlined English word 'kāma' in our meaning ("the one who is longed for (Kāma)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh70`: The underlined English word 'kāmadeva' in our meaning ("the god whom all desire (Kāmadeva)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh6`: The underlined English word 'manu' in our meaning ("the thinker (Manu)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh17`: The underlined English word 'niyama' in our meaning ("he who appoints all to their work (Niyama)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh11`: The underlined English word 'siddhi' in our meaning ("fulfilment, the fruit of all (Siddhi)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh91`: The underlined English word 'āśrama' in our meaning ("the resting place of those who wander in the world (Āśrama)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh54, stotra.sh78`: The underlined English word 'soma' in our meaning ("the moon (Soma)" (54); — **fixed by hand**
  - E `stotra.sh36, stotra.sh76`: The underlined English word 'vāsudeva' in our meaning ("the god who dwells in all (Vāsudeva)" (36), "the god who dwells in all and covers all" (76)) opens a shared hard entry that does not fit: — **fixed by hand**
  - E `mangala.sh3, mangala.sh4`: The underlined English word 'vasiṣṭha' in our meaning ("the great-grandson of Vasiṣṭha", "the descendant of Vasiṣṭha" (of Vyāsa)) opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh18, sh44, sh89, sh90, sh97, sh103`: The underlined Hindi word 'परे' in our meaning ("इन्द्रियोंसे परे", "शब्दोंसे परे", "गुणोंसे परे" etc. — **fixed by hand**
  - E `purva.sh16`: The underlined Hindi word 'पवित्र' in our meaning ("पवित्रोंमें भी पवित्र") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh56`: The underlined Hindi word 'पग' in our meaning ("तीन पगोंसे तीनों लोक नापनेवाले (त्रिविक्रम)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh25`: The underlined Hindi word 'धरणीधर' in our meaning ("पृथ्वीको धारण करनेवाले (धरणीधर)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh13`: The underlined Hindi word 'बभ्रु' in our meaning ("लोकोंका भरण करनेवाले (बभ्रु)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh16`: The underlined Hindi word 'पुनर्वसु' in our meaning ("बार-बार शरीरोंमें बसनेवाले (पुनर्वसु)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh17`: The underlined Hindi word 'सर्ग' in our meaning ("सृष्टिरूप (सर्ग)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `uttara.sh12`: The underlined Hindi word 'स्मृति' in our meaning ("आत्मसुख, क्षमा, श्री, धैर्य, स्मृति और कीर्ति" (memory)) opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh96`: The underlined Hindi word 'कपि' in our meaning ("सूर्य (कपि)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh69`: The underlined Hindi word 'कालनेमि' in our meaning ("कालनेमिका वध करनेवाले (कालनेमिनिहा)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh41`: The underlined Hindi word 'गुह' in our meaning ("अपनी मायासे अपनेको छिपानेवाले (गुह)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh85`: The underlined Hindi word 'जयन्त' in our meaning ("विजयी (जयन्त)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh58`: The underlined Hindi word 'सुषेण' in our meaning ("सुन्दर सेनावाले (सुषेण)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh27`: The underlined Hindi word 'सिद्धार्थ' in our meaning ("जिनके सब प्रयोजन सिद्ध हैं (सिद्धार्थ)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh28`: The underlined Hindi word 'वर्धमान' in our meaning ("(जगत्‌रूपसे) बढ़नेवाले (वर्धमान)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh44`: The underlined Hindi word 'शत्रुघ्न' in our meaning ("देवताओंके शत्रुओंका नाश करनेवाले (शत्रुघ्न)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh45, stotra.sh98`: The underlined Hindi word 'दक्ष' in our meaning ("कुशल (दक्ष)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh34`: The underlined Hindi word 'नहुष' in our meaning ("मायासे सबको बाँधनेवाले (नहुष)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh2`: The underlined Hindi word 'परमा' in our meaning ("मुक्त पुरुषोंकी परम गति (मुक्तानां परमा गतिः)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh23`: The underlined Hindi word 'निमिष' in our meaning ("योगनिद्रामें आँखें मूँदे हुए (निमिष)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh100`: The underlined Hindi word 'अनन्तरूप' in our meaning ("अनन्त रूपोंवाले (अनन्तरूप)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh53, stotra.sh63`: The underlined Hindi word 'गोपति' in our meaning ("गौओंके स्वामी (गोपति)", "पृथ्वीके स्वामी (गोपति)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `dhyana.dh1, stotra.sh55`: The underlined Hindi word 'मुकुन्द' in our meaning ("मुकुन्द हमें पवित्र करें", "मोक्ष देनेवाले (मुकुन्द)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `viniyoga, stotra.sh107, stotra.sh108`: The underlined Hindi word 'शार्ङ्ग' in our meaning ("शार्ङ्ग धनुषवाले") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh36`: The underlined Hindi word 'स्कन्द' in our meaning ("अमृतरूपसे बहनेवाले (स्कन्द)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh63, stotra.sh87`: The underlined Hindi word 'कुमुद' in our meaning ("पृथ्वीको आनन्दित करनेवाले (कुमुद)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh54`: The underlined Hindi word 'सोम' in our meaning ("चन्द्रमा (सोम)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh46`: The underlined Hindi word 'कोश' in our meaning ("महान् कोशोंसे ढके (महाकोश)" (the sheaths)) opens a shared hard entry that does not fit: — **fixed by hand**
  - E `stotra.sh6`: The underlined Hindi word 'विश्वकर्मा' in our meaning ("विश्वके रचयिता (विश्वकर्मा)") opens a shared hard entry that does not fit: — **fixed by hand**
  - E `mangala.sh3`: The underlined Hindi word 'वसिष्ठ' in our meaning ("वसिष्ठजीके प्रपौत्र" (of Vyāsa)) opens a shared hard entry that does not fit: — **fixed by hand**
  - A `stotra.sh48`: The English gives the name as 'Sattra'; — **fixed**
  - D `stotra.sh25`: 'the one veiled by ignorance (Saṃvṛta)' reads as if the Lord himself were covered by ignorance. — **fixed**
  - D `uttara.sh22`: The refrain's closing इति (… ॐ नम इति) is rendered after stotra 107 and 108 ('Thus the thousand names are complete', 'Thus the prayer is complete') but not after uttara 22, 24, 25, 27 and 28, whose meanings end 'Om, salu — **not taken: not a concrete fix**
  - B `stotra.sh41`: In the owner's base PDF the second line of stotra 41 (करणं कारणं कर्ता विकर्ता गहनो गुहः) is hidden under the site's sticky header on the printed page; — **fixed by hand**
  - F `README`: README.md says 'Meanings, word meanings: — **fixed**
- Recording `ms-subbulakshmi` (YouTube 0tubv1OKDjg): plays the whole video. Starts heard in 5-s windows: 40 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): none. Starts set from the windows: dhyana.dh7, stotra.sh79, dhyana.dh1, stotra.sh101, stotra.sh108.
- Recording `vande-guru-paramparaam` (YouTube A4D-Zf-HJLI): plays the whole video. Starts heard in 5-s windows: 27 verses (first, last, a sample, every flagged one). Hand starts dropped for MMS's (the windows agree with MMS): stotra.sh46. Starts set from the windows: none.

## Prabhu Shri Vishwakarma Ghar Aavo (`vishwakarma-aarti`)
- Witnesses read: book page image i-088 (p. 89), Drik Panchang `shri-vishwakarma-aarti.html` (drik.py).
- Verses compared: 5 (tek + 4 stanzas), every half-line against i-088 and Drik: word for word as recorded.
- Meanings read: 5 hi / 5 en.
- Words read: 94 verse words + 5 underlined.
- Title/shelf: work.json, library/index.json (vishwakarma group) checked.
- A: no finding.
- B: no unrecorded difference.
- D: meanings match the verses (pad3 करावो, pad4 विजय settled in reconciliation).
- E: 1 finding (की as the verb 'did' in पूजन की / रक्षा की opens only the postposition entry).
- F: no finding.
- Findings:
  - E `aarti.pad3`: In रामचन्द्र ने पूजन की and (pad2) ग्वाल बालों की रक्षा की, the last की is the verb 'did' (past of करना, feminine), but the shared entry the app opens gives only the postposition 'का/की (सम्बन्धसूचक) / of', a sense that  — **fixed**

## Shri Vishwakarma Chalisa (`vishwakarma-chalisa`)
- Witnesses: the book, page images i-084, i-085, i-086, i-087 and the top of i-088 (read on the images); Drik Panchang shri-vishwakarma-chalisa.html (drik.py, word-by-word diff).
- Verses compared: 44 (3 dohās, 40 chaupāīs, 1 chhanda). Text = book except लोह for लोक (cau34, recorded); every Drik difference is in the reconciliation's kept list.
- Meanings read: 44 hi / 44 en, with every underlined word (128).
- Words read: 433 verse words (no NONE, no POSSIBLE).
- Title / shelf: work.json and library/index.json (Bhagwan Vishwakarma › Shri Vishwakarma Chalisa) checked.
- A: no findings.
- B: no findings.
- D: no findings.
- E: 6 findings (नल hard entry = King Nala; परे → परा 'supreme' in cau4/cau40; भुवन as Viśvakarmā's father; सुनि है / गुनि है future; दर्शन lacks 'philosophy'; en Bhavānī Mānas note).
- F: no findings.
- Findings:
  - E `chalisa.cau36`: The underlined नल in the Hindi meaning ('परशुराम, नल और नील', Nala the monkey engineer, Nīla's companion, a disciple in the Tretā age) opens the shared hard entry for King Nala of Niṣadha, Damayantī's husband (under Śani — **fixed by hand**
  - E `chalisa.cau4`: In 'गुणोंसे परे रहनेवाले' (cau4) and 'वर्णनसे परे' (cau40) the plain word परे ('beyond') is underlined and opens the hard entry परा 'परम, सबसे ऊँची / supreme, highest', a sense that cannot fit (the app folds परे to परा). — **fixed by hand**
  - E `chalisa.cau25`: In 'भुवनके पुत्र विश्वकर्माके रूपमें' Bhuvana is a person, Viśvakarmā's father (the English has 'son of Bhuvana'); — **fixed**
  - E `chalisa.cha1`: 'सुनि है' and 'गुनि है' are the future सुनिहै / गुनिहै ('will hear', 'will ponder'), as both meanings read them; — **fixed**
  - E `chalisa.cau10`: दर्शन in 'दर्शन शास्त्र' is philosophy (both meanings: — **fixed**
  - E `chalisa.cau3`: The underlined 'Bhavānī' in the English meaning opens the shared entry 'Bhavānī, Pārvatī, Śiva's wife, to whom Śiva tells the Mānas'; — **fixed**

## Aarti Shri Vrishbhanu Lali Ki (`vrishbhanu-lali-aarti`)
- Witnesses read: Drik Panchang `devi-radhika-aarti.html` (drik.py); book OCR searched (वृषभानु): the book has other Rādhā texts (the Chālīsā and the वृषभानुसुता āratī) but not this one.
- Verses compared: 5 (tek + 4 stanzas), every line against Drik: identical apart from the standard.
- Meanings read: 5 hi / 5 en.
- Words read: 54 verse words + 25 underlined.
- Title/shelf: work.json (आरति as Drik prints it), library/index.json (radha group) checked.
- A: no finding.
- B: no unrecorded difference.
- D: meanings match the verses.
- E: 1 finding (underlined राजेश्वरी opens a Lalitā-only entry).
- F: no finding.
- Findings:
  - E `aarti.pad4`: The underlined राजेश्वरी in the Hindi meaning of this Rādhā āratī opens a shared entry that names the goddess Lalitā as its one sense: — **fixed**

## Aarti Shri Vrishbhanu Suta Ki (`vrishbhanu-suta-aarti`)
- Witnesses read: book page image i-224 (p. 225, "आरती श्री राधा जी की"), Drik Panchang `shri-radha-aarti.html` (drik.py).
- Verses compared: 5 (tek + 4 stanzas), every half-line against i-224 and Drik: word for word the same.
- Meanings read: 5 hi / 5 en.
- Words read: 76 verse words + 17 underlined.
- Title/shelf: work.json, library/index.json (radha group) checked.
- A: no finding.
- B: no unrecorded difference.
- D: 1 low finding (विभुता: Hindi 'प्रभुता' vs English 'all-pervading lordship').
- E: no new finding (the मोहन entry's repeated mohanbhog sense is reported under vindhyeshwari-aarti).
- F: no finding.
- Findings:
  - D `aarti.pad4`: विभुता is rendered differently in the two meanings: — **fixed**

## Om Jai Yamuna Mata (`yamuna-aarti`)
- Witnesses read: Drik Panchang `yamuna-mata-aarti.html` (drik.py); book OCR searched (यमुना): the book has no copy of this āratī.
- Verses compared: 6 (tek + 5 stanzas), every half-line against Drik: identical apart from the recorded मंगल and the standard.
- Meanings read: 6 hi / 6 en.
- Words read: 108 verse words + 16 underlined.
- Title/shelf: work.json, library/index.json (yamuna group) checked.
- A: no finding.
- B: no unrecorded difference.
- D: meanings match the verses (tek and pad5 readings settled in reconciliation).
- E: 1 finding (रही as 'remained' opens only the progressive-auxiliary sense). The underlined 'Hari' Mānas note is reported under tulsi-aarti.
- F: no finding.
- Findings:
  - E `aarti.pad3`: In महिमा तुम्हारी अटल रही ('your glory has remained unshaken') रही is the main verb 'remained' (रहना), but the shared entry gives only the progressive auxiliary sense 'is (doing): — **fixed**

## Aarti Karat Yasoda Pramudit (`yashoda-lala-aarti`)
- Witnesses read: Drik Panchang `shri-yashodalala-aarti.html` (drik.py); book OCR searched (यसोदा/यशोदा): the book has no copy of this pada.
- Verses compared: 4 stanzas, every line against Drik: identical apart from the recorded rejoining of सुर-नर-मुनि and the standard.
- Meanings read: 4 hi / 4 en.
- Words read: 78 verse words + 17 underlined (incl. the work-own कृष्णदास entries).
- Title/shelf: work.json, library/index.json (krishna group) checked.
- A: no finding.
- B: no unrecorded difference.
- D: meanings match the verses (pad3 and pad4 readings settled in reconciliation).
- E: no finding.
- F: no finding.
- Findings: none.

## Aarti Jugal Kishor Ki Kijai (`yugal-kishor-aarti`)
- Witnesses read: book page image i-046 (p. 47, "आरती श्री गोपाल जी की"), Drik Panchang `shri-gopala-aarti.html` (drik.py); the Budhwar recension (Drik weekdays page, Aarti Mala i-356) is listed in the reconciliation only as another recension and is not used for the text.
- Verses compared: 9 (tek + 8 stanzas), every half-line against i-046 and Drik: identical apart from Drik's स्वरुप slip (recorded) and the standard.
- Meanings read: 9 hi / 9 en.
- Words read: 99 verse words + 22 underlined.
- Title/shelf: work.json, library/index.json (krishna group) checked.
- A: 1 finding (underlined युगलकिशोरकी entry: 'Yugal Kiśor' half-IAST).
- B: no unrecorded difference.
- D: meanings match the verses (tek, pad6, pad8 readings settled in reconciliation).
- E: 1 finding (shared परमानन्द entry says 'the poet of this āratī', false in the four other works that use the word). श्याम ('here Khāṭū Śyāmajī') and the 'hari' Mānas note recur here; reported under tulsi-aarti.
- F: no finding.
- Findings:
  - E `aarti.pad8`: The shared entry for परमानन्द says 'इस आरतीके कवि' / 'the poet of this āratī' in its first sense. — **covered**
  - A `aarti.tek`: The underlined युगलकिशोरकी (Hindi meaning) opens an entry whose English spells the name half-IAST 'Yugal Kiśor'; — **fixed**

