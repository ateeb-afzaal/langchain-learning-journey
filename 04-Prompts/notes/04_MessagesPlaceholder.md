# 04 — MessagesPlaceholder in LangChain

## 1. What Is MessagesPlaceholder?

`MessagesPlaceholder` is a LangChain component that allows us to insert a list of chat messages into a `ChatPromptTemplate`.

It is commonly used to include previous conversations in a new model request.

**Simple idea:** Instead of manually writing every previous message into a prompt, we provide conversation history through a variable.

## 2. Why Do We Need It?

Imagine this conversation:

```text
User: My name is Ali.
AI: Nice to meet you, Ali.
User: What is my name?
```

To answer the final question, the model needs the earlier messages.

`MessagesPlaceholder` helps us include those messages in the prompt.

**Important:** It does not store conversation history by itself. Our application must maintain the messages.

## 3. Basic Syntax

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])
```

### Explanation

- `ChatPromptTemplate` creates the structured prompt.
- `MessagesPlaceholder` identifies where conversation history should be inserted.
- `variable_name="history"` names the input variable.
- `{question}` contains the latest user question.

## 4. Passing Conversation History

```python
from langchain_core.messages import HumanMessage, AIMessage

history = [
    HumanMessage(content="My name is Ali."),
    AIMessage(content="Nice to meet you, Ali!")
]

formatted_prompt = prompt.invoke({
    "history": history,
    "question": "What is my name?"
})

for message in formatted_prompt.to_messages():
    print(message.type, ":", message.content)
```

The formatted prompt contains the system instructions, previous conversation, and latest question.

## 5. Using MessagesPlaceholder with Groq

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

history = [
    ("human", "My name is Ali."),
    ("ai", "Nice to meet you, Ali!")
]

chain = prompt | model

response = chain.invoke({
    "history": history,
    "question": "What is my name?"
})

print(response.content)
```

**Expected behavior:** The model identifies the name as Ali because it receives the previous messages.

## 6. Building a Multi-Turn Chatbot

We can continuously update the history after each response.

```python
from langchain_core.messages import HumanMessage

history = []

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        break

    response = chain.invoke({
        "history": history,
        "question": question
    })

    print("AI:", response.content)

    history.append(HumanMessage(content=question))
    history.append(response)
```

After every successful request, we save the user's question and the AI's response.

The next request receives both through `MessagesPlaceholder`.

## 7. Optional Conversation History

Sometimes an application has no previous messages.

We can make the placeholder optional:

```python
MessagesPlaceholder(
    variable_name="history",
    optional=True
)
```

Then the prompt can work even when `history` is omitted.

## 8. Limiting Conversation History

Long conversations can use many tokens.

We can limit the number of inserted messages:

```python
MessagesPlaceholder(
    variable_name="history",
    n_messages=4
)
```

This includes at most the four most recent messages from the supplied history.

**Important:** This does not delete earlier messages from the original history list.

## 9. MessagesPlaceholder vs Memory

| MessagesPlaceholder            | Conversation Memory                           |
| ------------------------------ | --------------------------------------------- |
| Inserts messages into a prompt | Stores or manages conversation information    |
| Does not save messages         | Application-managed storage retains messages  |
| Works with ChatPromptTemplate  | Can use lists, databases, or persistent state |
| Controls where history appears | Controls what history is available            |

## 10. Common Beginner Mistakes

**Mistake 1 — Thinking MessagesPlaceholder remembers messages automatically**

It only inserts the history we provide.

**Mistake 2 — Forgetting to update history**

If the application does not save new user and AI messages, later requests won't include them.

**Mistake 3 — Using the wrong variable name**

The value passed to `history` must match `variable_name="history"`.

**Mistake 4 — Sending unlimited conversation history**

Long histories increase token usage and can exceed a model's context limits.

## 11. Interview Questions

**Q1. What is MessagesPlaceholder?**

A LangChain prompt component that inserts a list of chat messages into a chat prompt.

**Q2. Does MessagesPlaceholder store history?**

No. The application must maintain the history.

**Q3. Why is it useful?**

It allows reusable chat prompts to include previous conversation messages.

**Q4. What does optional=True do?**

Allows the prompt to work without supplying the history variable.

**Q5. What does n_messages do?**

Limits the number of recent history messages inserted into the prompt.

## 12. Key Takeaways

- `MessagesPlaceholder` inserts existing chat messages into a prompt.
- It is used with `ChatPromptTemplate`.
- Conversation history must be stored separately.
- The application updates history after successful responses.
- `optional=True` allows an empty or missing history.
- `n_messages` can limit how much history is included.
- This component is useful for building conversational LangChain applications.

---

## Learning Resources

- [CampusX LangChain Prompts](https://github.com/campusx-official/langchain-prompts)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 04 — Topic 04
