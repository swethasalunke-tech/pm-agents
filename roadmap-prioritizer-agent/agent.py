"""
Roadmap Prioritizer Agent — scores a feature list using RICE and ranks them.

Input: a CSV or newline-separated list of feature names (optionally with context notes).
Output: a ranked Markdown table with RICE scores and rationale.

Usage:
    python agent.py --features features.txt
    python agent.py --features features.csv --output ranked.md
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tools import TOOLS, handle_tool

load_dotenv()

SYSTEM_PROMPT = """You are a senior product manager who specializes in roadmap prioritization.

Given a list of features, score each one using the RICE framework:
- Reach: how many users will this affect per quarter (estimate)
- Impact: how much will it move the needle per user (1=minimal, 2=low, 3=medium, 5=high, 8=massive)
- Confidence: how confident are you in these estimates (10%=low, 50%=medium, 80%=high, 100%=certain)
- Effort: person-months of engineering work required

RICE Score = (Reach × Impact × Confidence) / Effort

Use the tools available to ask for missing context on any feature before scoring.
Present results as a Markdown table sorted by RICE score descending, with a one-sentence rationale for each item."""


def run(features_text: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [
        {
            "role": "user",
            "content": f"Score and prioritize these features using RICE:\n\n{features_text}",
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

        raise RuntimeError(
            f"Anthropic API stopped with unexpected stop_reason={response.stop_reason!r} "
            "and no text was returned. This usually means max_tokens was hit before "
            "the model finished; try a shorter input or a higher max_tokens."
        )


def main():
    parser = argparse.ArgumentParser(description="Prioritize features using RICE")
    parser.add_argument("--features", required=True, help="File with feature list (one per line or CSV)")
    parser.add_argument("--output", help="Write ranked table to this file instead of stdout")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    features_text = Path(args.features).read_text()
    result = run(features_text)

    if args.output:
        Path(args.output).write_text(result)
        print(f"Ranked roadmap written to {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
