# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Ashtotrashat Namavali's recording of Shri Sathya Sai Ashtottara Shatanamavali (YouTube `mLBceWHiVZA`), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.6` writes `aligned.json` and `check.json`. Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it). 76 of the 108 verses MMS was given take its start; 32 it scored below 0.5 and are left to the transcript: set by the owner by ear nama.n2, nama.n5, nama.n9, nama.n12, nama.n13, nama.n14, nama.n15, nama.n17, nama.n27, nama.n29, nama.n30, nama.n39, nama.n40, nama.n43, nama.n45, nama.n62, nama.n65, nama.n70, nama.n71, nama.n72, nama.n74, nama.n78, nama.n79, nama.n80, nama.n81, nama.n82, nama.n86, nama.n87, nama.n92, nama.n100, nama.n103, nama.n105.

**How good:** scored on the owner's 58 starts set by ear (`owner.json`; `tools/audio/mms_score.py`):

26 owner starts scored; lean 0.6 s (median of MMS minus the owner: 0.60 s)
| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 26 (100%) | 0 | 0 | 0.08 s | 0.11 s |
| MMS, lean 0.6 s removed | 25 (96%) | 0 | 1 | 0.00 s | 0.20 s |

MMS is not better on both counts here; his starts win over both wherever he has set them.

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 0.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
