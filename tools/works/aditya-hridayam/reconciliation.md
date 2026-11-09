# Āditya Hṛdayam — how the text is settled

**Source of truth:** the owner's printout of sanskritdocuments.org, *आदित्यहृदयम्* (file `adityahriday.itx`, transliterated by
M. Giridhar, proofread by Kirk Wortman, updated 13 June 2020, typeset 8 October 2023; private copy in scriptures-data at
`hinduism/stotra/surya/aditya-hridayam/printouts/sanskritdocuments/adityahriday.pdf`). Its text layer is Unicode. It gives
the stotra twice: with an English meaning, and as the recitation text (स्तोत्रपाठ: the viniyoga, the ṛṣyādi-, kara- and
hṛdayādi-ṣaḍaṅga-nyāsa, then the 31 ślokas). The text is the recitation text, which has the same 31 ślokas as the first.

**Second witness:** the Vālmīki Rāmāyaṇa of this library, Gita Press, Yuddha-kāṇḍa sarga 105
(`tools/works/valmiki-ramayana/text.txt`, `yuddha.105.1`–`.31`; the printout's last line also names it so). It is the same
sarga in the Gita Press reading, which differs from the printout in some 25 words.

**Third witness:** the owner's IIT Kanpur copy of the sarga (valmiki.gitasupersite.in, the southern recension, Yuddha
107; scriptures-data `hinduism/granth/valmiki/ramayana/printouts/iitk/valmiki-ramayana.json`). Its text runs the words of a
pāda together; it agrees with the printout against Gita Press in most places (भगवान् ऋषिः, जपेन्नित्यम्, भास्करो, तदेव,
वधिष्यसि) and with Gita Press in a few (मार्तण्डकोऽंशुमान्, हरये, सर्वेषु परमप्रभुः, ततोऽगस्त्यो … स, युद्धार्थं).

**The recordings:** Sri Sathya Sai Official (YouTube `Z7W59S6fH98`, the default) and Braja Beats (YouTube `I8Xg_2RC5Vk`), (YouTube `I8Xg_2RC5Vk`), through its transcript through their transcripts (`audio/<source>/transcripts/`). Braja Beats sings the 31 ślokas and then the sarga's closing
words; it does not recite the viniyoga or the nyāsas.

`source/compare.py` prints every word that differs between `text.txt` and the two witnesses; each is below.

## Why the stotra has its own text, not the Vālmīki work's verses
`docs/PLAYBOOK.md` §2 takes a verse that belongs to a bigger work from it by id. Here the owner's source for the stotra
and the recording both follow the reading in which the Āditya Hṛdayam is recited as a stotra, and that reading differs from
the Gita Press sarga in words, not spelling: the recording sings जपेन्नित्यम् (4), भगवानृषिः (2), वधिष्यसि (27), तदेव (22),
एष एवाग्निहोत्रं (23), मार्तण्डाय नमो नमः (18), वधे तस्य धृतोऽभवत् (30), with the printout. Taking the Gita Press verses
would put the highlight on words that are not being sung (§8), so the stotra keeps the printout's text, and the Vālmīki
work keeps the book's. The ids are the stotra's own (`sh1`–`sh31`).

## Choices against the printout
| Verse | Printout | Text | Why |
|---|---|---|---|
| viniyoga | भगवान्ब्रह्मा **देवताः** | भगवान्ब्रह्मा देवता | one deity, Brahmā, so the singular; the printout's own nyāsa has the singular (आदित्यहृदयभूतब्रह्मदेवतायै) |
| rishyadi | …देवतायै नमः**।** हृदि । | …देवतायै नमः हृदि । | a stray daṇḍa inside the line; every other line of the nyāsa reads नमः + the place |
| sh3 | श‍ृणु | शृणु | the printout's zero-width joiner, a typing aid, not a letter |
| sh11 | मार्ताण्ड अंशुमान् | मार्तण्डकोंऽशुमान् | मार्ताण्ड अंशुमान् leaves the two words unjoined, with no case ending on the first: broken Sanskrit. The Gita Press sarga and IIT Kanpur read मार्तण्डकोंऽशुमान् (मार्तण्डकोऽंशुमान्), and Braja Beats sings it (“mārtāṇḍakoṃśumān”); Sri Sathya Sai sings the printout's words here, so the highlight differs from its singing by one syllable |
| sh13 | विन्ध्यवीथी प्लवङ्गमः | विन्ध्यवीथीप्लवङ्गमः | one epithet, “who moves along the path of the Vindhya”: विन्ध्यवीथी alone has no case ending of its own here; the Gita Press sarga and IIT Kanpur write it as one word |
| sh14 | महातेजाः रक्तः | महातेजा रक्तः | the visarga after ā drops before a voiced sound (र); the Gita Press sarga |
| sh18 | मार्ताण्डाय (or मार्तण्डाय) | मार्तण्डाय | the printout's own alternative, so that the name is spelt one way in the stotra (मार्तण्डकः in 11; Monier-Williams mārtaṇḍa) |
| sh30 | सर्व यत्नेन | सर्वयत्नेन | one compound with महता, “with all his great effort”; the Gita Press sarga |

