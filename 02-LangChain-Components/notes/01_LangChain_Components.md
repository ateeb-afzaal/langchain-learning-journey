# LangChain Components — Complete Study Notes

## 1. Introduction

LangChain provides different components that help developers create applications powered by Large Language Models (LLMs).

Instead of building every feature from scratch, we can combine these components to create AI applications.

The CampusX course introduces six major components:

1. Models
2. Prompts
3. Chains
4. Indexes
5. Memory
6. Agents

---

## 2. Models

### What is a Model?

A model is the AI system that processes our input and produces an output.

LangChain provides interfaces for connecting our applications to different AI models.

### Main Types

**Language Models**

These understand and generate natural language.

Examples include chat models used for answering questions, writing explanations, and having conversations.

**Embedding Models**

These convert text into numerical vectors so that applications can compare the meaning of different texts.

### Simple Example

```python
from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-120b")

response = model.invoke("What is Python?")

print(response.content)
```

### Explanation

- `ChatGroq` connects LangChain to Groq.
- `model` holds our configured chat model.
- `invoke()` sends the question to the model.
- `response.content` contains the generated answer.

**Remember:** Language models generate text, whereas embedding models generate numerical representations.

---

## 3. Prompts

### What is a Prompt?

A prompt is an instruction or question given to an AI model.

For example:

"Explain Python in simple words."

### Why Are Prompts Important?

They help us control what task the model performs and how the answer should be written.

### Important Prompt Features

**Dynamic Prompts**

Instead of writing a new prompt every time, we can use variables.

**Role-Based Prompts**

We can provide system instructions and user messages.

**Few-Shot Prompting**

We can provide examples to show the model the expected response style.

### Example

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Explain {topic} in simple words.",
    input_variables=["topic"]
)

result = prompt.invoke({"topic": "Machine Learning"})

print(result.to_string())
```

### Explanation

- `{topic}` is a placeholder.
- `input_variables` identifies the required variable.
- `invoke()` inserts the supplied topic.

The resulting prompt can then be sent to a language model.

**Remember:** A prompt tells the model what to do.

---

## 4. Chains

### What is a Chain?

A chain connects multiple processing steps together.

The output of one step can become the input of another.

### Why Do We Need Chains?

Sometimes an AI application requires several operations rather than a single model call.

For example:

1. Prepare a prompt.
2. Send it to a model.
3. Extract the response text.

### Example

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template(
    "Give 3 facts about {topic}"
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({"topic": "Python"})

print(result)
```

This example assumes `model` was already initialized.

### Explanation

- `prompt` prepares the instructions.
- `model` generates the response.
- `parser` extracts the text.
- `|` connects the components.
- `chain.invoke()` runs the workflow.

### Types of Chains

- Simple chains
- Sequential chains
- Parallel chains
- Conditional chains

**Remember:** A chain connects steps into a workflow.

---

## 5. Indexes

### What Are Indexes?

In the instructor's course, indexes refer to the components and processes used to organize external knowledge so an application can search it efficiently.

### Why Do We Need Them?

An LLM does not automatically know the contents of our private documents.

For example, imagine a company has 500 PDF files.

We can prepare these documents for searching through the following process:

1. Load the documents.
2. Divide the text into smaller chunks.
3. Generate embeddings.
4. Store the embeddings in a vector store.
5. Retrieve relevant chunks when a user asks a question.

### Example

A user asks:

"What is the company's leave policy?"

The application retrieves the relevant policy text and passes it to the language model.

This is part of a Retrieval-Augmented Generation (RAG) system.

### Important Related Components

- Document Loaders
- Text Splitters
- Embedding Models
- Vector Stores
- Retrievers

**Remember:** Indexing makes external information easier to retrieve.

---

## 6. Memory

### What Is Memory?

LLM API requests do not automatically remember previous conversations.

Applications need a way to preserve and provide relevant conversation history.

### Why Do We Need Memory?

Imagine this conversation:

User: "My name is Ali."

AI: "Hello, Ali."

User: "What is my name?"

If the application sends only the final question, the model may not know the user's name.

If it also sends previous messages, the model can use that information.

### Common Memory Approaches

**Conversation Buffer**

Stores messages from the conversation.

**Window-Based History**

Keeps only a limited number of recent messages.

**Summarized History**

Summarizes older messages to reduce the amount of context.

**Custom Memory**

Stores useful application-specific information.

### Important Note

The CampusX notes describe historical memory classes such as `ConversationBufferMemory`.

Modern LangChain applications can manage message history and persistent agent state through newer APIs. We will distinguish older examples from current implementations in later sections.

**Remember:** Memory is how an application retains and reuses conversation context.

---

## 7. Agents

### What Is an AI Agent?

An AI agent uses a language model to decide which tools or actions are needed to complete a task.

### Why Do We Need Agents?

A normal language model primarily generates responses.

However, users may ask questions requiring external actions, such as:

- Searching the internet.
- Calculating numbers.
- Retrieving weather.
- Calling a currency exchange API.

An agent can decide which available tool to use.

### Simple Example

User asks:

"What is 25 multiplied by 8?"

The agent can:

1. Understand the question.
2. Select the multiplication tool.
3. Provide `a=25` and `b=8`.
4. Receive the result `200`.
5. Generate the final answer.

### Agent vs Chain

| Chain | Agent |
|---|---|
| Usually follows a predefined workflow | Can decide which available action to take |
| Steps are connected in advance | Tool selection depends on the request |
| Good for predictable processing | Good for dynamic, tool-using tasks |

**Remember:** An agent uses a model to decide what action to take.

---

## 8. How the Components Work Together

Imagine building an AI assistant that answers questions from uploaded documents.

**Step 1 — Document Loading**

Read the uploaded documents.

**Step 2 — Indexing**

Split documents into chunks, create embeddings, and store them.

**Step 3 — Retrieval**

Find relevant information for the question.

**Step 4 — Prompt**

Combine the user's question with the retrieved information.

**Step 5 — Model**

Generate an answer using the provided context.

**Step 6 — Memory**

Provide useful previous messages when necessary.

**Step 7 — Agent (Optional)**

Select external tools when the task requires additional actions.

Not every LangChain application needs all six components.

---

## 9. Quick Revision Questions

**Q1. What are the six main components introduced in the course?**

Models, Prompts, Chains, Indexes, Memory, and Agents.

**Q2. What is the purpose of Models?**

To process inputs and generate language or numerical representations.

**Q3. What is a Prompt?**

An instruction given to an AI model.

**Q4. What is a Chain?**

A sequence or combination of connected processing steps.

**Q5. Why do we need Indexes?**

To organize external information so we can retrieve relevant content efficiently.

**Q6. Why do we need Memory?**

To preserve information from earlier interactions.

**Q7. What makes an Agent different from a simple Chain?**

An agent can dynamically choose tools or actions based on the request.

**Q8. Does every LangChain application need an Agent?**

No. Many applications work well with simple chains or retrieval pipelines.

---

## 10. Key Takeaways

- Models process information.
- Prompts provide instructions.
- Chains connect operations.
- Indexes help organize external knowledge.
- Memory preserves useful conversation context.
- Agents dynamically select tools and actions.

These components form the foundation for building more advanced applications such as RAG systems, document assistants, and tool-using AI agents.

---

### Learning Reference

CampusX — LangChain Components (Video 2).

Based on the instructor's course notes, rewritten in simple English with Groq-based examples.

https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0