# 02 — Simple Chains in LangChain

## 1. What Is a Simple Chain?

A **simple chain** is a LangChain workflow that connects processing components in a predefined sequence.

The most common example connects three components:

1. Prompt Template
2. Language Model
3. Output Parser

### Workflow

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
Final Response
```

In simple words, a chain allows us to execute several connected operations using a single `invoke()` call.

---

## 2. Why Do We Need Simple Chains?

Imagine building an AI application that explains programming concepts.

Without a chain, we might write:

```python
formatted_prompt = prompt.invoke({
    "topic": "Python decorators"
})

response = model.invoke(formatted_prompt)

answer = parser.invoke(response)

print(answer)
```

With a chain, we can write:

```python
chain = prompt | model | parser

answer = chain.invoke({
    "topic": "Python decorators"
})

print(answer)
```

Both approaches perform the same basic operations.

### Benefits

- Cleaner and more readable code
- Reusable workflows
- Less repetitive code
- Support for dynamic inputs
- Integration with batching and streaming
- Easier composition with other LangChain components

---

## 3. Components of a Simple Chain

### A. PromptTemplate

Prepares the instructions sent to the language model.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 sentences."
)
```

`{topic}` is a dynamic variable.

### B. Chat Model

Generates the AI response.

```python
from langchain_groq import ChatGroq

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
```

The Groq API key must be configured in the environment.

### C. Output Parser

Extracts generated text from the model response.

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
```

### D. Chain

Connects all three components.

```python
chain = prompt | model | parser
```

The output of one component becomes the input of the next.

---

## 4. Creating a Simple Chain with Groq

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API credentials
load_dotenv()

# Initialize model
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# Define dynamic prompt
prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner in 3 simple sentences."
)

# Initialize output parser
parser = StrOutputParser()

# Connect components
chain = prompt | model | parser

# Execute chain
result = chain.invoke({
    "topic": "Machine Learning"
})

print(result)
```

### Step-by-Step Explanation

**Step 1:** `load_dotenv()` loads the Groq API key.

**Step 2:** `ChatGroq()` initializes the hosted language model.

**Step 3:** `PromptTemplate` defines instructions with a variable.

**Step 4:** `StrOutputParser` extracts text from the model response.

**Step 5:** `|` connects the components.

**Step 6:** `chain.invoke()` executes the entire workflow.

---

## 5. Understanding invoke()

The `invoke()` method executes a chain with one input.

```python
result = chain.invoke({
    "topic": "Python lists"
})

print(result)
```

Here, the chain processes one topic.

We can reuse the same chain:

```python
result = chain.invoke({
    "topic": "Neural Networks"
})

print(result)
```

There is no need to recreate the prompt or model for each request.

---

## 6. Understanding batch()

The `batch()` method processes multiple inputs.

Example:

```python
topics = [
    {"topic": "Python"},
    {"topic": "Machine Learning"},
    {"topic": "Deep Learning"}
]

results = chain.batch(topics)

for topic, result in zip(topics, results):
    print("Topic:", topic["topic"])
    print("Answer:", result)
    print()
```

### How It Works

1. The chain receives multiple input dictionaries.
2. Each input passes through the same workflow.
3. The method returns corresponding results.
4. We can process the results using a Python loop.

**Important:** `batch()` may execute multiple model requests concurrently. It does not necessarily send all inputs in one API request.

Batching can also be limited by provider rate limits.

---

## 7. Understanding stream()

The `stream()` method allows us to receive output incrementally when supported.

```python
for chunk in chain.stream({
    "topic": "Artificial Intelligence"
}):
    print(chunk, end="", flush=True)
```

### Why Is Streaming Useful?

Without streaming, the user generally waits until a complete response is returned.

With streaming, an application can display generated content progressively.

This is useful for:

- AI chatbots
- Coding assistants
- Educational applications
- Long-form responses

Streaming behavior depends on the model and the components in the chain.

---

## 8. Understanding the Output Type

