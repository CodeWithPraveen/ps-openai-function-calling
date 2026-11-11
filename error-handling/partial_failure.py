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

        try:
            result = FUNCTIONS[call.name](**args)
            print(f"{call.name}: ok")
        except Exception as error:
            # Return the failure as this call's output, so the model can work with it
            result = {"error": f"{call.name} failed: {error}"}
            print(f"{call.name}: failed, {error}")

        input_list.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            }
        )

print()
print(answer or f"Stopped after {MAX_STEPS} steps without a final answer.")
