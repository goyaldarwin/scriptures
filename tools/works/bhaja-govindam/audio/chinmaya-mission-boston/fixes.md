# Chinmaya Mission Boston, "Bhaja Govindam full, Verses 1 to 31" (YouTube xrNOEva86pA): hand-checked starts

What the recording sings: the refrain-verse 1 (4–60 s), then verses 2–31 in the text's order, each line sung twice and
each verse followed by the refrain (भज गोविन्दं भज गोविन्दं गोविन्दं भज मूढमते), and the refrain once more at the end
(1975–1996). **Verse 13a (द्वादशमञ्जरिकाभिरशेषः…) is not sung**; it has no time (`source.json` → `"fill": 0`).

Most starts come from the alignment. Here, from the transcript (`transcripts/xrNOEva86pA.jsonl`, 4–9 s pieces) and the
same model on 2.5 s windows, are the starts it took from a verse's repeated or second line, the three verses after its
last match (29–31), and 13a:

| Verse | Start | Evidence |
|---|---|---|
| sh1 | 4.0 | windows to 4.5 are music; 4.0–6.5 "अज़ाए़ बोए", piece 4.6–11.6 "तज़को बिवंदव तज़को बिवंदव" = भज गोविन्दं भज गोविन्दं |
| sh2 | 67.5 | 65.0–67.5 "वग़ा बादे…" (the refrain ending), 67.0–69.5 "वूड़े", 68.0–70.5 "वूरे तेदी" = मूढ जहीहि; the alignment took यल्लभसे (93.25) |
| sh13 | 749.3 | piece 741.45–749.25 "अज़ा ब" (the refrain), 749.25–753.85 "अदिए तान्टा अगे तरजी" = का ते कान्ता धनगतचिन्ता; the alignment took वातुल (753.45) |
| sh13a | (none) | not sung. The alignment matched it to the end of verse 13 (788.75, "तरने नाउदा…" = …तरणे नौका); its fix is verse 13's own start, so the match is dropped (a start that does not come after the previous verse's is not used) and, with `"fill": 0`, no time is guessed for it |
| sh14 | 808.5 | 806.0–808.5 "बज़़ बुड़ामः" (…भज मूढमते), 808.0–810.5 "अवादे चविर", 809.0–811.5 "जदी लोग मुर्ड़", 810.0–812.5 "अदिलो मुन्नी" = जटिलो मुण्डी; the alignment took 818.5 |
| sh18 | 1056.9 | piece 1048.15–1056.85 the refrain; 1056.85 "वुलतिवाष्ट्या" (…तरुमूलनिवासः), 1063.0 "अजिना मुवासबाः" = …मजिनं वासः; the alignment took the repeat of line 1 (1070.05) |
| sh19 | 1123.5 | 1110.8–1119.3 the refrain; 1123.5 "वो गले तोबार यो गले तोबार" = योगरतो वा; the alignment took 1129.3 |
| sh21 | 1291.3 | piece 1290.25 "और मुदे उनरभी जननम" = (मूढ)मते, पुनरपि जननं; windows 1290.0 "और वाडे", 1292.0 "वूडनारा पीज़ा"; the alignment took the repeat (1296.95) |
| sh22 | 1360.6 | 1351.85 the refrain; 1360.6 "तद्याज़ पट्ट्ट" = रथ्याचर्पट…; the alignment took the repeat (1370.55) |
| sh26 | 1611.0 | 1608.0–1610.5 "वज़ा वुना मागे" (…भज मूढमते), 1611.0–1613.5 "बाँवावुप्रज्वाव", 1612.0 "बामाम प्रोज़ां" = कामं क्रोधं; the alignment took 1592.7, inside verse 25 |
| sh27 | 1673.0 | 1665.05 the refrain; 1671.8 "वूल्बा बाते एदिंवूं भी लिटा नामबजा" = (मूढमते) गेयं गीतानाम…; windows 1673.0, 1674.0 "ये ये"; the alignment took ध्येयं (1687.85) |
| sh29 | 1796.4 | 1786.25–1796.35 the refrain; 1796.35 "अगा मागर्तम बावये मिलिख्यम" = अर्थमनर्थं भावय नित्यं |
| sh30 | 1856.9 | 1848.0 the refrain; 1856.85 "राडायामं तज्याशारम्" = प्राणायामं प्रत्याहारं |
| sh31 | 1917.7 | 1908.9 the refrain; 1917.7 "वुर्चर एडा वुर्चर" = गुरुचरण… |
