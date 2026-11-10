# MMS on this recording: run, every start unsure

`mms/Yi9TFXQYL-4.json` holds MMS's starts for the five verses (the `align` workflow on `mms/windows.json`, cut from the rough starts of `fixes.md`). MMS scores every one below 0.5 (the āratī is sung over a harmonium, the refrain after every stanza), so by `tools/audio/METHOD.md` none replaces the transcript's start (`aligned.json` is empty; `check.json` flags all five, `mms_merge.py --lean 0.6`). The starts are those checked in the transcript (`fixes.json`, evidence in `fixes.md`), which the to-check list leaves out as it does every start in `fixes.json`.

| Verse | Transcript (`fixes.json`) | MMS (score) | Apart |
|---|---|---|---|
| aarti.tek | 3312.0 | 3323.5 (0.28) | 11.5 s: the music starts at 3306 s and the transcript hears the refrain's first line from 3312 s; MMS took its repeat |
| aarti.pad1 | 3333.6 | 3333.9 (0.27) | 0.3 s |
| aarti.pad2 | 3360.2 | 3360.5 (0.31) | 0.3 s |
| aarti.pad3 | 3387.2 | 3387.2 (0.38) | 0.0 s |
| aarti.pad4 | 3413.2 | 3413.8 (0.42) | 0.6 s |

The four stanzas agree within 0.6 s. The owner's starts set by ear, when he sets them, win and score both.
