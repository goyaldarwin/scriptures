# Line starts from Meta's MMS (`aligned.json`, `lines.json`)

**What:** for Shabad Guru (Kirtan)'s 10 recordings (0.9 h; `recordings.json`), every singing of every line of the verse each sings, found in MMS's frame-by-frame letter probabilities (torchaudio `MMS_FA`, the whole track at once) by `tools/audio/line_align.py`: a search through how a shabad is sung (the rahao before the first pada and after each, lines and padas sung again, a stanza on its own) with a filler for what the text does not hold (alaap, music, a dhaarna, lines of another shabad), and the plain in-order alignment beside it (`tools/audio/METHOD.md`, "Line by line"); one run per recording in the public `align` workflow (`mms_align.py`, raw results in `mms/<video id>.json`); `mms_merge.py` writes `aligned.json` (each verse's first singing), `lines.json` (the singings the search scores 0.35 or more, and the in-order alignment's first singings of lines it left out, where the lines around place them: `line_align.merge`) and `check.json`. Each start is MMS's less the lean, 0.6 s until the owner has set starts by ear here.

**Figures:** 102 of 196 lines have a start; 111 singings (8 first singings from the in-order alignment; 10 more MMS scored below 0.35, dropped); verses flagged: title 3, unsung 4; to check 4.

**How good:** not scored yet: the owner has not set starts by ear on these recordings, and his marks are per verse; starts heard in 5-s windows (`tools/audio/windows.py`) are the check until then (`fixes.md`, where any are recorded).

**To check** (`check.json`, verses the owner has not set): 4; the source is published for review (`source.json` "review"), so every verse not set by ear is on his to-check list.
