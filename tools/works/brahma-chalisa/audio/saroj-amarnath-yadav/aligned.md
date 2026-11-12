# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Saroj Amarnath Yadav's recording of Shri Brahma Chalisa (YouTube `7lfOLotn17A`, its track 52.0–348.74 s), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.6` writes `aligned.json` and `check.json`. Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it). 19 of the 21 verses MMS was given take its start; 2 it scored below 0.5 and are left to the transcript: listed to check chalisa.cau35, chalisa.cau36.

**How good:** not scored yet: the owner has not set starts by ear on this recording. His first 20 or so will measure its lean and score MMS against the transcript (`tools/audio/mms_score.py`).

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 8.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
