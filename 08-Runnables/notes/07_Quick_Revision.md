# 07 — LangChain Runnables: Quick Revision

## 1. What Is a Runnable?

A **Runnable** is a LangChain component that follows a standard interface for processing inputs and producing outputs.

Runnables can perform ordinary Python operations or work with AI models.

Examples include:

- PromptTemplate
- ChatGroq
- StrOutputParser
- RunnableSequence
- RunnableParallel
- RunnablePassthrough
- RunnableLambda
- RunnableBranch

Runnables are important because they make LangChain components reusable and composable.

---

## 2. The Four Main Runnables We Studied

| Runnable              | Purpose                      | Simple Example      |
| --------------------- | ---------------------------- | ------------------- |
| `RunnableSequence`    | Execute operations in order  | Double → Square     |
| `RunnableParallel`    | Execute independent branches | Double and Square   |
| `RunnablePassthrough` | Preserve original input      | Input 5 → Output 5  |
| `RunnableLambda`      | Wrap a Python function       | Input 5 → Output 10 |

## 3. RunnableSequence

`RunnableSequence` connects several operations.

Each operation receives the output of the previous one.

```python
from langchain_core.runnables import (
    RunnableLambda,
    RunnableSequence
)

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)

sequence = RunnableSequence(double, add_five)

print(sequence.invoke(5))
```

**Output:**

```text
15
```

The same sequence can be written using LCEL:

```python
sequence = double | add_five
```

### Remember

- Processing happens in order.
- Each step depends on the previous step's output.
- The pipe operator (`|`) connects compatible Runnables.

---

## 4. RunnableParallel

`RunnableParallel` executes independent branches.

All branches receive the same input.

```python
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel
)

parallel = RunnableParallel(
    double=RunnableLambda(lambda x: x * 2),
    square=RunnableLambda(lambda x: x ** 2),
    cube=RunnableLambda(lambda x: x ** 3)
)

print(parallel.invoke(5))
```

**Output:**

```python
{
    "double": 10,
    "square": 25,
    "cube": 125
}
```

### Remember

- Every branch receives the same input.
- Results are returned in a dictionary.
- Independent branches can execute concurrently.
- Parallel model branches generally make separate API requests.

---

## 5. RunnablePassthrough

`RunnablePassthrough` forwards the input unchanged.

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

print(passthrough.invoke("Hello LangChain"))
```

**Output:**

```text
Hello LangChain
```

### RunnablePassthrough.assign()

`assign()` adds calculated fields to an existing dictionary.

```python
chain = RunnablePassthrough.assign(
    double=lambda data: data["number"] * 2,
    square=lambda data: data["number"] ** 2
)

result = chain.invoke({"number": 5})

print(result)
```

**Output:**

```python
{
    "number": 5,
    "double": 10,
    "square": 25
}
```

### Remember

- Preserves original input.
- `assign()` adds calculated fields to dictionaries.
- Useful for preserving user questions in RAG applications.
- Does not automatically retrieve documents or call an LLM.

---

## 6. RunnableLambda

`RunnableLambda` wraps an ordinary Python function as a Runnable.

```python
from langchain_core.runnables import RunnableLambda

uppercase = RunnableLambda(
    lambda text: text.upper()
)

print(uppercase.invoke("hello"))
```

**Output:**

```text
HELLO
```

We can also use regular Python functions.

```python
def clean_text(text):
    return text.strip().lower()

clean_runnable = RunnableLambda(clean_text)

print(clean_runnable.invoke("  HELLO  "))
```

**Output:**

```text
hello
```

### Remember

- Works with normal functions and lambda expressions.
- Supports Runnable methods.
- Can transform dictionaries and strings.
- Useful before or after an LLM call.
- Does not require a language model.

---

## 7. Six Important Runnable Methods

| Method      | Input           | Behavior                          |
| ----------- | --------------- | --------------------------------- |
| `invoke()`  | Single input    | Synchronous execution             |
| `batch()`   | Multiple inputs | Synchronous batch execution       |
| `stream()`  | Single input    | Incremental output when supported |
| `ainvoke()` | Single input    | Asynchronous execution            |
| `abatch()`  | Multiple inputs | Asynchronous batch execution      |
| `astream()` | Single input    | Asynchronous streaming            |

### invoke()

```python
result = double.invoke(5)
```

### batch()

```python
results = double.batch([2, 3, 4])
```

### stream()

```python
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="", flush=True)
```

### ainvoke()

```python
result = await double.ainvoke(5)
```

### abatch()

```python
results = await double.abatch([2, 3, 4])
```

### astream()

```python
async for chunk in chain.astream({"topic": "Python"}):
    print(chunk, end="", flush=True)
```

Asynchronous examples must run inside a suitable asynchronous context.

---

## 8. RunnableSequence vs RunnableParallel

| Feature        | RunnableSequence                   | RunnableParallel                |
| -------------- | ---------------------------------- | ------------------------------- |
| Execution      | Sequential                         | Concurrent where supported      |
| Dependencies   | Steps depend on earlier outputs    | Branches are independent        |
| Input handling | Previous result becomes next input | Shared input to all branches    |
| Output         | Final step's result                | Dictionary of branch results    |
| Example        | Explain then translate             | Summary and interview questions |

## 9. RunnableLambda vs RunnablePassthrough

| Feature           | RunnableLambda             | RunnablePassthrough                |
| ----------------- | -------------------------- | ---------------------------------- |
| Purpose           | Transform/process data     | Preserve original input            |
| Custom function   | Yes                        | Not required for basic passthrough |
| Default behavior  | Execute function           | Return input unchanged             |
| Dictionary fields | Can construct dictionaries | `assign()` can add fields          |
| RAG use           | Format retrieved context   | Preserve original question         |

---

## 10. Using Runnables with Groq

A typical LangChain pipeline:

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

print(str(result))
```

