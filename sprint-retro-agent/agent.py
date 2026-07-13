"""
Sprint Retro Agent — analyzes sprint data and generates a retro summary.

Input: sprint data as text (completed stories, spill-over, blockers, velocity).
Output: structured retro document with what went well, what didn't, and action items.

Usage:
    python agent.py --sprint sprint.txt
    python agent.py --sprint sprint.txt --output retro.md
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tools import TOOLS, handle_tool

load_dotenv()

SYSTEM_PROMPT = """You are a scrum master facilitating a sprint retrospective.

Given sprint data (completed stories, velocity, carry-over tickets, blockers, team notes),
produce a retro document with these sections:

## Sprint Summary
- Planned vs actual velocity
- Stories completed vs carried over
- One-sentence characterization of the sprint

## What Went Well
3-5 bullets of genuine positives. Be specific — reference actual stories or events.

## What Didn't Go Well
3-5 bullets of honest problems. Avoid blame; focus on systems and processes.

## Root Cause Analysis
For the 1-2 most significant problems, write a brief why-chain:
  Problem → Why? → Why? → Root cause

## Action Items for Next Sprint
Table: Owner | Action | Success Criteria

## Morale Check
One sentence on team energy based on the data and notes provided.

Use tools to ask about team size or context that would change the analysis."""


def run(sprint_data: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [
        {
            "role": "user",
            "content": f"Generate a sprint retrospective from this data:\n\n{sprint_data}",
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
    parser = argparse.ArgumentParser(description="Generate a sprint retrospective")
    parser.add_argument("--sprint", required=True, help="Path to sprint data file")
    parser.add_argument("--output", help="Write retro to this file instead of stdout")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    sprint_data = Path(args.sprint).read_text()
    retro = run(sprint_data)

    if args.output:
        Path(args.output).write_text(retro)
        print(f"Retro written to {args.output}")
    else:
        print(retro)


if __name__ == "__main__":
    main()
