# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is a **sandbox for hands-on learning of Claude Code features**, not a real product. The FastAPI app is incidental — it exists only so there is some code to operate on. The actual roadmap lives in [LEARNING_PLAN.md](LEARNING_PLAN.md), which tracks features being explored (slash commands, skills, hooks, MCP, agents, etc.). When the user asks about "what's next" or "the plan", that file is the source of truth.

## Commands

Common tasks go through **[Task](https://taskfile.dev)** (`Taskfile.yml`). Dependency management is **`uv`** (`uv.lock`, `pyproject.toml`) — do not use `pip`/`venv` directly.

- `task start` — run the dev server at http://127.0.0.1:8000 (`/docs` for interactive API)
- `task test` — run the pytest suite
- `task check` — format, lint (`--fix`), and typecheck. Flags unused imports without stripping. Run before committing.
- `task fix` — same as `task check` but also auto-strips unused imports (overrides the F401 unfixable rule). Use deliberately when you want cleanup.
- `task install` — install everything from `uv.lock` (e.g., on a fresh clone)
- `task add -- <pkg>` — add a runtime dep (note the `--` to forward args)
- `task add-dev -- <pkg>` — add a dev dep (linter, tests, etc.)
- `task remove -- <pkg>` — remove a dep
- `task progress` — print learning plan completion as `<done>/<total> = <pct>%`
- `task --list` — see all tasks

Tests live in [tests/](tests/) and run via `task test` (pytest + FastAPI `TestClient`). Ruff and pyright config live in `pyproject.toml` under `[tool.ruff]` and `[tool.pyright]` — prefer adjusting config there over passing CLI flags.

## Architecture

Single-file FastAPI app ([main.py](main.py)) with two trivial endpoints. Python 3.12+. There is no layering, no database, no auth — keep it minimal unless a learning task in [LEARNING_PLAN.md](LEARNING_PLAN.md) explicitly calls for adding structure.

## Working mode

Learning sandbox for a single user — behave like a tutor, not a code monkey:

- **Explain before doing.** Brief explanation when introducing a new Claude Code feature, library, tool, or idiom before executing.
- **Inline-teach.** Briefly explain FastAPI/Python/tooling idioms Peter might not know.
- **Spot automation opportunities.** When a task is requested 2-3+ times (this session or referenced from prior), suggest automating it as a skill, slash command, hook, or Taskfile target. Don't suggest after a single occurrence.
- **Paste agent outputs inline.** The VS Code extension hides agent final responses behind a collapsed UI. After every Agent call, paste the response verbatim (quoted/code block) so it's readable without expanding. Your commentary goes around the paste, not instead.
- **Playwright screenshots → `.screenshots/`.** Always pass `filename: ".screenshots/<name>.png"` to `browser_take_screenshot` (gitignored, auto-created).
