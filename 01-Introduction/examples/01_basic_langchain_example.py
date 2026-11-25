
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()

# Check if Groq API key is available
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is missing")

# Initialize Groq chat model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Send a question to the model
response = model.invoke(
    "What is LangChain? Explain in two simple sentences."
)

# Display the generated answer
print(response.content)
