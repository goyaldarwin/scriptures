<!-- The third step for each batch of a Sanskrit work's reviewed meanings (docs/HOW-TO.md, "Write our own meanings for a Sanskrit work"). Paths are relative to the repository root. -->
# Brief for the copy audit of our own meanings of a Sanskrit work

A batch has been written and reviewed. You check it for copying: `overlap.py` catches a run of 10+ words in common with a copied translation, but misses a sentence that follows one clause by clause with words swapped. The owner's first rule is **accuracy**, and accuracy is never traded for distance from another translation: you change **wording**, never **sense**.

**Before anything else:** `python3 tools/meanings/sanskrit_dict.py fetch && python3 tools/meanings/sanskrit_dict.py check`; if it fails, stop and report it. Read `tools/meanings/style.md` and the works table in `tools/meanings/briefs/sanskrit-writer.md` (each work's copied sources).

## What to read
For every id in `batch-NN.ids`, our final English for each line — `batch-NN.en.json` with the fixes of `batch-NN.review.jsonl` applied on top (a line with lang en, `line` and a non-empty `fix` replaces that piece) — side by side with each copied translation of the work:
`python3 -c "import json,sys; L=sys.argv[1]; S=[json.load(open(L+'/meanings/'+s+'.json'))['m'] for s in sys.argv[2].split(',')]; [print(i, *['\n  '+str(x.get(i)) for x in S]) for i in sys.argv[3:]]" <library folder> <source,source> <ids…>`
(`en-besant,en-telang` for the Gītā; `en-pargiter` for the Saptaśatī). Our Hindi has no copied Hindi source in these works: read it only for the same habit, a Hindi sentence that is a word-for-word rendering of one of theirs.

## What to flag
A sentence of ours that follows theirs: the same sentence shape and order of clauses, the same added ideas or bracketed insertions, their unusual word choices or archaic turns, with words swapped. **Not** a sentence that matches theirs only because both say what the verse says, and **not** the same reading: the sense of the verse belongs to no one.

## How to rewrite a flagged piece
From the verse itself, in our own sentence shape, keeping exactly the same sense (subject, object, speaker, addressee, tense, number, every clause, nothing added). Change as little as needed; never a less accurate reading, a rarer word or a stiffer sentence just to look different. Keep the line division and `style.md`. Read the new piece against the verse once more before you write it down.

## Output
`batch-NN.audit.jsonl` in the batch folder, one line per rewritten piece: `{"id", "lang": "hi"|"en", "kind": "copy", "problem", "line", "fix"}` (`fix` is the complete new piece for that line). An empty file if nothing needs rewriting. Then put all final pieces (review and audit fixes applied) in a scratch copy and run `tools/meanings/overlap.py` against each copied source: 0 runs of 10+. Do not edit the repository; name any helper file with the work and batch.

Reply in under 60 words: verses read, pieces rewritten (hi/en).
