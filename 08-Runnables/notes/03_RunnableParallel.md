# 03 — RunnableParallel in LangChain

## 1. What Is RunnableParallel?

`RunnableParallel` is a LangChain component that executes multiple independent Runnable branches using the same input.

Each branch performs its own operation and returns a result.

The outputs are combined into a dictionary.

### Example

```text
                  Input: 5
                     |
                     v
              RunnableParallel
                     |
          +----------+----------+
          |          |          |
          v          v          v
        Double     Square      Cube
          |          |          |
          v          v          v
         10         25         125
          |          |          |
          +----------+----------+
                     |
                     v
       {"double": 10, "square": 25,
               "cube": 125}
```

## 2. Why Do We Need RunnableParallel?

Imagine creating an AI learning assistant.

When a user provides a topic, the assistant needs to generate:

- A beginner-friendly summary.
- Three interview questions.
- Important keywords.

These tasks are independent.

Using `RunnableParallel`, the application can execute all three branches concurrently instead of waiting for each one to finish before starting the next.

### Benefits

1. Organizes independent tasks.
2. Can reduce execution latency.
3. Allows multiple outputs from the same input.
4. Makes workflows reusable.
5. Combines results in a dictionary.
6. Works with ordinary Python functions and LLMs.

## 3. Importing RunnableParallel

```python
from langchain_core.runnables import RunnableParallel
```

We will also use `RunnableLambda` to create operations without involving a language model.

```python
from langchain_core.runnables import RunnableLambda
```

## 4. Basic Example Without an LLM

First, define three Runnables:

```python
double = RunnableLambda(lambda x: x * 2)
square = RunnableLambda(lambda x: x ** 2)
cube = RunnableLambda(lambda x: x ** 3)
```

Now combine them:

```python
parallel = RunnableParallel(
    double=double,
    square=square,
    cube=cube
)
```

Execute:

```python
result = parallel.invoke(5)

print(result)
```

Expected output:

```python
{
    "double": 10,
    "square": 25,
    "cube": 125
}
```

### Explanation

- The input is `5`.
- The double branch calculates `10`.
- The square branch calculates `25`.
- The cube branch calculates `125`.
- `RunnableParallel` combines the results.

All three branches receive the original input `5`.

## 5. RunnableSequence vs RunnableParallel

### RunnableSequence

```python
sequence = double | square
```

For input `5`:

1. Double 5 → 10.
2. Square 10 → 100.

Final output:

```text
100
```

### RunnableParallel

```python
parallel = RunnableParallel(
    double=double,
    square=square
)
```

For input `5`:

```python
{
    "double": 10,
    "square": 25
}
```

### Comparison

| Feature    | RunnableSequence       | RunnableParallel             |
| ---------- | ---------------------- | ---------------------------- |
| Execution  | Sequential             | Concurrent where supported   |
| Input      | Previous step's output | Same input for every branch  |
| Output     | Last step's result     | Dictionary of branch results |
| Dependency | Dependent operations   | Independent operations       |
| Example    | Double then square     | Double and square            |

## 6. Understanding the Output Dictionary

The names we provide in `RunnableParallel` become dictionary keys.

Example:

```python
parallel = RunnableParallel(
    multiplication=lambda x: x * 10,
    addition=lambda x: x + 10
)
```

RunnableParallel can coerce compatible callables, such as these functions, into Runnables.

Result:

```python
{
    "multiplication": 50,
    "addition": 15
}
```

We can access specific outputs:

```python
result["multiplication"]
result["addition"]
```

## 7. Creating RunnableParallel Using Dictionary Syntax

We can explicitly create a parallel Runnable:

```python
parallel = RunnableParallel({
    "double": double,
    "square": square
})
```

We can also use a dictionary in an LCEL composition:

```python
chain = RunnableLambda(lambda x: x + 1) | {
    "double": double,
    "square": square
}
```

The dictionary is automatically converted into a `RunnableParallel` during composition.

For input `5`, the first step produces `6`, then both branches process `6`.

Expected result:

```python
{
    "double": 12,
    "square": 36
}
```

## 8. RunnableParallel with Groq

Now we'll create an AI assistant that generates two outputs for a programming topic.

### Initialize Groq

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

### Create Prompts

```python
from langchain_core.prompts import PromptTemplate

summary_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 sentences."
)

questions_prompt = PromptTemplate.from_template(
    "Generate 3 interview questions about {topic}."
)
```

### Create Two Chains

```python
from langchain_core.output_parsers import StrOutputParser

summary_chain = summary_prompt | model | StrOutputParser()

questions_chain = questions_prompt | model | StrOutputParser()
```

### Create RunnableParallel

