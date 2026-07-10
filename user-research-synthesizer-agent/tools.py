"""Tool definitions and handlers for the user research synthesizer agent."""

TOOLS = [
    {
        "name": "ask_research_context",
        "description": (
            "Ask about the research goals or participant context when it would "
            "meaningfully change the synthesis — e.g. whether participants were "
            "enterprise vs consumer users, or what decision this research informs."
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
    if name == "ask_research_context":
        print(f"\n[Context question]: {inputs['question']}")
        answer = input("Your answer: ").strip()
        return answer or "No additional context provided."

    return f"Unknown tool: {name}"
