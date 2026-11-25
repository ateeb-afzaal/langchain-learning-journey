
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# Load the API key from .env
load_dotenv()

# Initialize Groq
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Create a dynamic chat prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an experienced {subject} teacher. "
        "Explain concepts in simple English."
    ),
    (
        "human",
        "Explain {topic} to a beginner with one practical example."
    )
])

# Inspect formatted messages
formatted = prompt.invoke({
    "subject": "Python",
    "topic": "Decorators"
})

print("Formatted messages:")
for message in formatted.to_messages():
    print(f"{message.type}: {message.content}")

# Connect prompt, model, and parser
chain = prompt | model | StrOutputParser()

# Invoke the complete chain
response = chain.invoke({
    "subject": "Python",
    "topic": "Decorators"
})

print("\nAI Response:")
print(response)
