# Claude Code Learning Plan

Hands-on exploration of Claude Code features using a minimal FastAPI app as the sandbox.

## Foundation

- [ ] **`/init` command** — generate a project `CLAUDE.md`
- [ ] **CLAUDE.md scopes**
  - [ ] Project: `CLAUDE.md` (committed, team-shared)
  - [ ] Local: `.claude/CLAUDE.local.md` (personal, gitignored)
  - [ ] Machine: `~/.claude/CLAUDE.md` (global)

## Customization

- [ ] **Custom slash commands** — `.claude/commands/*.md` with `$ARGUMENTS`
- [ ] **Skills**
  - [ ] Project-level skill (committed)
  - [ ] Personal skill (in `~/.claude/skills/`)
- [ ] **Hooks** — automated behaviors via `settings.json`
  - [ ] Example: auto-format on save / pre-commit lint

## Extension

- [ ] **MCP** — connect an external MCP server (e.g. context7, GitHub MCP)
- [ ] **Agents** — try `Explore`, `Plan`, custom subagents
- [ ] **Workflows** — multi-step or scheduled tasks (`/loop`, `/schedule`)

## API-level (different scope from Claude Code)

- [ ] **Tools** — Claude API tool use (function calling)
- [ ] **Images / multimodal** — vision input or generated image workflows
- [ ] **MCP primitives** — resources (data) and prompts (user-triggered templates)

## Bonus

- [ ] **Superpowers** — Anthropic's plugin/skill ecosystem

## GitHub integration

- [ ] Conventional commit messages
- [ ] PR descriptions via skill
- [ ] Branch naming conventions
- [ ] CI checks on PRs
