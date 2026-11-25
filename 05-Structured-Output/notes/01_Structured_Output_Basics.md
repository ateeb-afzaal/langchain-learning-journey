# 01 — Structured Output Basics in LangChain

## 1. What Is Structured Output?

Structured output means receiving information from a language model in a predefined format, such as a JSON object with specific fields.

Normally, an LLM generates free-form text. But software applications often require predictable data that can be processed programmatically.

**Example — Unstructured Response**

```text
The customer's name is Ali. He wants to buy a laptop for $850 and prefers Lenovo.
```

**Example — Structured Response**

```json
{
  "customer_name": "Ali",
  "product": "Laptop",
  "budget": 850,
  "preferred_brand": "Lenovo"
}
```

In the structured response, each piece of information has a clearly defined field.

## 2. Why Do We Need Structured Output?

Imagine building an AI-based customer support system.

A customer sends the following message:

```text
I ordered a laptop yesterday, but it arrived damaged. I want a replacement.
```

We want the AI to identify:

- The customer's issue
- The product
- The requested action
- The sentiment

Instead of returning a paragraph, the model could generate:

```json
{
  "issue": "Damaged product",
  "product": "Laptop",
  "requested_action": "Replacement",
  "sentiment": "Negative"
}
```

Now our Python application can use individual fields to automate the next steps.

### Common Benefits

- Easier integration with APIs and databases
- Predictable field names
- Simpler data extraction
- Support for type validation
- Easier automation
- More reliable downstream processing

**Important:** Structured output improves predictability but does not guarantee that the extracted facts are correct.

## 3. Structured vs Unstructured Output

| Unstructured Output                    | Structured Output                  |
| -------------------------------------- | ---------------------------------- |
| Free-form sentences or paragraphs      | Defined fields and data types      |
| Designed mainly for human reading      | Designed for software processing   |
| Harder to extract information reliably | Easier to access individual values |
| Flexible format                        | Predictable schema                 |
| Example: Written product review        | Example: JSON product details      |

## 4. What Is a Schema?

A **schema** defines the expected structure of data.

For example, a customer feedback schema might require:

| Field           | Data Type | Purpose                        |
| --------------- | --------- | ------------------------------ |
| `customer_name` | String    | Name of the customer           |
| `issue`         | String    | Description of the problem     |
| `sentiment`     | String    | Positive, negative, or neutral |
| `priority`      | Integer   | Priority level                 |

A schema can also define required fields, allowed values, and validation constraints.

### Example

```json
{
  "customer_name": "Ali",
  "issue": "Damaged laptop",
  "sentiment": "negative",
  "priority": 2
}
```

## 5. What Is JSON?

JSON stands for **JavaScript Object Notation**.

It is a text-based data format commonly used for exchanging information between applications.

Example:

```json
{
  "name": "Ateeb",
  "age": 24,
  "skills": ["Python", "SQL", "LangChain"],
  "is_student": true
}
```

### Common JSON Data Types

| Type    | Example             |
| ------- | ------------------- |
| String  | `"Python"`          |
| Number  | `25`                |
| Boolean | `true`              |
| Array   | `["Python", "SQL"]` |
| Object  | `{"name": "Ali"}`   |
| Null    | `null`              |

**Note:** JSON uses lowercase `true`, `false`, and `null`, whereas Python uses `True`, `False`, and `None`.

## 6. How Structured Output Works with an LLM

A typical workflow is:

```text
User Input
    |
    v
LLM + Schema Instructions
    |
    v
Structured Response
    |
    v
Parsing and Validation
    |
    v
Python Application
```

### Explanation

1. The application receives user input.
2. We define the fields the model should return.
3. The model generates data in the requested structure.
4. The application parses the response.
5. Validation checks whether the data satisfies the schema.
6. The application uses the validated information.

Depending on the model and provider, the schema may be supplied through prompting, tool calling, or a native structured-output API.

## 7. Types of Structured Output in LangChain

In this section, we will explore three schema approaches.

### A. TypedDict

Defines the expected keys and types of a Python dictionary.

```python
from typing import TypedDict

class Student(TypedDict):
    name: str
    age: int
```

TypedDict primarily supports static type checking. It does not automatically validate normal dictionaries at runtime.

### B. Pydantic

Provides Python models with runtime validation.

```python
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
```

