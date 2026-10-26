# Split Gita Press English translation per verse

Each file `split/chunkNN.txt` (made by `split/prep.py` from `app_data.json`) holds groups. In a group, several Ramcharitmanas verses (ITEM 0..n-1, usually chaupais) share ONE English paragraph from the Gita Press English edition. That paragraph is pre-cut into numbered segments (SEG 0..m-1) at sentence / semicolon / colon boundaries. For each ITEM you get its transliteration (TR) and its Gita Press Hindi meaning (HI).

Your job: decide where the English for each item begins, so each verse gets the part of the English that translates it.

Use the transliteration (names, key words) and the Hindi meaning to match content. The English follows the verse order, so boundaries are monotone.

## Output
For each group write the start position of every item, as a list of length n:
- first entry is always 0
- each entry is a SEG index `j` (item starts at the start of SEG j), or `"j:w"` when the item must start in the middle of SEG j at word index w (0-based, words split on single spaces). Use "j:w" only when a segment clearly spans two verses (e.g. a comma-joined sentence) — otherwise prefer whole segments.
- strictly increasing positions; every item must get at least one word.
- If a sentence truly translates two verses jointly and cannot be divided, give it to the earlier verse and start the next verse at the next segment.

Write JSON to `split/out_NN.json` (NN = chunk number) as {"<group number>": [starts...], ...} covering EVERY group in that chunk. Do one chunk file at a time, and write its output before moving on. Work through the groups by reading them yourself and judging the content; do not write a heuristic script to guess the splits (reading the file with a script to list groups is fine). Don't change any text. Then validate with a quick python check: every group present, list length = item count, first is 0, increasing.

Report in one line per chunk: groups done, and any group you found ambiguous.
