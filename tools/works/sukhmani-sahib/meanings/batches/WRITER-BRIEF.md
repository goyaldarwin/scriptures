# Brief: our own English meaning of the Sukhmani Sahib

You are writing a new English meaning for one batch of Guru Arjan Dev Ji's **Sukhmani Sahib** (Sri Guru Granth Sahib, Ang 262–296), for a free, ad-free scripture-reading app owned by Darwin Goyal. The app now shows Dr. Sant Singh Khalsa's English translation, which is his copyright; ours will replace it. The owner's first rule is **accuracy**, then unambiguity, clarity, consistency.

## Read first
1. `/root/scriptures/tools/meanings/style.md` — especially §1 (the one rule), §2 (what a meaning is), §5 (English), and **§12 (Gurbani)**, which is binding for this work.
2. Our own Hindi meaning of the work, `/root/scriptures/tools/works/sukhmani-sahib/meanings/hi.json` — an aid for understanding (written for this library). Your English must agree with the Gurmukhi first; if our Hindi seems wrong somewhere, follow the Gurmukhi and record it in your doubts file.
3. Your batch file (named in your task): every item with its transliteration and our Gurmukhi word meanings (`library/glossary/pa.json`, which falls back to Sanskrit).

## How to write each item (in this order)
1. **From the Gurmukhi**, with the word meanings and our Hindi: work out each line exactly, and write one English sentence or clause per line, in the line order.
2. **Then, as guidance only, Sant Singh Khalsa's English:**
   `python3 -c "import json,sys; E=json.load(open('/root/scriptures/library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/meanings/en-sant-singh-khalsa.json'))['m']; [print(i,'\n EN:',E.get(i,[''])[0]) for i in sys.argv[1:]]" <ids…>`
   Use it to check your understanding; you may take an interpretation or a well-chosen word. Never his sentences, and never a sentence-by-sentence rewording; render the refrains in your own consistent wording (not his "In the remembrance of God…").
3. **Overlap check** (must end with 0 with a shared run of 10+ words; read every "read …" line and rewrite any that is his phrasing rather than the natural words):
   `python3 /root/scriptures/tools/meanings/overlap.py OUT/batch-NN.en.json /root/scriptures/library/sikhism/gurbani/guru-arjan-dev/sukhmani-sahib/meanings/en-sant-singh-khalsa.json --report`

## Rules
- Everything in style.md §12: Sikh terms as the community uses them (Naam, Simran, Gurmukh, Saadh Sangat, Brahm Giani, Hukam…), glossed once per ashtapadi where needed; God / the Lord; "Nanak" as the Guru's own signature; refrains consistent; lower-case pronouns; British spelling.
- No verse numbers, no quotation marks, no square brackets.
- Do not edit any file in `/root/scriptures`; write only in `/tmp/claude-0/-home-claude/cd79eb26-274e-56b0-afe9-b3ed51c80f1b/scratchpad/sukhmani/`.

## Output (NN = your batch number)
- `batch-NN.en.json`: `{"<id>": "<meaning>"}` — exactly the ids of `batch-NN.ids`, in order, UTF-8, `ensure_ascii=False`.
- `batch-NN.refrains.json`: how you rendered each repeated phrase in your batch: `{"<Gurmukhi phrase>": "<English>"}` (so the four batches can be made consistent).
- `batch-NN.doubts.jsonl`: `{"id", "issue", "our reading", "alternatives"}` per genuine doubt, including any place our Hindi seems wrong (may be empty).
- `batch-NN.words.jsonl`: Gurmukhi word meanings that are wrong or missing the sense a line needs: `{"id", "word", "current", "suggested": {"hi", "en"}, "reason"}` — keep every existing sense and add, separated by " / ".
- Final reply (short): items written, overlap result, doubts and word issues counted.
Before finishing, verify with python: the file loads, exact ids in order, no empty values.
