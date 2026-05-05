#!/usr/bin/env bash
# Hook helper: when Taskfile.yml is edited, warn if any task is undocumented
# in README.md or CLAUDE.md. Reads the PostToolUse hook stdin payload to
# decide whether to run.
#
# Exit codes:
#   0 - either not a Taskfile.yml edit, or no drift found
#   2 - drift found (Claude Code will surface stderr to the model as feedback)

set -euo pipefail

file_path=$(jq -r '.tool_input.file_path // ""')
[[ "${file_path}" == */Taskfile.yml ]] || exit 0

# Extract top-level task names: lines like "  taskname:" with exactly 2-space
# indent. Inner keys (desc:, cmds:, ...) live at 4-space indent and don't match.
tasks=$(grep -E '^  [a-z][a-z0-9_-]*:' Taskfile.yml | sed -E 's/^  ([a-z0-9_-]+):.*/\1/' | sort -u)

# For each task, check both docs. Word-boundary regex: task name must be
# followed by a non-word, non-dash char (or end of line) so `task add` doesn't
# falsely match `task add-dev`.
missing=()
for t in ${tasks}; do
  for doc in README.md CLAUDE.md; do
    if [[ -f "${doc}" ]] && ! grep -qE "task ${t}([^a-zA-Z0-9_-]|\$)" "${doc}"; then
      missing+=("- \`task ${t}\` not mentioned in ${doc}")
    fi
  done
done

if [[ ${#missing[@]} -eq 0 ]]; then
  echo '{"systemMessage":"✓ Taskfile docs in sync with README.md and CLAUDE.md"}'
  exit 0
fi

{
  echo "Documentation drift detected after Taskfile.yml change:"
  printf '%s\n' "${missing[@]}"
  echo ""
  echo "Each task should appear in both README.md (outside readers) and CLAUDE.md (contributors)."
} >&2
echo '{"systemMessage":"❌ Taskfile docs drift detected — see Claude'\''s next response"}'
exit 2
