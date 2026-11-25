# 06 — Runnable Methods in LangChain

## 1. Introduction

LangChain Runnables provide a common interface for executing different processing components.

Whether we use `RunnableLambda`, `RunnableSequence`, a prompt template, or a language model, we can interact with them through standard methods.

The six most important methods are:

1. `invoke()`
2. `batch()`
3. `stream()`
4. `ainvoke()`
5. `abatch()`
6. `astream()`

These methods are useful for building AI chatbots, RAG applications, APIs, automation systems, and AI agents.

---

## 2. Understanding Synchronous and Asynchronous Execution

Before learning the methods, we need to understand two important programming concepts.

### Synchronous Execution

In synchronous execution, Python normally waits for an operation to finish before proceeding to the next statement.

Example:

```python
result = chain.invoke({"topic": "Python"})
print(result)
```

The `print()` statement runs after `invoke()` returns.

### Asynchronous Execution

Asynchronous execution allows a Python program to suspend an operation while waiting for supported work, such as network communication.

Example:

```python
result = await chain.ainvoke({"topic": "Python"})
print(result)
```

The `await` keyword is used inside an asynchronous function.

Asynchronous programming is particularly useful for applications handling multiple API requests.

**Important:** Asynchronous execution does not automatically mean CPU-parallel processing.

---

## 3. invoke() — Single Input

`invoke()` executes a Runnable with one input.

### Example

```python
from langchain_core.runnables import RunnableLambda

square = RunnableLambda(lambda x: x ** 2)

result = square.invoke(5)

print(result)
```

Output:

```text
25
```

### When to Use invoke()

Use it when:

- Processing one input.
- Sending a single request to an LLM.
- Testing a Runnable.
- Executing a simple workflow.

### Groq Example

```python
result = chain.invoke({
    "topic": "Machine Learning"
})

print(str(result))
```

The program receives the complete result after execution finishes.

---

## 4. batch() — Multiple Inputs

`batch()` processes multiple inputs using the same Runnable.

### Example

```python
square = RunnableLambda(lambda x: x ** 2)

results = square.batch([2, 3, 4, 5])

print(results)
```

Output:

```text
[4, 9, 16, 25]
```

### How It Works

- The method receives a collection of inputs.
- Each input passes through the Runnable.
- The method returns a list of results.
- Results normally follow the same order as the inputs.

### Groq Example

```python
topics = [
    {"topic": "Python"},
    {"topic": "Machine Learning"},
    {"topic": "Deep Learning"}
]

results = chain.batch(
    topics,
    config={"max_concurrency": 2}
)
```

Here, `max_concurrency` controls the maximum number of concurrent Runnable operations where supported.

### Important

`batch()` does not necessarily send all prompts in one API call.

For many language model integrations, it may execute several requests concurrently.

---

## 5. stream() — Incremental Output

`stream()` allows a Runnable to provide results incrementally when the underlying components support streaming.

### Example

```python
for chunk in chain.stream({
    "topic": "Artificial Intelligence"
}):
    print(chunk, end="", flush=True)
```

### Why Use Streaming?

Without streaming, a chatbot might wait for the complete response before displaying it.

With streaming, the application can display text progressively.

### Common Uses

- Chatbots
- Coding assistants
- Long explanations
- Interactive learning applications

### Important

Not every Runnable produces multiple chunks.

For example:

```python
double = RunnableLambda(lambda x: x * 2)

for chunk in double.stream(5):
    print(chunk)
```

This may produce only one chunk:

```text
10
```

Streaming support depends on the components in the workflow.

---

## 6. ainvoke() — Asynchronous Single Input

`ainvoke()` is the asynchronous counterpart of `invoke()`.

It processes one input and returns the result asynchronously.

### Example

```python
import asyncio
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda x: x * 2)

async def main():
    result = await double.ainvoke(5)
    print(result)

asyncio.run(main())
```

Output:

```text
10
```

### Why Use ainvoke()?

It is useful when:

