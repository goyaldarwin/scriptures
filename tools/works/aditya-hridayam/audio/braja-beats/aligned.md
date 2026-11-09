# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every verse of Braja Beats's recording (`I8Xg_2RC5Vk`), the start found by torchaudio's `MMS_FA` aligner run
on the known text (romanised), with a wildcard between every two lines for what the recording has that the text does not
(its opening music), in the windows `mms_windows.py` cut from the transcript's rough starts (`tools/audio/METHOD.md`, steps
1–4; the `align` workflow). Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not yet timed
by ear. 30 of the 32 verses (the 31 ślokas and the closing words) scored 0.5 or more; ślokas 10 and 22 scored lower and
keep the transcript's starts. The viniyoga and the nyāsas are not recited (`recordings.json` → `from` `sh1`) and stay
untimed.

**Checked:** every start against the transcript (`transcripts/I8Xg_2RC5Vk.jsonl`, Whisper small): each lands where the
transcript hears the verse begin (śloka 1 at 8 s, 31 at 320 s, the closing words at 333 s). `check.json` lists ślokas 10
and 22 (MMS's low score); their transcript starts (99.7 s, 227.0 s) sit where the transcript hears आदित्यः सविता and
नाशयत्येष. The source is published for review (`source.json` "review"), so every start is on the owner's to-check list in
☰ › More settings › Audio timing.

**How good:** not scored yet. The score on the owner's starts set by ear is made once he has set 20 or so on this
recording; his first starts also measure its lean, which then replaces 0.6 s.

The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
