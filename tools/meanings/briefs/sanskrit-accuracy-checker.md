<!-- The fourth step for each batch of a Sanskrit work's reviewed meanings (docs/HOW-TO.md, "Write our own meanings for a Sanskrit work"). Paths are relative to the repository root. -->
# Brief for the accuracy and dictionary check of our own meanings of a Sanskrit work

A batch has been written, reviewed and copy-audited. A piece reworded by a later step can drift from the verse, so you read the final text once more against the verse, the grammar and the dictionaries. Accuracy and consistency come first, always.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`; if it fails, stop and report it. Read `tools/meanings/style.md` and `tools/meanings/briefs/sanskrit-writer.md` (the works table and the rules).

## The final text
`batch-NN.hi.json` / `.en.json` / `.notes.json`, with the fixes of `batch-NN.review.jsonl` and then `batch-NN.audit.jsonl` applied on top (a line with lang hi/en, `line` and a non-empty `fix` replaces that piece; a "note" line replaces the verse's footnotes; the audit's wins). The verses, the verses before them and our word meanings are in `batch-NN.md`.

## What to check
1. **Every piece the review or the copy audit changed**, against its verse and its context: subject, object, speaker, addressee, tense, number, every clause, nothing added or lost. Fix any that drifted, in our own wording.
2. **Every verse's Sanskrit, word by word:** look up with `python3 tools/meanings/sanskrit_dict.py look <word> …` (Devanagari; try the stem) every word whose sense is not certain, every compound, every word in `batch-NN.words.jsonl` or the review's "word" lines. Fix a piece only when the dictionaries and the grammar show it is wrong (sense, case, number, a compound split wrongly, a negation lost), not for taste.
3. Keep the line division, `style.md`, and the copy rule (run `tools/meanings/overlap.py` on a scratch copy with your fixes against each copied source of the work: 0 runs of 10+).

## Output
`batch-NN.dict.jsonl` in the batch folder, one JSON object per line:
- `{"id", "lang": "hi"|"en", "kind": "dict", "problem", "line", "fix"}` — `fix` is the complete corrected piece for that line;
- `{"id", "lang": "note", "kind": "dict", "problem", "fix": {"hi": [..], "en": [..]}}` — the verse's footnotes, whole;
- `{"id", "lang": "word", "word", "current", "suggested": {"hi", "en"}, "reason"}` — a word meaning to correct or add a sense to (old senses stay: other verses use them);
- `{"id", "lang": "doubt", "issue", "our reading", "alternatives"}` — where the dictionaries leave a real doubt.
An empty file if nothing. Do not edit the repository.

Reply in under 80 words: pieces checked (and how many were wrong), words looked up, pieces fixed (hi/en), word issues, doubts, overlap result.
