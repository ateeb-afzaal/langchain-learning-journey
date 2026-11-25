# 04 — RunnablePassthrough in LangChain

## 1. What Is RunnablePassthrough?

`RunnablePassthrough` is a LangChain component that forwards its input without changing it.

In simple words:

**Input → RunnablePassthrough → Same Input**

Example:

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

result = passthrough.invoke("Hello LangChain")

print(result)
```

Output:

```text
Hello LangChain
```

The input and output are the same.

## 2. Why Do We Need RunnablePassthrough?

In many AI applications, we want to preserve the original information while generating additional results.

For example, suppose we have:

```python
question = "What is Machine Learning?"
```

Our AI application generates an answer to that question.

We may want the final output to contain both:

```python
{
    "question": "What is Machine Learning?",
    "answer": "Machine learning is a field of AI..."
}
```

`RunnablePassthrough` allows us to preserve the question while another Runnable generates the answer.

### Common Applications

- Preserving user questions
- Combining original input with LLM responses
- Building RAG pipelines
- Preserving document metadata
- Adding calculated fields to dictionaries
- Connecting multiple processing branches

## 3. Importing RunnablePassthrough

```python
from langchain_core.runnables import RunnablePassthrough
```

No additional package is required beyond `langchain-core`.

## 4. Basic Example

```python
passthrough = RunnablePassthrough()

result = passthrough.invoke(10)

print(result)
```

Output:

```text
10
```

Another example:

```python
result = passthrough.invoke({
    "name": "Ali",
    "age": 22
})

print(result)
```

Output:

```python
{
    "name": "Ali",
    "age": 22
}
```

The dictionary passes through without transformation.

**Note:** Passthrough does not automatically make a deep copy of the input. Avoid modifying shared mutable data in other branches.

## 5. RunnablePassthrough with RunnableParallel

This is one of the most useful patterns.

Suppose we want to preserve an input number and calculate its square.

```python
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel
)

parallel = RunnableParallel(
    original=RunnablePassthrough(),
    square=RunnableLambda(lambda x: x ** 2)
)

result = parallel.invoke(5)

print(result)
```

Output:

```python
{
    "original": 5,
    "square": 25
}
```

### Explanation

- `RunnableParallel` sends `5` to both branches.
- `RunnablePassthrough` returns `5`.
- `RunnableLambda` calculates `25`.
- The results are combined into a dictionary.

## 6. Understanding Data Flow

```text
                    Input: 5
                       |
                       v
                RunnableParallel
                       |
             +---------+---------+
             |                   |
             v                   v
     RunnablePassthrough    RunnableLambda
             |                   |
             v                   v
             5                  25
             |                   |
             +---------+---------+
                       |
                       v
          {"original": 5, "square": 25}
```

## 7. What Is RunnablePassthrough.assign()?

`RunnablePassthrough.assign()` is used to add new fields to an existing dictionary.

The existing fields are preserved, and the new fields are calculated using Runnables or compatible functions.

### Example

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough.assign(
    full_name=lambda data: (
        data["first_name"] + " " + data["last_name"]
    )
)

result = chain.invoke({
    "first_name": "Ali",
    "last_name": "Khan"
})

print(result)
```

Output:

```python
{
    "first_name": "Ali",
    "last_name": "Khan",
    "full_name": "Ali Khan"
}
```

### Important

`assign()` expects a dictionary input.

It adds calculated fields to that dictionary.

If an assigned field has the same name as an existing field, the generated value replaces the existing value under that key.

## 8. Adding Multiple Fields with assign()

We can calculate multiple new fields simultaneously.

```python
chain = RunnablePassthrough.assign(
    double=lambda data: data["number"] * 2,
    square=lambda data: data["number"] ** 2
)

result = chain.invoke({
    "number": 5
})

print(result)
```

Expected output:

```python
{
    "number": 5,
    "double": 10,
    "square": 25
}
```

This pattern is useful for building reusable data-processing pipelines.

## 9. RunnablePassthrough with Groq

Now let's create an AI application that preserves the original question and generates an answer.

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

### Create the Prompt

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template(
    "Answer the following question in 3 simple sentences: {question}"
)

answer_chain = prompt | model | StrOutputParser()
```

### Combine the Original Question and Generated Answer

```python
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)

chain = RunnableParallel(
    question=RunnablePassthrough(),
    answer=(
        {"question": RunnablePassthrough()}
        | answer_chain
    )
)

result = chain.invoke("What is Machine Learning?")

