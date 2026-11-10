# BhaktiDhaam, "सम्पूर्ण चालीसा संग्रह" (YouTube lCwPg0LRRjk): hand-checked starts

**The track** (`recordings.json` start 2109.07, end 2710.08: 35:09.07–45:10.08 of the 3028-s video lCwPg0LRRjk): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 2108.60–2109.07 s, after it 2710.08–2710.89 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The text is the version sung (`../../reconciliation.md`). Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript's matches (the identify transcript, `transcripts/lCwPg0LRRjk.jsonl`).

| Verse | Start | Evidence |
|---|---|---|
| chalisa.do2 | 2136.8 | "जैया जैया श्रेशनी देव प्रभ हो" = जय जय श्री शनिदेव प्रभु; the automatic alignment took its second half (सुनहु विनय महाराज, 2143.8 s). |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| chalisa.cau17 | windows from 2363 to 2365 s begin "बारी दशा" (भारी दशा), the one from 2366 s "वीदशा": about 2365.3 s; MMS 2365.44 |