```python
parallel_chain = RunnableParallel(
    summary=summary_chain,
    questions=questions_chain
)
```

### Execute

```python
result = parallel_chain.invoke({
    "topic": "Python decorators"
})

print(result["summary"])
print(result["questions"])
```

Both branches receive the same topic.

## 9. Understanding Concurrency

`RunnableParallel` is designed to run independent operations concurrently where the execution environment supports it.

For network requests, concurrency can reduce overall waiting time.

For example, imagine:

- Summary request takes approximately 3 seconds.
- Questions request takes approximately 4 seconds.

If they run sequentially, total waiting time might be approximately 7 seconds.

If they run concurrently, the total might be closer to 4 seconds plus overhead.

These values are hypothetical and not guaranteed.

Actual performance depends on:

- Model inference time
- Network conditions
- Provider rate limits
- Number of branches
- Execution overhead

## 10. Does RunnableParallel Reduce API Calls?

No.

If we create three independent branches that each call an LLM, the application generally makes three model requests.

RunnableParallel changes how tasks are scheduled; it does not automatically combine requests into one API call.

This distinction is important when considering API costs and rate limits.

## 11. Using batch() with RunnableParallel

We can send multiple inputs through a parallel workflow.

```python
parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2)
)

results = parallel.batch([2, 3, 4])

print(results)
```

Expected output:

```python
[
    {"double": 4, "square": 4},
    {"double": 6, "square": 9},
    {"double": 8, "square": 16}
]
```

Every input is processed by both branches.

## 12. Controlling Concurrency

We can provide a maximum concurrency configuration:

```python
results = parallel.batch(
    [2, 3, 4],
    config={"max_concurrency": 2}
)
```

This can help limit the amount of concurrent work.

When using hosted LLMs, concurrency limits can help reduce the risk of exceeding API provider rate limits.

## 13. Error Handling

If one branch fails, the overall parallel invocation normally raises an exception.

Example:

```python
try:
    result = parallel.invoke(5)
    print(result)
except Exception as error:
    print("Parallel execution failed:", error)
```

More advanced applications can configure retries, fallbacks, or custom error handling.

## 14. Real-World Applications

### AI Learning Assistant

Input: Python decorators.

Outputs:

- Summary
- Interview questions
- Practical examples

### Customer Support Analysis

Input: Customer complaint.

Outputs:

- Sentiment
- Category
- Suggested response

### Document Processing

Input: Document text.

Outputs:

- Summary
- Keywords
- Topic classification

### Code Review Assistant

Input: Source code.

Outputs:

- Potential bugs
- Readability suggestions
- Security observations

These tasks are suitable for parallel processing when they do not depend on each other's outputs.

## 15. Common Beginner Mistakes

**Mistake 1: Thinking branches run sequentially**

Independent branches can run concurrently.

**Mistake 2: Thinking branches receive each other's outputs**

Every branch receives the shared input of that RunnableParallel stage.

**Mistake 3: Assuming one LLM request**

Each model branch can make a separate API request.

**Mistake 4: Ignoring API rate limits**

Several concurrent requests can trigger provider limits.

**Mistake 5: Expecting every parallel workflow to be faster**

Performance depends on the operations and execution environment.

## 16. Interview Questions

**Q1. What is RunnableParallel?**

A LangChain Runnable that executes independent branches and combines their outputs.

**Q2. What does RunnableParallel return?**

A dictionary mapping branch names to their outputs.

**Q3. Does each branch receive the same input?**

Yes.

**Q4. What is the difference between RunnableParallel and RunnableSequence?**

RunnableParallel executes independent branches, while RunnableSequence connects dependent steps.

**Q5. Can RunnableParallel work without an LLM?**

Yes.

**Q6. Can we combine PromptTemplate, ChatGroq, and StrOutputParser in a parallel workflow?**

Yes.

**Q7. Does RunnableParallel reduce the number of API requests?**

No.

**Q8. Can RunnableParallel process multiple inputs?**

Yes, through methods such as `batch()`.

**Q9. What happens if one branch fails?**

The overall operation normally raises an exception unless error handling is configured.

**Q10. When should we use RunnableParallel?**

When multiple tasks can operate independently on the same input.

## 17. Key Takeaways

- `RunnableParallel` executes independent branches.
- Each branch receives the same input.
- Outputs are returned as a dictionary.
- Branches can contain Python functions, models, prompts, or other Runnables.
- Parallel execution can improve latency for independent tasks.
- Multiple LLM branches usually make multiple API calls.
- `batch()` can process multiple inputs.
- Concurrency and error handling are important in production workflows.

---

## Learning Resources

- [LangChain RunnableParallel Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableParallel)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 — Topic 03
