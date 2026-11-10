# Chand Kumar, "Shani Aarti" (YouTube JtJ4P0302FY): hand-checked starts

What the recording sings: music to ~18 s; the refrain (जय जय श्री शनि देव भक्तन हितकारी · सूरज के पुत्र प्रभु छाया महतारी)
and its first line again (18.7–64); music; stanza 1 and the refrain (93.2–127); music; stanza 2 and the refrain (145.7–180);
music; stanza 3 and the refrain (209.3–247.6); then the refrain's first line, over and over, to the end (255–338).
**Stanza 4 (देव दनुज ऋषि मुनी…) is not sung**, so it has no time (`source.json` → `"fill": 0`). This is the āratī
जय जय जय श्री शनि देव, not जय शनि देवा (`jai-shani-deva-aarti`).

The identify transcript (`transcripts/JtJ4P0302FY.jsonl`) has only 15 segments, some misplaced (its first, at 0–10 s, is
music). Evidence: the same Whisper small model (its ONNX export, `tools/audio/transcribe_onnx.py`) on 4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 18.65 | pieces to 18.65 are music ("अगर"); 18.65–24.4 "जे जे श्रिशनी देब", 24.4 "तनहित कारी" = …शनि देव भक्तन हितकारी; 42.5 "सूरज के पुत्र प्रभूच्वाया महतारी" |
| aarti.pad1 | 93.2 | 68.35–93.2 music; 93.2–100.55 "शाम आंग वक्रे द्रिष्त च्टुर्ब हुजा दारी" = श्याम अंग वक्र-दृष्टि चतुर्भुजा धारी; the alignment took its repeat (102.0) |
| aarti.pad2 | 145.7 | 127.15–145.7 music; 145.7–153.45 "क्रीट मुक्त शीश रजद दिपत है लिनारी" = क्रीट मुकुट शीश राजित दिपत है लिलारी; the alignment took 132.0, which is music |
| aarti.pad3 | 209.3 | 180.6–209.3 music; 209.3–216.8 "मोदक मिष्ठान पान चडद ते है सुपारी"; 222.1 "लोहा किल तेल उडद महिश्याती प्यारी" |
| aarti.pad4 | (none) | not sung: after stanza 3's refrain (to 247.65) only "जेजे शिशनी देव…" (the refrain's first line) to the end. Its fix is stanza 3's own start, so no time is used for it, and with `"fill": 0` none is guessed |
