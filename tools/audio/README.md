# Audio sources

The website plays recordings from YouTube and highlights each verse as it is recited, so a reader can listen hands-free. An audio source therefore needs only the video ids and the time each verse starts. No audio is stored in the repository. To add a reciter, follow `docs/HOW-TO.md` → "Add a new audio source".

## How the timings are made
1. **`transcribe.py`**: Whisper small (CTranslate2 int8; e.g. `Systran/faster-whisper-small`) converts speech to text with times.
   - Audio is cut into 10-minute chunks with ffmpeg so memory stays low on a small machine.
   - Settings: language from `source.json`, beam 1, no carry-over of earlier text (stops runaway repetition).
   - Speed is about 1× real time per worker on 2 CPU cores. Run as many workers as you have cores.
   - Output is `transcripts/<video id>.jsonl`, plus `.done` when finished. A stopped run resumes from its last chunk.
2. **`align.py`**: the verses are split into half-lines. Both sides are reduced to a key that ignores the spelling slips speech recognition makes (vowel length, nasal marks, ब/व, श/ष/स, ण/न …).
   - A trigram vote finds where the recording starts.
   - Dynamic programming pairs transcript lines with half-lines, allowing one line to cover two or three half-lines.
   - It skips what reciters add: refrains, repeated dohās, kīrtana and tunes.
3. **`make_timings.py`**: takes each verse's first matched time, drops matches that go backwards, and fills short gaps (≤ 8 verses) by text length.
   - The first verses of a day are back-filled to the day's start.
   - Each recording is cached as `transcripts/<video id>.times.json` (item id → seconds). Delete the cache to realign.

Reading the verse ids in a recording's first/last printout is the quickest check. The key works for Devanagari texts; Gurmukhi or other scripts need their own `key()` in `align.py`.

## Status: Pt. Kamlesh Upadhyay "Haripuri" (Rāmacaritamānasa, Māsa-pārāyaṇa)
Timed: days 1–10 and 15–17. To do: 11–14 and 18–30. There is no recording for day 26 in `recordings.json`.
