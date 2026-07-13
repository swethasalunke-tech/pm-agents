# pm-agents

Six Claude-powered agents for the parts of a PM's job that eat the most time.

Each agent lives in its own directory with a standalone `agent.py`, tool definitions, and a README. Run any agent from the command line by following the setup steps in its README.

## Agents

| Agent | What it does |
|---|---|
| [prd-writer-agent](prd-writer-agent/) | Draft a full PRD from a one-paragraph brief |
| [roadmap-prioritizer-agent](roadmap-prioritizer-agent/) | Score and rank a feature list using RICE |
| [meeting-notes-agent](meeting-notes-agent/) | Turn a raw transcript into decisions and action items |
| [user-research-synthesizer-agent](user-research-synthesizer-agent/) | Cluster interview notes into themes and insights |
| [sprint-retro-agent](sprint-retro-agent/) | Analyze sprint data and write a retro summary |
| [competitive-intel-agent](competitive-intel-agent/) | Summarize competitor positioning from pasted content |

## Which agent should I use?

| If you're... | Use |
|---|---|
| Starting a new feature? | [prd-writer-agent](prd-writer-agent/) |
| Prioritizing the backlog? | [roadmap-prioritizer-agent](roadmap-prioritizer-agent/) |
| Just had a meeting? | [meeting-notes-agent](meeting-notes-agent/) |
| Ran user interviews? | [user-research-synthesizer-agent](user-research-synthesizer-agent/) |
| End of sprint? | [sprint-retro-agent](sprint-retro-agent/) |
| Watching a competitor? | [competitive-intel-agent](competitive-intel-agent/) |

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/settings/keys)

Each agent has its own `requirements.txt`. Install dependencies per agent:

```bash
cd prd-writer-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your ANTHROPIC_API_KEY
```

## License

MIT
