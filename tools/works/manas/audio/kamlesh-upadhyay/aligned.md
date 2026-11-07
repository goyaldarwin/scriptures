# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Pt. Kamlesh Upadhyay's Mānas, the start found by torchaudio's `MMS_FA` aligner run on the known
text (romanised), with a wildcard between every two lines for sung material that is not in the text. The run, its code and
its raw results are in `scriptures-data`, `experiments/align/` (README there). Each start here is MMS's minus 0.64 s, its
median lean against the owner's starts set by ear. Starts MMS scored below 0.5 (mean token score) are left out: on the
owner's starts every one of them was more than 3 s off. Those verses take the transcript's start and are listed in
`check.json`.

**How good:** scored on the owner's 637 starts set by ear (`owner.json`), each start compared with his:

| Starts | within 1 s | 1–3 s | more than 3 s | median miss | mean miss |
|---|---|---|---|---|---|
| Whisper transcript matched to the text (`make_timings.py` alone) | 295 (46%) | 124 | 218 (34%) | 1.20 s | 4.36 s |
| MMS, lean removed | **497 (78%)** | 108 | **32 (5%)** | **0.54 s** | **0.87 s** |

- The 136 verses where the two differed by more than 5 s (the owner set all of them): MMS within 1 s on 113, more than 3 s
  off on 4; the transcript within 1 s on 1, more than 3 s off on 134.
- The other 501: MMS within 1 s on 77% (transcript 59%), more than 3 s off on 6% (transcript 17%).
- By verse type, within 1 s (transcript / MMS): caupāī 49% / 85%, dohā 41% / 59%, chand 42% / 76%, sorṭhā 35% / 40%,
  śloka 36% / 91%. Dohās and sorṭhās, sung after the reciter's refrain, are its weakest; they are still better than the transcript's.
- Using MMS only where the two differ by more than 1, 2, 3 or 5 s, at any confidence threshold, scores below MMS everywhere
  (72%, 70%, 69%, 64% within 1 s), so MMS gives every start it is sure of.

Caveat: the owner's starts are mostly where the two disagreed and around them, not a random sample; on the others MMS still
leads.

The owner's starts (`owner.json`) and hand fixes (`fixes.json`) still win over these.
