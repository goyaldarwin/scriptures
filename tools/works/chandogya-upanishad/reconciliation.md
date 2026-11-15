# Chāndogya Upaniṣad — how the text is settled

**Base:** <https://shlokam.org/text/chandogya-upanishad.htm>, fetched on 2026-11-14 (private copy in scriptures-data at `hinduism/veda/samaveda/upanishad/chandogya-upanishad/printouts/shlokam/chandogya-upanishad.html`). It gives the Sāmaveda śānti mantra and the eight adhyāyas in 621 blocks of Devanagari, each with the page's own transliteration; there are no svara marks.

## Witnesses
- **The page's transliteration.** `source/settle.py` reads it back into Devanagari and compares it with the page's Devanagari, block by block. They agree everywhere but one place (8.5.2, below) and the page's ways of writing one sound twice (the candrabindu of अस्मिँल्लोके, which the transliteration writes m̐). They share most slips (निराकरणंं / nirākaraṇaṃṃ, तब्ब्रह्म / tabbrahma, the ; of 3.17.7): the transliteration is the page's own copy of its Devanagari, so it confirms what the page has, not what is right.
- **The text's own parallels and the grammar.** The Chāndogya repeats its formulas many times (the honey teaching's five directions, the Vaiśvānara's six questions, the tat tvam asi refrain, Nārada's list of learning). Each mantra was read against its parallels and against sandhi and the forms of the words; a place the page writes in a way that is no word, breaks the sandhi it keeps everywhere else, or departs from its own formula by a dropped or extra letter or word, is corrected (below). A valid reading the page has is kept.
- **sanskritdocuments.org.** The owner's printout of its Chāndogya is to be added to scriptures-data as the second written witness; its text then goes in `source/witness/` and every mantra is compared with it word by word, the way the Kaṭha's are (`tools/works/katha-upanishad/source/check.py`).

## Structure
- **Blocks and mantras.** Nine blocks hold more than one mantra (2.13.1–2, 3.12.7–9, 3.17.7–8, 4.1.5–6, 4.16.2–3, 5.8.1–2, 5.10.1–2, 6.11.1–2, 6.13.1–2): they are split at the page's ॥ a.k.m ॥ marks. Every khaṇḍa then runs 1 … N without a gap, every adhyāya's khaṇḍas run 1 … N, and `settle.py` checks it.
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
| 1.2.9 | प्राणानवति एतमु | प्राणानवत्येतमु | sandhi: -i before a vowel becomes -y |
| 1.6.1 | च्यध्यूढ़ं साम | च्यध्यूढं साम | ढ़ with a nukta is not a Sanskrit letter; the same word in 1.6.2–1.7.4 is अध्यूढं |
| 1.6.4 | नक्षत्रान्येवर्क् | नक्षत्राण्येवर्क् | ṇatva: नक्षत्राणि, as in the same mantra |
| 1.6.6 | आप्रणस्वात् | आप्रणखात् | a non-word: आ प्रणखात्, “to the tips of the nails” (ख typed as स्व) |
| 1.7.7 | स एष चामुष्मात् | स एष ये चामुष्मात् | a dropped ये: the relative is needed for लोकास्तांश्च, as in the parallel 1.6.8 |
| 1.8.2 | प्रावहणो | प्रवाहणो | the name is प्रवाहण, as in 1.8.1 and 1.8.8 |
| 1.9.1 | ज्यायानकाशः | ज्यायानाकाशः | आकाश lost its long ā; the same mantra has आकाशो, आकाशादेव |
| 1.11.2 | अहमवित्त्यान्यान | अहमवित्त्वान्यान | a non-word: the gerund अवित्त्वा, as अवित्त्वोत्क्रमति in 1.2.9 |
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
| 3.17.7 | वासरम्; परो | वासरम् । परो | a stray semicolon (in both scripts) where the quoted ṛc’s half-verse ends, after its second pāda: a daṇḍa |
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

## The page's Devanagari against its transliteration

| Block | Devanagari | Transliteration | Text |
|---|---|---|---|
| 8.5.2 | …मनुते ऽ॥ | …manute, with no avagraha | मनुते ॥ (the stray avagraha is a slip; above) |
