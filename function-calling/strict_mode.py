import openai
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
                "max_results": {
                    "type": "integer",
                    "description": "The most articles to return. Only set this when the customer asks for a specific number.",
                },
            },
            "required": ["query", "product"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

try:
    response = client.responses.create(
        model="gpt-6-luna",
        input="My CustomerConnect email sync stopped working. How do I fix it?",
        tools=tools,
    )
except openai.BadRequestError as error:
    print("Request rejected:", error.message)
else:
    for item in response.output:
        if item.type == "function_call":
            print("arguments:", item.arguments)
