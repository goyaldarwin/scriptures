# Handoff: an independent review of the audio-timing logic

Written 2026-10-20. The "Audio timing" feature (marking when each verse starts and ends in a recitation, by ear, in the app) grew through many rounds of owner feedback and bug fixes in one long session. The owner wants a fresh, independent reviewer to check it end to end. Paste the prompt below into a new session.

---

## Prompt

> You are reviewing one feature of Darwin Goyal's (`goyaldarwin`) scriptures library: **marking verse timings by ear** ("Audio timing"). The site is https://scriptures.craadle.org, built from the public repo `github.com/goyaldarwin/scriptures` (`main` is live). Clone it and read `CLAUDE.md`, `docs/START-HERE.md`, then `docs/PLAYBOOK.md` → the section **"Audio timing by ear"** (the owner's rules, which are the specification), and this file, `docs/handoff/2026-10-20-timing-review.md`.
>
> The logic was built incrementally with many bugs found by the owner on his phone. **Review it as a skeptical, independent reviewer:** find every bug, inconsistency and unhandled case; prove each with a concrete reproduction (a sequence of taps and times, or a failing test); then fix them, with tests, without changing the owner's rules. If a rule itself looks wrong or two rules conflict, do not change it: list it for the owner with a recommendation.
>
> Report to the owner in plain words (he reads on his phone): what was wrong, what you changed, what he should try, and the open questions. Do not change anything else in the app.

---

## What the feature does (the owner's view)

A reader (the owner, or a helper) turns on **Settings › Audio timing**, plays a work's recording, and marks verses as they are heard:

- Under every verse: **⏱ Starts now** and **⏹ Ends now**. A verse marked by you shows **−** and **+** on either side of each (start ± only when you set the start; end ± only when an end is set). Each − / + moves the time by a step chosen in the verse's **⋮** menu (0.1 / 0.25 / 0.5 / 1 s, default 0.5) and plays a **2-second preview** (the first 2 s from a new start, the last 2 s up to a new end), then pauses.
- The line under the buttons shows the verse's start (and end), and whether it is **yours**, **estimated** (a machine guess, to be checked), **from <helper>** (from a helper's file), or **moved to fit your times**.
- **The light waits for you:** while playing, the highlighted verse never moves on to a verse whose start is only a guess. It stays on your verse until you mark the next start, or until a set end passes (then it moves to the next verse at once, so its start can be marked during the music, and waits there).
- **Ends only stop playback** of a single verse or the last verse of a stretch; when playing through, nothing is skipped. Most verses need no end ("Until next" in the ⋮ menu removes one).
- **Order is kept**, with the same rule in the app and in the generator, so what you see is what gets published: a verse never starts before the previous one or before its set end; unset verses that break this are re-placed by text length between good times; an end later than the next verse's set start is cut back to it.
- **Neighbours move together:** an end pushed past the next verse's start (one you set) carries that start along; a start pulled before the previous verse's set end pulls that end back. Refused only if it would squeeze a neighbour to nothing.
- **"Ends now" on a verse whose estimated start lies after now** (the estimate was late): its start becomes the previous verse's set end (that is when the light moved to it); without one, the app asks for "Starts now" first.
- **The page never moves under your finger while marking:** a mark does not scroll; the page follows the light only when the lit verse leaves the screen.
- **Sending / sharing:** "Send to the library" opens a GitHub issue that a workflow (`.github/workflows/timing.yml` → `tools/audio/apply_owner_timing.py`) merges into the published timings; helpers "Save as a file", the owner "Open file"s it (times shown as "from <name>", to check). "Clear adjustments" removes only this work and recording's marks on this phone. Timing mode is off by default, turns itself off after 12 hours, and never travels in a saved personal file.

## Where the code is

`tools/site/app.js` (the app; `python3 tools/site/build.py` copies it to `app/`):

