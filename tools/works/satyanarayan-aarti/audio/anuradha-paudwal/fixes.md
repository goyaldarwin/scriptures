# Anuradha Paudwal, "Om Jai Jagdish Hare Aarti Sangrah" jukebox (YouTube sd31yGqZFlA): hand-checked starts

**The track** (`recordings.json` start 1634.38, end 1997.91: 27:14.38–33:17.91 of the 3641-s video sd31yGqZFlA): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1634.01–1634.38 s, after it 1997.91–1998.25 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The āratī is the jukebox's track from 27:15 to 33:12 (1635–1992 s). Starts not listed here come from the transcript's anchors.

No start is set by hand.

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.tek | music from the song’s start (1634.38 s); windows from 1646 to 1648 s begin "जे लक्ष्मी रमणा", the one from 1649 s does not: about 1648.4 s; MMS 1648.99 |
| aarti.pad2 | windows from 1732 to 1733 s begin "प्रगट भये", the one from 1734 s does not: about 1733.3 s; MMS 1733.9 |
