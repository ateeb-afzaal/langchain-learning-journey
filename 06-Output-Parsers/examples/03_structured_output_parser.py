
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain_classic.output_parsers import (
    ResponseSchema,
    StructuredOutputParser,
)

# Step 1: Load the Groq API key
load_dotenv()

# Step 2: Initialize the Groq model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Describe the expected fields
response_schemas = [
    ResponseSchema(
        name="brand",
        description="Brand of the purchased product",
        type="string"
    ),
    ResponseSchema(
        name="product",
        description="Type of purchased product",
        type="string"
    ),
    ResponseSchema(
        name="price",
        description="Price of the product as a number",
        type="number"
    ),
]

# Step 4: Create the output parser
parser = StructuredOutputParser.from_response_schemas(
    response_schemas
)

# Step 5: Create the prompt
prompt = PromptTemplate(
    template="""
    Extract the following product information:

    {message}

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

# Step 6: Connect the components
chain = prompt | model | parser

# Step 7: Generate and parse a response
try:
    result = chain.invoke({
        "message": "I bought a Lenovo laptop for $850."
    })

    print("STRUCTURED RESPONSE")
    print(result)

    print("\nRESULT TYPE")
    print(type(result))

    print("\nEXTRACTED INFORMATION")
    print("Brand:", result["brand"])
    print("Product:", result["product"])
    print("Price:", result["price"])

except (OutputParserException, KeyError, TypeError) as error:
    print("Parsing failed:", error)
except Exception as error:
    print("Model request failed:", error)
