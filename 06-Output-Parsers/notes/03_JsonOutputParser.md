# 03 — JsonOutputParser in LangChain

## 1. What Is JsonOutputParser?

`JsonOutputParser` is a LangChain component used to parse JSON-formatted language model output into Python data structures.

For example, suppose an AI model generates:

```json
{
  "name": "Python",
  "category": "Programming Language",
  "difficulty": "Beginner"
}
```

`JsonOutputParser` converts this JSON response into a Python dictionary that our application can access directly.

## 2. Why Do We Need JsonOutputParser?

Imagine we're building an AI application that extracts information from customer messages.

Customer message:

"I purchased a Lenovo laptop for $850."

We want:

```json
{
  "brand": "Lenovo",
  "product": "Laptop",
  "price": 850
}
```

Once parsed, Python can access:

```python
print(result["brand"])
print(result["price"])
```

This is easier than manually extracting values from a paragraph.

## 3. Importing JsonOutputParser

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
```

The parser processes correctly formatted JSON output.

It does not independently generate an AI response.

## 4. Understanding get_format_instructions()

`JsonOutputParser` provides formatting instructions that can be included in a prompt.

```python
parser = JsonOutputParser()

print(parser.get_format_instructions())
```

These instructions tell the model to return JSON rather than ordinary text.

For more specific output requirements, we should also describe the fields in the prompt or provide a compatible schema.

## 5. Creating a JSON Prompt

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
    Extract the product information from this message:

    {message}

    Return an object containing:
    - brand
    - product
    - price

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)
```

### Explanation

- `{message}` contains the customer input.
- `get_format_instructions()` supplies JSON formatting guidance.
- `partial_variables` pre-fills the instructions.
- The prompt can be reused for different customer messages.

## 6. Connecting JsonOutputParser with Groq

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
    Extract these fields from the message:
    brand, product, price.

    Message: {message}

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | model | parser

result = chain.invoke({
    "message": "I purchased a Lenovo laptop for $850."
})

print(result)
print(type(result))
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
JsonOutputParser
       |
       v
Python Dictionary
```

The output should contain structured information about the Lenovo laptop.

## 7. Accessing Parsed Values

If the model returns a JSON object, the parser typically produces a Python dictionary.

```python
print("Brand:", result["brand"])
print("Product:", result["product"])
print("Price:", result["price"])
```

If the response contains a JSON array, the parser may produce a Python list instead.

## 8. Parsing JSON Without an LLM

We can also test a parser directly.

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

json_text = '''
{
  "name": "Ali",
  "age": 22
}
'''

result = parser.parse(json_text)

print(result)
print(type(result))
```

Expected output:

```text
{'name': 'Ali', 'age': 22}
<class 'dict'>
```

This is useful for understanding parsers separately from model calls.

## 9. Handling Invalid JSON

A language model may produce malformed JSON.

```python
from langchain_core.exceptions import OutputParserException

parser = JsonOutputParser()

try:
    result = parser.parse('{"name": "Ali", "age": }')
    print(result)
except OutputParserException as error:
    print("JSON parsing failed:", error)
```

Applications should handle parsing errors rather than assuming every response will be valid.

## 10. JsonOutputParser vs StrOutputParser

| Feature                   | StrOutputParser        | JsonOutputParser                        |
| ------------------------- | ---------------------- | --------------------------------------- |
| Main purpose              | Extract text           | Parse JSON                              |
| Output                    | String                 | Dictionary, list, or another JSON value |
| Format instructions       | Usually unnecessary    | Available                               |
| Useful for                | Chatbots and summaries | Structured data extraction              |
| Runtime schema validation | No                     | Not automatically                       |

## 11. JsonOutputParser vs with_structured_output()

`JsonOutputParser` generally parses generated content after the model responds.

`with_structured_output()` configures a compatible model for structured generation, potentially using native provider features.

The two approaches can achieve similar application goals but work differently.

**Important:** `JsonOutputParser` alone does not enforce all field types, allowed values, or required keys. Use Pydantic or another validator when those guarantees matter.

## 12. Common Beginner Mistakes

**Mistake 1 — Assuming the parser generates JSON**

The model generates the response; the parser processes it.

**Mistake 2 — Forgetting formatting instructions**

Without sufficient guidance, the model may return ordinary prose.

**Mistake 3 — Assuming valid JSON means valid data**

The JSON may contain missing keys or incorrect values.

**Mistake 4 — Accessing keys without checking them**

A missing key can raise a `KeyError`.

**Mistake 5 — Assuming every response will parse correctly**

Parsing errors are possible and should be handled.

## 13. Interview Questions

**Q1. What is JsonOutputParser?**

A LangChain parser that converts JSON-formatted model output into Python data structures.

**Q2. What does get_format_instructions() do?**

Provides instructions intended to guide the model toward JSON output.

**Q3. What is the output type of JsonOutputParser?**

It depends on the JSON value, commonly a Python dictionary or list.

**Q4. Does JsonOutputParser call the LLM?**

No.

**Q5. Does JsonOutputParser automatically validate every field?**

No.

**Q6. Can we use JsonOutputParser with LCEL?**

Yes, with `prompt | model | parser`.

**Q7. How should we handle invalid JSON?**

Catch parsing errors and implement suitable recovery or error reporting.

## 14. Key Takeaways

- `JsonOutputParser` parses JSON-formatted output.
- It often converts model responses into Python dictionaries.
- `get_format_instructions()` helps guide JSON generation.
- LCEL connects prompts, models, and parsers.
- JSON parsing and schema validation are different.
- Model outputs can still contain unexpected values or malformed JSON.
- Use explicit validation when application correctness depends on the data structure.

---

## Learning Resources

- [CampusX Output Parsers Repository](https://github.com/campusx-official/langchain-output-parsers)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 06 — Topic 03
