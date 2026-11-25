# 01 — Output Parser Basics in LangChain

## 1. What Is an Output Parser?

An **output parser** is a LangChain component that converts a language model's response into a format that is easier for Python applications to use.

For example, a chat model normally returns an `AIMessage` object containing the generated content and additional information.

An output parser can extract plain text, parse JSON, or validate generated information against a schema.

### Simple Example

Without an output parser:

```python
response = model.invoke("What is Python?")

print(type(response))
print(response.content)
```

The model normally returns an `AIMessage`.

With an output parser:

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

result = parser.invoke(response)

print(type(result))
print(result)
```

The result is a Python string.

## 2. Why Do We Need Output Parsers?

AI applications often require specific data formats.

For example, imagine we're building a customer support ticket classifier.

The model might respond:

"The ticket is about a technical issue and should receive high priority."

But our backend application expects:

```json
{
  "category": "technical",
  "priority": "high"
}
```

A suitable output parser can convert correctly formatted model output into Python data structures.

### Benefits

- Simplifies processing LLM responses.
- Extracts the information applications need.
- Supports JSON-based workflows.
- Integrates with LangChain chains.
- Helps enforce expected data formats when paired with validation.

**Important:** An output parser cannot automatically transform arbitrary paragraphs into valid structured data. The model must generate a compatible format, or a separate extraction step must be used.

---

## 3. Understanding AIMessage

When we call a LangChain chat model:

```python
response = model.invoke("Explain Python lists.")
```

The response is normally an `AIMessage` object.

We can inspect it:

```python
print(type(response))
print(response.content)
print(response.response_metadata)
```

### Important Properties

| Property            | Purpose                                 |
| ------------------- | --------------------------------------- |
| `content`           | Generated response content              |
| `response_metadata` | Provider-specific response information  |
| `usage_metadata`    | Token usage information, when available |
| `tool_calls`        | Structured tool calls, when generated   |

The exact metadata depends on the model provider.

## 4. AIMessage vs Python String

An `AIMessage` contains more than just text.

Example:

```python
response = model.invoke("Hello!")

print(response.content)
```

To extract text using an output parser:

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

text = parser.invoke(response)

print(text)
print(type(text))
```

The parser produces a Python string for ordinary text responses.

### Comparison

| AIMessage                           | String                               |
| ----------------------------------- | ------------------------------------ |
| LangChain message object            | Standard Python data type            |
| Contains content and metadata       | Contains text                        |
| Can contain tool calls              | Cannot represent tool calls directly |
| Useful for conversational workflows | Useful for text processing           |

## 5. Common Output Parsers in LangChain

### A. StrOutputParser

Converts a model response into plain text.

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
```

Typical output:

```text
Python is a high-level programming language.
```

### B. JsonOutputParser

Parses JSON-formatted model output into Python dictionaries or lists.

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
```

Example model output:

```json
{
  "name": "Ali",
  "age": 22
}
```

Parsed result:

```python
{"name": "Ali", "age": 22}
```

### C. StructuredOutputParser

A parser that uses predefined response fields to format instructions and parse structured text.

It is commonly used with `ResponseSchema`.

```python
from langchain_classic.output_parsers import (
    ResponseSchema,
    StructuredOutputParser
)
```

This is a legacy-style parser covered in the CampusX course. The package location can differ from older tutorials.

### D. PydanticOutputParser

Parses model-generated data into a Pydantic model and validates it.

```python
from langchain_core.output_parsers import PydanticOutputParser
```

We'll study each parser separately.

---

## 6. What Is Parsing?

**Parsing** means reading data in a particular format and converting it into a usable representation.

For example:

```python
import json

json_text = '{"name": "Ali", "age": 22}'

data = json.loads(json_text)

print(data["name"])
```

Expected output:

```text
Ali
```

Here, `json.loads()` parses JSON text into a Python dictionary.

## 7. Parsing vs Validation

Parsing and validation are related but different operations.

### Parsing

Checks whether text can be interpreted as the expected format.

For example, valid JSON:

```json
{
  "name": "Ali",
  "age": "twenty"
}
```

### Validation

Checks whether the parsed values satisfy a predefined schema.

