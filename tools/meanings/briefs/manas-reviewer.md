<!-- The briefs for writing the rest of the Mānas (ROADMAP item 1), from the Sundarakāṇḍa pilot (2026-10-19), updated for line-by-line meanings. Paths are relative to the repository root. -->
# Brief for reviewing our own meanings of the Śrī Rāmacaritamānasa

Someone else wrote new Hindi and English meanings for a batch of verses. You are the second reader: you did not write them, and your job is to catch every error before the owner sees them. The owner's first rule is **accuracy**, then unambiguity, clarity, consistency. Be exact and sceptical; do not rubber-stamp.

## Read first
1. `tools/meanings/style.md` — the binding style sheet (read all of it).
2. Our Sundarakāṇḍa meanings, owner-approved: `tools/works/manas/meanings/hi/scriptures.json` and `en/scriptures.json` (`m`: verse id → one piece per verse line). Match this voice, length and line-by-line division. (No verse numbers in them; the exporter adds them.)
3. The batch file `batch-NN.md` (verses, transliteration, word meanings, context) and the writer's output: `batch-NN.hi.json`, `batch-NN.en.json`, `batch-NN.topics.json`, `batch-NN.doubts.jsonl`, `batch-NN.words.jsonl`.

## Check every verse, both languages, against the verse itself
- **Accuracy:** does the meaning say what the verse says — right subject, object, speaker, addressee, tense, negation, number, who "he/she" is? Check hard words against the word meanings and, for Sanskrit or Sanskrit-derived words, `python3 tools/meanings/sanskrit_dict.py look <word> …` (Monier-Williams, Apte).
- **Completeness:** every clause and every meaningful word of the verse is rendered; nothing left out.
- **Nothing added:** no commentary, no moral, no explanation that the verse does not say or plainly imply; no bracketed insertions except a rare short gloss.
- **Order and lines:** one piece per verse line, each under its own line, reading on its own; `""` only where a sentence truly cannot be cut, at the same lines in Hindi and English.
- **Hindi and English agree** with each other in sense.
- **Style sheet:** names and epithets, honorifics (तुम from the Lord; honorific plural; Rāvaṇa's tone his own), joined postpositions, हनुमान्‌जी with ZWNJ, speech form ("X ने कहा —" / "X said:", no quotation marks), "monkeys", "demons", lower-case pronouns for the Lord, British spelling, respectful wording for groups of people, **no verse numbers in the text**.
- **Language quality:** natural, correct Hindi (gender, agreement, spelling) and English.
- You may look at Gita Press's meaning to check a reading:
  `python3 -c "import json,sys; L='library/hinduism/granth/tulsidas/ramcharitmanas/meanings/'; H=json.load(open(L+'hi-gitapress.json'))['m']; E=json.load(open(L+'en-gitapress.json'))['m']; [print(i,'\n HI:',H[i][0],'\n EN:',E.get(i,[''])[0]) for i in sys.argv[1:]]" <ids…>`
  Where ours and theirs differ in reading, decide from the verse which is right. Any fix you propose must not copy their sentences (no 10+ consecutive words in common; 6–9 only when it is the natural words).
- **Topics:** each heading must be a correct, short label of what happens from that verse on, not Gita Press's wording.
- **Writer's doubts and word issues:** say for each whether you agree.

## Output (in the same folder; do not edit any other file, and do not edit the writer's files)
`batch-NN.review.jsonl`, one JSON object per problem: `{"id", "lang": "hi"|"en"|"topic"|"word"|"doubt", "kind": "error"|"omission"|"addition"|"style"|"language", "problem": "<what is wrong, briefly>", "line": <0-based verse line, for hi/en>, "fix": "<the complete corrected piece for that line (or heading/entry), ready to paste>"}`. A fix that moves a cut between lines gives one line per changed piece. Report only real problems; a perfect verse gets no line. Then check your fixes: put them in a scratch copy and run `python3 tools/meanings/overlap.py <copy> library/hinduism/granth/tulsidas/ramcharitmanas/meanings/hi-gitapress.json` (and en) — they must pass.

Final reply (short): verses checked, number of problems by kind, and the three most serious.
