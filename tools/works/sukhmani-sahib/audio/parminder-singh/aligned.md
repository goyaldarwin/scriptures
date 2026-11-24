# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Parminder Singh (Australia)'s recording of Sukhmani Sahib (YouTube `KJ8D_ObQNzQ`), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.6` writes `aligned.json` and `check.json`. Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it). 182 of the 218 verses MMS was given take its start; 36 it scored below 0.5 and are left to the transcript: set by the owner by ear a01.p4, a01.p6, a01.p7, a02.salok, a02.p2, a02.p6, a03.salok, a04.salok, a04.p2, a06.salok, a06.p8, a08.salok, a08.p1, a08.p3, a08.p7, a09.p6, a10.salok, a11.salok, a13.salok, a14.salok, a14.p2, a15.salok, a16.salok, a16.p2, a17.p6, a19.salok, a20.salok, a20.p4, a20.p7, a21.salok, a23.salok, a23.p2, a23.p6, a24.salok, a24.p2; not sung a07.salok.

**How good:** scored on the owner's 184 starts set by ear (`owner.json`; `tools/audio/mms_score.py`):

149 owner starts scored; lean 0.55 s (median of MMS minus the owner: 0.55 s)
| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 48 (32%) | 76 | 25 | 1.51 s | 1.79 s |
| MMS, lean 0.55 s removed | 143 (96%) | 4 | 2 | 0.21 s | 0.49 s |

MMS is better on both counts.

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 0.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
