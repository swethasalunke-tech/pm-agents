# user-research-synthesizer-agent

Paste in raw notes from user interviews and get back a structured synthesis: recurring themes, supporting quotes, evidence strength, and recommended next steps.

## What it produces

- **Themes** (3-6) — each with a one-sentence insight statement
- **Supporting quotes** — pulled directly from your notes
- **Evidence strength** — weak / moderate / strong per theme
- **Surprises & contradictions** — findings that cut against assumptions
- **Next steps** — 3 follow-up research questions

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
# Notes from multiple interviews in one file
python agent.py --notes interviews.txt

# Save to file
python agent.py --notes interviews.txt --output synthesis.md
```

### interviews.txt format

No special format required. Paste notes however you captured them:

```
--- Participant 1 (enterprise, 3 yrs using product) ---
Struggled to find export button. "I gave up and asked support."
Uses dashboards daily but doesn't trust the numbers after the incident last month.

--- Participant 2 (SMB, new user) ---
Onboarding felt long. Skipped the walkthrough entirely.
...
```

## Example output

```markdown
## Theme 1: Data trust is broken after reliability incidents

**Insight:** Users reduce engagement with dashboards after experiencing even one data
accuracy issue, because they have no way to verify when the problem is fixed.

**Evidence strength:** Strong

**Supporting observations:**
- "I stopped trusting the numbers after last month" (P1)
- P3 exports data to Excel to cross-check before sharing with leadership
```
