# 04 — Data Transformation in LangChain LCEL

## 1. What Is Data Transformation?

Data transformation is the process of converting information from one format into another.

In LangChain, we often transform data so that it can pass correctly between different Runnable components.

For example, a user might enter:

```python
"  machine learning  "
```

But our PromptTemplate expects:

```python
{"topic": "Machine Learning"}
```

We can use `RunnableLambda` to perform this conversion automatically.

## 2. Why Is Data Transformation Important?

Real-world applications receive information in different formats.

Some inputs may contain:

- Extra spaces
- Missing fields
- Incorrect data types
- Unnecessary information
- Inconsistent capitalization

Different LangChain components may also expect different input structures.

Data transformation helps us:

1. Clean user input.
2. Validate required fields.
3. Convert strings into dictionaries.
4. Add new calculated fields.
5. Preserve original information.
6. Format AI-generated responses.
7. Connect components with different input and output requirements.

## 3. Important Components

| Component                      | Purpose                                      |
| ------------------------------ | -------------------------------------------- |
| `RunnableLambda`               | Execute custom Python transformations        |
| `RunnablePassthrough`          | Preserve input unchanged                     |
| `RunnablePassthrough.assign()` | Add fields to dictionaries                   |
| `RunnableSequence`             | Connect transformation steps                 |
| `RunnableParallel`             | Produce multiple independent transformations |

The most important components for this topic are `RunnableLambda` and `RunnablePassthrough.assign()`.

## 4. Using RunnableLambda to Clean Text

First, create a regular Python function.

```python
def clean_text(text):
    return text.strip().lower()
```

Now convert it into a Runnable.

```python
from langchain_core.runnables import RunnableLambda

clean_runnable = RunnableLambda(clean_text)
```

Execute:

```python
result = clean_runnable.invoke("  HELLO LANGCHAIN  ")

print(result)
```

Output:

```text
hello langchain
```

### Explanation

- `strip()` removes leading and trailing whitespace.
- `lower()` converts text to lowercase.
- `RunnableLambda` makes this Python function compatible with LangChain's Runnable interface.

## 5. Combining Multiple Transformations

We can connect several transformations using LCEL.

```python
clean = RunnableLambda(lambda text: text.strip())
uppercase = RunnableLambda(lambda text: text.upper())
add_prefix = RunnableLambda(lambda text: "Processed: " + text)

chain = clean | uppercase | add_prefix

print(chain.invoke("  hello python  "))
```

Output:

```text
Processed: HELLO PYTHON
```

### Data Flow

```text
"  hello python  "
        |
        v
      strip()
        |
        v
  "hello python"
        |
        v
      upper()
        |
        v
  "HELLO PYTHON"
        |
        v
    Add Prefix
        |
        v
"Processed: HELLO PYTHON"
```

Every step receives the output of the previous step.

## 6. Converting a String into a Dictionary

One of the most common transformations in LangChain is converting a string into a dictionary.

Suppose our prompt expects a variable named `{topic}`.

We can prepare the input:

```python
def prepare_topic(text):
    return {
        "topic": text.strip().title()
    }

prepare_input = RunnableLambda(prepare_topic)
```

Execute:

```python
result = prepare_input.invoke("  machine learning  ")

print(result)
```

Output:

```python
{"topic": "Machine Learning"}
```

Now the resulting dictionary can be passed directly into a PromptTemplate containing `{topic}`.

## 7. Validating User Input

Data transformation can also include validation.

For example, we want to reject empty topics.

```python
def validate_topic(text):
    if not isinstance(text, str):
        raise TypeError("Topic must be a string")

    cleaned = text.strip()

    if not cleaned:
        raise ValueError("Topic cannot be empty")

    return cleaned
```

Wrap the function:

```python
validator = RunnableLambda(validate_topic)
```

Valid input:

```python
print(validator.invoke("  Python  "))
```

Output:

```text
Python
```

Invalid input:

```python
validator.invoke("   ")
```

Raises:

```text
ValueError: Topic cannot be empty
```

### Why Validate Before Calling an LLM?

Validation can:

- Prevent unnecessary model requests.
- Catch incorrect input formats.
- Produce clearer errors.
- Help enforce application requirements.

Validation does not guarantee that an LLM will generate factually correct information.

## 8. Transforming Dictionary Fields

Suppose we receive this dictionary:

```python
user_data = {
    "first_name": "Ali",
    "last_name": "Khan",
    "age": 22
}
```

We want to produce:

```python
{
    "full_name": "Ali Khan",
    "age": 22
}
```

Create a function:

```python
def format_user(data):
    return {
        "full_name": (
            data["first_name"].strip()
            + " "
            + data["last_name"].strip()
        ),
        "age": data["age"]
    }
```

Convert it into a Runnable:

```python
formatter = RunnableLambda(format_user)
```

Execute:

```python
print(formatter.invoke(user_data))
```

This technique is useful when preparing API payloads, application records, and prompt variables.

## 9. Understanding RunnablePassthrough

`RunnablePassthrough` returns its input unchanged.

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

