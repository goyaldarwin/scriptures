# Shirdi Sāī Bābā — Dhūpa Āratī (evening āratī)

Shelf: हिन्दू धर्म › Āratī › Shirdi Sāī Bābā › Dhūpa Āratī (`library/hinduism/aarti/shirdi-sai/dhoop-aarti/`, work id `shirdi-sai-dhoop-aarti`).

- `text.txt`: the verse text, section by section, with each verse's type and language (`mr` Marathi, `sa` Sanskrit, `hi` Hindi). `reconciliation.md` records how it is settled from the two source printouts.
- `meanings/hi/scriptures.json`, `meanings/en/scriptures.json`: ours, one meaning per verse, written for this library: the only Hindi source (the printouts have no Hindi meaning) and the default English; both cover all 64 verses.
- `meanings/en/shirdisaibabakripa.json`: the English meaning copied from the shirdisaibabakripa.org printout (dhoop.pdf), for 62 of the 64 verses (not the two closing jayaghoṣas, `prarthana.jay2` and `jay3`), still selectable (`order: 2`). How its paragraphs map to our verses and every typo fixed are in `reconciliation.md`.
- `glossary/mr.json`: the work's own senses of Marathi words whose shared entry carries another text's sense; every other word is in `library/glossary/<lang>.json`, by the language of the verse it is in (Marathi and Hindi fall back to Sanskrit).

The folder's format: `tools/works/README.md`.

The work has one part (Dhūpa Āratī). Its pages are the sections (āratī, abhaṅga, namana … the Guru-prasāda-yācanā-daśaka between the Mahimna stotra and the Puṣpāñjali), and each section is also a topic. Verse types are declared in `work.json` → `types` (dhruvapada, pada, abhaṅga, śloka, mantra, jayaghoṣa).

Item ids look like `aarti.pad3` or `mahimna.shloka9` (section, type, number). They are permanent.

Audio (Pramod Medhi):
- `audio/pramod-medhi-times/`: the Times Music upload (YouTube `b_JJzjc2Rgk`), the live source (`order: 1`). Its starts are the owner's, set by ear in the app's timing mode (`owner.json`, written by `tools/audio/apply_owner_timing.py`); `source.json` → `checked`.

## Structure
- **Hierarchy:** one part (Dhoop Aarti) › ten sections, each a composition with its own name (`work.json` → `sections`: Aarti, Shirdi Majhe, Naman, Namasmaran, Namaskarashtak, Aisa Yei Ba, Mahimna, Dashak, Pushpanjali, Prarthana) › its verses.
- **Numbering:** each composition numbers its verses from 1, as the printouts do; a verse is cited by its section's name and its own number ("Namaskarashtak · Stanza 1"), so the reader, the player and search never confuse two "Stanza 1"s. The dhruvapadas have no number.
- **Types** (`work.json` → `types`): dhruvapada, stanza (pad), abhaṅga, śloka, mantra, jayaghoṣa. **Topics:** one per section. **Reading plans:** none.

## Introduction
The readers' introduction (`intro` in `library/index.json`, shown in ⓘ About this work) states only what these support:
- Shri Saibaba Sansthan Trust, Shirdi (https://sai.org.in/sites/default/files/2011e-pages-21-37.pdf): Madhavrao Adkar composed Aarti Saibaba at Shirdi in 1903–04; Baba's blessing.
- The text itself: the sections and the signatures (Madhav, Ganu, Nama, Balkrishna Vishwanath Deo), our text from the owner's two printouts (tools/works/shirdi-sai-dhoop-aarti/reconciliation.md).
