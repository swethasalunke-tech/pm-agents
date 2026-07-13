# competitive-intel-agent

Build a competitive intelligence brief from any pasted content — competitor websites, release notes, G2/Capterra reviews, press releases, or LinkedIn posts.

## What it produces

- **Positioning** — their stated value prop and target customer
- **Strengths** — what they emphasize and what customers praise
- **Weaknesses & complaints** — gaps and customer frustrations
- **Recent moves** — new features, pricing changes, partnerships
- **Differentiation opportunities** — where you can win against them
- **Questions for further research** — what's still unknown

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
# competitor.txt = pasted content from their website, reviews, etc.
python agent.py --content competitor.txt --competitor "Acme Corp"

# Save to file
python agent.py --content competitor.txt --competitor "Acme Corp" --output brief.md
```

### What to put in competitor.txt

Paste anything — no special format:

```
[From their homepage]
"Acme is the project management tool built for engineering teams."
Pricing starts at $12/user/month...

[From G2 reviews]
★★★☆☆ "The Gantt chart is great but the mobile app is basically unusable."
★★★★★ "Best Jira alternative we've tried. Search is fast."
★★☆☆☆ "Customer support is slow. Took 4 days to get a response."

[From their blog — June 2025]
Announcing native Slack integration and a new AI assistant for sprint planning...
```
