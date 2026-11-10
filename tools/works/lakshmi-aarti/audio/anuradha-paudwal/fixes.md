# Anuradha Paudwal (YouTube sd31yGqZFlA): the track and hand-checked starts

**The track** (`recordings.json` start 1998.25, end 2330.25: 33:18.25–38:50.25 of the 3641-s video sd31yGqZFlA): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1997.91–1998.25 s, after it 2330.25–2330.57 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript. The starts below were found by hearing the stretch in 5-s windows a second apart (Whisper small, the ONNX export: `tools/audio/windows.py`): a transcript segment's start is not the line's.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 2012.4 | windows from 2010 to 2012 s begin "ॐ जय लक्ष्मी माता", the one from 2013 s "जे लख्ष्मी माथा" (ॐ clipped): the refrain starts at about 2012.4 s, as MMS has it (2012.45, score 0.373, so the transcript's start, its repeat at about 2036, was in use); windows from 2034 to 2036 s hear that repeat |
