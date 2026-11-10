# BhaktiDhaam, "सम्पूर्ण चालीसा संग्रह" (YouTube lCwPg0LRRjk): hand-checked starts

**The track** (`recordings.json` start 0.1, end 393.51: 0:00.10–6:33.51 of the 3028-s video lCwPg0LRRjk): this song alone. Its bounds are the silences between the songs, found on the audio (the loudness in 10 ms steps falls below −42 dB, most to digital silence): before it the video’s start (0–0.10) s, after it 393.51–393.82 s. Every verse is timed inside them (`make_timings.py` refuses one outside), the player starts at the first verse and stops at the end, and the listening time counts only this song.

The text is the version sung (`../../reconciliation.md`). Starts not listed here come from the forced aligner (MMS, `aligned.json`), else from the transcript's matches (the identify transcript, `transcripts/lCwPg0LRRjk.jsonl`).

| Verse | Start | Evidence |
|---|---|---|
| chalisa.do2 | 341.2 | "मितनेम कर प्रात ही · पाथ करो चालीस" = नित्त नेम कर प्रातः ही पाठ करौं चालीस, right after chaupāī 40 (335.2 s); the automatic alignment ends at chaupāī 40. |
| chalisa.do3 | 366.2 | "मग सर चथी हे मन तरी तो · समवत चो सथ जा" = मगसर छठि हेमन्त ऋतु संवत् चौंसठ जान. |

Chaupāī 41 (कहै अयोध्या आस तुम्हारी …) is not sung (chaupāī 40 ends at 339 s and the closing dohā follows at 341 s), so `source.json` → `"fill": 0` keeps it from being placed by length between them; it stays untimed.
