# Anuradha Paudwal, "Jai Santoshi Mata Aarti" (YouTube LCYAyR6EmDI): hand-checked starts

What the recording sings: music to ~9 s; the refrain (8.75–67); stanzas 1–7 (67–278), stanzas 8, 9, 10 (278–362), stanza 5
once more (367–397, a repeat: the light stays on stanza 10 there), stanza 11 (397–421), and the refrain to the end
(421–476); each stanza followed by the refrain's first line. Most starts come from the alignment of
`transcripts/LCYAyR6EmDI.jsonl`, which has nothing before 30 s. Evidence for the others: the same Whisper small model (its
ONNX export, `tools/audio/transcribe_onnx.py`) on 4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| aarti.pad5 | 187.0 | 187.0–192.65 "शुब्र भार दिया मानति" = शुक्रवार प्रिय मानत (the transcript: 187.52 "शुप्र भार भी आमानती"); the alignment took 195.52, its second half |
| aarti.pad9 | 308.3 | 302.95 "जे सन्तो शीबाता" (the refrain), 308.3 "यान दाए जल तेडा मन्वाचित वल्ग" = ध्यान धरो जाने तेरो मनवांछित फल (the transcript: 308.36); the alignment took 315.84, its repeat |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.tek | windows from 9 to 12 s begin "जे संतोषी माता", the one from 13 s does not: about 12.3 s; MMS 12.84 |
