<!-- The third step for each batch of our own meanings of Sri Guru Granth Sahib (docs/HOW-TO.md, "Write our own meanings for Sri Guru Granth Sahib"). Paths are relative to the repository root. -->
# Brief for the copy audit of our own meanings of Sri Guru Granth Sahib

A batch has been written and reviewed. You check that its wording is our own. **Be lenient** (the owner): the sense of a line belongs to no one, and two faithful renderings of a short Gurbani line often use the same words. You change **wording**, never **sense**, and only where it is plainly someone else's.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`; if it fails, stop and report it. Read `tools/meanings/style.md` §1, §9, §12, §13.

## What to read
For every id in `batch-NN.ids`, our final pieces (`batch-NN.pa.json` / `.en.json` with the fixes of `batch-NN.review.jsonl` applied: a line with lang pa/en, `line` and a non-empty `fix` replaces that piece) beside `batch-NN.refs.md` (the published translations, line by line).

## What to flag (only this)
- A run of 10 or more words in common with one of them (`overlap.py` finds it). A run made only of the fixed Ik Oankar sentence and the settled heading after it is not one.
- A sentence that is plainly theirs with words swapped: their unusual word choices, their bracketed additions, their particular turn of phrase, followed clause by clause.

**Not** to flag: the same reading; the natural words for a short line; a name, a term, a list, or the line's own order; a phrase of six to nine words that is simply how one says it. When in doubt, leave it.

## How to rewrite a flagged piece
From the Gurmukhi itself, in our own sentence shape, keeping exactly the same sense (subject, object, speaker, addressee, mood, number, every clause, nothing added). Change as little as needed; never a less accurate reading, a rarer word or a stiffer sentence. Read the new piece against the line once more.

## Output
`batch-NN.audit.jsonl` in the batch folder, one line per rewritten piece: `{"id", "lang": "pa"|"en", "kind": "copy", "problem", "line", "fix"}`. An empty file if nothing needs rewriting (the usual case). Then run `tools/meanings/overlap.py` on a scratch copy of the final pieces against each `copied-*.json` of its language: 0 runs of 10+. Do not edit the repository.

Reply in under 60 words: verses read, pieces rewritten (pa/en).
