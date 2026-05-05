# CLAUDE_OVERVIEW.md

Auto-generated reference of every Claude Code primitive in this project. Regenerate with `/claude-overview`.

## CLAUDE.md scopes

### What & when
Markdown files loaded into Claude's context every session — pick the scope based on whether the rule belongs to the team, just-this-machine, or just-this-project-for-me.

### Currently set up
- CLAUDE.md (team-shared codebase facts, committed)
  - Purpose
  - Commands
  - Architecture
  - Working mode
- CLAUDE.local.md (personal notes for this repo, gitignored)
  - Progress tracking
- ~/.claude/CLAUDE.md (cross-project preferences, machine-global)
  - Single source of commands
  - Code documentation

## Skills

### What & when
Markdown files with frontmatter that auto-trigger when a user prompt matches the description; the skill body becomes Claude's instructions for that turn.

### Currently set up
- install-python-library (project; when adding/removing Python deps via task)
- update-branch-with-main (project; when bringing origin/main into a feature branch)
- commit-message (user-global; when drafting a commit from staged files)
- context7-mcp (user-global; when asking about libraries/frameworks for current docs)

## Slash commands

### What & when
Markdown files in `.claude/commands/` invoked literally by typing `/<name>`; deterministic, user-driven workflows.

### Currently set up
- /claude-overview (regenerate this file)

## Subagents

### What & when
Specialized Claude instances spawned via the Agent tool, each with its own system prompt and restricted toolset; use when isolation, focus, or limited tools matter.

### Currently set up
- endpoint-tester (project; when adding pytest tests for a FastAPI endpoint in main.py)

## MCP servers

### What & when
External servers exposing typed tools, resources, and prompts over stdio or HTTP; give Claude structured access to systems beyond the local filesystem.

### Currently set up
- github (project, stdio via wrapper script; for GitHub API operations like issues, PRs, commits)
- playwright (project, stdio via npx; for browser automation — navigate, screenshot, interact with rendered pages)
- context7 (user-global, HTTP; for fetching current library/framework docs)

## Hooks

### What & when
Shell commands the harness runs at lifecycle events (PreToolUse, PostToolUse, Stop, etc.); deterministic enforcement that fires regardless of model attention.

### Currently set up
- PreToolUse Bash pip-block (project; blocks pip-prefixed commands so uv stays the only dep manager)
- PostToolUse Edit|Write|MultiEdit task check (project; runs format/lint/typecheck on every .py edit)
- PostToolUse Edit|Write|MultiEdit doc-drift (project; warns if Taskfile.yml tasks aren't documented in README/CLAUDE.md)

## Settings (`settings.json`)

### What & when
JSON config for hooks, permissions, env vars, MCP enable/disable, plugins, theme; project file is committed for the team, local file is gitignored for personal allowlists.

### Currently set up
- .claude/settings.json (committed; defines the three hooks)
- .claude/settings.local.json (gitignored; personal Bash/Skill/MCP-tool permission allowlist)
- ~/.claude/settings.json (user-global; currently empty `{}`)

## Workflows (`/loop`, `/schedule`)

### What & when
Built-in commands for repeating a task on an interval (`/loop`) or scheduling a remote agent on cron (`/schedule`).

### Currently set up
- None

## Plugins (Superpowers)

### What & when
Anthropic's plugin/skill ecosystem distributed via marketplaces; bundles skills, hooks, agents, and MCP servers from a remote source.

### Currently set up
- None

## Tooling around the repo (not Claude primitives)

### What & when
Project conventions for build/test/lint/dep management, listed for completeness so this overview stays a one-stop reference.

### Currently set up
- Taskfile.yml (single command runner; `task --list` shows everything)
- uv (dep manager; uv.lock + pyproject.toml)
- ruff (format + lint, config in pyproject.toml)
- pyright (static typecheck, config in pyproject.toml)
- pytest (test runner, config in pyproject.toml; tests live in tests/)
