# BhaktiDhaam, "सम्पूर्ण चालीसा संग्रह" (YouTube lCwPg0LRRjk): hand-checked starts

**The track** (`recordings.json` start 1790.55, end 2108.6: 29:50.55–35:08.60 of the 3028-s video lCwPg0LRRjk): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it the fade at 1790.53 s, after it 2108.60–2109.07 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The track: 29:50–35:09 (1790–2109 s; the previous track fades out at 1790 s, this one fades out after chaupāī 40 at 2104.5–2109 s). Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript's matches (the identify transcript, `transcripts/lCwPg0LRRjk.jsonl`).

| Verse | Start | Evidence |
|---|---|---|
| chalisa.cau1 | 1802.72 | "जैसन तो शी माजग जननी" = जय संतोषी मां जग जननी; the automatic alignment found nothing before chaupāī 9. Heard in 5-s windows: windows from 1799.7 to 1802.7 s begin “जेसन्तोशी माजग जननी” (जय संतोषी मां जग जननी), the one from 1803.7 s “तो शीमा जग जननी खल मती” (…संतोषी मां जग जननी खल मति, its middle): the line starts at about 1802.7 s; MMS (1804.17) is late. |
| chalisa.cau23 | 1968.6 | windows from 1965 to 1968 s hear the line before's end ("…भव तरनी") and then "चित लगाए", the one from 1969 s begins "तुमे जो…": the line starts at about 1968.6 s (the hand start 1967.8 was a transcript segment's); MMS 1969.06 agrees |
| chalisa.cau33 | 2049.4 | windows from 2041 to 2044 s hear the line before's end and then no words, those from 2045 to 2049 s begin "जो सुमिरत जैसी मनभावा", the one from 2050 s "जैसी मनबावा": the line starts at about 2049.4 s (the transcript's start, 2043.0, was early); MMS 2049.07 agrees (score 0.481) |

Chaupāīs 5–8 are not in the transcript (no segment from 1827.72 to 1857.72 s): placed by length between chaupāīs 4 and 9 and listed to check (the tune puts them at 1833.3, 1839.4, 1845.4, 1851.4 s).

Not sung: the opening dohā (windows from 1791 to 1797 s hear no words; those from 1799 s begin "जय संतोषी माँ जग जननी", chaupāī 1), so the recording starts at chaupāī 1 (`recordings.json` "from") and the dohā has no time; and the closing dohā (the track fades out right after chaupāī 40; it stays untimed).

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| chalisa.cau10 | the window from 1869 s still hears the line before ("…जाए नसाई"), the one from 1870 s begins "वेद पुरान रहे": about 1870.3 s; MMS 1870.66 |
| chalisa.cau11 | the window from 1876 s begins "ब्रम्हाडिंग सर स्वती", the one from 1877 s "अदिंग…": about 1876.3 s; MMS 1876.72 |
| chalisa.cau12 | the window from 1882 s begins "शिवदिन गिर जारुप", the one from 1883 s "वदिन…": about 1882.3 s; MMS 1882.84 |
