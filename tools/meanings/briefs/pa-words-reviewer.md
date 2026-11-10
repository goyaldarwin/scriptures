# Brief: review the Punjabi senses of a batch of Gurbani word meanings

A writer added a `pa` sense to each word of one batch (`batch-NN.pa.jsonl`, by `pa-words-writer.md`; read that brief
and `tools/meanings/style.md` §11 and §13 first). You check every word of the batch file (`batch-NN.md`) against its
lines, its entry and the commentary glosses (`python3 tools/meanings/teeka.py look WORD` for more):
- **Right:** each sense fits the lines and the entry's sense in the same position; the grammar of `g`; nothing missing
  (one Punjabi sense per sense of `hi`, same order, " / " between).
- **Punjabi:** today's standard Punjabi, plain, correctly spelled (ਵਿੱਚ, ਸ਼, ਨੂੰ), no Hindi word where Punjabi has its
  own, not the old teeka idiom; the same Sikh term and the same rendering of a word across the batch.
- **Not copied:** no gloss longer than a word or short phrase taken from the Darpan or the Faridkot Teeka.
- **The writer's `issue`s and `mk` marks:** agree, or say why not.

Write `batch-NN.review.jsonl` beside the batch, one line per word that needs a change:
`{"k": "<word>", "pa": "<the complete corrected sense>", "why": "<the evidence>"}`; a word whose entry (`hi`/`en`) is
wrong for its lines gets `"issue"` as well (your agreement or your own); a word the lines and commentaries cannot
settle gets `"mk": true`. **The three languages keep the same senses:** where `pa` (the writer's or yours) has a sense the entry's `hi`/`en`
lack because a line needs it, the line also carries `"hi"` and `"en"`: the complete corrected entry senses, in the same
order as `pa` (Hindi in Devanagari, English plain), so all three list the same senses. A sense of the entry that no line
of the works uses stays. Words that are right get no line. Edit no file in the repository. Reply in under 80 words:
words checked, changes, `issue`s and `mk`s, the most serious problem.
