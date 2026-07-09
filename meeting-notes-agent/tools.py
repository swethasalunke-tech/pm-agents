"""Tool definitions and handlers for the meeting notes agent."""

TOOLS = [
    {
        "name": "clarify_action_item",
        "description": (
            "Ask the user to clarify an ambiguous action item — e.g. when the owner "
            "is unclear or no due date was set."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "action_item": {"type": "string", "description": "The action item text"},
                "question": {"type": "string", "description": "What needs clarification"},
            },
            "required": ["action_item", "question"],
        },
    },
]


def handle_tool(name: str, inputs: dict) -> str:
    if name == "clarify_action_item":
        print(f"\n[Action item unclear]: {inputs['action_item']}")
        print(f"Question: {inputs['question']}")
        answer = input("Clarification: ").strip()
        return answer or "No clarification provided — use TBD."

    return f"Unknown tool: {name}"
