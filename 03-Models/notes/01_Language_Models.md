# 01 — Language Models in LangChain

## 1. What Is a Language Model?

A language model is an AI model trained to understand patterns in language and generate text.

A **Large Language Model (LLM)** is a language model with a large number of learned parameters, trained on substantial amounts of data.

Examples of LLM families include GPT, Llama, Gemma, and Qwen.

In simple words, an LLM takes text as input and generates text as output.

**Example:**

Input:

```text
Explain machine learning in simple words.
```

Possible output:

```text
Machine learning is a technology that allows computers to learn
patterns from data and make predictions.
```

## 2. How Does an LLM Work?

At a basic level, a generative language model predicts the next token based on the tokens it has already received.

For example:

```text
The capital of Pakistan is _____
```

The model might predict:

```text
Islamabad
```

It continues generating tokens until the response is complete or a stopping condition is reached.

Although models learn by predicting tokens, their training allows them to perform tasks such as answering questions, summarizing, translating, and writing code.

## 3. What Are Tokens?

Tokens are the units of text processed by language models.

A token can represent a word, part of a word, punctuation, or another piece of text.

For example:

```text
I love Python programming.
```

A tokenizer divides this sentence into tokens according to its vocabulary.

The exact token count depends on the model's tokenizer.

### Why Are Tokens Important?

Tokens affect:

- How much information a model can process at once.
- The length of generated answers.
- API usage and pricing.
- Response time.

**Context Window:** The maximum amount of token-based context a model can process in a request, subject to the provider's limits.

## 4. Types of Language Model Interfaces

### A. Text Completion Models

Traditional text completion models receive text and generate a continuation.

Example:

```text
Input: Python is a programming language used for

Output: web development, automation, data analysis, and AI.
```

Historically, LangChain used the `LLM` interface for these text-in/text-out models.

### B. Chat Models

Chat models are designed to process structured messages, often including different roles.

Example:

```text
System: You are a helpful Python teacher.
Human: Explain a Python list.
AI: A Python list is an ordered, mutable collection.
```

LangChain provides chat model integrations such as `ChatGroq`.

Today, many modern LLMs are accessed through chat interfaces rather than traditional completion interfaces.

## 5. LLMs vs Chat Models

| Feature           | Traditional LLM Interface            | Chat Model Interface                        |
| ----------------- | ------------------------------------ | ------------------------------------------- |
| Input             | Text prompt                          | Structured messages or text                 |
| Output            | Generated text                       | AI message                                  |
| Roles             | Not inherently structured            | Supports roles                              |
| Conversations     | History must be formatted manually   | Message history can be supplied as messages |
| LangChain example | Legacy/completion model integrations | `ChatGroq`                                  |

**Important:** An LLM and a chat model are not necessarily different underlying technologies. The distinction often refers to the way a model is accessed and how inputs and outputs are represented.

## 6. Language Models vs Embedding Models

Both belong to the broader AI model ecosystem, but they serve different purposes.

### Language Model

Generates language.

```text
Input: What is Python?
Output: Python is a high-level programming language.
```

### Embedding Model

Converts text into a numerical vector.

```text
Input: What is Python?
Output: [0.12, -0.43, 0.28, ...]
```

The numerical values can be used for semantic similarity and retrieval.

We will study embedding models in detail in `04_Embedding_Models.md`.

## 7. Important LLM Concepts

### Parameters

Parameters are learned numerical values within a model.

For example, a model described as having 120 billion parameters has approximately 120 billion learned parameters.

### Training

During training, the model learns language patterns from data.

### Inference

Inference is the process of using a trained model to generate an output.

When we call a model through Groq, we are performing inference.

### Temperature

Temperature is a generation setting that influences how the model selects tokens.

- Lower values generally produce more consistent responses.
- Higher values generally introduce more variation.

The supported range and behavior depend on the model and provider.

### Hallucination

A hallucination occurs when a model generates incorrect or unsupported information.

LLM responses should be checked when accuracy matters.

## 8. Using an LLM Through LangChain and Groq

For this learning journey, we use Groq to access a hosted GPT-OSS model.

```python
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

response = model.invoke(
    "Explain what a Large Language Model is in simple words."
)

print(response.content)
```

### Code Explanation

**`load_dotenv()`**

Loads environment variables from our local `.env` file.

**`ChatGroq(...)`**

Creates a LangChain chat model connected to Groq.

**`temperature=0`**

Requests low-variation generation where supported.

**`model.invoke(...)`**

Sends input to the model and returns its response.

**`response.content`**

Accesses the generated content.

The Groq API key must be configured as `GROQ_API_KEY` in the environment.

## 9. Real-World Applications

Language models are commonly used for:

- AI assistants
- Customer support
- Text summarization
- Code generation
- Translation
- Content classification
- Question answering

## 10. Quick Revision Questions

**Q1. What is an LLM?**

A large language model trained to process and generate language.

**Q2. What is a token?**

A unit of text processed by a language model.

**Q3. What is inference?**

Using a trained model to generate an output.

**Q4. What is the main difference between language models and embedding models?**

Language models generate language, while embedding models produce numerical representations.

**Q5. What is temperature?**

A generation setting that influences variation in model output.

**Q6. Can language models produce incorrect answers?**

Yes. They can hallucinate or generate unsupported information.

## Key Takeaways

- LLMs learn patterns in language through training.
- Generative LLMs produce responses token by token.
- Tokens determine how text is processed.
- Chat models accept structured messages.
- Embedding models produce numerical vectors.
- LangChain provides interfaces for working with different models.
- Groq provides hosted inference for our GPT-OSS 120B examples.

---

**Learning Reference:** CampusX — LangChain Models

[CampusX Models Repository](https://github.com/campusx-official/langchain-models)
