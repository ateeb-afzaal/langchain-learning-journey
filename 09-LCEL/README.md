# 09 — LangChain Expression Language (LCEL)

## Overview

**LCEL (LangChain Expression Language)** is a declarative way of connecting LangChain components into reusable workflows.

LCEL allows developers to combine prompts, language models, output parsers, Python functions, retrievers, and other Runnables.

The most recognizable feature of LCEL is the **pipe operator (`|`)**, which connects compatible components.

For example:

```python
chain = prompt | model | parser
```

In this section, I will learn how to build more advanced LangChain workflows using **Python, LCEL, and Groq GPT-OSS 120B**.

## Why Learn LCEL?

In previous sections, I learned about:

- **Section 06:** Output Parsers
- **Section 07:** Chains
- **Section 08:** Runnables

LCEL brings these concepts together.

Instead of manually executing each component, I can combine them into one reusable processing pipeline.

For example, an AI application might:

1. Receive a programming question.
2. Clean and format the input.
3. Generate a beginner-friendly explanation.
4. Generate interview questions independently.
5. Combine the results into a structured response.

LCEL makes this type of workflow easier to organize.

## Topics Covered

### 1. LCEL Basics

- What is LCEL?
- Why do developers use LCEL?
- Understanding Runnable composition
- How inputs and outputs flow between components
- LCEL vs traditional Python execution

### 2. Pipe Operator

- Understanding the `|` operator
- Connecting prompts, models, and parsers
- Building multi-step processing pipelines
- Using `RunnableSequence`
- Understanding input/output compatibility

### 3. Dictionary Composition

- Using dictionaries in LCEL
- Automatic conversion to `RunnableParallel`
- Running multiple independent branches
- Working with dictionary outputs
- Combining generated and original information

### 4. Data Transformation

- Using `RunnableLambda`
- Using `RunnablePassthrough`
- Adding new dictionary fields
- Transforming input before an LLM call
- Formatting model responses
- Preparing data for downstream components

### 5. Advanced LCEL

- Combining sequential and parallel workflows
- Using `RunnableBranch`
- Routing inputs based on conditions
- Nested Runnable composition
- Handling errors and fallbacks
- Inspecting workflow structure

### 6. Practical LCEL Project

Build a small **AI Programming Study Assistant** using Groq GPT-OSS 120B.

The assistant will:

- Accept a programming topic and difficulty level.
- Clean and validate the input.
- Select an appropriate explanation prompt.
- Generate an explanation and interview questions.
- Preserve the original topic.
- Return a structured Python dictionary.

### 7. Quick Revision

- Important concepts
- Comparison tables
- Interview questions
- Practical code examples
- Common mistakes
- Final testing checklist

## Learning Objectives

By the end of this section, I should be able to:

1. Explain what LCEL is and why it is useful.
2. Connect LangChain components using the pipe operator.
3. Understand how `RunnableSequence` works within LCEL.
4. Use dictionary composition to create parallel workflows.
5. Transform inputs using `RunnableLambda`.
6. Preserve original inputs using `RunnablePassthrough`.
7. Select workflows using `RunnableBranch`.
8. Combine multiple Runnable types into one application.
9. Execute and debug LCEL workflows.
10. Build a practical AI application using Groq.

## Repository Structure

```text
09-LCEL/
├── README.md
├── notes/
│   ├── 01_LCEL_Basics.md
│   ├── 02_Pipe_Operator.md
│   ├── 03_Dictionary_Composition.md
│   ├── 04_Data_Transformation.md
│   ├── 05_Advanced_LCEL.md
│   ├── 06_Practical_LCEL_Project.md
│   └── 07_Quick_Revision.md
└── examples/
    └── Practical Python examples will be added here
```

## Important Components

| Component             | Purpose                                 |
| --------------------- | --------------------------------------- |
| `PromptTemplate`      | Create reusable prompts                 |
| `ChatGroq`            | Connect to a Groq-hosted language model |
| `StrOutputParser`     | Extract generated text                  |
| `RunnableSequence`    | Execute operations in sequence          |
| `RunnableParallel`    | Execute independent branches            |
| `RunnableLambda`      | Wrap Python functions                   |
| `RunnablePassthrough` | Preserve original data                  |
| `RunnableBranch`      | Select a workflow based on conditions   |

## Basic LCEL Example

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
    "Explain {topic} to a beginner in three simple sentences."
)

chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "topic": "Machine Learning"
})

print(str(result))
```

### How This Works

1. The input dictionary supplies the `topic`.
2. The prompt formats the instructions.
3. Groq generates a response.
4. `StrOutputParser` extracts the generated text.
5. The chain returns the final output.

The pipe operator connects all components into a runnable sequence.

## LCEL Execution Methods

LCEL workflows generally support common Runnable methods.

| Method      | Purpose                       |
| ----------- | ----------------------------- |
| `invoke()`  | Execute one input             |
| `batch()`   | Process multiple inputs       |
| `stream()`  | Stream output where supported |
| `ainvoke()` | Asynchronous invocation       |
| `abatch()`  | Asynchronous batch processing |
| `astream()` | Asynchronous streaming        |

The exact behavior depends on the components used.

## LCEL vs Manual Python Processing

### Manual Approach

```python
formatted_prompt = prompt.invoke({"topic": "Python"})
response = model.invoke(formatted_prompt)
answer = parser.invoke(response)
```

### LCEL Approach

```python
chain = prompt | model | parser

answer = chain.invoke({"topic": "Python"})
```

Both approaches are valid.

LCEL is especially useful when building larger workflows using multiple composable components.

## Technologies Used

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| Python         | Application logic           |
| LangChain      | Workflow composition        |
| LangChain Core | Runnables, prompts, parsers |
| Groq           | Hosted LLM inference        |
| GPT-OSS 120B   | Language model              |
| python-dotenv  | Loading API credentials     |
| VS Code        | Development                 |
| GitHub         | Version control             |

## Progress Checklist

- [ ] 01 — LCEL Basics
- [ ] 02 — Pipe Operator
- [ ] 03 — Dictionary Composition
- [ ] 04 — Data Transformation
- [ ] 05 — Advanced LCEL
- [ ] 06 — Practical LCEL Project
- [ ] 07 — Quick Revision
- [ ] Create practical Python examples
- [ ] Test all examples
- [ ] Commit and push to GitHub

## Important Concepts to Remember

**LCEL:** LangChain Expression Language, used to compose processing components.

**Runnable:** A component that follows LangChain's common execution interface.

**Pipe Operator:** Connects compatible components.

**RunnableSequence:** Executes connected operations in order.

**RunnableParallel:** Runs independent processing branches.

**RunnableLambda:** Integrates ordinary Python functions.

**RunnablePassthrough:** Preserves input or adds computed fields using `assign()`.

**RunnableBranch:** Selects a branch based on predefined conditions.

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [LangChain Documentation](https://docs.langchain.com/)
- [LangChain Runnable Reference](https://reference.langchain.com/python/langchain-core/runnables/)

---

**Learning Journey:** Section 09 of 18

**Main Goal:** Learn advanced LCEL composition and build reusable AI workflows using LangChain and Groq.
