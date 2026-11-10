# Anuradha Paudwal, "Jai Ganesh Deva Aarti" (YouTube oWo6hMlex5M): hand-checked starts

What the recording sings: a spoken introduction on how an āratī is done (0–100 s, not text); the refrain twice (100.6–146.9);
stanza 1 (146.9–197); stanza 2 (197.7–222); the refrain (222–252); stanza 3 twice (252.4–296); stanza 5 (296.4–318); the
refrain (318–329). **Stanza 4 (दीनन की लाज…) is not sung**, so it has no time (`source.json` → `"fill": 0`).

Evidence: `transcripts/oWo6hMlex5M.jsonl` (the segments from the first sung line).

| Verse | Start | Evidence |
|---|---|---|
| aarti.pad1 | 157.8 | 5-s windows from 144 to 153 s hear no words after the refrain's last "…देवा" (the transcript's 146.9 was early by 11 s); the one from 154 s ends "…दन्त दया" (एकदन्त दयावन्त), those from 155 to 159 s begin "…दन्त दयावन्त चार भुजाधारी", the one from 160 s none: the stanza starts at about 157.8 s; MMS 178.44 took its repeat |
| aarti.pad2 | 198.9 | the window from 196 s ends "तान च़ी" (पान चढ़े), those from 197 and 198 s hear no words, the one from 199 s begins "अन चडी तुछ चडी आवर चडी" with पान clipped: the line starts just before 199 s (the transcript's start was 1.7 s early; MMS 199.82 is unsure, score 0.37) |
| aarti.pad3 | 253.4 | windows from 250 to 253 s begin "अन्दे को आखडे…" (अंधे को आँख देत), the one from 254 s "तेदो आखदिद": the line starts at about 253.4 s (the transcript's start was 1.4 s early; MMS 253.92 is unsure, score 0.313) |
| aarti.pad4 | (none) | not sung. The alignment matched it to stanza 3's repeat (275.36 "बन्दे को आखदे तको दिन को खाया", 285.36 "बानजन को पुट्र दे तनीर दन को माया" = अँधे को आँख देत… बाँझन को पुत्र देत…); its fix is stanza 3's own start (252.36 "अन्दे को आखदेट कोडिन को खाया"), so the match is dropped (a start that does not come after the previous verse's is not used) and, with `"fill": 0`, no time is guessed for it |
