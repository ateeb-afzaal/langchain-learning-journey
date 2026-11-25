# 03 — Pydantic in Python and LangChain

## 1. What Is Pydantic?

Pydantic is a Python library for defining structured data models and validating data at runtime using Python type annotations.

It helps ensure that data satisfies expected types, required fields, and constraints.

Unlike `TypedDict`, Pydantic performs runtime validation.

## 2. Why Do We Need Pydantic?

Consider a support ticket with the following fields:

- Category
- Priority
- Summary

We want the priority to be one of `low`, `medium`, or `high`.

Using `TypedDict`, incorrect values could still exist at runtime.

Pydantic allows us to reject values that violate our schema.

## 3. Creating a Pydantic Model

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    grade: str

student = Student(
    name="Ali",
    age=22,
    grade="A"
)

print(student)
print(student.name)
print(student.age)
```

### Explanation

- `BaseModel` is the parent class for Pydantic models.
- `Student` defines the expected fields.
- Pydantic validates the supplied data when the instance is created.
- We can access fields using dot notation.

## 4. Understanding Runtime Validation

```python
from pydantic import BaseModel, ValidationError

class Student(BaseModel):
    name: str
    age: int

try:
    student = Student(
        name="Ali",
        age="twenty"
    )
except ValidationError as error:
    print(error)
```

Because `"twenty"` cannot be interpreted as an integer, Pydantic raises a validation error.

**Important:** Pydantic may automatically convert compatible values.

For example, `"22"` may be converted into integer `22` under its default validation behavior.

Use strict validation when automatic type conversion is not acceptable.

## 5. Required and Optional Fields

### Required Fields

```python
from pydantic import BaseModel

class Employee(BaseModel):
    name: str
    department: str
```

Both fields are required when creating an instance.

### Optional Fields

```python
class Employee(BaseModel):
    name: str
    department: str
    phone: str | None = None
```

The `phone` field may be omitted or explicitly set to `None`.

**Important:** In Pydantic v2, `phone: str | None` without a default is still a required field.

## 6. Using Field()

`Field()` allows us to provide descriptions, defaults, and validation constraints.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(
        description="Name of the product"
    )

    price: float = Field(
        gt=0,
        description="Price must be greater than zero"
    )

    quantity: int = Field(
        ge=0,
        description="Available quantity"
    )
```

### Common Constraints

| Constraint      | Meaning                       |
| --------------- | ----------------------------- |
| `gt=0`          | Greater than zero             |
| `ge=0`          | Greater than or equal to zero |
| `lt=100`        | Less than 100                 |
| `le=100`        | Less than or equal to 100     |
| `min_length=3`  | Minimum string length         |
| `max_length=50` | Maximum string length         |

## 7. Using Literal for Restricted Values

```python
from typing import Literal
from pydantic import BaseModel

class SupportTicket(BaseModel):
    category: Literal[
        "technical", "billing", "general"
    ]

    priority: Literal[
        "low", "medium", "high"
    ]

    summary: str
```

Now invalid values such as `"urgent"` will raise a validation error.

## 8. Validating a Support Ticket

```python
ticket = SupportTicket(
    category="technical",
    priority="high",
    summary="Customer cannot log in"
)

print(ticket.model_dump())
```

Expected output:

```python
{
    "category": "technical",
    "priority": "high",
    "summary": "Customer cannot log in"
}
```

### Invalid Ticket

```python
from pydantic import ValidationError

try:
    ticket = SupportTicket(
        category="unknown",
        priority="urgent",
        summary="Customer needs help"
    )
except ValidationError as error:
    print(error)
```

Pydantic rejects the invalid category and priority.

This is the key difference from our previous `TypedDict` example.

## 9. Important Pydantic Methods

### model_dump()

Convert a Pydantic model to a Python dictionary.

```python
print(ticket.model_dump())
```

### model_dump_json()

Convert a Pydantic model to a JSON string.

