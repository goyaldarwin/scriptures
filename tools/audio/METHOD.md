# How verse times are made, checked and fixed

The method for every recording. What each step uses, what is built and what is still to build is marked. The Mānas
(Pt. Kamlesh Upadhyay) is the reference: its figures below are scored on the owner's starts and ends set by ear
(`tools/works/manas/audio/kamlesh-upadhyay/owner.json`; figures and method: `aligned.md` beside it).

## Why: a verse's end is the next verse's start

The app lights a verse until the next one starts, unless the verse has a set end. Machine timings set no ends, so a
verse that overruns into the next is the next verse's start being late. On the owner's 450 Mānas ends set by ear, the
next verse started:

| Next verse starts… | the owner's own start | Whisper's | MMS's |
|---|---|---|---|
| more than 2 s after the end | 63 | 137 | 104 |
| more than 5 s after (an overrun) | 8 | 72 | 9 |
| more than 1 s before (too early) | 1 | 176 | 6 |

The owner's 63 are real gaps: a refrain or music between two verses. MMS's 104 are mostly those gaps: the verse stays lit
through the refrain because it has no end.

## The steps

1. **Rough placement: Whisper** (built: the `transcribe` workflow, `make_timings.py`). The transcript matched to the
   text gives each verse a rough start. It also shows a recording that skips, repeats or reorders verses (a forced
   aligner assumes the text is all there, in order), and it cuts the recording into windows for step 2.
2. **Exact starts: Meta's MMS forced aligner** (built: `mms_windows.py` cuts the windows from step 1, the `align` workflow
   runs `mms_align.py` on each recording in this repository's free Actions, `mms_merge.py` writes `aligned.json`, read by
   `make_timings.py`; the Mānas's first run is in `scriptures-data`, `experiments/align/`). In windows of a minute or two from step 1, overlapping by a verse,
   MMS is given the known text (romanised) with a wildcard between every two lines and at both ends, which absorbs
   refrains and music not in the text. A song whose transcript placed too few verses to cut windows by (fast singing, chant) is given
   one window, its whole track, with every verse it sings (`mms_windows.py --whole`). Each start is moved by the recording's lean against the owner's starts (0.64 s
   for the Mānas; a new recording uses 0.6 s until the owner has set 20 or so by ear). A start MMS scores below 0.5
   keeps step 1's start and goes on the to-check list (`check.json`).
   Mānas, on the owner's 637 starts: within 1 s 78% (Whisper alone 46%), more than 3 s off 5% (34%).
3. **Ends: from MMS** (built: `mms_align.py` saves each verse's end, `mms_merge.py` passes it on, `make_timings.py` applies
   the rule). MMS knows where each line's last syllable ends. A verse's end is
   its last line's end + 0.3 s, kept only where the next start is more than 1.5 s later (a refrain or music), so the
   light moves on to the next verse when this one's singing ends, not when the next one begins.
4. **Find the errors** (built in `mms_merge.py`, into `check.json`, except listener flags, which the app adds), with no ear needed. A verse is flagged when:
   - MMS and Whisper disagree by more than 2 s;
   - MMS scores any of its lines below 0.5;
   - its length is out of pace: its time against its length in mātrās (syllables for prose and Sanskrit), compared with
     the reciter's pace over the verses around it, is less than half or more than double (an overrun shows as one verse
     too long and the next too short);
   - it starts before the verse before it starts or ends;
   - a listener has marked it "Review audio timing".
