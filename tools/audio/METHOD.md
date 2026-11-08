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
   refrains and music not in the text. Each start is moved by the recording's lean against the owner's starts (0.64 s
   for the Mānas; a new recording uses 0.6 s until the owner has set 20 or so by ear). A start MMS scores below 0.5
   keeps step 1's start and goes on the to-check list (`check.json`).
   Mānas, on the owner's 637 starts: within 1 s 78% (Whisper alone 46%), more than 3 s off 5% (34%).
3. **Ends: from MMS** (built: `mms_align.py` saves each verse's end, `mms_merge.py` passes it on, `make_timings.py` applies
   the rule). MMS knows where each line's last syllable ends. A verse's end is
   its last line's end + 0.3 s, kept only where the next start is more than 1.5 s later (a refrain or music), so the
   light leaves the verse when the singing does.
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
6. **The owner's ear** (built: timing mode, the `timing` workflow, `owner.json`). His starts and ends always win. Each
   start he sets becomes an anchor: the stretch up to his next set start is aligned again (to build), so the verses
   around it improve without being touched, and his first starts on a recording measure its lean.

## Before a new recording uses steps 2–5

Score them on the owner's starts set by ear for that recording (20–30 are enough; the Katha Upaniṣad has 75; `mms_score.py`): within 1 s,
more than 3 s off, against step 1 alone, the same table as `aligned.md`. Switch only when they are better, and record the
figures beside the recording (`aligned.md`).

## Where it runs

In the public repo's Actions (free), the `align` workflow, like `transcribe`, and like it with at most 14 jobs at once, so the checks, the site's
publishing and the owner's timing submissions are never queued behind it (`docs/PLAYBOOK.md`, "GitHub Actions minutes").
The whole Mānas with MMS is about 2,350 runner minutes.

## Next to apply it to

The Śrīmad Bhāgavata Mahāpurāṇa and the Upaniṣads, where the owner hears starts and ends off.
