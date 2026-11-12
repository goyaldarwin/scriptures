# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of VedicQB's recording of Shri Lalita Chalisa (YouTube `zAGrcGMkh90`), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.6` writes `aligned.json` and `check.json`. Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it). 37 of the 48 verses MMS was given take its start; 11 it scored below 0.5 and are left to the transcript: listed to check chalisa.cau5, chalisa.cau15, chalisa.cau33, chalisa.cau37, chalisa.cau38, chalisa.cau39, chalisa.cau40, chalisa.cau41, chalisa.cau43, chalisa.cau44, chalisa.do1.

**How good:** not scored yet: the owner has not set starts by ear on this recording. His first 20 or so will measure its lean and score MMS against the transcript (`tools/audio/mms_score.py`).

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 15.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
