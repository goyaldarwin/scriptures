# The Hindu āratīs (one work each)

| Work id | Shelf (`library/…`) | Text from | Language |
|---|---|---|---|
| `ram-aarti` | `hinduism/aarti/rama/ram-aarti` | the owner's jansatta.com printout (three āratīs); two Mānas verses from our Mānas | `bra` (the stuti), `awa`, `hi` |
| `hanuman-aarti` | `hinduism/aarti/hanuman/hanuman-aarti` | **taken from the Sundarakāṇḍa work** (`aarti.*`), never edited here | `hi` |
| `jagdish-aarti` | `hinduism/aarti/vishnu/jagdish-aarti` | text the owner pasted | `hi` |
| `shiv-aarti` | `hinduism/aarti/shiva/shiv-aarti` | the owner's screenshot | `hi` |
| `ganga-aarti` | `hinduism/aarti/ganga/ganga-aarti` | the owner's screenshot | `hi` |

Each āratī is its own work (playbook). They share one exporter because they are built the same way:

```
python3 tools/works/aartis/export.py     # after tools/works/ramcharitmanas/export.py and tools/works/sundarkand/export.py
python3 tools/site/build.py
```

Per work folder: `text.txt` (the verse text; format in `ram-aarti/text.txt`), `meanings/hi.json`, `en.json` (our own meanings, one per verse; the owner gave none), `reconciliation.md` (the source and every change made to it), `senses.json` (optional: the work's own sense of a word whose shared sense doesn't fit, written to `library/<path>/glossary.json`), and `audio/<source>/` (recordings, as for every work: `docs/HOW-TO.md`).

`glossary/<lang>.json`: the words of these āratīs that the shared dictionaries did not have. The exporter adds them to `library/glossary/<lang>.json` and never changes a word already there; it stops if any word of any verse has no meaning. The Rāma stuti (Tulasīdāsa's Vinaya-patrikā) is Braj, so it brought the language `bra` (fallback: Sanskrit).

Verse types: टेक (refrain, `tek`, shown once although it is sung after every stanza) and पद (stanza, `pad`), as in the Sundarakāṇḍa's āratī; the Rāmalalā āratī is in caupāīs (`cau`) and the stuti in chhandas (`cha`), types the app knows from the Mānas.
