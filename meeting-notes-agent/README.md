# meeting-notes-agent

Paste in a raw meeting transcript and get back structured notes with decisions, action items, and open questions.

Works with transcripts from Zoom, Google Meet, Otter.ai, or anything you copy-paste.

## Output format

- **TL;DR** — 2-sentence summary
- **Decisions** — explicit agreements made in the meeting
- **Action items** — owner, task, due date (asks you to clarify ambiguous ones)
- **Open questions** — things that came up but weren't resolved
- **Discussion summary** — key topics covered

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
# Print notes to terminal
python agent.py --transcript meeting.txt

# Save to a file
python agent.py --transcript meeting.txt --output notes.md
```

## Example output

```markdown
## TL;DR
The team aligned on launching the beta in Q3 and agreed to cut the offline mode feature.
Sarah owns the updated launch plan by Friday.

## Decisions
- Beta launch target: end of Q3
- Offline mode cut from v1 scope

## Action Items
| Owner | Task | Due Date |
|---|---|---|
| Sarah | Updated launch plan | Friday Jun 27 |
| Dev team | Performance benchmarks | TBD |
```
