# Hand-checked starts (fixes.json)

Every start here was found by reading the recording's transcript (`transcripts/<video id>.jsonl`, Whisper in 6-second windows, with word times): the time of the first word heard of the verse's first line, or, where the opening is garbled, of its first clearly recognisable word (said in the note). The verses between two heard or fixed starts are placed by length (`make_timings.py`, gaps of up to 8 verses).

## Starts matched in the wrong place

With `"align": "anchors"` a verse can be matched to a later line that sounds like it (a verse that opens like another, a repeated name), so that it starts far sooner or later than the reciter's pace allows. Every verse that a start made shorter than 0.3 or longer than 3.5 times the recording's usual time per letter was read in the transcript with its neighbours, and these starts set.

| Recording | Verse | Start (s) | Heard in the transcript | Why |
|---|---|---|---|---|
| `OCFJlevK9AA` | bala.58.7 | 59.1 | सराज़ा | स राजा, directly after 'लाखशरम' (क्रोधपर्याकुलाक्षरम्, end of 58.6); the 65.3 'बद्याजा पुन रेवाईता निद' is a squashed window tail |
| `Sss3Imu2FCg` | ayodhya.85.13 | 121.5 | शाष्वती खलु ते | शाश्वती खलु ते after मिहेच्छसि (end of 85.12) Heard in 5-s windows: the window from 118.5 s hears the end of 85.12 (“…च्फसी”), the one from 121.5 s begins “शाश्वती खल तेकिर तिर लोकानानु” (शाश्वती खलु ते कीर्तिर्लोकाननु), the one from 122.5 s “अश्वती खलुते…” (its middle): the line starts at about 121.5 s. |
| `iVnnipo0a94` | aranya.11.57 | 558.0 | ब्रातरम सम्स्कतंगर्ट्वादतस | भ्रातरं संस्कृतं कृत्वा ततस्, followed by 'तम्येशरूपिनम' (तं मेषरूपिणम्) |
| `ogsEhZmydxQ` | aranya.61.30 | 290.2 | साँच्टाः | 'तम साँच्टाः' = तं सान्त्वया; 'तम' has the window-start time 288.0 and 61.29 line 2 (हा...) begins 287.6, so the first reliable word is 'साँच्टाः'; line 2 'प्रश्रितः प्रश्रिताञ्जलिः' heard at 300.0-301.8; 303.68 is 61.31 |
| `tJXrwnLb4zA` | yuddha.17.61 | 580.1 | आ� बच्च्यम्सबज़गाँ़ाराव | अशक्यं सहसा राजन्, directly after 'सुखागतम' (end of 17.60); 'वो बोद्ध्वं' at 586.6 is a squashed window tail |
| `tJXrwnLb4zA` | yuddha.17.63 | 600.0 | आशांगेतमते स्वस्थो | अशङ्कितमतिः स्वस्थो; 598.1-599.2 is still 'नास्ति संशयः' of 17.62 (window-start time, real start about 599.5-600) |
| `X5PX55vTlNc` | yuddha.67.52 | 526.7 | सपर्वता | स पर्वताग्रम्, right after 'आन रादिपःा' (वानराधिपः, end of 67.51); 532.6 'बद्याग्र मुच्ख्षिप्या' is a squashed window tail |
