# Our own meanings: style sheet

Every meaning we write (sources `hi-scriptures` / `en-scriptures`, titled "भावार्थ — शास्त्र" / "Meaning — Scriptures") follows this sheet, so that some 12,000 meanings read as one voice. Rules and plan: `docs/handoff/2026-10-19-own-meanings.md`. Check every batch with `tools/meanings/overlap.py`.

Status: **draft for the pilot (Sundarakāṇḍa)**. Items marked ⟨owner⟩ are being settled with the owner on the samples; change them here first, then in every meaning.

## 1. The one rule
Write from the verse: its words (our word meanings in `library/glossary/`), who is speaking to whom, what has just happened. Use a published meaning only to check understanding (a hard word, an allusion, who "he" is) and only after writing. Never reword a published meaning. Facts and interpretation are free; another translator's sentences, sentence order, distinctive word choices and bracketed additions are not. If ours reads like theirs, write it again.

## 2. What a meaning is
- **What the verse says, all of it, nothing more.** Every clause of the verse is in the meaning; nothing is added that the verse does not say or plainly imply. No commentary, no moral drawn, no "that is to say".
- **In the verse's order where the language allows,** so a reader can follow line by line.
- **Length:** a caupāī one or two sentences; a dohā or sorathā one or two; a chhanda as many as its four lines need; a śloka one to three.
- **Brackets:** none as a habit. Write implied words into the sentence. A short gloss in round brackets only where a word would otherwise be unclear to most readers and cannot be worked into the sentence (once, not on every occurrence). Never square brackets.
- **No verse numbers** (no ।।१७।।, no (1)) and no speaker tags in brackets.
- **Doubt:** where the verse is genuinely ambiguous or traditions read it differently, give the plain reading of the words in the meaning, and record the issue in `docs/reviews/<date>-meaning-doubts.jsonl` (`{"id", "issue", "our reading", "alternatives"}`). The owner decides.

## 3. Speakers and the nested dialogue
- The Mānas is told by Śiva to Pārvatī (उमा, भवानी, गिरिजा), Kākabhuśuṇḍi to Garuḍa (खगेस, खगपति, उरगारि), Yājñavalkya to Bharadvāja, and Tulasīdāsa to the reader. When the verse addresses one of them, keep the address ("हे उमा!" / "Umā,"); do not add the narrator when the verse does not name one.
- **When a verse opens a speech** and names the speaker (कह, बोले, कहइ), write "X ने कहा —" / "X said:" and then the words. When it does not, the speech simply continues from the previous verse (the reader sees it there).
- **No quotation marks** for speech: a speech often runs over many verses, each a separate meaning, and quotes would open in one verse and close in another. Speech is written in the speaker's own person ("I", "you").
- **Each speaker keeps his tone.** Devotees and the narrator use honorifics; Rāvaṇa, Laṅkinī or a mocking rākṣasa do not: Rāvaṇa's "तपसी" stays "that ascetic", not "Śrī Rāmajī".

## 4. Hindi
- Natural modern Hindi in our house style (as in `tools/works/sundarkand/meanings/hi.json`, Sukhmani, Rudram, Īśa).
- **Postpositions joined to the noun** ⟨owner⟩: श्रीरामजीको, सीताजीसे, हनुमान्‌जीने, समुद्रके; pronouns too (उसको, उनके). Spellings of this style: लिये, गये, किये, दिये.
- **Honorific plural** for the Lord, Sītā, Lakṣmaṇa, Hanumān, sages, elders and anyone the speaker honours: वे, उन्होंने, कहते हैं; "आप" when they are addressed by a devotee. The Lord addresses others with तुम, a son or dear one with तुम/बेटा as the verse does.
- **Standard Hindi spelling for names** (विभीषण not बिभीषन, लक्ष्मण not लछिमन, जाम्बवान्‌ not जामवंत), anusvāra rather than a half-nasal (लंका, संत), ZWNJ in हनुमान्‌जी.
- Punctuation: । at the end of a sentence; ! after an address or exclamation; — before speech after "कहा"; ; and , as in prose.

## 5. English
- Plain, dignified, modern English; no thee/thou, no "verily", no inversion for effect.
- **IAST for names and Sanskrit terms**, as in our other meanings: Śrī Rāma, Sītā, Lakṣmaṇa, Hanumān, Rāvaṇa, Laṅkā, Ayodhyā. Common nouns that have an English word are translated (monkey, demon, ocean, lotus).
- **Pronouns for the Lord and Sītā in lower case** ⟨owner⟩ (he, his, you), as in our Chālīsā meanings.
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
| कपि, बानर, मर्कट (a group) | वानर | monkeys ⟨owner: monkeys or vānaras⟩ |
| भालु, रीछ | भालू, रीछ | bears |
| रीछपति, जामवंत | जाम्बवान्‌जी | Jāmbavān |
| लछिमन | लक्ष्मणजी | Lakṣmaṇa |
| सुग्रीव, कपिपति, कपीस (Sugrīva) | सुग्रीव, वानरराज | Sugrīva, king of the monkeys |
| बिभीषन | विभीषण(जी) (जी once he has taken refuge) | Vibhīṣaṇa |
| रावन, दसानन, दसमुख, दससीस, दसकंधर, दसकंठ | रावण (दशानन etc. only where the heads matter) | Rāvaṇa (the ten-headed where the heads matter) |
| लंकेस, लंकापति | लंकापति रावण | Rāvaṇa, lord of Laṅkā |
| निसिचर, निसाचर, जातुधान, राक्षस | राक्षस | demon ⟨owner: demon or rākṣasa⟩ |
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

## 9. What the pilot samples taught (2026-10-19)
- **Writing from the verse is not enough on its own.** Of 18 sample verses written from the verse alone, before Gita Press was opened, 9 Hindi and 7 English meanings still shared a run of 6+ words with Gita Press: two literal translations of the same words in the same order meet. So the checker is part of writing, not a formality: rewrite the flagged sentence in our own shape (another sentence order, another natural word), never by copying a third source.
- The verse's own list in the verse's order ("ढोल, गँवार, शूद्र, पशु और नारी") is the verse, not anyone's wording; still, the run around it is rephrased so that the limit stays a plain rule with no exceptions.
- Keep to the verse: the first draft of sundar.59.cau3 said "my bounds" where the verse says only "the bounds" (मरजादा). The second reading against the verse catches such additions.

## 10. Before a batch goes in
1. Every item has a Hindi and an English meaning, once, and nothing extra (the exporter checks).
2. `python3 tools/meanings/overlap.py` passes for Hindi against `hi-gitapress` and English against `en-gitapress`; read the `--report` list of close rewordings side by side.
3. A second reader who did not write the batch checks each meaning against the verse for accuracy and against this sheet.
4. Doubts are in the doubts file, not in the meanings.
