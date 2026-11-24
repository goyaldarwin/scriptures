# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Sounds of Isha's recording of Bilvashtakam (YouTube `6rJExE8HGVg`), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.6` writes `aligned.json` and `check.json`. Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it). 4 of the 9 verses MMS was given take its start; 5 it scored below 0.5 and are left to the transcript: listed to check sh2; set by hand sh1, sh5, sh6, kashi.

**By hand:** 8 starts set by hand win over these (`fixes.json`, each with the 5-s windows or words it was read from in `fixes.md`): kashi, sh1, sh3, sh4, sh5, sh6, sh7, sh8.

**How good:** not scored yet: of the owner's 7 starts set by ear here, 2 are timed by both MMS and the transcript, fewer than the 20 or so a score needs (`tools/audio/mms_score.py`).

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 1.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
