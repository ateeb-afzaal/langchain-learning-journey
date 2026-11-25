
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Initialize the chat model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Create a reusable prompt
prompt = PromptTemplate.from_template(
    "Explain {topic} in 3 simple sentences."
)

# Step 4: Call the model without a parser
formatted_prompt = prompt.invoke({
    "topic": "Machine Learning"
})

raw_response = model.invoke(formatted_prompt)

print("WITHOUT OUTPUT PARSER")
print("Response type:", type(raw_response))
print("Response content:", raw_response.content)

# Step 5: Create a string output parser
parser = StrOutputParser()

# Step 6: Connect components using LCEL
chain = prompt | model | parser

# Step 7: Execute the complete chain
result = str(chain.invoke({
    "topic": "Machine Learning"
}))

print("\nWITH OUTPUT PARSER")
print("Response type:", type(result))
print("Response:", result)

# Step 8: Demonstrate string operations
print("\nSTRING OPERATIONS")
print("Characters:", len(result))
print("Uppercase:", result.upper())
