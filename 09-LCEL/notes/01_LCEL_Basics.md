# 01 — LCEL Basics in LangChain

## 1. What Is LCEL?

**LCEL** stands for **LangChain Expression Language**.

LCEL is a way of connecting compatible LangChain components into reusable workflows using the pipe operator (`|`).

For example:

```python
chain = prompt | model | parser
```

This creates a processing pipeline where the output of each component becomes the input of the next component.

LCEL is built on LangChain's Runnable interface.

### Basic Workflow

```text
User Input
    |
    v
PromptTemplate
    |
    v
Language Model
    |
    v
Output Parser
    |
    v
Final Result
```

## 2. Why Do We Need LCEL?

Imagine building an AI assistant that explains Python programming concepts.

The application needs to:

1. Receive a topic.
2. Prepare instructions for the model.
3. Generate an explanation.
4. Extract the generated text.

Without LCEL, we can manually execute these operations.

```python
formatted_prompt = prompt.invoke({
    "topic": "Python decorators"
})

response = model.invoke(formatted_prompt)

result = parser.invoke(response)

print(result)
```

With LCEL:

```python
chain = prompt | model | parser

result = chain.invoke({
    "topic": "Python decorators"
})

print(result)
```

### Benefits of LCEL

- Reduces repetitive code.
- Improves readability.
- Makes workflows reusable.
- Connects prompts, models, parsers, and functions.
- Supports sequential and parallel composition.
- Supports batching and asynchronous execution.
- Supports streaming when components allow it.

## 3. Understanding the Pipe Operator

The pipe operator (`|`) connects compatible Runnables.

```python
chain = runnable_1 | runnable_2 | runnable_3
```

The execution order is:

```text
Input
  |
  v
Runnable 1
  |
  v
Runnable 2
  |
  v
Runnable 3
  |
  v
Output
```

### Example Without an LLM

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

chain = double | add_five

print(chain.invoke(10))
```

Output:

```text
25
```

Explanation:

- Input: 10
- Double: 20
- Add 5: 25

The order matters.

## 4. What Is Runnable Composition?

Runnable composition means combining multiple processing components into one executable workflow.

For example:

```python
chain = double | add_five
```

This creates a `RunnableSequence`.

We can inspect its type:

```python
print(type(chain))
```

Expected type:

```text
<class 'langchain_core.runnables.base.RunnableSequence'>
```

The exact module path shown in the terminal may depend on the installed LangChain version.

## 5. LCEL with PromptTemplate and Groq

Let's create an AI explanation workflow.

### Step 1 — Import Libraries

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
```

### Step 2 — Load Environment Variables

```python
load_dotenv()
```

This loads the Groq API key from the local `.env` file.

### Step 3 — Initialize the Model

```python
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

### Step 4 — Create the Prompt

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} in 3 simple sentences."
)
```

### Step 5 — Create the LCEL Chain

```python
chain = prompt | model | StrOutputParser()
```

### Step 6 — Execute

```python
result = chain.invoke({
    "topic": "Machine Learning"
})

print(str(result))
```

The chain executes all three components.

## 6. Understanding Input and Output Types

Every component expects a compatible input format.

| Component         | Input                             | Output                     |
| ----------------- | --------------------------------- | -------------------------- |
| `PromptTemplate`  | Dictionary                        | PromptValue                |
| `ChatGroq`        | Supported prompt or messages      | AIMessage                  |
| `StrOutputParser` | AIMessage or supported text input | Text                       |
| `RunnableLambda`  | Depends on Python function        | Depends on Python function |

### Example

The user provides:

```python
{"topic": "Machine Learning"}
```

The prompt transforms this into formatted instructions.

The model then generates an `AIMessage`.

The parser extracts the text.

This is why:

```python
prompt | model | parser
```

works: the data types are compatible.

## 7. LCEL with Ordinary Python Functions

LCEL does not require an LLM.

Example:

```python
from langchain_core.runnables import RunnableLambda

clean_text = RunnableLambda(
    lambda text: text.strip()
)

uppercase = RunnableLambda(
    lambda text: text.upper()
)

add_prefix = RunnableLambda(
    lambda text: "Processed: " + text
)

chain = clean_text | uppercase | add_prefix

result = chain.invoke("  hello langchain  ")

print(result)
```

Output:

```text
Processed: HELLO LANGCHAIN
```

This shows how LCEL can be used for ordinary data processing.

## 8. Understanding invoke()

`invoke()` executes a chain with one input.

```python
result = chain.invoke("hello")
```

If the chain expects a dictionary, we must provide the appropriate fields.

```python
result = ai_chain.invoke({
    "topic": "Python"
})
```

## 9. Understanding batch()

`batch()` processes multiple inputs through the same workflow.