result = passthrough.invoke({
    "topic": "Python"
})

print(result)
```

Output:

```python
{"topic": "Python"}
```

The original data is preserved.

## 10. Adding Fields with RunnablePassthrough.assign()

`RunnablePassthrough.assign()` allows us to add computed fields to an existing dictionary.

Example:

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

Output:

```python
{
    "number": 5,
    "double": 10,
    "square": 25
}
```

### How It Works

1. The input is a dictionary.
2. Existing fields are preserved.
3. The provided functions calculate new values.
4. The calculated values are added to the result.

**Important:** `assign()` expects a dictionary input.

If an assigned key already exists, the new value replaces that key in the result.

## 11. Difference Between RunnableLambda and assign()

Consider this input:

```python
{"number": 5}
```

### Using RunnableLambda

```python
chain = RunnableLambda(
    lambda data: {
        "double": data["number"] * 2
    }
)
```

Output:

```python
{"double": 10}
```

The original `number` field is not included because the function returned a new dictionary without it.

### Using assign()

```python
chain = RunnablePassthrough.assign(
    double=lambda data: data["number"] * 2
)
```

Output:

```python
{
    "number": 5,
    "double": 10
}
```

The original field remains available.

### Comparison

| Feature                                 | RunnableLambda              | Passthrough.assign()      |
| --------------------------------------- | --------------------------- | ------------------------- |
| Main purpose                            | Custom transformation       | Extend dictionary         |
| Preserves original fields automatically | No                          | Yes                       |
| Works with strings                      | Yes, depending on function  | Requires dictionary input |
| Supports multiple calculated fields     | Yes                         | Yes                       |
| Typical use                             | Clean/validate/reshape data | Enrich structured data    |

## 12. Building a Multi-Step Dictionary Workflow

Suppose our application receives:

```python
{
    "topic": "  machine learning  ",
    "level": "BEGINNER"
}
```

We want to:

1. Clean the topic.
2. Normalize the level.
3. Add a display label.

### Step 1 — Clean and Validate

```python
def normalize_input(data):
    topic = data["topic"].strip()
    level = data["level"].strip().lower()

    if not topic:
        raise ValueError("Topic cannot be empty")

    if level not in {"beginner", "intermediate", "advanced"}:
        raise ValueError("Invalid learning level")

    return {
        "topic": topic.title(),
        "level": level
    }
```

### Step 2 — Convert to Runnable

```python
normalize = RunnableLambda(normalize_input)
```

### Step 3 — Add a New Field

```python
add_label = RunnablePassthrough.assign(
    display_label=lambda data: (
        f"{data['topic']} ({data['level']})"
    )
)
```

### Step 4 — Connect Using LCEL

```python
chain = normalize | add_label
```

### Step 5 — Execute

```python
result = chain.invoke({
    "topic": "  machine learning  ",
    "level": "BEGINNER"
})

print(result)
```

Output:

```python
{
    "topic": "Machine Learning",
    "level": "beginner",
    "display_label": "Machine Learning (beginner)"
}
```

This is a practical example of data transformation using LCEL.

## 13. Data Transformation Before an LLM

Now we'll create a workflow that:

1. Accepts raw input.
2. Cleans and validates it.
3. Prepares the prompt.
4. Sends the prompt to Groq.
5. Extracts the generated explanation.

### Initialize Groq

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
```

### Create the Prompt

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} to a {level} student "
    "in 3 simple sentences."
)
```

### Create the LCEL Workflow

```python
ai_chain = (
    normalize
    | prompt
    | model
    | StrOutputParser()
)
```

### Execute

```python
result = ai_chain.invoke({
    "topic": "  neural networks  ",
    "level": "BEGINNER"
})

print(str(result))
```

The model receives normalized inputs rather than the original uncleaned values.

## 14. Data Transformation After an LLM

Sometimes we want to format a model's response.

Example:

```python
def format_output(text):
    return (
        "AI STUDY NOTES\n"
        + "=" * 30
        + "\n\n"
        + str(text).strip()
    )
```

Convert it into a Runnable:

```python
output_formatter = RunnableLambda(format_output)
```

Connect it to the model:

```python
chain = (
    normalize
    | prompt
    | model
    | StrOutputParser()
    | output_formatter
)
```

This generates a response and adds a heading.

### Important

An ordinary `RunnableLambda` after the model may delay incremental streaming because it usually processes the complete input before returning its result.

For streaming transformations, a streaming-aware component may be more appropriate.

## 15. Preserving Inputs and Adding an AI Answer

In many applications, we want the final output to contain:

- The normalized topic.
- The learning level.
- The display label.
- The AI-generated explanation.

We can use `RunnablePassthrough.assign()`.

```python
answer_chain = (
    prompt
    | model
    | StrOutputParser()
)

