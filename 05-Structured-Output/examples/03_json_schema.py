
from jsonschema import Draft202012Validator

# Step 1: Define the JSON Schema
ticket_schema = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["technical", "billing", "general"]
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        },
        "summary": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["category", "priority", "summary"],
    "additionalProperties": False
}

# Step 2: Prepare test data
valid_ticket = {
    "category": "technical",
    "priority": "high",
    "summary": "Customer cannot log in"
}

invalid_ticket = {
    "category": "unknown",
    "priority": "urgent",
    "summary": "Help"
}

# Step 3: Create a validator
Draft202012Validator.check_schema(ticket_schema)
validator = Draft202012Validator(ticket_schema)

# Step 4: Validate both tickets
for name, ticket in [
    ("VALID TICKET", valid_ticket),
    ("INVALID TICKET", invalid_ticket)
]:
    print(f"\n{name}")

    errors = list(validator.iter_errors(ticket))

    if not errors:
        print("Validation passed!")
    else:
        for error in errors:
            print("Validation error:", error.message)
