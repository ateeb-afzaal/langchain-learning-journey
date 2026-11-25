# 02 — RunnableSequence in LangChain

## 1. What Is RunnableSequence?

`RunnableSequence` is a LangChain component that connects multiple Runnables and executes them in a specific order.

The output of one Runnable becomes the input of the next Runnable.

In simple words:

**RunnableSequence = Step 1 → Step 2 → Step 3 → Final Output**

For example, we can create a workflow that:

1. Multiplies a number by two.
2. Adds five to the result.
3. Returns the final number.

## 2. Why Use RunnableSequence?

In real-world applications, many tasks require several processing steps.

Examples:

- Format a prompt → Call an LLM → Parse its response
- Extract text → Clean text → Analyze content
- Generate an explanation → Translate the explanation
- Retrieve documents → Prepare context → Generate an answer

`RunnableSequence` makes these workflows reusable and easier to maintain.

## 3. Basic RunnableSequence Example

First, create two Python operations.

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)
```

Now connect them:

```python
from langchain_core.runnables import RunnableSequence

sequence = RunnableSequence(
    double,
    add_five
)

result = sequence.invoke(5)
print(result)
```

Output:

```text
15
```

Explanation:

- Input = 5
- First step = 5 × 2 = 10
- Second step = 10 + 5 = 15

## 4. Using the Pipe Operator

Instead of writing:

```python
sequence = RunnableSequence(double, add_five)
```

We can write:

```python
sequence = double | add_five
```

Both create a sequential workflow.

The `|` operator is part of LangChain Expression Language (LCEL).

### Comparison

| Explicit                               | LCEL                        |
| -------------------------------------- | --------------------------- |
| `RunnableSequence(double, add_five)`   | `double \| add_five`        |
| Useful for understanding the component | Concise and readable        |
| Executes steps sequentially            | Executes steps sequentially |
| Produces the same result               | Produces the same result    |

## 5. Understanding Data Flow

Consider three operations:

```python
double = RunnableLambda(lambda x: x * 2)
add_five = RunnableLambda(lambda x: x + 5)
square = RunnableLambda(lambda x: x ** 2)

sequence = double | add_five | square
```

If we invoke:

```python
print(sequence.invoke(3))
```

The processing is:

```text
Input: 3
   |
   v
Multiply by 2
   |
   v
6
   |
   v
Add 5
   |
   v
11
   |
   v
Square
   |
   v
121
```

Final output:

```text
121
```

This demonstrates that the order of operations matters.

## 6. RunnableSequence with Groq

Let's connect a prompt, Groq model, and output parser.

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

sequence = prompt | model | parser

result = sequence.invoke({
    "topic": "Machine Learning"
})

print(str(result))
```

### Explanation

**PromptTemplate:** Receives the topic and prepares the prompt.

**ChatGroq:** Generates the explanation.

**StrOutputParser:** Extracts the model-generated text.

**RunnableSequence:** Connects the three components.

## 7. Explicit RunnableSequence with Groq

We can create the same workflow using the class directly.

```python
from langchain_core.runnables import RunnableSequence

sequence = RunnableSequence(
    prompt,
    model,
    parser
)
```

Then:

```python
result = sequence.invoke({
    "topic": "Python decorators"
})

print(str(result))
```

Both methods provide sequential execution.

## 8. Understanding invoke()

The `invoke()` method processes one input through the entire sequence.

```python
result = sequence.invoke({
    "topic": "Artificial Intelligence"
})
```

Each step runs in order.

For a prompt-model-parser sequence, the model normally makes one API request.

## 9. Understanding batch()

`batch()` processes multiple inputs through the sequence.

```python
topics = [
    {"topic": "Python"},
    {"topic": "Machine Learning"},
    {"topic": "Deep Learning"}
]

results = sequence.batch(
    topics,
    config={"max_concurrency": 2}
)

for result in results:
    print(str(result))
```

### Important

- Every input passes through the sequence.
- Outputs correspond to the inputs.
- Multiple requests may run concurrently.
- Batch execution does not necessarily mean one provider API request.

## 10. Understanding stream()

The `stream()` method produces incremental results when supported.

