# Sukhmani Sahib, English: final consistency and derivation pass

Result: 186 of 218 items changed (`final.changes.jsonl`). By reason (one item can have more than one): consistency 171, derivation 76, reading 14. The scratch copy with every change applied is `final/en.work.json`. `overlap.py --report` against Sant Singh Khalsa on that copy gives **0 verses with a shared run of 10+ words**. Before the pass the report listed 66 "sentence nearly theirs" lines; now it lists 19. The longest remaining run is 9 words, at a24.p1, and it is the gloss style.md requires: "in the Saadh Sangat (the company of the holy)".

The edit scripts are `final/edits1.py` to `final/edits6.py`. Each one is a set of exact substitutions with a reason, so each change can be audited. `final/apply.py` rebuilds the scratch copy and the changes file, and `final/check.py` checks the glosses.

## Task A: decisions applied across the work

### 1. Term glosses
Each gloss uses one wording, goes in round brackets, and appears at the first occurrence in each ashtapadi only. No appositive glosses ("the Naam, God's Name") remain, and no gloss repeats within an ashtapadi.

| Term | Gloss |
|---|---|
| Naam | the Naam (the Name, God's presence remembered) |
| Simran | Simran (meditative remembrance of God) |
| Gurmukh | Gurmukh (one who follows the Guru) |
| Saadh Sangat | the Saadh Sangat (the company of the holy) |
| Saadh / Saadhs | the Saadh (holy one) / the Saadhs (holy ones). Where the first use is ਸਾਧ ਕੈ ਸੰਗਿ: the Saadh's company (the company of the holy one) |
| Sant / Sants | the Sant (saint) / the Sants (saints) |
| Brahm Giani | Brahm Giani (one who knows God) |
| Hukam | Hukam (God's will and command) |
| Maya | Maya (the world's illusion and lure) |
| Haumai (ਹਉਮੈ, and ਹਉ in the same sense) | Haumai (ego) |
| Gobind | Gobind (the Lord of the universe) |
| Gopal (ਗੋਪਾਲ / ਗੁਪਾਲ) | Gopal (the sustainer of the world) |
| Dharam Rai | Dharam Rai (the judge of souls) |
| Kirtan | Kirtan (songs of God's praise) |
| Shabad | Shabad (the Word) |
| Ekankar (ਏਕੰਕਾਰ) | Ekankar (the One Creator) |
| Saakat | Saakat (one who has turned from God) |

Other one-off terms also take a bracketed gloss: Apras, Vaishnav, Bhagauti, Pandit, Ramdas, Jivan Mukat, Parijat, Kamadhenu, Neoli, Satsang, Chitra and Gupta, Shiva and Shakti, and Murari. "Sukhmani, the jewel of peace" stays an appositive in all three places (a01.rahao, a24.p5, a24.p8), because it translates the title rather than glossing a term.

### 2. Recurring phrases and words
- **ਸੰਤ** → Sant / Sants. "saint(s)" now appears only inside the gloss.
- **ਸਾਧ / ਸਾਧੂ** used alone → the Saadh / the Saadhs. "the holy" now appears only inside the glosses.
- **ਸਾਧ ਕੈ ਸੰਗਿ / ਸਾਧੂ ਕੈ ਸੰਗਿ / ਸਾਧ ਕੈ ਸੰਗ** → in the Saadh's company.
- **ਸਾਧਸੰਗਿ / ਸਾਧੂ ਸੰਗਿ / ਸਾਧਸੰਗਤਿ** → in the Saadh Sangat. In a07 the litany now alternates "In the Saadh's company" and "In the Saadh Sangat", just as the verse alternates ਸਾਧ ਕੈ ਸੰਗਿ and ਸਾਧਸੰਗਿ.
- **ਸੰਤਸੰਗਿ** → in the company of the Sants.
- **ਨਾਮੁ** used alone → the Naam. With a genitive (ਹਰਿ ਕਾ ਨਾਮੁ, ਹਰਿ ਨਾਮੁ, ਰਾਮ ਨਾਮ, ਪ੍ਰਭ ਨਾਮੁ, ਹਰਿ ਨਾਉ) → the Lord's Name / God's Name. Batch 1 had "the Lord's Naam" 31 times, and all are now "the Lord's Name".
- **ਜਪ-** → repeat (the Naam, the Lord's Name). "chant" and "meditate on" no longer stand for ਜਪ. ਧਿਆ- → meditate on. ਸਿਮਰ- → remember / Simran.
- **ਪ੍ਰਭ ਕੈ ਸਿਮਰਨਿ** → Through Simran of God, (unchanged). **ਜਿਹ ਪ੍ਰਸਾਦਿ** → By whose grace. ਜਿਸੁ ਪ੍ਰਸਾਦਿ at a18.p5 now follows it as well. **ਗੁਰ ਪ੍ਰਸਾਦਿ** → by the Guru's grace.
- **ਆਠ ਪਹਰ** → at all hours. Three places that said "all twenty-four hours" were changed.
- **ਦਰਸਨੁ / ਦਰਸੁ / ਦਰਸ** → the sight of … ("at the sight of him", "the sight of the Brahm Giani").
- **ਦਰਗਹ** → the Lord's court. "God's court" and "Court" were changed.
- **ਸਤਿਗੁਰ** → the True Guru. a18's "Satguru" was changed in 9 places.
- **ਪਰਮੇਸੁਰ** → the Supreme God. "Transcendent Lord" was changed in 3 places. **ਪਾਰਬ੍ਰਹਮ** → the Supreme Lord.
- **ਜਮ** → the messenger of Death. ਜਮ ਫਾਸੀ → Death's noose.
- **ਕਰਨ ਕਰਾਵਨ (ਹਾਰ / ਕਰਨੈਹਾਰੁ / ਜੋਗੁ)** → does and causes all to be done. **ਕਰਣ ਕਾਰਣ / ਕਰਨ ਕਾਰਨ** → the cause of all creation.
- **Verbless ਨਮਸਕਾਰੁ / ਅਦੇਸੁ** → salutations (for ever) to …, with no imperative such as "bow" added (a08.p7, a13.p8, a23.p8, a24.p1).
- **ਆਪਿ ਸਤਿ ਕੀਆ ਸਭੁ ਸਤਿ** appears at both a16.p7 and a23.p5 and now has the same wording in both.

### 3. Opening words
"Salok." and "Ashtapadi." begin exactly the items whose Gurmukhi begins with ਸਲੋਕੁ or ਅਸਟਪਦੀ. This was checked on all 218 items, and no change was needed.

### 4. The ਨਾਨਕ signature: one rule for every line
1. **ਨਾਨਕੁ** (with aunkar) is the subject: "Nanak …" (a07.salok, a20.p1).
2. **Bare ਨਾਨਕ / ਨਾਨਕਾ** is a vocative and is never the subject of a finite third-person verb. It is rendered in one of two ways:
   - **"O Nanak,"** when the line is a statement (third person or impersonal). The verb's subject comes from the pauri ("one", "he", "they").
   - **"says Nanak,"** when the ਨਾਨਕ line itself speaks in the first person (ਮੋਹਿ, ਲਾਗਉ, ਜਾਸਾ, ਜਾਉ, ਹਮਾਰੀ), prays to God in the second person (ਬਖਸਿ ਲੇਹੁ, ਕਾਢਿ ਲੇਹੁ, ਤੁਮਰੀ, ਬੁਲਾਵਹੁ, ਜਾਨਹੁ), or addresses the listener or the mind (imperatives, or "you will …"). In those lines "O Nanak" would wrongly make Nanak the person addressed.
3. **Verbless lines, or lines with only a participle, whose predicate describes Nanak himself** keep Nanak as the subject: "Nanak is a sacrifice to …", "Nanak is the slave of the slaves …", "Nanak has taken refuge …", "Nanak falls at the feet …", "Nanak is in your refuge". Genitive and oblique uses stay as they are ("Nanak's longing", "stay with Nanak").
4. **ਕਹੁ ਨਾਨਕ** → "Says Nanak,".
5. Third-person **ਜਪੈ / ਬੋਲੈ / ਕਹੈ** are rendered as third-person verbs, never as commands. This changed a06.p7 (it read "repeat his Name"), a03.p4, a06.p5, a11.p6 and a21.p8.

Every line was checked. Batch 1 had used "says Nanak" for statements, batch 2 used "O Nanak" for everything including commands, and batches 3 and 4 used a bare "Nanak," for everything. All of these now follow the rule above.

### 5. Spelling, pronouns and punctuation
British spelling, lower-case pronouns for God, no quotation marks, no digits and no square brackets were all checked across the work. The pass introduced none of these, and none needed fixing.

## Readings changed by the ਨਾਨਕ rule (for the owner to confirm)
Applying the rule in item 2 makes Nanak no longer the subject in these lines. Our Hindi (`hi.json`) still reads Nanak as the subject in each of them, so it disagrees with the English until it is reviewed:
- **a01.p5** ਨਾਨਕ ਜਨ ਕੀ ਮੰਗੈ ਰਵਾਲਾ. It was "Nanak begs for the dust of the feet of such servants" and is now "O Nanak, one begs for the dust of the feet of such a servant". style.md §12 uses the old sentence as its example of the signature ("Nanak begs for the dust of their feet"). If the rule stands, style.md should get a different example, such as a07.p4 "Nanak is a sacrifice to the Saadh".
- **a03.p4** ਨਾਨਕ ਬੋਲੈ ਸਹਜਿ ਸੁਭਾਇ → "O Nanak, one utters it in natural poise and with love".
- **a04.p6** ਨਾਨਕ ਤੁਮਰੀ ਕਿਰਪਾ ਤਰੈ → "by your grace, says Nanak, he crosses over". "He" is the humble one who prays in the line before.
- **a05.p4** ਨਾਨਕ ਜਪਿ ਜਪਿ ਜੀਵੈ ਹਰਿ ਕੇ ਚਰਨ → "O Nanak, one lives by dwelling … on the Lord's feet".
- **a06.p5** ਗੁਰ ਪ੍ਰਸਾਦਿ ਨਾਨਕ ਜਸੁ ਕਹੈ → "by the Guru's grace, O Nanak, one speaks his praise".
- **a06.p7** ਨਾਨਕ ਜਾਪੁ ਜਪੈ ਜਪੁ ਸੋਇ → "O Nanak, one repeats his Name, his alone". It had been a command.
- **a11.p4** ਨਾਨਕ ਜੀਵੈ ਦੇਖਿ ਬਡਾਈ → "O Nanak, beholding his own greatness, he rejoices". The subject is God, the subject of the pauri (compare a11.p1 ਕਰਿ ਕਰਿ ਦੇਖੈ ਅਪਨੀ ਵਡਿਆਈ). "Rejoices" gives the idiomatic sense of ਜੀਵੈ (thrives, is gladdened). The alternative is that the creature lives by beholding God's greatness.
- **a11.p6** ਗੁਰ ਪ੍ਰਸਾਦਿ ਨਾਨਕ ਸਚੁ ਕਹੈ → "By the Guru's grace, O Nanak, one speaks the truth". This is the case the reviewer raised.
- **a16.p4** ਜਪਿ ਜਪਿ ਜੀਵੈ ਨਾਨਕ ਹਰਿ ਨਾਉ → "O Nanak, one lives by repeating the Lord's Name again and again".
- **a19.p4** ਮਨਿ ਬੰਛਤ ਨਾਨਕ ਫਲ ਪਾਇ. ਪਾਇ is third person singular, so "you will receive" became "O Nanak, one receives the fruit one's heart desires".
- **a21.p8** ਜਿਉ ਬੁਲਾਵਹੁ ਤਿਉ ਨਾਨਕ ਦਾਸ ਬੋਲੈ → "As you make him speak, says Nanak, so your servant speaks". It was "so your servant Nanak speaks". This one is closest to the line: ਨਾਨਕ ਦਾਸ may be taken in apposition, "servant Nanak", as subject. Revert it if the owner reads it so.

Other reading changes:
- **a06.p1**: ਧਿਆਈਐ is impersonal, so "meditate always on him" became "one should meditate always on him".
- **a17.p6**: ਸੁਖੁ is "peace" (the draft had "comfort").
- **a23.salok**: ਸੰਤ ਭੇਟਿਆ has no first person, so "I met the saint" became "When by the Lord's grace one meets the Sant (saint)".

## Readings I think are doubtful but did not change
- **a08.p4** ਨਾਨਕ ਬ੍ਰਹਮ ਗਿਆਨੀ ਜਪੈ ਸਗਲ ਸੰਸਾਰੁ. Ours: through the Brahm Giani the whole world repeats God's Name. Another reading is that the whole world worships the Brahm Giani. Only the verb was changed for consistency (ਜਪ = repeat); the reading was kept.
- **a18.salok** ਤਿਸ ਕੈ ਸੰਗਿ ਸਿਖੁ ਉਧਰੈ ਨਾਨਕ ਹਰਿ ਗੁਨ ਗਾਉ. Ours takes ਗਾਉ as a command: "says Nanak, sing the virtues of the Lord". Another reading takes it as the means: the Sikh is saved by singing the Lord's virtues.
- **a15.p1** ਗਤਿ ਨਾਨਕ ਜਪਿ ਏਕ ਹਰਿ ਨਾਮ. Ours takes ਜਪਿ as "by repeating": "salvation comes by repeating the Name of the one Lord". It can also be read as a command: "repeat the one Lord's Name and be saved".
- **a16.p6** ਬਿਸ੍ਵਾਸੁ ਸਤਿ ਨਾਨਕ ਗੁਰ ਤੇ ਪਾਈ. ਪਾਈ is a participle that does not agree with Nanak, so ours stays impersonal: "O Nanak, true faith is gained from the Guru". Our Hindi has "नानकने … पाया है" (Nanak has gained).
- **a21.p8** ਉਨ ਕੀ ਸੋਭਾ ਉਨਹੂ ਬਨੀ is rendered "his glory befits him alone", taking ਉਨ as honorific for God. ਉਨ is plural, so it may mean the Sants of the line before: "their glory befits them alone".
- **a22.p6** ਨਾਨਕ ਬਹੁਰਿ ਨ ਆਵਹਿ ਜਾਹਿ. ਆਵਹਿ ਜਾਹਿ can be second person singular or third person plural. Ours: "you will not come and go again" (says Nanak). The third-person reading would be "they do not come and go again".

## Derivation (Task B)
I read side by side with Sant Singh Khalsa every item the report listed under "highest shares of three-word phrases", "close" or "sentence nearly theirs". Lines that followed his sentence shapes or distinctive wording were rewritten in our own words with the reading unchanged: a03.p7, a11.p4, a11.p8, a14.p3, a14.p7, a16.p1, a16.salok, a17.p6, a20.salok, a21.p4, a22.p1, a22.p3, a23.salok, a24.p1, a24.p8 and about 60 single sentences.

Three 10-word runs appeared only because of the consistency changes (a03.p5, a18.p2, a24.p1), and those were removed too.

The 19 "nearly theirs" lines that remain are short lines rendered in their plain natural words, or the verse's own lists. Examples: "What does a son know of his father's birth?"; "Millions upon millions are born, live and die" (the refrain ਕਈ ਕੋਟਿ kept as "Millions upon millions"); "O Nanak, the Creator is beyond all reckoning". They were left as they are.

## For later
- Our Hindi still has Nanak as the subject in the lines listed under "Readings changed by the ਨਾਨਕ rule". It should get the same rule, or the owner should decide the rule before both files go out.
- style.md §12 should record the ਨਾਨਕ rule and the gloss table above, and drop the "Nanak begs …" example.
