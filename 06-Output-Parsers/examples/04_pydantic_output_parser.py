
from typing import Literal

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field, ConfigDict

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Define Pydantic schema
class SupportTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Literal[
        "technical", "billing", "general"
    ] = Field(description="Category of the issue")

    priority: Literal[
        "low", "medium", "high"
    ] = Field(description="Urgency of the issue")

    summary: str = Field(
        min_length=5,
        description="Brief summary of the issue"
    )

# Step 3: Initialize Groq
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 4: Create the Pydantic output parser
parser = PydanticOutputParser(
    pydantic_object=SupportTicket
)

# Step 5: Create the prompt
prompt = PromptTemplate(
    template="""
    You are a customer support ticket classifier.

    Analyze the customer message and extract:
    - category
    - priority
    - summary

    Customer message:
    {message}

    Respond only in the required JSON format.

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

# Step 6: Connect prompt, model and parser
chain = prompt | model | parser

# Step 7: Invoke the chain
try:
    result = chain.invoke({
        "message": (
            "My account is locked and I cannot log in. "
            "I need urgent help before my meeting."
        )
    })

    print("PYDANTIC OUTPUT")
    print(result)

    print("\nRESULT TYPE")
    print(type(result))

    print("\nEXTRACTED INFORMATION")
    print("Category:", result.category)
    print("Priority:", result.priority)
    print("Summary:", result.summary)

    print("\nDICTIONARY OUTPUT")
    print(result.model_dump())

except OutputParserException as error:
    print("Parsing or validation failed:", error)

except Exception as error:
    print("Model request failed:", error)
