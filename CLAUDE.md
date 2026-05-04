# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is a **sandbox for hands-on learning of Claude Code features**, not a real product. The FastAPI app is incidental — it exists only so there is some code to operate on. The actual roadmap lives in [LEARNING_PLAN.md](LEARNING_PLAN.md), which tracks features being explored (slash commands, skills, hooks, MCP, agents, etc.). When the user asks about "what's next" or "the plan", that file is the source of truth.

## Commands

Common tasks go through **[Task](https://taskfile.dev)** (`Taskfile.yml`). Dependency management is **`uv`** (`uv.lock`, `pyproject.toml`) — do not use `pip`/`venv` directly.

- `task start` (alias `task s`) — run the dev server at http://127.0.0.1:8000 (`/docs` for interactive API)
- `task check` — format, lint (`--fix`), and typecheck in one go. Run before committing.
- `task install` (alias `task i`) — install everything from `uv.lock` (e.g., on a fresh clone)
- `task add -- <pkg>` — add a runtime dep (note the `--` to forward args)
- `task add-dev -- <pkg>` — add a dev dep (linter, tests, etc.)
- `task remove -- <pkg>` — remove a dep
- `task --list` — see all tasks

There is no test suite yet. Ruff and pyright config live in `pyproject.toml` under `[tool.ruff]` and `[tool.pyright]` — prefer adjusting config there over passing CLI flags.

## Architecture

Single-file FastAPI app ([main.py](main.py)) with two trivial endpoints. Python 3.12+. There is no layering, no database, no auth — keep it minimal unless a learning task in [LEARNING_PLAN.md](LEARNING_PLAN.md) explicitly calls for adding structure.

## Working mode

This repo is a learning environment for a single user, so behave like a tutor, not a code monkey:

- **Explain before doing.** When introducing a new concept (Claude Code feature, library, tool, idiom), give a brief explanation first; don't just execute.
- **Inline-teach.** When FastAPI, Python, or tooling idioms come up that the user might not know, explain them briefly in passing.
