# 01 — Runnable Basics in LangChain

## 1. What Is a Runnable?

A **Runnable** is a LangChain component that follows a common interface for processing inputs and producing outputs.

In simple words, a Runnable is something that can receive input, perform an operation, and return a result.

For example:

```text
Input → Runnable → Output
```

A Runnable might:

- Format a prompt.
- Generate a response using an LLM.
- Parse an LLM response.
- Execute a Python function.
- Combine several processing steps.

The Runnable interface is a major building block of LangChain's workflow composition system.

## 2. Why Do We Need Runnables?

Consider building an AI application with three operations:

1. Prepare a prompt.
2. Generate a model response.
3. Extract the response text.

Without a chain, we can execute the operations manually:

```python
formatted_prompt = prompt.invoke({
    "topic": "Python"
})

response = model.invoke(formatted_prompt)

result = parser.invoke(response)

print(result)
```

With Runnable composition:

```python
chain = prompt | model | parser

result = chain.invoke({
    "topic": "Python"
})
```

This approach makes the workflow easier to read and reuse.

### Main Benefits

- Common execution interface
- Reusable processing components
- Cleaner workflow composition
- Support for multiple inputs
- Support for asynchronous execution
- Support for streaming when components allow it
- Compatibility with other LangChain components

## 3. The Runnable Interface

LangChain Runnables share several important execution methods.

| Method      | Description                                  |
| ----------- | -------------------------------------------- |
| `invoke()`  | Execute a Runnable with one input            |
| `batch()`   | Process multiple inputs                      |
| `stream()`  | Return output incrementally when supported   |
| `ainvoke()` | Asynchronously process one input             |
| `abatch()`  | Asynchronously process multiple inputs       |
| `astream()` | Asynchronously produce output when supported |

These methods provide a consistent way to interact with different LangChain components.

**Important:** The exact implementation and streaming behavior depend on the Runnable.

## 4. Examples of Runnable Components

### A. PromptTemplate

A prompt template formats instructions using input variables.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in three simple sentences."
)

result = prompt.invoke({
    "topic": "Python"
})

print(result)
```

The output is a prompt value containing formatted instructions.

### B. Chat Model

A chat model is also a Runnable.

```python
from langchain_groq import ChatGroq

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

response = model.invoke(
    "What is Machine Learning?"
)

print(response.content)
```

The model returns an AI message object.

### C. Output Parser

An output parser processes model-generated responses.

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

result = parser.invoke(response)

print(str(result))
```

This produces text suitable for further processing.

### D. RunnableLambda

A `RunnableLambda` wraps an ordinary Python function as a Runnable.

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(
    lambda number: number * 2
)

result = double.invoke(10)

print(result)
```

Output:

```text
20
```

This example does not require an LLM or API key.

## 5. What Is Runnable Composition?

Runnable composition means connecting multiple Runnables into a workflow.

LangChain commonly uses the pipe operator (`|`).

```python
chain = prompt | model | parser
```

### Execution Flow

```text
User Input
    |
    v
PromptTemplate
    |
    v
ChatGroq
    |
    v
StrOutputParser
    |
    v
Final Answer
```

The output of each component becomes the input of the next component.

This composition style is commonly called **LangChain Expression Language (LCEL)**.

## 6. Understanding Input and Output Types

Each Runnable receives an input and produces an output.

For example:

| Component       | Typical Input                              | Typical Output          |
| --------------- | ------------------------------------------ | ----------------------- |
| PromptTemplate  | Dictionary                                 | PromptValue             |
| ChatGroq        | PromptValue, string, or supported messages | AIMessage               |
| StrOutputParser | AIMessage or text                          | Text                    |
| RunnableLambda  | Depends on the function                    | Depends on the function |

When connecting Runnables, their input and output formats must be compatible.

### Example

```python
from langchain_core.runnables import RunnableLambda

uppercase = RunnableLambda(
    lambda text: str(text).upper()
)

result = uppercase.invoke("hello")

print(result)
```

Output:

```text
HELLO
```

We can also connect Python functions using Runnable composition.

```python
uppercase = RunnableLambda(
    lambda text: text.upper()
)

add_exclamation = RunnableLambda(
    lambda text: text + "!"
)

chain = uppercase | add_exclamation

print(chain.invoke("hello"))
```

Output:

```text
HELLO!
```

## 7. Understanding invoke()

`invoke()` executes a Runnable with one input.

Example:

```python
square = RunnableLambda(
    lambda number: number ** 2
)

print(square.invoke(5))
```

Output:

```text
25
```

This is the simplest Runnable execution method.

## 8. Understanding batch()

`batch()` processes several inputs.

```python
square = RunnableLambda(
    lambda number: number ** 2
)

results = square.batch([2, 3, 4, 5])

print(results)
```

Expected output:

```text
[4, 9, 16, 25]
```

The outputs correspond to the input order.

Batching can involve concurrent execution, depending on the Runnable implementation.

## 9. Understanding stream()

`stream()` is used to produce outputs incrementally.

```python
for chunk in chain.stream("hello"):
    print(chunk)
