# MMS on this recording: scored, not yet used

`mms/QjSpUgnEPLU.json` holds MMS's starts for every verse (the `align` workflow on `mms/windows.json`). Scored on the
owner's 46 starts set by ear that MMS and the transcript both time (`tools/audio/mms_score.py`):

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 17 (37%) | 2 | 27 | 5.05 s | 12.63 s |
| MMS, lean 0.55 s removed | 42 (91%) | 1 | 3 | 0.14 s | 0.48 s |

It is not used yet, for the owner to decide: MMS scores 181 of the 408 verses below 0.5 (the reciter sings the Mānas's
caupāīs to a tune, with long held notes), so switching would put 200 verses on the to-check list of a recording whose
list is empty now, and would move 11 starts the owner has not set by more than 3 s (sundar.41.do41 by 26 s). To switch:
`python3 tools/audio/mms_merge.py tools/works/sundarkand/audio/ashwin-pathak --lean 0.55`, then `make_timings.py` for this
source and for `tools/works/hanuman-aarti/audio/ashwin-pathak`, and write `aligned.md` from the table above.
