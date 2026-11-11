from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6-luna",
    input="In one sentence, what does a customer support assistant do?",
)

print(response.output_text)
