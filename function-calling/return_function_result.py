import json

from openai import OpenAI

from knowledge_base import SEARCH_KNOWLEDGE_BASE_TOOL, search_knowledge_base

MODEL = "gpt-6-luna"

client = OpenAI()
tools = [SEARCH_KNOWLEDGE_BASE_TOOL]

input_list = [
    {
        "role": "user",
        "content": "My CustomerConnect email sync stopped working. How do I fix it?",
    }
]

# First request: the model asks for a function call
response = client.responses.create(model=MODEL, input=input_list, tools=tools)

# Keep everything the model returned
input_list += response.output

for item in response.output:
    if item.type != "function_call":
        continue

    # Run the function in our own code
    args = json.loads(item.arguments)
    result = search_knowledge_base(**args)
    print("Function result:", json.dumps(result, indent=2))

    # Return the result with the matching call ID
    input_list.append(
        {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(result),
        }
    )

# Second request: the model writes the final answer
response = client.responses.create(model=MODEL, input=input_list, tools=tools)

print("\nFinal answer:")
print(response.output_text)
