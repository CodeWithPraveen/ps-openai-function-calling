# Function Calling and Tool Use with OpenAI

Demo files for the Pluralsight course **Function Calling and Tool Use with OpenAI**. The course walks through every step; this repository holds the files it uses.

## Prerequisites

- Python 3.12 or later.
- An OpenAI API account with billing enabled, and an API key in `OPENAI_API_KEY`. Every demo uses `gpt-6-luna`, so the whole course costs a few cents.
- A free GitHub account, and a fine-grained personal access token with read-only access to public repositories in `GITHUB_TOKEN`. Only the authentication, MCP, and error-handling demos need it.

Set up once, from the repository folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`, and set variables with `set NAME=value` (Command Prompt) or `$env:NAME = "value"` (PowerShell). Use `python` in place of `python3`. Where a command starts with `NAME=value`, set the variable first, run the command, then set it back.

## Folders

| Folder | Module | What it holds |
| --- | --- | --- |
| `data/` | All | The knowledge base articles, the company profile for file search, and the function definition and result to paste into the Playground |
| `function-calling/` | Implementing function calling with the OpenAI API | The first API call, the function schema, tool choice, strict mode, the tool-calling loop, and the Chat Completions comparison |
| `custom-tools/` | Building custom tools with third-party APIs and MCP | The GitHub custom function, with and without a token, and the GitHub MCP server scripts |
| `error-handling/` | Managing responses and errors from tool integrations | Partial failure, retry with fallback, and tool-call logging |

The Issues tab of this repository holds three sample Globomantics bugs that the GitHub demos read. Globomantics is a fictional company.

## Warnings

- The MCP scripts send your `GITHUB_TOKEN` to OpenAI with each request, so that OpenAI can call GitHub's MCP server for you. Use a read-only token made for this course.
- The Playground file search demo creates a vector store and an uploaded file in your OpenAI project. They stay until you delete them.

## Tear down

- Delete the tickets the demos created: `rm -f data/tickets.json`
- On the OpenAI platform, open **Storage**. Under **Vector stores**, delete `globomantics-company-profile`. Under **Files**, delete `company-profile.md`.
- On the OpenAI platform, open **API Keys** and revoke the key you created for the course.
- On GitHub, open **Settings**, then **Developer settings**, and delete the token you created for the course.
- Remove the virtual environment: `rm -rf .venv`
