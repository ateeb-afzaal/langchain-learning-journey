# 05 — with_structured_output() in LangChain

## 1. What Is with_structured_output()?

`with_structured_output()` is a LangChain method that configures a compatible chat model to return data matching a specified schema.

Instead of receiving a normal paragraph, we can receive structured information as a Python dictionary or a validated Pydantic object.

## 2. Why Do We Need It?

Imagine a customer sends:

"I cannot log in to my account. Please resolve this urgently."

Our application needs:

```json
{
  "category": "technical",
  "priority": "high",
  "summary": "Customer cannot log in to their account"
}
```

With a structured-output schema, we can define these fields in advance.

## 3. Basic Workflow

1. Define a schema using TypedDict, Pydantic, or JSON Schema.
2. Initialize a compatible chat model.
3. Call `model.with_structured_output(schema)`.
4. Invoke the configured model.
5. Inspect and validate the result.
6. Use the structured data in the application.

## 4. Using TypedDict

```python
from typing import TypedDict, Literal
from langchain_groq import ChatGroq

class Ticket(TypedDict):
    category: Literal["technical", "billing", "general"]
    priority: Literal["low", "medium", "high"]
    summary: str

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

structured_model = model.with_structured_output(
    Ticket,
    method="json_schema"
)

result = structured_model.invoke(
    "I cannot log in to my account. Please help urgently."
)

print(result)
print(type(result))
```

A successful response is normally parsed into a Python dictionary.

**Important:** TypedDict alone does not provide Pydantic-style runtime validation.

## 5. Using Pydantic

```python
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class SupportTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Literal["technical", "billing", "general"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(description="Short summary of the issue")
```

Now configure the model:

```python
structured_model = model.with_structured_output(
    SupportTicket,
    method="json_schema",
    strict=True
)

result = structured_model.invoke(
    "My payment was charged twice. Please help."
)

print(result)
print(result.model_dump())
```

The result should be a validated Pydantic `SupportTicket` instance if the request succeeds.

## 6. Understanding the Methods

LangChain's Groq integration supports different structured-output approaches.

| Method             | Purpose                                     |
| ------------------ | ------------------------------------------- |
| `function_calling` | Uses tool/function calling                  |
| `json_mode`        | Requests JSON output                        |
| `json_schema`      | Uses Groq's dedicated structured-output API |

For the GPT-OSS 120B model, Groq supports native JSON Schema structured outputs.

With `strict=True`, Groq uses constrained decoding for supported schemas. In this mode, every object must disallow additional properties, and every property must be required.

Not all JSON Schema features or models are supported. We must handle API errors if the schema is incompatible.

## 7. What Does include_raw=True Do?

By default, a successful call returns the parsed result.

With `include_raw=True`:

```python
structured_model = model.with_structured_output(
    SupportTicket,
    method="json_schema",
    strict=True,
    include_raw=True
)

result = structured_model.invoke(
    "My account is locked."
)

print(result["raw"])
print(result["parsed"])
print(result["parsing_error"])
```

The result contains:

- `raw`: Original model response.
- `parsed`: Parsed structured data, when available.
- `parsing_error`: Parsing or validation error, if captured.

This is helpful for debugging.

## 8. TypedDict vs Pydantic in Structured Output

| TypedDict                                 | Pydantic                             |
| ----------------------------------------- | ------------------------------------ |
| Defines expected dictionary fields        | Defines a validated model            |
| Usually returns a dictionary              | Returns a model instance             |
| No automatic TypedDict runtime validation | Performs Pydantic runtime validation |
| Lightweight                               | Supports validation and constraints  |

## 9. Structured Output vs JSON Parsing

There is an important difference:

**Asking for JSON in a prompt**

The LLM receives a text instruction asking it to return JSON. It may still produce an unexpected format.

**Using structured output**

The schema is supplied through a supported model integration and structured-output mechanism.

**Validating the result**

The application checks the parsed values using Pydantic or another validator.

These are related but distinct operations.

## 10. Common Errors

**Unsupported model or method:** The model may not support the chosen structured-output feature.

**Invalid schema:** The provider may reject an unsupported schema structure.

**Missing API key:** Groq authentication fails.

**Parsing error:** The response cannot be parsed into the requested structure.

**Validation error:** The parsed data violates model constraints.

**Incorrect extracted facts:** A response may satisfy its schema while misinterpreting the input.

## 11. Interview Questions

**Q1. What does with_structured_output() do?**

It configures a chat model to return structured data matching a supplied schema.

**Q2. Can we use Pydantic?**

Yes, with compatible model integrations.

**Q3. Can we use TypedDict?**

Yes.

**Q4. What is json_schema mode?**

A method that uses a provider's native structured-output API.

**Q5. What does strict=True mean?**

For supported Groq models, it enables constrained generation using supported JSON Schema constraints.

**Q6. What does include_raw=True return?**

Raw response, parsed result, and parsing error information.

**Q7. Does structured output guarantee factual correctness?**

No. It helps enforce structure, not the truth of extracted facts.

## 12. Key Takeaways

- `with_structured_output()` connects a schema to a chat model.
- TypedDict can define dictionary-shaped responses.
- Pydantic adds runtime validation.
- JSON Schema describes the expected structure.
- `json_schema` uses provider-native structured output where supported.
- Strict mode requires compatible schemas and models.
- Applications must still handle errors and verify important facts.

---

## Learning Resources

- [LangChain Groq Integration Reference](https://reference.langchain.com/python/langchain-groq/chat_models/ChatGroq/with_structured_output)
- [Groq Structured Outputs](https://console.groq.com/docs/structured-outputs)
- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)

**Learning Journey:** Section 05 — Topic 05
