# 05 — LangChain Models: Quick Revision

## 1. Core Concepts

| Concept             | Simple Explanation                                                 |
| ------------------- | ------------------------------------------------------------------ |
| LLM                 | A large model trained to process and generate language             |
| Chat Model          | A model interface that works with structured conversation messages |
| Embedding Model     | Converts text into numerical vectors                               |
| Token               | A unit of text processed by a model                                |
| Inference           | Using a trained model to produce an output                         |
| Temperature         | A setting that influences response variation                       |
| Context Window      | The amount of token-based context a model can process              |
| Open-Weight Model   | A model with downloadable trained weights                          |
| Quantization        | Reducing numerical precision to improve efficiency                 |
| Semantic Similarity | Measuring how closely related two inputs are in meaning            |

## 2. Important Comparisons

### Language Models vs Embedding Models

| Language Model                       | Embedding Model              |
| ------------------------------------ | ---------------------------- |
| Generates text                       | Generates numerical vectors  |
| Used in chatbots and text generation | Used in search and retrieval |
| Example: GPT-OSS 120B                | Example: all-MiniLM-L6-v2    |

### Hosted vs Local Models

| Hosted Inference                | Local Inference                      |
| ------------------------------- | ------------------------------------ |
| Runs on provider infrastructure | Runs on your own hardware            |
| Usually requires internet       | Can run offline after setup          |
| Provider manages infrastructure | Developer manages infrastructure     |
| Example: Groq API               | Example: local Transformers pipeline |

## 3. Important LangChain Classes and Methods

| Class or Method         | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| `ChatGroq`              | Connect to a Groq-hosted chat model           |
| `SystemMessage`         | Provide assistant instructions                |
| `HumanMessage`          | Represent user input                          |
| `AIMessage`             | Represent an assistant response               |
| `model.invoke()`        | Invoke a model                                |
| `response.content`      | Access generated response content             |
| `HuggingFaceEmbeddings` | Load a supported Hugging Face embedding model |
| `embed_query()`         | Generate one query embedding                  |
| `embed_documents()`     | Generate embeddings for multiple documents    |

## 4. Important Code Snippets

### Chat Model

```python
from langchain_groq import ChatGroq

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

response = model.invoke("What is Python?")
print(response.content)
```

Requires `GROQ_API_KEY` to be configured.

### Embedding Model

```python
from langchain_huggingface import HuggingFaceEmbeddings

model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = model.embed_query("What is LangChain?")

print(len(vector))
```

Expected vector length: 384.

## 5. Interview Questions

**Q1. What is the difference between an LLM and a chat model?**

An LLM describes a language model, while a chat model refers to an interface that processes structured conversational messages.

**Q2. What is the difference between `SystemMessage` and `HumanMessage`?**

A system message provides instructions, while a human message represents user input.

**Q3. Does a chat model automatically remember previous conversations?**

No. The application must provide previous messages or maintain conversation state.

**Q4. What is an embedding?**

A numerical representation of text or other information.

**Q5. Why are embeddings important?**

They enable semantic comparison, retrieval, clustering, and related applications.

**Q6. What is cosine similarity?**

A mathematical measure of the angle between two nonzero vectors.

**Q7. What is the difference between hosted and local inference?**

Hosted inference runs on external infrastructure, while local inference runs on the user's own hardware.

**Q8. What is quantization?**

Reducing numerical precision to lower memory or computational requirements.

**Q9. What is Hugging Face?**

An ecosystem offering AI models, datasets, libraries, and model-sharing tools.

**Q10. Why are embeddings useful in RAG?**

They help retrieve relevant information that can be provided to a language model as context.

## 6. Practical Test Results

### Conversation History

Tested a chatbot using `ChatGroq` with conversation history.

```text
You: My name is Ateeb.
AI: Nice to meet you, Ateeb!

You: What is my name?
AI: Your name is Ateeb.
```

Result: Conversation history successfully provided previous context to the model.

### Semantic Similarity

Model: `sentence-transformers/all-MiniLM-L6-v2`

```text
Python vs Python: 0.8686
Python vs Pizza: 0.2902
```

Result: The two Python-related sentences received a higher cosine similarity score.

## 7. Key Takeaways

- Language models generate text and conversational responses.
- Chat models support structured messages and roles.
- Open-weight models can be deployed locally when hardware and licensing permit.
- Hugging Face provides tools for working with AI models.
- Embedding models convert text into numerical vectors.
- Similar meaning often results in higher vector similarity.
- Combining language and embedding models is fundamental to RAG applications.

---

**Course:** CampusX LangChain

**Learning Journey:** Section 03 of 18

**Status:** Notes and embedding/conversation-history examples completed.
