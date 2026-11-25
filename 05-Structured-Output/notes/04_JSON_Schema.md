# 04 — JSON Schema in Python and LangChain

## 1. What Is JSON Schema?

JSON Schema is a standard way to describe the expected structure and rules of JSON data.

It tells an application which fields should exist, what types they should contain, and what restrictions apply to their values.

**In simple words:**

- **JSON** contains the actual data.
- **JSON Schema** defines the rules that data should follow.
- **Validation** checks whether the data follows those rules.

## 2. JSON vs JSON Schema

### Example JSON Data

```json
{
  "name": "Ali",
  "age": 22,
  "department": "IT"
}
```

### Example JSON Schema

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer"
    },
    "department": {
      "type": "string"
    }
  },
  "required": ["name", "age"]
}
```

The schema describes which data types are expected. Here, `name` and `age` are required, while `department` can be omitted.

## 3. Important JSON Schema Keywords

| Keyword                | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| `type`                 | Defines the expected data type            |
| `properties`           | Describes fields inside an object         |
| `required`             | Specifies mandatory fields                |
| `enum`                 | Restricts values to a predefined list     |
| `description`          | Explains the meaning of a field           |
| `minimum`              | Sets the minimum numeric value            |
| `maximum`              | Sets the maximum numeric value            |
| `minLength`            | Sets the minimum string length            |
| `additionalProperties` | Controls whether extra fields are allowed |

### Example: Restricting Values with enum

```json
{
  "type": "string",
  "enum": ["low", "medium", "high"]
}
```

Only these three values satisfy the schema.

## 4. JSON Schema Data Types

| JSON Schema Type | Example             |
| ---------------- | ------------------- |
| `string`         | `"Python"`          |
| `integer`        | `25`                |
| `number`         | `25.5`              |
| `boolean`        | `true`              |
| `array`          | `["Python", "SQL"]` |
| `object`         | `{"name": "Ali"}`   |
| `null`           | `null`              |

## 5. Building a Support Ticket Schema

Let's define a schema for our AI support ticket classifier.

```python
ticket_schema = {
    "type": "object",
    "properties": {
        "category": {
            "type": "string",
            "enum": ["technical", "billing", "general"]
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"]
        },
        "summary": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": [
        "category",
        "priority",
        "summary"
    ],
    "additionalProperties": False
}
```

### Explanation

- `type: object` means the data must be a JSON object.
- `properties` describes its fields.
- `enum` restricts the category and priority.
- `minLength: 5` requires at least five characters in the summary.
- `required` identifies mandatory fields.
- `additionalProperties: False` rejects unexpected fields.

## 6. Valid and Invalid Data

### Valid Ticket

```json
{
  "category": "technical",
  "priority": "high",
  "summary": "Customer cannot log in"
}
```

### Invalid Ticket

```json
{
  "category": "unknown",
  "priority": "urgent",
  "summary": "Help"
}
```

The invalid ticket violates three rules:

1. `unknown` is not an allowed category.
2. `urgent` is not an allowed priority.
3. `Help` contains fewer than five characters.

These are the same issues we detected with Pydantic.

## 7. Validating JSON Schema in Python

Python's built-in `json` module parses JSON, but it does not validate JSON Schema.

For schema validation, we can use the `jsonschema` library.

Install it:

```powershell
python -m pip install jsonschema
```

Example:

```python
from jsonschema import validate, ValidationError

ticket = {
    "category": "technical",
    "priority": "high",
    "summary": "Customer cannot log in"
}

try:
    validate(instance=ticket, schema=ticket_schema)
    print("Ticket is valid!")

except ValidationError as error:
    print("Validation failed:", error.message)
```

Expected output:

```text
Ticket is valid!
```

## 8. Finding Multiple Validation Errors

The simple `validate()` function reports a validation failure. To collect multiple errors, use a validator.

```python
from jsonschema import Draft202012Validator

invalid_ticket = {
    "category": "unknown",
    "priority": "urgent",
    "summary": "Help"
}

validator = Draft202012Validator(ticket_schema)

errors = sorted(
    validator.iter_errors(invalid_ticket),
    key=lambda error: str(error.path)
)

for error in errors:
    print("Error:", error.message)
```

This allows us to inspect all three problems instead of stopping at the first error.

## 9. JSON Schema vs TypedDict vs Pydantic

| Feature              | TypedDict                    | Pydantic             | JSON Schema              |
| -------------------- | ---------------------------- | -------------------- | ------------------------ |
| Main purpose         | Describe Python dictionaries | Validate Python data | Describe JSON structures |
| Runtime validation   | Not by itself                | Built-in             | With a validator         |
| Language-independent | No                           | No                   | Yes                      |
| Field descriptions   | `Annotated`                  | `Field()`            | `description`            |
| Value restrictions   | `Literal` hints              | Enforced constraints | `enum` and other rules   |

## 10. How JSON Schema Is Used with LangChain

LangChain can work with JSON Schema dictionaries to describe structured model responses.

A simple schema might look like:

```python
review_schema = {
    "title": "Review",
    "description": "Extract information from a customer review",
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "string",
            "enum": ["positive", "negative", "neutral"]
        },
        "summary": {
            "type": "string"
        }
    },
    "required": ["sentiment", "summary"],
    "additionalProperties": False
}
```

The schema can be supplied to a compatible LangChain model integration using `with_structured_output()`.

However, the accepted schema format and supported features depend on the model provider and selected structured-output method.

We will test this in the next topic.

## 11. JSON Schema and LLM Reliability

JSON Schema helps define valid output structures, but it does not guarantee factual correctness.

For example:

```json
{
  "category": "technical",
  "priority": "high",
  "summary": "Customer cannot log in"
}
```

This may be structurally valid even if the original customer message was actually about a billing problem.

**Therefore, schema validation checks structure and constraints, not whether an LLM understood the input correctly.**

## 12. Interview Questions

**Q1. What is JSON Schema?**

A standard for defining the expected structure and constraints of JSON data.

**Q2. What does `properties` do?**

Defines the fields expected inside an object.

**Q3. What does `required` do?**

Specifies which fields must be present.

**Q4. What does `enum` do?**

Restricts a value to one of the predefined choices.

**Q5. What does `additionalProperties: false` mean?**

Unexpected properties are not allowed.

**Q6. Does `json.loads()` validate a JSON Schema?**

No. It only parses JSON syntax.

**Q7. How can we validate JSON Schema in Python?**

Using a library such as `jsonschema`.

**Q8. How is JSON Schema different from Pydantic?**

JSON Schema is a language-independent schema standard, while Pydantic is a Python validation library.

**Q9. Can Pydantic generate JSON Schema?**

Yes, using `model_json_schema()`.

**Q10. Does JSON Schema guarantee factually correct LLM output?**

No. It validates data structure and specified rules.

## 13. Key Takeaways

- JSON Schema defines rules for JSON data.
- `properties` specifies fields and their types.
- `required` specifies mandatory fields.
- `enum` restricts values.
- `additionalProperties` controls unexpected fields.
- `jsonschema` performs runtime validation in Python.
- Pydantic can generate JSON Schema automatically.
- LangChain can use JSON Schema for structured-output integrations.
- Valid structure does not guarantee accurate information.

---

## Learning Resources

- [JSON Schema Official Documentation](https://json-schema.org/understanding-json-schema/)
- [Python jsonschema Documentation](https://python-jsonschema.readthedocs.io/)
- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)

**Learning Journey:** Section 05 — Topic 04
