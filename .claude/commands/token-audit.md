---
description: Audit Claude Code context overhead in this project (CLAUDE.md, skills, agents, MCP servers, plugins, hooks) and recommend optimizations to reduce per-session token cost.
---

Audit the token / context overhead of Claude Code primitives in the current project. The goal is to identify what's expensive at session start and what can be trimmed without losing utility.

**Before producing recommendations**, Read `.claude/docs/token-efficiency.md` — it contains the best-practice patterns and the recommendation format to apply. Do not freelance optimization advice; follow the patterns there.

## What to inspect

Run shell commands to gather sizes from each source. Use `wc -c` for files; for skills/agents extract just the `description:` frontmatter (that's what gets sent on every turn — the body only loads on trigger).

1. **CLAUDE.md files (loaded every session, full content):**
   - `CLAUDE.md`, `CLAUDE.local.md` (if present), `~/.claude/CLAUDE.md`

2. **Project skill descriptions:**
   - For each `.claude/skills/*/SKILL.md`: extract the `description:` line and count chars

3. **User-global skill descriptions:**
   - Same for `~/.claude/skills/*/SKILL.md`

4. **Project subagent descriptions:**
   - For each `.claude/agents/*.md`: extract the `description:` line and count chars

5. **MCP servers configured:**
   - List servers from `.mcp.json` (project) and `~/.claude.json` `mcpServers` (user-global)
   - **Note the multiplier:** each MCP server publishes its tools with full JSON schemas at session start. Typical sizes: `github` ~30 tools, `playwright` ~20, `context7` ~2, custom servers vary. Each tool schema is ~100-300 chars. So a single connected `github` MCP server alone adds ~3-9K chars of context.

6. **Plugins enabled:**
   - `jq -r '.enabledPlugins // {} | keys[]' .claude/settings.json` and same for user-global

7. **Hooks defined:**
   - Count and rough-size from `.claude/settings.json` `hooks` field

## Output format

Produce a structured report under 500 words:

### 1. Survey table
| Source | Chars | Approx tokens |
|---|---|---|
| CLAUDE.md (project) | ... | ... |
| ... | | |
| **Total measurable** | ... | ... |

(Token estimate: chars / 4 for English text, chars / 3 for JSON-heavy content)

### 2. Top 3 contributors
Which sources dominate. Almost always: MCP tool schemas first, CLAUDE.md second, skill descriptions third — but verify against actual numbers.

### 3. Recommendations
Concrete and actionable. Examples:
- *"Disable `playwright` MCP server in this project — there's no UI to drive here. Edit `.mcp.json` to remove it."*
- *"Set `skillOverrides: { 'install-python-library': 'name-only' }` — saves ~280 chars per session."*
- *"Trim CLAUDE.md from 3.5KB to ~1.5KB by removing the long Working-mode section that's stale."*
- *"Set `skillListingMaxDescChars: 80` to cap descriptions globally."*

For each recommendation, include the **expected savings** (chars or %) and the **exact edit** to apply.

### 4. Suggested settings.json diff
A copy-pasteable JSON snippet the user can apply if they want.

## Rules

- **Be specific, not generic.** "Review your CLAUDE.md" is useless. "Your CLAUDE.md is 3510 chars; the longest section is `## Working mode` at 1247 chars — consider trimming." is actionable.
- **Don't apply any changes.** Just report and suggest. The user decides.
- **Surface unexpected wins.** If something's surprisingly large, call it out — they may not realize.
- **Note caching context.** Mention that within a single session, prompt caching makes the overhead cheap on turns 2+; the cost mainly hits on session start (after 5-min cache TTL).
