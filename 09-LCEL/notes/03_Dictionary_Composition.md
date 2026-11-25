# 03 — Dictionary Composition in LangChain LCEL

## 1. What Is Dictionary Composition?

Dictionary composition is a technique in LangChain Expression Language (LCEL) that allows us to combine multiple Runnable operations using dictionary syntax.

Each dictionary key represents an output field, while its value represents a Runnable or compatible operation.

Example:

```python
chain = some_runnable | {
    "double": double,
    "square": square
}
```

LangChain automatically converts the dictionary into a `RunnableParallel` stage.

Both branches receive the same input from `some_runnable`.

## 2. Why Do We Need Dictionary Composition?

Imagine building an AI assistant that generates three results for a programming topic:

1. A summary.
2. Interview questions.
3. An example.

Each task can work independently.

Instead of writing three separate model invocations manually, we can combine these operations into one LCEL workflow.

### Benefits

- Clearer workflow organization.
- Multiple outputs in one dictionary.
- Reusable parallel processing.
- Easy integration with sequential operations.
- Useful for AI assistants, RAG, and data-processing applications.

## 3. Basic Example Without an LLM

First, define some Runnables.

```python
from langchain_core.runnables import RunnableLambda

identity = RunnableLambda(lambda x: x)
double = RunnableLambda(lambda x: x * 2)
square = RunnableLambda(lambda x: x ** 2)
```

Now compose them:

```python
chain = identity | {
    "double": double,
    "square": square
}

result = chain.invoke(5)

print(result)
```

Expected output:

```python
{
    "double": 10,
    "square": 25
}
```

### Explanation

- The first Runnable receives `5` and forwards it.
- LangChain converts the dictionary into a parallel stage.
- Both branches receive `5`.
- The outputs are combined into a dictionary.

## 4. Dictionary Composition vs RunnableParallel

We can create the same workflow explicitly.

### Explicit RunnableParallel

```python
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    double=double,
    square=square
)

print(chain.invoke(5))
```

### Dictionary Composition

```python
chain = identity | {
    "double": double,
    "square": square
}

print(chain.invoke(5))
```

Both produce:

```python
{
    "double": 10,
    "square": 25
}
```

### Comparison

| RunnableParallel                     | Dictionary Composition                  |
| ------------------------------------ | --------------------------------------- |
| Explicitly creates parallel branches | Uses dictionary syntax within LCEL      |
| Can be invoked directly              | Converted when composed with a Runnable |
| Clear component declaration          | Concise syntax                          |
| Same general execution behavior      | Same general execution behavior         |

**Important:** A plain Python dictionary does not have an `invoke()` method.

This will not work:

```python
branches = {
    "double": double,
    "square": square
}

# Incorrect:
# branches.invoke(5)
```

To invoke the mapping directly, wrap it:

```python
chain = RunnableParallel(branches)

print(chain.invoke(5))
```

## 5. Understanding Input Distribution

Consider:

```python
chain = identity | {
    "double": double,
    "square": square
}
```

The execution flow is:

```text
           Input: 5
              |
              v
         Identity
              |
              v
              5
              |
       +------+------+
       |             |
       v             v
     Double        Square
       |             |
       v             v
      10            25
       |             |
       +------+------+
              |
              v
  {"double": 10, "square": 25}
```

Both branches receive the same input.

They do not automatically receive each other's outputs.

## 6. Dictionary Composition After a Transformation

We can add a processing step before the dictionary.

```python
add_one = RunnableLambda(lambda x: x + 1)

chain = add_one | {
    "double": double,
    "square": square
}

print(chain.invoke(5))
```

Expected output:

```python
{
    "double": 12,
    "square": 36
}
```

Explanation:

1. Input is `5`.
2. `add_one` produces `6`.
3. Both dictionary branches receive `6`.
4. The double branch returns `12`.
5. The square branch returns `36`.

The dictionary stage receives the output of the previous Runnable, not necessarily the original user input.

## 7. Dictionary Keys and Values

Consider:

```python
chain = identity | {
    "multiplication": RunnableLambda(lambda x: x * 10),
    "addition": RunnableLambda(lambda x: x + 10)
}
```

