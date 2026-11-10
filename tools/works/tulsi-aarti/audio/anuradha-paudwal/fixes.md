# Anuradha Paudwal, "Aarti Vol. 2" (YouTube faxIif-3F8o, 39:59–47:10): hand-checked starts

**The track** (`recordings.json` start 2365.12, end 2827.16: 39:25.12–47:07.16 of the 3712-s video faxIif-3F8o): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 2363.96–2365.12 s, after it 2827.16–2831.90 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The transcript (`transcripts/faxIif-3F8o.jsonl`, the identify run) begins each segment where the one before ended, so a stanza after an instrumental interlude is placed seconds early or on the refrain before it, and it missed some lines. The starts below come from a second transcription of the same stretches with Whisper small (`tools/audio/transcribe_onnx.py`), which cuts the audio into 4–9 s pieces at its quiet points: the time is the start of the piece in which the verse's first words are heard (the pieces before it are music). Starts not listed here come from the transcript. To be set by ear.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 2403.9 | windows from 2394 to 2398 s hear no words (music: the hand start 2398.8 was a transcript segment's); the one from 2399 s ends "जेजे", those to 2403 s only "जे जे" at their end, the one from 2404 s begins "जे जे तुसी माता", the one from 2405 s "तुल सी माता": the refrain starts at about 2403.9 s; MMS 2425.08 took a later repeat |
| aarti.pad2 | 2557.3 | 2557.3 "बद्दू भुद्द्री हे शामा" = बहु पुत्री हे श्यामा; 2543.0–2557.3 music. |
| aarti.pad3 | 2628.4 | 2628.4 "औरिके शीशवी राजद · त्रिबो वंशे हो वंदित" = हरि के शीश विराजत त्रिभुवन से हो वंदित; the automatic match took the line's repeat (2645.7). |
| aarti.pad4 | 2700.4 | 2700.4 "लिकर जन्मवे जन्मे" = लेकर जन्म विजन में; 2691.8–2700.4 music. |
| aarti.pad5 | 2770.4 | the window from 2770 s begins "रवको तुम्मदी प्यारी" (हरि को तुम अति प्यारी), the one from 2771 s does not: about 2770.3 s; MMS took the stanza’s repeat at 2789.1 |
