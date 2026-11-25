# Vijay Laxmi (YouTube EvCraLQF3XM): hand-checked starts

Read with `tools/audio/windows.py` (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`): 5-s windows a second apart; the last window that still begins with the line's first words is at or just before its start.

| Verse | Start (s) | Evidence |
|---|---|---|
| aarti.pad1 | 16.6 | the window from 16.5 s begins “पितु मात्र साहायक स्वामी सखाए”, the one from 17.5 s “अद्र सहायक” (the line already begun) |
| aarti.pad2 | 60.6 | after pad 1 ends (“…वारे हु” at 56.6 s), the window from 60.6 s begins “सब भार दिस अदा सुख्डा”, the one from 61.6 s “अदि से ता” (mid-line); MMS took the repeat of the line at 71.7 s |
| aarti.pad3 | 126.9 | windows from 124.6 to 126.6 s begin “बूली है रम ही तुम”; the one from 123.6 s hears only “बूली” at its end |
| aarti.pad5 | 193.2 | after the refrain and music (169 to 191 s), the window from 193 s begins “येह जीवनके तुम जीवनके”, the one from 194 s “जीवन के तुम जीवन हो” (इस already sung); the line is sung again at 204 s, where MMS put it |

`aarti.pad4` (महाराज महा महिमा तुम्हरी) is not sung (`source.json` → `unsung`): after pad 3 the windows from 169 to 173 s hear the refrain पितु मात सहायक, then music to 191 s, then pad 5; nothing later in the recording has its words.
