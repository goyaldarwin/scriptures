# BhaktiDhaam, "सम्पूर्ण चालीसा संग्रह" (YouTube lCwPg0LRRjk): hand-checked starts

**The track** (`recordings.json` start 1149.61, end 1478.89: 19:09.61–24:38.89 of the 3028-s video lCwPg0LRRjk): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1148.56–1149.61 s, after it 1478.89–1479.26 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The text is the version sung (`../../reconciliation.md`). Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript's matches (the identify transcript, `transcripts/lCwPg0LRRjk.jsonl`).

| Verse | Start | Evidence |
|---|---|---|

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| chalisa.cau16 | windows from 1283 to 1285 s begin "देवन को अमृत", the one from 1286 s "तो मर्द पान": about 1285.3 s; MMS 1285.42 |
