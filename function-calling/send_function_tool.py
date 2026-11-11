from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "search_knowledge_base",
        "description": "Search the Globomantics knowledge base for help articles about a product.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keywords that describe the customer's problem.",
                },
                "product": {
                    "type": "string",
                    "enum": ["EnterprisePro", "CustomerConnect", "SupportDesk"],
                    "description": "The product the question is about.",
                },
            },
            "required": ["query", "product"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

response = client.responses.create(
    model="gpt-6-luna",
    input="My CustomerConnect email sync stopped working. How do I fix it?",
    tools=tools,
)

for item in response.output:
    print(item.type)

    if item.type == "function_call":
        print("  name:", item.name)
        print("  arguments:", item.arguments)
        print("  call_id:", item.call_id)
