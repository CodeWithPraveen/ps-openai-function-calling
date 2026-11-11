import json
from pathlib import Path

ARTICLES_FILE = Path(__file__).parent.parent / "data" / "knowledge-base.json"

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


def search_knowledge_base(query, product):
    articles = json.loads(ARTICLES_FILE.read_text())
    keywords = query.lower().split()

    # Keep the articles for this product that mention any keyword
    matches = []
    for article in articles:
        text = (article["title"] + " " + article["content"]).lower()
        if article["product"] == product and any(word in text for word in keywords):
            matches.append(article)

    return {"articles": matches}
