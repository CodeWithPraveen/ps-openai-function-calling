import os

import requests

from assistant import run_assistant
from github_issue import GET_GITHUB_ISSUE_TOOL, REPO


def get_github_issue(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"
    headers = {}

    # The token comes from the environment, never from the model
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print("Rate limit:", response.headers["X-RateLimit-Limit"], "requests per hour")

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
