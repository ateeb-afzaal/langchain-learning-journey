# 06 — Output Parsers: Quick Revision

## 1. What Are Output Parsers?

Output parsers are LangChain components that convert language model responses into formats that Python applications can use.

They are commonly connected to prompts and models using LangChain Expression Language (LCEL).

```python
chain = prompt | model | parser
```

The prompt prepares the instructions, the model generates a response, and the parser processes the output.

---

## 2. Four Important Output Parsers

| Parser                   | Purpose                                     | Typical Result                              |
| ------------------------ | ------------------------------------------- | ------------------------------------------- |
| `StrOutputParser`        | Extract model-generated text                | Python string or compatible string subclass |
| `JsonOutputParser`       | Parse JSON-formatted output                 | Dictionary or list                          |
| `StructuredOutputParser` | Parse JSON using predefined response fields | Dictionary                                  |
| `PydanticOutputParser`   | Parse and validate output using Pydantic    | Pydantic model instance                     |

### StrOutputParser

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = prompt | model | parser
```

Useful for chatbots, summaries, and text-generation applications.

### JsonOutputParser

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

chain = prompt | model | parser
```

Useful when the application expects JSON-formatted information.

### StructuredOutputParser

```python
from langchain_classic.output_parsers import (
    ResponseSchema,
    StructuredOutputParser
)

schemas = [
    ResponseSchema(
        name="name",
        description="Name of the person",
        type="string"
    )
]

parser = StructuredOutputParser.from_response_schemas(
    schemas
)
```

Useful for learning schema-guided text parsing. This is a legacy-style LangChain parser.

### PydanticOutputParser

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)

parser = PydanticOutputParser(
    pydantic_object=Product
)
```

Useful when generated JSON must be checked against field types and validation constraints.

---

## 3. Important Methods

| Method                      | Purpose                                   |
| --------------------------- | ----------------------------------------- |
| `parser.invoke()`           | Process parser input                      |
| `parser.parse()`            | Parse generated text                      |
| `get_format_instructions()` | Generate model-facing formatting guidance |
| `ResponseSchema()`          | Describe an expected output field         |
| `from_response_schemas()`   | Build a StructuredOutputParser            |
| `model_dump()`              | Convert a Pydantic model to a dictionary  |
| `chain.invoke()`            | Execute a complete LCEL workflow          |

## 4. Parsing vs Validation vs Structured Generation

**Parsing** converts text into usable data.

Example: JSON text becomes a Python dictionary.

**Validation** checks whether data satisfies rules.

Example: A priority must be `low`, `medium`, or `high`.

**Structured generation** configures a compatible model to produce output that follows a supplied schema.

Example:

```python
structured_model = model.with_structured_output(
    SupportTicket,
    method="json_schema",
    strict=True
)
```

For compatible Groq models, native structured output can provide stronger structural guarantees than prompt instructions alone.

Even validated output can contain factually incorrect information.

---

## 5. Practical Test Results

### StrOutputParser — Verified

Our test demonstrated:

- Without parser: `AIMessage`
- With parser: `TextAccessor` in the installed LangChain version
- With explicit `str()` conversion: built-in Python `str`
- Standard string operations worked

### JsonOutputParser — Verified

Customer input:

"I bought a Lenovo laptop for $850."

Extracted information:

```python
{
    "brand": "Lenovo",
    "product": "laptop",
    "price": 850
}
```

### StructuredOutputParser — Example Created

The example uses `ResponseSchema` to describe the brand, product, and price fields.

Its successful execution should be confirmed separately.

### PydanticOutputParser — Example Created

The example uses a `SupportTicket` schema with:

- Restricted category values
- Restricted priority values
- A minimum summary length

Its successful execution should be confirmed separately.

---

## 6. Important Interview Questions

**Q1. What is an output parser?**

A component that converts language model output into a usable format.

**Q2. What does StrOutputParser do?**

Extracts text from a model response.

**Q3. What does JsonOutputParser do?**

Parses JSON-formatted output into Python data.

**Q4. What is ResponseSchema?**

A description of an expected output field used by StructuredOutputParser.

**Q5. What does PydanticOutputParser do?**

Parses generated JSON and validates it using a Pydantic model.

**Q6. What is the difference between JsonOutputParser and PydanticOutputParser?**

JsonOutputParser focuses on parsing JSON, while PydanticOutputParser also validates the result against a Pydantic model.

**Q7. Does StrOutputParser validate JSON?**

No.

**Q8. What is the purpose of get_format_instructions()?**

It produces instructions to guide the model toward the required output format.

**Q9. What is LCEL?**

LangChain Expression Language, used to compose processing components into workflows.

**Q10. What does the pipe operator (`|`) do?**

Connects compatible LangChain components.

**Q11. Does parsing guarantee factual accuracy?**

No.

**Q12. What happens when output violates the expected Pydantic schema?**

The parser raises an error instead of returning a successfully validated model instance.

---

## 7. Which Parser Should We Choose?

| Requirement                                      | Suitable Choice          |
| ------------------------------------------------ | ------------------------ |
| Generate plain text                              | StrOutputParser          |
| Parse JSON-formatted text                        | JsonOutputParser         |
| Follow legacy CampusX ResponseSchema examples    | StructuredOutputParser   |
| Validate JSON output with Python models          | PydanticOutputParser     |
| Enforce provider-supported structured generation | with_structured_output() |

For production applications, prefer validation and provider-native structured generation when supported and appropriate.

## 8. Key Takeaways

- Output parsers process generated model responses.
- Different parsers return different Python types.
- StrOutputParser is useful for text pipelines.
- JsonOutputParser parses JSON.
- StructuredOutputParser uses response-field descriptions.
- PydanticOutputParser validates against Pydantic models.
- LCEL makes it easy to combine prompts, models, and parsers.
- Parsing, validation, and structured generation serve different purposes.
- Applications should handle invalid outputs and model errors.

---

## Learning Resources

- [CampusX Output Parsers Repository](https://github.com/campusx-official/langchain-output-parsers)
- [LangChain Documentation](https://docs.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Learning Journey:** Section 06 of 18

**Status:** Notes complete; final example verification pending.
