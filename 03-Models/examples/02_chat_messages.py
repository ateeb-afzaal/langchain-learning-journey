
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

messages = [
    SystemMessage(
        content="You are an expert Python teacher. Explain concepts simply."
    ),
    HumanMessage(
        content="What is object-oriented programming?"
    )
]

response = model.invoke(messages)

print(response.content)
