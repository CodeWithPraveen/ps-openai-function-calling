import json
import time

import requests
from openai import OpenAI

from support_tools import FUNCTIONS, QUESTION, TOOLS

MODEL = "gpt-6-luna"
MAX_STEPS = 6
MAX_ATTEMPTS = 3

client = OpenAI()


def is_retryable(error):
    """Timeouts, dropped connections, rate limits, and server errors can succeed on a retry."""
    if isinstance(error, (requests.Timeout, requests.ConnectionError)):
        return True

    if isinstance(error, requests.HTTPError):
        status = error.response.status_code
        return status == 429 or status >= 500

    return False


def call_with_retry(name, args):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return FUNCTIONS[name](**args)
        except Exception as error:
            if not is_retryable(error) or attempt == MAX_ATTEMPTS:
                print(f"{name}: attempt {attempt} failed, giving up")
                break

            # Back off: wait 1 second, then 2 seconds
            delay = 2 ** (attempt - 1)
            print(f"{name}: attempt {attempt} failed, retrying in {delay}s")
            time.sleep(delay)

    # The fallback tells the model what happened and what to offer instead
    return {
        "error": f"{name} is not available right now.",
        "fallback": "Tell the customer this information is temporarily unavailable, "
        "share what the other tools returned, and offer to follow up by email.",
    }


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
        result = call_with_retry(call.name, args)

        if "error" not in result:
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
