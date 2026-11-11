import json

from openai import OpenAI

MODEL = "gpt-6-luna"
MAX_STEPS = 6

client = OpenAI()


def run_assistant(question, tools, functions):
    """Run the tool-calling loop until the model returns a final answer."""
    input_list = [{"role": "user", "content": question}]

    for step in range(MAX_STEPS):
        response = client.responses.create(model=MODEL, input=input_list, tools=tools)
        input_list += response.output

        function_calls = [item for item in response.output if item.type == "function_call"]

        if not function_calls:
            return response.output_text

        for call in function_calls:
            args = json.loads(call.arguments)
            print(f"Function call: {call.name} {args}")

            result = functions[call.name](**args)
            output = json.dumps(result)
            print(f"Returned to the model: {len(output)} characters")

            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": output,
                }
            )

    return f"Stopped after {MAX_STEPS} steps without a final answer."