```

Not all Runnables produce multiple streaming chunks.

For example, a simple Python function wrapped in `RunnableLambda` may emit its result as a single chunk.

Chat models can often stream generated text incrementally.

We will study streaming with Groq in Topic 06.

## 10. Understanding Asynchronous Runnables

Asynchronous execution allows Python programs to perform operations without blocking the current asynchronous workflow while waiting for supported operations.

An asynchronous Runnable can be executed using `ainvoke()`.

```python
import asyncio
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(
    lambda number: number * 2
)

async def main():
    result = await double.ainvoke(10)
    print(result)

asyncio.run(main())
```

Output:

```text
20
```

Asynchronous operations become especially useful when handling multiple network requests.

## 11. What Is RunnableSequence?

`RunnableSequence` connects processing steps in sequence.

Example:

```python
from langchain_core.runnables import (
    RunnableLambda,
    RunnableSequence
)

double = RunnableLambda(
    lambda x: x * 2
)

add_five = RunnableLambda(
    lambda x: x + 5
)

chain = RunnableSequence(
    double,
    add_five
)

print(chain.invoke(10))
```

Output:

```text
25
```

Explanation:

1. Input: `10`
2. Double: `20`
3. Add five: `25`

We can also write:

```python
chain = double | add_five
```

Both approaches execute the same processing steps.

## 12. What Is RunnableParallel?

`RunnableParallel` sends the same input to multiple independent branches.

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2)
)

print(parallel.invoke(5))
```

Expected output:

```python
{
    "double": 10,
    "square": 25
}
```

Each branch processes the input independently.

## 13. What Is RunnablePassthrough?

`RunnablePassthrough` forwards an input without changing it.

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

result = passthrough.invoke(
    "Hello LangChain"
)

print(result)
```

Output:

```text
Hello LangChain
```

This is useful when we want to preserve original input while generating additional values.

We will explore `RunnablePassthrough.assign()` in Topic 04.

## 14. Runnable vs Chain vs Agent

| Concept  | Meaning                                               | Example                 |
| -------- | ----------------------------------------------------- | ----------------------- |
| Runnable | A component with a common execution interface         | RunnableLambda          |
| Chain    | A connected workflow of processing steps              | Prompt → Model → Parser |
| Agent    | A system that can select actions or tools dynamically | Tool-using AI assistant |

A chain can be a Runnable.

An individual prompt, model, or output parser can also be a Runnable.

A Runnable does not necessarily require an LLM.

## 15. Common Beginner Mistakes

**Mistake 1 — Thinking every Runnable uses AI**

Many Runnables perform ordinary Python operations.

**Mistake 2 — Assuming every Runnable streams multiple chunks**

Some Runnables return only one complete output.

**Mistake 3 — Confusing invoke() with batch()**

`invoke()` handles one input, while `batch()` handles multiple inputs.

**Mistake 4 — Connecting incompatible data types**

The output of one step must be suitable for the next step.

**Mistake 5 — Assuming asynchronous execution means parallel CPU processing**

Asynchronous execution is especially useful for coordinating waiting operations, such as network requests. It does not automatically make CPU-intensive Python code run in parallel.

## 16. Interview Questions

**Q1. What is a Runnable in LangChain?**

A component that follows a common interface for executing operations.

**Q2. Why are Runnables important?**

They allow LangChain components to be composed and executed consistently.

**Q3. What is LCEL?**

LangChain Expression Language, used to compose Runnable components.

**Q4. What does the pipe operator do?**

Connects compatible Runnables.

**Q5. What does invoke() do?**

Processes one input.

**Q6. What does batch() do?**

Processes multiple inputs.

**Q7. What does stream() do?**

Returns incremental output when supported.

**Q8. What is RunnableLambda?**

A wrapper that turns a Python function into a Runnable.

**Q9. What is RunnableSequence?**

A Runnable that executes processing steps in order.

**Q10. What is RunnableParallel?**

A Runnable that executes independent branches using the same input.

**Q11. What is RunnablePassthrough?**

A Runnable that passes the input through unchanged.

**Q12. Can we create Runnables without using an LLM?**

Yes.

## 17. Key Takeaways

- Runnables provide a common execution interface.
- Runnables can perform AI and non-AI operations.
- Runnable composition uses LCEL.
- The pipe operator connects compatible components.
- `invoke()` handles one input.
- `batch()` handles multiple inputs.
- `stream()` supports incremental output when available.
- `ainvoke()` supports asynchronous invocation.
- `RunnableSequence` connects sequential steps.
- `RunnableParallel` executes independent branches.
- `RunnablePassthrough` preserves input.
- `RunnableLambda` integrates Python functions.

---

## Learning Resources

- [LangChain Runnable Documentation](https://reference.langchain.com/python/langchain-core/runnables/)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 — Topic 01
