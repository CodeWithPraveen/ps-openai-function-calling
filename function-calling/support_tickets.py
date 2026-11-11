import json
from pathlib import Path

TICKETS_FILE = Path(__file__).parent.parent / "data" / "tickets.json"

CREATE_SUPPORT_TICKET_TOOL = {
    "type": "function",
    "name": "create_support_ticket",
    "description": "Open a support ticket so the Globomantics support team follows up with the customer.",
    "parameters": {
        "type": "object",
        "properties": {
            "product": {
                "type": "string",
                "enum": ["EnterprisePro", "CustomerConnect", "SupportDesk"],
                "description": "The product the ticket is about.",
            },
            "summary": {
                "type": "string",
                "description": "One sentence that describes the customer's problem.",
            },
            "priority": {
                "type": "string",
                "enum": ["low", "normal", "high"],
                "description": "How urgent the problem is for the customer.",
            },
        },
        "required": ["product", "summary", "priority"],
        "additionalProperties": False,
    },
    "strict": True,
}


def create_support_ticket(product, summary, priority):
    tickets = json.loads(TICKETS_FILE.read_text()) if TICKETS_FILE.exists() else []

    ticket = {
        "ticket_id": f"TICKET-{1001 + len(tickets)}",
        "product": product,
        "summary": summary,
        "priority": priority,
        "status": "open",
    }

    # Save the ticket, the way a real ticketing system would
    tickets.append(ticket)
    TICKETS_FILE.write_text(json.dumps(tickets, indent=2))

    return ticket
