# Anuradha Paudwal, "Ganesh Chalisa" (YouTube oHHniScYJzo): hand-checked starts

What the recording sings: music to ~13 s; the opening dohā (13.6–41), the 38 chaupāīs in order (from 53.9), the two closing
dohās (481–537). Most starts come from the alignment of `transcripts/oHHniScYJzo.jsonl`. Its vote for where the recording
begins skipped the opening (it began at chaupāī 6), and it missed chaupāīs 27–28 (one 29 s segment, 351–380, holds only
chaupāī 29's words). Evidence for these: the same Whisper small model (its ONNX export, `tools/audio/transcribe_onnx.py`)
on 4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| chalisa.do1 | 13.6 | pieces to 13.6 are music ("अगर"); 13.6–21.05 "जाया गानो पती सद गुडे सदार" = जय गणपति सदगुण सदन, 21.05 "कारी वर बदेन" |
| chalisa.cau2 | 65.9 | 65.9–72.3 "जय गज बदन स", 72.3 "वीश्ववि नायत बुत्तिवि ताद्धा" = विश्वविनायक बुद्धि विधाता |
| chalisa.cau20 | 265.4 | windows from 264 and 265 s begin "…लखियत्ती आनन्द" (लखि अति आनन्द), those from 266 to 268 s hear none of it: the line starts at about 265.4 s (the start in use, 266.49, was late; MMS 267.09) |

The same pieces confirm the wording she sings in closing dohā 2: 508.85 "समबन्द्ह अपनी सहस्ट्रदशे" (the transcript: "सम बन्द, अपने सहस्ट्र दश्य") = सम्बन्ध अपने सहस्र दश.

## Starts left to the forced aligner (MMS), checked
These verses have no hand start: a transcript segment's start is not the line's, and 5-s windows a second apart (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`) show that MMS's start is the line's.

| Verse | Evidence |
|---|---|
| chalisa.cau3 | windows from 86 to 90 s begin "वक्र तुंड शुचि", the one from 91 s does not: the line starts at about 90.3 s; MMS 90.14 |
| chalisa.cau4 | windows from 97 to 99 s begin "राजत मनी मुक्तन", the one from 100 s does not: about 99.3 s; MMS 99.35 |
| chalisa.cau8 | the window from 132 s begins "रिद ति" (ऋद्धि), the ones before hear the line before (…विश्वर विख्यात): about 132.6 s; MMS 133.12 |
| chalisa.cau27 | windows from 354 to 357 s begin "अगा खार मच्छो" (हाहाकार मच्यो), the one from 358 s "अखार": about 357.4 s; MMS 357.73 |
| chalisa.cau28 | windows from 363 to 367 s begin "तुरत गरुड़", the one from 368 s "तचड़ि": about 367.3 s; MMS 366.95 |
| chalisa.cau30 | windows from 379 to 381 s begin "नाम गनेश", the one from 382 s does not: about 381.5 s; MMS 382.24 |
