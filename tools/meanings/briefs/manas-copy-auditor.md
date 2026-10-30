<!-- The third step for each batch of the Mānas (docs/HOW-TO.md, "Write our own meanings for a kāṇḍa of the Mānas"). Paths are relative to the repository root. -->
# Brief for the copy audit of our own meanings of the Śrī Rāmacaritamānasa

A batch has been written and reviewed. You check it for copying: `overlap.py` catches a run of 10+ words in common with Gita Press, but misses a sentence that follows theirs clause by clause with words swapped. The owner's first rule is **accuracy**, and accuracy and consistency are never traded for distance from Gita Press: your job is to change **wording**, never **sense**.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`; if it fails, stop and report it. Read all of `tools/meanings/style.md`, and the owner-approved samples: the `sundar.` entries of `tools/works/manas/meanings/hi/scriptures.json` and `en/scriptures.json`.

## What to read
For every verse id in `batch-NN.ids`, our final piece for each line — `batch-NN.hi.json` / `.en.json` with the fixes of `batch-NN.review.jsonl` applied on top (a line with lang hi/en, `line` and a non-empty `fix` replaces that piece) — side by side with Gita Press's meaning:
`python3 -c "import json,sys; L='library/hinduism/granth/tulsidas/ramcharitmanas/meanings/'; H=json.load(open(L+'hi-gitapress.json'))['m']; E=json.load(open(L+'en-gitapress.json'))['m']; [print(i,'\n HI:',H[i][0],'\n EN:',E.get(i,[''])[0]) for i in sys.argv[1:]]" <ids…>`

## What to flag
A sentence of ours that follows theirs: the same sentence shape and order of clauses, the same added ideas, their bracketed insertions or unusual word choices, with words swapped. **Not** a sentence that matches theirs only because both say what the verse says, and **not** the same reading: the sense of the verse belongs to no one, and where Gita Press reads the verse rightly, ours must say the same thing.

## How to rewrite a flagged piece
- From the verse itself, in our own sentence shape, keeping exactly the same sense: subject, object, speaker, addressee, tense, number, every clause, nothing added (drop their additions that the verse lacks).
- Change as little as needed. Never pick a less accurate reading, a rarer word or a stiffer sentence just to look different.
- Keep the line division, `style.md` (honorifics, names, speech form) and the voice of the Sundarakāṇḍa samples.
- Read the new piece against the verse once more before you write it down.

## Output
`batch-NN.audit.jsonl` in the batch folder, one line per rewritten piece: `{"id", "lang": "hi"|"en", "kind": "copy", "problem", "line", "fix"}` (`fix` is the complete new piece for that line). An empty file if nothing needs rewriting. Then put all final pieces (review and audit fixes applied) in a scratch copy and run `tools/meanings/overlap.py` against `hi-gitapress.json` and `en-gitapress.json`: both must show 0 runs of 10+. Do not edit the repository; name any helper file with your kāṇḍa and batch.

Reply in under 60 words: verses read, pieces rewritten (hi/en). The rewrites then go to the accuracy check (`manas-accuracy-checker.md`).
