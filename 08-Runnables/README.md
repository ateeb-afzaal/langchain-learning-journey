# 08 — Runnables in LangChain

## Overview

Runnables are one of the fundamental building blocks of modern LangChain applications.

A **Runnable** is a component that follows a common interface for processing inputs and producing outputs.

Runnables allow developers to connect prompts, language models, output parsers, Python functions, and other operations into reusable workflows.

In this section, I will learn how Runnables work using **Python, LangChain, and Groq GPT-OSS 120B**.

## Why Learn Runnables?

In Section 07 — Chains, I learned how to build:

- Simple chains
- Sequential chains
- Parallel chains
- Conditional chains

These workflows rely on LangChain's Runnable interface.

Understanding Runnables will help me build more flexible and maintainable AI applications, including RAG pipelines and agent-related workflows.

## Topics Covered

### 1. Runnable Basics

- What is a Runnable?
- Why are Runnables useful?
- Runnable input and output
- Runnable interface
- Runnable composition
- Introduction to LCEL

### 2. RunnableSequence

- What is `RunnableSequence`?
- Sequential processing
- Passing data between steps
- Using the pipe operator (`|`)
- Explicit vs implicit RunnableSequence

### 3. RunnableParallel

- What is `RunnableParallel`?
- Running independent workflows concurrently
- Passing shared input to multiple branches
- Combining branch results
- Understanding dictionary outputs

### 4. RunnablePassthrough

- What is `RunnablePassthrough`?
- Passing data through unchanged
- Preserving original user input
- Combining original input with generated output
- Using `RunnablePassthrough.assign()`

### 5. RunnableLambda

- What is `RunnableLambda`?
- Converting Python functions into Runnables
- Transforming inputs and outputs
- Using lambda functions
- Building custom processing steps

### 6. Runnable Methods

- `invoke()` — Single input execution
- `batch()` — Multiple input execution
- `stream()` — Incremental output
- `ainvoke()` — Asynchronous invocation
- `abatch()` — Asynchronous batching
- `astream()` — Asynchronous streaming

### 7. Quick Revision

- Important definitions
- Comparison tables
- Common mistakes
- Interview questions
- Practical test results

## Learning Objectives

By the end of this section, I should be able to:

1. Explain what the Runnable interface is.
2. Understand how Runnables process inputs and outputs.
3. Create sequential workflows with `RunnableSequence`.
4. Create concurrent branches with `RunnableParallel`.
5. Preserve original data using `RunnablePassthrough`.
6. Integrate Python functions using `RunnableLambda`.
7. Execute Runnables using synchronous and asynchronous methods.
8. Combine multiple Runnable components into practical AI applications.

## Repository Structure

```text
08-Runnables/
├── README.md
├── notes/
│   ├── 01_Runnables_Basics.md
│   ├── 02_RunnableSequence.md
│   ├── 03_RunnableParallel.md
│   ├── 04_RunnablePassthrough.md
│   ├── 05_RunnableLambda.md
│   ├── 06_Runnable_Methods.md
│   └── 07_Quick_Revision.md
└── examples/
    └── Practical Python examples will be added here
```

## Important Runnable Components

| Runnable              | Purpose                                 | Example                            |
| --------------------- | --------------------------------------- | ---------------------------------- |
| `RunnableSequence`    | Connect operations sequentially         | Prompt → Model → Parser            |
| `RunnableParallel`    | Execute independent operations          | Summary + Questions                |
| `RunnablePassthrough` | Forward original input                  | Preserve question alongside answer |
| `RunnableLambda`      | Wrap Python functions                   | Convert text to uppercase          |
| `RunnableBranch`      | Select an operation based on conditions | Beginner vs Advanced               |

`RunnableBranch` was introduced in Section 07 and will remain useful when building more complex workflows.

## Basic Runnable Example

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "Explain {topic} in three simple sentences."
)

chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "topic": "Artificial Intelligence"
})

print(str(result))
```

### How It Works

1. The prompt receives the input.
2. The prompt formats the instructions.
3. The chat model generates a response.
4. The parser extracts the response text.
5. `invoke()` executes the connected workflow.

Each component participates in the Runnable processing interface.

## Technologies Used

| Technology     | Purpose                               |
| -------------- | ------------------------------------- |
| Python         | Writing application logic             |
| LangChain      | Building runnable workflows           |
| LangChain Core | Runnable abstractions and composition |
| Groq           | Hosted model inference                |
| GPT-OSS 120B   | Language model                        |
| python-dotenv  | Loading environment credentials       |
| VS Code        | Development environment               |
| GitHub         | Version control                       |

## Progress Checklist

- [ ] 01 — Runnable Basics
- [ ] 02 — RunnableSequence
- [ ] 03 — RunnableParallel
- [ ] 04 — RunnablePassthrough
- [ ] 05 — RunnableLambda
- [ ] 06 — Runnable Methods
- [ ] 07 — Quick Revision
- [ ] Create practical Python examples
- [ ] Test all examples
- [ ] Commit and push to GitHub

## Important Concepts to Remember

**Runnable:** A component that accepts input and returns output through a common interface.

**LCEL:** LangChain Expression Language, which enables runnable composition.

**Pipe Operator (`|`):** Connects compatible processing components.

**RunnableSequence:** Executes operations in sequence.

**RunnableParallel:** Executes independent branches and returns their results in a dictionary.

**RunnablePassthrough:** Forwards data without changing it unless additional transformations are configured.

**RunnableLambda:** Wraps Python functions for use in runnable workflows.

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [LangChain Runnable Reference](https://reference.langchain.com/python/langchain-core/runnables/)
- [LangChain Documentation](https://docs.langchain.com/)

---

**Learning Journey:** Section 08 of 18

**Main Goal:** Understand the Runnable interface and learn how to create reusable, composable LangChain workflows.
