# The site's build and checks: how long they take

`check.py` runs every check before a commit: the build, then `regen_check`, `history_check`, `smoke_test` and the UX
test in four shards, side by side. Measured on the session machine (2 cores, 8 GB; a first run, so `regen_check` remakes
every work), each step's wall time:

| Step | Time |
|---|---|
| build (`build.py`, with `library.py`) | 60 s |
| `regen_check.py` (every work; a later run: only what changed) | 200–560 s |
| `history_check.py` | 5 s |
| `smoke_test.py` | 80–130 s |
| UX shard 0 (the checks of the whole app, then its share of the works) | 1,176 s |
| UX shards 1–3 (the per-work checks of their share of the works) | 1,065–1,346 s |
| all, side by side | 1,347 s |

The UX shards set the time. Shard 0's checks of the whole app take about 15% as long as all the per-work checks
(`APP_SHARE` in `ux_test.py`), so it takes a share of the works after them; before it did, shards 1–3 took
1,350–1,580 s and the run 1,623 s. In CI (4 cores) the browser step takes about 21 minutes.

Quicker paths, each keeping a commit checked before it is made: `--fast` (the build, `regen_check`, `history_check`: a
data-only change, about 4 minutes; the browser tests run in CI on the pull request), `--works a,b` (the per-work checks
of those works only), `--browser` (the browser tests only).

What is left to gain: the per-work checks wait a fixed time after many steps (`wait_for_timeout`), most of a work's
time; waiting on a condition instead is the next step.
