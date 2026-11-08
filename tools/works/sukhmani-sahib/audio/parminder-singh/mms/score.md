# MMS on this recording: ready, not yet used

`mms/KJ8D_ObQNzQ.json` holds MMS's starts for every verse (the `align` workflow on `mms/windows.json`). They are not used
yet: `tools/audio/METHOD.md` switches a recording only after scoring MMS on 20 or so of the owner's starts set by ear, and
only 7 of his 11 here are timed by both MMS and the transcript. On those 7 (`tools/audio/mms_score.py`, lean 0.6 s):

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 3 (43%) | 0 | 4 | 6.00 s | 5.07 s |
| MMS, lean 0.6 s removed | 5 (71%) | 0 | 2 | 0.38 s | 4.28 s |

Once he has set 20 or so, run `mms_score.py` again; if MMS is better, `mms_merge.py tools/works/sukhmani-sahib/audio/parminder-singh --lean <its lean>`, then `make_timings.py`, and `aligned.md` from the score.
