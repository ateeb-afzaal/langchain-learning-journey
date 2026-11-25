
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Load the Groq API key
load_dotenv()

# Initialize the model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Create a reusable prompt template
prompt = PromptTemplate.from_template(
    """
    You are an experienced Python teacher.

    Explain {topic} to a {level} student.

    Requirements:
    - Use simple English.
    - Include one practical example.
    - Keep the explanation concise.
    """
)

# Display the required variables
print("Required variables:", prompt.input_variables)

# Format the prompt without calling the model
formatted = prompt.format(
    topic="Python decorators",
    level="beginner"
)

print("\nFormatted Prompt:\n")
print(formatted)

# Connect prompt, model and output parser
chain = prompt | model | StrOutputParser()

# Invoke the complete chain
response = chain.invoke({
    "topic": "Python decorators",
    "level": "beginner"
})

print("\nAI Response:\n")
print(response)
