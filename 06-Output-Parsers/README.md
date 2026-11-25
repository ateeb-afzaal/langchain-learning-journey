# 06 — Output Parsers in LangChain

## Overview

Output parsers are LangChain components that transform language model responses into formats that are easier for Python applications to use.

For example, a chat model typically returns an `AIMessage` object. An output parser can extract the message text, convert a JSON response into a Python dictionary, or validate generated data against a schema.

In this section, I will learn how to use different LangChain output parsers with Python and Groq GPT-OSS 120B.

## Topics Covered

### 1. Output Parser Basics

- What is an output parser?
- Why do we need output parsers?
- Parsing vs validation
- Understanding model responses
- Using parsers in LangChain workflows

### 2. StrOutputParser

- Converting an AI response into plain text
- Understanding `StrOutputParser`
- Connecting prompts, models, and parsers
- Using LCEL with the pipe operator (`|`)

### 3. JsonOutputParser

- Understanding JSON output parsing
- Converting JSON responses into Python dictionaries
- Using format instructions
- Handling invalid JSON
- Parsing JSON in LangChain chains

### 4. StructuredOutputParser

- Defining response fields
- Using `ResponseSchema`
- Generating format instructions
- Extracting structured responses
- Understanding differences from provider-native structured output

### 5. PydanticOutputParser

- Using Pydantic models as output schemas
- Parsing LLM output into validated objects
- Handling validation errors
- Using `PydanticOutputParser` in a chain

### 6. Quick Revision

- Important definitions
- Comparison tables
- Interview questions
- Practical test results

## Learning Objectives

By the end of this section, I should be able to:

1. Explain the purpose of output parsers.
2. Extract plain text from AI responses using `StrOutputParser`.
3. Convert JSON responses into Python data using `JsonOutputParser`.
4. Understand how `StructuredOutputParser` and `ResponseSchema` work.
5. Validate generated output using `PydanticOutputParser`.
6. Connect prompts, models, and parsers using LCEL.
7. Understand the difference between parsing model-generated text and provider-native structured output.

## Repository Structure

```text
06-Output-Parsers/
├── README.md
├── notes/
│   ├── 01_Output_Parser_Basics.md
│   ├── 02_StrOutputParser.md
│   ├── 03_JsonOutputParser.md
│   ├── 04_StructuredOutputParser.md
│   ├── 05_PydanticOutputParser.md
│   └── 06_Quick_Revision.md
└── examples/
    └── Python examples will be added here
```

## Output Parser Comparison

| Parser                   | Purpose                             | Typical Output          |
| ------------------------ | ----------------------------------- | ----------------------- |
| `StrOutputParser`        | Extract response text               | Python string           |
| `JsonOutputParser`       | Parse JSON-formatted text           | Dictionary or list      |
| `StructuredOutputParser` | Parse fields using response schemas | Dictionary              |
| `PydanticOutputParser`   | Parse and validate using Pydantic   | Pydantic model instance |

**Important:** The output parser cannot guarantee that the language model follows its formatting instructions. Parsing and validation errors can still occur.

## Example Workflow

```text
User Input
    |
    v
Prompt Template
    |
    v
Groq Chat Model
    |
    v
Output Parser
    |
    v
Python Application
```

Using LangChain Expression Language (LCEL):

```python
chain = prompt | model | parser
```

Each component passes its output to the next component.

## Technologies

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Python         | Application development         |
| LangChain      | Prompt and parser integration   |
| LangChain Core | Output parser classes           |
| Groq           | Hosted language model inference |
| GPT-OSS 120B   | Language model                  |
| Pydantic       | Runtime validation              |
| VS Code        | Development environment         |

## Progress Checklist

- [ ] Output Parser Basics
- [ ] StrOutputParser
- [ ] JsonOutputParser
- [ ] StructuredOutputParser
- [ ] PydanticOutputParser
- [ ] Quick Revision
- [ ] Practical Python Examples
- [ ] Test all examples

## Learning Resources

- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [CampusX Output Parsers Repository](https://github.com/campusx-official/langchain-output-parsers)
- [LangChain Documentation](https://docs.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Key Goal

Understand how to convert language model responses into predictable Python data formats using output parsers.

Learn how to combine prompts, Groq models, and parsers to create reliable AI application workflows.

---

**Learning Journey:** Section 06 of 18

**Course Reference:** CampusX — LangChain Output Parsers.
