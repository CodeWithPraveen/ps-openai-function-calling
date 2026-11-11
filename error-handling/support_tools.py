import json
import os
from pathlib import Path

import requests

ARTICLES_FILE = Path(__file__).parent.parent / "data" / "knowledge-base.json"
REPO = "CodeWithPraveen/ps-openai-function-calling"

SEARCH_KNOWLEDGE_BASE_TOOL = {
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


def search_knowledge_base(query, product):
    articles = json.loads(ARTICLES_FILE.read_text())
    keywords = query.lower().split()

    matches = []
    for article in articles:
        text = (article["title"] + " " + article["content"]).lower()
        if article["product"] == product and any(word in text for word in keywords):
            matches.append(article)

    return {"articles": matches}


def get_github_issue(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"
    headers = {}

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # GITHUB_TIMEOUT lets a demo force a timeout; the default is 10 seconds
    timeout = float(os.environ.get("GITHUB_TIMEOUT", "10"))

    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

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


TOOLS = [SEARCH_KNOWLEDGE_BASE_TOOL, GET_GITHUB_ISSUE_TOOL]

FUNCTIONS = {
    "search_knowledge_base": search_knowledge_base,
    "get_github_issue": get_github_issue,
}

QUESTION = (
    "A customer says EnterprisePro CSV exports time out. Find the workaround in the "
    "knowledge base, and check whether issue 1 in our tracker is fixed yet."
)
