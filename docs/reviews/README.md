# Readings still to settle

Each file lists readings our meanings or word meanings take where a question is still open: the verse or word, the issue, our reading, and the alternatives. A session settles each (`docs/PLAYBOOK.md` §2: decide, never leave doubts for the owner) with the dictionaries, the grammar and the commentaries; a settled reading is applied to the data and removed from its file (git keeps the record). A reading a reviewer has agreed with is settled.

| File | What |
|---|---|
| `dictionary-doubts.jsonl` | word meanings whose sense is not settled (`library/glossary/<lang>.json`): `{k, lang, why}` |
| `ramraksha-doubts.jsonl` | our Hindi and English of the Śrī Rāma Rakṣā Stotram: `{id, issue, our reading, alternatives}` |
| `bilvashtakam-doubts.jsonl` | our Hindi and English of the Bilvāṣṭakam, and its numbering |
| `sukhmani-doubts.jsonl` | our Hindi and English of the Sukhmani Sahib |
| `sukhmani-pa-doubts.jsonl` | our Punjabi of the Sukhmani Sahib, by verse line (`line`) |
| `manas-<kāṇḍa>-doubts.jsonl` | our Hindi and English of the Rāmacaritamānasa, one file per kāṇḍa (Araṇya, Ayodhyā, Kiṣkindhā, Laṅkā, Uttara): the writer's `{id, issue, our reading, alternatives}`, the reviewer's `{id, review, reviewer_fix}` and the dictionary check's lines |

A new doubts file is named `<work or topic>-doubts.jsonl`, one JSON object per line.
