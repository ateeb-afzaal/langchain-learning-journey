# 02 — TypedDict in Python and LangChain

## 1. What Is TypedDict?

`TypedDict` is a Python typing feature that allows developers to define the expected keys and value types of a dictionary.

It is especially useful when we want dictionaries to follow a predictable structure.

### Normal Python Dictionary

```python
student = {
    "name": "Ali",
    "age": 22,
    "grade": "A"
}
```

Python allows us to create dictionaries without explicitly declaring the expected fields.

### Using TypedDict

```python
from typing import TypedDict

class Student(TypedDict):
    name: str
    age: int
    grade: str

student: Student = {
    "name": "Ali",
    "age": 22,
    "grade": "A"
}
```

Here:

- `Student` defines the expected dictionary structure.
- `name` must be a string according to the type definition.
- `age` is declared as an integer.
- `grade` is declared as a string.

**Important:** TypedDict provides type information primarily for static type checkers. It does not automatically validate values at runtime.

---

## 2. Why Do We Need TypedDict?

Suppose we're building an AI-powered support ticket classifier.

We want each result to contain:

- Ticket category
- Priority
- Sentiment

Without a schema, different parts of our code might use inconsistent field names or types.

For example:

```python
ticket = {
    "category": "Technical",
    "priority": 2,
    "sentiment": "negative"
}
```

We can describe the expected structure using TypedDict:

```python
from typing import TypedDict

class Ticket(TypedDict):
    category: str
    priority: int
    sentiment: str
```

This makes the expected format easier for developers, editors, and type-checking tools to understand.

## 3. How TypedDict Works

A TypedDict definition looks similar to a class, but instances are ordinary dictionaries.

```python
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

person: Person = {
    "name": "Ateeb",
    "age": 23
}

print(person)
print(type(person))
```

Expected type:

```text
<class 'dict'>
```

A TypedDict instance is not a special validated object.

It remains a Python dictionary.

## 4. Does TypedDict Validate Data?

No. This is one of the most important concepts.

Consider:

```python
from typing import TypedDict

class Student(TypedDict):
    name: str
    age: int

student: Student = {
    "name": "Ali",
    "age": "twenty"
}

print(student)
```

The code can run even though `"twenty"` is a string instead of an integer.

A static type checker, such as mypy or Pyright, can flag this mismatch.

**Remember:**

- TypedDict = type hints and static checking.
- Pydantic = runtime validation.

We'll study Pydantic in the next topic.

---

## 5. Required Fields

By default, all fields in a TypedDict are required for static type checking.

```python
from typing import TypedDict

class Employee(TypedDict):
    name: str
    department: str
    salary: float
```

A correctly typed dictionary should contain all three fields:

```python
employee: Employee = {
    "name": "Ali",
    "department": "IT",
    "salary": 50000.0
}
```

If we omit `salary`, a static type checker can report a missing required key.

Python itself does not automatically raise an error when constructing such a dictionary.

---

## 6. Optional Fields Using NotRequired

Sometimes a dictionary contains fields that are not always available.

Python provides `NotRequired` to describe these fields.

```python
from typing import TypedDict, NotRequired

class Employee(TypedDict):
    name: str
    department: str
    phone: NotRequired[str]
```

Now this is valid according to the TypedDict definition:

```python
employee: Employee = {
    "name": "Ali",
    "department": "IT"
}
```

The `phone` key can be omitted.

### Important Difference

`NotRequired[str]` means that the key can be absent.

It does not mean that the value can be `None`.

If we want a field that may contain a string or `None`, we can write:

```python
phone: NotRequired[str | None]
```

---

## 7. Using Required

We can explicitly mark fields as required.

```python
from typing import TypedDict, Required, NotRequired

class User(TypedDict, total=False):
    name: Required[str]
    age: NotRequired[int]
    city: NotRequired[str]
```

Here:

- `name` is required.
- `age` is optional.
- `city` is optional.

The `total=False` setting makes fields non-required by default, while `Required` overrides that setting for `name`.

For older Python versions, `Required` and `NotRequired` may need to be imported from `typing_extensions`.

---

## 8. What Is Annotated?

`Annotated` allows us to attach additional information to a Python type.

For example:

```python
from typing import Annotated, TypedDict

class Student(TypedDict):
    name: Annotated[str, "Full name of the student"]
    age: Annotated[int, "Age in years"]
```

### Explanation

`Annotated[str, "..."]` means the underlying type is still `str`, but additional metadata is attached.

This metadata can be useful when frameworks generate schemas or documentation.

### Why Is It Useful in LangChain?

When describing structured output to an LLM, field descriptions help explain what information should appear in each field.

However, whether the metadata is used depends on the LangChain integration and schema conversion.

---

## 9. What Is Literal?

`Literal` restricts the values accepted by static type checkers to specific choices.

For example:

```python
from typing import TypedDict, Literal

class Ticket(TypedDict):
    category: Literal["technical", "billing", "general"]
    priority: Literal["low", "medium", "high"]
```

According to this schema:

- `category` should be one of three predefined values.
- `priority` should be `low`, `medium`, or `high`.

Example:

```python
ticket: Ticket = {
    "category": "technical",
    "priority": "high"
}
```

### Why Is Literal Useful?

Imagine a support ticket classifier.

Without predefined choices, an LLM might return:

```text
Urgent
Very High
Critical
High Priority
```

But our application might expect exactly:

```text
low
medium
high
```

`Literal` lets us describe these allowed values in the schema.

**Important:** Literal restrictions are not automatically enforced at runtime by TypedDict.

---

