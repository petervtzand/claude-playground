"""Ask Claude a question programmatically via the Claude Agent SDK.

Embeds Claude as a library — *your code* drives Claude (vs. Claude Code being
the shell that drives your code). Restricted to read-only tools so the demo
can't accidentally edit anything.

Usage:
    uv run python scripts/ask_claude.py "<question>"

Example:
    uv run python scripts/ask_claude.py "How many endpoints does main.py have?"
"""

import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    query,
)


async def ask(question: str) -> None:
    """Run a one-shot Claude query and stream the response.

    Prints text blocks as Claude speaks, tool-call blocks inline (so you can
    see the agent loop happening), and the final USD cost from the SDK.
    """
    options = ClaudeAgentOptions(
        system_prompt="You are a concise assistant. Answer in 2-3 sentences.",
        allowed_tools=["Read", "Glob", "Grep"],
        max_turns=5,
    )

    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"  [tool: {block.name}({block.input})]")
        elif isinstance(message, ResultMessage):
            print(f"\n— Cost: ${message.total_cost_usd:.4f}")


def main() -> None:
    """CLI entry point. Reads the question from argv[1] or uses a default."""
    if len(sys.argv) < 2:
        question = "How many endpoints does main.py have?"
        print(f"(No question provided — using default: {question!r})\n")
    else:
        question = sys.argv[1]
    asyncio.run(ask(question))


if __name__ == "__main__":
    main()
