---
name: commit-message
description: Use when Peter wants a draft commit message for files he has already staged in VSCode. Inspects the staged diff, drafts the message, and outputs it for Peter to copy and commit himself. Does NOT commit or push — that's Peter's job. Examples - "draft a commit message", "commit the staged changes", "what should I commit this as", "give me a commit message".
---

# commit-message

Peter stages files himself in VSCode. This skill drafts a commit message from the staged diff and outputs it inside a fenced code block. Peter copies it and runs `git commit` himself — that's faster than the back-and-forth approval flow. **The skill never commits, pushes, or stages.**

## Procedure

1. **Inspect what is staged.** Run in parallel:
   - `git status` — to see which files are staged vs unstaged and the current branch.
   - `git diff --cached` — to see the actual content of the staged changes.
   - `git log -5 --oneline` — to glance at recent commit style in this repo.

2. **Sanity-check.**
   - If nothing is staged, say so and stop.
   - If staged and unstaged changes overlap meaningfully, mention it once so Peter knows the message only covers what's staged.
   - **Check the staged diff for any secrets or keys.** If you spot any, **stop**, point them out, and tell Peter to remove them before drafting. (The pre-commit `gitleaks` hook will block the commit anyway; the skill catches it earlier.)

3. **Draft the message in this format:**
   - **One short sentence** describing what the commit does (imperative mood: "add X", "fix Y").
   - **Conventional Commits prefix required.** The summary line must start with one of: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `style:`, `perf:`, `build:`, `ci:`. Pick the type that best fits the commit's primary purpose. Optional scope in parens, e.g. `feat(skills): ...`. Lowercase the verb after the prefix.
   - **A blank line.**
   - **Short, high-level bullets** — one per logically distinct change. Skip the bullets entirely for a single-change commit.

4. **Output the message inside a fenced code block.** That's it — don't ask for approval, don't commit, don't push. Peter takes it from here.

## Format example

```
feat: add httpx for outbound HTTP calls

- Add httpx 0.28.1 as runtime dep
- Whitelist task add/add-dev/remove in project settings
```

## Rules for the bullets

- **Stay high-level.** Describe *what* changed, not *how*. A reader scanning `git log --oneline` should get the gist from the summary; the bullets exist for someone who clicks in.
- **One bullet per concern.** Split combined bullets ("update X and refactor Y"); collapse repetitive ones.
- **Don't list file paths.** Git already shows those. Bullets describe behaviour or intent.
- **Skip the `Co-Authored-By` block** unless Peter explicitly asks for it.

## When NOT to apply

- If Peter dictates the exact message verbatim, use his text as-is.
- If a project's `CLAUDE.md` mandates a *different* format (e.g. omitting the prefix, or a custom prefix scheme), follow the project rule over this default.

## What you must NEVER do

- **Never** `git commit`, `git push`, or `git add` on Peter's behalf — he handles those.
- **Never** ask "happy with this? reply yes" — just output the draft and stop.