## 10. Combining TypedDict, Annotated, Literal, and NotRequired

Let's define a more realistic structured-output schema.

```python
from typing import (
    TypedDict,
    Annotated,
    Literal,
    NotRequired
)

class SupportTicket(TypedDict):
    category: Annotated[
        Literal["technical", "billing", "general"],
        "Category of the customer issue"
    ]

    priority: Annotated[
        Literal["low", "medium", "high"],
        "Urgency of the ticket"
    ]

    summary: Annotated[
        str,
        "A short summary of the customer's issue"
    ]

    customer_name: NotRequired[str]
```

### Explanation

| Field           | Type         | Meaning                         |
| --------------- | ------------ | ------------------------------- |
| `category`      | Literal      | One of three allowed categories |
| `priority`      | Literal      | Low, medium, or high            |
| `summary`       | String       | Short explanation of the issue  |
| `customer_name` | Optional key | Name, if available              |

Example output:

```json
{
  "category": "technical",
  "priority": "high",
  "summary": "Customer cannot access their account",
  "customer_name": "Ali"
}
```

This structure is useful for AI-based ticket classification.

---

## 11. Using TypedDict with LangChain

LangChain can use TypedDict definitions as schemas for structured model responses.

Example:

```python
from typing import TypedDict, Annotated, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class Review(TypedDict):
    sentiment: Annotated[
        Literal["positive", "negative", "neutral"],
        "Overall sentiment of the review"
    ]

    summary: Annotated[
        str,
        "A brief summary of the review"
    ]

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

structured_model = model.with_structured_output(
    Review,
    method="function_calling"
)

result = structured_model.invoke(
    "Review: The laptop is fast, but its battery life is disappointing."
)

print(result)
```

### What Happens Here?

1. `Review` defines the output structure.
2. `ChatGroq` connects to the model hosted by Groq.
3. `with_structured_output()` configures a structured response.
4. `method="function_calling"` requests the tool/function-calling approach.
5. `invoke()` sends the review to the model.
6. The result is parsed into a Python dictionary.

### Important Compatibility Note

The available structured-output methods depend on the Groq model, API, and installed LangChain integration.

If the provider rejects a selected method, we should check the model's supported capabilities rather than assume every method works.

Also, a TypedDict schema does not itself perform Pydantic-style runtime validation on the resulting dictionary.

We'll explore this more deeply in `05_with_structured_output.md`.

---

## 12. TypedDict vs Pydantic

| Feature                       | TypedDict        | Pydantic                   |
| ----------------------------- | ---------------- | -------------------------- |
| Defines fields and types      | Yes              | Yes                        |
| Static type checking          | Yes              | Yes                        |
| Runtime validation by default | No               | Yes                        |
| Supports descriptions         | Through metadata | Through `Field()`          |
| Returns ordinary dictionaries | Yes              | Can create model instances |
| Useful for structured output  | Yes              | Yes                        |

### When Should We Use TypedDict?

Use TypedDict when:

- We need a lightweight dictionary schema.
- We're documenting the expected structure.
- We want editor and type-checker support.
- Runtime validation is handled elsewhere.

### When Should We Use Pydantic?

Use Pydantic when:

- We need runtime data validation.
- Fields have important constraints.
- We want clear validation errors.
- Our application must enforce the expected data structure.

---

## 13. Common Beginner Mistakes

**Mistake 1 — Thinking TypedDict validates data at runtime**

It primarily provides static type information.

**Mistake 2 — Confusing NotRequired with nullable values**

An optional key may be absent; a nullable value may explicitly contain `None`.

**Mistake 3 — Thinking Literal automatically rejects invalid values**

A static type checker can detect invalid values, but TypedDict itself doesn't enforce them at runtime.

**Mistake 4 — Assuming Annotated always changes program behavior**

The additional metadata only affects tools that understand and use it.

**Mistake 5 — Assuming every LLM supports every structured-output method**

Model and provider support must be checked.

---

## 14. Interview Questions

**Q1. What is TypedDict?**

A Python typing feature for defining the expected keys and value types of dictionaries.

**Q2. Does TypedDict perform runtime validation?**

No.

**Q3. What does NotRequired do?**

Allows a dictionary key to be omitted.

**Q4. What is the purpose of Required?**

Explicitly marks a key as required.

**Q5. What does total=False mean?**

Fields are non-required by default unless explicitly marked as required.

**Q6. What does Annotated do?**

Attaches metadata to a Python type.

**Q7. What is Literal used for?**

Describing a restricted set of allowed values.

**Q8. What is the difference between TypedDict and Pydantic?**

TypedDict describes dictionary types, while Pydantic provides runtime validation.

**Q9. Can LangChain use TypedDict for structured output?**

Yes, with supported chat model integrations.

**Q10. Does a valid TypedDict schema guarantee factually correct LLM output?**

No. A schema describes structure, not factual accuracy.

---

## 15. Key Takeaways

- TypedDict defines the expected structure of dictionaries.
- TypedDict instances remain ordinary dictionaries.
- TypedDict does not automatically validate data at runtime.
- Required fields are mandatory for static type checking by default.
- `NotRequired` allows keys to be omitted.
- `Required` explicitly marks mandatory keys.
- `Annotated` attaches descriptive metadata.
- `Literal` describes a limited set of accepted values.
- LangChain can use TypedDict schemas for structured output.
- Pydantic is preferable when runtime validation is essential.

---

## Learning Resources

- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)
- [Python TypedDict Documentation](https://docs.python.org/3/library/typing.html#typing.TypedDict)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 05 — Topic 02
