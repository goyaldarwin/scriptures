# Our own meanings: style sheet

Every meaning we write (sources `hi-scriptures` / `en-scriptures`, titled "भावार्थ — शास्त्र" / "Meaning — Scriptures") follows this sheet, so that all our meanings read as one voice. The rules behind it are in `docs/PLAYBOOK.md` §4. Check every batch with `tools/meanings/overlap.py`. A change of rule is made here first, then in every meaning.

## 1. The one rule
**Accuracy and consistency come first, and are never traded for anything else** — not for distance from another translation, not for style.

**The meaning comes from the verse, its word meanings, the dictionaries and its context in the work overall and in the nearby verses.** Read the verse with our word meanings (`library/glossary/`), look up every hard Sanskrit or Sanskrit-derived word in Monier-Williams and Apte (§11; `python3 tools/meanings/sanskrit_dict.py look <word>`), and read it in its context: in the nearby verses, who is speaking to whom and what has just happened; in the work overall, what this moment means in it (for the Mānas, in the Rāmāyaṇa). Often the context makes the sense plain where the words alone leave it open; derive the meaning from both. Write the whole draft from that, **without any published meaning open**.

Only after the draft, open the published meanings (Gita Press; Growse's 1883 translation where a copy is at hand, §11) to check the reading: a hard word, an allusion, who "he" is. Where theirs is the better reading, take the reading — **the sense of the verse belongs to no one**, so when the right meaning is the same as Gita Press's, ours says the same thing (the owner: "I don't like changing them or distorting the meanings to match the copyright meanings"). What we never take is their **wording**: no copied sentence (`overlap.py` stops at 10 or more consecutive words in common), no sentence-by-sentence rewording of one, none of their bracketed additions. A shorter shared run (6–9 words) is fine when it is the natural words or the verse's own list (the owner: "if we are creating our own meaning from the words then it should be fine").

**When wording must change to avoid a copy, change only the wording.** Keep the subject, object, speaker, tense, number and every clause exactly; never move a reading away from the right one, never add or drop a word of sense, never make a sentence less natural just to pass the check. Every reworded piece is read against the verse again before it goes in.

## 2. What a meaning is
- **What the verse says, all of it, nothing more.** Every clause of the verse is in the meaning; nothing is added that the verse does not say or plainly imply. No commentary, no moral drawn, no "that is to say".
- **In the verse's order:** the meaning follows the verse line by line and half-line by half-line, so a reader can match each part of the meaning to its words. Reorder only where Hindi or English grammar needs it, and never so far that the parts no longer line up.
- **Length:** a caupāī one or two sentences; a dohā or sorathā one or two; a chhanda as many as its four lines need; a śloka one to three.
- **Brackets:** none as a habit. Write implied words into the sentence. A short gloss in round brackets only where a word would otherwise be unclear to most readers and cannot be worked into the sentence (once, not on every occurrence). Never square brackets.
- **Verse numbers:** every meaning ends with the verse's number as the verse shows it — `॥१७॥`, `॥३० (क)॥` in Hindi, `॥17॥`, `॥30 (क)॥` in English. They are **not** written in the meaning files: the exporter adds them from the verse itself, so they always match. No speaker tags in brackets.
- **People as a group (women, a caste, the unlettered, a people of the forest, another sect):** fair, never distorted. Use respectful, neutral words (स्त्री / woman, not औरत or a slur; "the unlettered", not "boors"); where a word has an established milder sense, use it (the owner approved ताड़ना → शिक्षा / instruction in sundar.59.cau3); never make a line harsher than the verse; and make clear who is speaking (the frightened Ocean, a description of Kali-yuga's decline), so a character's words never read as a timeless instruction. What the words plainly say is not softened (aranya.34.cau1 stays as it reads, the owner's decision). Nothing is added to excuse or explain the verse; a reading that is open goes in the doubts file.
- **Aphorisms and lessons** (सूक्तियाँ, नीति — the verses people quote): present them well. A clear, complete sentence that reads on its own and can be carried away, in the verse's own image and order, without a moral added that the verse does not draw.
- **Doubt:** where the verse is genuinely ambiguous or traditions read it differently, give the plain reading of the words in the meaning, and record the issue in `docs/reviews/<work>-doubts.jsonl` (the Mānas: one file per kāṇḍa, `docs/reviews/<date>-manas-<kāṇḍa>-doubts.jsonl`) as `{"id", "issue", "our reading", "alternatives"}`. The owner decides; a decided doubt is applied and removed from the file.

## 3. Speakers and the nested dialogue
- The Mānas is told by Śiva to Pārvatī (उमा, भवानी, गिरिजा), Kākabhuśuṇḍi to Garuḍa (खगेस, खगपति, उरगारि), Yājñavalkya to Bharadvāja, and Tulasīdāsa to the reader. When the verse addresses one of them, keep the address ("हे उमा!" / "Umā,"); do not add the narrator when the verse does not name one.
- **When a verse opens a speech** and names the speaker (कह, बोले, कहइ), write "X ने कहा —" / "X said:" and then the words. When it does not and **the same speaker goes on**, the speech simply continues from the previous verse (the reader sees it there). When **the speaker changes** and the verse does not name the new one (an answer, a reply), name them anyway — "जाम्बवान्‌जीने कहा —" / "Jāmbavān said:" — so the reader never takes one speaker's words for another's (e.g. kishkindha.30.cau6).
- **No quotation marks** for speech: a speech often runs over many verses, each a separate meaning, and quotes would open in one verse and close in another. Speech is written in the speaker's own person ("I", "you").
- **Each speaker keeps his tone.** Devotees and the narrator use honorifics; Rāvaṇa, Laṅkinī or a mocking rākṣasa do not: Rāvaṇa's "तपसी" stays "that ascetic", not "Śrī Rāmajī".

## 4. Hindi
- Natural modern Hindi in our house style (as in the owner-approved Sundarakāṇḍa: the `sundar.` entries of `tools/works/manas/meanings/hi/scriptures.json`, the same as `tools/works/sundarkand/meanings/hi/scriptures.json`; Sukhmani, Rudram, Īśa).
- **Postpositions joined to the noun:** श्रीरामजीको, सीताजीसे, हनुमान्‌जीने, समुद्रके; pronouns too (उसको, उनके). Spellings of this style: लिये, गये, किये, दिये.
- **Honorific plural** for the Lord, Sītā, Lakṣmaṇa, Hanumān, sages, elders and anyone the speaker honours: वे, उन्होंने, कहते हैं; "आप" when they are addressed by a devotee. The Lord addresses others, Hanumān included, with तुम (the owner's choice; Gita Press uses तू).
- **Standard Hindi spelling for names** (विभीषण not बिभीषन, लक्ष्मण not लछिमन, जाम्बवान्‌ not जामवंत; the monkey king is बालि / Vāli, as the verse spells him, kept apart from बलि / Bali, the king Vāmana bound), anusvāra rather than a half-nasal (लंका, संत), ZWNJ in हनुमान्‌जी.
- Punctuation: । at the end of a sentence; ! after an address or exclamation; — before speech after "कहा"; ; and , as in prose.

## 5. English
- Plain, dignified, modern English; no thee/thou, no "verily", no inversion for effect.
- **IAST for names and Sanskrit terms**, as in our other meanings: Śrī Rāma, Sītā, Lakṣmaṇa, Hanumān, Rāvaṇa, Laṅkā, Ayodhyā. Common nouns that have an English word are translated (monkey, demon, ocean, lotus).
- **Pronouns for the Lord and Sītā in lower case** (he, his, you), as in all our meanings.
- British/Indian spelling (honour, colour, realise).
- Punctuation: a colon before speech ("Hanumān said: …"); ordinary commas and full stops; no exclamation marks except where the verse exclaims (जय, धन्य, हा).

## 6. Names and epithets

The verse's epithet is kept where it is a familiar name or where its sense matters in the verse (कृपासिंधु in "the servant of the ocean of mercy"); otherwise it is rendered by the plain name, so the reader always knows who is meant. In English, a Raghu-epithet in narration is simply "Śrī Rāma" (no "(the Lord of the Raghus)" gloss: that habit is the Gita Press translation's, and it alone makes six-word overlaps); an epithet used **in address** is translated ("O Lord of the Raghus", "O best of the Raghus").

| Verse | Hindi | English |
|---|---|---|
| राम, रामु, रामचंद्र | श्रीरामजी (narration, devotees); राम (Rāvaṇa and his court) | Śrī Rāma; Rāma (Rāvaṇa and his court) |
| रघुपति, रघुनाथ, रघुनायक, रघुराई | श्रीरघुनाथजी | Śrī Rāma; in address "O Lord of the Raghus" |
| रघुबीर, रघुबर | श्रीरघुवीर | Śrī Rāma; in address "O hero of the Raghus" |
| प्रभु, नाथ, स्वामी (of Rāma) | प्रभु, नाथ, स्वामी | the Lord; "my Lord" in address |
| कोसलाधीस, कोसलनाथ | कोसलपति श्रीरामजी | the Lord of Kosala |
| कृपाल, कृपानिधि, कृपासिंधु, करुनानिधान | कृपालु (प्रभु), कृपाके सागर, करुणाके भण्डार | the compassionate Lord; ocean of mercy; treasury of compassion |
| खरारि, त्रिसिरारि | खरके शत्रु, त्रिशिराके शत्रु श्रीरामजी | Śrī Rāma, slayer of Khara / of Triśirā |
| हरि, भगवान, भगवंत | भगवान्, श्रीहरि | the Lord, Śrī Hari |
| सीता, सीतहि, जानकी, बैदेही | सीताजी, जानकीजी, वैदेहीजी (the verse's name) | Sītā (Jānakī where the verse calls her so in address) |
| मातु (Hanumān to Sītā) | माता | Mother |
| हनुमान, हनुमंत, हनू | हनुमान्‌जी | Hanumān |
| पवनसुत, पवनतनय, पवनकुमार, मारुतसुत | पवनपुत्र हनुमान्‌जी / पवनकुमार | Hanumān, son of the Wind |
| कपि (of Hanumān) | हनुमान्‌जी; in an address, as the speaker says it: हे कपि / हे वानर | Hanumān; in an address "Hanumān" |
| कपि, बानर, मर्कट (a group) | वानर | monkeys (owner) |
| भालु, रीछ | भालू, रीछ | bears |
| रीछपति, जामवंत | जाम्बवान्‌जी | Jāmbavān |
| लछिमन | लक्ष्मणजी | Lakṣmaṇa |
| सुग्रीव, कपिपति, कपीस (Sugrīva) | सुग्रीव, वानरराज | Sugrīva, king of the monkeys |
| बिभीषन | विभीषण(जी) (जी once he has taken refuge) | Vibhīṣaṇa |
| रावन, दसानन, दसमुख, दससीस, दसकंधर, दसकंठ | रावण (दशानन etc. only where the heads matter) | Rāvaṇa (the ten-headed where the heads matter) |
| लंकेस, लंकापति | लंकापति रावण | Rāvaṇa, lord of Laṅkā |
| निसिचर, निसाचर, जातुधान, राक्षस | राक्षस | demon (owner) |
| मेघनाद; अच्छकुमार | मेघनाद; अक्षयकुमार | Meghanāda; Akṣaya Kumāra |
| लंकिनी, सुरसा, त्रिजटा, मंदोदरी, सुक | लंकिनी, सुरसा, त्रिजटा, मन्दोदरी, शुक | Laṅkinī, Surasā, Trijaṭā, Mandodarī, Śuka |
| अंगद, नल, नील, मैनाक | अंगद, नल, नील, मैनाक | Aṅgada, Nala, Nīla, Maināka |
| सिंधु, जलनिधि, बारिधि, उदधि, पयोनिधि, पाथोधि, सागर | समुद्र | the ocean (the Ocean, when he appears as a person) |
| बिरंचि, ब्रह्मा; संभु, सिव; सारद | ब्रह्माजी; शिवजी; सरस्वती | Brahmā; Śiva; Sarasvatī |
| उमा, भवानी, गिरिजा (addressed) | हे उमा / हे पार्वती | Umā / Pārvatī (as the verse says) |
| खगेस, खगपति, उरगारि (addressed) | हे गरुड़जी | Garuḍa |
| तुलसी, तुलसीदास | तुलसीदास | Tulasīdāsa |

## 7. Recurring terms

| Verse | Hindi | English |
|---|---|---|
| भगति, भक्ति | भक्ति | devotion |
| भजन, भजहु | भजन, भजना | worship (and turn to in love) |
| सुमिरन, सुमिरि | स्मरण | remembrance; remembering |
| सरन, सरनागत | शरण, शरणागत | refuge; one who has come for refuge |
| कृपा, दाया | कृपा, दया | grace; mercy |
| माया | माया | māyā (the Lord's power of illusion) — gloss once per kāṇḍa |
| सतसंग | सत्संग | the company of the good (satsaṅga) |
| संत, साधु | संत, साधु | saints, the good |
| ग्यान, बिग्यान, बिबेक | ज्ञान, विज्ञान, विवेक | knowledge, realised knowledge, discernment |
| बैराग, बिरति | वैराग्य | dispassion |
| धर्म, नीति | धर्म, नीति | dharma (duty, right conduct); policy, right counsel |
| भव, भवसागर | संसार, भवसागर | worldly existence; the ocean of worldly existence |
| परम पद, अपबर्ग, मोच्छ | परमपद, मोक्ष | the supreme state; liberation |
| अघ, पाप | पाप | sin |
| काम, क्रोध, मद, लोभ, मोह, मत्सर | काम, क्रोध, मद, लोभ, मोह, मत्सर | desire, anger, pride, greed, delusion, envy |
| सुर, देव; मुनि; सिद्ध | देवता; मुनि; सिद्ध | gods; sages; siddhas |
| राम काज | श्रीरामजीका काम | Śrī Rāma's work |
| जय, जय जय | जय हो | glory to … / victory to … |

## 8. Ślokas and Sanskrit stutis
Translated from the Sanskrit directly, word by word against `glossary/sa.json`, then put into natural Hindi and English. Keep the structure of a list of epithets (one phrase per epithet, in the verse's order) and end with the verb of the verse (वन्दे → "I bow to", नमामि → "I salute").

## 8a. Stotras of names (Rāma Rakṣā and the like)
A stotra is a litany of names, and the names are its text: render each name as the verse gives it (राम, रामभद्र, रामचन्द्र; श्रीराम only where the verse has श्री), translating an epithet's sense where it matters (कौसल्येय → कौसल्यानन्दन / son of Kausalyā). Honorific verbs throughout (रक्षा करें). A sentence spread over several verses is closed in the last of them, and each verse still reads on its own.

## 9. Shared runs of words
- **Two faithful translations meet.** A meaning written from the verse alone often shares a run of 6–9 words with Gita Press: the natural words ("साम दान भय और भेद", "in my dream a monkey"). Keep such a run; do not make a sentence less natural to dodge the check. The limit is 10 or more words.
- The verse's own list in the verse's order ("ढोल, गँवार, शूद्र, पशु और नारी") is the verse, not anyone's wording; still, the run around it is rephrased so that the limit stays a plain rule with no exceptions.
- Keep to the verse: read every meaning a second time against the verse to catch additions (the verse says "the bounds", मरजादा, not "my bounds": sundar.59.cau3).

## 10. Before a batch goes in
0. The dictionaries were in use from the first verse: `python3 tools/meanings/sanskrit_dict.py check` passes (no batch is made, written or applied without them).
1. Every item has a Hindi and an English meaning, once, and nothing extra (the exporter checks).
2. `python3 tools/meanings/overlap.py` passes (no 10+ run) for Hindi against `hi-gitapress` and English against `en-gitapress`; read its 6–9-word runs and the `--report` list of close rewordings side by side.
3. A second reader who did not write the batch checks each meaning against the verse for accuracy and against this sheet.
4. Every piece reworded to avoid a copy has been read against the verse again (§1).
5. Doubts are in the doubts file, not in the meanings.

## 11. Word meanings and dictionaries
Our word meanings (`library/glossary/<lang>.json`) are the starting point. Where a word is hard, rare or its entry does not fit the line, check it in trusted dictionaries and fix the entry if it is wrong. The commit message says what changed and why.
- **Sanskrit and Sanskrit-derived words:** Monier-Williams, *Sanskrit-English Dictionary* (1899); V. S. Apte, *Practical Sanskrit-English Dictionary* (1890) — Cologne Digital Sanskrit Lexicon (`github.com/sanskrit-lexicon/csl-orig`; `tools/meanings/sanskrit_dict.py` looks words up).
- **Awadhi, Braj and Hindi:** J. T. Platts, *Dictionary of Urdū, Classical Hindī and English* (1884), the main dictionary for Awadhi and Braj; Śyāmasundara Dāsa, *Hindī Śabdasāgara*; R. S. McGregor, *Oxford Hindi-English Dictionary*, read on its page images (or by hand on dsal.uchicago.edu), never from its OCR, which is unreliable; Mahendra Caturvedi, *Practical Hindi-English Dictionary* (dsal.uchicago.edu, which needs the owner to allow the site).
- **Punjabi (Gurmukhi):** Bhai Kahn Singh Nabha, *Gur Shabad Ratnakar Mahan Kosh*.
- **The reference books** are in `scriptures-data` under `reference/<lang>/dictionaries/`: `hi/dictionaries/platts/`, `hi/dictionaries/mcgregor/` (the page images; its `ocr/` text is not to be trusted), `hi/dictionaries/hindi-shabdasagar/` (volume 1) and `pa/dictionaries/mahan-kosh/`. The Gurbani commentaries of §13 are under `reference/pa/commentaries/`.
- **A second translation to check against:** F. S. Growse, *The Rāmāyaṇa of Tulasīdāsa* (1883, public domain).

Take the facts (the sense, the grammar), never a dictionary's sentences. A word's entry lists every sense the work uses it in (जाहू: "जाओ / जिसे, जिसके" — "go / whom, whose"), separated by " / ", so the word sheet shows them all; **the verse's meaning uses only the sense that fits its context**. A sense that is not settled goes in `docs/reviews/dictionary-doubts.jsonl`.

## 12. Gurbani (Sukhmani Sahib and later Sikh works)
The verse is Gurmukhi (Sant Bhasha: Braj, Punjabi, Sanskrit and Persian words), read with `library/glossary/pa.json` and our own Hindi meaning (`tools/works/sukhmani-sahib/meanings/hi/scriptures.json`) as aids. The Sikh understanding is the frame: one formless Lord (Ik Oankar), reached by the Guru's word and remembrance of the Naam, not by ritual.
- **Sikh terms as the community uses them**, in the plain Roman spelling of Sikh English (no IAST diacritics), glossed once per ashtapadi where a reader may not know them: **Naam** (the Name: God's presence remembered), **Simran** (remembrance, meditating on the Naam), **Gurmukh** (one who follows the Guru) / **manmukh** (the self-willed), **Saadh Sangat** (the company of the holy), **Sant** / **Saadh** (the saint, the holy one), **Brahm Giani** (one who knows God), **Hukam** (God's will, command), **Maya**, **Haumai** (ego), **Waheguru**, **Gurbani**, **Kirtan**, **Har** / **Hari**, **Gobind**, **Paarbrahm** (the Supreme Lord).
- **God:** ਪ੍ਰਭ / ਪ੍ਰਭੂ → God; ਹਰਿ → the Lord (Har where it is a name in a list); ਠਾਕੁਰ, ਸੁਆਮੀ → the Master, my Lord; ਪਾਰਬ੍ਰਹਮ → the Supreme Lord (Paarbrahm). Pronouns lower case, as in all our English (he, you); where natural, repeat "God" rather than lean on "he".
- **ਨਾਨਕ** in the last line is the Guru's own signature: "Nanak", as he speaks of himself ("Nanak begs for the dust of their feet"), never "Guru Nanak".
- **Refrains:** a pauri repeats one phrase line after line (ਪ੍ਰਭ ਕੈ ਸਿਮਰਨਿ…, ਬ੍ਰਹਮ ਗਿਆਨੀ…). Render the phrase the same way every time in a pauri and across the work, in our own wording, so the litany is heard.
- **Order and completeness:** one English sentence (or clause) per line of the pauri, in the line order, so a reader can match them; nothing added.
- **Verse numbers:** none in the text; the exporter adds the stanza number from the verse (॥੧॥ → ॥1॥).
- **Glosses in the Sukhmani**, in round brackets at the first use in each ashtapadi: Naam (the Name, God's presence remembered) · Simran (meditative remembrance of God) · Gurmukh (one who follows the Guru) · Saadh Sangat (the company of the holy) · Saadh (holy one) · Sant (saint) · Brahm Giani (one who knows God) · Hukam (God's will and command) · Maya (the world's illusion and lure) · Haumai (ego) · Gobind (the Lord of the universe) · Gopal (the sustainer of the world) · Dharam Rai (the judge of souls) · Kirtan (songs of God's praise) · Shabad (the Word) · Ekankar (the One Creator).
- **Recurring renderings:** ਸਾਧ ਕੈ ਸੰਗਿ "in the Saadh's company", ਸਾਧਸੰਗਿ "in the Saadh Sangat"; ਨਾਮੁ alone "the Naam", with an owner "the Lord's Name"; ਜਪ "repeat", ਧਿਆ "meditate on", ਸਿਮਰ "remember"; ਆਠ ਪਹਰ "at all hours"; ਦਰਸਨੁ "the sight of …"; ਦਰਗਹ "the Lord's court"; ਸਤਿਗੁਰ "the True Guru"; ਪਰਮੇਸੁਰ "the Supreme God"; ਕਰਨ ਕਰਾਵਨ "does and causes all to be done".
- **ਨਾਨਕ in the last line:** a third-person verb (ਜਪੈ, ਬੋਲੈ, ਕਹੈ) is never a command. Where our Hindi reads Nanak as the subject, so does the English; the grammarians' reading of a bare ਨਾਨਕ (no ੁ) as an address ("O Nanak") is kept where our Hindi has it and is a doubt for the owner elsewhere.
- **Copying shows as shared phrases, not only runs:** a pauri can follow another translation line by line with only its refrain changed. Read the checker's "highest shares of shared three-word phrases" beside theirs.

## 13. Punjabi (ਪੰਜਾਬੀ) meanings
Source `pa-scriptures` ("ਪੰਜਾਬੀ ਅਰਥ — ਸ਼ਾਸਤਰ / Punjabi meaning — Scriptures"), shown in the ਪੰ layer.
- **Language:** today's standard Punjabi in Gurmukhi (Unicode, NFC), as an educated reader in Punjab writes it: plain, clear, warm. Not the old teeka idiom (ਕਰਤੇ ਹੈਂ, ਤਿਸ ਕੌ, ਹੈਣ) and not word-for-word glossing; whole sentences. Postpositions written separately (ਦੇ, ਨੂੰ, ਵਿੱਚ, ਤੋਂ, ਨਾਲ); ਵਿੱਚ, ਪਰਮਾਤਮਾ, ਪ੍ਰਭੂ, ਸ਼ਬਦ (with ਸ਼ where modern spelling has it).
- **Line by line:** one piece per verse line, in the verse's order; "" for a line that is only a heading (ਅਸਟਪਦੀ ॥, ਸਲੋਕੁ ॥). Each piece reads as a sentence or clause under its line; a sentence may run on to the next line's piece where the verse's sentence does.
- **The same reading as our Hindi and English** (written and reviewed for this library, some points settled by the owner). Where the Gurmukhi plainly needs another reading, follow the Gurmukhi and record a doubt; never change the reading only because a commentary reads differently.
- **God:** ਪ੍ਰਭ / ਪ੍ਰਭੂ → ਪ੍ਰਭੂ; ਹਰਿ → ਹਰੀ or ਪ੍ਰਭੂ; ਪਾਰਬ੍ਰਹਮ → ਪਾਰਬ੍ਰਹਮ ਪ੍ਰਭੂ; ਠਾਕੁਰ, ਸੁਆਮੀ → ਮਾਲਕ, ਸੁਆਮੀ; ਗੋਬਿੰਦ, ਗੋਪਾਲ kept as names. God addressed as ਤੂੰ / ਤੇਰਾ, as Gurbani itself does; the Guru spoken of with ਜੀ where natural.
- **Sikh terms as Punjabi readers use them, unglossed:** ਨਾਮ, ਸਿਮਰਨ, ਗੁਰਮੁਖ, ਮਨਮੁਖ, ਸਾਧ ਸੰਗਤ, ਸਾਧੂ, ਸੰਤ, ਬ੍ਰਹਮ ਗਿਆਨੀ, ਹੁਕਮ, ਮਾਇਆ, ਹਉਮੈ, ਕੀਰਤਨ, ਸ਼ਬਦ, ਦਰਗਾਹ, ਧਰਮ ਰਾਜ. Refrains rendered the same way every time (§12).
- **ਨਾਨਕ in the last line:** as our Hindi reads it (subject, or ਹੇ ਨਾਨਕ! where our Hindi has the address); a third-person verb is never a command.
- Round brackets for words the line implies; no quotation marks, no square brackets, no verse numbers (the exporter adds ॥੧॥ in Gurmukhi digits).
- **Checks, never copies:** Prof. Sahib Singh's Darpan (copyright) and the Faridkot Teeka (public domain, older idiom) are read only to check a reading, after drafting from the Gurmukhi; the overlap check runs against both (0 runs of 10+ words; 6–9 read).
