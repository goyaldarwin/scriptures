<!-- The fourth step for each batch of our own meanings of Sri Guru Granth Sahib (docs/HOW-TO.md, "Write our own meanings for Sri Guru Granth Sahib"). Paths are relative to the repository root. -->
# Brief for the accuracy check of our own meanings of Sri Guru Granth Sahib

A batch has been written, reviewed and copy-audited. A piece changed by a later step can drift from the Gurmukhi, so you read the final text once more against the line, its grammar, its context and the commentaries. Accuracy comes first, always.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check` and `python3 tools/meanings/teeka.py fetch <scriptures-data checkout>`; if either fails, stop and report it. Read `tools/meanings/briefs/gurbani-writer.md` (the materials, the rules) and `tools/meanings/style.md` §12, §13.

## The final text
`batch-NN.pa.json` / `.en.json` / `.notes.json`, with the fixes of `batch-NN.review.jsonl` and then `batch-NN.audit.jsonl` applied (a line with lang pa/en, `line` and a non-empty `fix` replaces that piece; a "note" line replaces the verse's notes; the later step wins).

## What to check
1. **Every piece the review or the audit changed**, against its line and its shabad: subject, object, speaker, addressee, mood, number, every word accounted for, nothing added. Fix any that drifted.
2. **Every verse once more, as a whole:** does the meaning carry the Rahao's thought and the speaker through? Is every line's grammar right (endings, number, person, mood, negation)? For every word whose sense is not certain, and every word of `batch-NN.words.jsonl` or the review's "word" lines: the Darpan's and the Faridkot Teeka's glosses (`teeka.py look`), the Santhya and the Shabdarth (`grep -n` in the checkout), the dictionaries. Fix a piece only where the Gurmukhi, its grammar and the materials show it is wrong, not for taste.
3. Keep the line division, the style sheet, and the copy rule (`overlap.py` on a scratch copy with your fixes, against each `copied-*.json` of its language: 0 runs of 10+).

## Output
`batch-NN.dict.jsonl` in the batch folder, one JSON object per line:
- `{"id", "lang": "pa"|"en", "kind": "dict", "problem", "line", "fix"}` — the complete corrected piece;
- `{"id", "lang": "note", "kind": "dict", "problem", "fix": {"pa": [..], "en": [..]}}` — the verse's notes, whole;
- `{"id", "lang": "word", "word", "current", "suggested": {"pa", "en"}, "reason"}`;
- `{"id", "lang": "doubt", "issue", "our reading", "alternatives", "decided because"}` — a reading you decided.
An empty file if nothing. Do not edit the repository.

Reply in under 80 words: pieces checked (and how many were wrong), words looked up, pieces fixed (pa/en), word issues, doubts, overlap result.
