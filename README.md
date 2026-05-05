# claude-playground

A FastAPI sandbox for hands-on learning of Claude Code features.

## Quick start

```bash
task start
```

Then visit http://127.0.0.1:8000 or http://127.0.0.1:8000/docs for the interactive API docs.

## Tasks

All workflows go through [Task](https://taskfile.dev) — run `task --list` to see everything.

- `task start` — run the dev server
- `task test` — run the pytest suite
- `task check` — format, lint (`--fix`), and typecheck
- `task install` — install all deps from `uv.lock`
- `task add -- <pkg>` — add a runtime dep
- `task add-dev -- <pkg>` — add a dev dep
- `task remove -- <pkg>` — remove a dep
- `task progress` — print learning plan completion

## What's this for?

See [LEARNING_PLAN.md](LEARNING_PLAN.md) for the full list of Claude Code features being explored here.
