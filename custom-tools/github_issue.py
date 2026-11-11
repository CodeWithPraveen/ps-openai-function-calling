import requests

from assistant import run_assistant

REPO = "CodeWithPraveen/ps-openai-function-calling"

GET_GITHUB_ISSUE_TOOL = {
    "type": "function",
    "name": "get_github_issue",
    "description": "Get the title, status, and details of a bug in the Globomantics issue tracker on GitHub.",
    "parameters": {
        "type": "object",
        "properties": {
            "issue_number": {
                "type": "integer",
                "description": "The number of the issue, for example 1.",
            },
        },
        "required": ["issue_number"],
        "additionalProperties": False,
    },
    "strict": True,
}


def get_github_issue(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    print(f"GitHub returned: {len(response.text)} characters")

    # Return only the fields the model needs
    issue = response.json()
    return {
        "number": issue["number"],
        "title": issue["title"],
        "state": issue["state"],
        "labels": [label["name"] for label in issue["labels"]],
        "updated_at": issue["updated_at"],
        "comments": issue["comments"],
        "body": issue["body"],
    }


if __name__ == "__main__":
    answer = run_assistant(
        question="A customer says EnterprisePro CSV exports time out. That is issue 1 in our tracker. Is it fixed yet?",
        tools=[GET_GITHUB_ISSUE_TOOL],
        functions={"get_github_issue": get_github_issue},
    )

    print()
    print(answer)
