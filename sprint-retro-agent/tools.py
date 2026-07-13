"""Tool definitions and handlers for the sprint retro agent."""

TOOLS = [
    {
        "name": "ask_sprint_context",
        "description": (
            "Ask for additional sprint context that would improve the retro analysis — "
            "e.g. team size, whether there were holidays, or what the sprint goal was."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
            },
            "required": ["question"],
        },
    },
]


def handle_tool(name: str, inputs: dict) -> str:
    if name == "ask_sprint_context":
        print(f"\n[Sprint context needed]: {inputs['question']}")
        answer = input("Your answer: ").strip()
        return answer or "No additional context provided."

    return f"Unknown tool: {name}"