```python
for chunk in sequence.stream({
    "topic": "Neural Networks"
}):
    print(chunk, end="", flush=True)
```

A prompt-model-parser sequence can often stream generated text progressively.

However, not every Runnable supports incremental transformation.

For example, a normal `RunnableLambda` may prevent downstream streaming from starting until the function finishes processing its input.

For streaming custom transformations, LangChain also provides components such as `RunnableGenerator`.

## 11. Input and Output Compatibility

Each Runnable must accept the output generated by the previous Runnable.

Consider:

```python
double = RunnableLambda(lambda x: x * 2)
uppercase = RunnableLambda(lambda text: text.upper())

sequence = double | uppercase
```

If the input is an integer, the first step returns another integer.

But the second step expects a string.

Therefore, the sequence fails.

### Fix

Convert the intermediate output to a string:

```python
convert_to_text = RunnableLambda(lambda x: str(x))

sequence = double | convert_to_text | uppercase

print(sequence.invoke(5))
```

Output:

```text
10
```

The final result is a string.

## 12. RunnableSequence vs RunnableParallel

| RunnableSequence                              | RunnableParallel                       |
| --------------------------------------------- | -------------------------------------- |
| Executes steps in order                       | Executes independent branches          |
| Each step receives the previous step's output | Each branch receives shared input      |
| Usually returns the last step's output        | Returns a dictionary of branch outputs |
| Good for dependent operations                 | Good for independent operations        |

## 13. RunnableSequence vs Sequential Chains

We studied sequential chains in Section 07.

A **sequential chain** describes the workflow pattern.

`RunnableSequence` is a concrete LangChain component that implements sequential processing.

For example:

```python
chain = prompt | model | parser
```

This is both:

- A simple chain workflow
- A RunnableSequence

## 14. Error Handling

If a step fails, later steps normally do not execute.

Example:

```python
try:
    result = sequence.invoke(5)
    print(result)
except Exception as error:
    print("Sequence failed:", error)
```

In production applications, developers may use retries, fallbacks, and more specific exception handling.

## 15. Common Beginner Mistakes

**Mistake 1 — Thinking each step receives the original input**

Only the first step receives the original input directly. Later steps receive the outputs of preceding steps.

**Mistake 2 — Assuming operation order does not matter**

Changing the order can change the result.

**Mistake 3 — Ignoring input and output types**

Connected steps must be compatible.

**Mistake 4 — Assuming batch() makes only one API request**

Batching may involve multiple model calls.

**Mistake 5 — Assuming all custom functions support streaming**

Regular Python functions often process their complete input before returning an output.

## 16. Interview Questions

**Q1. What is RunnableSequence?**

A LangChain Runnable that executes multiple processing steps sequentially.

**Q2. How can we create RunnableSequence?**

Using the `RunnableSequence()` constructor or the LCEL pipe operator.

**Q3. What does the pipe operator do?**

Connects compatible Runnables into a workflow.

**Q4. Does every step receive the original input?**

No. Each step receives the previous step's output.

**Q5. Does RunnableSequence support batch execution?**

Yes.

**Q6. Does RunnableSequence support streaming?**

Yes, but incremental streaming behavior depends on its components.

**Q7. Can RunnableSequence work without an LLM?**

Yes. It can connect ordinary Python functions wrapped as Runnables.

**Q8. What happens when a processing step fails?**

The error normally propagates and later steps do not run.

**Q9. Why is input and output compatibility important?**

Each step must be able to process the previous step's result.

**Q10. What is the difference between RunnableSequence and RunnableParallel?**

RunnableSequence executes dependent operations in order. RunnableParallel executes independent branches.

## 17. Key Takeaways

- `RunnableSequence` connects processing steps sequentially.
- Each step receives the output of the previous step.
- Both explicit construction and the `|` operator are supported.
- The order of operations matters.
- Runnables can perform AI and non-AI tasks.
- `invoke()` handles one input.
- `batch()` handles multiple inputs.
- `stream()` supports incremental results where components allow it.
- Input/output compatibility is essential.
- RunnableSequence is widely used in modern LangChain applications.

---

## Learning Resources

- [LangChain RunnableSequence Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 08 — Topic 02
