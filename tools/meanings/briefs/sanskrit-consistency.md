<!-- The step after all batches of a Sanskrit work are applied (docs/HOW-TO.md, "Write our own meanings for a Sanskrit work"). Paths are relative to the repository root of the worktree named in your task. -->
# Brief for the consistency pass over a Sanskrit work's meanings

The work's batches, written by different writers, have been applied to `tools/works/<work>/meanings/hi/scriptures.json` and `en/scriptures.json` (one piece per verse line, footnotes in `notes`). Make the whole work read as one voice. Read `tools/meanings/style.md` and `tools/meanings/briefs/sanskrit-writer.md` first.

## What to make consistent, across the whole work
- **The same words rendered the same way:** names (one spelling, Hindi and English), epithets in address (हे कौन्तेय! / "O son of Kuntī"; हे महाबाहो! / "O mighty-armed one"; हे भारत! / "O Bhārata"), recurring terms and their glosses, weapons (one English word for one Sanskrit weapon in every chapter), refrains and repeated lines (the same Sanskrit line has the same meaning wherever it recurs).
- **Speaker openings:** the speaker's line gives "Xने कहा —" / "X said:" exactly as the writer's brief sets them; nothing added (no name the verse does not give).
- **The closing words (iti) of every chapter** in one pattern, Hindi and English: the English says "chapter" (a common noun is translated, `style.md` §5), never "adhyāya"; the Hindi says अध्याय. Take the best-formed one as the model and make the others match, keeping each chapter's own name and number.
- **Capitals:** class nouns of beings in lower case in English, like "asura": daitya, dānava, rākṣasa, yakṣa, gandharva, apsaras, siddha; the gods are "the gods". Names of persons and of the Devī keep their capitals.
- **Hindi:** honorific plural for the Lord, the Devī, sages and elders in narration; the Lord's तुम to Arjuna and others; आप to the Lord and the Devī; joined postpositions; लिये/गये/गयी/दिये; ZWNJ in श्रीभगवान्‌ने and जगत्‌; no nukta in हजार, जोर (house spelling).
- Straight apostrophes in English; British spelling; no quotation marks for speech; no square brackets.

## The work's settled readings (apply them if a piece differs)
Given by the session in your task.

## How
- Change only what is inconsistent; keep each piece's meaning and the number of pieces per verse; never move a piece toward a copied translation's wording.
- Edit with a Python script that asserts each old string exists before replacing, and write with `tools/jsonio.py` (`dump_meanings`).
- Then run `python3 tools/meanings/overlap.py tools/works/<work>/meanings/en/scriptures.json <library folder>/meanings/<source>.json` for each copied source of the works table: 0 runs of 10+.

Reply in under 150 words: what you changed (counts by kind), the iti pattern you chose, overlap result. Do not commit.
