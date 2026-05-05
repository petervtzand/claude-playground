---
name: pr-description
description: Use when Peter wants to draft and open a pull request from his current branch. Inspects the branch's commits and diff against main, drafts a structured PR title and body, asks Peter to approve, then creates the PR via the GitHub MCP. Examples - "create a PR", "open a pull request", "draft a PR description", "make a PR for these changes".
---

# pr-description

Peter has been working on a feature branch and wants to open a PR. This skill drafts the title and body from the branch's commits + diff, asks for approval, then creates the PR via `mcp__github__create_pull_request`. Mirrors the shape of the `commit-message` skill at PR scope.

## Procedure

1. **Inspect the branch.** Run in parallel:
   - `git rev-parse --abbrev-ref HEAD` — current branch name.
   - `git log main..HEAD --oneline` — commits on this branch since main.
   - `git diff main..HEAD --stat` — files changed and line counts.
   - `git status` — confirm working tree is clean (no unstaged changes that wouldn't be in the PR).
   - `git remote get-url origin` — derive `owner/repo` for the API call.
   - Check for a template: `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE.md`. If present, mirror its sections.

2. **Sanity-check.**
   - If current branch is `main` or `master`: stop. PRs are for feature branches; tell Peter to create one first.
   - If `git log main..HEAD` is empty: stop. Nothing to PR.
   - If working tree is dirty: surface the uncommitted files once and ask whether to proceed (those changes won't be in the PR).

3. **Ensure the branch is on the remote.**
   - `git rev-parse --abbrev-ref --symbolic-full-name @{u}` to check upstream. If unset, `git push -u origin <branch>` to publish. If already published but ahead of remote, `git push`.
   - If push would be a force-push for any reason: stop and confirm with Peter first.

4. **Draft the PR.**
   - **Title:** start with the dominant Conventional Commits prefix from the branch's commits (if 3 of 4 are `feat:`, title is `feat: ...`). One short imperative sentence summarizing the branch's overall purpose.
   - **Body:** unless a template was found, default to two sections:
     ```md
     ## Summary
     - <1-3 bullets describing what the PR does, in user-facing terms>

     ## Test plan
     - [ ] <thing to verify>
     - [ ] <another thing>
     ```
     If a template was found, fill its sections faithfully (don't drop required sections; do add a `## Summary` if the template lacks one).
   - **Skip the `🤖 Generated with...` attribution trailer** unless Peter explicitly asks for it.

5. **Output title and body inside fenced code blocks** so Peter can copy if he prefers, then ask:
   > **Happy with this PR? Reply `yes` to create it, or tell me what to change.**

6. **Wait for Peter's response.**
   - Yes (or equivalent) → step 7.
   - Edits requested → redraft, re-show, re-ask.
   - No / cancel → stop.

7. **Create the PR.** Call `mcp__github__create_pull_request` with:
   - `owner` and `repo` parsed from `git remote get-url origin`
   - `title` — the approved title
   - `body` — the approved body (markdown)
   - `head` — current branch name
   - `base` — `main` by default; if `git symbolic-ref refs/remotes/origin/HEAD` shows a different default, use that
   - `draft: false` unless Peter requested a draft PR

   If the GitHub MCP isn't available in the session, fall back to `gh pr create --title "..." --body "..."`.

8. **Confirm.** Report:
   - PR number and URL (from the API response)
   - Branch → base
   - Whether to switch back to main now (offer; don't do it unprompted)

## Format example

```
feat: add /landing demo and Playwright MCP, plus repo cleanup

## Summary
- Add /landing HTML endpoint with modern-minimalist styling and SVG favicon
- Wire up Playwright MCP server for browser navigation/screenshots in-session
- Tick off Workflows and Playwright in learning plan; minor cleanup

## Test plan
- [ ] Run `task test` — all 6 endpoint tests pass
- [ ] Visit http://127.0.0.1:8000/landing — page renders with the new styling
- [ ] Confirm `task check` is green
```

## Rules for the body

- **Stay user-facing.** Describe what the PR *does* and how to verify, not how the code changed line-by-line. The diff is on the PR page; don't recapitulate it.
- **One bullet per concern in the Summary.** Same discipline as commit-message bullets: don't combine ("update X and refactor Y" → split).
- **Test plan items must be runnable** — concrete commands or steps, not vague intentions ("test it works").
- **Don't list file paths** in Summary. The PR's "Files changed" tab covers that.

## When NOT to apply

- If Peter dictates the exact title/body verbatim, use his text as-is — still ask for approval before creating.
- If the project's `CLAUDE.md` mandates a different PR format, follow the project rule.

## Safety

- Never use `--force` / `--force-with-lease` on push, ever.
- Never run `gh pr merge` or set the PR to auto-merge from this skill.
- Never close or comment on existing PRs from this skill — it only *creates*.