### Execution Flow

```text
Input Dictionary
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
Final Explanation
```

The entire workflow follows the Runnable interface.

---

## 11. What Is LCEL?

**LCEL** stands for LangChain Expression Language.

It allows developers to compose compatible Runnable components using the pipe operator.

Example:

```python
chain = prompt | model | parser
```

This automatically creates a sequential runnable workflow.

LCEL can also combine sequential and parallel processing.

---

## 12. How Runnables Help in RAG

RAG stands for Retrieval-Augmented Generation.

A common RAG workflow:

```text
User Question
      |
      v
Retrieve Relevant Documents
      |
      v
Prepare Context + Original Question
      |
      v
PromptTemplate
      |
      v
Language Model
      |
      v
Generated Answer
```

Runnables can help connect:

- Document retrievers
- Prompt templates
- Language models
- Output parsers
- Data transformation functions

A common pattern uses `RunnablePassthrough` to preserve the question while a retriever supplies context.

We will implement complete RAG pipelines in later sections.

---

## 13. Important Interview Questions

**Q1. What is a Runnable?**

A LangChain component that follows a common execution interface.

**Q2. What is RunnableSequence?**

A Runnable that executes processing steps sequentially.

**Q3. What is RunnableParallel?**

A Runnable that executes independent branches and combines the outputs.

**Q4. What is RunnablePassthrough?**

A Runnable that forwards its input unchanged.

**Q5. What is RunnableLambda?**

A Runnable that wraps a Python function.

**Q6. What is LCEL?**

LangChain Expression Language, used for Runnable composition.

**Q7. What does the pipe operator do?**

Connects compatible Runnables.

**Q8. What is the difference between invoke() and batch()?**

`invoke()` handles one input, while `batch()` handles multiple inputs.

**Q9. What is the difference between invoke() and ainvoke()?**

`invoke()` is synchronous, while `ainvoke()` is asynchronous.

**Q10. What is the difference between stream() and astream()?**

`stream()` uses synchronous iteration, while `astream()` uses asynchronous iteration.

**Q11. Does RunnableParallel reduce the number of API calls?**

No. Each model branch can still make a separate request.

**Q12. Does RunnableLambda require an LLM?**

No.

**Q13. What does RunnablePassthrough.assign() do?**

Adds computed fields to an existing dictionary.

**Q14. Can all Runnables stream tokens?**

No. Incremental streaming depends on the implementation.

**Q15. Why are Runnables useful in RAG?**

They connect retrieval, input preparation, model generation, and output processing.

---

## 14. Common Beginner Mistakes

1. Assuming every Runnable requires an LLM.
2. Assuming every Runnable produces streaming tokens.
3. Confusing sequential execution with parallel execution.
4. Forgetting input and output compatibility.
5. Thinking `batch()` always makes one API request.
6. Using `await` outside an asynchronous context.
7. Assuming `RunnablePassthrough.assign()` accepts arbitrary string input.
8. Confusing the Runnable interface with an AI agent.
9. Ignoring model provider rate limits.
10. Forgetting to handle API errors.

---

## 15. Practical Examples in This Section

| File                         | Topic                                                   |
| ---------------------------- | ------------------------------------------------------- |
| `01_runnable_basics.py`      | Basic Runnable operations                               |
| `02_runnable_sequence.py`    | Sequential workflows                                    |
| `03_runnable_parallel.py`    | Independent parallel branches                           |
| `04_runnable_passthrough.py` | Preserving input and adding fields                      |
| `05_runnable_lambda.py`      | Custom Python functions                                 |
| `06_runnable_methods.py`     | Synchronous, asynchronous, batch, and streaming methods |

### Testing Checklist

- [ ] Runnable Basics test passed
- [ ] RunnableSequence test passed
- [ ] RunnableParallel test passed
- [ ] RunnablePassthrough test passed
- [ ] RunnableLambda test passed
- [ ] Runnable Methods test passed

Update these checkboxes after confirming the terminal outputs.

---

## 16. Final Key Takeaways

- Runnables are fundamental building blocks of LangChain workflows.
- They provide a consistent execution interface.
- `RunnableSequence` connects dependent operations.
- `RunnableParallel` processes independent branches.
- `RunnablePassthrough` preserves original data.
- `RunnableLambda` integrates custom Python functions.
- Six common methods support single, batch, streaming, and asynchronous execution.
- LCEL makes Runnable composition convenient.
- Runnables are useful for chatbots, RAG applications, APIs, and other AI workflows.

---

## Learning Resources

- [LangChain Runnable Documentation](https://reference.langchain.com/python/langchain-core/runnables/)
- [LangChain Documentation](https://docs.langchain.com/)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 of 18

**Status:** Notes and examples prepared; execution verification pending.
