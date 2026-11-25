# 05 — PydanticOutputParser in LangChain

## 1. What Is PydanticOutputParser?

`PydanticOutputParser` is a LangChain component that converts model-generated JSON into a validated Pydantic model instance.

It combines two operations:

1. **Parsing:** Convert JSON text into structured Python data.
2. **Validation:** Check that the data follows a Pydantic schema.

### Example

Suppose an AI model generates:

```json
{
  "category": "technical",
  "priority": "high",
  "summary": "Customer cannot log in"
}
```

We want to convert this into a validated `SupportTicket` object.

## 2. Why Do We Need PydanticOutputParser?

In previous topics, we used `JsonOutputParser` and `StructuredOutputParser`.

These parsers help extract JSON data, but we may also need to enforce important rules.

For example:

- Category must be `technical`, `billing`, or `general`.
- Priority must be `low`, `medium`, or `high`.
- Summary must contain at least five characters.

Pydantic allows us to validate these requirements.

## 3. Importing PydanticOutputParser

```python
from langchain_core.output_parsers import PydanticOutputParser
```

We also need Pydantic:

```python
from pydantic import BaseModel, Field
```

Unlike the legacy `StructuredOutputParser`, `PydanticOutputParser` is available in `langchain-core`.

## 4. Defining a Pydantic Schema

```python
from typing import Literal
from pydantic import BaseModel, Field

class SupportTicket(BaseModel):
    category: Literal["technical", "billing", "general"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(min_length=5)
```

### Explanation

- `BaseModel` enables runtime validation.
- `Literal` restricts the accepted values.
- `Field(min_length=5)` requires a sufficiently long summary.

## 5. Creating the Parser

```python
parser = PydanticOutputParser(
    pydantic_object=SupportTicket
)
```

The `pydantic_object` parameter specifies which Pydantic model will validate the parsed output.

## 6. Understanding get_format_instructions()

```python
print(parser.get_format_instructions())
```

This generates instructions describing the JSON structure expected by the Pydantic model.

These instructions can be included in the prompt sent to the LLM.

**Important:** The instructions guide generation but do not guarantee that the model will always produce valid JSON.

## 7. Testing the Parser Without an LLM

```python
json_text = '''
{
    "category": "technical",
    "priority": "high",
    "summary": "Customer cannot log in"
}
'''

result = parser.parse(json_text)

print(result)
print(type(result))
print(result.model_dump())
```

### Expected Result

The parsed result is an instance of `SupportTicket`.

We can access its fields using dot notation:

```python
print(result.category)
print(result.priority)
print(result.summary)
```

## 8. What Happens with Invalid Data?

Consider:

```json
{
  "category": "unknown",
  "priority": "urgent",
  "summary": "Help"
}
```

This violates the Pydantic schema.

```python
from langchain_core.exceptions import OutputParserException

try:
    result = parser.parse('''
    {
        "category": "unknown",
        "priority": "urgent",
        "summary": "Help"
    }
    ''')
except OutputParserException as error:
    print("Parsing or validation failed:", error)
```

The parser raises an `OutputParserException` when it cannot produce an object satisfying the Pydantic schema.

## 9. Using PydanticOutputParser with Groq

We can combine the parser with Groq GPT-OSS 120B.

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

parser = PydanticOutputParser(
    pydantic_object=SupportTicket
)

prompt = PromptTemplate(
    template="""
    Classify the following support ticket:

    {message}

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | model | parser

result = chain.invoke({
    "message": "My account is locked. Please help urgently."
})

print(result)
print(result.model_dump())
```

### Execution Flow

```text
Customer Message
       |
       v
PromptTemplate
       |
       v
ChatGroq
       |
       v
PydanticOutputParser
       |
       v
Validated SupportTicket Object
```

## 10. Understanding the Returned Object

The result is a Pydantic model instance.

```python
print(type(result))
print(result.category)
print(result.priority)
print(result.summary)
```

We can convert it into a dictionary:

```python
data = result.model_dump()
print(data)
```

Or into JSON text:

```python
print(result.model_dump_json())
```

This is useful when preparing responses for backend APIs or storing structured data.

## 11. Comparing the Four Output Parsers

| Parser                   | Typical Output     | Runtime Schema Validation                        |
| ------------------------ | ------------------ | ------------------------------------------------ |
| `StrOutputParser`        | String             | No                                               |
| `JsonOutputParser`       | Dictionary or list | Not automatically                                |
| `StructuredOutputParser` | Dictionary         | Checks expected keys, not full field constraints |
| `PydanticOutputParser`   | Pydantic model     | Yes                                              |

## 12. PydanticOutputParser vs with_structured_output()

We previously used:

```python
structured_model = model.with_structured_output(
    SupportTicket,
    method="json_schema",
    strict=True
)
```

### PydanticOutputParser

- Supplies formatting instructions through a prompt.
- Receives generated text from the model.
- Parses and validates the generated JSON.
- May fail if the model does not follow the requested format.

### with_structured_output()

- Configures a compatible model's structured-output capabilities.
- May use provider-native JSON Schema or tool calling.
- Can provide stronger format guarantees when supported.
- Can also return validated Pydantic objects.

For compatible models such as Groq GPT-OSS 120B, provider-native structured output is often preferable for production workflows requiring strict schemas.

However, `PydanticOutputParser` remains useful when learning parsing or working with models that lack native structured output.

## 13. Common Beginner Mistakes

**Mistake 1 — Forgetting the Pydantic model**

The parser requires a model to define expected fields and constraints.

**Mistake 2 — Assuming formatting instructions guarantee valid JSON**

The LLM may still produce malformed output.

**Mistake 3 — Confusing parsing with factual verification**

Pydantic checks structure and constraints, not whether the model interpreted the customer correctly.

**Mistake 4 — Assuming the result is a dictionary**

A successful `PydanticOutputParser` typically returns a Pydantic instance, not a plain dictionary.

**Mistake 5 — Ignoring parsing errors**

Applications should handle invalid model outputs appropriately.

## 14. Interview Questions

**Q1. What is PydanticOutputParser?**

A LangChain parser that converts generated JSON into validated Pydantic objects.

**Q2. What does pydantic_object do?**

Specifies the Pydantic model used for validation.

**Q3. What does get_format_instructions() do?**

Generates instructions describing the desired JSON format.

**Q4. What does parser.parse() do?**

Parses model-generated text and validates it against the Pydantic model.

**Q5. What does model_dump() do?**

Converts a Pydantic model instance into a Python dictionary.

**Q6. What happens when the generated data violates the schema?**

The parser raises a parsing or validation exception.

**Q7. How is PydanticOutputParser different from JsonOutputParser?**

It validates the parsed output against a Pydantic model.

**Q8. Does PydanticOutputParser guarantee factual accuracy?**

No. It validates structure and specified constraints.

## 15. Key Takeaways

- `PydanticOutputParser` combines JSON parsing with Pydantic validation.
- It uses `pydantic_object` to define the expected schema.
- `get_format_instructions()` guides the model toward the required format.
- A successful result is a Pydantic model instance.
- Invalid structured data raises parsing or validation errors.
- It integrates with LCEL using `prompt | model | parser`.
- Provider-native structured output is an alternative when supported.

---

## Learning Resources

- [LangChain PydanticOutputParser Reference](https://reference.langchain.com/python/langchain-core/output_parsers/pydantic/PydanticOutputParser)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [CampusX Output Parsers Repository](https://github.com/campusx-official/langchain-output-parsers)

**Learning Journey:** Section 06 — Topic 05