| Function (line, 2026-10-20) | Role |
|---|---|
| `buildAudio` (~576) | merges the published times with the reader's own (`S.timing.fix[work:source]` = `{item id: [track, start, end]}`), applies the order rule, sets `AUT[track] = [[item index, start, end], …]`, `moved`, `checkSet` |
| `markBar` (~562), `nud`/`step` (~571) | the per-verse row: − Starts now +, − Ends now +, and the info line |
| the click handler (~490: `tstart`, `tend`, `tn`, `tok`) | taps on that row |
| `itemMenu` (~513) | the ⋮ menu's Audio timing box (± start/end, Until next, step chooser, Play this verse, Undo) |
| `setTime` (~765), `setStart`, `clearStart` | writing a start or end, the neighbour linking, the late-estimate rule, refusals, re-rendering, moving the light |
| `nowAt` (~763) | the moment of a tap (last player report + elapsed − 0.3 s reaction) |
| `tick` (~708), `curAt` (~706), `endOf` (~705) | every 300 ms: which verse is lit (incl. "the light waits"), stopping at the end of what was asked |
| `setCur` (~743), `keepInView` (~737) | lighting a verse and scrolling (the timing-mode no-scroll rule) |
| `snippet` (~665) | the 2-second preview after − / + (own 50 ms poll; pauses at the target) |
| `playFrom` (~678), `stepVerse` (~760), `onEnded` (~698) | playing a verse / stretch, ⏮ ⏭ |
| `seekGuard`, `playTime` (~691) | after a seek, YouTube reports its old time for a moment; the asked-for time is used until a report arrives near it (max 4 s) |
| `timingHTML`, `bindTiming` (~1018) | Settings › Audio timing: switch, recording choice, send, save/open file, clear |

`tools/audio/make_timings.py` — builds `library/<work>/audio/<source>.json` from transcripts, `fixes.json` (hand-checked) and `owner.json` (the owner's sent times); **its order rule must match `buildAudio` exactly**. `tools/audio/apply_owner_timing.py` — validates an issue's times and merges them into `owner.json` (only for issues opened by the repository owner).

Tests: `tools/site/ux_test.py` (search it for `timing`) drives the real app in Chromium at phone size. YouTube cannot be reached from the build machine, so playback is simulated by setting `ytInfo.t`, `PL.on`, etc.; say clearly which findings could only be reasoned about, not run.

## Bugs found so far (to see the pattern)

1. "Ends now" refused ("The end must come after the start") on a verse whose estimated start was later than the real one.
2. A mark reset the auto-scroll pause, so the page jumped after every tap.
3. ▶ on a verse briefly lit the previous verse (YouTube's stale time right after a seek).
4. Increasing an end did nothing: it was silently cut back to the next verse's start.
5. Earlier: the light jumping ahead onto guessed starts; times not travelling correctly between helper files and the owner; timing mode found left on for another user; refresh and Back losing the place.

Most came from **interactions**: estimated vs set times, the light-waiting rule vs the order rule, seeks vs the player's reported time, and re-rendering vs scrolling.

## What to check, at least

- **The order rule, app vs generator:** build the same inputs both ways (a work's published JSON + an `owner.json`/`fix` set) and compare every start, end and "moved" flag. Include ends, neighbours set by you, estimates in between, the first and last verse of a track, two recordings (tracks).
- **Every path that writes a time** (`tstart`, `tend`, `tn`, the ⋮ box's ± / Until next / Undo, Open file, Clear, apply from an issue): with estimated neighbours, set neighbours, ends present or absent, at a track boundary, when the player is paused, when no audio is loaded, when the verse is not on screen.
- **The light** (`tick` in timing mode) after each kind of write, while playing and paused, and after a seek, ⏮ / ⏭ and a preview.
- **Rounding:** times are stored to 0.1 s; steps are 0.1–1 s; comparisons use small epsilons. Look for off-by-rounding refusals or drift.
- **The preview** (`snippet`): stopping late or early, a preview interrupted by another tap / ▶ / ⏮ ⏭ / closing the player; a preview of a verse in another track (recording).
- **Persistence:** what is saved in `S.timing` and the personal file; that timing marks and "on" never leak into another work, recording or person.
- **The send path:** `apply_owner_timing.py` validation against what the app can produce (e.g. linked neighbours, cleared ends, verses no longer in the text).

## Rules for the session

- Read `CLAUDE.md` first: before every commit run `python3 tools/site/build.py && python3 tools/site/smoke_test.py && python3 tools/site/ux_test.py`; `git pull` before pushing; changes to shared code go on a branch `work/<name>` with a pull request, merged by you once the tests pass.
- Add a UX test for every bug you fix, named for the behaviour.
- Record what you learn in `docs/PLAYBOOK.md` → "Audio timing by ear", in the same commit.
- No `pkill -f`; GitHub GraphQL is unavailable (use `gh api` REST).