```python
print(ticket.model_dump_json())
```

### model_validate()

Validate a Python dictionary against a Pydantic model.

```python
data = {
    "category": "technical",
    "priority": "high",
    "summary": "Account login issue"
}

ticket = SupportTicket.model_validate(data)
print(ticket)
```

### model_validate_json()

Validate data supplied as a JSON string.

```python
json_data = """
{
    "category": "billing",
    "priority": "medium",
    "summary": "Incorrect invoice"
}
"""

ticket = SupportTicket.model_validate_json(json_data)
print(ticket)
```

### model_json_schema()

Generate a JSON Schema describing the Pydantic model.

```python
print(SupportTicket.model_json_schema())
```

This is particularly useful when integrating Pydantic schemas with other systems.

## 10. Pydantic with LangChain

LangChain supports Pydantic models as structured-output schemas.

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()

class MovieReview(BaseModel):
    sentiment: str = Field(
        description="Overall sentiment"
    )
    summary: str = Field(
        description="Short summary of the review"
    )

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

structured_model = model.with_structured_output(
    MovieReview,
    method="function_calling"
)

result = structured_model.invoke(
    "The movie was excellent, but slightly too long."
)

print(result)
```

When the integration successfully returns a Pydantic instance, its fields have undergone Pydantic validation.

**Compatibility note:** Structured-output methods depend on the Groq model and integration version. Not every method is supported by every model.

We'll examine this in the dedicated `with_structured_output()` topic.

## 11. TypedDict vs Pydantic

| Feature                | TypedDict                     | Pydantic                   |
| ---------------------- | ----------------------------- | -------------------------- |
| Type hints             | Yes                           | Yes                        |
| Runtime validation     | No                            | Yes                        |
| Field constraints      | Not enforced                  | Enforced                   |
| JSON Schema generation | Requires external tooling     | Built-in                   |
| Output object          | Dictionary                    | Model instance             |
| Best suited for        | Lightweight type descriptions | Validated application data |

## 12. Common Beginner Mistakes

**Mistake 1 — Assuming all values are strictly typed**

Pydantic can coerce compatible values by default.

**Mistake 2 — Confusing optional and non-required fields**

A nullable field without a default can still be required.

**Mistake 3 — Forgetting to handle ValidationError**

Invalid inputs should be handled safely.

**Mistake 4 — Assuming validation guarantees factual accuracy**

A valid Pydantic object may still contain factually incorrect values generated by an LLM.

**Mistake 5 — Using Pydantic v1 method names**

For Pydantic v2, prefer `model_dump()`, `model_validate()`, and `model_json_schema()`.

## 13. Interview Questions

**Q1. What is Pydantic?**

A Python library used to define data models and perform runtime validation.

**Q2. What is BaseModel?**

The base class used for defining Pydantic models.

**Q3. What does Field() do?**

It provides metadata, defaults, and validation constraints for fields.

**Q4. What is ValidationError?**

An exception raised when data fails Pydantic validation.

**Q5. What does model_dump() do?**

Converts a Pydantic model into a Python dictionary.

**Q6. What does model_validate() do?**

Validates Python data and creates a Pydantic model instance.

**Q7. What is the difference between TypedDict and Pydantic?**

TypedDict primarily describes dictionary types, while Pydantic validates data at runtime.

**Q8. Does Pydantic guarantee that AI-generated data is factually correct?**

No. It validates structure and defined constraints, not the truth of every statement.

## 14. Key Takeaways

- Pydantic provides runtime validation.
- `BaseModel` defines structured data models.
- `Field()` defines descriptions and constraints.
- `Literal` restricts acceptable values.
- `ValidationError` reports invalid data.
- `model_dump()` converts models into dictionaries.
- `model_validate()` validates Python data.
- `model_json_schema()` generates JSON Schema.
- LangChain can use Pydantic models for structured outputs.

---

## Learning Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 05 — Topic 03
