# 01 — Chains Basics in LangChain

## 1. What Is a Chain?

A **chain** is a workflow that connects multiple processing steps to complete a task.

In LangChain, these steps can include:

- Prompt templates
- Language models
- Output parsers
- Python functions
- Retrievers
- Other chains

Instead of manually calling each component, we can connect them into one reusable workflow.

### Example

```text
User Question
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

This is an example of a simple chain.

## 2. Why Do We Need Chains?

Imagine building an application that explains programming concepts.

Without a chain, we might manually perform each operation:

```python
formatted_prompt = prompt.invoke({"topic": "Python"})
response = model.invoke(formatted_prompt)
answer = parser.invoke(response)

print(answer)
```

With a chain:

```python
chain = prompt | model | parser

answer = chain.invoke({"topic": "Python"})

print(answer)
```

Both approaches accomplish the same basic task.

### Benefits of Chains

- Reduce repetitive code.
- Make workflows reusable.
- Separate application components.
- Allow multiple steps to be combined.
- Support sequential, parallel, and conditional processing.
- Provide a common interface for execution.

## 3. What Is LCEL?

**LCEL** stands for LangChain Expression Language.

It is a declarative way to connect LangChain components into workflows.

LCEL commonly uses the pipe operator:

```python
|
```

Example:

```python
chain = prompt | model | parser
```

This means:

1. The prompt receives the input.
2. The formatted prompt is passed to the model.
3. The model generates a response.
4. The response is passed to the parser.
5. The parser returns the final result.

We will study LCEL in greater detail in Section 09.

## 4. Understanding the Pipe Operator

In LangChain, the `|` operator connects compatible runnable components.

Example:

```python
chain = prompt | model
```

We can add an output parser:

```python
chain = prompt | model | StrOutputParser()
```

The result is a runnable sequence.

**Important:** The pipe operator does not mean that ordinary Python objects can always be connected. The components must be compatible with LangChain's runnable composition system.

## 5. What Is a Runnable?

A **Runnable** is a LangChain abstraction that provides a common interface for executing processing components.

Examples of runnable components include:

- `PromptTemplate`
- `ChatPromptTemplate`
- Chat models
- Output parsers
- `RunnableLambda`
- `RunnableSequence`
- `RunnableParallel`
- `RunnableBranch`

### Important Runnable Methods

| Method      | Purpose                                       |
| ----------- | --------------------------------------------- |
| `invoke()`  | Process one input                             |
| `batch()`   | Process multiple inputs                       |
| `stream()`  | Produce output incrementally, where supported |
| `ainvoke()` | Asynchronous invocation                       |
| `abatch()`  | Asynchronous batch processing                 |
| `astream()` | Asynchronous streaming, where supported       |

Different components may implement these capabilities differently.

## 6. Using invoke()

`invoke()` executes a runnable with one input.

```python
result = chain.invoke({
    "topic": "Machine Learning"
})

print(result)
```

This is the method we have used throughout our learning journey.

## 7. Using batch()

`batch()` processes multiple inputs.

```python
topics = [
    {"topic": "Python"},
    {"topic": "Machine Learning"},
    {"topic": "Neural Networks"}
]

results = chain.batch(topics)

for result in results:
    print(result)
```

Each input is processed through the same workflow.

**Important:** Batch execution does not necessarily mean a provider performs all requests as one API call. It may execute multiple requests concurrently, depending on the runnable implementation.

## 8. Using stream()

`stream()` allows us to receive output incrementally when supported by the components.

```python
for chunk in chain.stream({
    "topic": "Artificial Intelligence"
}):
    print(chunk, end="", flush=True)
```

This can make AI applications feel more responsive because users can see output as it is generated.

Streaming behavior depends on the underlying model and the connected components.

## 9. Building a Simple Chain with Groq

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
    "Explain {topic} to a beginner in three sentences."
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({
    "topic": "Python decorators"
})

print(result)
```

### Code Explanation

**`load_dotenv()`**

Loads the Groq API key from the local environment.

**`ChatGroq()`**

Creates the chat model integration.

**`PromptTemplate.from_template()`**

Defines a reusable prompt containing `{topic}`.

**`StrOutputParser()`**