The dictionary keys determine the names of the output fields.

Example:

```python
result = chain.invoke(5)

print(result["multiplication"])
print(result["addition"])
```

Expected output:

```text
50
15
```

The keys themselves do not perform operations.

The Runnable values perform the processing.

## 8. Using Different Output Types

Not every branch must return a string.

Example:

```python
chain = identity | {
    "original": RunnableLambda(lambda x: x),
    "length": RunnableLambda(lambda x: len(x)),
    "uppercase": RunnableLambda(lambda x: x.upper())
}

result = chain.invoke("python")

print(result)
```

Expected output:

```python
{
    "original": "python",
    "length": 6,
    "uppercase": "PYTHON"
}
```

One branch returns an integer while the others return strings.

Dictionary composition can combine different result types.

## 9. Dictionary Composition with Groq

Now we'll create an AI study assistant.

### Initialize the Model

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

### Create Two Prompts

```python
from langchain_core.prompts import PromptTemplate

summary_prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in three sentences."
)

questions_prompt = PromptTemplate.from_template(
    "Generate exactly three interview questions about {topic}."
)
```

### Create the Chains

```python
from langchain_core.output_parsers import StrOutputParser

summary_chain = summary_prompt | model | StrOutputParser()

questions_chain = questions_prompt | model | StrOutputParser()
```

### Compose Them Using a Dictionary

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough() | {
    "summary": summary_chain,
    "questions": questions_chain
}
```

### Execute

```python
result = chain.invoke({
    "topic": "Python Decorators"
})

print(str(result["summary"]))
print(str(result["questions"]))
```

Both chains receive the same input dictionary.

The final result contains two fields.

## 10. Preserving the Original Input

Suppose we also want the original topic in our final result.

We can create an additional branch:

```python
from langchain_core.runnables import RunnableLambda

chain = RunnablePassthrough() | {
    "topic": RunnableLambda(lambda data: data["topic"]),
    "summary": summary_chain,
    "questions": questions_chain
}
```

The output will have the following structure:

```python
{
    "topic": "Python Decorators",
    "summary": "...",
    "questions": "..."
}
```

This is useful when the application must return both the original request and generated information.

## 11. Using RunnablePassthrough.assign()

There is another useful way to preserve dictionary fields while adding generated results.

```python
chain = RunnablePassthrough.assign(
    summary=summary_chain,
    questions=questions_chain
)
```

Execute:

```python
result = chain.invoke({
    "topic": "Python Decorators"
})
```

The original `topic` field is preserved, and the generated fields are added.

### Difference

**Dictionary composition:**

```python
chain = RunnablePassthrough() | {
    "summary": summary_chain,
    "questions": questions_chain
}
```

Returns only the keys defined in the output dictionary.

**RunnablePassthrough.assign():**

```python
chain = RunnablePassthrough.assign(
    summary=summary_chain,
    questions=questions_chain
)
```

Keeps existing dictionary fields and adds new fields.

This distinction is useful for real applications.

## 12. Adding a Formatting Step After the Dictionary

We can connect another Runnable after the parallel stage.

```python
def format_results(data):
    return (
        "SUMMARY:\n"
        + str(data["summary"])
        + "\n\nQUESTIONS:\n"
        + str(data["questions"])
    )

formatter = RunnableLambda(format_results)

chain = (
    RunnablePassthrough()
    | {
        "summary": summary_chain,
        "questions": questions_chain
    }
    | formatter
)
```

The parallel stage produces a dictionary.

The formatter receives that dictionary and creates a readable text response.

### Execution Flow

```text
              Topic
                |
                v
         RunnablePassthrough
                |
        +-------+-------+
        |               |
        v               v
    Summary Chain   Questions Chain
        |               |
        +-------+-------+
                |
                v
          Dictionary
                |
                v
          Formatter
                |
                v
        Final Text Output
