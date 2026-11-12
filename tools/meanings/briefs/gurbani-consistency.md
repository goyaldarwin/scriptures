<!-- The last step for each part of our own meanings of Sri Guru Granth Sahib, after its batches are applied (docs/HOW-TO.md, "Write our own meanings for Sri Guru Granth Sahib"). Paths are relative to the repository root. -->
# Brief for the consistency pass over a part of Sri Guru Granth Sahib

The batches of one part (a raag, or the Nitnem banis) have been written, checked and applied to `tools/works/guru-granth-sahib/meanings/{pa,en}/scriptures.json`. Different writers wrote them; you make the part read as one voice, and one with the rest of the Granth's meanings, without changing any reading.

Read `tools/meanings/style.md` §12, §13 and `tools/meanings/briefs/gurbani-writer.md` (the heading rules). Then, over every verse of the part (ids given by the session) and the meanings already written for the Granth before it:
- **Headings** (raag, ghar, writer; ੴ ਸਤਿਗੁਰ ਪ੍ਰਸਾਦਿ): one form for each, as the writer's brief sets it.
- **Refrains and repeated lines** (the batches' `refrains.json` files are in the batch folder): one rendering each, everywhere.
- **Terms and names:** Naam, Simran, Gurmukh, manmukh, Haumai, Hukam, Shabad, Maya, Saadh Sangat, Dharam Rai; God (ਪ੍ਰਭੂ, ਹਰੀ, ਮਾਲਕ / God, the Lord, the Master) as §12, §13 set them; a term glossed once in the part.
- **ਨਾਨਕ** lines and a Bhagat's signature: §12's three cases, the same in both languages.
- **Notes:** none repeating an earlier note of the part; the same note text where the same term is explained.

Change only wording that breaks consistency; never a reading. Then run `tools/meanings/overlap.py` on a scratch copy with your fixes against each `copied-*.json` of the batch folder: 0 runs of 10+ (a refrain made uniform can make one). Output `consistency.jsonl` in the batch folder: `{"id", "lang": "pa"|"en"|"note", "problem", "line", "fix"}` (the complete piece, or the verse's whole notes), then reply in under 60 words: verses read, pieces changed, what was made consistent.
