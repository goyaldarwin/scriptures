# Anuradha Paudwal, "Jai Santoshi Mata Aarti" (YouTube LCYAyR6EmDI): hand-checked starts

What the recording sings: music to ~9 s; the refrain (8.75–67); stanzas 1–7 (67–278), stanzas 8, 9, 10 (278–362), stanza 5
once more (367–397, a repeat: the light stays on stanza 10 there), stanza 11 (397–421), and the refrain to the end
(421–476); each stanza followed by the refrain's first line. Most starts come from the alignment of
`transcripts/LCYAyR6EmDI.jsonl`, which has nothing before 30 s. Evidence for the others: the same Whisper small model (its
ONNX export, `tools/audio/transcribe_onnx.py`) on 4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| aarti.pad5 | 188.4 | windows from 186 to 188 s begin "शुग्र भार…" (शुक्रवार), the one from 189 s "अज दी": the line starts at about 188.4 s (the hand start 187.0 was a transcript segment's); MMS 188.87 agrees |
| aarti.pad9 | 308.3 | 302.95 "जे सन्तो शीबाता" (the refrain), 308.3 "यान दाए जल तेडा मन्वाचित वल्ग" = ध्यान धरो जाने तेरो मनवांछित फल (the transcript: 308.36); the alignment took 315.84, its repeat |
| aarti.pad11 | 398.4 | windows from 395 to 397 s hear no words of it, the one from 398 s begins "संतोषी माँ की आरती", the one from 399 s none: the line starts at about 398.4 s (the start in use, 396.74, was early) |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.tek | windows from 9 to 12 s begin "जे संतोषी माता", the one from 13 s does not: about 12.3 s; MMS 12.84 |
