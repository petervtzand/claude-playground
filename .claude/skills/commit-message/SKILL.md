---
name: commit-message
description: Use when Peter wants to commit (and push) files he has already staged in VSCode. Inspects the staged diff, drafts a commit message, asks Peter to approve, then runs git commit and git push. Examples - "draft a commit message", "commit the staged changes", "what should I commit this as", "give me a commit message", "commit and push".
---

# commit-message

Peter stages files himself in VSCode. This skill drafts a commit message from the staged diff, **asks him to approve it**, then commits and pushes on his go-ahead.

## Procedure

1. **Inspect what is staged.** Run in parallel:
   - `git status` — to see which files are staged vs unstaged and the current branch.
   - `git diff --cached` — to see the actual content of the staged changes.
   - `git log -5 --oneline` — to glance at recent commit style in this repo.

2. **Sanity-check.**
   - If nothing is staged, say so and stop.
   - If staged and unstaged changes overlap meaningfully, mention it once so Peter knows the message only covers what's staged.

3. **Draft the message in this format:**
   - **One short sentence** describing what the commit does (imperative mood: "add X", "fix Y").
   - **Conventional Commits prefix required.** The summary line must start with one of: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `style:`, `perf:`, `build:`, `ci:`. Pick the type that best fits the commit's primary purpose. Optional scope in parens, e.g. `feat(skills): ...`. Lowercase the verb after the prefix.
   - **A blank line.**
   - **Short, high-level bullets** — one per logically distinct change. Skip the bullets entirely for a single-change commit.

4. **Output the message inside a fenced code block** so Peter can copy it if he prefers, then ask explicitly:
   > **Happy with this message? Reply `yes` to commit and push, or tell me what to change.**

5. **Wait for Peter's response.** Do not commit until he approves.
   - If he says yes (or equivalent): proceed to step 6.
   - If he edits the message or asks for changes: redraft, re-output, ask again.
   - If he says no / cancels: stop.

6. **Commit and push.** On approval:
   - `git commit` using a HEREDOC for the message:
     ```
     git commit -m "$(cat <<'EOF'
     <summary line>

     - <bullet>
     - <bullet>
     EOF
     )"
     ```
   - Then `git push`.
   - **Never** use `--amend`, `--no-verify`, `--no-gpg-sign`, or `--force`.
   - **Never** `git add` on Peter's behalf — he stages himself.
   - If a pre-commit hook fails, surface the error verbatim and ask how to proceed (likely fix the underlying issue, then re-stage and re-commit as a *new* commit). Don't bypass hooks.

7. **Confirm.** After push, run `git status` once and report: branch, that the commit landed, and that the push succeeded.

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

- If Peter dictates the exact message verbatim, use his text as-is — still ask for approval before committing.
- If a project's `CLAUDE.md` mandates a *different* format (e.g. omitting the prefix, or a custom prefix scheme), follow the project rule over this default.

## Safety

- Pushing to `main`/`master`: do it (per Peter's request via this skill), but if the push would be a force-push for any reason, **stop and confirm first**.
- If the current branch has no upstream set, use `git push -u origin <branch>` and mention that you set the upstream.
