# BhaktiDhaam (YouTube lCwPg0LRRjk): the track and hand-checked starts

**The track** (`recordings.json` start 1479.26, end 1790.53: 24:39.26–29:50.53 of the 3028-s video lCwPg0LRRjk): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1478.89–1479.26 s, after it the fade to −42 dB at 1790.53 (no silence: the next song starts at 1790.55) s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript. The starts below were found by hearing the stretch in 5-s windows a second apart (Whisper small, the ONNX export: `tools/audio/windows.py`): a transcript segment's start is not the line's.

| Verse | Start | Evidence |
|---|---|---|
| chalisa.cau17 | 1609.4 | windows from 1606 to 1609 s begin "के हरी वाहन सो हे भावानी", the one from 1610 s "बीर चलत": the line starts at about 1609.4 s (MMS 1609.40, score 0.498, just under the 0.5 it needs, so the transcript's early start was in use) |
| chalisa.cau33 | 1732.4 | windows from 1729 to 1732 s begin "शाएरे नागती…" (शरणागत हुई कीर्ति बखानी), the one from 1733 s "अगतिख हुई": the line starts at about 1732.4 s; the ones from 1726 and 1727 s hear no words (the transcript's start, 1726.0, was early); MMS 1732.47 agrees (score 0.444) |
