# The Hindu āratīs (one work each)

| Work id | Shelf (`library/…`) | Text from | Language |
|---|---|---|---|
| `shri-ramchandra-kripalu` | `hinduism/aarti/rama/shri-ramchandra-kripalu` | the owner's jansatta.com printout; the two closing Mānas verses from our Mānas | `bra` (+ `awa`) |
| `ramlala-aarti` | `hinduism/aarti/rama/ramlala-aarti` | the same printout | `awa` |
| `ramchandra-aarti` | `hinduism/aarti/rama/ramchandra-aarti` | the same printout | `hi` |
| `hanuman-aarti` | `hinduism/aarti/hanuman/hanuman-aarti` | **taken from the Sundarakāṇḍa work** (`aarti.*`), never edited here | `hi` |
| `jagdish-aarti` | `hinduism/aarti/vishnu/jagdish-aarti` | text the owner pasted | `hi` |
| `shiv-aarti` | `hinduism/aarti/shiva/shiv-aarti` | the owner's screenshot | `hi` |
| `ganga-aarti` | `hinduism/aarti/ganga/ganga-aarti` | the owner's screenshot | `hi` |

Each āratī is its own work (playbook), even when several come from one page (the three Rāma āratīs: owner, 2026-10-24). They share one exporter because they are built the same way:

```
python3 tools/works/aartis/export.py     # after tools/works/ramcharitmanas/export.py and tools/works/sundarkand/export.py
python3 tools/site/build.py
```

Per work folder: `text.txt` (the verse text; format in `shri-ramchandra-kripalu/text.txt`), `meanings/hi.json`, `en.json` (our own meanings, one per verse; the owner gave none), `reconciliation.md` (the source and every change made to it), `senses.json` (optional: the work's own sense of a word whose shared sense doesn't fit, written to `library/<path>/glossary.json`), and `audio/<source>/` (recordings, as for every work: `docs/HOW-TO.md`).

`glossary/<lang>.json`: the words of these āratīs that the shared dictionaries did not have. The exporter adds them to `library/glossary/<lang>.json` and never changes a word already there; it stops if any word of any verse has no meaning. The Rāma stuti (Tulasīdāsa's Vinaya-patrikā) is Braj, so it brought the language `bra` (fallback: Sanskrit).

Verse types: टेक (refrain, `tek`, shown once although it is sung after every stanza) and पद (stanza, `pad`), as in the Sundarakāṇḍa's āratī; the Rāmalalā āratī is in caupāīs (`cau`) and the stuti in chhandas (`cha`), types the app knows from the Mānas.

## Recordings (the owner's files, 2026-10-23; transcribed with `tools/audio/transcribe_onnx.py`)
| Work | Source | Video | State |
|---|---|---|---|
| jagdish-aarti | `mahendra-kapoor` | XOHdvjVkBdE | live; 3 starts fixed (`fixes.md`) |
| ganga-aarti | `anuradha-paudwal` | 5X_cMif5qPM | live; the refrain fixed |
| shri-ramchandra-kripalu | `satya-adhikari` | J5cllhBiAV0 | live for the stuti and the two Mānas verses only (`from`/`to`, `"align": "anchors"`) |
| shiv-aarti | `anuradha-paudwal` | Yb2GMwJyGnE | **draft**: sings another version of the āratī (`fixes.md`) |
| hanuman-aarti | `ashwin-pathak` | QjSpUgnEPLU | taken from the Sundarakāṇḍa's timings by `export.py` |

Not used: "Aarti Kije Ram Ki – Ram Mandir Ayodhya Aarti" (3_QR2HxO3N4). It shares the refrain "आरती कीजे श्रीरामलला की" but sings other stanzas ("नारायण नर तन धर आए … कौशल्या सुत राजीव लोचन …"), which are not in our text.
The recordings themselves belong in scriptures-data at each `recordings.json` → `data` (to add).
