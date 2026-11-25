# 05 — Structured Output in LangChain

## Overview

Structured output allows developers to receive AI-generated responses in a predictable format instead of ordinary paragraphs.

For example, instead of asking an AI model to describe a product in free-form text, we can request specific fields such as the product name, category, price, and availability.

LangChain supports different approaches for defining structured responses, including Python `TypedDict`, Pydantic models, and JSON Schema.

In this section, I will learn how to define schemas, validate data, and generate structured responses using LangChain and Groq GPT-OSS 120B.

## Topics Covered

### 1. Structured Output Basics

- What is structured output?
- Structured vs unstructured responses
- Why applications need predictable data formats
- Common use cases and limitations

### 2. TypedDict

- Defining dictionary structures using type hints
- Required and optional fields
- `Annotated` and `Literal`
- Using TypedDict schemas with LangChain

### 3. Pydantic

- Creating models using `BaseModel`
- Type validation
- `Field` descriptions and constraints
- Handling validation errors
- Pydantic vs TypedDict

### 4. JSON Schema

- Understanding JSON objects and properties
- Defining required fields
- JSON Schema data types
- Writing JSON Schema for structured responses

### 5. with_structured_output()

- Connecting schemas to LangChain chat models
- Generating structured model responses
- Using TypedDict and Pydantic schemas
- Handling invalid model outputs
- Understanding provider and model compatibility

### 6. Quick Revision

- Important definitions
- Comparison tables
- Interview questions
- Practical exercises

## Learning Objectives

By the end of this section, I should be able to:

1. Explain why structured output is important in AI applications.
2. Define structured data using TypedDict.
3. Create and validate schemas using Pydantic.
4. Understand the purpose of JSON Schema.
5. Use `with_structured_output()` with compatible chat models.
6. Understand the difference between schema guidance and runtime validation.
7. Handle missing or invalid fields safely.

## Repository Structure

```text
05-Structured-Output/
├── README.md
├── notes/
│   ├── 01_Structured_Output_Basics.md
│   ├── 02_TypedDict.md
│   ├── 03_Pydantic.md
│   ├── 04_JSON_Schema.md
│   ├── 05_with_structured_output.md
│   └── 06_Quick_Revision.md
└── examples/
    └── Python examples will be added here
```

## Technologies

| Technology   | Purpose                                 |
| ------------ | --------------------------------------- |
| Python       | Application development                 |
| LangChain    | Model and structured-output integration |
| Groq         | Hosted inference                        |
| GPT-OSS 120B | Language model                          |
| TypedDict    | Dictionary structure definitions        |
| Pydantic     | Data validation and schema definitions  |
| JSON Schema  | Language-independent data schemas       |
| VS Code      | Development environment                 |

## Example: Structured vs Unstructured Output

### Unstructured Response

```text
The product is a laptop called ThinkBook.
It belongs to the electronics category and costs $850.
```

### Structured Response

```json
{
  "name": "ThinkBook",
  "category": "Electronics",
  "price": 850,
  "currency": "USD"
}
```

Structured output is easier for software to process because each value has a defined field.

## Progress Checklist

- [ ] Structured Output Basics
- [ ] TypedDict
- [ ] Pydantic
- [ ] JSON Schema
- [ ] with_structured_output()
- [ ] Quick Revision
- [ ] Practical Python Examples
- [ ] Test all examples

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [CampusX Structured Output Repository](https://github.com/campusx-official/langchain-structured-output)
- [LangChain Documentation](https://docs.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Key Goal

Learn how to make LLM responses easier to use in real applications by defining predictable data structures and validating important fields.

**Important:** A schema does not automatically guarantee that every model response will be correct. Model support, output parsing, and validation still matter.

---

**Learning Journey:** Section 05 of 18

**Course Reference:** CampusX — LangChain Structured Output.
