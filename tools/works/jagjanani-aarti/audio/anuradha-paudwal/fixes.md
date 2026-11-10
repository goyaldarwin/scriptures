# Anuradha Paudwal, "Aarti Vol. 2" (YouTube faxIif-3F8o, 19:07–30:54): hand-checked starts

**The track** (`recordings.json` start 1100.85, end 1853.38: 18:20.85–30:53.38 of the 3712-s video faxIif-3F8o): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 1097.00–1100.85 s, after it 1853.38–1860.15 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The transcript (`transcripts/faxIif-3F8o.jsonl`, the identify run) begins each segment where the one before ended, so a stanza after an instrumental interlude is placed seconds early or on the refrain before it, and it missed some lines. The starts below come from a second transcription of the same stretches with Whisper small (`tools/audio/transcribe_onnx.py`), which cuts the audio into 4–9 s pieces at its quiet points: the time is the start of the piece in which the verse's first words are heard (the pieces before it are music). Starts not listed here come from the transcript. To be set by ear.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 1147.0 | 1147.0 "जग जए मनी जे जे माँ", 1150.0 "माजब जननी जेजे · भायगारिनी भावतारिनी" = जगजननी जय जय, (माँ) जगजननी जय जय, भयहारिणि भवतारिणि; 1099.4–1147.0 music. The transcript has nothing before 1180.6. |
| aarti.pad1 | 1218.7 | 1218.7 "तुही सच्चित सुखा मैं" = तू ही सत-चित-सुखमय; 1199.9–1218.7 music and vocalise. |
| aarti.pad2 | 1270.0 | 1270.0 "आदी", 1274.5 "आवी चला वी नाशी" = आदि … अविचल अविनाशी; 1250.7–1270.0 music and vocalise. |
| aarti.pad3 | 1320.5 | 1320.5 "अभी तारी अगवारी" = अविकारी अघहारी; 1301.3–1320.5 music and vocalise. |
| aarti.pad5 | 1421.1 | 1421.1 "राम त्रेशन तुसीपा · ब्रेजे रानी रादा" = राम कृष्ण तू सीता व्रजरानी राधा; the transcript missed this line, and the automatic match took the second line's repeat (1439). |
| aarti.pad6 | 1472.4 | 1472.4 "दश्वेख्यान वजुर्गा · नानाशा स्ट्रकरा" = दश विद्या नव दुर्गा नानाशस्त्रकरा; the automatic match took stanza 5's "हारिणि सब बाधा" (1447). |
| aarti.pad9 | 1624.0 | 1624.0 "तुही स्नी है सुदा मैं · तुवति गर्ल मना" = तू ही स्नेह-सुधामयि तू अति गरलमना; the automatic match took the refrain before it (1599). |
| aarti.pad10 | 1674.7 | 1674.7 "मुडा दार निवास्णी · इह बरे सी भी प्रदे" = मूलाधारनिवासिनि इह-पर-सिद्धिप्रदे; 1654.9–1674.7 music and vocalise. |
| aarti.pad11 | 1725.3 | 1725.3 "शाएटी शक्ति दर किवी" = शक्ति शक्तिधर तू ही; 1706.3–1725.3 music and vocalise. |
| aarti.pad12 | 1776.0 | 1776.0 "खम्मती दीन जुखीमा · विपत जाल गिए" = हम अति दीन दुखी मा विपत-जाल घेरे; 1756.8–1776.0 music and vocalise. |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| aarti.pad7 | windows from 1520 to 1522 s begin "ती पर गाम निवासिनी" (तू परधामनिवासिनि), the one from 1523 s "प्रगाम…": about 1522.4 s; MMS 1523.08 |
