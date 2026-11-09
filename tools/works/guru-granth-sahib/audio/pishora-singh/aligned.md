# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Bhai Pishora Singh Ji's Sahaj Paath of the Sri Guru Granth Sahib (66 recordings of about an
hour, `recordings.json`), the start and end found by torchaudio's `MMS_FA` aligner run on the known text (its
transliteration in plain letters), with a wildcard between every two lines and at both ends for anything not in the text
(`tools/audio/METHOD.md`, steps 2–4), in the windows `mms_windows.py` cut from the transcript's rough starts
(`mms/windows.json`); one run per recording in the public `align` workflow (`mms_align.py`, raw results in
`mms/<video id>.json`); `mms_merge.py --lean 0.55` writes `aligned.json` and `check.json`. The rough starts come from
matching each recording's transcript line by line (`"align": "anchors"`), between the verse in progress where its first Ang
begins (`from`) and the last verse beginning on its last Ang (`to`). The lean, 0.55 s, is the Japji Sahib recording's (the
same script, read aloud); it is not yet scored on the owner's starts set by ear for this recording. 5,926 of the 6,017 verses
take MMS's start; those MMS scored below 0.5 keep the transcript's and are listed to check.

**How good:** not yet scored: there are no starts set by ear for this recording (`owner.json`). Scoring needs 20 or more,
spread over several volumes (`tools/audio/mms_score.py`); until then the source stays a draft.

**To check** (`check.json`, the checks of METHOD.md step 4, verses the owner has not set): 1,991 (MMS and the transcript
more than 2 s apart 1,935, low score 56, out of pace 7). Most of the first are the transcript's rough starts, which are
spread by length between the lines matched word for word, not MMS's. The opening two minutes of volumes 21 and 66 match no
verse. The owner's starts (`owner.json`) and hand fixes (`fixes.json`) still win over these.
