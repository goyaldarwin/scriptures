# Hand-checked verse starts (Vande Guru Paramparaam, ZIDdE4SZAuw)

Speech recognition garbled or dropped some lines of the chant, so the automatic match gave these verses the next line's time. Each start was read from `transcripts/ZIDdE4SZAuw.jsonl`: the segment where the verse's own first words are heard. They are applied from `fixes.json` by `tools/audio/make_timings.py`.

| Verse | Start (s) | Evidence |
|---|---|---|
| dhyana | 66.5 | "द्यानं द्याये दाजानु" — the heading ध्यानम् and the verse's first words |
| sh3 | 127.0 | "सासितूण…" inside the 126.0–134.7 segment, before "नक्तंचरान्तकम्" |
| sh4 | 143.65 | "ता वरक्शाम पदेद प्राग्ण्या" = रामरक्षां पठेत्प्राज्ञः |
| sh18 | 331.0 | "…ष्णाजिनाम्बरौ | फलमूलाशिनौ दान्तौ" (328.5–334.45), after śloka 17's last word |
| sh20 | 358.0 | "आत्तसज्जधनुषा…" |
| sh21 | 372.6 | "…गच्छन्मनोरथान्नश्च": the segment holds both lines; the first was not recognised |
| sh29 | 508.5 | "…शरणं भव राम राम | श्रीरामचन्द्र चरणौ" at the end of 503.05–511.6 |
| sh38 | 667.9 | after śloka 37 ends ("रामे चित्तलयः…" 661.9–667.9); its second half is at 681.7 |

Note: `transcripts/ZIDdE4SZAuw.align.json` was made before `fixes.json` existed and already carries these starts. Re-running `make_timings.py` reproduces the published timings exactly. If you delete the cache to realign, check the neighbouring verses again.
