# BhaktiDhaam, "सम्पूर्ण चालीसा संग्रह" (YouTube lCwPg0LRRjk): hand-checked starts

**The track** (`recordings.json` start 2710.89, end 3026.76: 45:10.89–50:26.76 of the 3028-s video lCwPg0LRRjk): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it 2710.08–2710.89 s, after it 3026.76–3028.09, the video’s end s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The text is the version sung (`../../reconciliation.md`). Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript's matches (the identify transcript, `transcripts/lCwPg0LRRjk.jsonl`).

| Verse | Start | Evidence |
|---|---|---|
| chalisa.cau4 | 2741.6 | "जैजे जे रगुनाक्धिपाला" = जय जय जय रघुनाथ कृपाला. |
| chalisa.cau5 | 2753.9 | "दोत तुमार वीर हन्माना" = दूत तुम्हार वीर हनुमाना. |
| chalisa.cau6 | 2760.2 | "तब बुज दंद प्रचंद खपाला" = तव भुज दण्ड प्रचण्ड कृपाला. |
| chalisa.cau7 | 2766.3 | "तुम अनात के नात को साई" = तुम अनाथ के नाथ गोसाईं, the first of four half-lines in the segment 2766.3–2778.3 s. |
| chalisa.cau8 | 2772.3 | "रम्हा दिक तब पार ना पावे" = ब्रह्मादिक तव पार न पावैं, the third of those four half-lines (the segment shared by length). |
| chalisa.cau9 | 2784.3 | "चारी उवेद भरत है साखी" = चारिउ वेद भरत हैं साखी, the first of three half-lines in 2784.3–2793.3 s. |
| chalisa.cau10 | 2790.3 | "गुडगावत शारत मनमाही" = गुण गावत शारद मन माहीं, the third of those (shared by length). |
| chalisa.cau11 | 2796.5 | "नाम तुमार लेत जो कोई" = नाम तुम्हार लेत जो कोई, the second of five half-lines in 2793.3–2809.3 s (shared by length). |
| chalisa.cau12 | 2802.9 | "राम नाम है अप्रम पारा" = राम नाम है अपरम्पारा, the fourth of those five (shared by length). |
| chalisa.cau29 | 2932.3 | "सत्य है सत्य व्रत स्वामी" = सत्य सत्य सत्य ब्रत स्वामी, the first half-line of the segment 2932.3–2960.3 s, right after chaupāī 28 (2925.3 s); the segment holds seven half-lines (chaupāīs 29–31 and the first half of 32) in 28 s, and the automatic alignment matched it from chaupāī 30 on, at its start. |

Chaupāīs 13–16 are not in the transcript (it has nothing between 2809.3 and 2839.3 s, where chaupāī 17 is heard); they are placed by length between chaupāīs 12 and 17 and listed to check. The video ends after chaupāī 40: chaupāīs 41–46 and the closing dohās are untimed.

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| chalisa.cau1 | music after the silence that ends the Śani Chālīsā (2710.08–2710.89 s); windows from 2719 to 2723 s begin "शीर गुवीर भक्त", the one from 2724 s does not: about 2723.0 s; MMS 2723.17 (score 0.82) |
| chalisa.cau2 | the window from 2729 s begins "निश्दिन दियान दरे", the one from 2730 s "तासम…": about 2729.3 s; MMS 2729.32 |
| chalisa.cau3 | the window from 2735 s begins "भ्यान दरे शिव", the one from 2736 s "तरे शिव": about 2735.3 s; MMS 2735.56 |
| chalisa.cau30 | the window from 2943 s hears "…सद्द्बजन तुम्हरो" first, the one from 2945 s "तबजन तुम हरो": about 2944.3 s; MMS 2944.81 |
| chalisa.cau31 | the window from 2951 s begins "…पत्गग़ी पत्टिकी" (सत्य शपथ गौरिपति), the one from 2952 s "ग़ोरी पति की": about 2951 s; MMS 2950.92 |
| chalisa.cau32 | the window from 2957 s begins "सुनहु राम तुम", the one from 2958 s "तुम तात": about 2957.3 s; MMS 2957.1 |
