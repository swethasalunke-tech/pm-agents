# sprint-retro-agent

Generate a structured sprint retrospective from raw sprint data. Covers velocity, what went well, problems, root causes, and action items.

## What it produces

- **Sprint Summary** — planned vs actual velocity, stories completed vs carried
- **What Went Well** — specific positives from the sprint
- **What Didn't Go Well** — honest, blameless problems
- **Root Cause Analysis** — why-chain for the top 1-2 issues
- **Action Items** — owner, action, success criteria
- **Morale Check** — one-line read on team energy

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
python agent.py --sprint sprint.txt
python agent.py --sprint sprint.txt --output retro.md
```

### sprint.txt format

No special format — paste whatever you have:

```
Sprint 24 — June 9–20, 2025
Planned velocity: 42 points
Actual velocity: 31 points

Completed:
- PLAT-401 Auth token rotation (8 pts)
- PLAT-405 Dashboard query optimization (5 pts)
- PLAT-407 Fix CSV export encoding bug (3 pts)

Carried over:
- PLAT-402 Multi-region failover (13 pts) — blocked on infra review
- PLAT-406 Notification preferences UI (8 pts) — design changed mid-sprint

Blockers this sprint:
- Infra review meeting kept getting cancelled (3 times)
- Design delivered updated specs on day 8 of 10-day sprint

Team notes:
- Two engineers out sick mid-sprint
- Demo on Friday went well, stakeholders liked the query speed improvements
```