full_chain = (
    normalize
    | RunnablePassthrough.assign(
        display_label=lambda data: (
            f"{data['topic']} ({data['level']})"
        ),
        explanation=answer_chain
    )
)
```

### Execute

```python
result = full_chain.invoke({
    "topic": "  machine learning  ",
    "level": "BEGINNER"
})
```

The result contains the original normalized fields and the generated fields.

Its structure is:

```python
{
    "topic": "Machine Learning",
    "level": "beginner",
    "display_label": "Machine Learning (beginner)",
    "explanation": "..."
}
```

The explanation is generated by Groq, so its exact content may vary.

### Execution Flow

```text
Raw Input Dictionary
          |
          v
  RunnableLambda
  Normalize + Validate
          |
          v
   Normalized Dictionary
          |
          v
RunnablePassthrough.assign()
          |
     +----+----------------+
     |                     |
     v                     v
Display Label        Explanation Chain
     |                     |
     |               PromptTemplate
     |                     |
     |                  ChatGroq
     |                     |
     |               StrOutputParser
     |                     |
     +----------+----------+
                |
                v
       Combined Dictionary
```

## 16. Adding More Fields After Generation

We can add another transformation after the AI response.

For example, calculate the length of the generated explanation.

```python
final_chain = full_chain | RunnablePassthrough.assign(
    explanation_length=lambda data: len(
        str(data["explanation"])
    )
)
```

Now the final output includes:

```python
{
    "topic": "Machine Learning",
    "level": "beginner",
    "display_label": "Machine Learning (beginner)",
    "explanation": "...",
    "explanation_length": 123
}
```

The number `123` is illustrative; the actual value depends on the generated text.

### Important

The later `assign()` stage can access fields produced by earlier stages.

This allows us to build multi-step data-enrichment workflows.

## 17. Data Transformation in RAG

RAG stands for Retrieval-Augmented Generation.

A RAG application commonly needs to:

1. Receive a question.
2. Retrieve relevant documents.
3. Convert documents into readable context.
4. Combine the context with the original question.
5. Generate an answer.

LCEL transformations can help at each stage.

For example:

```python
def format_documents(documents):
    return "\n\n".join(
        document.page_content
        for document in documents
    )
```

We can wrap this function:

```python
format_docs = RunnableLambda(format_documents)
```

And connect it to a configured retriever:

```python
context_chain = retriever | format_docs
```

The retriever produces documents, while the formatter converts them into text suitable for a prompt.

This is a conceptual example that requires a configured retriever.

## 18. Common Beginner Mistakes

**Mistake 1 — Forgetting input validation**

An invalid input may cause later stages to fail.

**Mistake 2 — Returning the wrong data type**

A prompt expecting a dictionary may not accept the output of a function returning an unrelated value.

**Mistake 3 — Assuming assign() works on strings**

`RunnablePassthrough.assign()` expects a dictionary.

**Mistake 4 — Accidentally discarding original fields**

A RunnableLambda that creates a new dictionary preserves only the fields explicitly returned.

**Mistake 5 — Thinking all assigned fields depend on each other**

Fields added in a single `assign()` stage are generally calculated from the input to that stage. To calculate a field using another newly generated field, add a subsequent stage.

**Mistake 6 — Assuming data transformation requires AI**

Many transformations are ordinary Python operations.

**Mistake 7 — Ignoring model errors**

LLM requests can fail because of network problems, provider limits, or invalid configuration.

## 19. Interview Questions

**Q1. What is data transformation in LCEL?**

Converting inputs or outputs into formats suitable for other processing components.

**Q2. What is RunnableLambda used for?**

Executing custom Python functions inside Runnable workflows.

**Q3. What does RunnablePassthrough.assign() do?**

Adds calculated fields while preserving existing dictionary fields.

**Q4. Why should we validate input before an LLM call?**

To reject invalid information and avoid unnecessary model requests.

**Q5. Can RunnableLambda transform dictionaries?**

Yes.

**Q6. What is the difference between RunnableLambda and RunnablePassthrough?**

RunnableLambda executes custom processing, while RunnablePassthrough preserves input by default.

**Q7. Does assign() accept a string directly?**

No. It expects dictionary input.

**Q8. How can we add an AI-generated answer to an existing dictionary?**

Use RunnablePassthrough.assign() with an LLM chain.

**Q9. Can we add new fields after an AI response?**

Yes, using an additional transformation stage.

**Q10. Why is data transformation important in RAG?**

It helps convert retrieved documents into context and combine them with user questions.

## 20. Key Takeaways

- Data transformation prepares information for different processing steps.
- RunnableLambda is useful for cleaning, validating, and restructuring data.
- RunnablePassthrough preserves input.
- RunnablePassthrough.assign() adds fields to dictionaries.
- Multiple transformations can be composed with LCEL.
- Validation should happen before expensive model requests.
- Transformations can occur before or after an LLM.
- Multi-step pipelines can enrich data incrementally.
- These patterns are especially useful in AI assistants, APIs, and RAG applications.

---

## Learning Resources

- [LangChain RunnableLambda Reference](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda)
- [LangChain RunnablePassthrough Reference](https://reference.langchain.com/python/langchain-core/runnables/passthrough/RunnablePassthrough)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 09 — Topic 04
