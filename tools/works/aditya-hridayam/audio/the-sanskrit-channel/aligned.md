# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every śloka of The Sanskrit Channel's recording (`qLXRj4HIdJA`), the start found by torchaudio's `MMS_FA`
aligner run on the known text (romanised), with a wildcard between every two lines for what the recording has that the
text does not (the title अथ श्रीआदित्यहृदयस्तोत्रम् at the start, अथ फलश्रुतिः before śloka 25, इति आदित्यहृदयस्तोत्रम् and
music at the end), in the windows `mms_windows.py` cut from the transcript's rough starts (`tools/audio/METHOD.md`, steps
1–4; the `align` workflow). Each start is MMS's minus 0.6 s, the default lean for a recording the owner has not yet timed
by ear. All 31 ślokas scored 0.5 or more. The recording does not recite the viniyoga or the nyāsas (`recordings.json` →
`from` `sh1`); they stay untimed.

**Checked:** every start against the transcript (`transcripts/qLXRj4HIdJA.jsonl`, Whisper small): each lands where the
transcript hears the śloka begin (śloka 1 at 8 s, 22 at 389 s, 31 at 554 s). `check.json` lists the three verses the
automatic checks flag, where MMS and the transcript's coarse segments are more than 2 s apart: ślokas 6 (96.5 s, inside
the transcript's piece from 91.8 s), 11 (187.3 s, inside the piece from 183.3 s) and 25 (447.1 s, after the spoken अथ
फलश्रुतिः at 443 s); each is where the śloka's first words fall in its piece. The source is published for review
(`source.json` "review"), so every start is on the owner's to-check list in ☰ › More settings › Audio timing.

**How good:** not scored yet. The score on the owner's starts set by ear is made once he has set 20 or so on this
recording; his first starts also measure its lean, which then replaces 0.6 s.

The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
