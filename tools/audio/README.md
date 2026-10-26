# Audio sources

The website plays recordings from YouTube and highlights each verse as it is recited, so a reader can listen hands-free. An audio source therefore needs only the video ids and the time each verse starts. No audio is stored in the repository. To add a reciter, follow `docs/HOW-TO.md` → "Add a new audio source". The state of each work's recordings is in `docs/START-HERE.md`.

## How the timings are made
1. **`transcribe.py`**: Whisper small (CTranslate2 int8; e.g. `Systran/faster-whisper-small`) converts speech to text with times.
   - Audio is cut into 10-minute chunks with ffmpeg so memory stays low on a small machine.
   - Settings: Hindi mode for Hindi, Awadhi, Sanskrit and Punjabi (it writes Devanagari, which `align.py` needs), beam 1, no carry-over of earlier text (stops runaway repetition).
   - For chant and singing, `source.json` → `"window": 6` transcribes each 6-second stretch on its own, so the recogniser cannot skip long passages it takes for music.
   - Speed is about 1× real time per worker on 2 CPU cores. Run as many workers as you have cores.
   - Output is `transcripts/<video id>.jsonl`, plus `.done` when finished. A stopped run resumes from its last chunk.
   - `transcribe_onnx.py` does the same with Whisper's ONNX export from GitHub, for when the faster-whisper model can't be downloaded.
2. **`align.py`**: the verses are split into half-lines. Both sides are reduced to a key that ignores the spelling slips speech recognition makes (vowel length, nasal marks, ब/व, श/ष/स, ण/न …). Gurmukhi is read by mapping it onto Devanagari (`gur2dev`), and Vedic svara marks are ignored.
   - A trigram vote finds where the recording starts.
   - Dynamic programming pairs transcript lines with half-lines, allowing one line to cover two or three half-lines.
   - It skips what reciters add: refrains, repeated dohās, kīrtana and tunes.
   - For recordings heard only in patches (chant, kīrtan), `source.json` → `"align": "anchors"` keeps only confident matches (`anchor_min`).
3. **`make_timings.py`**: takes each verse's first matched time, drops matches that go backwards, and fills short gaps (≤ 8 verses, or `source.json` → `fill`) by text length.
   - The first verses of a day are back-filled to the day's start.
   - Each recording's alignment is cached as `transcripts/<video id>.align.json`. Delete the cache to realign.
   - `fixes.json` (hand-checked starts, with the evidence in `fixes.md`) wins over the automatic match; `owner.json` (times the owner set by ear in the app) wins over both.
   - Around the owner's times, `order.py` places the other verses again so that starts never go backwards. The app applies the same rule (`buildAudio` in `tools/site/app.js`), and `tools/site/ux_test.py` checks that both agree.
   - With `"estimate": true` and no transcript, the verses are spread over the recording by text length, as a starting point for timing by ear.

Reading the verse ids in a recording's first/last printout is the quickest check. The key works for Devanagari and Gurmukhi texts; another script needs its own mapping in `align.py`'s `key()`.
