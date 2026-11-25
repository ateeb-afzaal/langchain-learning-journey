
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import HumanMessage

# Step 1: Load Groq API key
load_dotenv()

# Step 2: Initialize the chat model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Step 3: Create a prompt with a history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Python learning assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# Step 4: Connect the prompt to the model
chain = prompt | model

# Step 5: Store previous messages
history = []

print("Chatbot started! Type 'exit' to quit.\n")

# Step 6: Start the conversation
while True:
    question = input("You: ").strip()

    if question.lower() in {"exit", "quit"}:
        break

    if not question:
        continue

    try:
        # Insert previous messages and the new question
        response = chain.invoke({
            "history": history,
            "question": question
        })
    except Exception as error:
        print("Request failed:", error)
        continue

    print("\nAI:", response.content, "\n")

    # Save the exchange for future requests
    history.append(HumanMessage(content=question))
    history.append(response)
