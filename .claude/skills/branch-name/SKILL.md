---
name: branch-name
description: Use when Peter wants help naming and creating a new feature branch. Asks what the branch is for if needed, suggests a kebab-case name with a Conventional Commits-style type prefix (feat/fix/etc.), confirms with him, then runs `git checkout -b`. Examples - "give me a good branch name, I want to fix the user tests", "I need a new branch for adding a /search endpoint", "branch name for the docs cleanup".
---

# branch-name

Helps Peter pick a clean branch name for a new piece of work and (on his approval) creates it. Mirrors the shape of `commit-message` and `pr-description`: inspect → suggest → approve → execute → confirm.

## Format

`<type>-<short-description>` — all lowercase, kebab-case, no slashes, no underscores.

- **Type prefix** is one of: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `build`, `ci` (same set as Conventional Commits).
- **Description** is 2-5 words, slugified (lowercase, spaces → `-`, strip non-alphanumeric except `-`).
- **Total length** under ~40 chars.

Examples:

- "fix the user tests" → `fix-user-tests`
- "add a /search endpoint" → `feat-add-search`
- "clean up the README" → `docs-readme-cleanup`

## Procedure

1. **Get the description.** If Peter's prompt doesn't already include what the branch is for, ask once: *"What's the branch for?"*

2. **Inspect state.** Run in parallel:
   - `git rev-parse --abbrev-ref HEAD` — current branch.
   - `git status --porcelain` — dirty-tree check.

3. **Sanity-check.**
   - If working tree is dirty (per `git status --porcelain`): stop. Tell Peter to commit or stash first — branching from main requires switching to main, which a dirty tree blocks. Don't try to auto-stash.
   - **Branching from main is the strong default.** If currently *not* on main, warn Peter explicitly: *"You're on `<current-branch>`. Branching from latest main — I'll switch and pull first. Reply `yes` to continue, or `from current` if you want to branch from this branch instead."* Wait for his answer before proceeding.

4. **Generate the name.**
   - Pick the type prefix from the description: "fix" / "broken" / "bug" → `fix`; "add" / "new" / "build" → `feat`; "update docs" / "readme" → `docs`; "clean up" / "rename" → `chore`; "refactor" → `refactor`; "tests" → `test`; etc.
   - Slugify the rest: lowercase, replace whitespace and punctuation with `-`, collapse repeats, strip leading/trailing `-`.
   - Cap total length around 40 chars.
   - **Verify uniqueness:** `git rev-parse --verify <name> 2>/dev/null` should fail (branch must not exist). If it does exist, suggest a variant (`-v2`, or a different short description).

5. **Suggest and ask.**

   > **Create branch `<name>`? Reply `yes`, suggest a different name, or say "no" to skip creation.**

6. **Wait for Peter's response.**
   - Yes (or equivalent) → step 7.
   - Different name → re-validate it (must follow the format above), re-confirm, then create.
   - No / skip creation → stop. The suggested name was just for reference.

7. **Create the branch from latest main.**
   - Default flow: `git fetch origin main && git checkout main && git pull --ff-only && git checkout -b <name>`. This always pulls the latest main first, even if Peter was already on main — branching from a stale main defeats the purpose.
   - If `pull --ff-only` would not be a fast-forward (main has diverged locally): stop and surface the issue rather than forcing.
   - **Override:** if in step 3 Peter said `from current`, branch from current location instead — just `git checkout -b <name>` (no fetch/pull).
   - **Never** force-overwrite an existing branch.

8. **Confirm.** Report:
   - New branch name
   - What it was branched from (main + short SHA, or current branch + short SHA)
   - That Peter is now on the new branch

## Constraints

- **Never** delete branches.
- **Never** push the new branch on creation — Peter pushes when he's ready.
- **Never** pick a type that doesn't fit the description; if unclear after one attempt, ask.
- **Never** use slashes (`feat/foo`) or underscores (`feat_foo`) in the name — kebab-case dashes only.

## When NOT to apply

- If Peter dictates the exact branch name verbatim, use his text as-is — still validate format and ask for approval before creating.
- If a project's `CLAUDE.md` mandates a different branch naming scheme, follow the project rule.
