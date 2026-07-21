"""
PRD Writer Agent — generates a structured PRD from a one-paragraph brief.

Usage:
    python agent.py --brief "We want to add a saved searches feature to our SaaS app."
    python agent.py --brief-file brief.txt --output prd.md
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tools import TOOLS, handle_tool

load_dotenv()

SYSTEM_PROMPT = """You are a senior product manager writing a Product Requirements Document (PRD).

Given a brief description of a feature or product, produce a complete PRD with these sections:
1. Overview — one paragraph summary
2. Problem Statement — what user pain this solves and evidence for it
3. Goals & Success Metrics — 3-5 measurable outcomes
4. User Stories — written as "As a [persona], I want [action] so that [benefit]"
5. Functional Requirements — numbered list of must-have behaviors
6. Non-Functional Requirements — performance, security, accessibility constraints
7. Out of Scope — explicit exclusions to prevent scope creep
8. Open Questions — unresolved decisions that need stakeholder input

Use the tools available to ask clarifying questions or look up related context before writing.
When you have enough information, write the PRD in clean Markdown."""


def run(brief: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": f"Write a PRD for the following:\n\n{brief}"}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return next(
                block.text for block in response.content if block.type == "text"
            )

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = handle_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        raise RuntimeError(
            f"Anthropic API stopped with unexpected stop_reason={response.stop_reason!r} "
            "and no text was returned. This usually means max_tokens was hit before "
            "the model finished; try a shorter input or a higher max_tokens."
        )


def main():
    parser = argparse.ArgumentParser(description="Generate a PRD from a brief")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", help="One-paragraph feature brief")
    group.add_argument("--brief-file", help="Path to a text file containing the brief")
    parser.add_argument("--output", help="Write PRD to this file instead of stdout")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    brief = args.brief
    if args.brief_file:
        brief = Path(args.brief_file).read_text()

    prd = run(brief)

    if args.output:
        Path(args.output).write_text(prd)
        print(f"PRD written to {args.output}")
    else:
        print(prd)


if __name__ == "__main__":
    main()