- Writing asynchronous applications.
- Handling network I/O.
- Building asynchronous FastAPI endpoints.
- Coordinating multiple model requests.

### Important Keywords

**`async def`**

Defines an asynchronous function.

**`await`**

Waits for an awaitable operation without blocking the asynchronous event loop in the same way as a regular synchronous call.

**`asyncio.run()`**

Runs the asynchronous entry-point function in a standard Python script.

In environments with an already-running event loop, such as some notebooks, use the environment's supported asynchronous execution pattern instead.

---

## 7. abatch() — Asynchronous Multiple Inputs

`abatch()` is the asynchronous counterpart of `batch()`.

It processes multiple inputs asynchronously.

### Example

```python
import asyncio
from langchain_core.runnables import RunnableLambda

square = RunnableLambda(lambda x: x ** 2)

async def main():
    results = await square.abatch([2, 3, 4, 5])
    print(results)

asyncio.run(main())
```

Output:

```text
[4, 9, 16, 25]
```

### Groq Example

```python
results = await chain.abatch(
    [
        {"topic": "Python"},
        {"topic": "Neural Networks"}
    ],
    config={"max_concurrency": 2}
)
```

### Benefits

- Suitable for async application architectures.
- Can coordinate multiple I/O-bound requests.
- Provides concurrency controls.
- Returns outputs corresponding to inputs.

Actual performance depends on the implementation and service limits.

---

## 8. astream() — Asynchronous Streaming

`astream()` is the asynchronous counterpart of `stream()`.

It produces an asynchronous stream of output chunks.

### Example

```python
async for chunk in chain.astream({
    "topic": "Machine Learning"
}):
    print(chunk, end="", flush=True)
```

The `async for` statement is used to iterate over an asynchronous stream.

### Full Structure

```python
import asyncio

async def main():
    async for chunk in chain.astream({
        "topic": "Machine Learning"
    }):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

### Common Uses

- Async chatbot backends.
- Streaming HTTP responses.
- Interactive applications.
- Real-time model response delivery.

---

## 9. Comparison of All Six Methods

| Method      | Inputs   | Execution Style                      | Output                   |
| ----------- | -------- | ------------------------------------ | ------------------------ |
| `invoke()`  | One      | Synchronous                          | One result               |
| `batch()`   | Multiple | Synchronous API; may use concurrency | List                     |
| `stream()`  | One      | Synchronous streaming                | Iterator of chunks       |
| `ainvoke()` | One      | Asynchronous                         | One result               |
| `abatch()`  | Multiple | Asynchronous; may use concurrency    | List                     |
| `astream()` | One      | Asynchronous streaming               | Async iterator of chunks |

## 10. Understanding Concurrency

Concurrency means managing multiple tasks whose execution can overlap.

For example, suppose we need three AI explanations.

We could request them individually:

```python
a = chain.invoke({"topic": "Python"})
b = chain.invoke({"topic": "SQL"})
c = chain.invoke({"topic": "FastAPI"})
```

These calls run one after another.

Alternatively:

```python
results = chain.batch([
    {"topic": "Python"},
    {"topic": "SQL"},
    {"topic": "FastAPI"}
])
```

This may allow concurrent processing.

### max_concurrency

```python
config={"max_concurrency": 2}
```

This limits supported concurrent execution to two operations.

It can help manage resource usage, although provider rate limits may still apply.

## 11. Batch Error Handling

By default, failures may cause the batch operation to raise an exception.

Some Runnables support:

```python
results = chain.batch(
    inputs,
    return_exceptions=True
)
```

This returns exception objects alongside successful results, allowing applications to inspect individual failures.

Example:

```python
for result in results:
    if isinstance(result, Exception):
        print("Failed:", result)
    else:
        print("Success:", result)
