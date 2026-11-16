import json
from ai_engine import get_client
from tools import calculate, count_words

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a basic mathematical expression safely.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "word_counter",
            "description": "Count words, characters, and sentences in text.",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
                "additionalProperties": False,
            },
        },
    },
]

def _execute_tool(name, arguments):
    if name == "calculator":
        return {"result": calculate(arguments["expression"])}
    if name == "word_counter":
        return count_words(arguments["text"])
    return {"error": "Unknown tool."}

def run_agent(api_key: str, model: str, task: str) -> str:
    client = get_client(api_key)
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI study and career agent. Plan briefly, use available tools "
                "when useful, then provide a clear final answer. Do not claim a tool was used "
                "unless it was actually called."
            ),
        },
        {"role": "user", "content": task},
    ]
    for _ in range(4):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            temperature=0.2,
        )
        message = response.choices[0].message
        if not message.tool_calls:
            return message.content or "The agent did not return a text answer."
        messages.append(message)
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")
            try:
                result = _execute_tool(name, args)
            except Exception as exc:
                result = {"error": str(exc)}
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })
    return "The agent reached its tool-call limit. Please simplify the task and try again."
