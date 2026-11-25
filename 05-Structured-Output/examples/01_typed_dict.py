
from typing import TypedDict, Annotated, Literal, NotRequired

# Step 1: Define the expected structure
class SupportTicket(TypedDict):
    category: Annotated[
        Literal["technical", "billing", "general"],
        "Category of the support request"
    ]

    priority: Annotated[
        Literal["low", "medium", "high"],
        "Priority of the support request"
    ]

    summary: str
    customer_name: NotRequired[str]


# Step 2: Create a dictionary matching the schema
ticket: SupportTicket = {
    "category": "technical",
    "priority": "high",
    "summary": "Customer cannot log in to their account",
    "customer_name": "Ali"
}

# Step 3: Read individual fields
print("Category:", ticket["category"])
print("Priority:", ticket["priority"])
print("Summary:", ticket["summary"])
print("Customer:", ticket.get("customer_name", "Not provided"))

# Step 4: Demonstrate that TypedDict does not
# automatically validate dictionaries at runtime
invalid_ticket: SupportTicket = {
    "category": "unknown",  # Invalid according to Literal
    "priority": "urgent",   # Invalid according to Literal
    "summary": "Example of incorrect values"
}

print("\nInvalid data still exists at runtime:")
print(invalid_ticket)
