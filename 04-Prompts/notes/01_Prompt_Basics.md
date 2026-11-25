# 01 — Prompt Basics in LangChain

## 1. What Is a Prompt?

A **prompt** is the input we provide to a Large Language Model (LLM) to tell it what task to perform.

A prompt can contain:

- Instructions
- Questions
- Context or background information
- Examples
- Output formatting requirements

### Simple Example

**Prompt:**

```text
Explain Python in simple words.
```

**Possible response:**

```text
Python is a programming language used for web development, automation, data analysis, and artificial intelligence.
```

The quality and clarity of a prompt can influence the quality of the response.

---

## 2. Why Are Prompts Important?

A language model needs clear instructions to understand what we want.

Compare these two prompts.

### Unclear Prompt

```text
Tell me about Python.
```

The model might generate a very broad answer.

### Clear Prompt

```text
You are a Python teacher.

Explain Python to a beginner in 5 sentences.

Include:
1. What Python is
2. Where Python is used
3. One simple example
```

The second prompt provides more specific instructions about the task, audience, and expected output.

### Benefits of Good Prompts

- More relevant responses
- Better control over response formatting
- Reduced ambiguity
- More consistent application behavior
- Easier integration into software applications

**Important:** Even a well-written prompt cannot guarantee that a model will always produce correct information.

---

## 3. Types of Prompts

In this lesson, we focus on two types:

1. Static prompts
2. Dynamic prompts

### A. Static Prompt

A static prompt contains fixed instructions.

Example:

```python
prompt = "Explain what machine learning is."
```

Every time we send this prompt, the text remains the same.

#### Advantages

- Simple to write
- Easy to understand
- Useful for fixed tasks

#### Limitations

- Less flexible
- Requires manual modification when the topic changes

### B. Dynamic Prompt

A dynamic prompt contains variables or placeholders that can be replaced with different values.

Example:

```python
topic = "Machine Learning"

prompt = f"Explain {topic} in simple words."

print(prompt)
```

Output:

```text
Explain Machine Learning in simple words.
```

If we change the value of `topic`, the prompt changes automatically.

#### Advantages

- Reusable
- Flexible
- Useful for applications that accept user input
- Easier to maintain

---

## 4. Static vs Dynamic Prompts

| Feature     | Static Prompt      | Dynamic Prompt           |
| ----------- | ------------------ | ------------------------ |
| Text        | Fixed              | Changes using variables  |
| Reusability | Limited            | High                     |
| Flexibility | Low                | High                     |
| Example     | "Explain Python"   | "Explain {topic}"        |
| Common Use  | Fixed instructions | User-driven applications |

### Real-World Example

Imagine an educational chatbot.

A static prompt might always ask:

```text
Explain Python to a beginner.
```

A dynamic prompt might ask:

```text
Explain {topic} to a {level} student.
```

Possible values:

```text
topic = "Machine Learning"
level = "beginner"
```

The resulting instruction becomes:

```text
Explain Machine Learning to a beginner student.
```

---

## 5. What Is Prompt Engineering?

**Prompt engineering** is the process of designing and improving prompts to obtain more useful and reliable responses from language models.

It involves selecting suitable instructions, context, examples, and output requirements.

### Common Prompt Engineering Techniques

**Clear instructions**

Explain exactly what the model should do.

**Role prompting**

Specify a role or perspective for the model.

Example:

```text
You are an experienced Python instructor.
```

**Providing context**

Supply relevant background information.

Example:

```text
The user is a beginner who knows Python variables and loops.
```

**Few-shot prompting**

Provide example inputs and outputs to demonstrate the expected behavior.

**Output constraints**

Specify the desired format.

Example:

```text
Return exactly three bullet points.
```

### Example of a Structured Prompt

```text
Role:
You are a Python programming instructor.

Task:
Explain Python dictionaries.

Audience:
Beginner programming students.

Requirements:
- Use simple English.
- Include one code example.
- Explain when dictionaries are useful.
- Keep the explanation under 200 words.
```

---

## 6. What Are Prompt Variables?

Prompt variables are placeholders that allow developers to insert values into a prompt.

For example:

```text
Explain {topic} in {language}.
```

Here:

- `{topic}` is the first variable.
- `{language}` is the second variable.

Possible input values:

```python
{
    "topic": "Artificial Intelligence",
    "language": "English"
}
```

