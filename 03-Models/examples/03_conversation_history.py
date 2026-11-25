
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Start a conversation with system instructions
history = [
    SystemMessage(content="You are a helpful AI assistant.")
]

print("Chat started! Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    history.append(HumanMessage(content=question))

    try:
        response = model.invoke(history)
    except Exception as error:
        history.pop()
        print("Request failed:", error)
        continue

    print("AI:", response.content)

    # Save the AI response so the next request has context
    history.append(response)
