import json

from openai import OpenAI

from knowledge_base import SEARCH_KNOWLEDGE_BASE_TOOL, search_knowledge_base
from support_tickets import CREATE_SUPPORT_TICKET_TOOL, create_support_ticket

MODEL = "gpt-6-luna"
MAX_STEPS = 6

TOOLS = [SEARCH_KNOWLEDGE_BASE_TOOL, CREATE_SUPPORT_TICKET_TOOL]

FUNCTIONS = {
    "search_knowledge_base": search_knowledge_base,
    "create_support_ticket": create_support_ticket,
}

client = OpenAI()

input_list = [
    {
        "role": "user",
        "content": (
            "I have two problems. EnterprisePro CSV exports time out, and "
            "CustomerConnect email sync stopped after a password change. "
            "Find the fixes, and open a ticket for any problem that only has a workaround."
        ),
    }
]

answer = None

for step in range(1, MAX_STEPS + 1):
    response = client.responses.create(
        model=MODEL,
        input=input_list,
        tools=TOOLS,
        parallel_tool_calls=True,
    )

    # Keep everything the model returned
    input_list += response.output

    function_calls = [item for item in response.output if item.type == "function_call"]

    # No function calls means the model has written its final answer
    if not function_calls:
        answer = response.output_text
        break

    item_types = ", ".join(item.type for item in response.output)
    print(f"Request {step}: {item_types}")

    for call in function_calls:
        args = json.loads(call.arguments)
        print(f"  {call.name} {args}")

        # Run the function and return its result with the matching call ID
        result = FUNCTIONS[call.name](**args)
        input_list.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            }
        )

print()
print(answer or f"Stopped after {MAX_STEPS} steps without a final answer.")
