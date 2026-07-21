"""
Meeting Notes Agent — converts a raw meeting transcript into structured notes.

Produces:
  - TL;DR (2 sentences)
  - Decisions made
  - Action items (owner, task, due date)
  - Open questions / parking lot
  - Key discussion points

Usage:
    python agent.py --transcript meeting.txt
    python agent.py --transcript meeting.txt --output notes.md
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from tools import TOOLS, handle_tool

load_dotenv()

SYSTEM_PROMPT = """You are a meticulous note-taker who extracts signal from meeting transcripts.

Given a raw meeting transcript (which may be messy, include filler words, or lack punctuation),
produce structured meeting notes in Markdown with these sections:

## TL;DR
Two sentences maximum — the most important thing that happened in this meeting.

## Decisions
Bulleted list of concrete decisions made. Only include things that were explicitly agreed upon.

## Action Items
Table with columns: Owner | Task | Due Date
If no due date was mentioned, write "TBD".

## Open Questions / Parking Lot
Things that came up but weren't resolved.

## Discussion Summary
3-5 bullet points covering the main topics discussed.

Use the tools to flag ambiguous owners or missing due dates before finalizing."""


def run(transcript: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [
        {
            "role": "user",
            "content": f"Please extract structured meeting notes from this transcript:\n\n{transcript}",
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
    parser = argparse.ArgumentParser(description="Extract structured notes from a meeting transcript")
    parser.add_argument("--transcript", required=True, help="Path to the transcript file")
    parser.add_argument("--output", help="Write notes to this file instead of stdout")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    transcript = Path(args.transcript).read_text()
    notes = run(transcript)

    if args.output:
        Path(args.output).write_text(notes)
        print(f"Notes written to {args.output}")
    else:
        print(notes)


if __name__ == "__main__":
    main()
