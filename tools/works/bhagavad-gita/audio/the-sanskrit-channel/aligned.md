# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of The Sanskrit Channel's recording (`WITUOwi3EYk`), the start found by torchaudio's `MMS_FA` aligner run on the
known text (romanised), with a wildcard between every two lines for what the recording has that the text does not (the
opening invocation, each adhyāya's spoken title, the spoken meanings), in the windows `mms_windows.py` cut from the transcript's rough starts
(`tools/audio/METHOD.md`, steps 1–4). Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not
yet timed by ear. A verse's end is kept where the next verse starts more than 1.5 s after it (28 verses). Starts MMS scored below 0.5
keep the transcript's.

**Checked:** each adhyāya's first verse and its colophon (ॐ तत्सदिति …) against the transcript: all land where the transcript
hears them. `check.json` lists the 330 verses the automatic checks flag (mostly MMS and the transcript more than 2 s apart,
where the transcript is the one astray); the source is published for review (`source.json` "review"), so every start is on
the owner's to-check list in ☰ › More settings › Audio timing.

**How good:** not scored yet. The score on the owner's starts set by ear (within 1 s, more than 3 s off, against the
transcript alone, as in the Mānas's `aligned.md`) is made once he has set 20 or so on this recording; his first starts also
measure its lean, which then replaces 0.6 s.

The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