```

This demonstrates how LCEL can mix sequential and parallel processing.

## 13. Nested Dictionary Composition

We can build more complex workflows using nested RunnableParallel stages.

Example:

```python
chain = RunnableParallel(
    original=RunnablePassthrough(),
    calculations=RunnableParallel(
        double=RunnableLambda(lambda x: x * 2),
        square=RunnableLambda(lambda x: x ** 2)
    )
)
```

For input `5`:

```python
{
    "original": 5,
    "calculations": {
        "double": 10,
        "square": 25
    }
}
```

Nested output structures can help organize larger applications.

However, deeply nested pipelines can become difficult to understand and debug.

## 14. Dictionary Composition in RAG

RAG stands for Retrieval-Augmented Generation.

In a typical RAG application, we need two pieces of information:

- The user's question.
- Relevant documents retrieved from a knowledge source.

LCEL dictionary composition can combine both.

Conceptual example:

```python
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | model
    | StrOutputParser()
)
```

Here:

- The retriever produces the context.
- RunnablePassthrough preserves the original question.
- The prompt receives both fields.
- The model generates an answer.

This example requires a configured retriever and RAG prompt.

We will implement it later when studying retrievers and RAG.

## 15. Concurrency and API Usage

Dictionary composition can create concurrent processing branches.

If both branches call Groq, they normally make separate model requests.

For example:

```python
{
    "summary": summary_chain,
    "questions": questions_chain
}
```

contains two LLM branches.

This usually results in two model requests for each invocation.

Parallel processing can reduce waiting time, but it does not automatically reduce total API usage.

Be mindful of provider rate limits.

## 16. Error Handling

If one branch raises an exception, the combined workflow normally raises an exception.

Example:

```python
try:
    result = chain.invoke({
        "topic": "Python"
    })
    print(result)
except Exception as error:
    print("Execution failed:", error)
```

Applications that require partial results need explicit error-handling logic or other failure-management strategies.

## 17. Common Beginner Mistakes

**Mistake 1 — Assuming a Python dictionary is itself a Runnable**

A dictionary must be coerced through supported LCEL composition or wrapped with RunnableParallel.

**Mistake 2 — Assuming branches receive each other's outputs**

Independent branches receive the same input at that stage.

**Mistake 3 — Forgetting required prompt variables**

Each branch must receive compatible data.

**Mistake 4 — Confusing output keys with prompt variables**

Dictionary keys identify output fields; prompt variables identify required inputs.

**Mistake 5 — Assuming parallel execution means one API request**

Each LLM branch can make its own request.

**Mistake 6 — Forgetting original fields**

A normal RunnableParallel output contains only the defined branch results. Use a passthrough branch or `assign()` to preserve other fields.

## 18. Interview Questions

**Q1. What is dictionary composition in LCEL?**

Using a dictionary of compatible processing operations within a Runnable workflow.

**Q2. What happens when a dictionary is composed with a Runnable?**

LangChain can convert it into RunnableParallel.

**Q3. What does RunnableParallel return?**

A dictionary containing branch results.

**Q4. Does each branch receive the same input?**

Yes, the same input from the preceding stage.

**Q5. Can dictionary composition work without an LLM?**

Yes.

**Q6. Can different branches return different data types?**

Yes.

**Q7. What is the difference between RunnableParallel and RunnablePassthrough.assign()?**

RunnableParallel creates a mapping of branch results, while assign preserves existing dictionary fields and adds computed ones.

**Q8. Can dictionary composition be combined with sequential steps?**

Yes.

**Q9. Why is dictionary composition useful in RAG?**

It helps combine retrieved context and the original question.

**Q10. Does dictionary composition reduce LLM API calls?**

Not automatically.

## 19. Key Takeaways

- LCEL supports dictionary composition.
- Dictionaries of Runnables can be converted to RunnableParallel during composition.
- Every branch receives the same input at its stage.
- Results are combined in a dictionary.
- Dictionary keys determine the output field names.
- Multiple branches can return different data types.
- RunnablePassthrough.assign() preserves original dictionary fields.
- Dictionary stages can be combined with sequential transformations.
- Dictionary composition is useful in RAG and structured AI workflows.

---

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [LangChain RunnableParallel Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableParallel)
- [LangChain RunnablePassthrough Reference](https://reference.langchain.com/python/langchain-core/runnables/passthrough/RunnablePassthrough)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 09 — Topic 03
