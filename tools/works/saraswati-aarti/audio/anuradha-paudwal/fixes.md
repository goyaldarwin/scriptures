# Anuradha Paudwal, "Aarti Vol. 2" (YouTube faxIif-3F8o, 10:29–18:19): hand-checked starts

**The track** (`recordings.json` start 590.73, end 1097.0: 9:50.73–18:17.00 of the 3712-s video faxIif-3F8o): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 586.13–590.73 s, after it 1097.00–1100.85 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The transcript (`transcripts/faxIif-3F8o.jsonl`, the identify run) begins each segment where the one before ended, so a stanza after an instrumental interlude is placed seconds early or on the refrain before it, and it missed some lines. The starts below come from a second transcription of the same stretches with Whisper small (`tools/audio/transcribe_onnx.py`), which cuts the audio into 4–9 s pieces at its quiet points: the time is the start of the piece in which the verse's first words are heard (the pieces before it are music). Starts not listed here come from the transcript. To be set by ear.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 630.4 | windows from 627 to 630 s hear "जय सरस्वती माता" (the first two only at their end), the one from 631 s no words of it: the refrain starts at about 630.4 s (the hand start 629.5 was a transcript segment's); MMS 657.61 took its repeat |
| aarti.pad5 | 910.4 | the window from 905 s hears no words, those from 906 to 910 s more and more of "दूप दीप फल मेवा" (धूप दीप फल मेवा), the one from 911 s "…विप ख़ग मेवा": the line starts at about 910.4 s (the hand start 907.5 was a transcript segment's); MMS 910.36 agrees |
| aarti.pad6 | 960.1 | 960.1 "माशरस्वती की आरती" = माँ सरस्वती की आरती; 940.9–960.1 music. |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.pad1 | windows from 702 to 704 s begin "चंद्रवजनी पज्माशी", the one from 705 s "वग़ानी…": about 704.3 s; MMS 704.18 |
| aarti.pad2 | the window from 755 s begins "बाई कर्मेवीना", the one from 756 s "ताए कर्मे…": about 755.3 s; MMS 755.9 |
| aarti.pad3 | windows from 804 to 806 s begin "देवी शरन जो", the one from 808 s does not: about 806.8 s; MMS 807.44 |
| aarti.pad4 | windows from 857 to 858 s begin "वीट्या/वेजा ग्यान", the one from 859 s "जा ग्यान": about 858.3 s; MMS 858.84 |
