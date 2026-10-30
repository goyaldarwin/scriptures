<!-- The fourth step for each batch of the Mānas (docs/HOW-TO.md, "Write our own meanings for a kāṇḍa of the Mānas"). Paths are relative to the repository root. -->
# Brief for the accuracy and dictionary check of our own meanings of the Śrī Rāmacaritamānasa

A batch has been written, reviewed and copy-audited. A piece reworded to avoid a copy can drift from the verse, so you read the final text once more against the verse and the dictionaries. Accuracy and consistency come first, always.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`; if it fails, stop and report it. Read `tools/meanings/style.md`.

## The final text
`batch-NN.hi.json` / `.en.json`, with the fixes of `batch-NN.review.jsonl` and then `batch-NN.audit.jsonl` applied on top (a line with lang hi/en, `line` and a non-empty `fix` replaces that piece; the audit's wins). The verses, their nearby verses and our word meanings are in `batch-NN.md`.

## What to check
1. **Every piece the copy audit rewrote**, against its verse and its context in the work overall and in the nearby verses: subject, object, speaker, addressee, tense, number, every clause, nothing added or lost. Fix any that drifted, in our own wording (do not move it back to Gita Press's sentence shape).
2. **The hard words of the batch:** look up with `python3 tools/meanings/sanskrit_dict.py look <word> …` (Devanagari; try the stem) every word of each Sanskrit verse, and in the Avadhī verses every Sanskrit or Sanskrit-derived word whose sense is not obvious, every compound epithet, and every word in `batch-NN.words.jsonl` or the review's "word" lines. Fix a piece only when the dictionaries and the grammar show it is wrong (sense, case, number, a compound split wrongly), not for taste.
3. Keep the line division, `style.md`, and the copy rule (no sentence of Gita Press's, no run of 10+ words: run `tools/meanings/overlap.py` on a scratch copy with your fixes).

## Output
`batch-NN.dict.jsonl` in the batch folder, one JSON object per line:
- `{"id", "lang": "hi"|"en", "kind": "dict", "problem", "line", "fix"}` — `fix` is the complete corrected piece for that line;
- `{"id", "lang": "word", "word", "current", "suggested": {"hi", "en"}, "reason"}` — a word meaning in `library/glossary` to correct or add a sense to (old senses stay: other verses use them);
- `{"id", "lang": "doubt", "issue", "our reading", "alternatives"}` — where the dictionaries leave a real doubt.
An empty file if nothing. Do not edit the repository.

Reply in under 80 words: rewritten pieces checked (and how many were wrong), words looked up, pieces fixed (hi/en), word issues, doubts, overlap result.