Result:

```text
Explain Artificial Intelligence in English.
```

LangChain provides `PromptTemplate` for managing this type of prompt.

---

## 7. Introduction to PromptTemplate

Instead of manually using Python f-strings, we can use LangChain's `PromptTemplate`.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple words."
)

result = prompt.invoke({
    "topic": "Machine Learning"
})

print(result.to_string())
```

### Code Explanation

**`PromptTemplate.from_template()`**

Creates a reusable prompt template.

**`{topic}`**

Represents a variable that will be replaced with actual input.

**`prompt.invoke()`**

Supplies the value for the variable and creates a formatted prompt value.

**`result.to_string()`**

Converts the prompt value into a readable string.

### Expected Output

```text
Explain Machine Learning in simple words.
```

**Important:** `PromptTemplate` only prepares the prompt. It does not generate an AI answer by itself.

To generate an answer, we must send the formatted prompt to a language model.

---

## 8. Using a Dynamic Prompt with Groq

We can combine a prompt template with our Groq chat model.

```python
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = PromptTemplate.from_template(
    "Explain {topic} to a {level} student in 3 sentences."
)

formatted_prompt = prompt.invoke({
    "topic": "Neural Networks",
    "level": "beginner"
})

response = model.invoke(formatted_prompt)

print(response.content)
```

### Step-by-Step Explanation

1. `load_dotenv()` loads the Groq API key.
2. `ChatGroq()` initializes the language model.
3. `PromptTemplate` defines the reusable instruction.
4. `prompt.invoke()` inserts the supplied variables.
5. `model.invoke()` sends the formatted prompt to Groq.
6. `response.content` displays the AI-generated answer.

---

## 9. Real-World Applications of Dynamic Prompts

### Educational Assistant

```text
Explain {topic} to a {level} student.
```

### Translation Application

```text
Translate the following text into {language}:

{text}
```

### Email Generator

```text
Write a {tone} email about {subject}.
```

### Code Explanation Tool

```text
Explain the following {language} code:

{code}
```

### Document Summarizer

```text
Summarize the following document in {number_of_points} points:

{document}
```

Dynamic prompts help developers build reusable application features.

---

## 10. Common Beginner Mistakes

### Mistake 1 — Confusing PromptTemplate with an LLM

`PromptTemplate` does not generate answers.

It only prepares input for a model.

### Mistake 2 — Forgetting Input Variables

If a template contains `{topic}`, the developer must provide a suitable value for `topic`.

### Mistake 3 — Writing Ambiguous Instructions

A vague prompt may produce an overly broad or irrelevant answer.

### Mistake 4 — Assuming Prompts Guarantee Accuracy

Prompts can guide the model, but generated information may still need verification.

### Mistake 5 — Putting Sensitive Information into Prompts

Do not include API keys, passwords, or confidential data in prompts sent to external services.

---

## 11. Quick Revision Questions

**Q1. What is a prompt?**

Input provided to a language model to guide its behavior or response.

**Q2. What is a static prompt?**

A prompt with fixed text that does not change automatically.

**Q3. What is a dynamic prompt?**

A prompt containing variables that can be replaced with different values.

**Q4. What is prompt engineering?**

Designing and improving prompts to obtain useful responses from language models.

**Q5. What is a placeholder?**

A variable in a template, such as `{topic}`, that is replaced with an input value.

**Q6. What does `PromptTemplate` do?**

Creates and formats reusable prompts.

**Q7. Does `PromptTemplate.invoke()` call the language model?**

No. It formats a prompt using the supplied variables.

**Q8. Why are dynamic prompts useful?**

They allow applications to reuse instructions with different inputs.

---

## 12. Key Takeaways

- Prompts provide instructions and context to LLMs.
- Static prompts contain fixed text.
- Dynamic prompts use variables and placeholders.
- Prompt engineering improves the clarity and usefulness of instructions.
- LangChain's `PromptTemplate` creates reusable prompts.
- `PromptTemplate.invoke()` formats a prompt but does not generate an AI answer.
- A formatted prompt can be passed to Groq or another supported language model.

---

## Learning Resources

- [CampusX LangChain Prompts Repository](https://github.com/campusx-official/langchain-prompts)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)
- [LangChain Documentation](https://docs.langchain.com/)

**Learning Journey:** Section 04 — Topic 01
