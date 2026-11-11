# Reconciliation: Śrī Durgā Saptaśatī

The base is the owner's copy of sanskritdocuments.org's text (`README.md`). The witness is the owner's Gita Press book (code 118), whose 700 mantras `source/gitapress.py` reads from the PDF's text layer and `source/compare.py` compares with the base word for word, after spacing, punctuation, the avagraha, footnote marks, the closing bījas and the nasal spelling are set aside: 83 mantras differ (`source/witness/differences.json`), and each is decided below. The base is corrected only where its reading is clearly an error (a word that does not exist, a broken form or sandhi, a space inside a word or a missing one); a reading of its own edition stays (`docs/PLAYBOOK.md` §2). The data is in `source/corrections.json` and the rules in `source/make_text.py`.

## The copy's layout, read as the book prints it
- **Order.** The copy's nineteen sections are the work's parts in the copy's order, which is the order the recording sings them (the Caṇḍikā-dhyāna, Argalā, Kīlaka, Kavaca, the 13 adhyāyas, the Aparādha-kṣamāpaṇa stotra, the Devī Sūkta). Gita Press orders the stotras Kavaca, Argalā, Kīlaka and adds others the copy and the recording do not have (the Rātri Sūktas, Devyatharvaśīrṣa, the Navārṇa-vidhi, the three Rahasyas, the Siddha-kuñjikā); they are not in this work.
- **Numbers.** Each numbered item's last line ends with its number (॥१॥), which the copy leaves out. The 700 mantras are numbered as Gita Press numbers them, and as the copy's own numbers and each adhyāya's tally count them: each speaker's line (ॐ ऐं मार्कण्डेय उवाच ॥१॥, ऋषिरुवाच ॥) is a mantra, and so is each part of the triple namaskāras of adhyāya 5. The copy gives each of those stanzas as one item numbered 14-16, 17-19 … 78-80; here they are three mantras each, as the book prints them (या देवी सर्वभूतेषु विष्णुमायेति शब्दिता । नमस्तस्यै ॥१४॥, नमस्तस्यै ॥१५॥, नमस्तस्यै नमो नमः ॥१६॥), so that adhyāya 5 has 129 mantras and the thirteen 700, and a reader can find every mantra by its number. The meaning of the stanza is given piece by piece (`source/meanings.py`) and Pargiter's, written for the stanza, sits under its last mantra, as the Mānas's joint meanings do.
- **Speakers.** In the adhyāyas the speaker's line is a mantra of its own, as in the copy. A stotra that opens with मार्कण्डेय उवाच (Argalā, Kīlaka, Kavaca) has it as the first line of its first verse, as Gita Press prints it above the verse; the copy gives it as a field of the verse.
- **Closing bījas.** The copy prints । ऐं ॐ । after adhyāya 1 and । ह्रीं ॐ । after adhyāya 4; they are written at the end of the last mantra (॥ ऐं ॐ ॥१०४॥), as Gita Press prints them. Gita Press also closes every other adhyāya with ॐ; the copy does not, and its text stays. Adhyāya 13 ends with the copy's repeat of mantras 28–29 with क्लीं ॐ (`13.end`).
- **Colophons.** Each section's स्वस्ति … / इति … is its last item (`<section>.iti`), ending ॥N॥ for an adhyāya, without the copy's opening ॥.
- **Left out, not being the text:** the copy's header lines (॥ देवी माहात्म्यम् ॥, ॥ श्री ॥, ॥ श्रीदुर्गायै नमः ॥, ॥ अथ श्रीदुर्गासप्तशती ॥, ॥ श्रीसप्तशतीदेवीमाहात्म्यं समाप्तम् ॥, ॥ ॐ तत् सत् ॐ ॥), the word अथवा before the alternative dhyāna (`dhyana.4`), and each adhyāya's tally of its mantras (उवाच १४, अर्धश्लोकाः २४, श्लोकाः ६६, एवमादितः ॥१०४॥).
- **Characters.** Runs of spaces are one space; र + ृ is written र्ऋ (नैर्ऋत्यै, विष्णुर्ऋषिः, असिभिर्ऋष्टिभिः), as Unicode spells r + ṛ; the text is NFC.