Kept as the printout writes them: रश्मिमतेरिति in the viniyoga (no witness gives another form); भास्करो in 12, where the
Gita Press sarga has ऽहस्करो: IIT Kanpur has भास्करो, and the recording does not make it clear; हिरण्यरेता (10) and वह्नये (21) over the printout's
alternatives विश्वरेता and हरये, which the recording also bears out (“hiraṇyaretā”, “vahnaye”); चिन्ताशोकप्रशमनं आयुर्वर्धनम्
(5, which the writing standard gives as प्रशमनम् आयुर्…, docs/PLAYBOOK.md §3); सहस्रांशो आदित्याय (17, a vocative before a
vowel, unjoined in both witnesses); तदाऽगस्त्यो (27).

Left out: the printout's headings and markers, which are not recited as verses (स्तोत्रपाठ, अथ … न्यासः, इति … न्यासः,
॥ अथ आदित्यहृदयम्॥, ॥ फलश्रुतिः ॥): they are the work's topics instead. The printout's text layer also runs some words
together (सुप्तेषुजागर्ति, कृच्छ्रेषुकान्तारेषुभयेषुच, युद्धेषुविजयिष्यसि, लोकेषुसर्व); its printed page has the spaces.

## Closing words
The printout ends with इति आदित्यहृदयं मन्त्रम्॥. The recording instead sings the sarga's colophon, which the Gita Press
book prints after sarga 105 (page 1916 of the owner's sanskrit-english.pdf, read from its text layer as the Vālmīki work's
`source/build_lines.py` reads it): इत्यार्षे श्रीमद्रामायणे वाल्मीकीये आदिकाव्ये युद्धकाण्डे पञ्चाधिकशततमः सर्गः॥ १०५॥. The text
takes the words the recording sings (§3: a recording's lines not in the book are added and timed), without the sarga number.

## Verse numbers and order
The 31 ślokas are numbered as both witnesses number them; the viniyoga, the nyāsas and the closing words have no number.
The order is the printout's recitation order, which is also the recording's.

## Meanings
Our own Hindi and English, written from the Sanskrit (`tools/meanings/style.md`), with the readings below. The printout's
English (M. Giridhar's, which the printout says is not to be copied) and the Vālmīki work's copied Gita Press meanings are
read only to check a reading, and our meanings share no run of ten words with them (`tools/meanings/overlap.py`).
- **12 शङ्खः**: a name of the Sun in this list; Monier-Williams and Apte give śaṅkha only as the conch and other senses, so
  the word meaning follows its parts (शम्, welfare): Śaṅkha, the bringer of good, as the IIT Kanpur copy reads it.
- **18 सारङ्गाय**: Sāraṅga, “the many-hued” (Monier-Williams, Apte: dappled, variegated); “swift-moving” is a commentary's
  gloss that neither dictionary gives.
- **13 विन्ध्यवीथीप्लवङ्गमः**: who speeds along the path of the Vindhya (IIT Kanpur reads it the same way).
- **22 पायति**: from √pai, “to dry” (Monier-Williams, Apte), beside tapati “heats” and varṣati “rains”: he dries, heats and
  rains with his rays; one web translation reads it so too (“dries … and causes rain”, vishwaas.blogspot.com). The Gita
  Press meaning reads it as “sustains”, which the form does not give (√pā “to protect” makes pāti).
- **24 सर्व एष रविः प्रभुः**: the printout's reading; “of all the deeds done in the worlds, this Sun is the lord”.
- **31 वचस्त्वरेति**: the Sun's word to Rāma is “त्वर”, “make haste”.
