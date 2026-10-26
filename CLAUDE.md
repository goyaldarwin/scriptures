# Scriptures library — notes for Claude sessions

Live site: https://scriptures.craadle.org/ (published from `main`). Owner: Darwin Goyal (`goyaldarwin`).

**Read first:** `docs/START-HERE.md` (the documents, the repositories, the status of each work), `docs/PLAYBOOK.md` (every rule and preference), `docs/HOW-TO.md` (procedures), `docs/LIBRARY.md` (data format).

Non-negotiables:
- Accuracy above all, then unambiguity, clarity, consistency, structure. Never write a scripture text from memory; texts come from the owner's sources (or web sources the owner allows), with every choice in the work's `reconciliation.md`.
- Never route around a blocked site or a copyright limit. `goyaldarwin/scriptures-data` is private, always; never copy its raw files here.
- Before every commit: `python3 tools/site/build.py && python3 tools/site/regen_check.py && python3 tools/site/history_check.py && python3 tools/site/smoke_test.py && python3 tools/site/ux_test.py`. Diff regenerated data before committing it.
- `git pull` before pushing: the `timing` workflow pushes to `main` when the owner sends audio times from the app.
- Files state the current state only: no dates, change logs, "was / used to / superseded" notes or stories. Git is the history. A new owner preference or lesson changes the rule in `docs/PLAYBOOK.md` in the same commit as the change.
- No `pkill -f` (it kills the session's own shell); GitHub GraphQL is unavailable — use `gh api` (REST).
- Reply to the owner in plain words: what changed, what to check, one next step.
