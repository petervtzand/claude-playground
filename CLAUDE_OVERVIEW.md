# CLAUDE_OVERVIEW.md

Auto-generated quick reference of Claude Code primitives in this sandbox. Regenerate with `/claude-overview`.

## CLAUDE.md scopes

### What & when
Markdown files auto-injected into every Claude session as durable instructions.

### Currently set up
- CLAUDE.md (team-shared codebase facts, committed)
  - Purpose
  - Commands
  - Architecture
  - Working mode
- CLAUDE.local.md (personal notes for this repo, gitignored)
  - Progress tracking
- ~/.claude/CLAUDE.md (cross-project preferences)
  - Single source of commands
  - Code documentation

## Skills

### What & when
Reusable procedures Claude invokes by description, not by name.

### Currently set up
- ~/.claude/skills/context7-mcp (fetch live library docs)
- ~/.claude/skills/pr-description (write PR descriptions)
- Built-ins: init, review, security-review, update-config, simplify, loop, schedule
- No project-level skills yet

## Slash commands

### What & when
Markdown templates in `.claude/commands/` triggered explicitly with `/<name>`.

### Currently set up
- /claude-overview (regenerate this file)

## Subagents

### What & when
Sub-Claudes spawned via the Agent tool with their own context window.

### Currently set up
- Built-ins: Explore, general-purpose, Plan, claude-code-guide, statusline-setup
- No custom subagents

## MCP servers

### What & when
External tool servers Claude talks to over the Model Context Protocol.

### Currently set up
- context7 (live library docs, global)
- Gmail / Google Calendar / Google Drive (global)
- No project-level `.mcp.json`

## Hooks

### What & when
Shell commands the harness runs automatically on lifecycle events.

### Currently set up
- None

## Settings (`settings.json`)

### What & when
JSON config for permissions, hooks, env vars, MCP toggles.

### Currently set up
- .claude/settings.local.json (allowlists `task progress`, `ls`, and reads under `~/.claude/`)
- No project-level `settings.json`

## Workflows (`/loop`, `/schedule`)

### What & when
Built-in commands for recurring (`/loop`) or cron-scheduled (`/schedule`) work.

### Currently set up
- None active

## Plugins (Superpowers)

### What & when
Anthropic's plugin marketplace — bundled skills/commands/hooks.

### Currently set up
- Not installed

## Tooling around the repo

*Not Claude primitives — listed for completeness.*

- Taskfile.yml (single command runner; `task --list` shows everything)
- pyproject.toml (deps + ruff/pyright config)
- uv (package manager, wrapped by `task add` etc.)
- ruff (formatter + linter, in `task check`)
- pyright (type checker, in `task check`)
