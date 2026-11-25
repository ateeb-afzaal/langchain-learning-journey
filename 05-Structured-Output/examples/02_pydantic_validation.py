
from typing import Literal
from pydantic import BaseModel, Field, ValidationError

# Step 1: Define a validated data model
class SupportTicket(BaseModel):
    category: Literal[
        "technical", "billing", "general"
    ]

    priority: Literal[
        "low", "medium", "high"
    ]

    summary: str = Field(
        min_length=5,
        description="Short summary of the issue"
    )

# Step 2: Test valid data
valid_ticket = {
    "category": "technical",
    "priority": "high",
    "summary": "Customer cannot log in"
}

ticket = SupportTicket.model_validate(valid_ticket)

print("VALID TICKET:")
print(ticket.model_dump())

# Step 3: Test invalid data
invalid_ticket = {
    "category": "unknown",
    "priority": "urgent",
    "summary": "Help"
}

print("\nINVALID TICKET:")

try:
    SupportTicket.model_validate(invalid_ticket)
except ValidationError as error:
    print(error)

# Step 4: Display the JSON Schema
print("\nJSON SCHEMA:")
print(SupportTicket.model_json_schema())
