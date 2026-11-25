# 06 — Structured Output: Quick Revision

## 1. Core Concepts

| Concept                  | Explanation                                        |
| ------------------------ | -------------------------------------------------- |
| Structured Output        | Data returned in a predefined format               |
| Schema                   | Defines expected fields, types, and constraints    |
| JSON                     | Text-based format for structured data              |
| TypedDict                | Describes Python dictionary types                  |
| Pydantic                 | Provides runtime data validation                   |
| BaseModel                | Base class for Pydantic data models                |
| Field                    | Defines descriptions and validation constraints    |
| Literal                  | Restricts values to predefined choices             |
| Annotated                | Adds metadata to type annotations                  |
| JSON Schema              | Standard for describing JSON data structures       |
| with_structured_output() | Configures an LLM to generate structured responses |

## 2. TypedDict vs Pydantic vs JSON Schema

| Feature               | TypedDict         | Pydantic  | JSON Schema           |
| --------------------- | ----------------- | --------- | --------------------- |
| Defines structure     | Yes               | Yes       | Yes                   |
| Runtime validation    | No, not by itself | Yes       | Using a validator     |
| Python-specific       | Yes               | Yes       | No                    |
| Required fields       | Yes               | Yes       | Yes                   |
| Restricted values     | Type hints        | Enforced  | Enforced by validator |
| LangChain integration | Supported         | Supported | Supported             |

## 3. Important Methods

| Method                     | Purpose                                     |
| -------------------------- | ------------------------------------------- |
| `model_validate()`         | Validates Python data using Pydantic        |
| `model_dump()`             | Converts a Pydantic model into a dictionary |
| `model_dump_json()`        | Converts a Pydantic model into JSON text    |
| `model_json_schema()`      | Generates JSON Schema from a Pydantic model |
| `with_structured_output()` | Configures a model for structured output    |
| `invoke()`                 | Executes a model request                    |
| `iter_errors()`            | Collects JSON Schema validation errors      |

## 4. Practical Test Results

### TypedDict

Incorrect values such as `unknown` and `urgent` were accepted at runtime.

**Result:** Demonstrated that TypedDict does not automatically validate dictionary contents.

### Pydantic

The invalid support ticket produced three errors:

1. Invalid category.
2. Invalid priority.
3. Summary shorter than five characters.

**Result:** Runtime validation worked.

### JSON Schema

The valid ticket passed, while the invalid ticket produced three validation errors.

**Result:** JSON Schema validation worked.

### LangChain with_structured_output()

Model: Groq GPT-OSS 120B

Method: `json_schema` with `strict=True`

Output:

```python
{
    "category": "technical",
    "priority": "high",
    "summary": "Unable to access account, urgent resolution needed"
}
```

Returned type: `SupportTicket` (Pydantic model).

**Result:** Structured output generated and parsed successfully.

## 5. Important Interview Questions

**Q1. What is structured output?**

Data generated in a predefined structure.

**Q2. Why is structured output useful?**

It makes LLM responses easier to integrate with applications, APIs, and databases.

**Q3. Does TypedDict validate data at runtime?**

No.

**Q4. What does Pydantic do?**

It defines data models and validates their values at runtime.

**Q5. What is JSON Schema?**

A standard for describing the expected structure and constraints of JSON data.

**Q6. What is Literal?**

A typing feature that specifies allowed values.

**Q7. What does Field() do?**

It adds metadata and validation constraints to Pydantic fields.

**Q8. What does with_structured_output() do?**

It configures a compatible LLM integration to produce structured responses.

**Q9. What is the difference between JSON parsing and schema validation?**

Parsing checks JSON syntax; validation checks whether the data satisfies the required structure and constraints.

**Q10. Does valid structured output guarantee correct facts?**

No. Structurally valid data can still contain incorrect information.

## 6. Key Takeaways

- TypedDict defines dictionary structures without automatic runtime validation.
- Pydantic enforces data types and constraints at runtime.
- JSON Schema provides language-independent data rules.
- LangChain can generate structured responses using compatible models.
- Groq GPT-OSS 120B successfully returned a Pydantic-validated support ticket.
- Structured data is useful in AI agents, RAG applications, ticket classifiers, and backend APIs.
- Important AI-generated information should still be checked for accuracy.

---

## Learning Resources

- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema Documentation](https://json-schema.org/)
- [Groq Structured Outputs](https://console.groq.com/docs/structured-outputs)

**Learning Journey:** Section 05 of 18

**Status:** All five practical topics completed and tested.
