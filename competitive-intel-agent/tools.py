"""Tool definitions and handlers for the competitive intel agent."""

TOOLS = [
    {
        "name": "ask_own_product_context",
        "description": (
            "Ask about your own product's strengths or positioning so differentiation "
            "opportunities are grounded in real advantages, not generic ones."
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
    if name == "ask_own_product_context":
        print(f"\n[Context about your product]: {inputs['question']}")
        answer = input("Your answer: ").strip()
        return answer or "No product context provided — use generic framing."

    return f"Unknown tool: {name}"