```python
results = ai_chain.batch(
    [
        {"topic": "Python"},
        {"topic": "SQL"},
        {"topic": "FastAPI"}
    ],
    config={"max_concurrency": 2}
)
```

The outputs correspond to the input order.

Batch processing may involve multiple provider requests.

## 10. Understanding stream()

`stream()` can produce incremental output when the workflow supports streaming.

```python
for chunk in ai_chain.stream({
    "topic": "Artificial Intelligence"
}):
    print(str(chunk), end="", flush=True)
```

This is useful for AI assistants that display responses progressively.

Not every Runnable streams multiple chunks.

## 11. Inspecting an LCEL Chain

LangChain provides methods for examining Runnable workflows.

### Inspect the Chain Type

```python
print(type(chain))
```

### Inspect the Steps

For a `RunnableSequence`:

```python
print(chain.steps)
```

This returns the processing components within the sequence.

### Inspect the Graph

```python
graph = chain.get_graph()

print(graph.draw_ascii())
```

This attempts to display the chain's structure as an ASCII diagram.

Depending on the installed packages and LangChain version, ASCII graph rendering may require an additional dependency such as `grandalf`.

Install it when needed:

```powershell
python -m pip install grandalf
```

### Why Is Graph Inspection Useful?

It helps us:

- Understand workflow structure.
- Identify processing stages.
- Debug complex pipelines.
- Document our AI architecture.

## 12. LCEL vs RunnableSequence

LCEL is the composition syntax and approach.

`RunnableSequence` is one of the concrete Runnable components used to execute a sequence.

For example:

```python
chain = double | add_five
```

creates a RunnableSequence.

The same sequence can be written explicitly:

```python
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    double,
    add_five
)
```

Both approaches execute the same operations.

## 13. LCEL vs RunnableParallel

LCEL also supports parallel composition.

Example:

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2)
)

print(parallel.invoke(5))
```

Output:

```python
{
    "double": 10,
    "square": 25
}
```

We can combine parallel and sequential operations within larger LCEL workflows.

## 14. LCEL vs Traditional Python

| Feature                  | Traditional Python               | LCEL                           |
| ------------------------ | -------------------------------- | ------------------------------ |
| Execute functions        | Direct function calls            | Runnable methods               |
| Connect processing steps | Manual composition               | Pipe operator                  |
| Batch execution          | Implement or coordinate manually | Runnable batch interface       |
| Streaming                | Implement or coordinate manually | Runnable streaming interface   |
| Workflow inspection      | Custom debugging                 | Runnable graph inspection      |
| Best for                 | General programming              | Composable LangChain workflows |

LCEL does not replace ordinary Python.

Instead, it provides a convenient framework for composing compatible processing components.

## 15. Common Beginner Mistakes

**Mistake 1 — Thinking LCEL is an AI model**

LCEL is a way of connecting processing components.

**Mistake 2 — Assuming the pipe operator works with every Python object**

The components must be compatible with LangChain's composition system.

**Mistake 3 — Ignoring data types**

The output of one Runnable must be acceptable to the next.

**Mistake 4 — Assuming every chain requires an LLM**

LCEL can connect ordinary Python functions.

**Mistake 5 — Assuming batch() is one API request**

It may make multiple API calls.

**Mistake 6 — Assuming every chain supports token-by-token streaming**

Streaming depends on the components.

## 16. Interview Questions

**Q1. What is LCEL?**

LangChain Expression Language, used to compose compatible processing components.

**Q2. What does the pipe operator do?**

Connects Runnables into workflows.

**Q3. What is Runnable composition?**

Combining processing components into a reusable workflow.

**Q4. What is a RunnableSequence?**

A component that executes connected Runnables in order.

**Q5. Does LCEL require a language model?**

No.

**Q6. What does invoke() do?**

Processes one input.

**Q7. What does batch() do?**

Processes multiple inputs.

**Q8. What does stream() do?**

Produces incremental output when supported.

**Q9. How can we inspect a chain?**

Using methods such as `get_graph()` and, for sequences, inspecting `steps`.

**Q10. Why is input/output compatibility important?**

Each component must be able to process the preceding component's output.

## 17. Key Takeaways

- LCEL stands for LangChain Expression Language.
- LCEL composes compatible Runnables.
- The pipe operator connects processing steps.
- A pipe-based sequence creates a RunnableSequence.
- LCEL works with LLM and non-LLM components.
- Runnables share execution methods such as invoke, batch, and stream.
- Input and output types must be compatible.
- LCEL workflows can be inspected using graph utilities.
- LCEL provides a foundation for more advanced LangChain and RAG workflows.

---

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [LangChain Runnable Reference](https://reference.langchain.com/python/langchain-core/runnables/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 09 — Topic 01
