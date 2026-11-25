# VedicQB (YouTube zAGrcGMkh90): hand-checked starts

Read with `tools/audio/windows.py` (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`): 5-s windows a second apart; the last window that still begins with the line's first words is at or just before its start.

| Verse | Start (s) | Evidence |
|---|---|---|
| chalisa.cau5 | 27.0 | the windows from 25 to 27 s begin “आदिशक्ति श्री विद्या रूपा”, the one from 29 s the next line; MMS 27.04 s |
| chalisa.cau15 | 73.0 | the windows from 71 to 73 s begin “योग सिद्धि पावे सब योगी”, the one from 74 s “…सब योगी भोगे” (mid-line); MMS 73.01 s |
| chalisa.cau37 | 180.6 | the window from 179 s hears the end of cau 36 (…दिखाती हो माँ) and then हेमावती उमा ब्रह्माणी; the one from 181 s begins the second half (भण्डासुर का हृदय विदारिणी) |
| chalisa.cau38 | 186.2 | the window from 186 s begins “सर्व विपति हर सर्वाधारे तुमने क…”, the one from 188 s the second half (तुमने कुटिल कुपंथी तारे) |
| chalisa.cau39 | 191.5 | the window from 190 s hears …तारे, then चन्द्रधारणी; the one from 191 s begins “चंद्रधारणी नैमिषवासिनी”, the one from 192 s “…धारणी” (mid-word) |
| chalisa.cau40 | 194.3 | MMS’s start less its lean (194.9 − 0.6 s; score 0.27): the windows from 193 to 200 s hear no words (Whisper’s “अगर बादा”), so the line is too soft for them; it falls where the reading’s pace (about 3 s a line) puts it, between cau 39 (191.5 s) and cau 42 (199.9 s). To check by ear |
| chalisa.cau41 | 196.9 | MMS’s start less its lean (197.5 − 0.6 s; score 0.49), as for cau 40. To check by ear |
| chalisa.cau43 | 203.2 | the windows from 201 and 202 s end cau 42 (…संकट मिट जावे) and run into ध्यान लगा; the one from 203 s begins “ध्यान लगा पढ़े इक्कीस बारा” |
| chalisa.cau44 | 207.5 | the transcript’s line “तुख कहीन संटबी सुक पावे” (पुत्र-हीन सन्तति सुख पावे) at 207.6 s; the windows from 204 and 205 s end cau 43 (…होवे सारा), the one from 209 s is the second half (निर्धन धनी बने गुण गावे) |
| chalisa.do1 | 222.3 | the transcript’s “यालिते बाः” (ललिते माँ) at 222.2 s, after cau 48’s …ललिता चालीसा (221 s); MMS 222.35 s |

`chalisa.cau46` (जितेन्द्र चन्द्र भारतीय बतावें, the verse with the poet’s name) is not sung (`source.json` → `unsung`): cau 45 (इस विधि पाठ करे, 213.7 s) runs straight into cau 47 (सबसे लघु उपाय, 216.8 s).
