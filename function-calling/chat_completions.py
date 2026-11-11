import json

from openai import OpenAI

from knowledge_base import SEARCH_KNOWLEDGE_BASE_TOOL, search_knowledge_base

MODEL = "gpt-6-luna"

client = OpenAI()

# Chat Completions nests the same definition under a "function" key
tools = [
    {
        "type": "function",
        "function": {
            "name": SEARCH_KNOWLEDGE_BASE_TOOL["name"],
            "description": SEARCH_KNOWLEDGE_BASE_TOOL["description"],
            "parameters": SEARCH_KNOWLEDGE_BASE_TOOL["parameters"],
            "strict": True,
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "My CustomerConnect email sync stopped working. How do I fix it?",
    }
]

# First request: the tool calls arrive on the assistant message
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    reasoning_effort="none",
)

message = response.choices[0].message
messages.append(message)

for tool_call in message.tool_calls:
    print("Tool call:", tool_call.function.name, tool_call.function.arguments)

    # Run the function and return its result in a "tool" message
    args = json.loads(tool_call.function.arguments)
    result = search_knowledge_base(**args)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        }
    )

# Second request: the model writes the final answer
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    reasoning_effort="none",
)

print("\nFinal answer:")
print(response.choices[0].message.content)