print("Question:", result["question"])
print("Answer:", str(result["answer"]))
```

### Explanation

The input is a plain string.

The `question` branch preserves that string.

The `answer` branch converts the input into the dictionary required by the prompt and then generates an answer.

The final output contains both fields.

## 10. Alternative: assign() with Groq

When the original input is already a dictionary, `assign()` can make the workflow simpler.

```python
chain = RunnablePassthrough.assign(
    answer=answer_chain
)

result = chain.invoke({
    "question": "What is Deep Learning?"
})

print(result["question"])
print(str(result["answer"]))
```

Here:

1. The input dictionary already contains `question`.
2. The answer chain receives that dictionary.
3. `assign()` adds an `answer` field.
4. The original `question` field remains available.

This pattern is particularly useful when several input fields need to be retained.

## 11. RunnablePassthrough in RAG Applications

RAG stands for **Retrieval-Augmented Generation**.

A typical RAG workflow retrieves relevant information before asking an LLM to generate an answer.

Example:

```text
                   User Question
                         |
                         v
                  RunnableParallel
                         |
               +---------+---------+
               |                   |
               v                   v
        RunnablePassthrough     Retriever
               |                   |
               v                   v
         Original Question    Relevant Documents
               |                   |
               +---------+---------+
                         |
                         v
                   RAG Prompt
                         |
                         v
                       LLM
                         |
                         v
                     Answer
```

The key idea is:

- Preserve the user's original question.
- Retrieve useful document context.
- Pass both question and context to the model.

### Conceptual RAG Example

The following illustrates the typical pattern. It requires a configured retriever and a prompt with `{context}` and `{question}` variables.

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

We will implement a complete working RAG application in later sections.

## 12. RunnablePassthrough vs RunnableLambda

| Feature                | RunnablePassthrough    | RunnableLambda                   |
| ---------------------- | ---------------------- | -------------------------------- |
| Main purpose           | Preserve input         | Transform input                  |
| Default behavior       | Return input unchanged | Execute Python function          |
| Example                | Return `5`             | Convert `5` into `25`            |
| Common use             | Preserve question      | Clean or modify text             |
| Dictionary enhancement | Supports `assign()`    | Can return a modified dictionary |

Both are useful when creating reusable LangChain workflows.

## 13. RunnablePassthrough vs RunnableParallel

These components perform different jobs.

`RunnablePassthrough` preserves data.

`RunnableParallel` runs multiple independent branches and combines their results.

They are often used together.

Example:

```python
parallel = RunnableParallel(
    original=RunnablePassthrough(),
    doubled=RunnableLambda(lambda x: x * 2)
)
```

## 14. Common Beginner Mistakes

**Mistake 1 — Assuming RunnablePassthrough changes input**

Its default behavior is to return the input unchanged.

**Mistake 2 — Assuming assign() works directly on any string**

`RunnablePassthrough.assign()` expects dictionary input.

**Mistake 3 — Confusing Passthrough with Parallel**

Passthrough preserves input, while Parallel coordinates independent processing branches.

**Mistake 4 — Forgetting prompt variables**

If a prompt expects `{question}`, it needs a compatible input containing that variable.

**Mistake 5 — Thinking Passthrough automatically retrieves documents**

Document retrieval requires a retriever. Passthrough only preserves information.

## 15. Interview Questions

**Q1. What is RunnablePassthrough?**

A LangChain Runnable that forwards its input unchanged.

**Q2. Why is RunnablePassthrough useful?**

It preserves original data while other processing steps generate additional information.

**Q3. What does RunnablePassthrough.assign() do?**

Adds calculated fields to an existing dictionary.

**Q4. Does assign() require dictionary input?**

Yes.

**Q5. Can RunnablePassthrough work without an LLM?**

Yes.

**Q6. What is the difference between RunnablePassthrough and RunnableLambda?**

Passthrough preserves input, while Lambda uses a Python function to process input.

**Q7. What is the difference between RunnablePassthrough and RunnableParallel?**

Passthrough forwards input, whereas Parallel runs independent branches and combines results.

**Q8. Why is RunnablePassthrough important in RAG?**

It can preserve the user's original question while relevant context is retrieved.

**Q9. Can assign() add multiple fields?**

Yes.

**Q10. Does RunnablePassthrough automatically call an LLM?**

No.

## 16. Key Takeaways

- `RunnablePassthrough` forwards data unchanged.
- It can preserve original input while other Runnables process that input.
- It is often combined with `RunnableParallel`.
- `RunnablePassthrough.assign()` adds fields to dictionaries.
- It can work with ordinary Python functions and LLM chains.
- Preserving original questions is useful in RAG applications.
- RunnablePassthrough does not automatically retrieve documents or generate model responses.

---

## Learning Resources

- [LangChain RunnablePassthrough Reference](https://reference.langchain.com/python/langchain-core/runnables/passthrough/RunnablePassthrough)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 — Topic 04
