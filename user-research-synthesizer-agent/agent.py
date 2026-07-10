"""
User Research Synthesizer Agent — clusters interview notes into themes and insights.

Input: a text file with raw notes from one or more user interviews.
Output: synthesized themes, supporting quotes, and recommended next steps.

Usage:
    python agent.py --notes interviews.txt
    python agent.py --notes interviews.txt --output synthesis.md
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tools import TOOLS, handle_tool

load_dotenv()

SYSTEM_PROMPT = """You are a UX researcher synthesizing notes from user interviews.

Given raw interview notes (which may include multiple participants), your job is to:

1. Identify 3-6 recurring themes across the interviews
2. For each theme:
   - Write a one-sentence insight statement ("Users feel X because Y")
   - List 2-4 supporting quotes or observations from the notes
   - Rate the strength of the evidence (weak / moderate / strong)
3. Identify any surprising or contradictory findings
4. Recommend 3 specific follow-up research questions or next steps

Format your output as clean Markdown. Use the tools to ask about research goals
or participant context if it would change your synthesis."""


def run(notes: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [
        {
            "role": "user",
            "content": f"Synthesize these user research notes into themes and insights:\n\n{notes}",
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return next(block.text for block in response.content if block.type == "text")

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

        break

    return ""


def main():
    parser = argparse.ArgumentParser(description="Synthesize user research notes into themes")
    parser.add_argument("--notes", required=True, help="Path to interview notes file")
    parser.add_argument("--output", help="Write synthesis to this file instead of stdout")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    notes = Path(args.notes).read_text()
    synthesis = run(notes)

    if args.output:
        Path(args.output).write_text(synthesis)
        print(f"Synthesis written to {args.output}")
    else:
        print(synthesis)


if __name__ == "__main__":
    main()
