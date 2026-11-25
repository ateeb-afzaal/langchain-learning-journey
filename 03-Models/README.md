# 03 — LangChain Models

## Overview

Models are one of the fundamental components of LangChain. They allow developers to connect Python applications with AI models for generating responses, understanding language, and creating numerical representations of text.

In this section, I will learn how to use language models, chat models, open-source models, and embedding models through LangChain.

I will use **Groq GPT-OSS 120B** for chat model examples and **Hugging Face** for embedding model examples.

## Topics Covered

### 1. Language Models

- What are Large Language Models (LLMs)?
- Difference between traditional LLMs and chat models
- How language models process input and generate responses
- Basic model invocation using LangChain

### 2. Chat Models

- What are chat models?
- Using `ChatGroq` with LangChain
- System, Human, and AI messages
- Model parameters such as temperature and maximum output tokens
- Sending messages and receiving model responses

### 3. Open-Source Models

- Open-source and proprietary AI models
- Hugging Face model ecosystem
- Hosted inference versus local inference
- Advantages and limitations of different deployment approaches

### 4. Embedding Models

- What are text embeddings?
- Converting text into numerical vectors
- Semantic similarity
- Hugging Face embedding models
- How embeddings support vector search and RAG

### 5. Quick Revision

- Important definitions
- Comparison tables
- Interview questions
- Key takeaways

## Learning Objectives

By the end of this section, I should be able to:

1. Explain the difference between LLMs, chat models, and embedding models.
2. Connect a Groq-hosted model to LangChain.
3. Use system and human messages to interact with a chat model.
4. Understand how temperature affects model output.
5. Explain hosted and locally running models.
6. Generate text embeddings using Hugging Face.
7. Understand why embedding models are important for semantic search and RAG.

## Repository Structure

```text
03-Models/
├── README.md
├── notes/
│   ├── 01_Language_Models.md
│   ├── 02_Chat_Models.md
│   ├── 03_Open_Source_Models.md
│   ├── 04_Embedding_Models.md
│   └── 05_Quick_Revision.md
└── examples/
    └── Python examples will be added here
```

## Tools and Technologies

| Technology     | Purpose                                 |
| -------------- | --------------------------------------- |
| Python         | Programming language                    |
| LangChain      | Framework for building LLM applications |
| Groq           | Hosted model inference                  |
| GPT-OSS 120B   | Chat model                              |
| Hugging Face   | Model ecosystem and embedding models    |
| VS Code        | Development environment                 |
| Git and GitHub | Version control                         |

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [CampusX LangChain Models Repository](https://github.com/campusx-official/langchain-models)
- [LangChain Documentation](https://docs.langchain.com/)

## Progress Checklist

- [ ] Language Models
- [ ] Chat Models
- [ ] Open-Source Models
- [ ] Embedding Models
- [ ] Quick Revision
- [ ] Practical Python Examples

## Key Goal

Understand how LangChain connects to different types of AI models and learn how to use those models in real Python applications.

---

**Learning Journey:** Section 03 of 18

**Reference:** CampusX — LangChain Models.
