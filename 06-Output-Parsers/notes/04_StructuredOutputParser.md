# 04 — StructuredOutputParser in LangChain

## 1. What Is StructuredOutputParser?

`StructuredOutputParser` is a LangChain parser that uses predefined response fields to guide an LLM toward a structured JSON response.

It is commonly used with `ResponseSchema`, which describes the expected fields.

For example, we want to extract:

```json
{
  "brand": "Lenovo",
  "product": "laptop",
  "price": 850
}
```

Instead of manually describing the format in every prompt, we define a list of response schemas.

**Note:** This parser is part of the older LangChain API and is now available through `langchain-classic`. We are learning it because it is covered in the CampusX course.

## 2. What Is ResponseSchema?

`ResponseSchema` describes one expected field.

```python
from langchain_classic.output_parsers import ResponseSchema

brand_schema = ResponseSchema(
    name="brand",
    description="The brand of the product",
    type="string"
)
```

### Parameters

- `name`: Name of the expected field.
- `description`: Explains what the field represents.
- `type`: Describes the expected output type for the model's formatting instructions.

These descriptions guide the model. They do not provide the same strict runtime validation as Pydantic.

## 3. Creating Multiple Response Schemas

```python
from langchain_classic.output_parsers import (
    ResponseSchema,
    StructuredOutputParser
)

response_schemas = [
    ResponseSchema(
        name="brand",
        description="Product brand",
        type="string"
    ),
    ResponseSchema(
        name="product",
        description="Type of product",
        type="string"
    ),
    ResponseSchema(
        name="price",
        description="Product price",
        type="number"
    )
]

parser = StructuredOutputParser.from_response_schemas(
    response_schemas
)
```

### Explanation

1. We define the fields using `ResponseSchema`.
2. We place the schemas in a list.
3. `from_response_schemas()` creates the parser.
4. The parser can generate formatting instructions and parse the model response.

## 4. Using get_format_instructions()

```python
instructions = parser.get_format_instructions()

print(instructions)
```

This generates instructions telling the model to return structured JSON with the specified fields.

The default instructions may request a Markdown JSON code block.

## 5. Creating a Prompt

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
    Extract product information from this message:

    {message}

    {format_instructions}
    """,
    input_variables=["message"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)
```

The formatting instructions are inserted automatically because they are supplied through `partial_variables`.

## 6. Connecting the Parser to Groq

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

chain = prompt | model | parser

result = chain.invoke({
    "message": "I purchased a Lenovo laptop for $850."
})

print(result)
print(type(result))
```

### Workflow

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
StructuredOutputParser
       |
       v
Python Dictionary
```

A successful result should contain the brand, product, and price fields.

## 7. Parsing a Response Without Calling an LLM

We can test the parser separately.

````python
sample_response = """
```json
{
  "brand": "Lenovo",
  "product": "laptop",
  "price": 850
}
````

"""

result = parser.parse(sample_response)

print(result)

```

The parser reads the JSON and returns a dictionary.

This is useful for testing parsing behavior without using API credits.

## 8. StructuredOutputParser vs JsonOutputParser

| Feature | JsonOutputParser | StructuredOutputParser |
|---|---|---|
| Parses JSON | Yes | Yes |
| Uses ResponseSchema | No | Yes |
| Generates format instructions | Yes | Yes |
| Returns dictionaries | Commonly | Yes |
| Strict Pydantic validation | Not by default | No |
| Modern package | `langchain-core` | `langchain-classic` |

`StructuredOutputParser` focuses on declaring expected response fields through `ResponseSchema`.

However, its field descriptions and type labels do not automatically provide strict runtime validation.

## 9. StructuredOutputParser vs PydanticOutputParser

`StructuredOutputParser` uses response-field descriptions and parses JSON into a dictionary.

`PydanticOutputParser` uses a Pydantic model to parse output and validate data against defined types and constraints.

For applications where strong validation matters, Pydantic is generally preferable.

## 10. Common Errors

**Missing required field:** The parser can raise an error when an expected response field is absent.

**Invalid JSON:** Malformed JSON may cause a parsing error.

**Incorrect value type:** The returned dictionary may contain an unexpected type because response descriptions are not strict runtime validators.

**Unsupported or moved imports:** Older LangChain tutorials may use import paths that no longer work with modern versions.

**Incorrect extracted facts:** The response may be structurally valid but factually inaccurate.

## 11. Quick Revision Questions

**Q1. What is StructuredOutputParser?**

A LangChain parser that uses response schemas to guide and parse structured JSON responses.

**Q2. What is ResponseSchema?**

A description of an expected output field.

**Q3. What does from_response_schemas() do?**

Creates a structured output parser from a list of response schemas.

**Q4. What does get_format_instructions() do?**

Generates formatting instructions for the language model.

**Q5. Does StructuredOutputParser perform Pydantic validation?**

No.

**Q6. Where is StructuredOutputParser available in modern LangChain?**

In the `langchain-classic` package.

**Q7. Can it be used in an LCEL chain?**

Yes, using `prompt | model | parser`.

## 12. Key Takeaways

- `StructuredOutputParser` parses structured JSON responses.
- `ResponseSchema` describes expected output fields.
- `from_response_schemas()` creates the parser.
- `get_format_instructions()` guides model formatting.
- The parser can be connected to Groq using LCEL.
- It is a legacy-style LangChain component.
- Parsing structured JSON does not automatically guarantee correct field types or facts.
- Pydantic provides stronger runtime validation.

---

## Learning Resources

- [CampusX Output Parsers Repository](https://github.com/campusx-official/langchain-output-parsers)
- [LangChain StructuredOutputParser Reference](https://reference.langchain.com/python/langchain-classic/output_parsers/structured/StructuredOutputParser)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 06 — Topic 04
```
