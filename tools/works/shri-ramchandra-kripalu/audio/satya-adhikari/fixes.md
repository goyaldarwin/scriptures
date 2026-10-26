# Satya Adhikari, "Aarti Shree Ram Ji Ki" (YouTube J5cllhBiAV0): hand-checked starts

The recording sings the stuti श्रीरामचन्द्र कृपालु (chhandas 1–5) and the Mānas's Bāla 236 chhand and sorathā, then the
jaikāras "बोलो सियावर रामचन्द्र भगवान की जय · दशरथ नन्दन श्री राम की जय" (from 171 s). It does not sing the other two
āratīs. So `recordings.json` sets `from` kripalu.cha1 and `to` bal.236.so236, with `"align": "anchors"` in `source.json`
(the only alignment that takes a last verse): without it, the jaikāra is matched to the Rāmalalā refrain.

Starts taken from the transcript (`transcripts/J5cllhBiAV0.jsonl`), segment start → verse:

| Verse | Start | Evidence |
|---|---|---|
| kripalu.cha1 | 17.6 | The first sung segment ("शिना मुच्ट्ट…", 17.6–26.6 s) is followed by "…नव कंज लोचन कंज मुख" (the verse's second line) at 26.6; before 17.6 there is only the instrumental opening, which the recogniser heard as "अपने/अगर". To check by ear. |
| kripalu.cha4 | 72.75 | "शिर भिनन्वर शिर … कुंडले" = सिर मुकुट कुंडल, at 72.75; the automatic alignment puts the verse at the line's second half, "चारु उदारु अंग विभूषणं" (78.75). |
| bal.236.cha1 | 108.6 | "भवन चाही राचे हुँ" = मनु जाहिं राचेउ, the verse's first words, at 108.6. |