```

The same concept applies to `abatch()`.

## 12. Runnable Methods vs Runnable Types

These are different concepts.

### Runnable Types

- `RunnableSequence`
- `RunnableParallel`
- `RunnableLambda`
- `RunnablePassthrough`
- `RunnableBranch`

### Runnable Methods

- `invoke()`
- `batch()`
- `stream()`
- `ainvoke()`
- `abatch()`
- `astream()`

A Runnable type defines what processing is performed.

A Runnable method defines how that processing is executed.

## 13. RunnableLambda and Streaming Limitations

A common misunderstanding is assuming that every `RunnableLambda` supports token-by-token streaming.

Consider:

```python
formatter = RunnableLambda(lambda text: text.upper())
```

It processes its input as a complete value.

When connected after a streaming model, such a step can delay output until the upstream content has been collected.

For custom chunk-by-chunk transformations, a streaming-aware implementation such as `RunnableGenerator` may be more suitable.

## 14. Which Method Should We Use?

| Situation                                  | Recommended Method |
| ------------------------------------------ | ------------------ |
| Ask an LLM one question                    | `invoke()`         |
| Generate responses for multiple questions  | `batch()`          |
| Display model text progressively           | `stream()`         |
| Make a model call inside async Python code | `ainvoke()`        |
| Handle multiple requests in async code     | `abatch()`         |
| Stream an answer inside async code         | `astream()`        |

## 15. Practical Applications

### Chatbot

Use `stream()` or `astream()` to display generated responses progressively.

### FastAPI Backend

Use asynchronous Runnable methods when they fit the API architecture and underlying integration.

### Document Processing

Use `batch()` or `abatch()` to process multiple documents.

### RAG Application

Use `invoke()` for one retrieval-and-generation request or `stream()` when incremental response delivery is supported.

### AI Agent

Agent runtimes may expose similar execution methods for running and streaming agent workflows.

## 16. Common Beginner Mistakes

**Mistake 1 — Assuming async always means faster**

Performance depends on the task and implementation.

**Mistake 2 — Using await outside async code**

Use `await` inside an asynchronous function or a supported async environment.

**Mistake 3 — Assuming batch means one API call**

Batching may involve several model requests.

**Mistake 4 — Assuming stream always produces tokens**

A Runnable may yield complete values instead of individual tokens.

**Mistake 5 — Ignoring provider limits**

Concurrent calls can trigger API rate limits.

**Mistake 6 — Mixing sync and async code without understanding execution**

Use execution methods appropriate for the application environment.

## 17. Interview Questions

**Q1. What is invoke()?**

A method that processes one input synchronously.

**Q2. What is batch()?**

A method that processes multiple inputs.

**Q3. What is stream()?**

A method that returns output incrementally where supported.

**Q4. What is ainvoke()?**

The asynchronous counterpart of invoke().

**Q5. What is abatch()?**

The asynchronous counterpart of batch().

**Q6. What is astream()?**

The asynchronous counterpart of stream().

**Q7. What is the purpose of max_concurrency?**

To limit concurrent Runnable execution where supported.

**Q8. Does batch() use one API request?**

Not necessarily.

**Q9. Does asynchronous execution guarantee faster performance?**

No.

**Q10. Can RunnableLambda use async methods?**

Yes.

**Q11. What is the difference between stream() and astream()?**

stream() uses synchronous iteration, while astream() uses asynchronous iteration.

**Q12. What is the difference between a Runnable type and a Runnable method?**

The type describes processing behavior; the method describes execution.

## 18. Key Takeaways

- LangChain Runnables provide six commonly used execution methods.
- `invoke()` processes one input.
- `batch()` processes multiple inputs.
- `stream()` produces incremental output when supported.
- `ainvoke()` executes a single input asynchronously.
- `abatch()` processes multiple inputs asynchronously.
- `astream()` supports asynchronous streaming.
- Batch processing can involve multiple API requests.
- Concurrency must be managed carefully.
- Streaming behavior depends on the components.
- Understanding these methods is important for AI application development.

---

## Learning Resources

- [LangChain Runnable Reference](https://reference.langchain.com/python/langchain-core/runnables/base/Runnable)
- [LangChain RunnableSequence Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 — Topic 06
