# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for the Sanskrit Parayan recordings of the Śrīmad Bhāgavata, each verse's start and end found by torchaudio's
`MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two verses and at
both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4). Windows of about 90 s around the transcript's
rough starts (`mms/windows.json`, `tools/audio/mms_windows.py`); one run per recording in the public `align` workflow
(`mms_align.py`), whose raw starts, ends and scores are `mms/<video id>.json`; `mms_merge.py --lean 0.3` writes
`aligned.json` and `check.json`. Each start here is MMS's minus 0.3 s, its median lean against the owner's 132 starts set by
ear (0.32 s), taken for the whole series: one reciter, one recording set. Starts MMS scored below 0.5 are left out: those
verses keep the transcript's start and are listed to check. 14,506 of the 14,770 verses on the recordings take MMS's start;
MMS also times the long prose passages the transcript missed.

**How good:** scored on the owner's 132 starts set by ear (`owner.json`, all 30 recordings), each compared with his:

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 88 (67%) | 40 | 4 | 0.70 s | 12.01 s |
| MMS, lean removed | **124 (94%)** | 7 | **1** | **0.24 s** | **0.39 s** |

- The random sample (30 verses, one in each recording, `check.json` before the switch): the transcript within 1 s on 20, MMS on 28.
- The other 102 are the sample's neighbours, which the owner set while there; where he only confirmed the transcript's start
  (✓ Correct) the transcript scores 0, which favours it.
- The one MMS miss over 3 s is 8.3.23 (7.9 s late; the transcript was 8.4 s off too).
- MMS's start and the transcript's differ by more than 2 s on 2,114 verses; on the owner's starts that flag caught 3 of
  MMS's 8 misses over 1 s while flagging 16 verses, so it mostly marks the transcript's errors.

**To check** (`check.json`, the checks of METHOD.md step 4): MMS score below 0.5 (176), MMS and the transcript more than
2 s apart (2,114), out of pace (67): 2,295 verses. The owner's starts (`owner.json`) still win over all of these.
