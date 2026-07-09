# roadmap-prioritizer-agent

Score and rank a feature list using the RICE framework. The agent asks clarifying questions when it needs more context, then produces a prioritized Markdown table.

## RICE scoring

`RICE = (Reach × Impact × Confidence) / Effort`

| Factor | What to provide |
|---|---|
| Reach | Users affected per quarter |
| Impact | 1 / 2 / 3 / 5 / 8 scale |
| Confidence | 10% / 50% / 80% / 100% |
| Effort | Person-months |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
# features.txt — one feature per line
python agent.py --features features.txt

# Save ranked output
python agent.py --features features.txt --output ranked.md
```

### features.txt example

```
Saved searches — users currently rebuild filters every session
In-app notifications — currently email only
SSO / SAML support — repeatedly requested by enterprise prospects
CSV export for all tables
Dark mode
```

## Example output

| Rank | Feature | Reach | Impact | Confidence | Effort | RICE | Rationale |
|---|---|---|---|---|---|---|---|
| 1 | SSO / SAML | 800 | 8 | 80% | 3 | 1707 | Unblocks enterprise deals |
| 2 | Saved searches | 3000 | 5 | 80% | 1 | 1200 | High reach, low effort |
| … | … | … | … | … | … | … | … |
