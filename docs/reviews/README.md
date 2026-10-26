# Open questions for the owner

Each file lists readings our meanings or word meanings take where a question is still open: the verse or word, the issue, our reading, and the alternatives. The owner decides; a decided question is applied to the data and removed from its file (git keeps the record).

| File | What |
|---|---|
| `dictionary-doubts.jsonl` | word meanings whose sense is not settled (`library/glossary/<lang>.json`): `{k, lang, why}` |
| `ramraksha-doubts.jsonl` | our Hindi and English of the Śrī Rāma Rakṣā Stotram: `{id, issue, our reading, alternatives}` |
| `sukhmani-doubts.jsonl` | our Hindi and English of the Sukhmani Sahib |
| `sukhmani-pa-doubts.jsonl` | our Punjabi of the Sukhmani Sahib, by verse line (`line`) |

A new doubts file is named `<work or topic>-doubts.jsonl`, one JSON object per line.
