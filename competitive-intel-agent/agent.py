"""
Competitive Intel Agent — summarizes competitor positioning from pasted content.

Input: text pasted from competitor websites, release notes, G2/Capterra reviews,
       press releases, or any other source.
Output: structured competitive brief with positioning, strengths, weaknesses, and gaps.

Usage:
    python agent.py --content competitor.txt --competitor "Acme Corp"
    python agent.py --content competitor.txt --competitor "Acme Corp" --output brief.md
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tools import TOOLS, handle_tool

load_dotenv()

SYSTEM_PROMPT = """You are a product strategist building a competitive intelligence brief.

Given pasted content about a competitor (from their website, release notes, reviews, etc.),
produce a structured brief in Markdown:

## Positioning
How does this competitor position themselves? What is their core value proposition and
who do they say their ideal customer is?

## Strengths (from their perspective)
What do they emphasize? What do customers praise in reviews?

## Weaknesses & Complaints
What do customers complain about? What are gaps in their marketing or product?

## Recent Moves
Any new features, pricing changes, partnerships, or strategic shifts visible in the content?

## Differentiation Opportunities
Based on their weaknesses and gaps, where could a competitor win against them?
List 3-5 specific angles.

## Questions for Further Research
What key things are still unknown after reviewing this content?

Use tools to ask for context about your own product before writing differentiation opportunities."""


def run(content: str, competitor: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [
        {
            "role": "user",
            "content": (
                f"Build a competitive intelligence brief for {competitor} "
                f"based on this content:\n\n{content}"
            ),
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
    parser = argparse.ArgumentParser(description="Generate a competitive intelligence brief")
    parser.add_argument("--content", required=True, help="Path to file with competitor content")
    parser.add_argument("--competitor", required=True, help="Competitor name")
    parser.add_argument("--output", help="Write brief to this file instead of stdout")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    content = Path(args.content).read_text()
    brief = run(content, args.competitor)

    if args.output:
        Path(args.output).write_text(brief)
        print(f"Brief written to {args.output}")
    else:
        print(brief)


if __name__ == "__main__":
    main()
