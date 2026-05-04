---
name: install-python-library
description: Use when the user wants to install, add, or remove a Python package, library, or dependency in this repo. Examples - "install requests", "add httpx as a dep", "we need pytest", "drop pydantic". Distinguishes runtime vs dev deps, runs the right Taskfile target, and reports what changed.
---

# install-python-library

Add or remove a Python dependency in this `uv`-managed FastAPI sandbox.

## Procedure

1. **Resolve the package name.** If the user said something ambiguous ("the http library"), confirm before proceeding.

2. **Decide runtime vs dev.**
   - If the package is clearly tooling (linter, formatter, test runner, type checker — e.g. `pytest`, `mypy`, `ruff`, `pre-commit`, `coverage`), say "looks like a dev tool — adding as dev unless you say otherwise" and proceed with dev.
   - Otherwise ask: *"runtime dep (imported by `main.py`) or dev dep (tooling only)?"*

3. **Run the right Taskfile target** (not `uv add` directly — the project standardises on Task for discoverability; `--` forwards args to `uv`):
   - Runtime: `task add -- <package>`
   - Dev: `task add-dev -- <package>`
   - Removal: `task remove -- <package>`

4. **Report what changed.** In one short message:
   - The version `uv` resolved (read from the command output or `uv.lock`).
   - Which `pyproject.toml` section it landed in (`[project] dependencies` vs `[dependency-groups] dev`).
   - Any notable transitive deps pulled in (only mention if non-trivial — skip for a standard lib install).

## Notes

- Don't run `task check` or the dev server afterwards unless the user asks.
- Don't pin a version unless the user specified one; let `uv` pick the latest compatible.
- If `uv add` fails (e.g. resolution conflict), surface the error verbatim and ask how to proceed — don't silently retry with `--force` flags.
