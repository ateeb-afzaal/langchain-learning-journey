
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load the GROQ_API_KEY from .env
load_dotenv()

# Initialize the chat model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Send a question to the model
response = model.invoke(
    "What is LangChain? Explain in simple words."
)

# Print the response and its type
print("Response:", response.content)
print("Response type:", type(response))
