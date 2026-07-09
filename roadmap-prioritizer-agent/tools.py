"""Tool definitions and handlers for the roadmap prioritizer agent."""

TOOLS = [
    {
        "name": "ask_feature_context",
        "description": (
            "Ask the user for missing context about a specific feature before scoring it. "
            "Use when you lack enough information to estimate Reach, Impact, or Effort."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string", "description": "The feature name"},
                "question": {"type": "string", "description": "What context you need"},
            },
            "required": ["feature", "question"],
        },
    },
    {
        "name": "record_score",
        "description": "Record the RICE score for a feature.",
        "input_schema": {
            "type": "object",
            "properties": {
                "feature": {"type": "string"},
                "reach": {"type": "number"},
                "impact": {"type": "number"},
                "confidence": {"type": "number"},
                "effort": {"type": "number"},
                "rationale": {"type": "string"},
            },
            "required": ["feature", "reach", "impact", "confidence", "effort", "rationale"],
        },
    },
]

_scores: list[dict] = []


def handle_tool(name: str, inputs: dict) -> str:
    if name == "ask_feature_context":
        print(f"\n[{inputs['feature']}]: {inputs['question']}")
        answer = input("Your answer: ").strip()
        return answer

    if name == "record_score":
        _scores.append(inputs)
        rice = (inputs["reach"] * inputs["impact"] * inputs["confidence"]) / max(inputs["effort"], 0.1)
        return f"Recorded. RICE = {rice:.1f}"

    return f"Unknown tool: {name}"
