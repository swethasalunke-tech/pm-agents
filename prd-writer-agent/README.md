# prd-writer-agent

Generate a complete, structured PRD from a one-paragraph feature brief using Claude.

## What it produces

- Overview
- Problem Statement
- Goals & Success Metrics
- User Stories
- Functional Requirements
- Non-Functional Requirements
- Out of Scope
- Open Questions

The agent may ask you one or two clarifying questions before writing if the brief is ambiguous.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
```

## Usage

```bash
# From a string
python agent.py --brief "Add a saved searches feature to our B2B SaaS dashboard."

# From a file
python agent.py --brief-file brief.txt

# Write to a file
python agent.py --brief "..." --output prd.md
```

## Example output

```markdown
## Overview
Saved Searches lets users bookmark complex filter combinations in the dashboard...

## Problem Statement
Power users rebuild the same 5–10 filter sets every session. In the last quarter,
"search setup" appeared in 34% of support tickets flagged as friction...
```
