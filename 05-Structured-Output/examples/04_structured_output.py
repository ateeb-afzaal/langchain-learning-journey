
from typing import Literal

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, ConfigDict, Field

# Step 1: Load environment variables
load_dotenv()

# Step 2: Define the output schema
class SupportTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Literal[
        "technical", "billing", "general"
    ] = Field(description="Customer issue category")

    priority: Literal[
        "low", "medium", "high"
    ] = Field(description="Urgency of the issue")

    summary: str = Field(
        description="Brief summary of the issue"
    )

# Step 3: Initialize the Groq model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 4: Enable native structured output
structured_model = model.with_structured_output(
    SupportTicket,
    method="json_schema",
    strict=True
)

# Step 5: Send the customer request
customer_message = (
    "I cannot access my account and I have an "
    "important meeting today. Please resolve it urgently."
)

try:
    result = structured_model.invoke(
        "Classify this customer support message. "
        "Use only the information provided.\n\n"
        f"Customer message: {customer_message}"
    )

    # Step 6: Inspect the validated result
    print("Result type:", type(result))
    print("Category:", result.category)
    print("Priority:", result.priority)
    print("Summary:", result.summary)

    # Step 7: Convert the model to a dictionary
    print("\nStructured dictionary:")
    print(result.model_dump())

except Exception as error:
    print("Structured output request failed:")
    print(error)
