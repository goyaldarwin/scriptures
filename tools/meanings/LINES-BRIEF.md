# Brief: divide our meanings into one piece per verse line

The app shows a meaning **line by line**: each line of the verse, then its meaning right under it (the owner: "whatever our line in the verse, its meaning below it wherever present"; the format is `p` in `docs/LIBRARY.md` §3). Your job is to divide our existing, already reviewed Hindi and English meanings of some verses into **one piece per verse line**. You are not re-translating: the meanings are settled; you only cut them at the right places and make each piece read well on its own.

## Inputs
- Verses: the work's `work.json` (named in your task): `items[]` with `id` and `v` (the verse lines, in order).
- Our meanings: `hi.json` and `en.json` (named in your task): `{id: "whole meaning"}`. They follow the verse line by line, so most lines already have their own sentence.
- Style: `tools/meanings/style.md` (§2, §4, §5; §8a for stotras; §12 for Gurbani).

## Rules
1. For every item, produce a list with **exactly as many pieces as the verse has lines** (`len(v)`), in line order: piece k is the meaning of line k.
2. **Nothing lost, nothing added, no change of sense.** Every word of the whole meaning goes into exactly one piece, in order. You may make the smallest change needed where a sentence spans two lines so that each piece stands on its own (e.g. repeat the subject, turn a comma clause into a sentence, move a verb). Do not reword otherwise.
3. **Where the sense of two lines cannot be cut** (one Sanskrit sentence with the verb only in the second line; a phrase running across), keep it together in the piece of the **later** line and give the earlier line `""` — but prefer cutting whenever the lines can carry their own sense (the owner wants the meaning under each line).
4. **Heading lines** with no meaning of their own (Gurbani `ਸਲੋਕੁ ॥`, `ਅਸਟਪਦੀ ॥`, a `॥ ਰਹਾਉ ॥` marker alone on a line): piece `""`. Drop our meanings' opening words "Salok." / "Ashtapadi." and "सलोक।" / "अष्टपदी।" (the verse line itself shows the heading).
5. A line that is only a number or an invocation keeps whatever the whole meaning says for it.
6. Hindi and English must cut at the same lines (both have a piece, or both `""`, for each line).
7. No verse numbers (the exporter adds them), no quotation marks.

## Output (in the folder named in your task)
- `<name>.hi.lines.json`, `<name>.en.lines.json`: `{id: [piece, piece, …]}` for every id in your range, in the work's order, UTF-8, `ensure_ascii=False`.
- Verify with python before finishing: (a) every list has `len(v)` pieces; (b) at least one piece is not empty; (c) Hindi and English have empty pieces at the same lines; (d) for each item, the joined pieces have at least 95% of the original's words in order (`difflib.SequenceMatcher` on word lists ≥ 0.95) — report any item below 0.97 with the reason.
- Final reply (short): items done, how many lines got `""` and why, and any item where you had to change wording at a boundary (list ids).
