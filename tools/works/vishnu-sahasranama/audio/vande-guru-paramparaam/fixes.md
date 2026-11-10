# Hand-checked starts (vande-guru-paramparaam, YouTube `A4D-Zf-HJLI`)

From the transcript (`transcripts/A4D-Zf-HJLI.jsonl`: the identify transcript, with the stretches it lost or heard
garbled re-transcribed in 4–9 s pieces by `tools/audio/transcribe_onnx.py`; where both have a stretch, the re-transcription
is kept). Not yet heard by ear.

| Verse | Start | Evidence |
|---|---|---|
| `stotra.sh14` | 538.5 | the piece 529.5–534.0 is śloka 13's first line (रुद्रो बहुशिरा बभ्रुर्विश्वयोनिः शुचिश्रवाः); its second line takes about 4.5 s. The matcher took the first transcript's 533.0, whose times run early here |
| `stotra.sh45` | 822.3 | the piece 812.55–817.8 is śloka 44's first line (वैकुण्ठः पुरुषः प्राणः); its second line follows (about 4.5 s). The matcher had 814.1, inside śloka 44 |
| `stotra.sh52` | 885.0 | the piece 880.7–884.8 is śloka 51's second line (अविज्ञाता सहस्रांशुर्विधाता कृतलक्षणः); śloka 52's second line, आदिदेवो महादेवो, at 889.8. The matcher had 878.6, inside śloka 51 |
| `stotra.sh54` | 903.4 | the piece 898.9–903.4 is śloka 53's second line (शरीरभूतभृद्भोक्ता कपीन्द्रो भूरिदक्षिणः); 903.4–912.35 is śloka 54 (… विनयो जयः सत्यसन्धो दाशार्हः सात्वताम्पतिः). The matcher had 898.1 |
| `stotra.sh79` | 1129.8 | the piece 1126.55–1129.8 is śloka 78's second line (लोकबन्धुर्लोकनाथो माधवो भक्तवत्सलः); śloka 79's second line, वीरहा विषमः शून्यो, follows. The matcher had 1123.6, two seconds after śloka 78 |
| `stotra.sh80` | 1140.3 | śloka 80's second line (सुमेधा मेधजो धन्यः) is heard in the re-transcription at 1144.8 (the first transcript has it at 1137.8: its times run about 7 s early here); its first line takes about 4.5 s. The matcher had 1132.4 |
| `stotra.sh96` | 1280.65 | the piece 1280.65 “चनाड चना त” (सनात्सनातनतमः), after śloka 95's second line (1275.0) and before śloka 97 (अरौद्रः कुण्डली चक्री, 1288.8); not matched |
| `stotra.sh104` | 1350.8 | the piece 1350.8 “बूर्भु वस्” (भूर्भुवःस्वस्तरुस्तारः), after śloka 103's second line at 1346.3; not matched |
| `uttara.sh18` | 1580.1 | the piece 1575.7–1584.5 is uttara 17's second line (आचारप्रभवो धर्मो) and then the first of 18; 18's second line, जङ्गमाजङ्गमं चेदं, at 1584.5; not matched |

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| stotra.sh46 | windows from 830 to 831 s begin "विस्तारस्ता वरस्तानु", the one from 832 s "वर्श्थानु…": about 831 s; MMS 830.9 (score 0.90) |
