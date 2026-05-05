"""MCP server exposing a single `run_tests` tool for subagents.

Wraps `task test` so a subagent (like endpoint-tester) can verify its work
without needing full Bash access. Stdio transport.
"""

import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

PROJECT_ROOT = Path(__file__).resolve().parent.parent

mcp = FastMCP(
    "local-tests",
    instructions=(
        "One tool: run_tests. Executes the project's pytest suite via "
        "`task test` and returns structured stdout/stderr/exit code. "
        "Use after editing test files to verify they pass."
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


def main() -> None:
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
