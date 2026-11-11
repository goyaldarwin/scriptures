# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Bhajan aur Aarti — Badrinath Kedarnath Gangotri Yamnotri's recording of Om Jai Gangadhar (YouTube `Zn78FYVwbZM`), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.6` writes `aligned.json` and `check.json`. Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not timed by ear (20 or so of his starts measure it). 4 of the 9 verses MMS was given take its start; 5 it scored below 0.5 and are left to the transcript: set by hand aarti.tek, aarti.pad3, aarti.pad5, aarti.pad8; set by the owner by ear aarti.pad4.

**By hand:** 4 starts set by hand win over these (`fixes.json`, each with the 5-s windows or words it was read from in `fixes.md`): aarti.pad3, aarti.pad5, aarti.pad8, aarti.tek.

**How good:** not scored yet: of the owner's 4 starts set by ear here, 1 are timed by both MMS and the transcript, fewer than the 20 or so a score needs (`tools/audio/mms_score.py`).

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 0.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
