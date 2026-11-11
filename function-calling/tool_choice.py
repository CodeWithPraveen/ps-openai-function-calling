from openai import OpenAI

from knowledge_base import SEARCH_KNOWLEDGE_BASE_TOOL

MODEL = "gpt-6-luna"

QUESTIONS = [
    "Hi! Which Globomantics products can you help me with?",
    "My CustomerConnect email sync stopped working. How do I fix it?",
]

TOOL_CHOICES = {
    "auto": "auto",
    "required": "required",
    "forced function": {"type": "function", "name": "search_knowledge_base"},
    "none": "none",
}

client = OpenAI()

for question in QUESTIONS:
    print(question)

    for label, tool_choice in TOOL_CHOICES.items():
        response = client.responses.create(
            model=MODEL,
            input=question,
            tools=[SEARCH_KNOWLEDGE_BASE_TOOL],
            tool_choice=tool_choice,
        )

        # Report whether the model asked for a function or answered in text
        function_calls = [item.name for item in response.output if item.type == "function_call"]
        outcome = f"calls {function_calls[0]}" if function_calls else "answers in text"
        print(f"  {label:16} {outcome}")

    print()
