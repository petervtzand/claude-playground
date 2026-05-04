---
name: update-branch-with-main
description: Use when Peter wants to bring the latest main into his current feature branch. Fetches and merges origin/main, refuses to run if dirty or already on main, surfaces conflicts without resolving them. Examples - "update this branch with main", "merge main in", "pull main into this branch", "sync with main", "bring main into my branch".
---

# update-branch-with-main

Bring the latest `origin/main` into the current feature branch via merge. Strict and predictable: refuses on dirty trees, refuses on `main`, never auto-stashes, never auto-resolves conflicts, never pushes.

## Procedure

1. **Pre-flight checks.** Run in parallel:
   - `git branch --show-current` — current branch name.
   - `git status --porcelain` — dirty-tree check (must be empty).

2. **Refuse-to-run guards.**
   - If current branch is `main` (or `master`): stop. Tell Peter the skill is for feature branches; he can `git pull` directly if he wants to update main itself.
   - If `git status --porcelain` is non-empty: stop. List the dirty files briefly and tell Peter to commit or stash first. Do **not** auto-stash.

3. **Fetch the latest main.**
   - `git fetch origin main`
   - If fetch fails (no network, no remote, etc.): surface the error and stop.

4. **Merge `origin/main` into the current branch.**
   - `git merge origin/main`
   - The merge will either fast-forward, create a merge commit, or hit a conflict.

5. **Report the outcome.**
   - **Fast-forward:** say so, show the new HEAD (`git log -1 --oneline`).
   - **Merge commit created:** say so, show the merge commit (`git log -1 --oneline`), and note how many commits from main were brought in (`git log --oneline ORIG_HEAD..HEAD` count).
   - **Conflict:** list the conflicting files (from `git status --short` — lines starting with `UU`, `AA`, etc.). Leave the merge **in progress** — do not run `git merge --abort`, do not edit files to resolve. Tell Peter to resolve in VSCode, then either:
     - commit the resolution himself (or via the `commit-message` skill), or
     - run `git merge --abort` to bail out.

6. **No push.** Whether the merge succeeded or not, do not push. Peter pushes manually when he's ready.

## Rules

- **Never** `git stash` on Peter's behalf.
- **Never** rebase — this skill is merge-only by design.
- **Never** force-push or push at all.
- **Never** auto-resolve conflicts (no `-X ours`/`-X theirs`, no editing conflicted files).
- **Never** `git merge --abort` on Peter's behalf — leave the choice to him.
- If `origin/main` doesn't exist (e.g. the default branch is `master`): stop, surface the error, and ask Peter which branch to merge from. Do **not** silently fall back.

## Output template

On success (fast-forward):
> Updated `<branch>` with `origin/main` (fast-forward). HEAD is now `<short-sha> <subject>`.

On success (merge commit):
> Merged `origin/main` into `<branch>`. Brought in N commits, created merge commit `<short-sha>`.

On conflict:
> Merge in progress with conflicts in:
> - `<file1>`
> - `<file2>`
>
> Resolve in VSCode, then commit (or run `git merge --abort` to bail).
