# Chāndogya Upaniṣad — how the text is settled

**Base:** <https://shlokam.org/text/chandogya-upanishad.htm>, fetched on 2026-11-14 (private copy in scriptures-data at `hinduism/veda/samaveda/upanishad/chandogya-upanishad/printouts/shlokam/chandogya-upanishad.html`). It gives the Sāmaveda śānti mantra and the eight adhyāyas in 621 blocks of Devanagari, each with the page's own transliteration; there are no svara marks.

## Witnesses
- **The page's transliteration.** `source/settle.py` reads it back into Devanagari and compares it with the page's Devanagari, block by block. They agree everywhere but one place (8.5.2, below) and the page's ways of writing one sound twice (the candrabindu of अस्मिँल्लोके, which the transliteration writes m̐). They share most slips (निराकरणंं / nirākaraṇaṃṃ, तब्ब्रह्म / tabbrahma, the ; of 3.17.7): the transliteration is the page's own copy of its Devanagari, so it confirms what the page has, not what is right.
- **The text's own parallels and the grammar.** The Chāndogya repeats its formulas many times (the honey teaching's five directions, the Vaiśvānara's six questions, the tat tvam asi refrain, Nārada's list of learning). Each mantra was read against its parallels and against sandhi and the forms of the words; a place the page writes in a way that is no word, breaks the sandhi it keeps everywhere else, or departs from its own formula by a dropped or extra letter or word, is corrected (below). A valid reading the page has is kept.
- **Four web witnesses**, compared with every mantra by `source/check.py` (raw downloads in scriptures-data at `hinduism/veda/samaveda/upanishad/chandogya-upanishad/printouts/<site>/`, each with its `.meta.json`; `source/witnesses.py` makes `source/witness/<site>.txt` from them):
  - **IIT Kanpur Heritage** (`heritage.iitk.ac.in`, text CHU; `iitk/`): the primary mūla of each ref. No printed edition named; many typing slips of the old Gita Supersite data: ध्द for द्ध and ड्ग for ङ्ग, which `check.py` reads as the letter they stand for (`NORM`), and श्र for भ, ष्र्ट for र्ष्ट, dropped or doubled signs, recorded as its readings.
  - **upanishads.org.in** (`upanishads-org/`, one page per mantra): the same text as GRETIL letter for letter, with GRETIL's word division and slips (nearly every difference it has from the base, GRETIL has too): a copy of GRETIL, so the two count as **one** witness.
  - **Sanskrit Wikisource** (`wikisource/`, one page per adhyāya): the page's own edition. It shares the page's slips in most places the text corrects (57 of its readings are the page's), so it confirms what the page prints, not what is right.
  - **GRETIL** (`gretil/sa_chAndogyopaniSad-comm.xml`, with Śaṅkara's bhāṣya, IAST read into Devanagari word by word). It shares 20 of the page's slips (प्रावहणो, भूतन्य, प्रजपति, मूधा, ब्रह्मचार्यम्, वार्षाण्य, सर्वमयुरेति, उदाङ्मुख, सर्ष्टितां, उपासित …), so it and the page come from one digital ancestor; where they part, it often has the right form.
  - The Vedic Heritage Portal's Chāndogya page has no text (video only).
- **How they weigh.** IIT Kanpur is the one witness independent of the page; GRETIL (with upanishads.org.in) is half-independent; Wikisource is the page. A correction needs the base to be clearly wrong (a non-word, a broken form, a sense the sentence cannot carry, a word dropped from the text's own formula) and the witnesses to give the right form; a valid reading of the page stays, whatever the others read.

## Structure
- **Blocks and mantras.** Nine blocks hold more than one mantra (2.13.1–2, 3.12.7–9, 3.17.7–8 (below, "3.17.7"), 4.1.5–6, 4.16.2–3, 5.8.1–2, 5.10.1–2, 6.11.1–2, 6.13.1–2): they are split at the page's ॥ a.k.m ॥ marks. Every khaṇḍa then runs 1 … N without a gap, every adhyāya's khaṇḍas run 1 … N, and `settle.py` checks it.
- **6.6.5.** The page numbers the last mantra of 6.6 “६.६.६” and has no 6.6.5. Nothing is missing: the khaṇḍa is the four likenesses (curd 6.6.1, food 6.6.2, water 6.6.3, fire 6.6.4, each “योऽणिमा स ऊर्ध्वः समुदीषति”) and the mantra that sums them up (अन्नमयं हि सोम्य मन आपोमयः प्राणस्तेजोमयी वाक्), which closes the khaṇḍa with ॥ इति षष्ठः खण्डः ॥, as 6.5.4 closes 6.5 with the same words after three likenesses. It is 6.6.5 (`RENUMBER`).
- **Headings and closing lines.** The page's ॥ प्रथमोऽध्यायः ॥ before each adhyāya and its ॥ इति … खण्डः ॥ and ॥ इति … अध्यायः ॥ lines are not part of any mantra and are left out (the page has no adhyāya closing after 8.15.1, and none for khaṇḍa 4.17). One closing line stands at the start of 5.4.1 on the page; it is left out too.
- **The śānti mantra** is the page's opening block (“1.1.0”), and the work's `shanti.1`. The page does not give it again at the end.
- **Word spacing** is the page's: it often writes a word ending in ं against the next (हीदंसर्वं, तंह, रसानांरसतमः), as Vedic prose is often printed; the words are the same, and the spacing is kept except where it breaks a word (below).
- **Numbers.** The page ends each mantra with its full number (॥ ६.८.७ ॥); the text ends it with its own, as the library writes every verse (॥७॥), and cites it 6.8.7. The pluta marks of the sāman passages (ओ३म्, हा३उ, the ३ and २ of 1.12.5 and 2.24) are kept as printed.

## Corrections to the page (all in `source/settle.py` → `FIX`)

| Item | The page | The text | Why |
|---|---|---|---|
| shanti.1 | निराकरणंं | निराकरणं | a doubled anusvāra (ṃṃ in the transliteration too) |
| 1.2.1 | संयेतिरे उभये | संयेतिर उभये | sandhi: -e before a vowel becomes -a (संयेतिरे is a plural, not a dual) |
| 1.2.6 | संकल्पनीयंच चासंकल्पनीयं | संकल्पनीयं चासंकल्पनीयं | an extra च: the parallels 1.2.3–1.2.5 read X चाX च |
| 1.6.1 | च्यध्यूढ़ं साम | च्यध्यूढं साम | ढ़ with a nukta is not a Sanskrit letter; the same word in 1.6.2–1.7.4 is अध्यूढं |
| 1.6.4 | नक्षत्रान्येवर्क् | नक्षत्राण्येवर्क् | ṇatva: नक्षत्राणि, as in the same mantra |
| 1.6.6 | आप्रणस्वात् | आप्रणखात् | a non-word: आ प्रणखात्, “to the tips of the nails” (ख typed as स्व) |
| 1.7.7 | स एष चामुष्मात् | स एष ये चामुष्मात् | a dropped ये: the relative is needed for लोकास्तांश्च, as in the parallel 1.6.8 |
| 1.8.2 | प्रावहणो | प्रवाहणो | the name is प्रवाहण, as in 1.8.1 and 1.8.8 |
| 1.9.1 | ज्यायानकाशः | ज्यायानाकाशः | आकाश lost its long ā; the same mantra has आकाशो, आकाशादेव |
| 1.11.9 | भूतन्यन्नमेव | भूतान्यन्नमेव | a dropped ā: भूतानि, as in 1.11.5 and 1.11.7 |
| 1.12.5 | प्रजपतिः | प्रजापतिः | a non-word: प्रजापति |
| 1.13.1 | हाउकारः वायु | हाउकारो वायु | sandhi: -aḥ before a voiced consonant becomes -o |
| 1.13.2 | प्रजपतिर् | प्रजापतिर् | a non-word: प्रजापति |
| 2.1.2 | साधुनैनमुपगादित्येव | साधुनैनमुपागादित्येव | a dropped ā: the same mantra reads उपागात् three times |
| 2.5.1 | हिंकारः ग्रीष्मः | हिंकारो ग्रीष्मः | sandhi: -aḥ before ग् becomes -o, as in the parallel 2.16.1 |
| 2.8.1 | सप्तविध्ं | सप्तविधं | a stray virama under ध |
| 2.10.6 | आप्नोती हादित्यस्य | आप्नोति हादित्यस्य | wrong vowel length: आप्नोति, as in 2.10.5 |
| 2.15.2 | सुरूपंश्च | सुरूपांश्च | accusative plural सुरूपान्, beside विरूपांश्च |
| 2.19.1 | द्गीथोस्थि | द्गीथोऽस्थि | a missing avagraha: उद्गीथोऽस्थि, as उद्गीथोऽग्निः, उद्गीथोऽश्वाः |
| 2.21.3 | त्रीणी त्रीणि | त्रीणि त्रीणि | a non-form: त्रीणि त्रीणि (“three each”) |
| 2.23.2 | सम्प्रास्र्वन्त | सम्प्रास्रवन्त | a dropped a: सम्प्रास्रवन्त, as सम्प्रास्रवत् in the same mantra |
| 2.24.3 | गार्हपत्यस्योदाङ्मुख | गार्हपत्यस्योदङ्मुख | the word is उदङ्मुख, as in the parallels 2.24.7 and 2.24.11 |
| 3.2.1 | ता अमृत आपः | ता अमृता आपः | agreement: अमृताः with आपः, as in the parallels 3.1.2, 3.3.1, 3.4.1 |
| 3.2.2 | रसोजायत | रसोऽजायत | a missing avagraha: रसोऽजायत, as in the parallels |
| 3.4.2 | तिहासपूराण | तिहासपुराण | a non-word: पुराण |
| 3.4.2 | भ्यतपं स्तस्या | भ्यतपंस्तस्या | a word split by a space, as in 3.5.2 |
| 3.4.2 | तेज इन्द्रियां | तेज इन्द्रियं | इन्द्रियं, as in the parallels 3.1.3, 3.2.2, 3.3.3, 3.5.3 |
| 3.5.2 | भ्यतपं स्तस्या | भ्यतपंस्तस्या | a word split by a space: अभ्यतपन्, written अभ्यतपंस्तस्या… in 3.1.3 and 3.3.2 |
| 3.6.3 | स य एतदेव रूपमभि | स एतदेव रूपमभि | an extra य: the parallels 3.7.3–3.10.3 read स एतदेव रूपम् |
| 3.9.4 | धिपत्य्ं | धिपत्यं | a stray virama before the anusvāra |
| 3.12.1 | वा ईदं | वा इदं | a non-word: इदं |
| 3.12.7 | तद्योयं | तद्योऽयं | a missing avagraha: योऽयम्, as in 3.12.8 and 3.12.9 |
| 3.12.8 | पुरुष अकाशो | पुरुष आकाशो | आकाश lost its long ā; the same mantra has आकाशः |
| 3.13.8 | यत्रितदस्मिञ् | यत्रैतदस्मिञ् | sandhi: यत्र + एतत् is यत्रैतत्, as in the same mantra |
| 3.14.2 | मभ्यत्तोऽवाक्य | मभ्यात्तोऽवाक्य | अभि + आत्तः is अभ्यात्तः, as in 3.14.4 |
| 3.16.6 | प्राणा अदित्या | प्राणा आदित्या | wrong vowel length: आदित्याः, as आदित्यानां in the same mantra |
| 3.17.6 | घोर् आङ्गिरसः | घोर आङ्गिरसः | sandhi: घोरः before a vowel is घोर, never घोर् |
| 3.18.2 | पादा अदित्यः | पाद आदित्यः | sandhi: पादः + आदित्यः is पाद आदित्यः (the page moved the ā of आदित्य onto पाद) |
| 3.18.4 | तपति च् भाति | तपति च भाति | a stray virama under च |
| 3.19.2 | समेघो | स मेघो | a missing space: स मेघो, as स समुद्रः in the same list |
| 4.1.2 | हं सोहं समभ्युवाद | हंसो हंसमभ्युवाद | two broken words: “a swan spoke to a swan” (हंसो हंसम्), after हंसा निशायामतिपेतुः |
| 4.1.2 | प्रसाङ्क्षी स्तत्त्वा | प्रसाङ्क्षीस्तत्त्वा | a word split by a space: प्रसाङ्क्षीः |
| 4.3.8 | तस्म उ ह | तस्मा उ ह | sandhi: तस्मै before उ is तस्मा उ |
| 4.4.4 | परिचरिणी | परिचारिणी | परिचारिणी, as in 4.4.2 |
| 4.6.1 | ग आभिप्रस्थापयांचकार | गा अभिप्रस्थापयांचकार | गाः before a vowel is गा; the parallels 4.7.1 and 4.8.1 read गा अभिप्रस्थापयांचकार |
| 4.8.4 | स यै एतमेवं | स य एतमेवं | a non-word यै: the parallels 4.5.3, 4.6.4, 4.7.4 read स य एतमेवं |
| 4.9.1 | हाचर्यकुलं | हाचार्यकुलं | a non-word: आचार्यकुलं, as in 4.5.1 |
| 4.9.1 | तमाचर्योऽभ्युवाद | तमाचार्योऽभ्युवाद | a non-word: आचार्यो, as in 4.14.1 |
| 4.10.1 | ब्रह्मचार्यमुवास | ब्रह्मचर्यमुवास | ब्रह्मचर्यम् उवास, “lived as a student” |
| 4.10.1 | वार्षाण्य | वर्षाण्य | a non-word: वर्षाणि |
| 4.10.3 | व्याधीभिः | व्याधिभिः | व्याधि is a short-i stem: व्याधिभिः |
| 4.13.2 | सर्वमयुरेति | सर्वमायुरेति | a dropped ā: सर्वमायुरेति, as in every parallel |
| 4.16.1 | पवते एष | पवत एष | sandhi: -e before a vowel becomes -a |
| 4.16.2 | यत्रौपाकृते | यत्रोपाकृते | sandhi: यत्र + उपाकृते is यत्रोपाकृते, as in 4.16.4 |
| 4.17.1 | न्तरिक्षातादित्यं | न्तरिक्षादादित्यं | sandhi: the ablative’s -t before a vowel is -d |
| 5.3.4 | किमनुशिष्ठोऽवोचथा | किमनुशिष्टोऽवोचथा | अनुशिष्ट, as सोऽनुशिष्टो in the same mantra |
| 5.4.1 | इति तृतीयः खण्डः ॥ असौ | असौ | the page puts the closing line of khaṇḍa 5.3 at the start of 5.4.1; it is left out like every other closing line |
| 5.4.2 | तस्या अहुतेः | तस्या आहुतेः | आहुति, as in the parallels 5.5.2, 5.6.2, 5.8.2 |
| 5.12.2 | मूधा त्वेष | मूर्धा त्वेष | a dropped reph: मूर्धा, as मूर्धा ते in the same mantra |
| 5.15.1 | त्वमात्मानमुपस्से | त्वमात्मानमुपास्से | a non-form: उपास्से (upa-ās), as in 5.12.1–5.16.1 |
| 5.17.1 | त्वमात्मानमुपस्स इति | त्वमात्मानमुपास्स इति | a non-form: उपास्स इति, as in 5.12.1–5.16.1 |
| 5.23.2 | ब्रह्मवर्चसेन ॥ | ब्रह्मवर्चसेनेति ॥ | a dropped इति: every parallel (5.19.2–5.22.2) ends ब्रह्मवर्चसेनेति |
| 5.24.1 | इदमविद्वाग्निहोत्रं | इदमविद्वानग्निहोत्रं | a dropped न: अविद्वान्, set against विद्वानग्निहोत्रं in 5.24.2 |
| 6.1.3 | प्राक्ष्यः येनाश्रुतं | प्राक्ष्यो येनाश्रुतं | sandhi: -aḥ before a voiced consonant becomes -o |
| 6.1.6 | सोम्यिकेन | सोम्यैकेन | a non-word: सोम्य + एकेन is सोम्यैकेन, as in 6.1.4 and 6.1.5 |
| 6.4.3 | यच्छन्द्रमसो | यच्चन्द्रमसो | तत् + चन्द्रमसः is यच्चन्द्रमसो (च्च, not च्छ) |
| 6.5.4 | सोम्य मनः आपोमयः | सोम्य मन आपोमयः | sandhi: -aḥ before आ becomes -a, as in 6.6.5 and 6.7.6 |
| 6.6.1 | स उर्ध्वः | स ऊर्ध्वः | a non-word: ऊर्ध्वः |
| 6.6.2 | स उर्ध्वः | स ऊर्ध्वः | a non-word: ऊर्ध्वः |
| 6.6.3 | स उर्ध्वः | स ऊर्ध्वः | a non-word: ऊर्ध्वः |
| 6.6.3 | सा प्राणो भवति | स प्राणो भवति | agreement: प्राण is masculine (स प्राणो); 6.6.4 rightly has सा वाग् |
| 6.6.4 | स उर्ध्वः | स ऊर्ध्वः | a non-word: ऊर्ध्वः |
| 6.7.2 | पञ्चदशाहानि नशाथ | पञ्चदशाहानि नाशाथ | sandhi: न + आश is नाश |
| 6.7.3 | महतोऽभ्या हितस्यैको | महतोऽभ्याहितस्यैको | a word split by a space: अभ्याहितस्य, as in 6.7.5 |
| 6.7.4 | स हशाथ | स हाशाथ | sandhi: ह + आश is हाश |
| 6.8.3 | तत्रितच्छुङ्गमु | तत्रैतच्छुङ्गमु | sandhi: तत्र + एतत् is तत्रैतत्, as तत्रैतदेव in 6.8.5 |
| 6.8.6 | न्यत्राद्भ्य्ऽद्भिः | न्यत्राद्भ्योऽद्भिः | a stray virama: अद्भ्यः + अद्भिः is अद्भ्योऽद्भिः |
| 6.9.3 | त इह व्यघ्रो | त इह व्याघ्रो | a non-word: व्याघ्रो, as in 6.10.2 |
| 6.11.3 | म्रियते इति | म्रियत इति | sandhi: -e before a vowel becomes -a |
| 6.12.3 | दद्ं सर्वं | दं सर्वं | a stray द्: इदं सर्वं, as in every other refrain |
| 6.16.2 | भवति ततेव | भवति तत एव | a broken word: तत एव, as in 6.16.1 |
| 6.16.2 | प्रतिगृह्णाति सन दह्यते | प्रतिगृह्णाति स न दह्यते | a missing space that makes another word: स न दह्यते, “he is not burned”, against स दह्यते in 6.16.1 |
| 7.2.1 | क्षत्रविद्यां सर्पदेवजनविद्यां | क्षत्रविद्यां नक्षत्रविद्यां सर्पदेवजनविद्यां | a dropped word: the same list in 7.1.2 and 7.7.1 has नक्षत्रविद्यां between क्षत्रविद्यां and सर्पदेवजनविद्यां |
| 7.12.2 | भूय इति आकाशाद्वाव | भूय इत्याकाशाद्वाव | sandhi: इति + आ is इत्या, as in the parallel lines |
| 7.24.1 | तन्मर्त्य्ं | तन्मर्त्यं | a stray virama before the anusvāra |
| 8.1.3 | न्तर्हृदय अकाश | न्तर्हृदय आकाश | आकाश lost its long ā; the same mantra has अयमाकाशः |
| 8.1.5 | स ब्रूयात्नास्य | स ब्रूयान्नास्य | sandhi: -t before a nasal becomes -n |
| 8.1.5 | ब्रह्मपुरमस्मिकामाः | ब्रह्मपुरमस्मिन्कामाः | a dropped न्: अस्मिन् |
| 8.1.6 | तद्य इहात्मानमनुविद्य | तद्य इहात्मानमननुविद्य | the sense: this clause ends in अकामचारो, so it speaks of those who go without knowing the Self (अननुविद्य); the next, ending in कामचारो, has अनुविद्य |
| 8.1.6 | मनिवुद्य | मनुविद्य | a non-word, letters transposed: अनुविद्य |
| 8.1.6 | व्रजन्त्येतंश्च | व्रजन्त्येतांश्च | accusative plural एतान्, written एतांश्च earlier in the same mantra |
| 8.5.2 | तब्ब्रह्मचर्येण | तद्ब्रह्मचर्येण | तद् + ब्रह्म is तद्ब्रह्म, as earlier in the same mantra (the transliteration has the same slip) |
| 8.5.2 | मनुते ऽ ॥ | मनुते ॥ | a stray avagraha at the end (not in the transliteration) |
| 8.5.4 | एवैतवरं | एवैतावरं | sandhi: एतौ + अरं is एतावरं |
| 8.6.3 | समस्त्ः | समस्तः | a stray virama: समस्तः, as in 8.11.1 |
| 8.12.5 | सात्मा मनोऽस्य | स आत्मा मनोऽस्य | sandhi: सः before a vowel is स (स आत्मा), as three times in 8.12.4 |
| 8.12.6 | प्र्जापतिरुवाच | प्रजापतिरुवाच | a stray virama under प |
| 8.15.1 | तधैतद्ब्रह्मा प्रजापतयै उवाच | तद्धैतद्ब्रह्मा प्रजापतय उवाच | two slips: तद्ध (तत् + ह), and the dative प्रजापतये, which before a vowel is प्रजापतय |
| 8.15.1 | प्रजाभ्यः आचार्यकुलाद् | प्रजाभ्य आचार्यकुलाद् | sandhi: -aḥ before a vowel becomes -a |
| 8.15.1 | धर्मिकान्विदधदा | धार्मिकान्विदधदा | the adjective is धार्मिक (vṛddhi) |
| 8.15.1 | सर्वैन्द्रियाणि | सर्वेन्द्रियाणि | sandhi: सर्व + इन्द्रियाणि is सर्वेन्द्रियाणि |

## Numbering: the text and each witness
The text has the śānti and **629 mantras**; upanishads.org.in has the same 629 in the same places, and so do the other witnesses once their own ways of dividing are read as below. `check.py` compares each khaṇḍa as one run of letters, so a witness that divides a khaṇḍa otherwise is still compared word for word.

- **3.17.7.** The page writes, after आदित्प्रत्नस्य रेतसः, the rest of that ṛc (ज्योतिः पश्यन्ति वासरम्; परो यदिध्यते दिवि) and then numbers the next ṛc's words (उद्वयं तमसस्परि …) 3.17.8. No witness has the added half-verse, Wikisource neither, and every witness has one mantra, 3.17.7, running आदित्प्रत्नस्य रेतसः । उद्वयं तमसस्परि … ज्योतिरुत्तममिति: the half-verse is left out and the two are one mantra (`settle.py` → `BLOCK_FIX`). Item `3.17.8` is gone; khaṇḍa 3.17 has 7 mantras, adhyāya 3 has 95.
- **6.6** has 5 mantras in every witness (the page's “६.६.६” is 6.6.5, above).
- **IIT Kanpur** lists 632 refs and has text for 621: khaṇḍa 4.3 (4.3.1–8) is empty, and 6.13 has three empty refs after 6.13.3 (6.13.4–6), so its 6.13 is the text's 3 mantras. It also files mantras under the number before their own, so two refs hold the same text and a mantra is missing: 1.3.7 holds 1.3.8, likewise 1.4.2, 1.6.4, 1.7.4, 1.7.6, 1.8.4, 1.9.1, 1.10.1, 1.12.2, 1.12.4, 2.22.1, 2.24.4, 3.13.5, 3.18.1, 3.18.3, 4.1.7, 4.8.2, 4.16.1, 5.24.4, 6.2.1, 6.4.3, 6.11.2, 7.2.1, 7.13.1, 7.15.3; and 4.4.1 holds 4.4.2's text and 4.4.2 4.4.3's, 5.1.7 holds 5.1.8 and 5.1.8 5.1.9, 7.3.2 holds 7.4.1, 7.10.1 holds 7.10.2 and 7.10.2 7.11.1. `witnesses.py` leaves out the earlier copy of each pair (29 refs, 592 mantras kept) and `check.py` → `LACKS` skips the 29 mantras of ours whose text IIT Kanpur does not have; within 4.7.1 and 4.7.4 it moves a sentence (recorded as its readings). So IIT Kanpur's 629 = 632 refs − 3 empty in 6.13, with 4.3 and those 29 mantras not in it.
- **GRETIL** marks 623 mantras: in 3.13, 3.15, 6.2 and 8.3 one of its refs covers two of ours, and in 4.7 one covers three; it also abbreviates repeated passages (2.1.2, 3.15.5, 4.7.1–2, 5.24.5, 6.2.4, 8.3.5), each recorded as an omission of the witness. upanishads.org.in divides as the text does, with GRETIL's omissions.
- **Wikisource** has 631 numbers: its 4.15 has 6 and its 5.2 has 9 (it numbers within a mantra), and its 2.3.1 is in a different order; the letters are the text's.

## Corrections from the witnesses (`source/settle.py` → `WITNESS_FIX`, `BLOCK_FIX`)

| Item | The page | The text | Witnesses | Why |
|---|---|---|---|---|
| 1.1.2 | पृथिव्या अपो रसः | पृथिव्या आपो रसः | IITK, GRETIL (and upanishads.org.in) आपो; Wikisource अपो | the nominative āpaḥ, “water is the essence of earth”; अपः is accusative |
| 1.2.6 | तेनोभयंसंकल्पते | तेनोभयंसंकल्पयते | IITK सङ्कलप्यते (for सङ्कल्पयते), GRETIL संकल्पयते; Wikisource संकल्पते | it takes the object उभयं (“thinks both”), as जिघ्रति, वदति, पश्यति, शृणोति in 1.2.2–5: the causative, not the intransitive middle |
| 1.2.9 | ऽवित्त्वोत्क्रमति | ऽवित्त्वोत्क्रामति | IITK, GRETIL उत्क्रामति; Wikisource उत्क्रमति | √kram lengthens in the active present (Pāṇini 7.3.76): क्रामति |
| 1.8.5, 1.8.7 | लोकमिति नयेदिति | लोकमतिनयेदिति | all four (Wikisource लोकमति नयेदिति) | “one should not lead (the sāman) beyond the heavenly world”: अति-नयेत्; इति there is no sense |
| 2.1.4 | विद्वानसाधु | विद्वान्साधु | IITK, GRETIL विद्वान्साधु; Wikisource विद्वानसाधु | “knowing this, meditates on the sāman as good (साधु)”: असाधु reverses the sense of the khaṇḍa |
| 2.11.2 | स एवमेतद्गायत्रं | स य एवमेतद्गायत्रं | GRETIL स य एवम्, IITK स वमेतद्; Wikisource स एवमेतद् | the relative for वेद, as in every parallel (2.12.2–2.20.2: स य एवमेतद्) |
| 2.20.2 | सलोकतांसर्ष्टितां | सलोकतांसार्ष्टितां | IITK साष्र्टिताँ (its way of typing सार्ष्टिताँ); GRETIL and Wikisource सर्ष्टितां | सार्ष्टिता, “equality of rank”, beside सलोकता and सायुज्य; सर्ष्टिता is no word |
| 2.21.4 | सर्वमस्मीत्युपासित | सर्वमस्मीत्युपासीत | IITK उपासीत; GRETIL and Wikisource उपासित | the optative “let him meditate”, as उपासीत throughout; उपासित is no form of upa-√ās |
| 3.17.7–8 | रेतसः ज्योतिः पश्यन्ति वासरम्; परो यदिध्यते दिवि ॥ ३.१७.७ ॥ उद्वयं | रेतसः । उद्वयं | all four | the page adds the rest of the ṛc; one mantra (“Numbering”) |
| 4.4.2 | जाबालो ब्रवीथा | जाबालो ब्रुवीथा | GRETIL ब्रुवीथा (IITK lacks the mantra); Wikisource ब्रवीथा | the optative middle of √brū is ब्रुवीथाः; ब्रवीथाः is no form |
| 4.16.2 | ब्रह्मा व्यवदति | ब्रह्मा व्यववदति | IITK, GRETIL व्यववदति; Wikisource व्यवदति | vi-ava-√vad, “breaks the silence”; व्यवदति is no form of it |
| 4.16.4 | ब्रह्मा व्यवदत्युभे | ब्रह्मा व्यववदत्युभे | IITK, GRETIL; Wikisource व्यवदत्युभे | the same verb, as 4.16.2 |
| 5.11.5 | न कर्दर्यो | न कदर्यो | IITK, GRETIL कदर्यो; Wikisource कर्दर्यो | कदर्य, “a miser”; कर्दर्य is no word |
| 5.13.2 | चक्षुषेतदात्मन | चक्षुष्ट्वेतदात्मन | IITK चक्षुष्ट्वेतदात्मन, GRETIL चक्षुष् ट्व् एतद्; Wikisource चक्षुषेतदात्मन | “this is but the eye of the Self”: चक्षुस्तु एतत्, as मूर्धा त्वेष (5.12.2), प्राणस्त्वेष (5.14.2), पादौ त्वेतौ (5.17.2) |
| 7.6.1 | ध्यायन्तीव पर्वता देवमनुष्या | ध्यायन्तीव पर्वता ध्यायन्तीव देवमनुष्या | IITK, GRETIL; Wikisource lacks it | a dropped word: every member of the list has its own ध्यायतीव / ध्यायन्तीव |
| 7.15.1 | प्राणो वा आशाया | प्राणो वाव आशाया | IITK, GRETIL वाव; Wikisource वा | the formula of 7.2–7.14, “X वाव Y-आद्भूयः”: वा (“or”) breaks it |
| 7.26.2 | विंशतिराहारशुद्धौ सत्त्वशुद्धौ | विंशतिराहारशुद्धौ सत्त्वशुद्धिः सत्त्वशुद्धौ | IITK, GRETIL; Wikisource lacks it | a dropped word: “when food is pure, the being is pure; when the being is pure, memory is firm” |
| 8.5.3 | ब्रह्मचर्यमेव तदरश्च | ब्रह्मचर्यमेव तत्तदरश्च | IITK तत्तदरश्च, GRETIL तत् तद् अरश् च; Wikisource तदरश्च | a dropped word: each clause of 8.5.1–3 ends ब्रह्मचर्यमेव तत्, and the next sentence begins तद् |
| 8.7.3 | किमिच्छन्तावास्तमिति | किमिच्छन्ताववास्तमिति | IITK, GRETIL अवास्तम्; Wikisource as the page | “wishing what have you two lived (here)?”: अवास्तम्, as तमिच्छन्ताववास्तमिति at the end of the same mantra |

## Readings of the page kept against witnesses
Each is a valid reading, so it stays (§2 of the playbook):
- **1.2.9 प्राणानवति एतमु**: all four witnesses keep अवति and एतमु apart; a sentence ends after अवति (GRETIL prints the daṇḍa), so there is no sandhi.
- **1.11.2 अहमवित्त्यान्यानवृषि**: all four read अवित्त्या, the instrumental of अवित्ति, “for want of finding (you), I chose others”.
- **4.1.2 अथ हंसा** (IITK and GRETIL अथ ह हंसा): ह is a particle; the sentence is whole without it.
- **4.2.5 उवास स तस्मै होवाच** (IITK, GRETIL उवास तस्मै): the pronoun is grammatical.
- **4.17.5 स यदि यजुष्टो** (IITK, GRETIL अथ यदि): “he, if …”, grammatical.
- **5.2.8 स्वप्नेषु पश्यन्ति** (IITK, GRETIL पश्यति): a valid plural, “(people) see”.
- **5.5.1 अङ्गाराह्रादनयो** (GRETIL ह्रादुनयो; IITK हादनयो, with the page): ह्रादन, “roaring, thunder”, is a word and IIT Kanpur shares it.
- **6.4.7 यथा तु खलु** (GRETIL and Wikisource नु, IITK खलु नु) and **6.8.6 यथा तु खलु** (IITK तु, with the page): both particles are valid.
- **7.4.3 संकॢप्तान्वै** (IITK, GRETIL कॢप्तान्): a valid word, as संकल्प in the same mantra.
- **3.16.7 न प्रेष्यामीति** (IITK प्रेष्यामिति, GRETIL प्रेष्याम् इति): प्रेष्यामि + इति; the witnesses' form is no word.
- **8.12.4 शृणवानीति** (GRETIL शृण्वानीति): शृणवानि is the imperative of √śru.
- Readings the page and every witness share stay, though a word writer asked: **6.7.6 प्राज्वाली** (all four).

## The witnesses' own readings (`source/witness-readings.tsv`)
Every other difference is a witness's own reading, where the text follows the page and at least one other witness; each is one line of `source/witness-readings.tsv` (witness, our item, the witness's letters, ours, kind), which `check.py` applies and requires to be found. Kinds: `own` (the witness's slip or variant: IIT Kanpur 453, GRETIL 129, upanishads.org.in 129, Wikisource 29), `page` (the witness has the page's reading, which the text corrects: Wikisource 57, GRETIL 20, upanishads.org.in 20), `omits` / `adds` (a passage the witness leaves out or adds: GRETIL's abbreviations, IIT Kanpur's moved sentences in 4.7, Wikisource's order in 2.3.1 and its note “रथन्तरोपरिटिप्पणी” in 2.12.2). The lines are made by `check.py --write` only after each difference has been reviewed. `check.py` then finds **no unexplained difference** with any witness.

## The page's Devanagari against its transliteration

| Block | Devanagari | Transliteration | Text |
|---|---|---|---|
| 8.5.2 | …मनुते ऽ॥ | …manute, with no avagraha | मनुते ॥ (the stray avagraha is a slip; above) |
