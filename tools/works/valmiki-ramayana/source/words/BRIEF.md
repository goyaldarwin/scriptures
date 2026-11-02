# Brief: Sanskrit word meanings for the Vālmīki Rāmāyaṇa (one batch)

You write the dictionary entries a reader sees when they tap a word of a verse in a scripture app. Accuracy is the first priority ("these are the tiny steps someone is taking to learn Sanskrit… we cannot afford mistakes"). Work alone; write only your output file.

**Input:** a batch file of words (JSON list). Each item: `word` (the word exactly as printed in the Gita Press verse: often several words joined by sandhi or a compound), `count` (how often it occurs in this kāṇḍa), and up to three `contexts`, each with the verse id, the verse, and `glosses`: word-by-word glosses that two published translations (IIT Kanpur / RSV Tirupati and valmikiramayan.net) give for that verse — their Sanskrit split differently and sometimes spelled a little differently; they may be imperfect.

**For every word write one entry:**
- `en`: the English meaning, short and plain, in the word's own form (its case and number shown in the English: "of the trees", "having seen", "to search for"). For a joined word, the meaning of the whole. If the word has more than one sense in this work, give each, separated by " / ".
- `hi`: the same meaning in simple, correct Hindi (Gita Press house style: joined postpositions as in वृक्षोंके, रामने; ए not ये), e.g. "वृक्षोंके", "देखकर", "खोजनेके लिये".
- `r`: the root or stem (प्रातिपदिक or धातु) in Devanagari, e.g. "वृक्ष", "दृश्", "अन्विष्" — for a joined word, the parts' stems joined with " + ".
- `g`: the grammar in Hindi terms, short: "षष्ठी, बहुवचन", "क्त्वा (पूर्वकालिक)", "तुमुन्", "लङ्, प्रथम पुरुष, एकवचन", "समास", "संधि"; for a joined word, what joins it (e.g. "संधि: पदम् + अन्वेष्टुम्").
- `p` (only for a word that is several words joined by sandhi, or a compound whose members a learner needs): `[[part, "हिन्दी अर्थ"], …]` in order, each part in its own pausal form (पदम्, अन्वेष्टुम्; राम, सीता).
**How:** read the verse; take the sense the glosses give, but write it in your own short wording (never copy their sentences; take the facts) and CHECK it — every content word's sense and every part in Monier-Williams and Apte: `cd /home/claude/scriptures && python3 tools/meanings/sanskrit_dict.py look <word> [<word> …]` (Devanagari stems; look up stems and roots, not inflected forms). Where the glosses are missing or wrong, decide from the verse, the grammar and the dictionaries. Names: give who they are briefly ("Hanumān (son of the wind-god)"; Hindi "हनुमान्जी"). Never leave a question for anyone and never leave an entry empty: decide.

**Output:** `<the batch file name>.out.json`: one JSON object `{word: {"en", "hi", "r", "g", "p"?}}` with every word of the batch exactly as given (keys unchanged), written with json.dump(ensure_ascii=False). Reply with only the number of entries written and the path.
