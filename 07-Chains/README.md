# 07 — Chains in LangChain

## Overview

Chains are workflows that connect different processing steps in a LangChain application.

Instead of sending one question directly to a language model, we can combine prompts, models, output parsers, and other processing components to perform more complex tasks.

For example, an application might generate a summary of a document and then translate that summary into another language.

In this section, I will learn how to create different types of chains using **Python, LangChain, and Groq GPT-OSS 120B**.

The examples use modern LangChain runnable components and LangChain Expression Language (LCEL).

## Topics Covered

### 1. Chains Basics

- What is a chain?
- Why do we need chains?
- How chains work
- Introduction to LCEL
- The pipe operator (`|`)
- Understanding Runnable components

### 2. Simple Chain

- Connecting a prompt, model, and output parser
- Using `chain.invoke()`
- Passing dynamic variables
- Receiving the final output

### 3. Sequential Chain

- Running multiple steps in sequence
- Passing the output of one step into another
- Using `RunnableSequence`
- Building summarization and translation workflows

### 4. Parallel Chain

- Running independent processing branches
- Using `RunnableParallel`
- Generating multiple outputs from the same input
- Combining results from different branches

### 5. Conditional Chain

- Creating workflows with decision-making logic
- Using `RunnableBranch`
- Defining conditions and fallback branches
- Routing user requests to different prompts

### 6. Quick Revision

- Important definitions
- Comparison tables
- Interview questions
- Practical test results

## Learning Objectives

By the end of this section, I should be able to:

1. Explain what a chain is and why it is useful.
2. Connect prompts, models, and output parsers.
3. Build simple chains using LCEL.
4. Create sequential workflows.
5. Run independent processing branches in parallel.
6. Build conditional workflows with `RunnableBranch`.
7. Understand when to use each type of chain.
8. Handle basic chain execution errors.

## Repository Structure

```text
07-Chains/
├── README.md
├── notes/
│   ├── 01_Chains_Basics.md
│   ├── 02_Simple_Chain.md
│   ├── 03_Sequential_Chain.md
│   ├── 04_Parallel_Chain.md
│   ├── 05_Conditional_Chain.md
│   └── 06_Quick_Revision.md
└── examples/
    └── Python examples will be added here
```

## Types of Chains

| Chain Type  | Purpose                               | Example                          |
| ----------- | ------------------------------------- | -------------------------------- |
| Simple      | Execute a basic workflow              | Prompt → LLM → Parser            |
| Sequential  | Connect dependent steps               | Generate summary → Translate     |
| Parallel    | Execute independent branches          | Generate summary and quiz        |
| Conditional | Select a workflow based on conditions | Beginner vs advanced explanation |

## Basic Example

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
    "topic": "Machine Learning"
})

print(result)
```

### How It Works

1. `PromptTemplate` prepares the instructions.
2. `ChatGroq` generates a response.
3. `StrOutputParser` extracts the response text.
4. `chain.invoke()` executes the workflow.

## Technologies

| Technology     | Purpose                           |
| -------------- | --------------------------------- |
| Python         | Application development           |
| LangChain      | Building composable workflows     |
| LangChain Core | Runnables, prompts, and parsers   |
| Groq           | Hosted LLM inference              |
| GPT-OSS 120B   | Language model                    |
| VS Code        | Development environment           |
| GitHub         | Version control and documentation |

## Progress Checklist

- [ ] Chains Basics
- [ ] Simple Chain
- [ ] Sequential Chain
- [ ] Parallel Chain
- [ ] Conditional Chain
- [ ] Quick Revision
- [ ] Practical Python Examples
- [ ] Test all examples

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [CampusX Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain Documentation](https://docs.langchain.com/)

## Key Goal

Learn how to combine LangChain components into reusable workflows and understand the differences between simple, sequential, parallel, and conditional chains.

---

**Learning Journey:** Section 07 of 18

**Course Reference:** CampusX — LangChain Chains.
