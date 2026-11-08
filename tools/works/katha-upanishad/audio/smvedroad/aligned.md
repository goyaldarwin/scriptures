# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of SMVedroad's recording of the Kaṭha Upaniṣad (`NQhdLn7FHwA`), the start and end found by
torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two
lines and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut
from the transcript's rough starts (`mms/windows.json`); one run per recording in the public `align` workflow
(`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py --lean 0.08` writes `aligned.json` and `check.json`.
Each start is MMS's minus 0.08 s, the median lean of MMS against the owner's starts set by ear. 118 of the 120 verses
take MMS's start; those MMS scored below 0.5 keep the transcript's and are listed to check.

**How good:** scored on 62 of the owner's starts set by ear (`owner.json`) that MMS and the transcript both time
(`tools/audio/mms_score.py`):

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 11 (18%) | 25 | 26 | 2.38 s | 6.37 s |
| MMS, lean 0.08 s removed | 57 (92%) | 4 | 1 | 0.19 s | 0.65 s |

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 6.
The owner's starts (`owner.json`) and hand fixes (`fixes.json`) still win over these.