Extracts text from the model response.

**`prompt | model | parser`**

Combines the components into one runnable workflow.

**`chain.invoke()`**

Executes the complete workflow.

## 10. Types of Chains

### A. Simple Chain

A straightforward sequence of operations.

```text
Prompt → Model → Parser
```

### B. Sequential Chain

One operation depends on the result of a previous operation.

```text
Input
  |
  v
Generate Summary
  |
  v
Translate Summary
  |
  v
Final Result
```

### C. Parallel Chain

Multiple independent operations receive input and generate separate results.

```text
             Input
               |
        +------+------+
        |             |
        v             v
     Summary         Quiz
        |             |
        +------+------+
               |
               v
        Combined Results
```

### D. Conditional Chain

The workflow selects a branch based on a condition.

```text
User Input
    |
    v
Check Condition
    |
    +---- Beginner ----> Simple Explanation
    |
    +---- Advanced ----> Technical Explanation
```

We'll build each of these in the upcoming topics.

## 11. Chains vs Agents

Both chains and agents can perform multiple steps, but their approaches differ.

| Chains                                       | Agents                                         |
| -------------------------------------------- | ---------------------------------------------- |
| Usually follow predefined workflows          | Can dynamically choose available tools         |
| Suitable for predictable processing          | Suitable for tasks requiring decisions         |
| Steps are typically configured by developers | Action selection may be determined by an LLM   |
| Example: Summarize then translate            | Example: Decide whether to search or calculate |

Not every AI application needs an agent.

For predictable tasks, a chain is often simpler and easier to test.

## 12. Chains vs Plain Python Functions

A chain is not the only way to build a workflow.

We could write:

```python
def explain_topic(topic):
    formatted = prompt.invoke({"topic": topic})
    response = model.invoke(formatted)
    return parser.invoke(response)
```

That is a valid Python approach.

LangChain chains are useful when we want reusable runnable interfaces, composition, batching, streaming, and integrations with other LangChain components.

## 13. Common Beginner Mistakes

**Mistake 1 — Assuming chains are AI models**

A chain is a workflow. It may contain an AI model, but the chain itself is not necessarily a model.

**Mistake 2 — Confusing prompt.invoke() and chain.invoke()**

`prompt.invoke()` formats the prompt.

`chain.invoke()` executes all connected steps.

**Mistake 3 — Assuming every chain requires an LLM**

Some chains can connect ordinary Python functions or other non-LLM processing components.

**Mistake 4 — Assuming batch() is one API request**

Batching can involve multiple underlying model requests.

**Mistake 5 — Using outdated chain classes without checking compatibility**

Some older LangChain tutorials use classes such as `LLMChain` and `SequentialChain`. Modern applications commonly use runnable composition.

## 14. Interview Questions

**Q1. What is a chain in LangChain?**

A workflow that connects multiple processing steps.

**Q2. What is LCEL?**

LangChain Expression Language, used for composing runnable components.

**Q3. What does the pipe operator (`|`) do?**

Connects compatible components into a runnable workflow.

**Q4. What is a Runnable?**

A LangChain abstraction that provides a common execution interface.

**Q5. What does invoke() do?**

Processes one input.

**Q6. What does batch() do?**

Processes multiple inputs.

**Q7. What does stream() do?**

Returns incremental output where supported.

**Q8. What is the difference between sequential and parallel chains?**

Sequential chains connect dependent steps, while parallel chains execute independent branches.

**Q9. What is a conditional chain?**

A workflow that selects different processing branches based on a condition.

**Q10. How is a chain different from an agent?**

A chain usually follows predefined logic, while an agent can dynamically decide which tools or actions to use.

## 15. Key Takeaways

- Chains combine multiple operations into reusable workflows.
- LCEL provides a convenient way to connect LangChain components.
- The `|` operator connects compatible runnables.
- `invoke()` processes one input.
- `batch()` processes multiple inputs.
- `stream()` provides incremental output when supported.
- Chains can be simple, sequential, parallel, or conditional.
- Chains are useful when application workflows are predictable.
- Modern LangChain applications commonly use runnable composition.

---

## Learning Resources

- [CampusX LangChain Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 07 — Topic 01
