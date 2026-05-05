"""MCP server exposing test-suite tools, resources, prompts, and completions.

Stdio transport. Four capabilities:
- Tool `run_tests`: execute the pytest suite via `task test`.
- Resource `tests://file/{filename}`: read the source of a file under tests/.
- Prompt `debug_failure`: frame an analysis prompt for a failed test run.
- Completion handler: autocomplete for the resource template's `filename` arg.
"""

import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import (
    Completion,
    CompletionArgument,
    CompletionContext,
    PromptReference,
    ResourceTemplateReference,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"

mcp = FastMCP(
    "local-tests",
    instructions=(
        "Three primitives for working with this project's test suite:\n"
        "1. Tool `run_tests` — execute `task test`, returns structured result.\n"
        "2. Resource `tests://file/{filename}` — read a test file's source. "
        "Filename autocompletes from actual files in tests/.\n"
        "3. Prompt `debug_failure(stdout, stderr)` — frame a debug analysis "
        "prompt from a failed pytest run."
    ),
)


@mcp.tool()
def run_tests(pytest_args: str = "") -> dict[str, str | int | bool]:
    """Run the pytest suite via `task test`.

    pytest_args: optional extra args forwarded to pytest (e.g. "-k test_version"
    to run a single test, or "-x" to stop on first failure). Whitespace-split.

    Returns: dict with stdout (str), stderr (str), exit_code (int), passed (bool).
    """
    cmd = ["task", "test"]
    if pytest_args:
        cmd.extend(["--", *pytest_args.split()])

    result = subprocess.run(  # noqa: S603 - command list is fixed; only arg vec varies
        cmd,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        timeout=120,
        check=False,
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
    }


@mcp.resource("tests://file/{filename}")
def read_test_file(filename: str) -> str:
    """Return the source of a single file under `tests/`.

    URI: `tests://file/<filename>` (e.g. `tests://file/test_main.py`).

    Guards against path traversal — `filename` must be a plain filename
    with no slashes or `..`.
    """
    if "/" in filename or "\\" in filename or ".." in filename:
        return (
            f"# Invalid filename (no path separators or traversal allowed): {filename}"
        )

    path = TESTS_DIR / filename
    if not path.is_file():
        return f"# Not found: tests/{filename}"

    return path.read_text()


@mcp.prompt()
def debug_failure(stdout: str, stderr: str) -> str:
    """Frame an analysis prompt for a failed pytest run.

    Pass the pytest stdout and stderr; returns a user-message prompt that asks
    Claude to identify likely causes and propose concrete fixes.
    """
    return f"""A pytest run just failed. Analyze the output below and propose
2-3 likely causes, with a concrete suggested fix for each.

stdout:
```
{stdout}
```

stderr:
```
{stderr}
```

Be specific — refer to actual error messages, file/line locations, and
propose concrete fixes (one-line change ideal). If the failure looks flaky
(intermittent / environment-dependent), say so explicitly."""


@mcp.completion()
async def handle_completion(
    ref: PromptReference | ResourceTemplateReference,
    argument: CompletionArgument,
    context: CompletionContext | None,
) -> Completion | None:
    """Autocomplete for the `tests://file/{filename}` resource's filename arg.

    Returns sorted matching `.py` filenames in tests/. None for everything
    else (the prompt args take arbitrary text — no useful suggestions).
    """
    del context  # unused — we don't depend on prior arg resolutions
    if isinstance(ref, ResourceTemplateReference) and argument.name == "filename":
        prefix = argument.value or ""
        candidates = sorted(
            p.name for p in TESTS_DIR.glob("*.py") if p.name.startswith(prefix)
        )
        return Completion(values=candidates)
    return None


def main() -> None:
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
