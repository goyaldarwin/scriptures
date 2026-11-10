# "Aarti Gangadhar Ji Ki", Bhajan aur Aarti — Badrinath Kedarnath Gangotri Yamnotri (YouTube Zn78FYVwbZM): hand-checked starts

The singer is not named in the file. What the recording sings: music to ~10 s; the refrain (10.6–44); stanzas 1, 2 and 3
whole, each line or half-line sung twice and each stanza followed by the cue ॐ हर हर हर महादेव; **of stanza 4 only its first
two lines** (रुण रुण चरणे…, चक्रावर्ते…, 247–274) and **of stanza 5 only its last two** (सुन्दरजटाकलापं…, डमरुत्रिशूलपिनाकं…,
281–308); stanzas 6 and 7 whole; **of stanza 8 only its last two lines** (सन्गतिमेवं…, शिवसायुज्यं…, 447–474); the refrain
again (480–514); then the śloka कर्पूरगौरं करुणावतारं… (514–543), which is not part of this āratī's text and is not timed.
The lines it leaves out stay in the text; each of these stanzas starts where its first sung line starts.

Evidence: `transcripts/Zn78FYVwbZM.jsonl` (segments from 30 s, the first sung words it heard) and, where it is silent or the
alignment took a repeat, the same Whisper small model (its ONNX export, `tools/audio/transcribe_onnx.py`) on 4–9 s pieces.

| Verse | Start | Evidence |
|---|---|---|
| aarti.tek | 10.6 | pieces to 10.6 are music; 10.6–19.3 "अँ जय जंगा दर हर जय गी जादी शा" = ॐ जय गङ्गाधर (जय) हर जय गिरिजाधीशा; the transcript has nothing between 9.76 and 30 |
| aarti.pad1 | 44.55 | the transcript's 44.16 "कैना शेगे रिषिखरे" and the piece 44.55 "तटेला शेगे रीशितरे कल प्रदे" = कैलासे गिरिशिखरे कल्पद्रुम…; the alignment took 53.08 (its repeat) |
| aarti.pad3 | 180.35 | 165.2 "इंद्रा आदिक सुरे सेविते" (stanza 2's last line, again), 173.85 "औब रर बर बर माहादे" (the cue); 180.35 "भी बुद्वाव दूबाव ने च्यतिते" = बिबुधबधू बहु नृत्यत; the alignment took 165.28, stanza 2's last line |
| aarti.pad5 | 281.4 | 274.9 "औब वर वर" (the cue); 281.4 "सुंदरे चटा कलापाम पावक युट खाला" = सुन्दरजटाकलापं पावकयुतभालम्, its third line: the first two (कर्पूरद्युतिगौरं…, त्रिनयनशशिधरमौलिं…) are not sung, nor stanza 4's last two; the alignment took 293.88 (डमरुत्रिशूलपिनाकं) |
| aarti.pad6 | 314.28 | the transcript's 308.28 cue, 314.28 "मुन्दे रच्यसी माला" = मुण्डै रचयति माला; the alignment took 322.88 (पन्नगमुपवीतम्) |
| aarti.pad8 | 447.4 | 428.28 "आवलो कईती मैंशम…" (stanza 7's last line), 441.12 the cue, 447.4 "संगित मीव, प्रतीजिन, पच्णम्य, फुरुदि" = सन्गतिमेवं प्रतिदिन पठनं यः कुरुते, its third line: its first two (ध्यानं आरति समये…, रामस्त्रिजटानाथं…) are not sung; the alignment found nothing for it |