Pydantic can validate incoming values and report errors when data does not satisfy the model requirements.

### C. JSON Schema

Defines structured data requirements using a language-independent JSON-compatible schema.

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "age"]
}
```

We will study these approaches individually in upcoming topics.

## 8. JSON Formatting vs Validation

These are two different concepts.

**JSON formatting:** The response is valid JSON that a parser can read.

**Schema validation:** The parsed JSON contains the required fields, types, and constraints.

Consider:

```json
{
  "name": "Ali",
  "age": "twenty"
}
```

This is valid JSON, but it does not satisfy a schema requiring `age` to be an integer.

Therefore, valid JSON does not automatically mean valid application data.

## 9. Simple Python Example Without an LLM

Before using a model, let's understand how structured data works in Python.

```python
customer = {
    "name": "Ali",
    "product": "Laptop",
    "budget": 850,
    "sentiment": "negative"
}

print("Customer:", customer["name"])
print("Product:", customer["product"])
print("Budget:", customer["budget"])
print("Sentiment:", customer["sentiment"])
```

Expected output:

```text
Customer: Ali
Product: Laptop
Budget: 850
Sentiment: negative
```

Because the information is structured, our application can access each value directly.

## 10. Example: Extracting Information with Groq

We can ask the model to return JSON.

```python
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

response = model.invoke(
    """
    Extract information from this message:

    "I bought a Lenovo laptop for $850."

    Return only a JSON object with:
    - brand
    - product
    - price
    """
)

print(response.content)

# Attempt to parse the response as JSON.
try:
    data = json.loads(response.content)
    print("Brand:", data["brand"])
    print("Product:", data["product"])
    print("Price:", data["price"])
except (json.JSONDecodeError, KeyError, TypeError) as error:
    print("Parsing or extraction failed:", error)
```

### Important Limitation

This example only asks for JSON using natural-language instructions.

The model may still return extra text, omit fields, or produce an unexpected type.

Later, we will use `with_structured_output()` with compatible models and schemas to make structured responses more dependable.

## 11. Real-World Applications

### Support Ticket Classification

Extract category, urgency, sentiment, and issue description.

### Resume Information Extraction

Extract skills, education, and experience.

### Product Data Processing

Extract product names, categories, and prices.

### Document Analysis

Extract important dates, organizations, and referenced amounts.

### AI Agents

Return structured tool arguments instead of free-form instructions.

## 12. Common Beginner Mistakes

**Mistake 1 — Assuming JSON always follows a schema**

Valid JSON may still contain missing fields or incorrect types.

**Mistake 2 — Assuming TypedDict validates data automatically**

TypedDict provides type information but does not validate ordinary dictionaries at runtime.

**Mistake 3 — Trusting every value generated by an LLM**

Even structurally valid responses can contain inaccurate information.

**Mistake 4 — Skipping error handling**

Applications should handle invalid JSON, missing keys, and validation failures.

**Mistake 5 — Confusing data extraction with factual verification**

Extracting a value from text does not prove that the value is true.

## 13. Quick Revision Questions

**Q1. What is structured output?**

Model output organized into predefined fields or structures.

**Q2. Why is structured output useful?**

It makes AI-generated information easier for software applications to process.

**Q3. What is JSON?**

A text-based format for representing structured data.

**Q4. What is a schema?**

A definition of the expected fields, types, and constraints of data.

**Q5. Does valid JSON guarantee schema compliance?**

No.

**Q6. What is TypedDict?**

A Python typing feature for describing dictionary structures.

**Q7. What is Pydantic?**

A Python library for defining models and validating data.

**Q8. What is JSON Schema?**

A standard way of describing JSON data structures and validation rules.

**Q9. What does `json.loads()` do?**

Parses a JSON string into Python data structures.

**Q10. Can structured output contain incorrect information?**

Yes. Structural validity does not guarantee factual accuracy.

## 14. Key Takeaways

- Structured output organizes responses into predictable fields.
- Schemas define expected data structures.
- JSON is commonly used for exchanging structured data.
- JSON formatting and schema validation are different.
- TypedDict provides type hints.
- Pydantic provides runtime validation.
- JSON Schema describes data requirements.
- Applications should validate AI-generated data before using it.

---

## Learning Resources

- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)
- [LangChain Documentation](https://docs.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Learning Journey:** Section 05 — Topic 01
