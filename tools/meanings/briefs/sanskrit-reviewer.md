<!-- The second step for each batch of a Sanskrit work's reviewed meanings (docs/HOW-TO.md, "Write our own meanings for a Sanskrit work"). Paths are relative to the repository root. -->
# Brief for reviewing our own meanings of a Sanskrit work

Someone else wrote the Hindi and English meanings of a batch of verses. You are the second reader: you did not write them, and your job is to catch every error before the owner sees them. The owner's first rule is **accuracy**, then unambiguity, clarity, consistency. Be exact and sceptical; do not rubber-stamp.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`; if it fails, stop and report it.

## Read first
1. `tools/meanings/briefs/sanskrit-writer.md` — what the writer was asked to do, the works table (library folder, traditional reading, copied sources), the speaker openings and the address rules.
2. `tools/meanings/style.md`, all of it.
3. The batch file `batch-NN.md` and the writer's output: `batch-NN.hi.json`, `.en.json`, `.notes.json`, `.doubts.jsonl`, `.words.jsonl`.

## Check every verse, both languages, against the verse itself
- **Accuracy:** read the Sanskrit yourself. Split every compound and sandhi; check case, number, person, tense and voice; look up any word whose sense you are not certain of in Monier-Williams and Apte (`python3 tools/meanings/sanskrit_dict.py look <word> …`). Right subject, object, speaker, addressee; negations kept; who "he" is.
- **The traditional reading** of the works table is the one given; another materially different reading is at most a footnote.
- **Completeness:** every clause and every meaningful word rendered (an epithet in address included).
- **Nothing added:** no commentary, no moral, no explanation the verse does not say or plainly imply; no bracketed insertions except a rare short gloss. Footnotes are short, factual, the same in both languages.
- **Lines:** one piece per verse line, each under its own line and reading on its own; `""` only where a sentence truly cannot be cut, at the same lines in both languages; the speaker's line gives the opening ("सञ्जयने कहा —" / "Sañjaya said:").
- **Hindi and English agree** with each other in sense.
- **Style sheet and language:** honorifics and address (the Lord says तुम; आप to the Lord and the Devī), joined postpositions, लिये/गये, names, IAST, ṃ, lower-case pronouns for the Lord and the Devī, British spelling, no verse numbers; natural, correct Hindi (gender, agreement) and English.
- **Writer's doubts and word issues:** say for each whether you agree.

## Output (in the same folder; do not edit any other file, and do not edit the writer's files)
`batch-NN.review.jsonl`, one JSON object per problem: `{"id", "lang": "hi"|"en"|"note"|"word"|"doubt", "kind": "error"|"omission"|"addition"|"style"|"language", "problem": "<briefly>", "line": <0-based verse line, for hi/en>, "fix": "<the complete corrected piece for that line, ready to paste>"}`. A footnote line's `fix` is the verse's whole footnotes, `{"hi": [..], "en": [..]}` (both `[]` to remove them). A fix that moves a cut between lines gives one line per changed piece. Report only real problems; a perfect verse gets no line. Then put your fixes in a scratch copy and run `python3 tools/meanings/overlap.py <copy of en> <library folder>/meanings/<source>.json` for each copied source of the works table: 0 runs of 10+.

Final reply (short): verses checked, number of problems by kind, and the three most serious.
