# Verse starts from Meta's MMS forced aligner (`aligned.json`)

**What:** for every śloka of Sri Sathya Sai Official's recording (`Z7W59S6fH98`), the start found by torchaudio's `MMS_FA`
aligner run on the known text (romanised), with a wildcard between every two lines for what the recording has that the
text does not (its opening music, the closing Om śānti), in the windows `mms_windows.py` cut from the transcript's rough
starts (`tools/audio/METHOD.md`, steps 1–4; the `align` workflow). Each start is MMS's minus 0.6 s, the default lean for a
recording the owner has not yet timed by ear. All 31 ślokas scored 0.5 or more. The viniyoga and the nyāsas are not
recited (`recordings.json` → `from` `sh1`) and stay untimed.

**Checked:** every start against the transcript (`transcripts/Z7W59S6fH98.jsonl`, Whisper small): each lands where the
transcript hears the śloka begin (śloka 7 at 121 s, 22 at 370 s, 31 at 510 s). `check.json` lists the one verse the
automatic checks flag: śloka 1, where MMS (20.6 s) and the transcript's coarse segment (18.2 s) are more than 2 s apart;
the transcript's piece also holds the music before it. The source is published for review (`source.json` "review"), so
every start is on the owner's to-check list in ☰ › More settings › Audio timing.

**How good:** not scored yet. The score on the owner's starts set by ear is made once he has set 20 or so on this
recording; his first starts also measure its lean, which then replaces 0.6 s.

The owner's starts (`owner.json`) and hand fixes (`fixes.json`) win over these.
