# MMS on this recording: run, not yet used

`mms/<video id>.json` holds MMS's starts for every verse of all 467 recordings (the `align` workflow on `mms/windows.json`,
`tools/audio/METHOD.md` steps 2–4). With the default lean of 0.6 s, `mms_merge.py` would take 17,291 of the 17,623 verses'
starts from MMS (332 score below 0.5 and keep the transcript's) and put 1,622 on the to-check list (MMS and the transcript
more than 2 s apart 1,289; low score 332; out of pace 9).

It is not used yet: METHOD.md switches a recording only once MMS has been scored on the owner's starts set by ear for it,
and this recording has none (`owner.json`). When he has set 20 or so: `python3 tools/audio/mms_score.py` on this source
(it gives the lean and the table for `aligned.md`); if MMS is better, `python3 tools/audio/mms_merge.py
tools/works/valmiki-ramayana/audio/sanatana-dharma-parayana --lean <lean>`, then `make_timings.py` for this source, and
`aligned.md` from the table.
