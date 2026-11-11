import os

from openai import OpenAI

client = OpenAI()

github_mcp = {
    "type": "mcp",
    "server_label": "github",
    "server_description": "GitHub's MCP server, for reading issues in the Globomantics issue tracker.",
    "server_url": "https://api.githubcopilot.com/mcp/x/issues/readonly",
    "authorization": os.environ["GITHUB_TOKEN"],
    "require_approval": "never",
}

response = client.responses.create(
    model="gpt-6-luna",
    input=(
        "A customer says EnterprisePro CSV exports time out. That is issue 1 in the "
        "CodeWithPraveen/ps-openai-function-calling repository. Is it fixed yet?"
    ),
    tools=[github_mcp],
)

for item in response.output:
    print(item.type)

    if item.type == "mcp_list_tools":
        for tool in item.tools:
            print("  tool:", tool.name)

    if item.type == "mcp_call":
        print("  name:", item.name)
        print("  arguments:", item.arguments)

print()
print(response.output_text)
