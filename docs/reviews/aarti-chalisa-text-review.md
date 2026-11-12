# Text review of the Āratī and Chālīsā shelves: every change from the base

Every āratī (98) and chālīsā (54) was read again for one kind of error: a word changed from the base (the Randhir Prakashan book, or Drik Panchang or another booklet where the book lacks the work) on too little evidence, as the Tulasī āratī's बटु पुत्री was once changed to बहु पुत्री on Drik Panchang alone. The rules: `docs/PLAYBOOK.md` §2 (witnesses; sites that copy one another are one witness; Gita Press, Bhāratkosh and sanskritdocuments.org first) and §3 (an āratī follows the version sung in its chosen recording; a corruption corrected on independent witnesses stays corrected where a recording sings it).

**How each work was read.** Every row of its `reconciliation.md` that changes a word; then `text.txt` word by word against Drik Panchang's page and against the OCR of the base pages (a finding aid), every difference the file does not record read on the page image. **What the recording sings** at each difference: the transcript, the 5-s windows of `tools/audio/windows.py` (Whisper small, one window a second), and a scoring of the competing readings on the same stretch of audio (Whisper small, teacher-forced: the log-probability of each whole reading; the higher is the one heard; a margin under about 2 is no evidence). **Verdicts:** āratī: keep, revert to the base, or follow the recording; chālīsā: keep or revert (the recording is evidence, never alone).

Each work: the base and witnesses read; every difference checked, with what the recording sings, the witnesses and the verdict; then the other direction (the recording against our text where we follow the base). Lines left for the owner to hear are collected at the end.

## Āratīs

