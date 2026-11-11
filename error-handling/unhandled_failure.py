import json

from openai import OpenAI

from support_tools import FUNCTIONS, QUESTION, TOOLS

MODEL = "gpt-6-luna"
MAX_STEPS = 6

client = OpenAI()

input_list = [{"role": "user", "content": QUESTION}]
answer = None

for step in range(MAX_STEPS):
    response = client.responses.create(model=MODEL, input=input_list, tools=TOOLS)
    input_list += response.output

    function_calls = [item for item in response.output if item.type == "function_call"]

    if not function_calls:
        answer = response.output_text
        break

    for call in function_calls:
        args = json.loads(call.arguments)

        # Nothing catches an error here, so one failed tool stops the whole run
        result = FUNCTIONS[call.name](**args)
        print(f"{call.name}: ok")

        input_list.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            }
        )

print()
print(answer or f"Stopped after {MAX_STEPS} steps without a final answer.")
