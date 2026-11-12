<!-- The second step for each batch of our own meanings of Sri Guru Granth Sahib (docs/HOW-TO.md, "Write our own meanings for Sri Guru Granth Sahib"). Paths are relative to the repository root. -->
# Brief for reviewing our own meanings of Sri Guru Granth Sahib

Someone else wrote the Punjabi and English meanings of a batch of the Granth. You are the second reader: you did not write them, and your job is to catch every error before the owner sees them. The owner's first rule is **accuracy**, and understanding the context is what makes a meaning right. Be exact and sceptical; do not rubber-stamp.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check` and `python3 tools/meanings/teeka.py fetch <scriptures-data checkout>`; if either fails, stop and report it.

## Read first
1. `tools/meanings/briefs/gurbani-writer.md` — what the writer was asked to do, the materials and how to search them, the heading and refrain rules.
2. `tools/meanings/style.md` §1, §2, §5, §12, §13.
3. `batch-NN.md`, `batch-NN.refs.md` and the writer's output: `batch-NN.pa.json`, `.en.json`, `.notes.json`, `.refrains.json`, `.doubts.jsonl`, `.words.jsonl`.

## Check every verse, both languages, against the Gurmukhi itself
- **Context:** the Rahao's thought carried through the shabad; who speaks to whom (the Guru to God, to the mind, to a pandit or yogi; the soul-bride and the Husband Lord); a vaar's salok and pauri; the verses before.
- **Grammar:** aunkar and sihari endings, number, person, mood (a command stays a command), negations; the right subject and object. Look up any word you are not certain of: the Darpan and the Faridkot Teeka (`teeka.py look`), the Santhya and the Shabdarth OCR (`grep -n` in the checkout), Monier-Williams and Apte, Platts.
- **The reading:** where the writer's reading differs from the commentaries, is the writer's the one the grammar and context bear out? Say so for each of the writer's doubts.
- **Completeness, nothing added:** every word of the line accounted for; no commentary or moral; notes few, short, factual and the same in both languages.
- **Lines:** one piece per line, each reading under its line; Punjabi and English cut at the same lines; headings, ੴ, ਰਹਾਉ and ਨਾਨਕ as the writer's brief and §12 set them; refrains the same each time and as the Granth's meanings already render them.
- **Punjabi and English agree** in sense; natural, correct modern Punjabi (§13) and English (§5, §12).

## Output (in the same folder; do not edit any other file, and do not edit the writer's files)
`batch-NN.review.jsonl`, one JSON object per problem: `{"id", "lang": "pa"|"en"|"note"|"word"|"doubt", "kind": "error"|"omission"|"addition"|"style"|"language", "problem": "<briefly>", "line": <0-based verse line, for pa/en>, "fix": "<the complete corrected piece for that line>"}`. A note line's `fix` is the verse's whole notes `{"pa": [..], "en": [..]}` (both `[]` to remove them). Report only real problems; a perfect verse gets no line. Then run `tools/meanings/overlap.py` on a scratch copy with your fixes against each `copied-*.json` of its language: 0 runs of 10+.

Final reply (short): verses checked, problems by kind, the three most serious.