## Corrections
| Item | The copy | Here | Why |
|---|---|---|---|
| 1.104 | वदामि ते ॥ | वदामि ते ॥ ऐं ॐ ॥ | the closing bīja, which the copy prints as a line of its own after the adhyāya (। ऐं ॐ ।), written at the end of the last mantra as Gita Press prints it (॥ ऐंॐ॥ १०४॥) |
| 3.4 | तस्य छित्वा | तस्य च्छित्त्वा | छित्त्वा, the absolutive of छिद्, with the doubled च्छ after the short vowel (Gita Press: तस्यच्छित्त्वा); छित्वा is a slip |
| 3.5 | चातिसमुच्छृतम् | चातिसमुच्छ्रितम् | समुच्छ्रित (उत् + श्रि, "raised high"); समुच्छृत is not a word (Gita Press: समुच्छ्रितम्) |
| 4.9 | महाव्रता त्वं | महाव्रता त्व- | a word-final m before a vowel is joined to it (त्वमभ्यस्यसे, Gita Press's), written across the line with a hyphen as the copy itself does in 4.10 (निधान- / मुद्गीथ…) |
| 4.9 | अभ्यस्यसे सुनियतेन्द्रिय | मभ्यस्यसे सुनियतेन्द्रिय | the same |
| 4.19 | तेष्वहितेषुसाध्वी | तेष्वहितेषु साध्वी | a missing space: साध्वी is a word of its own (the mind is kind, साध्वी, even towards the hostile) |
| 4.23 | भयमप्यपास्तम् | भयमप्यपास्त- | as 4.9 (अपास्तमस्माकम्, Gita Press's) |
| 4.23 | अस्माकमुन्मदसुरारिभवं | मस्माकमुन्मदसुरारिभवं | the same |
| 4.27 | चास्त्रानि | चास्त्राणि | न after र in the same word is ण (अस्त्राणि; Gita Press agrees) |
| 4.42 | कथयामि ते ॥ | कथयामि ते ॥ ह्रीं ॐ ॥ | the closing bīja, which the copy prints after the adhyāya (। ह्रीं ॐ ।), at the end of the last mantra as Gita Press prints it |
| 8.53 | प्राहसत्वरम् | प्राह सत्वरम् | a missing space: प्राह ("said") and सत्वरम् ("quickly") are two words |
| 8.55 | क्षेणरक्तो | क्षीणरक्तो | क्षीण ("drained"): with his blood drained the demon will perish; क्षेण is not a word (Gita Press: क्षीणरक्तो) |
| 9.15 | आविद्याथ | आविध्याथ | आविध्य, the absolutive of आ + व्यध् ("whirling" the mace); आविद्य is a slip (Gita Press: आविध्याथ) |
| 9.15 | देव्यास् त्रिशूलेन | देव्यास्त्रिशूलेन | a space inside the sandhi: देव्याः + त्रिशूलेन is देव्यास्त्रिशूलेन |
| 9.23 | वैः शब्दैरसुरा | तैः शब्दैरसुरा | तैः ("by those" cries); वैः is not a word (Gita Press: तैः) |
| 10.16 | अभ्यधा वत | अभ्यधावत | a space inside the word अभ्यधावत ("rushed at") |
| 12.10 | माहात्म्यम् उच्चार्यं | माहात्म्यमुच्चार्यं | a word-final m before a vowel is joined to it |
| 13.15 | ददामिते | ददामि ते | a missing space: ददामि ("I give") ते ("to you") |
| kavacha.47 | तत्रार्थलाभश्व | तत्रार्थलाभश्च | च ("and"); श्व is a slip (Gita Press: तत्रार्थलाभश्च) |
| 2 dhyāna | अक्षस्रक्परशू | अक्षस्रक्परशुं | परशुम्, an accusative like every other weapon she holds (दधतीं); परशू is a slip (Gita Press: परशुं) |
| 7 dhyāna | मातङ्गी शङ्कपात्रां | मातङ्गीं शङ्खपात्रां | accusatives, the objects of ध्यायेयं (Gita Press: मातङ्गीं), and शङ्ख, the conch-shell cup; शङ्क is a slip |
| 12 dhyāna | करवाळखेटविलसधस्ताभि | करवालखेटविलसद्धस्ताभि | विलसत् + हस्त is विलसद्धस्त (the copy drops the द्), and करवाल is written with ल as everywhere else in the text (Gita Press: करवालखेटविलसद्धस्ताभि) |

## Readings where Gita Press differs and the base stays
Both are readings of the Devī Māhātmya's editions; the base's is good Sanskrit and fits the line, so it stays. Spelling differences alone (a sandhi written or not, ङ्ग printed by Gita Press as ङ्.ग, a footnote mark) are not listed.

| Mantra | Base | Gita Press | Note |
|---|---|---|---|
| 1.12 | ममत्वाकृष्टमानसः | ममत्वाकृष्टचेतनः |  |
| 1.13 | शूरो हस्ती | शूरहस्ती |  |
| 1.48 | विषयाश्च; यान्ति | विषयश्च; याति |  |
| 1.69 | तामेकाग्रहृदयः स्थितः | तामेकाग्रहृदयस्थितः |  |
| 1.78 | महेश्वरी | महासुरी |  |
| 1.80 | खड्गिनी | खङ्गिनी |  |
| 1.83 | मया | तदा |  |
| 1.98 | मया | मम |  |
| 1.103 | छिन्ने | च्छिन्ने |  |
| 2.19 | ततो देवा ददुस्तस्यै स्वानि स्वान्यायुधानि च | — | the copy prints a third line, ततो देवा ददुस्तस्यै स्वानि स्वान्यायुधानि च, which Gita Press does not; the copy's line stays |
| 2.20 | समुत्पाट्य | समुत्पाद्य |  |
| 2.22 | समुत्पाट्य | समुत्पाद्य |  |
| 2.24 | तस्यै चर्म | तस्याश्चर्म |  |
| 2.69 | तथासुरैः | महासुरैः |  |
| 3.10 | —; तच्छतधा; शूलं | तच्छूलं शतधा; —; — |  |
| 3.15 | युध्यमानौ | युद्ध्यमानौ |  |
| 3.18 | बाष्कलं | वाष्कलं |  |
| 3.41 | पदाक्रान्तस्तया निजमुखात्तदा | पदाऽऽक्रान्तस्तया निजमुखात्ततः |  |
| 4.6 | किञ्चातिवीर्यमसुरक्षयकारि; तवाति यानि | किं चातिवीर्यमसुरक्षयकारि; तवाद्भुतानि |  |
| 4.10 | देवि; वार्तासि | देवी; वार्ता च |  |
| 4.15 | बन्धुवर्गः | धर्मवर्गः |  |
| 4.19 | तेष्वहितेषु साध्वी | तेष्वपि तेऽतिसाध्वी |  |
| 4.26 | चात्यन्तघोराणि | चात्यर्थघोराणि |  |
| 4.30 | समस्तैस्त्रिदशैर्दिव्यैर्धूपैः सुधूपिता | समस्तैस्त्रिदशैर्दिव्यैर्धूपैस्तु धूपिता |  |
| 5.77 | व्याप्त्यै देव्यै | व्याप्तिदेव्यै |  |
| 5.84 | स्तवाभियुक्तानां | स्तवादियुक्तानां |  |
| 5.90 | सातीव | अतीव |  |
| 5.104 | —; च देवीं | सा देवी; — |  |
| 5.109 | हृतं | हृत्वा |  |
| 5.121 | महाबलः | महासुरः |  |
| 5.128 | निशुम्भश्चापितादृशः | निशुम्भश्चातिवीर्यवान् |  |
| 5.129 | यत् | तत् |  |
| 6.16 | आक्रान्त्या; —; स | आक्रम्य; स; — |  |
| 7.14 | ममर्दाभक्षयच्चान्यानन्यांश्चाताडयत्तदा | ममर्दाभक्षयच्चान्यानन्यांश्चाताडयत्तथा |  |
| 7.19 | काली करालवदना दुर्दर्शदशनोज्ज्वला | कालीकरालवक्त्रान्तर्दुर्दर्शदशनोज्ज्वला |  |
| 7.27 | देवी | देवि |  |
| 8.6 | मौर्वाः कालिकेयास्तथासुराः | मौर्याः कालकेयास्तथासुराः |  |
| 8.9 | तान्नादानम्बिका | तन्नादमम्बिका |  |
| 8.15 | शक्तिर्ब्रह्माणीत्यभिधीयते | शक्तिर्ब्रह्माणी साभिधीयते |  |
| 8.41 | तत्प्रमाणो महासुरः | तत्प्रमाणस्तदासुरः |  |
| 8.53 | सत्वरम् | सत्वरा |  |
| 9.15 | देव्यास्त्रिशूलेन | देव्या त्रिशूलेन | देव्यास्त्रिशूलेन ("with the trident of the Devī") is good Sanskrit; Gita Press has देव्या ("by the Devī") |
| 9.31 | देवी | तानि |  |
| 9.32 | दैत्यसैन्यसमावृतः | दैत्यसेनासमावृतः |  |
| 10.3 | बलावलेपदुष्टे; चातिमानिनी | बलावलेपाद्दुष्टे; यातिमानिनी |  |
| 10.11 | शस्त्रैस्तथा चास्त्रैः सुदारुणैः | शस्त्रैस्तथास्त्रैश्चैव दारुणैः |  |
| 10.16 | अभ्यधावत तां | अभ्यधावत्तदा |  |
| 10.17 | अश्वांश्च पातयामास रथं सारथिना सह | — | the copy prints a third line, अश्वांश्च पातयामास रथं सारथिना सह, which Gita Press does not; the copy's line stays |
| 10.24 | उत्पाट्य | उत्पात्य |  |
| 10.25 | वेगवान् | वेगितः |  |
| 11.7 | भुक्तिमुक्तिप्रदायिनी | स्वर्गमुक्ति प्रदायिनी |  |
| 11.10 | सर्वमङ्गलमाङ्गल्ये | सर्वमङ्गलमङ्गल्ये |  |
| 11.22 | महामाये | महाऽविद्ये |  |
| 11.25 | सर्वभूतेभ्यः | सर्वभीतिभ्यः |  |
| 11.33 | धारयसीह | धारयसीति |  |
| 11.43 | वैप्रचित्तांश्च | वैप्रचित्तांस्तु |  |
| 11.46 | संस्मृता | संस्तुता |  |
| 11.47 | निरीक्षिष्याम्यहं मुनीन् | निरीक्षिष्यामि यन्मुनीन् |  |
| 12.2 | शमयिष्याम्यसंशयम् | नाशयिष्याम्यसंशयम् |  |
| 12.6 | शत्रुभ्यो | शत्रुतो |  |
| 12.7 | महत् | हि तत् |  |
| 12.10 | ममैतन्माहात्म्यमुच्चार्यं | ममैतच्चरितमुच्चार्यं |  |
| 12.11 | यथा; प्रतीक्षिष्याम्यहं | तथा; प्रतीच्छिष्याम्यहं |  |
| 12.13 | सर्वाबाधाविनिर्मुक्तो धनधान्यसमन्वितः | सर्वाबाधा विनिर्मुक्तो धनधान्यसुतान्वितः |  |
| 12.22 | सकृदुच्चरिते | सकृत्सुचरिते |  |
| 12.25 | प्रयच्छन्तु | प्रयच्छन्ति |  |
| 12.33 | पश्यतां सर्वदेवानां | पश्यतामेव देवानां |  |
| 12.35 | जगद्विध्वंसके | जगद्विध्वंसिनि |  |
| 12.38 | महादेव्या महाकाली | महाकाल्या महाकाले | the copy's महादेव्या महाकाली (Mahākālī named beside the instrumental) is its edition's reading, as its IAST confirms; Gita Press has महाकाल्या महाकाले |
| 12.41 | पुष्पैर्गन्धधूपादिभिस्तथा | पुष्पैर्धूपगन्धादिभिस्तथा |  |
| 13.8 | संशितव्रतम् | शंसितव्रतम् |  |
| 13.9 | सन्दर्शनार्थमम्बाया नदीपुलिनमास्थितः | संदर्शनार्थमम्बाया नदीपुलिनसंस्थितः |  |
| 13.11 | यतात्मानौ | यताहारौ |  |
| 13.15 | ते | तत् |  |
| 13.23 | मनुर्नाम भवान्भुवि | नाम मनुर्भवान् भुवि |  |

## The stotras
The copy's Argalā (27 ślokas), Kīlaka (16) and Kavaca (61) are another recension than Gita Press's (24, 14 and 56, in another order), so they are not compared word for word. Their lines were read against Gita Press's where the two share them, and corrected only where the copy is clearly wrong (`kavacha.47` श्व for च, and the dhyānas of adhyāyas 2, 7 and 12, above).

## Readings of our meanings
Our meanings give the plain reading of the words as the recitation tradition takes it; a well-known second reading is a footnote. The places where the writers and checkers weighed two readings, and what was settled:

| Verse | Settled reading | Why |
|---|---|---|
| argala.1 | भूतापहारिणि: remover of the sufferings of beings | the recitation tradition's reading |
| argala.21 | सदा goes with संस्तुते, ever praised | the line's own order |
| kilaka.2 | सोऽपि … जप्यतत्परः: he too who is intent on recitation | the plain words; the commentators' 'one reciting other mantras' is an explanation, not the verse |
| kilaka.5 | निमन्त्रयामास: bound (kīlita) the hymn | the commentators, and the hymn's own name; 'summoned' (the dictionaries) in the footnote |
| kilaka.6, kilaka.8 | as the words say: one attains that binding; one gives and receives back | nothing added the verse does not say |
| kilaka.13 | उच्चकैः: in great measure | Monier-Williams; the soft-and-loud reading in the footnote |
| kavacha.5 | ब्रह्मणा: the Veda | Brahmā himself is the speaker of the kavaca (kavacha.2); 'by Brahmā' in the footnote |
| kavacha.24, kavacha.44, kavacha.46 | Trinetrā with the trident, Yamaghaṇṭā at the sides; Mahālakṣmī and Vijayā two goddesses; 'because of your devotion' | the words as they stand |
| 1.5 | Kolāvidhvaṃsin, a royal line | Monier-Williams |
| 1.22, 1.32 | deprived of wealth, wife and sons; the wife gave up love for husband and kin | विहीन with the instrumental; 1.31's santyajya continued |
| 1.45, 1.71 | each of us blind in discernment; Brahmā, the lord of radiance | the genitives as printed; प्रभुः nominative |
| 1.103, 1.104 | on his thigh; she herself came forth | जघने locative; स्वयम् with समुत्पन्ना |
| 2.42, 2.44 | five crore; five hundred crore chariots | niyuta a million (Monier-Williams); fifty ayutas of ayutas |
| 2.43 | Parivārita, the name of an asura | a second finite verb follows; 'surrounded' in the footnote |
| 2.60, 2.69, 3.22, 3.40 | swooping like hawks; the Devī and her attendants; one group lashed and torn; pressing his throat with her foot | the grammar of each line |
| 4.7, 4.11, 4.14, 4.37, 5.11 | as the words stand, the plain reading | no reading the grammar does not give |
| 5.41 | जाति: birth | Monier-Williams's first sense; जाति alone reads as caste in modern Hindi |
| 5.77, 5.82 | the senses of beings; two clauses about her, no verb supplied | the recitation tradition; the verse as it stands |
| 5.111, 5.129 | beings and things; with care | the list before it; Monier-Williams ādṛta |
| 6.dhyana | भैरवाङ्ग: Bhairava's body | the text as printed (some read अङ्क, lap) |
| 6.16 | अधरेण: with its lip | Monier-Williams and Apte adhara |
| 6.24 | अथ: or else | two alternatives |
| 7.17 | Caṇḍa with the arrows, Muṇḍa with the discuses | the recitation tradition; Caṇḍa has just rushed at her |
| 8.4, 8.5 | weapons raised; of boundless valour | the only senses Monier-Williams and Apte give; कोटिवीर्याणि agrees with कुलानि |
| 8.10, 8.32, 8.39, 8.54, 8.56 | as the words stand | the grammar of each line |
| 9.26, 9.30 | a thunderclap's crash, no owner named; the lord of the dānavas left unnamed | the verse names neither |
| 10.23 | प्रथमं: a combat never seen before | Apte prathama 'matchless' |
| 10.32 | शान्ताः अग्नयः: the fires that had gone out blazed up | Gita Press's reading; Monier-Williams śānta 'extinguished' |
| 11.2 | आशाः: the quarters | the recitation tradition |
| 11.6 | स्तव्यपरा परोक्तिः: beyond all that is to be praised, the highest speech | Gita Press's two words; the one-compound reading in the footnote |
| 11.33 | विश्वेश: the lord of the universe | our word meaning |
| 11.50, 11.52 | तत्: and so (my name) | Monier-Williams tad 'therefore' |
| 12.22, 12.23, 12.38 | recited or heard; the recital of my births protects from evil spirits; Mahākālī in apposition | the locatives side by side; bhūtebhyaḥ ablative; the received text |
| 13.9, 13.10 | the king took his place on the bank, and the merchant too did austerity | आस्थितः goes with the main subject, Suratha; 13.10's 'and that merchant too' |
| 13.25 | संसिद्ध्यै between the two clauses | the verse's order |
| devi-sukta.4 | उपक्षियन्ति: dwell in me | Monier-Williams cites -kṣiyanti for this very ṛc; 'waste away' in the footnote |
