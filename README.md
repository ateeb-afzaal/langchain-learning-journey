# LangChain Learning Journey 🤖

Welcome to my **LangChain Learning Journey** repository!

This repository documents my journey of learning **LangChain, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Tool Calling, and AI Agents** using Python.

The goal is to build a strong understanding of Generative AI application development through simple notes, practical Python examples, and hands-on projects.

## 🎯 Learning Objectives

- Understand LangChain and its core components.
- Learn how to work with LLMs and chat models.
- Build reusable prompts and chains.
- Understand structured outputs and output parsers.
- Work with document loaders, text splitters, and embeddings.
- Learn vector stores, semantic search, and retrievers.
- Build RAG-based applications.
- Create custom tools and tool-calling workflows.
- Develop AI agents that interact with external APIs.

## 🛠️ Technologies Used

- **Programming:** Python
- **Framework:** LangChain
- **LLM Provider:** Groq
- **LLM:** GPT-OSS 120B
- **Embeddings:** Hugging Face Sentence Transformers
- **Vector Stores:** FAISS, Chroma
- **Environment:** Google Colab, VS Code
- **Libraries:** LangChain Core, Pydantic, Requests, DDGS

## 📚 Learning Roadmap

This repository follows the CampusX LangChain playlist.

| No. | Topic | Main Concepts |
|---|---|---|
| 01 | Introduction to LangChain | Introduction, benefits, alternatives |
| 02 | LangChain Components | Models, prompts, chains, indexes, memory, agents |
| 03 | Models | LLMs, chat models, embedding models |
| 04 | Prompts | PromptTemplate, ChatPromptTemplate, messages |
| 05 | Structured Output | TypedDict, Pydantic, JSON Schema |
| 06 | Output Parsers | String, JSON, Pydantic output parsers |
| 07 | Chains | Simple, sequential, parallel, conditional |
| 08 | Runnables | Runnable interface, invoke, batch, stream |
| 09 | LCEL | RunnableSequence, Parallel, Lambda, Branch, Passthrough |
| 10 | Document Loaders | Text, PDF, directory, web, CSV |
| 11 | Text Splitters | Character, recursive, semantic splitting |
| 12 | Vector Stores | Embeddings, FAISS, Chroma |
| 13 | Retrievers | Similarity search, MMR, multi-query retrieval |
| 14 | RAG Fundamentals | Indexing, retrieval, augmentation, generation |
| 15 | RAG Using LangChain | End-to-end YouTube RAG application |
| 16 | Tools | Built-in tools, custom tools, schemas |
| 17 | Tool Calling | Tool binding, execution, currency conversion |
| 18 | AI Agents | ReAct, agent execution, tool orchestration |

Each section will contain beginner-friendly notes, commented code examples, and practical exercises.

## 🚀 Hands-On Projects

### 1. Multi-Tool AI Agent

An AI assistant built using **LangChain and Groq** that can select and execute different Python tools based on a user's question.

**Features:**
- Mathematical calculations
- Web search
- Currency exchange-rate lookup
- Currency conversion
- Current weather information
- AI-driven tool selection and execution

**Technologies:** Python, LangChain, Groq, DDGS, Requests, Frankfurter API, Open-Meteo API.

### 2. YouTube RAG Chatbot

A Retrieval-Augmented Generation application that answers questions using information extracted from YouTube video transcripts.

**Features:**
- YouTube transcript extraction
- Text splitting and chunking
- Hugging Face embeddings
- FAISS vector storage
- Similarity-based retrieval
- Context-based answer generation using Groq

## 📂 Repository Organization

Each numbered learning section will be organized into:

- `notes/` — Concepts and explanations in simple English.
- `examples/` — Practical Python code with comments.
- `README.md` — Topic overview and learning references.

The `projects/` directory will contain complete practical implementations and their documentation.

## 🔐 API Key Security

This repository does not include private API keys.

API keys must be stored using environment variables, `.env` files excluded from Git, or Google Colab Secrets.

## 📖 Learning Resources

**CampusX LangChain Playlist:**

https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0

**Official LangChain Documentation:**

https://docs.langchain.com/

**CampusX GitHub:**

https://github.com/campusx-official

The learning materials are based on CampusX tutorials, with independently written explanations and examples adapted for my Python and Groq environment.

## 🎯 Future Goals

- Strengthen my understanding of RAG and AI agents.
- Build more advanced multi-tool assistants.
- Integrate LangChain with FastAPI and PostgreSQL.
- Learn LangGraph for stateful agent workflows.
- Apply these concepts in practical AI engineering projects.

---

**Learning by understanding, coding, experimenting, and building real AI applications.**
