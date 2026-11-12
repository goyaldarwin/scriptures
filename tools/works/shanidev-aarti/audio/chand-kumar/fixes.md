# Chand Kumar, "Shani Aarti" (YouTube JtJ4P0302FY): hand-checked starts

What the recording sings: music to ~18 s; the refrain (जय जय श्री शनि देव भक्तन हितकारी · सूरज के पुत्र प्रभु छाया महतारी)
and its first line again (18.7–64); music; stanza 1 and the refrain (93.2–127); music; stanza 2 and the refrain (145.7–180);
music; stanza 3 and the refrain (209.3–247.6); then the refrain's first line, over and over, to the end (255–338).
**Stanza 4 (देव दनुज ऋषि मुनी…) is not sung**, so it has no time (`source.json` → `"fill": 0`). This is the āratī
जय जय श्री शनि देव, not जय शनि देवा (`jai-shani-deva-aarti`).

The identify transcript (`transcripts/JtJ4P0302FY.jsonl`) has only 15 segments, some misplaced (its first, at 0–10 s, is
music). Evidence: the same Whisper small model (its ONNX export, `tools/audio/transcribe_onnx.py`) on 4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 20.4 | the window from 16 s hears music only, the one from 17 s only "जे जे", those from 18 to 21 s more and more of "जय जय श्री शनि देव": the singing starts at about 20 s; MMS took the line’s repeat at 27.2 |
| aarti.pad1 | 95.4 | windows from 91 to 95 s begin "शाम आंग" (श्याम अंग), the one from 96 s "अग वक्रे": about 95.3 s; MMS took the repeat at 100.9 |
| aarti.pad2 | 148.6 | windows from 147 to 148 s begin "क्रीट मुकुट शीश", the one from 149 s "वुट शीश": about 148.3 s; MMS took the repeat at 153.8 |
| aarti.pad3 | 212.6 | windows from 209 to 212 s begin "मोदक मिष्ठान", the one from 213 s "विश्ठान पान": about 212.3 s; MMS took the repeat at 217.4 |
| aarti.pad4 | (none) | not sung: after stanza 3's refrain (to 247.65) only "जेजे शिशनी देव…" (the refrain's first line) to the end. Its fix is stanza 3's own start, so no time is used for it, and with `"fill": 0` none is guessed |
