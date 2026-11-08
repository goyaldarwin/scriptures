# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for Braja Beats's recording of the Śrī Durgā Saptaśatī (`zmGU9QbLUVM`, 3 h 28 min), each item's start and end found by torchaudio's `MMS_FA` aligner run on the known text (its transliteration in plain letters), with a wildcard between every two items and at both ends for anything not in the text (`tools/audio/METHOD.md`, steps 2–4). 127 windows of about 90 s around the rough starts (`mms/windows.json`, `tools/audio/mms_windows.py`); one run in the public `align` workflow (`mms_align.py`), whose raw starts, ends and scores are `mms/zmGU9QbLUVM.json`; `mms_merge.py --lean 2.0` writes `aligned.json` and `check.json`. Each start here is MMS's minus 2.0 s, its median lean against the owner's 101 starts set by ear (1.98 s): the owner marks a start where the item before it ends, so his starts take in the pause before the singing. Starts MMS scored below 0.5 are left out: those items keep the transcript's start and are listed to check. 698 of the 867 items take MMS's start; of the 169 it scored low, 66 are adhyāya 5's short namaskāras (नमस्तस्यै ॥, sung as one refrain).

**How good:** scored on the owner's 101 starts set by ear (`owner.json`: the Caṇḍikā-dhyāna, Argalā, the Kīlaka's colophon, the Kavaca and adhyāya 1's viniyoga), each compared with his:

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 27 (27%) | 39 | 35 | 2.00 s | 3.19 s |
| MMS, lean removed | **94 (93%)** | 2 | **5** | **0.21 s** | **0.86 s** |

- The five misses over 3 s are where a section begins: `1.viniyoga` (36.4 s; the owner's start takes in what is sung before the viniyoga), `dhyana.1` (8.0 s early), `argala.viniyoga` (7.4 s), `kilaka.iti` (5.4 s early) and `kilaka.viniyoga` (3.8 s). The owner's starts win there.
- All 101 are in the opening stotras and the start of adhyāya 1; the adhyāyas' lean is assumed the same (one reciter, one recording).

**To check** (`check.json`, the checks of METHOD.md step 4): MMS score below 0.5 (155), MMS and the transcript more than 2 s apart (306), out of pace (80), a start before the item before (4): 484 items. The owner's starts (`owner.json`) still win over all of these.
