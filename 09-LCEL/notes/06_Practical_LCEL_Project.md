# 06 — Practical LCEL Project: AI Programming Study Assistant

## 1. Project Overview

In this project, I will build an interactive AI Programming Study Assistant using Python, LangChain Expression Language (LCEL), and Groq GPT-OSS 120B.

The purpose of this project is to combine the concepts learned in Sections 07, 08, and 09 into one reusable application.

Instead of testing individual components separately, the application will connect multiple Runnables into a complete AI workflow.

## 2. Project Features

The application will:

1. Accept a programming topic from the user.
2. Ask for the student's learning level.
3. Validate and normalize the input.
4. Select an explanation prompt according to the level.
5. Generate a topic explanation.
6. Generate three interview questions.
7. Preserve the original normalized input.
8. Calculate the explanation length.
9. Display the result in the terminal.
10. Allow repeated questions until the user exits.

## 3. Technologies

| Technology     | Purpose                             |
| -------------- | ----------------------------------- |
| Python         | Application development             |
| LangChain Core | Runnable composition                |
| LangChain Groq | Connect to Groq-hosted models       |
| GPT-OSS 120B   | Generate explanations and questions |
| python-dotenv  | Load the API key                    |
| VS Code        | Code development                    |
| GitHub         | Version control                     |

## 4. Project Architecture

```text
User Input
   |
   v
Input Validation and Normalization
   |
   v
RunnablePassthrough.assign()
   |
   +----------------+----------------+
   |                |                |
   v                v                v
Display Label   RunnableBranch   Questions Chain
                    |                |
              Beginner/Advanced     Groq
                    |
                  Groq
                    |
              Text Parser
   |                |                |
   +----------------+----------------+
                    |
                    v
              Result Dictionary
                    |
                    v
          Additional Transformations
                    |
                    v
             Terminal Display
```

## 5. Project Structure

```text
09-LCEL/
├── README.md
├── notes/
│   ├── 01_LCEL_Basics.md
│   ├── 02_Pipe_Operator.md
│   ├── 03_Dictionary_Composition.md
│   ├── 04_Data_Transformation.md
│   ├── 05_Advanced_LCEL.md
│   ├── 06_Practical_LCEL_Project.md
│   └── 07_Quick_Revision.md
└── examples/
    ├── 01_lcel_basics.py
    ├── 02_pipe_operator.py
    ├── 03_dictionary_composition.py
    ├── 04_data_transformation.py
    ├── 05_advanced_lcel.py
    └── 06_ai_study_assistant.py
```

## 6. Understanding Each Component

### RunnableLambda

Validates and normalizes user input.

For example:

```python
{
    "topic": "  python decorators  ",
    "level": "BEGINNER"
}
```

becomes:

```python
{
    "topic": "python decorators",
    "level": "beginner"
}
```

### RunnableBranch

Selects the explanation prompt according to the level.

- Beginner → Simple explanation
- Intermediate → Balanced explanation
- Advanced → Technical explanation

Only one explanation branch runs per request.

### RunnableParallel

Runs independent operations.

In this project, the explanation and interview-question generation are independent.

### RunnablePassthrough.assign()

Preserves the normalized input while adding fields such as:

- `display_label`
- `explanation`
- `questions`
- `explanation_length`

### StrOutputParser

Processes the model response into text that can be used by Python.

## 7. Input Validation

Validation happens before contacting Groq.

Rules:

- The topic must be a nonempty string.
- The topic cannot contain only whitespace.
- The level must be beginner, intermediate, or advanced.
- Capitalization and unnecessary spaces are normalized.

Invalid input raises a clear error.

This helps avoid unnecessary API requests.

## 8. Data Flow

Example input:

```python
{
    "topic": "  Python Decorators  ",
    "level": "BEGINNER"
}
```

Normalized input:

```python
{
    "topic": "Python Decorators",
    "level": "beginner"
}
```

Final output structure:

```python
{
    "topic": "Python Decorators",
    "level": "beginner",
    "display_label": "Python Decorators (beginner)",
    "explanation": "...",
    "questions": "...",
    "explanation_length": 200
}
```

The length above is illustrative; the actual value depends on the generated explanation.

## 9. Model Requests

Each successful study request normally generates two Groq model calls:

1. One explanation.
2. One set of interview questions.

The explanation branch selects only one prompt.

The model responses are generated independently and then combined.

## 10. Error Handling

The application handles:

- Invalid user input.
- Empty topics.
- Unsupported learning levels.
- Model or network exceptions.
- Keyboard interruption during interactive use.

Errors should be displayed clearly without exposing API credentials.

## 11. Practical Test Cases

| Test                           | Expected behavior          |
| ------------------------------ | -------------------------- |
| Python decorators, beginner    | Beginner explanation       |
| Machine learning, intermediate | Balanced explanation       |
| Neural networks, advanced      | Technical explanation      |
| Empty topic                    | Reject before calling Groq |
| Invalid level                  | Reject before calling Groq |
| Exit command                   | Stop application           |

## 12. Concepts Demonstrated

- LCEL pipe composition
- RunnableLambda
- RunnableSequence
- RunnableBranch
- RunnableParallel through assign()
- RunnablePassthrough.assign()
- PromptTemplate
- ChatGroq
- StrOutputParser
- Input validation
- Error handling
- Interactive terminal applications

## 13. Future Improvements

The application could later include:

- Save study notes to PostgreSQL.
- Generate multiple-choice quizzes.
- Export explanations to Markdown.
- Track study history.
- Add a FastAPI backend.
- Add a web interface.
- Retrieve information from uploaded documents.
- Implement RAG with a vector store.
- Add automated tests using pytest.

These improvements are outside the current project's scope.

## 14. Important Learning Outcomes

After completing this project, I should understand how to:

1. Build reusable multi-stage LCEL workflows.
2. Use Python functions to validate inputs.
3. Route inputs through conditional branches.
4. Execute independent model tasks.
5. Preserve and enrich structured data.
6. Build an interactive Python application.
7. Handle expected input and model failures.

## 15. Interview Questions

**Q1. Why did we use RunnableLambda?**

To integrate input validation and normalization into the LangChain workflow.

**Q2. Why did we use RunnableBranch?**

To select different explanations according to the learning level.

**Q3. Why did we use RunnablePassthrough.assign()?**

To preserve normalized inputs and add generated results.

**Q4. Are both LLM tasks executed sequentially?**

No. The explanation and question-generation branches can execute concurrently.

**Q5. How many Groq requests does one successful study request normally make?**

Two.

**Q6. Is this application an AI agent?**

No. It is a predefined LCEL workflow.

**Q7. Can the application later be integrated with FastAPI?**

Yes. The LCEL workflow can be reused in a FastAPI backend.

## 16. Key Takeaways

This project demonstrates how multiple LangChain components can work together to create a practical AI application.

The application uses validation, conditional routing, parallel processing, structured dictionary outputs, and terminal interaction.

It provides a foundation for larger applications involving FastAPI, RAG, databases, and AI agents.

---

## Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [RunnablePassthrough Reference](https://reference.langchain.com/python/langchain-core/runnables/passthrough/RunnablePassthrough)
- [RunnableBranch Reference](https://reference.langchain.com/python/langchain-core/runnables/branch/RunnableBranch)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 09 — Topic 06

**Project:** AI Programming Study Assistant
