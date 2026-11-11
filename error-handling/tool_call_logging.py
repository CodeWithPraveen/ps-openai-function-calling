import json
import logging
import time

from openai import OpenAI

from support_tools import FUNCTIONS, QUESTION, TOOLS

MODEL = "gpt-6-luna"
MAX_STEPS = 6

# Libraries log warnings only; our own logger logs every tool call
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.WARNING)
log = logging.getLogger("support_assistant")
log.setLevel(logging.INFO)

client = OpenAI()

input_list = [{"role": "user", "content": QUESTION}]
answer = None

for step in range(MAX_STEPS):
    response = client.responses.create(model=MODEL, input=input_list, tools=TOOLS)
    input_list += response.output

    function_calls = [item for item in response.output if item.type == "function_call"]
    log.info("response id=%s tool_calls=%d", response.id, len(function_calls))

    if not function_calls:
        answer = response.output_text
        break

    for call in function_calls:
        args = json.loads(call.arguments)
        started = time.perf_counter()

        try:
            result = FUNCTIONS[call.name](**args)
            outcome = "ok"
        except Exception as error:
            # The model gets a message that is safe to repeat; the log keeps the raw error
            result = {"error": f"{call.name} is not available right now."}
            outcome = f"error: {error}"

        duration_ms = round((time.perf_counter() - started) * 1000)

        # One line per tool call: what ran, with what input, how long it took, how it ended
        log.info(
            "tool_call name=%s call_id=%s arguments=%s duration_ms=%d outcome=%s",
            call.name,
            call.call_id,
            call.arguments,
            duration_ms,
            outcome,
        )

        input_list.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            }
        )

print()
print(answer or f"Stopped after {MAX_STEPS} steps without a final answer.")
