<!-- The step after all batches of a kāṇḍa are applied (docs/HOW-TO.md, "Write our own meanings for a kāṇḍa of the Mānas"). Paths are relative to the repository root. -->
# Brief for the consistency pass over a kāṇḍa of our own Mānas meanings

The kāṇḍa's batches, written by different writers, have been applied to `tools/works/manas/meanings/hi/scriptures.json` and `en/scriptures.json` (one piece per verse line), with headings in `tools/works/manas/topics.json`. Make the kāṇḍa read as one voice with the rest of the Mānas. Read `tools/meanings/style.md` and `docs/PLAYBOOK.md` §4–5 first.

## Against what
`style.md`, the owner-approved Sundarakāṇḍa entries (ids `sundar.`), and the published entries of the other kāṇḍas in the same files.

## What to make consistent
- Straight apostrophes (') only.
- Names one way throughout, Hindi and English: the `style.md` form, else the form the other kāṇḍas use, else the majority (बालि / Vāli the monkey king, बलि / Bali the king Vāmana bound).
- Epithets (Raghu-epithets → "Śrī Rāma" in narration; श्रीहरि / "Śrī Hari" for हरि; संभु → शिवजी / Śiva), honorifics (हनुमान्‌जी with ZWNJ U+200C; श्रीरामजी, सीताजी, लक्ष्मणजी, भरतजी), each speaker's tone.
- The speaker named when speech starts or changes ("X ने कहा —" / "X said:"); the frame (Śiva to Pārvatī, Kākabhuśuṇḍi to Garuḍa) named when it changes.
- Refrains and stuti epithets rendered the same way each time; māyā glossed at most once in the kāṇḍa; British spelling; no exclamation marks where `style.md` disallows them.
- Headings: short, correct, well-formed.

## How
- Change only what is inconsistent; keep each piece's meaning and the number of pieces per verse; do not move a piece toward Gita Press's wording. Do not touch entries of other kāṇḍas, or an owner-approved entry except for a plain spelling.
- Edit with a Python script that asserts each old string exists before replacing, and write with `tools/jsonio.py` (`dump_meanings`).
- Then run `python3 tools/meanings/overlap.py tools/works/manas/meanings/hi/scriptures.json library/hinduism/granth/tulsidas/ramcharitmanas/meanings/hi-gitapress.json` (and en): 0 runs of 10+. Read this kāṇḍa's sentences it lists as nearly theirs, and reword any that follow Gita Press's sentence rather than simply the verse.

Reply in under 120 words: what you changed (counts by kind), sentences reworded, overlap result. Do not commit.
