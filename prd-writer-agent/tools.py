"""Tool definitions and handlers for the PRD writer agent."""

TOOLS = [
    {
        "name": "ask_clarifying_question",
        "description": (
            "Ask a clarifying question when the brief is ambiguous. "
            "Use this before writing if you need to know the target persona, "
            "platform, or key constraints."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The question to ask the user"},
            },
            "required": ["question"],
        },
    },
    {
        "name": "set_section",
        "description": "Store a completed PRD section so it can be assembled at the end.",
        "input_schema": {
            "type": "object",
            "properties": {
                "section_name": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["section_name", "content"],
        },
    },
]

_sections: dict[str, str] = {}


def handle_tool(name: str, inputs: dict) -> str:
    if name == "ask_clarifying_question":
        print(f"\n[Agent question]: {inputs['question']}")
        answer = input("Your answer: ").strip()
        return answer

    if name == "set_section":
        _sections[inputs["section_name"]] = inputs["content"]
        return f"Section '{inputs['section_name']}' saved."

    return f"Unknown tool: {name}"