With `StrOutputParser`, the result is text suitable for Python string operations.

```python
result = chain.invoke({
    "topic": "Python"
})

print(type(result))
print(str(result).upper())
```

### Version Note

During our Section 06 testing, the installed LangChain version returned a `TextAccessor` object, which behaves like a string.

If an application requires an exact built-in Python string:

```python
result = str(result)
```

Then:

```python
print(type(result))
```

returns:

```text
<class 'str'>
```

---

## 9. What Is RunnableSequence?

A simple chain created using:

```python
chain = prompt | model | parser
```

is represented as a sequence of runnable operations.

We can also use `RunnableSequence` explicitly:

```python
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    prompt,
    model,
    parser
)
```

Both approaches connect the components in order.

For everyday examples, the pipe operator is usually easier to read.

---

## 10. Practical Example: AI Programming Tutor

Imagine building an educational assistant that explains programming concepts according to a student's level.

```python
prompt = PromptTemplate.from_template(
    """
    You are an experienced programming teacher.

    Topic: {topic}
    Student level: {level}

    Instructions:
    - Explain the concept clearly.
    - Include one practical example.
    - Use simple English.
    """
)

chain = prompt | model | StrOutputParser()

result = chain.invoke({
    "topic": "Python decorators",
    "level": "beginner"
})

print(result)
```

### Real-World Benefit

Instead of creating a separate prompt for every student, we reuse the same workflow with different topics and difficulty levels.

---

## 11. Simple Chain vs Sequential Chain

A simple chain is usually a straightforward processing pipeline.

Example:

```text
Prompt → Model → Parser
```

A more complex sequential workflow might perform two separate AI tasks:

```text
Original Text
     |
     v
Summarization Chain
     |
     v
Translation Chain
     |
     v
Translated Summary
```

Both use sequential execution, but the second example connects multiple task-level operations.

We'll study sequential chains in Topic 03.

---

## 12. Common Beginner Mistakes

**Mistake 1 — Assuming a chain is an AI model**

A chain is a workflow that may contain an AI model.

**Mistake 2 — Confusing prompt.invoke() with chain.invoke()**

`prompt.invoke()` formats a prompt.

`chain.invoke()` executes all connected components.

**Mistake 3 — Assuming batch() is one API request**

Batching can involve multiple independent requests.

**Mistake 4 — Expecting every chain to support token-by-token streaming**

Streaming depends on the components and provider.

**Mistake 5 — Forgetting required prompt variables**

If the prompt expects `{topic}`, the input must provide a value for `topic`.

---

## 13. Interview Questions

**Q1. What is a simple chain?**

A workflow that connects processing components in a predefined order.

**Q2. What is the purpose of the pipe operator?**

It connects compatible LangChain runnable components.

**Q3. What does invoke() do?**

Processes one input through the chain.

**Q4. What does batch() do?**

Processes multiple inputs through the same workflow.

**Q5. What does stream() do?**

Produces incremental output where supported.

**Q6. What is RunnableSequence?**

A runnable that executes multiple components sequentially.

**Q7. Can a chain be reused with different inputs?**

Yes.

**Q8. Does every chain require a language model?**

No.

**Q9. Why use StrOutputParser?**

To obtain the generated response as text suitable for downstream processing.

**Q10. Can a simple chain contain dynamic prompt variables?**

Yes.

---

## 14. Key Takeaways

- Simple chains connect components into reusable workflows.
- `PromptTemplate` prepares model instructions.
- `ChatGroq` generates responses.
- `StrOutputParser` extracts response text.
- The pipe operator connects runnable components.
- `invoke()` processes one input.
- `batch()` processes multiple inputs.
- `stream()` provides incremental output when supported.
- `RunnableSequence` represents sequential processing.
- Simple chains are useful for predictable AI application tasks.

---

## Learning Resources

- [CampusX LangChain Chains Repository](https://github.com/campusx-official/langchain-chains)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 07 — Topic 02