### Jai Ahoi Mata (`ahoi-aarti`)
- Base: Aarti Mala, page image i-335 (the Randhir book's āratī on i-189/190 is the Lakṣmī āratī). Witnesses: Drik Panchang (= Bhakti Bharat); India TV's text (indiatvnews.com, Ahoi Ashtami 2017); a 2019 blog copy (ambertheme.blogspot.com). No recording.
- हरि विष्णु धाता → हर विष्णु विधाता (refrain): Drik Panchang and India TV, independently; the base names Viṣṇu twice and its half is a mātrā short. **Keep.**
- जग दाता → जग माता (st. 1): Drik Panchang, India TV, and the Lakṣmī āratī whose line this is (Randhir p. 191: जग माता). **Keep.**
- रूद्राणी → रुद्राणी, मे → में, नही → नहीं (st. 4–6): spelling slips (the base's own spelling elsewhere, Drik Panchang). **Keep.**
- Unrecorded differences: none (the OCR's differences are misreadings, checked on the image).

### Jai Ambe Gauri (`ambe-aarti`)
- Base: the Randhir book, i-176, i-177. Witnesses: Drik Panchang; Aarti Mala i-336. Recording: Anuradha Paudwal (sd31yGqZFlA, 900–1350 s).
- रक्तपुष्प की माला → रक्तपुष्प गल माला (st. 2): she sings गल माला (scored at 1008–1020 s: −22.3 against −33.5); Drik Panchang's words, Aarti Mala गलमाला. **Follow the recording (as now).**
- राजत सम ज्योति → सम राजत ज्योति (st. 4): she sings सम राजत (1075–1087 s: −28.0 against −39.6); Drik Panchang's order. **Follow the recording (as now).**
- अम्बे की आरती → श्री अम्बेजी की आरती (st. 12): the 5-s windows from 1293 to 1296 s hear “श्रीयम भेची किया”, “वश्री आमबेची की आज़े ती”, “बेजी की आरती”: श्री अम्बेजी की आरती, as Drik Panchang. **Follow the recording (as now);** `reconciliation.md` no longer leaves जी to the owner's ear.
- The other way: at every word where Drik Panchang differs and we keep the book (दोऊ, निशदिन, चौंसठ योगिनी गावत without मंगल, भैरू, गावे, पावे), the scoring favours the book's words or cannot tell them apart. Nothing to change.

### Barambar Pranam Maiya Barambar Pranam (`annapurna-aarti`)
- Base: the Randhir book, i-244. Witnesses: Drik Panchang; Aarti Mala i-337. No recording.
- No word changed from the book (the rows are the standard: lines, commas). Unrecorded differences: none. **Nothing to change.**

### Jai Ho Gangaram Baba (`baba-gangaram-aarti`)
- Base: the Randhir book, i-170, i-171. Witness: Drik Panchang (no word differs). No recording.
- No word changed; म्हानै नही (st. 6) is the book's own spelling (read on i-171). **Nothing to change.**

### Pavan Mand Sugandh / Badrinath (`badrinath-aarti`)
- Base: Drik Panchang (the book lacks it). No recording.
- मेधवर्ण → मेघवर्ण (st. 1): ध for घ, one stroke; मेध ("sacrifice") gives the line no sense, मेघवर्ण ("cloud-coloured") is Viṣṇu's standing epithet. Clearly a typing slip. **Keep.**

### Jai Jai Shri Bagalamukhi / Bagalamukhi (`bagalamukhi-aarti`)
- Base: the Randhir book, i-254. Witness: Drik Panchang (no word differs). No recording.
- No word changed. (The OCR's अस्तुति करहिं देव नर-नारी is the Chālīsā's line on i-250, not this āratī's.) **Nothing to change.**

### Balaji (`balaji-aarti`)
- Base: the Randhir book. Witnesses: Drik Panchang; Aarti Mala. No recording.
- सुग्रीव, लंक (st. 3, 4): letters lost in a damaged print, filled as Drik Panchang and Aarti Mala (independent) read. **Keep.**

### Banke Bihari (`banke-bihari-aarti`)
- Base: Drik Panchang. No recording. कुन्ज → कुञ्ज is the writing standard (the class nasal), not a change of word. **Nothing to change.**

### Jai Bhairav Deva / Batuk Bhairav (`batuk-bhairav-aarti`)
- Base: the Randhir book. Witnesses: Drik Panchang (agrees throughout); Aarti Mala (another version, not followed). No recording. No word changed. **Nothing to change.**

### Jai Jai Bhagirath Nandini (`bhagirath-nandini-aarti`)
- Base: Drik Panchang. No recording. The only change moves सोभित to the start of st. 3's second line (the rhyme पूजोपहार · धार · भार and the sense); no word changed; न् → ं is the writing standard. **Keep.**

### Suno Ji Bhairav Ladile (`bhairav-aarti`)
- Base: the Randhir book. Witness: Drik Panchang (छुता for the book's छूता, kept). No recording. No word changed. **Nothing to change.**

### Pitu Matu Sahayak Swami Sakha (`brahma-aarti`)
- Base: the Randhir book, i-052. Witness: Drik Panchang (a copy of the same collection). Independent: Mukesh's recording (1950), as transcribed on Atul's Song A Day (atulsongaday.me, 2013). No recording of our own.
- दुःख निर्गुण नाशन हारे → दुःख दुर्गुण नाशन हारे (st. 2): the book and its copy agree, but निर्गुण splits the compound दुःख … नाशन हारे ("destroyer of sorrow") with an epithet that cannot stand there, so the line is broken in sense; Mukesh's independent singing has दुर्गुण, the pair "sorrow and vice". Two grounds, neither "makes more sense" alone. **Keep.**

### Brahmacharini (`brahmacharini-aarti`)
- Base: Drik Panchang. No recording.
- रद्रक्षा → रुद्राक्ष (st. 4): रद्रक्षा is no word; the rosary of the next line. **Keep.**

### Om Jai Brihaspati Deva (`brihaspati-aarti`)
- Base: Aarti Mala, i-357 (an indif.com printout, a near relative of Drik Panchang). Witness: Drik Panchang. No recording.
- फल मेवा → कदली फल मेवा (refrain): the closing quarter is two syllables short of every other closing quarter (metre); Drik Panchang supplies कदली. **Keep.**
- भव बन्धन हार → भव बन्धन हारी (st. 4): the closing quarters have ten mātrās and rhyme in -ī (हितकारी · हारी); हार leaves both a mātrā and the rhyme short. The base is a printout of the same typed collection as Drik Panchang, which keeps the full form. Metre and rhyme, with the witness. **Keep.**

### Jai Maa Chandraghanta Sukh Dham (`chandraghanta-aarti`)
- Base: Drik Panchang. No recording.
- चन्द्र समाज → चन्द्र समान (st. 1): समाज gives the line no sense ("cool like the moon"); one letter; Patrika (patrika.com) prints समान, independent of Drik Panchang. **Keep.**

### Om Jai Chitragupta Hare (`chitragupta-aarti`)
- Base: Drik Panchang. No recording. Only line breaks moved (st. 2, 4), no word changed. **Nothing to change.**

### Jai Dhanvantari Deva (`dhanvantari-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Ambe Tu Hai Jagdambe Kali (`durga-aarti`)
- Base: the Randhir book. Witnesses: Drik Panchang; Aarti Mala. Recording: Anuradha Paudwal (OQ5K_GILwzQ). Every change follows the recording, each in a written witness's words; each was scored on the audio:
  - st. 1 तेरे भक्त जनों पर माता । भीर पड़ी (Drik Panchang's order): −29.3 against −40.6 for the book's order (70–82 s); she sings पे for पर, which no witness writes. **Follow the recording (as now).**
  - st. 1 है अष्ट भुजाओं वाली: the windows from 89 to 92 s hear “से भी बलशाली है दस्पुचा(वाली)”: है is sung (Drik Panchang, Aarti Mala). **Follow the recording.**
  - st. 1 and 2 दुखियों के दुखड़े निवारती: −23.9 against −44.8 for दुःख को (94–106 s), the same in st. 2. **Follow the recording.**
  - st. 2 मां बेटे का है इस जग में: −26.9 against −35.7 (131–143 s). **Follow the recording.**
  - st. 3 हम तो मांगे माँ तेरे मन में (Aarti Mala): −30.2 against −47.3 for the book's मांगते तेरे मन का, −60.2 for Drik Panchang's (229–241 s). **Follow the recording.**
- The other way: एक छोटा सा कोना (the book; Drik Panchang lacks एक) scores −20.0 against −21.1 with the extra word: एक is sung; the book stands. She sings सौ सौ सिंहों से **भी** बलशाली (89–90 s: “से भी बलशा…”, “से भी बलशाली है”): no witness writes भी, so the text keeps the book's words (§3: each word as a written witness has it). उतारें / उतारे, सुने हैं / है: one sound; the book stands.

### Om Jai Ekadashi (`ekadashi-aarti`)
- Base: Drik Panchang (the only witness). No recording. Four line breaks moved to the names that end the long lines (मोहिनी, पवित्रा, विनती, पद्मिनी: the rhyme and the metre), no word changed; आश्चिन → आश्विन (st. 10): no word, the month Āśvina. **Keep.**

### Gajvadan Vinayak (`gajvadan-vinayak-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Jai Ganesh Jai Ganesh Jai Ganesh Deva (`ganesh-aarti`)
- Base for the words: the version Anuradha Paudwal sings (oWo6hMlex5M), written as Drik Panchang writes it; the book (i-010) has an older wording in another order. Every line she sings was scored: माथे पर तिलक सोहे −22.9 against −43.7 (माथे पर सिन्दूर) and −64.5 (the book's मस्तक सिन्दूर) at 166–179 s; सफल कीजे सेवा −32.3 against −36.2 (सुफल) at 296–309 s; her order and words throughout. Stanza 4 (दीनन की लाज), which she does not sing, keeps the book's words and place, untimed. **Follow the recording (as now).**

### Ganpati Seva (`ganpati-seva-aarti`)
- Base: Drik Panchang. No recording. One line break moved (st. 8: the short rhyming lines), no word changed. **Keep.**

### Gau Mata (`gau-mata-aarti`)
- Base: Aarti Mala, i-342. Witness: Drik Panchang. No recording. दारिद्रय → दारिद्र्य (st. 3): no word without the halant. The OCR's other differences are misreadings (read on the image). **Keep.**

### Jayati Jai Gayatri Mata (`gayatri-aarti`)
- Base: the Randhir book, p. 201 (i-200). Witnesses: Drik Panchang (= Bhakti Bharat, InstaAstro); Bhāratkosh's Bharat Discovery (bharatdiscovery.org, "गायत्री माता की आरती"). No recording.
- जग गङ्गा गीता → जय गङ्गा गीता (st. 4): जग गङ्गा could be read "the Gaṅgā of the world", so the sense alone does not settle it; but Bhāratkosh (editorial standing) and Drik Panchang, independent of each other, both read जय, as st. 6 hails जय सतरूपा. **Keep.**
- दारिद्रय → दारिद्र्य, प्राणयिनी → प्रणयिनी, सहस्त्रार → सहस्रार, चलाओं → चलाओ: non-words and a stray anusvāra. **Keep.**

### Jai Govind Dayanidhi / Giridhari (`giridhari-aarti`)
- Base: Drik Panchang. No recording. न् before a consonant → ं or the class nasal (वंशीधर, मङ्गल, संहारी, संरक्षक, मञ्झारी, कंस): the writing standard, no word changed; one line break moved (st. 7: 12 + 10 mātrās). **Keep.**

### Om Jai Jai Jai Giriraj (`giriraj-aarti`)
- Base: the Randhir book, pp. 139–140 (i-138, i-139). Witness: Drik Panchang. No recording. No word changed; the OCR's राखो, तुम्हरों, तुम्हारा are misreadings (the image: राखौ, तुम्हरौं, तुम्हारौ). **Nothing to change.**

### Gita Aarti (`gita-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Jai Gorakh Deva (`gorakhnath-aarti`)
- Base: the Randhir book, pp. 99–100. Witness: Drik Panchang. No recording. No word changed (the OCR's differences are misreadings). **Nothing to change.**

### Govardhan (`govardhan-aarti`)
- Base: Drik Panchang. Recording: Supertone Digital (FXhcAncuBXk). No word changed; at every word where the scoring could compare, it favours our text. **Nothing to change.**

### Aarti Kijai Hanuman Lala Ki (`hanuman-aarti`, the Sundarakāṇḍa's āratī)
- Base: the Sundarakāṇḍa work's āratī (`tools/works/sundarkand/reconciliation.md`): Bhakti Bharat and Bhāratkosh. Recording: Pt. Ashwin Kumar Pathak (QjSpUgnEPLU, from 6062 s).
- **The other way:** st. 5, line 1 सुर नर मुनि जन आरती उतारें: he sings सुर नर मुनि आरती उतारें, without जन. The 5-s windows at 6138 s hear “सुरनरम नियारती उनारे”, at 6140 s “यारती वुदारे”; the scoring gives −80.1 without जन against −90.8 with it (6141–6153 s) and −115.1 against −124.6 (6124–6140 s). Drik Panchang writes the line without जन, and the caupāī metre agrees: सुर नर मुनि आरती उतारें is 16 mātrās, like every other line (जय जय जय हनुमान उचारें 16); with जन it is 18. **Follow the recording: drop जन** (in the Sundarakāṇḍa's text, from which this work is taken).
- The rest: बीड़ा / बीरा, सँवारे / सवारे, बाईं / बाएं are sung alike (the scoring cannot tell them apart); the text keeps them as settled.

### Har Har Har Mahadev (`har-har-mahadev-aarti`)
- Base: Drik Panchang (the only witness). No recording. Only the refrain's division and punctuation, no word changed. **Nothing to change.**

### Om Jai Jagdish Hare (`jagdish-aarti`)
- Base: the text the owner pasted. Recording: Mahendra Kapoor (XOHdvjVkBdE). स्वमी → स्वामी (st. 7): a typing slip; the source's bracketed variant (कष्ट) not taken. Everywhere the scoring could compare, it favours our text. **Keep.**

### Jagjanani Jai Jai (`jagjanani-aarti`)
- Base: Drik Panchang. Recording: Anuradha Paudwal (faxIif-3F8o, 1100–1853 s). सरुपा → सरूपा (st. 8): no word with the short u; ु and ू are sung alike (the scoring cannot tell them apart). Every other word as the base. **Keep.**

### Jaharveer (`jaharveer-aarti`)
- Base: the Randhir book, pp. 105–106. Witness: Drik Panchang. No recording. No word changed (the OCR's नोमी is a misreading of नौमी). **Nothing to change.**

### Jai Shani Deva (`jai-shani-deva-aarti`)
- Base: Drik Panchang. No recording. करू → करूं (st. 3): the verb needs its nasal, as its partner चढ़ाऊं has it. **Keep.**

### Janaki (`janaki-aarti`)
- Base: Drik Panchang. No recording. सुमन्गल → सुमंगल (the standard); वन्धन → बन्धन (st. 2): no word, the व/ब slip. **Keep.**

### Janakinath (`janakinath-aarti`), Kailashvasi (`kailashvasi-aarti`), Kalaratri (`kalaratri-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Katyayani (`katyayani-aarti`)
- Base: Drik Panchang. No recording. छुडाने → छुड़ाने (st. 4): a dropped nukta; DNA Hindi has छुड़ाने. **Keep.**

### Om Jai Shri Shyam Hare (`khatu-shyam-aarti`)
- Base: the Randhir book, p. 156. Witness: Drik Panchang (another version, not followed). No recording. वान्छित → वांछित: the standard. No word changed (the OCR's differences are misreadings). **Nothing to change.**

### Krishna Kanhaiya (`krishna-kanhaiya-aarti`)
- Base: Drik Panchang. No recording. सरक → सरद (st. 2): no word; the autumn moon (सरद ससि) of the image. कन्स → कंस: the standard. **Keep.**

### Om Jai Yaksh Kuber Hare (`kuber-aarti`), Kushmanda (`kushmanda-aarti`)
- Base: Drik Panchang. No recording. Only line divisions, no word changed. **Nothing to change.**

### Aarti Kunj Bihari Ki (`kunj-bihari-aarti`)
- Base: Drik Panchang. Recording: Kumar Vishu (rI-DXgiHALU, 1542–1819 s). No word changed; wherever the scoring could compare, it favours our text. **Nothing to change.**

### Om Jai Lakshmi Mata (`lakshmi-aarti`)
- Base for the words: the version Anuradha Paudwal sings (sd31yGqZFlA, 1998–2330 s), from Drik Panchang and Aarti Mala, with the book's words where she sings them (हर विष्णु विधाता; नर गाता). Every row of `reconciliation.md` follows her singing in a written witness's words.
- st. 4 जिस घर तुम रहती तहँ (Aarti Mala) against Drik Panchang's जिस घर में तुम रहतीं: the scoring cannot separate them (−38.2 against −37.3), but the 5-s windows from 2158 to 2160 s hear “जिस गर तुम रहेती तां सब …”: no में, and तहँ. **Follow the recording (as now).**
- The other way: nothing else; every other comparison favours our text. **Nothing to change.**

### Om Jai Lakshmi Ramana (`lakshmi-narayan-aarti`)
- Base: Drik Panchang. No recording. अदभुत → अद्भुत, सन्तित → सन्तति (st. 5: the list धन जन सुख सन्तति), मन्गल → मङ्गल: a dropped virāma, a non-word, the standard. **Keep.**

### Lalita (`lalita-aarti`)
- Base: the Randhir book, p. 282. Witness: Drik Panchang. No recording. No word changed (the OCR's मातेश्वी, सुन्दी are misreadings). **Nothing to change.**

### Mahagauri (`mahagauri-aarti`)
- Base: Drik Panchang. No recording.
- वहा निवास → वहाँ निवासा (st. 1): वहा is वहाँ without its candrabindu; निवास breaks the rhyme with पासा that every couplet keeps; Aaj Tak (aajtak.in), independent, prints वहां निवासा. Rhyme and an independent witness. **Keep.**
- विख्यता → विख्याता (st. 2): no word, and the rhyme with माता; Aaj Tak विख्याता. **Keep.**

### Mangal Ki Seva / Mahakali (`mahakali-aarti`)
- Base: the Randhir book, pp. 212–214. Witnesses: Drik Panchang; Aarti Mala (another version, not followed). No recording. No word changed (a comma restored at the caesura of st. 5). The OCR's द्वारा, धेरे are misreadings (the image, i-213: द्वारे, धरे). **Nothing to change.**

### Mahavir (`mahavir-aarti`)
- Base: the Randhir book, p. 145. Witness: Drik Panchang. No recording. जन्में → जन्मे (st. 1): a stray anusvāra on the past tense; the same word, its spelling. **Keep.**

### Mangal Murti Hanuman (`mangal-murti-hanuman-aarti`)
- Base: Drik Panchang (the only witness). No recording. No word changed (stanza 11 kept as a stanza). **Nothing to change.**

### Narmada (`narmada-aarti`)
- Base: the Randhir book, p. 265. Witness: Drik Panchang. No recording. रूद्री → रुद्री: the spelling of the name from रुद्र. **Keep.**

### Om Jai Narsingh Hare (`narsingh-aarti`)
- Base: Drik Panchang (the only witness). No recording. दुस्यु → दस्यु (st. 2): no word; the demon slain. **Keep.**

### Aarti Kijai Narsingh Kunwar Ki (`narsingh-kunwar-aarti`), Natvar (`natvar-aarti`)
- Base: Drik Panchang. No recording. Only the refrain's place and line ends; no word changed. **Nothing to change.**

### Om Jai Parshudhari (`parashuram-aarti`)
- Base: the Randhir book, pp. 150–151. Witness: Drik Panchang. No recording. No word changed (the OCR's differences are misreadings). **Nothing to change.**

### Jai Parvati Mata (`parvati-aarti`)
- Base: the Randhir book, p. 250. Witnesses: Drik Panchang; Aarti Mala. Recording: Anuradha Paudwal (faxIif-3F8o, 1860–2364 s).
- देवबंधु → देववधू (st. 2): she sings देववधू (scored −37.0 against −44.7 for देवबंधु at 2024–2034 s; the windows from 2024 to 2026 s “…ववड़ु जस्दावत”, “तेवबदूँ जस”, with no n); Drik Panchang and Aarti Mala read देव वधू, and the line's dancers are the gods' wives. **Keep.**
- सहस्त्र → सहस्र (st. 4): the spelling of the word. **Keep.**
- st. 5 नन्दी भृंगी बीन लही सारा जग मदमाता: as she sings it, Drik Panchang's line. **Follow the recording (as now).**
- **The other way:** st. 4 सहस्र भुज तनु धरिके: she sings **भुजा** (the windows from 2124 to 2126 s: “शाहस्त्र भुजा तनुदरी के”; scored −26.8 against −32.3), Drik Panchang's word. **Follow the recording: भुजा.**
- **The other way:** st. 6 देवन अरज करत तव चित को लाता: she sings **हम** (the windows from 2213 to 2215 s: “…जगकरत हुं”, “…जकरत हम”; scored −37.7 against −53.4), Drik Panchang's word. **Follow the recording: हम.**
- She sings, in four places, words that no witness writes: the refrain's second line as मैया जय गौरा माता (1887–1889 s), st. 1 जग जननी जगदंबा (1970–1972 s), st. 6's second line as another line (2225–2236 s: “तेरी कृपा रहे तो … मन नहीं भर माता”), st. 7 नर गाता and धन सम्पत्ति (2266–2287 s). The text keeps the book there (§3: each word as a written witness has it); `reconciliation.md` records this as decided.

### Pavansut Hanuman (`pavansut-hanuman-aarti`)
- Base: Drik Panchang (the only witness). No recording. शाषी → शाखी (st. 4): no word; कल्पशाखी, the wish-tree. **Keep.**

### Pitar (`pitar-aarti`), Pretraj (`pretraj-aarti`)
- Base: the Randhir book (pp. 166; 112). Witness: Drik Panchang. No recording. No word changed (the OCR's कीजे, लीजे, खेवबनहारे are misreadings of कीजै, लीजै, खेवनहारे). **Nothing to change.**

### Purushottam (`purushottam-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Aarti Kijai Shri Raghuvar Ji Ki (`raghuvar-aarti`)
- Base: the Randhir book, p. 16. Witness: Drik Panchang. No recording. पुरूषोतम → पुरुषोतम: the spelling of पुरुष (the book's single त kept). **Keep.**

### Ram Raghupati (`ram-raghupati-aarti`), Ram Raghuvir (`ram-raghuvir-aarti`)
- Base: Drik Panchang. No recording. न् → ं (the standard); रुप → रूप, सन्शय → संशय: spelling slips of the same words. **Keep.**

### Aarti Shri Ramayanji Ki (`ramayan-aarti`)
- Base: Gita Press, the āratī at the end of the owner's Mānas. Witness: Drik Panchang. Recording: Pt. Kamlesh Upadhyay, the 30th day (Yi9TFXQYL-4, from about 3290 s). No word changed from Gita Press.
- The other way: the refrain's second line कीरति कलित ललित सिय पी की: Drik Panchang has सिया; the windows at 3317 s hear “ती रशी खली तलड़ी तेशी या पी”, and the scoring gives −39.7 for सिया against −42.4 for सिय, a margin too small to decide; a sung सिय is often drawn out to sound like सिया. Gita Press stands until heard: **on the list to hear.**

### Ramdev (`ramdev-aarti`)
- Base: the Randhir book, p. 161. Witness: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Ramlala (`ramlala-aarti`)
- Base: the words shown with the song (the owner's screenshot of Sohini Mishra's video, 3_QR2HxO3N4). Recording: the same video. सूत हरी → सुत हरि, दिव्यायुद्ध → दिव्यायुध, आज → अज: the captions' slips (सूत "charioteer", हरी "green", युद्ध "war", आज "today" give the lines no sense: Daśaratha's son Hari; weapons with धनुष बाण; Śiva, Aja and Indra). Sung alike, so the recording cannot separate them (every margin under 2). **Keep.**

### Rani Sati (`rani-sati-aarti`)
- Base: the Randhir book, pp. 287–288. Witness: Drik Panchang. No recording. क़रो → करो (a speck of ink), संप्त → सप्त (no word). **Keep.**

### Ravidas (`ravidas-aarti`)
- Base: the Randhir book, p. 94. Witnesses: Drik Panchang; the hymn's own text in Sri Guru Granth Sahib (Rāg Dhanāsarī, Ang 694: ਮਜਨੁ). No recording. भजनु → मजनु (refrain): the Granth's word ("ablution"), the book's भ a misprint. **Keep.**

### Sai Guruvar (`sai-guruvar-aarti`)
- Base: the Randhir book, p. 134. Witnesses: Drik Panchang; Aarti Mala. No recording. दर्शन इच्छित → दर्शन कर इच्छित (st. 4): the half-line has 14 mātrās where every other has 16, and both witnesses fill it (Drik Panchang कर, Aarti Mala से); the metre and two witnesses. **Keep.**

### Jai Santoshi Mata (`santoshi-aarti`)
- Base: the Randhir book, p. 240. Witnesses: Drik Panchang; Aarti Mala (an indif.com printout, close to Drik Panchang). Recording: Anuradha Paudwal (LCYAyR6EmDI), who sings eleven stanzas; the book has seven.
- अपने जन को → अपने सेवक जन को (refrain): she sings सेवक (the transcript at 43–58 s: “अप्दे सेबख जवने”, three times), and the half needs 12 mātrās. **Keep.**
- सुन्दर वीर → सुन्दर चीर (st. 1): she sings चीर (“सुंदरजीर सुनेरी”, 67 s); वीर with धारण कीन्हों gives no sense. **Keep.**
- शुक्रवार प्रिया → प्रिय (st. 5): the singing cannot separate them (−33.4 against −32.1 at 366–375 s); the first half has 12 mātrās in every stanza (हीरा पन्ना दमके, अपने सेवक जन को), प्रिया makes 13, and प्रिय मानना ("hold dear") is the construction; Drik Panchang and Aarti Mala have प्रिय. The metre with the witnesses. **Keep.**
- st. 3 (no नैवेद्य), st. 5 भक्त मण्डली, stanzas 8–11 (not in the book): as she sings them, in the witnesses' words. **Follow the recording (as now).**
- The other way: st. 1 तन श्रृंगार लीन्हों (the book) against Drik Panchang's कीन्हों: −42.4 against −47.0 (80–93 s): the book's word is sung. st. 11 संतोषी माँ की आरती (Aarti Mala): the transcript hears “सन्तो शीमा की आरती” (397 s), not Drik Panchang's माता. Nothing to change.

### Jai Saraswati Mata (`saraswati-aarti`)
- Base: Drik Panchang (the only witness). Recording: Anuradha Paudwal (faxIif-3F8o, 591–1097 s). No word changed; nothing the scoring compared favours another reading. **Nothing to change.**

### Om Jai Lakshmi Ramana / Satyanarayan (`satyanarayan-aarti`)
- Base: Aarti Mala, i-329. Witness: Drik Panchang. Recording: Anuradha Paudwal (sd31yGqZFlA, 1634–1998 s).
- नारद कहत निरंजन → नारद करत निराजन (st. 1): she sings it (the transcript at 1715 s: “नारद करतनी रंखर”); Drik Panchang; the line pictures the āratī itself (nīrājana). **Keep.**
- **The other way:** st. 7 चढ़त प्रसाद सवायो: she sings **सवाया** (the transcript at 1882 s: “चडत प्रसाद सवाया”; scored −25.3 against −32.8 at 1880–1892 s and −49.2 against −57.3 at 1884–1896 s), Drik Panchang's word. **Follow the recording: सवाया.**
- **The other way:** st. 8 जो कोई गावे: she sings **जो कोई नर गावे** (the windows at 1915–1917 s: “…जोग़े नरगावे”, “जो कोई नर गावे”), Drik Panchang's words. **Follow the recording: add नर.** She opens that line with लक्ष्मीरमण जी की आरती (1911–1912 s: “लग्श्मीर मनजी की आरे ती”; −27.6 against −72.2 for श्रीसत्यनारायण जी), which no witness writes: the text keeps श्रीसत्यनारायण जी (§3).
- st. 6 मनवांछित फल दीन्हा (the base): the transcript hears “दीना” (1865 s), the base's ending, not Drik Panchang's दीनो. Nothing to change.

### Shailputri (`shailputri-aarti`), Shankar (`shankar-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Shakambhari (`shakambhari-aarti`)
- Base: the Randhir book, p. 277. Witnesses: Drik Panchang; Aarti Mala. No recording. No word changed. **Nothing to change.**

### Jai Jai Shri Shani Dev (`shanidev-aarti`; now titled from its sung refrain)
- Base: the Randhir book, p. 58. Witness: Drik Panchang. Recording: Chand Kumar (JtJ4P0302FY).
- सूर्य पुत्र प्रभुछाया → सूरज के पुत्र प्रभु छाया (refrain, line 2): as he sings it (the transcript at 42 s: “सुरज के पुत्र प्रभूच्वाया महतारी”), Drik Panchang's words. **Follow the recording (as now).**
- **The other way:** the refrain's first line जय जय जय श्री शनि देव: he sings **two** जय (the transcript: “जेजे श्रिशनी देव” every time; scored −24.1 against −34.0 at 19–29 s, −22.7 against −32.6 at 53–63 s), as Drik Panchang writes it, and his own `fixes.md` quotes it so. **Follow the recording: जय जय श्री शनि देव** (the title follows the text's first words: Jai Jai Shri Shani Dev).
- st. 2 राजित / Drik सहज: no difference in the scoring; the book stands.

### Maiya Sharda Tore Darbar (`sharda-aarti`)
- Base: the Randhir book, pp. 270–271. Witness: Drik Panchang. No recording. दियां → दीया and सुनाऊ → सुनाऊँ: the book's own first printing of the same lines. **Keep.**

### Shirdi Sai Dhoop Aarti (`shirdi-sai-dhoop-aarti`)
- Base: the printout dhoop2 (Marathi, Sanskrit). Witness: dhoop.pdf (an independent printing, read on its text layer). Recording: Pramod Medhi (b_JJzjc2Rgk).
- Every one of the 22 changes is a spelling slip of dhoop2 corrected to dhoop.pdf's form, or a broken Sanskrit form (the Mahimna stotra, the Puṣpāñjali) corrected to the form dhoop.pdf and the grammar both give: तळी, संसृति, दीन (twice), गाता, गाला, ज्यांते, सदनी, वृद्धही, दत्तगुरु, यक्षिणीही, हृदयीं, कृपातपत्रं and the rest. Two witnesses in every case. The singing cannot separate these spellings (every margin under 5, with the longer spelling's extra tokens against it). **Keep.**

### Jai Shitala Mata (`shitala-aarti`)
- Base: the Randhir book, pp. 219–220. Witness: Drik Panchang. No recording. No word changed (the OCR's मृंग, नारायग are misreadings). **Nothing to change.**

### Om Jai Shiv Omkara (`shiv-aarti`)
- Base: four written witnesses, each line as Anuradha Paudwal sings it (Yb2GMwJyGnE); the doubtful lines were settled by the owner's ear (st. 4 ब्रह्मादिक सनकादिक, st. 5 जगकर्ता जगहर्ता जग पालनकर्ता, st. 6 प्रणवाक्षर के मध्ये, st. 7, the closing refrain). The owner's ear wins. Nothing the scoring compared favours another reading. **Follow the recording (as now).**

### Siddhidatri (`siddhidatri-aarti`)
- Base: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Sita (`sita-aarti`)
- Base: Drik Panchang. No recording. दीनोद्वारिणि → दीनोद्धारिणि, श्रोमणि → शिरोमणि (st. 1, 2): no words; Amar Ujala and mantra.tips (independent of Drik Panchang) have the right forms, and the metre needs शिरोमणि. **Keep.**

### Sitaram (`sitaram-aarti`)
- Base: Drik Panchang. No recording. न् → ं (सिंगार, दंपति): the standard. **Keep.**

### Skandamata (`skandamata-aarti`)
- Base: Drik Panchang. No recording.
- मै → मैं, कही → कहीं: dropped nasals (the rhyme with मैं; कहीं "somewhere"); DNA Hindi, Boldsky. **Keep.**
- खण्ड → खण्डा (st. 5): खण्ड ("a piece") is a word, but the half is a mātrā short of 16 and खण्डा is the sword she raises; DNA Hindi and Boldsky, independent of Drik Panchang and of each other, both have खंडा. Metre and two witnesses. **Keep.**

### Surya (`surya-aarti`)
- Base: Aarti Mala, i-332. Witness: Drik Panchang. No recording. तिमिन → तिमिर, सुर्कम → सुकर्म (a misplaced repha), करूणा → करुणा: no words, or the spelling of the same word. **Keep.**

### Jai Jai Tulsi Mata (`tulsi-aarti`)
- Base: the Randhir book, p. 230 (i-229). Witnesses: Drik Panchang (= Bhakti Bharat); Hindupad; mantra.tips. Recording: Anuradha Paudwal (faxIif-3F8o, 2365–2827 s).
- बटु पुत्री (st. 2): the book's word, as now. She sings बटु (scored −34.8 against −43.0 for बहु at 2556–2568 s, −33.6 against −41.5 at 2574–2586 s). **The base stands (as now).**
- सब लोगों → सब रोगों (st. 1): she sings रोगों (the transcript at 2493 s: “सब रोगो की उबर”; −21.8 against −25.7), and the line goes on रुज से रक्षा ("guarding from illness"). **Keep.**
- श्याम वरुण → श्याम वर्ण (st. 5): she sings वर्ण (−37.0 against −43.6 at 2786–2801 s); वरुण gives the line no sense. **Keep.**
- The other way: at every word where Drik Panchang differs and we keep the book (the refrain's सब जग की सुख दाता, विष्णु प्रिये, कुमारी, उनका तुमसे कैसा नाता), the singing favours the book's words (−34.2 against −51.0; −55.6 against −58.7; −37.0 against −48.6; −37.7 against −69.4). Nothing to change. (`fixes.md`'s gloss of the stanza 2 windows wrote बहु for the बटु it hears; set right.)

### Vaishno Devi (`vaishno-devi-aarti`)
- Base: Aarti Mala, i-353 (an indif.com printout, a copy of the same web text as Drik Panchang). Witness: Drik Panchang. No recording.
- सेवत → सेवक (st. 2): the base and Drik Panchang are two copies of one typed text and differ here; सेवत leaves its clause with no subject in a stanza where every clause names who serves (ब्रह्मा, शंकर, नारद). **Keep.**
- मै → मैं, ब्रह्मावेद पढे → ब्रह्मा वेद पढ़े, पाव सुपारी ध्वाजा → पान सुपारी ध्वजा, चरणो → चरणों: dropped signs and non-words. **Keep.**
- Two half-stanzas the page drops (st. 6, 7), taken from Drik Panchang: their sentences are incomplete without them. **Keep.**

### Vindhyeshwari (`vindhyeshwari-aarti`)
- Base: the Randhir book, p. 182. Witnesses: Drik Panchang; Aarti Mala. No recording. The bracketed (तेरा) not taken. No word changed. **Nothing to change.**

### Vishwakarma (`vishwakarma-aarti`)
- Base: the Randhir book, p. 89. Witness: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Vrishbhanu Lali (`vrishbhanu-lali-aarti`), Yamuna (`yamuna-aarti`), Yashoda Lala (`yashoda-lala-aarti`)
- Base: Drik Panchang. No recording. Only the refrain's place, line ends, न् → ं (the standard) and a compound put whole on one line; no word changed. **Nothing to change.**

### Vrishbhanu Suta (`vrishbhanu-suta-aarti`)
- Base: the Randhir book, p. 225. Witness: Drik Panchang. No recording. Only the stanza division (the rhyme), no word changed. **Nothing to change.**

### Aarti Jugal Kishor Ki Kijai (`yugal-kishor-aarti`)
- Base: the Randhir book, p. 47. Witnesses: Drik Panchang; Aarti Mala. No recording. No word changed (the OCR's differences are misreadings or Aarti Mala's other spellings). **Nothing to change.**

## Chālīsās

For each chālīsā the metre was counted at every changed half-line (a caupāī half 16 mātrās, a dohā 13 + 11), with the base's reading beside ours. The recording is evidence; it does not decide alone.

### Shri Annapurna Chalisa (`annapurna-chalisa`)
- Base: the Randhir book, pp. 241–244. Witnesses: Drik Panchang; Shubh Panchang; InstaAstro. No recording.
- अनंद → आनंद (cau. 1): the half is 15 mātrās with अनंद, 16 with आनंद; Drik Panchang, Shubh Panchang, InstaAstro. **Keep.**
- गाय → गाये (cau. 11), मनभाय → मनभाये (cau. 26): the rhyme (गनाये, सिधाये) and the metre (15 → 16); Shubh Panchang and InstaAstro. **Keep.**
- पदिदेवता → पतिदेवता, कीह्न → कीन्ह (3 places), स्त्रष्टा → स्रष्टा, इज्ञ → दक्ष, पनि → पति, प·ढ़हहिं → पढ़िहहिं: non-words or a damaged print, the right forms in the witnesses and in the book itself. **Keep.**

### Baba Gangaram (`baba-gangaram-chalisa`)
- Base: the Randhir book, pp. 167–171. Witness: Drik Panchang. No recording. जन्में → जन्मे (cau. 31): a stray anusvāra on the same word. **Keep.**

### Balaji (`balaji-chalisa`)
- Base: the Randhir book, pp. 112–115. Witness: Drik Panchang. No recording. No word changed (the OCR's differences are misreadings). **Nothing to change.**

### Bagalamukhi (`bagalamukhi-chalisa`)
- Base: the Randhir book, pp. 251–254. Witness: Drik Panchang. No recording. गग्गुल → गुग्गुल (cau. 26): the book's own word in cau. 25. **Keep.**

### Batuk Bhairav (`batuk-bhairav-chalisa`)
- Base: the Randhir book, pp. 69–72. Witnesses: Drik Panchang; Shubh Panchang. No recording. भजं → भजूं (dohā 2): no word; the lost ū of the first person, as रचूं before it. **Keep.**

### Bhairav (`bhairav-chalisa`)
- Base: the Randhir book, pp. 64–67. Witness: Drik Panchang. No recording. अहछु → अहहु (cau. 33): a damaged letter; the book's own अहहु in cau. 13 and 25. **Keep.**

### Brahma (`brahma-chalisa`)
- Base: the Randhir book, pp. 48–52. Witnesses: Drik Panchang; Shubh Panchang. No recording.
- कमलासान → कमलासन (cau. 1): no word, 17 mātrās; the book's own spelling in cau. 11 and 15. **Keep.**
- घाता → धाता (dohā 2): घाता is no name of Brahmā; अज, विधि, धाता are his names; ध/घ one stroke. **Keep.**
- मुन्दर → सुन्दर, भैटहु → भैंटहु: non-words. **Keep.**

### Shri Durga Chalisa (`durga-chalisa`)
- Base: the Randhir book, pp. 173–176. Witnesses: Drik Panchang (= Chalisa Mala, an indif.com printout of the same text); Green Message. Recording: BhaktiDhaam (lCwPg0LRRjk, 1479–1791 s).
- नाग कोटि → नगर कोटि (cau. 20): the passage names the Mother's seats (हिंगलाज, ज्वाला), Nagarkoṭ among them; Drik Panchang and Green Message (नगरकोट), independent; the recording sings it (the transcript at 1627 s: “नागर कोट में तुम ही विराजत”). **Keep.**
- काली को धारा → कालिका धारा (cau. 23): the book's half has 17 mātrās, कालिका gives 16; Drik Panchang; the recording sings कालिका (1652 s: “रूप कराल का लिका दारा”). The metre with the witness. **Keep.**
- बाला → ज्वाला (cau. 26): Drik Panchang and Green Message, independent, have ज्वाला, and the passage names the seats (ज्वाला in cau. 21); बाला in "बाला में है ज्योति तुम्हारी" gives no clear sense. The recording cannot settle it (the 5-s windows at 1675–1677 s: “सवाला मी है जोती”, “वायला मी है जोती”; the scoring within its margin of doubt). **Keep; on the list to hear.**
- अमर पुरी औरों सब लोका → अमरपुरी अरु बासव लोका (cau. 25), जस → यश (cau. 27, 39): changed only because the recording sings Drik Panchang's words. The book's readings are sound ("Amarāvatī and all the other worlds"; जस is the Hindi form of यश, the same word), and the metre is the same. A recording and one witness against a sound base. **Revert to the base.** The recording sings अमरपुरी अरु बासव लोका and यश there.
- The other way: the recording sings cau. 40 as दुर्गा चालीसा जो कोई गावै (no witness) and cau. 36's second half as the book has it. Nothing else.

### Shri Ganesha Chalisa (`ganesha-chalisa`)
- Base: the Randhir book, pp. 7–10. Witnesses: Drik Panchang (= Chalisa Mala, Bhakti Bharat); Bhāratkosh; Prabhat Khabar; Shubh Panchang; Hindu Blog. Recording: Anuradha Paudwal (oHHniScYJzo).
- केहि → कहि (cau. 16): केहि ("whom") gives no sense before अन्तर्धान ("having said so, vanished") and makes the half 17 mātrās; Drik Panchang, Bhāratkosh, Prabhat Khabar, Shubh Panchang and Hindu Blog have कहि. **Keep.**
- सम्बन्ध → सम्वत् (closing dohā 2): the line gives the year; Bhāratkosh, Prabhat Khabar and Hindu Blog print सम्वत्, Shubh Panchang संवत्; she sings सम्बन्ध (the transcript at 509 s: “सम बन्द”), which stays corrected (§3). **Keep.**
- अपना → अपने (closing dohā 2) and भक्ति शक्ति → शक्ति भक्ति (cau. 38): changed only because she sings Drik Panchang's words; the book's are sound. **Revert to the base.** She sings अपने and शक्ति भक्ति there (467 s: “आपनी शक्तिवाप्ति पुछ दीजे”).
- The other way: closing dohā 1 पाठ करै धर ध्यान (the book; Drik Panchang कर ध्यान): she sings धर (481 s: “पाथ करे दर्द्यान”). Elsewhere her differences from our text are spellings sung alike (मिलहिं / मिलहि, ह्वै / हवै).

### Shri Ganga Chalisa (`ganga-chalisa`)
- Base: the Randhir book, pp. 256–259. Witness: Drik Panchang. No recording.
- जय हनु सुता → जहनु सुता (cau. 3): हनु सुता gives no sense, and the half has 17 mātrās; Jahnu's daughter, the ज misread as a separate जय. **Keep.**
- तंग → तुंग (cau. 7): तंग ("narrow") cannot describe waves; the opening dohā's own अनुपम तुंग तरंग. **Keep.**
- सहत्र → सहस्र, अधिन → अघिन: non-words. **Keep.**

### Shri Gayatri Chalisa (`gayatri-chalisa`)
- Base: the Randhir book, pp. 197–200. Witness: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Giriraj (`giriraj-chalisa`)
- Base: the Randhir book, pp. 135–139. Witness: Drik Panchang. No recording. पखवारे → रखवारे (cau. 22: "fortnight" gives no sense), पढ़ावें → चढ़ावें (cau. 34: offerings; the book's own word elsewhere), चालिसा → चालीसा (the book's own title). **Keep.**

### Gita (`gita-chalisa`)
- Base: Drik Panchang. No recording. श्रद्घा → श्रद्धा (no word); सामान → समान (cau. 39: "goods" gives no sense; "like me", as cau. 23, 27, 33; the metre 17 → 16). **Keep.**

### Gopal (`gopal-chalisa`)
- Base: the Randhir book, pp. 43–47. Witness: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Gorakhnath (`gorakhnath-chalisa`)
- Base: the Randhir book, pp. 95–99. Witness: Drik Panchang. No recording. अगर → अगम (closing dohā 2): अगर ("if") gives no sense; अगम अगोचर is the pair of cau. 30. **Keep.**

### Shri Hanuman Chalisa (`hanuman-chalisa`, the Sundarakāṇḍa's)
- Base: the Sundarakāṇḍa work's text (`tools/works/sundarkand/reconciliation.md`): Bhakti Bharat and Kavita Kosh for the words, the Gita Press spelling of our Mānas for the spelling (बिभीषन, लंकेस्वर, संकर, कबि कोबिद, रच्छक, जियाए), the metre where they differ. Recording: Pt. Ashwin Kumar Pathak (QjSpUgnEPLU, 5791–6062 s).
- Every difference from Drik Panchang is a spelling the Mānas decides (मुकुरु, बिभीषन, लंकेस्वर, रच्छक, बचन, सर्ब, सेइ, जै) or a word the two web witnesses and the metre settled (औ, सोइ, नौ निधि); the singing cannot separate the spellings (sung alike; the margins come from the longer spellings' extra tokens). **Nothing to change.**

### Jaharveer (`jaharveer-chalisa`)
- Base: the Randhir book, pp. 101–105. Witness: Drik Panchang. No recording. हे → है (cau. 2: a call cannot stand inside the phrase; the verb is needed), जन्में → जन्मे. **Keep.**

### Kali (`kali-chalisa`)
- Base: the Randhir book, pp. 202–206. Witness: Drik Panchang. No recording. रूद्राणी → रुद्राणी, अग्रि → अग्नि, सहस्त्राक्षि → सहस्राक्षि, अरू → अरु: spellings of the same words, or a non-word. **Keep.**

### Khatu Shyam (`khatu-shyam-chalisa`)
- Base: the Randhir book, pp. 152–155. Witness: Drik Panchang. No recording. जगदीश → जगदीशा (cau. 14: the rhyme with ईसा and the metre, 15 → 16), श्याय → श्याम (no word). **Keep.**

### Krishna (`krishna-chalisa`)
- Base: the Randhir book, pp. 33–36. Witnesses: Drik Panchang; Shubh Panchang. No recording. घुँघँराले → घुँघराले, मारथ → भारथ (no word; the rhyme with पारथ), नवनिद्धि → नवनिधि, चरि → चारि (the rhyme with धारि): misprints. **Keep.**

### Kuber (`kuber-chalisa`)
- Base: Drik Panchang. No recording. ढ़ेर → ढेर: no word with the dot; the rhyme with टेर. **Keep.**

### Lakshmi (`lakshmi-chalisa`)
- Base: the Randhir book, pp. 183–186. Witnesses: Drik Panchang (= Chalisa Mala). No recording in the library (an unused recording in scriptures-data, p88Tkkuz0W8, was scanned for cau. 38 and does not settle it).
- ताप → त्रिविध ताप (cau. 21): the book's half has 14 mātrās; Drik Panchang supplies the dropped word, the "threefold" afflictions. Metre and the witness. **Keep.**
- मन में → तन में (cau. 38, first half): the book's नहिं मोहि ज्ञान बुद्धि है मन में ("I have no knowledge or wisdom in my mind") makes sense and keeps the metre; only its rhyme repeats the second half's मन में. Drik Panchang and its copy are one witness; "makes more sense" is not enough. **Revert to the base.**

### Lalita (`lalita-chalisa`)
- Base: the Randhir book, pp. 278–281. Witness: Drik Panchang. No recording. तब → तव (cau. 1, 28): "then" leaves the virtues and glory with no possessor; "your" (तव). सहस्त्रार → सहस्रार: the spelling. **Keep.**

### Mahakali (`mahakali-chalisa`)
- Base: the Randhir book, pp. 208–212. Witness: Drik Panchang. No recording. ब्योंम → ब्योम (no word), धूप्र → धूम्र (the demon Dhūmralocana; the page's म्र prints like प्र). **Keep.**

### Mahalakshmi (`mahalakshmi-chalisa`)
- Base: the Randhir book, pp. 187–190. Witness: Drik Panchang. Recording in scriptures-data not in the library. सौहे → सोहे, अरू → अरु, राजााहि → राजाहि: misprints. मेरी → मोरी (cau. 36): the same word, its rhyming form with जोरी. **Keep.**

### Mahavir (`mahavir-chalisa`)
- Base: the Randhir book, pp. 141–144. Witness: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Mangalmay Ganesha (`mangalmay-ganesha-chalisa`)
- Base: Drik Panchang. No recording. Every change is a typing slip of the page with the metre to show it: रूज → रुज (dohā 13 + 11; twice), शम्भ्पूत → शम्भुपूत (15 → 16), मे/नही → में/नहीं, बढाये/बढाओं → बढ़ाये/बढ़ाओ, कसे → कैसे (15 → 16), चढि → चढ़ि, श्रृद्धा → श्रद्धा, चालीस → चालीसा (the rhyme with गौरीसा), शंबू → शम्भु (the page's own spelling). **Keep.**

### Narasimha (`narasimha-chalisa`)
- Base: Drik Panchang. No recording. ताकि → ताकी (cau. 27): "his body", and the metre 15 → 16. **Keep.**

### Narmada (`narmada-chalisa`)
- Base: the Randhir book, pp. 261–264. Witness: Drik Panchang. No recording. कुरूक्षेत्र → कुरुक्षेत्र: the spelling of the name. **Keep.**

### Navagraha (`navagraha-chalisa`)
- Base: the Randhir book, pp. 79–83. Witness: Drik Panchang. No recording. चालीसाा → चालीसा, गुरूदेवा → गुरुदेवा (the book's own गुरु in the next chaupāī; the metre). **Keep.**

### Parashurama (`parashurama-chalisa`)
- Base: the Randhir book, pp. 146–150. Witness: Drik Panchang. No recording. सहस्त्र → सहस्र, सहस → सहस्र (a dropped sign; the śloka's metre): spellings. **Keep.**

### Parvati (`parvati-chalisa`), Pretraj (`pretraj-chalisa`)
- Base: the Randhir book. Witness: Drik Panchang. No recording in the library. No word changed. **Nothing to change.**

### Pitar (`pitar-chalisa`)
- Base: the Randhir book, pp. 162–166. Witness: Drik Panchang. No recording. झंझुनू ने → झुंझुनू में, देवो → देवों (cau. 8: the town's name and dropped signs), मरूप्रदेश → मरुप्रदेश. **Keep.**

### Radha (`radha-chalisa`)
- Base: the Randhir book, pp. 221–224. Witnesses: Drik Panchang (= Chalisa Mala); Shubh Panchang; Aaj Tak. No recording.
- वृन्दावनविपिन → वृन्दाविपिन (dohā 1: 25 mātrās for 24; the book's own word elsewhere), वृषभान → वृषभानु (cau. 1: 15 → 16, the book's own spelling in cau. 9 and 40), युग युग → युत युग (cau. 12: a doubled word), भेजिहैं → भजिहैं (cau. 33: "send" gives no sense; the rhyme with तरिहैं; 17 → 16), बढ़ना → बदना (cau. 11: the face, rhyming with नयना), तिहारौ → तिहारी (cau. 40: the rhyme with दुलारी). **Keep.**
- सारद → सादर (cau. 32): सारद गान करत नित वेदा could be read "Śāradā and the Vedas ever sing", so the sense alone does not settle it; but Drik Panchang, Shubh Panchang and Aaj Tak all read सादर, and a swap of two letters (सादर ↔ सारद) is the printer's commonest slip. Three witnesses against the book. **Keep.**

### Shri Ram Chalisa (`ram-chalisa`)
- Base: the Randhir book, pp. 12–15. Witness: Drik Panchang. Recording: BhaktiDhaam (lCwPg0LRRjk, 2711–3027 s).
- हदय → हृदय (cau. 17, 36), शंरव्र → शंख (cau. 38): a dropped ऋ sign and a broken word. **Keep.**
- हमारे → हमरे (cau. 39): the half has 17 mātrās with हमारे, 16 with हमरे; Drik Panchang; the recording sings हमरे. The metre with the witness, not the recording alone. **Keep.**
- The other way: the recording's other differences (लखन for लषन, तुव for तव) are Drik Panchang's spellings of the same words; the book stands.

### Ramdev (`ramdev-chalisa`), Ravidas (`ravidas-chalisa`)
- Base: the Randhir book. Witness: Drik Panchang. No recording. No word changed. **Nothing to change.**

### Rani Sati (`rani-sati-chalisa`)
- Base: the Randhir book, pp. 283–287. Witnesses: Drik Panchang; InstaAstro; Festivals of India; Bhakti Bharat. No recording. भवान → भवानी (cau. 1: the rhyme with मानी, 15 → 16), सुन्दरर → सुन्दर (17 → 16), मु → मुख (cau. 19: no word), the bracketed (मैं) not part of the verse (cau. 40: 18 → 16). **Keep.**

### Sai (`sai-chalisa`)
- Base: the Randhir book, pp. 117–133. Witnesses: Drik Panchang (= Chalisa Mala). No recording.
- यहो → यही, तिमिरि → तिमिर, हो → ही (v. 66: हो has no place before गुण गाया): non-words or no sense. **Keep.**
- मैं प्यासा था → मैं प्यासा का प्यासा था (v. 26), हो उठा → होश हो उठा (v. 41): the halves are 8 and 13 mātrās where every line has 14 and 16, and say nothing without the dropped words; the witness supplies them. **Keep.**
- सच को → सब को (v. 59): "gave affection to truth" against the half's own pair सबको अनतुल प्यार किया. **Keep.**
- क्षण भर में → क्षण भर के (v. 88): the couplet rhymes हर के / भर के; the rhyme with the witness. **Keep.**

### Santoshi (`santoshi-chalisa`)
- Base: the Randhir book, pp. 236–239. Witness: Drik Panchang. Recording: BhaktiDhaam (lCwPg0LRRjk, 1791–2109 s). अरू → अरु (cau. 19: the spelling, 17 → 16). The recording favours our text wherever the scoring could compare. **Keep.**

### Saraswati (`saraswati-chalisa`)
- Base: the Randhir book, pp. 192–195. Witnesses: Chalisa Mala; Drik Panchang; Shubh Panchang. No recording in the library.
- पदम दुरज → पद कमल रज (dohā 1): दुरज is no word and the quarter is short of 13; the witnesses all read "the dust of the lotus feet", in different forms; Drik Panchang's taken. **Keep.**
- चर्तुभुज → चतुर्भुज, नवैद्य → नैवेद्य, सकहिन → सकहिं न: misprints of the same words. तब → तव (cau. 6): "by your grace". करु → करउं (cau. 13): the speaker's "I plead", and 14 → 16 mātrās; Chalisa Mala. **Keep.**

### Shakambhari (`shakambhari-chalisa`)
- Base: the Randhir book, pp. 272–276. Witness: Drik Panchang. No recording. नें → ने: the spelling. **Keep.**

### Shani (`shani-chalisa`)
- Base: the Randhir book, pp. 59–62. Witness: Drik Panchang. Recording: BhaktiDhaam (lCwPg0LRRjk, 2109–2710 s).
- हवैं → ह्वैं (cau. 8: the book's own form in cau. 18), स्वर्ण सर्व सर्वसुख → स्वर्ण सर्वसुख (cau. 35: सर्व printed twice, 19 → 16 mātrās), कीहों → कीन्हों (closing dohā). **Keep.**
- मंगल भारी → मंगल कारी (cau. 35): changed only because the recording sings Drik Panchang's word; भारी ("great") is sound and rhymes. **Revert to the base.** The recording sings कारी.
- स्वान सवार → स्वान सवारी (cau. 32): सवार ("riding") is sound and gives the half its 16 mātrās; सवारी makes 17. Only the rhyme with भारी and one witness speak for it, and the recording cannot tell them apart (−131.3 against −130.5). **Revert to the base.**
- The other way: the recording sings Drik Panchang's कीन्हों / दीन्हों for the book's कीन्हयों / दीन्हयों (cau. 22; −114.8 against −142.2 at 2381–2393 s) and है for ह्वैं (cau. 8; −79.0 against −94.5), and लखन for लषण: forms of the same words; the book stands.

### Shanishchar (`shanishchar-chalisa`)
- Base: the Randhir book, pp. 54–57. Witness: Drik Panchang. No recording. मगाऊँ → मनाऊँ (cau. 3: "have it brought" gives no sense with the names invoked), कीहौं → कीन्हौं (a dropped न्, as the other Śani Chālīsā's dohā). **Keep.**

### Sharda (`sharda-chalisa`)
- Base: the Randhir book, pp. 266–269. Witness: Drik Panchang. No recording. सहस्त्र → सहस्र: the spelling. **Keep.**

### Shitala (`shitala-chalisa`)
- Base: the Randhir book, pp. 215–218. Witness: Drik Panchang. No recording. त्रलोक्य → त्रैलोक्य (no word; 15 → 16), मोर मोर → मोर (a typesetter's repeat; 19 → 16). **Keep.**

### Shiv (`shiv-chalisa`)
- Base: the Randhir book, pp. 17–20. Witness: Drik Panchang. Recording: BhaktiDhaam (lCwPg0LRRjk, 0–394 s), which sings the book's version.
- कि → की (cau. 5): "the darling of mother Mainā" needs the postposition; कि ("that") gives no sense. **Keep.**
- The other way: the recording's differences from our text are forms of the same words (तब ही दुख for तबहीं दुःख, कीन्ही for कीन्हीं, जय for जै); the book stands.

### Surya (`surya-chalisa`)
- Base: the Randhir book, pp. 74–77. Witness: Drik Panchang. No recording. सहस्त्रांशु → सहस्रांशु (3), छन → धन (cau. 17: "wealth, sons and family grow"), वांस → वास (cau. 20: "bamboo" gives no sense), रहम → रहत (cau. 23), बीज → बीच (cau. 29), धन्य-२ → धन्य-धन्य (the printer's sign for a repeat; 13 → 16), मध → मधु (cau. 37: the month). Misprints, each shown by the sense or the metre. **Keep.**

### Tulsi (`tulsi-chalisa`)
- Base: Drik Panchang. No recording. बिरजिनी → बिराजिनी (no word; 12 → 13), संग्राम → संग्रामा (the rhyme with बलधामा; 15 → 16), प्रयास → प्रयाग (cau. 39: the poet's place, east of Prayāga; "effort" gives no sense). **Keep.**

### Vaishno Devi (`vaishno-devi-chalisa`)
- Base: the Randhir book, pp. 231–234. Witnesses: Drik Panchang (which copies the book's slips); Patrika; Shubh Panchang. No recording in the library.
- नमोः → नमो (cau. 1): a broken form. **Keep.**
- शोषण → पोषण (cau. 8): Patrika and Shubh Panchang, independent of the book and of each other, print पोषण; the goddesses will "nourish" her in the cave, not "dry her up". A corruption the book and its copy share, shown by independent witnesses (§2). **Keep.**

### Vindhyeshwari (`vindhyeshwari-chalisa`)
- Base: the Randhir book, pp. 179–182. Witnesses: Drik Panchang; Chalisa Mala. No recording. चौसट्टी → चौसट्ठी (the word sixty-four), मन माई → मन लाई (cau. 25: no sense; the book's own पाठ करे मन लाई in cau. 35). **Keep.**

### Vishnu (`vishnu-chalisa`)
- Base: the Randhir book, pp. 38–41. Witness: Drik Panchang. Recording: BhaktiDhaam (lCwPg0LRRjk, 1150–1479 s).
- मतस्य → मत्स्य (cau. 14): no word; the fish avatar. **Keep.**
- नित → निज (cau. 30): changed only because the recording sings Drik Panchang's word; देखहुँ मैं नित दरश तुम्हारे ("may I see your sight every day") is sound. **Revert to the base.** The recording sings निज.

### Vishwakarma (`vishwakarma-chalisa`)
- Base: the Randhir book, pp. 85–89. Witness: Drik Panchang. No recording. लोक → लोह (cau. 34): the half lists the crafts (iron, wood, stone, copper); "world" is no craft. **Keep.**

## Lines to hear

The two places where neither the transcript, the 5-s windows nor the scoring settles what is sung. The text stands as decided above until the owner hears them.

| Work | Verse | Recording, time | Our text | The other reading |
|---|---|---|---|---|
| Aarti Shri Ramayanji Ki (`ramayan-aarti`) | refrain, line 2 | Yi9TFXQYL-4, 55:15–55:18 (3315–3318 s) | कीरति कलित ललित सिय पी की (Gita Press) | सिया पी की (Drik Panchang) |
| Shri Durga Chalisa (`durga-chalisa`) | chaupāī 26 | lCwPg0LRRjk, 27:55–28:00 (1675–1680 s) | ज्वाला में है ज्योति तुम्हारी (Drik Panchang, Green Message) | बाला में है ज्योति तुम्हारी (the book) |

## What changed

- **Āratīs, following their recordings** (each word as a written witness has it): the Hanumān āratī (in the Sundarakāṇḍa) drops जन from सुर नर मुनि आरती उतारें; the Pārvatī āratī sings भुजा (st. 4) and हम (st. 6); the Satyanārāyaṇa āratī sings सवाया (st. 7) and नर (st. 8); the Śani āratī's refrain opens जय जय श्री शनि देव (its title with it).
- **Chālīsās reverted to the base**, where a sound reading had been changed only because the recording sings Drik Panchang's: the Durgā Chālīsā (cau. 25, 27, 39), the Gaṇeśa Chālīsā (cau. 38; closing dohā 2's अपना), the Śani Chālīsā (cau. 32, 35), the Viṣṇu Chālīsā (cau. 30); and the Lakṣmī Chālīsā's मन में (cau. 38), changed on one witness.
- **Settled in the files:** the Ambe āratī's श्री अम्बेजी (heard); the Pārvatī and Satyanārāyaṇa āratīs' lines with no witness (heard, the base kept); the Tulasī āratī's `fixes.md` gloss.
- Every other change from the base in the 152 works stands, on the grounds given above.

## Recordings added during this review

While this review ran, the recordings of the Chālīsā and Āratī shelves were extended on `main` (62 āratīs and 31 chālīsās now live, more as drafts). This review heard the recordings each work had before then. Each newly added recording's `reconciliation.md` section ("The recording") lists the verses where it sings another witness's words against the base, and the verses where it sings words no witness has; for an āratī whose recording is now live, those verses are the next to hear and decide as above (an āratī follows its recording; a chālīsā keeps its sound base).
