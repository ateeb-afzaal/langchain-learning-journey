
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Initialize the chat model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Initialize JSON parser
parser = JsonOutputParser()

# Step 4: Create a dynamic prompt
prompt = PromptTemplate(
    template="""
    Extract product information from this message:

    {message}

    Return exactly these fields:
    - brand: string
    - product: string
    - price: number

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

# Step 5: Create the chain
chain = prompt | model | parser

# Step 6: Invoke the chain
try:
    result = chain.invoke({
        "message": "I bought a Lenovo laptop for $850."
    })

    print("PARSED JSON RESPONSE")
    print(result)

    print("\nRESULT TYPE")
    print(type(result))

    # Step 7: Access individual values
    print("\nEXTRACTED INFORMATION")
    print("Brand:", result["brand"])
    print("Product:", result["product"])
    print("Price:", result["price"])

except (OutputParserException, KeyError, TypeError) as error:
    print("Parsing or extraction failed:", error)
