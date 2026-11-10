# Anuradha Paudwal, "Ambe Tu Hai Jagdambe" (YouTube OQ5K_GILwzQ): hand-checked starts

What the recording sings: music to ~11 s; the refrain twice (11–48); stanza 1 and the refrain (53.7–122); stanza 2 and the
refrain (128–196); stanza 3 and the refrain (202–257); the refrain's last line to the end (257–291). The transcript
(`transcripts/OQ5K_GILwzQ.jsonl`) sets its first segment at 0 and holds long segments; the alignment took the refrain's
repeats for stanzas 2 and 3. Evidence: the same Whisper small model (its ONNX export, `tools/audio/transcribe_onnx.py`) on
4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| aarti.pad1 | 53.7 | 48.05 music; 53.7–61.9 "तेरी वाद जनो पे माथा", 61.9 "भीर पडी है पारी" = तेरे भक्त जनों पर माता भीर पड़ी है भारी (the transcript: 55.82) |
| aarti.pad2 | 133.4 | windows from 130 to 133 s begin "मा बेटे का है", the one from 134 s does not, and the one from 129 s hears only "मा बे…": the line starts at about 133 s (the transcript segment began at 128.2); MMS took its repeat at 149.1 |
| aarti.pad3 | 207.6 | the window from 207 s begins "नहीं मागते धन", the one from 208 s "अगते धन": about 207.3 s (the segment began at 202.3); MMS took its repeat at 223.3 |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.tek | windows from 12 to 15 s begin "अम्बे तु है जग जंबे", the one from 16 s with "तु है": the line starts at about 15.3 s; MMS 15.51 (14.91 with the lean) |
