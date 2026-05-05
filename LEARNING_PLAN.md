# Claude Code Learning Plan

Hands-on exploration of Claude Code features using a minimal FastAPI app as the sandbox.

## Foundation

- [x] **`/init` command** — generate a project `CLAUDE.md`
- [x] **CLAUDE.md scopes**
  - [x] Project: `CLAUDE.md` (committed, team-shared)
  - [x] Local: `CLAUDE.local.md` (personal, gitignored) — consciously skipped: single-user learning repo, so personal prefs went into the committed `CLAUDE.md` instead
  - [x] Machine: `~/.claude/CLAUDE.md` (global)

## Customization

- [x] **Custom slash commands** — `.claude/commands/*.md` with `$ARGUMENTS` (built `/claude-overview`)
- [x] **Skills**
  - [x] Project-level skill (committed)
  - [x] Personal skill (in `~/.claude/skills/`)
  - [x] Build a concrete skill: **install a Python library** — takes a package name, asks regular vs dev, runs `uv add`/`uv add --dev`, reports what changed
  - [x] Build a concrete skill: **update branch with main** — likely `git merge origin/main` (to discuss)
- [x] **Hooks** — automated behaviors via `settings.json`
  - [x] Example: auto-format on save / pre-commit lint

## Extension

- [x] **MCP** — connect an external MCP server (e.g. context7, GitHub MCP)
- [x] **Build a custom MCP server** — write a stdio MCP server exposing domain-specific tools (e.g. `run_tests`); register it in `.mcp.json` and use it from a subagent
- [x] **Agents** — try `Explore`, `Plan`, custom subagents
- [x] **Workflows** — multi-step or scheduled tasks (`/loop`, `/schedule`)
- [x] **Playwright** — browser automation (to discuss: Playwright MCP server vs. Python lib for tests)

## Bonus

- [x] **Superpowers** — Anthropic's plugin/skill ecosystem

## GitHub integration

- [x] Conventional commit messages
- [x] PR descriptions via skill
- [x] Branch naming conventions
- [ ] CI checks on PRs