5. **Fix them** (to build), in order, each only if the one before fails:
   1. align again just the stretch between the nearest trusted starts on each side (the owner's, or MMS's unflagged);
   2. move the start to the nearest onset of singing within ±1.5 s;
   3. spread it by its length between the trusted neighbours, and put it on the to-check list.
   Until these are built, a session checks a flagged start by hearing its stretch in 5-s windows a second apart
   (`windows.py`: the last window that still begins with the line's first words is at the start), never by a transcript
   segment's start (it may open on music or the line before), and sets it in `fixes.json` with the windows in `fixes.md`. A start so set leaves the to-check list; where MMS's start agrees with the windows (within a second) the hand start is not kept and MMS's stands; where the windows do not settle a start, the start stays, `fixes.md` says so and `check.json` → `also` keeps it on the list. A word held long (a sung जय) or a line sung twice makes several windows in a row begin with the line's first words: then the windows that hear the line before, or the line's later words, decide, and where they cannot the start is listed.
6. **The owner's ear** (built: timing mode, the `timing` workflow, `owner.json`). His starts and ends always win. Each
   start he sets becomes an anchor: the stretch up to his next set start is aligned again (to build), so the verses
   around it improve without being touched, and his first starts on a recording measure its lean.

## Line by line: kirtan (every singing of every line)

In kirtan a verse (a whole shabad) is one recording of a few minutes, and its lines are sung again and again: the rahao
(refrain) opens the song and returns after every pada, lines are sung twice, padas again, and a ragi adds an alaap, a
manglacharan or a dhaarna, or lines of another shabad. A source like this (`source.json` `"lines": true`) is timed line by
line: MMS finds every singing of every line, and the app lights the lines moving forward only, each from its first singing after the line before (the app's `lines`, `docs/LIBRARY.md` §4):

1. **No transcript:** Whisper places little in singing, and each recording is one verse (`recordings.json` `from`/`to`),
   so the step 1 windows are not needed: each track is one window, its whole length, carrying its verses' text
   (`mms_windows.py`, which a "lines" source always cuts so).
2. **MMS on the whole track** (`mms_align.py` → `line_align.py`): from MMS's frame-by-frame letter probabilities, the best
   path through a grammar of how a shabad is sung: a pada line by line (a line again, back to an earlier line of the
   pada, a line left out at a cost, a heading — ਮਹਲਾ, ਸਲੋਕੁ, ੴ … — at none); the rahao before the first pada and after
   each, as often as sung; the next pada, or a later one at a cost (a chhant's stanza sung on its own, one recording
   each); and between any two lines a filler for what the text does not hold, which costs a frame its best letter less a
   penalty, so a line is placed only where its own letters are heard about as well as anything else. Beside it the plain
   in-order alignment (each line once, in order, a filler between: step 2 above) gives each line's first singing.
3. **Checks** (`mms_merge.py` → `check.json`): the letters MMS hears are compared with the verse and with every other
   verse of the work (`title`: the recording may not sing the verse its title names); a line with no singing scored 0.5
   or more (`unsung`); first singings that differ by more than 2 s between the two searches for more than a quarter of
   the verse's lines (`first`). Singings MMS scores below 0.5 are dropped. Starts move by the lean (0.6 s until the
   owner has set some by ear).
4. **By ear:** a flagged line is heard in 5-s windows (`windows.py`), as in step 5 above. The owner's marks in the app are
   per verse (its first singing); the lines are MMS's.

The search's costs (`line_align.py` `P`) were tuned on the first recordings of the source that uses them; its `aligned.md`
gives the figures.

## When a recording uses steps 2–5

**A new recording** uses steps 2–5 at once and is published without waiting for the owner's ear (the owner: "Don't wait
for me to review the recordings"); its lean is 0.6 s until he has set starts on it, and what the checks flag is on his
to-check list.

**A recording already timed from step 1 alone** switches once steps 2–5 score better on the owner's starts set by ear for
it (20–30 are enough; the Kaṭha Upaniṣad has 75; `mms_score.py`): within 1 s and more than 3 s off, against step 1 alone,
the same table as `aligned.md`, with the figures recorded beside the recording (`aligned.md`). On the owner's word it may
switch before he has set any start (the Gītā's, the Vālmīki Rāmāyaṇa's): it is then published for review (`source.json`
"review"), so every start stays on his to-check list until scored.

## Where it runs

In the public repo's Actions (free), the `align` workflow, like `transcribe`, and like it with at most 14 jobs at once, so the checks, the site's
publishing and the owner's timing submissions are never queued behind it (`docs/PLAYBOOK.md`, "GitHub Actions minutes").
Many short recordings (kirtan: a few minutes each) share a job (`per_job`, e.g. 25), so a machine's setup (about a minute)
is paid once per job and a run of 256 jobs holds thousands of recordings. MMS takes about as long as the audio.
The whole Mānas with MMS is about 2,350 runner minutes.
MMS's weights (`model.pt`, about 1.2 GB) come from Meta's `dl.fbaipublicfiles.com`; when that download fails (its certificate
expired once), the `align` workflow takes the same file from its copy on Hugging Face (`seanghay/khmer-forced-aligner`) and
accepts it only with the SHA-256 pinned in `align.yml`: the file whose alignments of two recordings already aligned with
Meta's download (the Kuber and Chandraghanta āratīs) came out identical, start, end and score of every verse.

## Still to apply it to

The recordings `docs/WORKS.md` lists as timed from the transcript alone (its last section, made by the build).
