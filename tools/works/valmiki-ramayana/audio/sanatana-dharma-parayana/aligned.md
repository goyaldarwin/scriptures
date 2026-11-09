# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Sanatana Dharma Parayana's 467 recordings (one per sarga), the start found by torchaudio's
`MMS_FA` aligner run on the known text (romanised), with a wildcard between every two lines for what the recording has that
the text does not, in the windows `mms_windows.py` cut from the transcript's rough starts (`tools/audio/METHOD.md`,
steps 1–4). Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not yet timed by ear. 17,291 of
the 17,623 verses take MMS's start; the 332 MMS scored below 0.5 keep the transcript's.

**Checked:** `check.json` lists the 1,622 verses the automatic checks flag (MMS and the transcript more than 2 s apart 1,289,
low score 332, out of pace 9). Against the transcript's starts used before, the median start moved 0.68 s; 342 moved more
than 3 s. The source is published for review (`source.json` "review", on the owner's word, before any start was set by
ear), so every start is on the owner's to-check list in ☰ › More settings › Audio timing.

**How good:** not scored yet. The score on the owner's starts set by ear (within 1 s, more than 3 s off, against the
transcript alone, as in the Mānas's `aligned.md`) is made once he has set 20 or so on this recording (`mms_score.py`); his
first starts also measure its lean, which then replaces 0.6 s.

The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
