# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Pt. Ashwin Kumar Pathak's recording of the Sundarakāṇḍa (`QjSpUgnEPLU`), the start and end
found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between
every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows
`mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run in the public `align` workflow
(`mms_align.py`, raw results in `mms/QjSpUgnEPLU.json`); `mms_merge.py --lean 0.55` writes `aligned.json` and `check.json`.
Each start is MMS's minus 0.55 s, the median lean of MMS against the owner's starts set by ear. 216 of the 408 verses take
MMS's start; the 181 MMS scored below 0.5 (the caupāīs sung to a tune, with long held notes) keep the transcript's and are
listed to check. The Hanumān āratī takes its timings from this recording.

**How good:** scored on 46 of the owner's starts set by ear (`owner.json`) that MMS and the transcript both time
(`tools/audio/mms_score.py`):

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 17 (37%) | 2 | 27 | 5.05 s | 12.63 s |
| MMS, lean 0.55 s removed | 42 (91%) | 1 | 3 | 0.14 s | 0.48 s |

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 207 (low score 181, MMS and the
transcript more than 2 s apart 13, out of pace 29, out of order 1). The owner's starts (`owner.json`) and hand fixes
(`fixes.json`) still win over these.
