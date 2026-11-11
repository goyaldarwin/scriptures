# Anuradha Paudwal, "Aarti Vol. 2" (YouTube faxIif-3F8o, 19:07–30:54): hand-checked starts

**The track** (`recordings.json` start 1100.85, end 1853.38: 18:20.85–30:53.38 of the 3712-s video faxIif-3F8o): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1097.00–1100.85 s, after it 1853.38–1860.15 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The transcript (`transcripts/faxIif-3F8o.jsonl`, the identify run) begins each segment where the one before ended, so a stanza after an instrumental interlude is placed seconds early or on the refrain before it, and it missed some lines. The starts below come from a second transcription of the same stretches with Whisper small (`tools/audio/transcribe_onnx.py`), which cuts the audio into 4–9 s pieces at its quiet points: the time is the start of the piece in which the verse's first words are heard (the pieces before it are music). Starts not listed here come from the transcript. To be set by ear.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 1147.0 | 1147.0 "जग जए मनी जे जे माँ", 1150.0 "माजब जननी जेजे · भायगारिनी भावतारिनी" = जगजननी जय जय, (माँ) जगजननी जय जय, भयहारिणि भवतारिणि; 1099.4–1147.0 music. The transcript has nothing before 1180.6. Heard in 5-s windows: windows from 1144 to 1147 s begin “जग जए में लिजे जे माँ” (जगजननी जय जय माँ), the one from 1148 s “वज़नी जे जे…” (…जननी जय जय, its middle), and from 1150 s the line sung again: the line starts at about 1147 s. |
| aarti.pad3 | 1320.5 | 1320.5 "अभी तारी अगवारी" = अविकारी अघहारी; 1301.3–1320.5 music and vocalise. Heard in 5-s windows: windows from 1317.5 to 1320.5 s begin “अभी तारी आद़़ारी” (अविकारी अघहारी), the one from 1322.5 s “अगर कला ता” (…अकल कलाधारी, its middle): the line starts at about 1320.5 s. |
| aarti.pad9 | 1624.0 | 1624.0 "तुही स्नी है सुदा मैं · तुवति गर्ल मना" = तू ही स्नेह-सुधामयि तू अति गरलमना; the automatic match took the refrain before it (1599). Heard in 5-s windows: windows from 1621 to 1624 s begin “तुही स्नी है सुदा मैं” (तू ही स्नेह-सुधामयि), the one from 1625 s “तुवति अगर तुवति” (तू अति…, its middle): the line starts at about 1624 s. |
| aarti.pad10 | 1674.7 | 1674.7 "मुडा दार निवास्णी · इह बरे सी भी प्रदे" = मूलाधारनिवासिनि इह-पर-सिद्धिप्रदे; 1654.9–1674.7 music and vocalise. Heard in 5-s windows: windows from 1672.7 to 1675.7 s begin “मुडा दार निवासिनी” (मूलाधारनिवासिनि), the one from 1676.7 s “अगर निवासिनी यहाम बरे से” (…निवासिनि इह-पर, its middle): the line starts between 1674.7 and 1675.7 s. |
| aarti.pad11 | 1725.3 | 1725.3 "शाएटी शक्ति दर किवी" = शक्ति शक्तिधर तू ही; 1706.3–1725.3 music and vocalise. Heard in 5-s windows: windows from 1724.3 to 1725.3 s begin “शाएक्ती शाक्ती दर किवी” (शक्ति शक्तिधर तू ही), the one from 1726.3 s no words: the line starts at about 1725.3 s. |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.pad7 | windows from 1520 to 1522 s begin "ती पर गाम निवासिनी" (तू परधामनिवासिनि), the one from 1523 s "प्रगाम…": about 1522.4 s; MMS 1523.08 |
