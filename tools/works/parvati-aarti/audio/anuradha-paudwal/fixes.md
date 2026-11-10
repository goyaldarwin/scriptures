# Anuradha Paudwal, "Aarti Vol. 2" (YouTube faxIif-3F8o, 31:22–39:22): hand-checked starts

**The track** (`recordings.json` start 1860.15, end 2363.96: 31:00.15–39:23.96 of the 3712-s video faxIif-3F8o): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1853.38–1860.15 s, after it 2363.96–2365.12 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The transcript (`transcripts/faxIif-3F8o.jsonl`, the identify run) begins each segment where the one before ended, so a stanza after an instrumental interlude is placed seconds early or on the refrain before it, and it missed some lines. The starts below come from a second transcription of the same stretches with Whisper small (`tools/audio/transcribe_onnx.py`), which cuts the audio into 4–9 s pieces at its quiet points: the time is the start of the piece in which the verse's first words are heard (the pieces before it are music). Starts not listed here come from the transcript. To be set by ear.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 1882.8 | 1882.8 "पुंजे पार्वत्ति माता", 1887.8 "मैंया जेए गोरा माता", 1892.7 "ब्रम्हस्नावा कम देवी" = the refrain; 1860.0–1882.8 music (the transcript dates its first line 1863.5). |
| aarti.pad5 | 2162.9 | 2162.9 "सिस्टिलुपा" = सृष्टिरूप; 2143.6–2162.9 music. |
| aarti.pad7 | 2262.2 | 2262.2 "मैं आखी की आपी …", 2269.6 "जो कोई लर्गाता" = (श्री प्रताप) आरती मैया की जो कोई (नर) गाता; 2245.4–2262.2 music. The automatic match found no start. |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.pad1 | windows from 1956 to 1957 s begin "औरी पुले पन्त्य…" (अरिकुलपद्म), the one from 1958 s does not: about 1957.3 s; MMS 1957.34 |
| aarti.pad2 | windows from 2006 to 2008 s begin "शिव को वाह…" (सिंह का बाहन), the one from 2009 s "वाहर साजे": about 2008.3 s; MMS 2008.9 |
| aarti.pad3 | windows from 2057 to 2060 s begin "सत युग रूप", the one from 2061 s "अगरुपशी": about 2060.3 s; MMS 2060.5 |
