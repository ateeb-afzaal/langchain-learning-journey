# 02 — Chat Models in LangChain

## 1. What Is a Chat Model?

A chat model is a language model interface designed to handle conversations using structured messages.

Instead of treating everything as one plain-text prompt, chat models can distinguish between system instructions, user messages, and AI responses.

**Example conversation:**

```text
System: You are a helpful Python teacher.
Human: What is a Python list?
AI: A list is an ordered, mutable collection in Python.
Human: Can you give me an example?
AI: Yes! fruits = ["apple", "banana", "mango"]
```

## 2. Why Do We Use Chat Models?

Chat models are useful because they support:

- Role-based instructions
- Multi-turn conversations
- Structured message history
- Model parameters
- Integration with tools and agents

**Important:** Chat models do not automatically remember previous conversations. The application must provide earlier messages or use a system that maintains conversation history.

## 3. Message Types in LangChain

LangChain represents chat messages using different classes.

### SystemMessage

Defines instructions about the assistant's behavior.

```python
from langchain_core.messages import SystemMessage

message = SystemMessage(
    content="You are a helpful Python teacher."
)
```

### HumanMessage

Represents a message from the user.

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content="Explain Python functions."
)
```

### AIMessage

Represents a response from the assistant.

```python
from langchain_core.messages import AIMessage

message = AIMessage(
    content="A function is a reusable block of code."
)
```

### Comparison

| Message Type    | Purpose                   |
| --------------- | ------------------------- |
| `SystemMessage` | Instructions to the model |
| `HumanMessage`  | User input                |
| `AIMessage`     | Assistant response        |

Other message types, such as `ToolMessage`, are used when working with tools and agents.

## 4. Using ChatGroq with LangChain

In this learning journey, we use Groq to access GPT-OSS 120B.

**Example:**

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

response = model.invoke(
    "Explain Python decorators in simple words."
)

print(response.content)
```

### Code Explanation

- `load_dotenv()` loads environment variables.
- `ChatGroq` creates a chat model instance.
- `model` selects the hosted GPT-OSS 120B model.
- `invoke()` sends a request to the model.
- `response.content` returns the generated content.

The environment must contain a valid `GROQ_API_KEY`.

## 5. Sending System and Human Messages

We can provide multiple messages in one request.

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(
        content="You are a Python teacher. Use simple examples."
    ),
    HumanMessage(
        content="What is a dictionary in Python?"
    )
]

response = model.invoke(messages)

print(response.content)
```

### How It Works

1. The system message defines the assistant's role.
2. The human message contains the actual question.
3. The model processes both messages.
4. It generates an AI response.

## 6. Conversation History

Suppose we want the model to remember a name mentioned earlier.

```python
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My name is Ali."),
    AIMessage(content="Nice to meet you, Ali!"),
    HumanMessage(content="What is my name?")
]

response = model.invoke(messages)

print(response.content)
```

**Expected answer:** The model should identify the name as Ali.

### Important Point

The model knows the name because we included the earlier messages.

If we send only:

```python
model.invoke("What is my name?")
```

the model would not automatically have that previous context.

## 7. How to Build a Simple Multi-Turn Conversation

We can store the conversation in a Python list.

```python
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

history = [
    SystemMessage(content="You are a helpful Python teacher.")
]

while True:
    question = input("You: ").strip()

    if question.lower() in {"exit", "quit"}:
        break

    history.append(HumanMessage(content=question))

    response = model.invoke(history)

    print("AI:", response.content)

    history.append(response)
```

### Explanation

- `history` stores previous messages.
- `HumanMessage` adds the latest question.
- `model.invoke(history)` sends the conversation.
- The generated response is added to history.
- Future requests include previous messages.

This example keeps history in memory while the Python process runs. It does not save conversations permanently.

## 8. Model Parameters

### Temperature

Temperature influences variation in generated responses.

```python
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

Lower temperature generally requests more consistent output.

### Maximum Tokens

This limits the number of tokens the model can generate.

```python
model = ChatGroq(
    model="openai/gpt-oss-120b",
    max_tokens=150
)
```

The parameter must be supported by the chosen provider and model.

### Other Parameters

Some chat model integrations support:

- `timeout` — How long a request can take.
- `max_retries` — How many times certain failed requests may be retried.
- `streaming` — Receiving the response in chunks.

Available parameters vary by integration.

## 9. Understanding the AI Response

When we call:

```python
response = model.invoke("Hello!")
```

LangChain normally returns an `AIMessage`.

We can inspect:

```python
print(type(response))
print(response.content)
print(response.response_metadata)
```

### What Do These Mean?

**`type(response)`**

Shows the Python type of the returned object.

**`response.content`**

Contains the response content.

**`response.response_metadata`**

May contain provider-specific metadata, such as model information, token usage, or finish reasons.

The metadata fields depend on the provider.

## 10. Practical Applications

Chat models are used in:

- AI assistants
- Customer support chatbots
- Learning assistants
- Programming assistants
- Conversational RAG systems
- Tool-using AI agents

## 11. Quick Revision Questions

**Q1. What is a chat model?**

A model interface that handles structured conversational messages.

**Q2. What does `SystemMessage` do?**

It provides instructions about the assistant's role or behavior.

**Q3. What does `HumanMessage` represent?**

A message from the user.

**Q4. What does `AIMessage` represent?**

A response from the assistant.

**Q5. Does a chat model automatically remember earlier conversations?**

No. Earlier context must be supplied or maintained by the application.

**Q6. What does `model.invoke()` do?**

It sends input to the model and returns a response.

**Q7. What is temperature?**

A model setting that influences response variation.

**Q8. Why do we store message history?**

To make earlier conversation context available in later requests.

## 12. Key Takeaways

- Chat models work with structured conversational messages.
- `SystemMessage`, `HumanMessage`, and `AIMessage` represent different roles.
- LangChain's `ChatGroq` connects Python applications to Groq.
- `invoke()` sends input and returns a model response.
- Message history helps maintain conversational context.
- Model parameters influence generation behavior.
- The model does not automatically remember previous calls.

---

## Learning Resources

- [CampusX LangChain Models](https://github.com/campusx-official/langchain-models)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 03 — Topic 02
