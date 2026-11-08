# MMS on this recording: ready, not yet used

`mms/ZIDdE4SZAuw.json` holds MMS's starts for every verse (the `align` workflow on `mms/windows.json`). They are not used yet:
`tools/audio/METHOD.md` switches a recording only after scoring MMS on the owner's starts set by ear, 20 or so, and he has
set 0 on this one. Once he has, `python3 tools/audio/mms_score.py tools/works/ramraksha/audio/vande-guru-paramparaam` scores them; if MMS is better,
`mms_merge.py tools/works/ramraksha/audio/vande-guru-paramparaam --lean <its lean>`, then `make_timings.py`, and `aligned.md` from the score.
