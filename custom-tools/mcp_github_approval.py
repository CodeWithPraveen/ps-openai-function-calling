import os

from openai import OpenAI

MODEL = "gpt-6-luna"

client = OpenAI()

github_mcp = {
    "type": "mcp",
    "server_label": "github",
    "server_description": "GitHub's MCP server, for reading issues in the Globomantics issue tracker.",
    "server_url": "https://api.githubcopilot.com/mcp/x/issues/readonly",
    "authorization": os.environ["GITHUB_TOKEN"],
    "allowed_tools": ["issue_read"],
    "require_approval": "always",
}

# First request: the model asks to call a tool, and the API waits for approval
response = client.responses.create(
    model=MODEL,
    input=(
        "A customer says EnterprisePro CSV exports time out. That is issue 1 in the "
        "CodeWithPraveen/ps-openai-function-calling repository. Is it fixed yet?"
    ),
    tools=[github_mcp],
)

approvals = []

for item in response.output:
    if item.type == "mcp_list_tools":
        print("Tools the model can use:", [tool.name for tool in item.tools])

    if item.type == "mcp_approval_request":
        print("The model wants to call:", item.name, item.arguments)
        answer = input("Approve this call? (y/n) ")

        approvals.append(
            {
                "type": "mcp_approval_response",
                "approval_request_id": item.id,
                "approve": answer == "y",
            }
        )

# Second request: send the decision, and the API runs the approved call
response = client.responses.create(
    model=MODEL,
    previous_response_id=response.id,
    input=approvals,
    tools=[github_mcp],
)

print()
print(response.output_text)
