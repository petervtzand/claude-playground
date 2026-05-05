# Token efficiency best practices for Claude Code primitives

Reference for any tool / command / skill that recommends optimizations to a Claude Code primitive (skill, subagent, slash command, MCP server, hook, plugin, CLAUDE.md). **Loaded on demand**, not in the default session context — that's the point.

## The cost model

Claude Code primitives have layered context cost:

| Layer | When loaded | Cost characteristic |
|---|---|---|
| **Frontmatter `description:`** | Every session, always | Pure overhead. The price you pay for the primitive *existing*. |
| **Body (markdown after frontmatter)** | Only when triggered / invoked | Free until used. Then the full body loads once for that turn. |
| **Sub-files referenced by the body** | Only when the body explicitly tells the model to Read them | Even cheaper than body — body can stay slim, branch into sub-files only when needed. |
| **Helper scripts the body invokes** | Source code never enters context — only stdout does | The biggest win. Move logic out of prose, into code on disk. |

## Optimization patterns (apply in this order)

When recommending changes to a primitive, evaluate each pattern in order. Recommend the highest-impact one that fits.

### 1. Tighten the description (highest leverage — paid every session)

Test: can the description lose words without losing trigger reliability?

- ❌ "Use this skill when the user wants help with creating a new pull request from their current branch by drafting a title and body, asking for approval, and creating the PR via the GitHub MCP" (45 words)
- ✅ "Use to draft and open a PR from the current branch. Drafts title + body, opens via GitHub MCP." (18 words)

Removed: "this skill", "the user wants", "by ... and ... and" — connective fluff. Kept: trigger phrases ("draft", "PR"), action verbs, key tools.

### 2. Move parsable logic to a helper script (biggest body savings)

Test: does the body include steps the model has to *execute mechanically* rather than *judge*? Examples:

- "Parse `Taskfile.yml`, extract task names matching `^  [a-z]+:`, dedupe, sort"
- "Read JSON config, find the field, check it's non-empty"
- "Run command, capture stdout, count lines matching pattern X"

These are scripts pretending to be prose. Move to a real script (`scripts/<name>.sh` or `scripts/<name>.py`). The body becomes:
- ❌ Body: 30-line procedural breakdown
- ✅ Body: "Run `bash scripts/extract-tasks.sh` and use its output."

Source stays on disk; only stdout reaches the model.

### 3. Split the body into sub-files for branchy procedures

Test: does the body have a happy path + one or more rare branches (error handling, edge cases, conflict resolution)?

If yes:
- Keep the happy path in `SKILL.md`
- Move each rare branch to its own file (e.g., `SKILL_conflict.md`, `SKILL_dirty_tree.md`)
- Body says: *"If you hit a merge conflict, Read `./SKILL_conflict.md` and follow it."*

The model only loads sub-files when the rare branch fires. Saves tokens on every happy-path invocation.

### 4. Settings-level levers (no primitive changes needed)

For *user-facing* recommendations:

- `skillOverrides: { '<name>': 'name-only' }` — keeps slash-command invocability, drops description from the model's listing
- `skillOverrides: { '<name>': 'off' }` — fully hides the skill (won't auto-trigger, no slash invocation)
- `skillListingMaxDescChars: <N>` — caps each skill's description in the listing (e.g., 80)
- `skillListingBudgetFraction: <fraction>` — fraction of context window reserved for skill listings
- Per-project MCP server enable/disable — heavy MCPs (`github`, `playwright`) shouldn't load in projects that don't need them

### 5. Reframe as a different primitive

Sometimes the right move is to *change form*:

- Heavy skill that's used rarely → consider making it a **plugin** (zero context cost when not enabled in a project)
- Skill body that's basically a sub-LLM prompt → consider making it a **subagent** (only loads on delegation; isolated context too)
- Skill that auto-fires too aggressively → consider making it a **slash command** (user-invoked only, no description in the model's auto-trigger list)

## Anti-patterns (don't recommend these)

- ❌ Stripping clarity for char count — explicit > terse-and-confusing
- ❌ Removing safety rails ("always confirm before deleting") to save chars
- ❌ Splitting a clean linear procedure into sub-files just because — only split when there's a branch
- ❌ Moving model-judgment logic to scripts — only mechanical / parsable logic goes to scripts
- ❌ Trimming examples — concrete examples in skills are high-value, low-cost (only load on trigger)

## When to recommend vs. apply

**Default: recommend, don't apply.** The user reviews and decides which suggestions to take. Reasons:
- Token-saving changes can have subtle side effects (e.g., a tighter description triggers less reliably)
- The user knows which skills they actually use vs. ones they keep "just in case"
- Settings-level changes have project-wide effects

Apply changes only if the user explicitly asks for it (e.g., "go ahead and apply").

## Output format for recommendations

For each suggestion, include:

1. **What to change** (specific file + section)
2. **Why** (one line tying it back to a pattern above)
3. **Expected savings** (chars or %, with the math)
4. **Exact edit** (copy-pasteable diff or settings snippet)

Bad recommendation: *"Consider tightening your descriptions."*
Good recommendation: *"Tighten `pr-description`'s description from 339 → ~150 chars. Pattern 1 (description trim). Saves ~190 chars per session. Replace with: `Use to draft and open a PR from the current branch. Drafts title + body, opens via GitHub MCP.`"*