If the schema requires `age` to be an integer, the value `"twenty"` may fail validation.

### Comparison

| Parsing                                  | Validation                            |
| ---------------------------------------- | ------------------------------------- |
| Converts formatted text into usable data | Checks data against requirements      |
| Can detect malformed JSON                | Can detect incorrect fields or values |
| Example: `json.loads()`                  | Example: Pydantic                     |

Some LangChain parsers combine both operations.

## 8. Understanding LCEL

LangChain Expression Language (LCEL) allows us to connect processing components using the pipe operator (`|`).

Example:

```python
chain = prompt | model | parser
```

### Execution Flow

```text
Input Dictionary
       |
       v
Prompt Template
       |
       v
Chat Model
       |
       v
Output Parser
       |
       v
Python Result
```

For example:

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template(
    "Explain {topic} in one sentence."
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({
    "topic": "Machine Learning"
})

print(result)
```

This example assumes `model` has already been initialized.

## 9. Output Parsers vs with_structured_output()

In Section 05, we used:

```python
structured_model = model.with_structured_output(
    SupportTicket,
    method="json_schema",
    strict=True
)
```

This uses a supported provider's structured-output capability.

A traditional output parser often works differently:

1. Provide formatting instructions to the model.
2. Receive generated text.
3. Parse the response.
4. Validate it when appropriate.

### Comparison

| Output Parser                         | with_structured_output()                  |
| ------------------------------------- | ----------------------------------------- |
| Processes generated output            | Configures structured model generation    |
| Often relies on format instructions   | Can use provider-native structured output |
| May fail on malformed responses       | May provide stronger format guarantees    |
| Useful in general LangChain workflows | Useful when model integration supports it |

Neither approach guarantees that the information is factually correct.

## 10. Common Beginner Mistakes

**Mistake 1 — Assuming an output parser generates AI responses**

The model generates responses. The parser processes those responses.

**Mistake 2 — Confusing parsing with validation**

Successfully parsing JSON does not guarantee that the data satisfies a schema.

**Mistake 3 — Assuming every output parser accepts arbitrary text**

Parsers expect particular formats.

**Mistake 4 — Ignoring parsing errors**

Applications should handle unexpected output safely.

**Mistake 5 — Assuming every parser is part of langchain-core**

Some older parsers have moved into separate packages, such as `langchain-classic`.

---

## 11. Real-World Applications

### Customer Support

Convert generated classifications into Python dictionaries.

### Sentiment Analysis

Extract sentiment categories and supporting explanations.

### Information Extraction

Parse names, dates, prices, and other fields.

### Document Analysis

Convert extracted information into structured data.

### AI Workflows

Pass model-generated information into downstream processing steps.

## 12. Quick Revision Questions

**Q1. What is an output parser?**

A component that processes model responses into useful formats.

**Q2. What does StrOutputParser return?**

A Python string for ordinary text responses.

**Q3. What does JsonOutputParser return?**

Parsed JSON data, usually a dictionary or list.

**Q4. What does PydanticOutputParser do?**

Parses and validates generated output using a Pydantic model.

**Q5. What is an AIMessage?**

A LangChain message object representing an assistant response.

**Q6. What is parsing?**

Converting data from a particular format into a usable representation.

**Q7. What is validation?**

Checking whether data satisfies defined rules.

**Q8. What does the pipe operator do?**

Connects compatible LangChain components into a workflow.

**Q9. Does an output parser call the LLM by itself?**

No.

**Q10. Does successfully parsed JSON guarantee factual accuracy?**

No.

## 13. Key Takeaways

- Output parsers transform model responses into usable Python data.
- Chat models normally return `AIMessage` objects.
- `StrOutputParser` extracts text.
- `JsonOutputParser` parses JSON-formatted content.
- `StructuredOutputParser` supports response-field schemas.
- `PydanticOutputParser` provides runtime validation.
- Parsing and validation are different operations.
- LCEL connects prompts, models, and parsers.
- Provider-native structured output can offer stronger format guarantees when supported.

---

## Learning Resources

- [CampusX Output Parsers Repository](https://github.com/campusx-official/langchain-output-parsers)
- [LangChain Documentation](https://docs.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Learning Journey:** Section 06 — Topic 01
