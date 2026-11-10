# Brief: the Punjabi sense of a batch of Gurbani word meanings (`library/glossary/pa.json`)

You add the `pa` (Punjabi) sense to each word of one batch of our Gurbani word meanings. Each entry already has `hi`
and `en`; the app shows `pa` beside them on the word sheet and in the word list while the ਪੰ switch is on
(`docs/design/languages.md` §2).

Read first: `tools/meanings/style.md` §11 (word meanings) and §13 (Punjabi), `docs/LIBRARY.md` §5 (the entry format).

The batch file (`batch-NN.md`) gives, for each word: its entry (`hi`, `en`, grammar `g`), up to three lines where it
occurs (Sukhmani Sahib, Japji Sahib, then the Granth by Ang) and the word glosses (ਪਦਅਰਥ) of Prof. Sahib Singh's Darpan
and the Faridkot Teeka found for it. `python3 tools/meanings/teeka.py look WORD --lines 3` finds more (after
`teeka.py fetch`).

For each word:
- **The senses:** one Punjabi sense for each sense of the entry, in the same order, separated by " / " as `hi` is
  (ਜਾਹੂ-like entries list every sense the works use). Short: a word or a few, as `hi` is; the grammar of `g` (a noun
  as a noun, a verb form as that verb form, an address as an address: ਹੇ …).
- **Today's standard Punjabi** in Gurmukhi (Unicode, NFC), as §13 sets it: ਵਿੱਚ, ਸ਼ where modern spelling has it,
  no Hindi word where Punjabi has its own, not the teeka idiom. Sikh terms as Punjabi readers use them (ਨਾਮ, ਹੁਕਮ,
  ਹਉਮੈ, ਸਾਧ ਸੰਗਤ …); God as §13 (ਪ੍ਰਭੂ, ਮਾਲਕ).
- **Checked against the lines:** the sense must fit the lines given. A commentary gloss is a fact (a sense, a
  grammar); take its sense, never more than its single word or short phrase of wording.
- **If the entry's `hi` or `en` looks wrong** for the lines, say so in `issue` (what is wrong, the evidence); still
  write `pa` for every sense the lines need (the reviewer gives the matching `hi` and `en`).
- **If neither the lines nor the commentaries settle the sense** (no gloss, glosses that disagree, a rare word), add
  `"mk": true`: the session checks it in the Mahan Kosh.

Write `batch-NN.pa.jsonl` beside the batch, one line per word in the batch's order:
`{"k": "<word>", "pa": "<sense / sense>"}`, with `"issue"` and `"mk"` only when they apply. Check that every key of
`batch-NN.keys` has exactly one line and every `pa` is Gurmukhi and NFC. Edit no file in the repository. Reply in
under 80 words: words written, how many marked `mk`, how many `issue`s.
