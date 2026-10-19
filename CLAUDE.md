# Scriptures library — notes for Claude sessions

Live site: https://scriptures.craadle.org/ (published from `main`). Owner: Darwin Goyal (`goyaldarwin`).

**Read first:** `docs/START-HERE.md` (repos, rules, status), `docs/PLAYBOOK.md` (every preference and lesson), `docs/HOW-TO.md` (procedures), `docs/LIBRARY.md` (data format), `docs/APPS.md` (the store apps).

Non-negotiables:
- Accuracy above all, then unambiguity, clarity, consistency, structure. Never write a scripture text from memory; texts come from the owner's sources (or web sources the owner allows), with every choice in the work's `reconciliation.md`.
- Never route around a blocked site or a copyright limit. `goyaldarwin/scriptures-data` is private, always; never copy its raw files here.
- Before every commit: `python3 tools/site/build.py && python3 tools/site/smoke_test.py && python3 tools/site/ux_test.py`. Diff regenerated data before committing it.
- `git pull` before pushing: the `timing` workflow pushes to `main` when the owner sends audio times from the app.
- Record every new owner preference or lesson in `docs/PLAYBOOK.md` in the same commit as the change.
- No `pkill -f` (it kills the session's own shell); GitHub GraphQL is unavailable — use `gh api` (REST).
- Reply to the owner in plain words: what changed, what to check, one next step.
