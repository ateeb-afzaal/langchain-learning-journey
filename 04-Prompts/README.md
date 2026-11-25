# 04 — Prompts in LangChain

## Overview

Prompts are one of the most important components of LangChain. They define the instructions and information sent to a language model.

LangChain provides prompt templates that help developers create reusable, dynamic, and structured prompts instead of manually writing the same instructions repeatedly.

In this section, I will learn how to create and manage prompts using Python, LangChain, and Groq GPT-OSS 120B.

## Topics Covered

### 1. Prompt Basics

- What is a prompt?
- Why are prompts important?
- Static vs dynamic prompts
- Prompt engineering fundamentals
- Prompt variables and placeholders

### 2. PromptTemplate

- Creating reusable text prompts
- Using `PromptTemplate`
- Passing values through `invoke()`
- Formatting dynamic prompts
- Connecting prompt templates to language models

### 3. ChatPromptTemplate

- Creating structured conversational prompts
- System, human, and AI messages
- Using `ChatPromptTemplate.from_messages()`
- Dynamic variables in chat messages
- Connecting chat prompts to Groq

### 4. MessagesPlaceholder

- What is `MessagesPlaceholder`?
- Inserting conversation history into prompts
- Building a chatbot with previous message context
- Understanding message roles and history

### 5. Quick Revision

- Important definitions
- Comparison tables
- Key methods
- Interview questions
- Practical learning exercises

## Learning Objectives

By the end of this section, I should be able to:

1. Explain the difference between static and dynamic prompts.
2. Create reusable prompts using `PromptTemplate`.
3. Use `ChatPromptTemplate` with structured messages.
4. Understand the purpose of `SystemMessage`, `HumanMessage`, and `AIMessage`.
5. Insert conversation history using `MessagesPlaceholder`.
6. Connect prompts to Groq GPT-OSS 120B.
7. Build simple prompt-based LangChain applications.

## Repository Structure

```text
04-Prompts/
├── README.md
├── notes/
│   ├── 01_Prompt_Basics.md
│   ├── 02_PromptTemplate.md
│   ├── 03_ChatPromptTemplate.md
│   ├── 04_MessagesPlaceholder.md
│   └── 05_Quick_Revision.md
└── examples/
    └── Python examples will be added here
```

## Technologies

| Technology     | Purpose                                 |
| -------------- | --------------------------------------- |
| Python         | Application development                 |
| LangChain      | Prompt management and model integration |
| LangChain Core | Prompt template and message classes     |
| Groq           | Hosted LLM inference                    |
| GPT-OSS 120B   | Language model                          |
| VS Code        | Development environment                 |

## Progress Checklist

- [ ] Prompt Basics
- [ ] PromptTemplate
- [ ] ChatPromptTemplate
- [ ] MessagesPlaceholder
- [ ] Quick Revision
- [ ] Practical Python Examples
- [ ] Test all examples

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [CampusX Prompts Repository](https://github.com/campusx-official/langchain-prompts)
- [LangChain Documentation](https://docs.langchain.com/)

## Key Goal

Learn how to design reusable prompts and pass structured instructions and conversation history to language models using LangChain.

---

**Learning Journey:** Section 04 of 18

**Course Reference:** CampusX — LangChain Prompts.
