# Ramawtar Sharma (YouTube cKYi3i6-jPM): hand-checked starts

Read with `tools/audio/windows.py` (Whisper small, the ONNX export of `tools/audio/transcribe_onnx.py`): 5-s windows a second apart; the last window that still begins with the line's first words is at or just before its start.

| Verse | Start (s) | Evidence |
|---|---|---|
| aarti.pad5 | 154.0 | windows from 137 to 149 s hear no words (music; Whisper's "अगर"); those from 152 to 154 s begin "मैदी मैद्वाँ / मैरी मैं तो मधाए / मैंडी मैं तो मधाए आचे रज" (माड़ी में तुम करी तपस्या अचरज), the one from 155 s "अच्रज सबी कर" (the line's later words): the line starts at about 154 s. MMS took the repeated अचरज सभी करें at 158.6 |

`aarti.pad3` (धर्म की बेल) is not sung (`source.json` → `unsung`): the windows from 126 to 131 s hear the refrain (बाबा जय गोगा वीर हरे) after stanza 2, then an interjection and music before माड़ी में.
