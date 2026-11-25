# 02 — PromptTemplate in LangChain

## 1. What Is PromptTemplate?

`PromptTemplate` is a LangChain class that helps developers create reusable text-based prompts.

Instead of manually rewriting instructions, we define a template containing variables and supply their values whenever needed.

### Example

Template:

```text
Explain {topic} to a {level} student.
```

Input values:

```python
{
    "topic": "Machine Learning",
    "level": "beginner"
}
```

Formatted prompt:

```text
Explain Machine Learning to a beginner student.
```

**Important:** `PromptTemplate` prepares prompts. It does not generate AI responses by itself.

---

## 2. Why Do We Need PromptTemplate?

Consider an educational application that explains different programming concepts.

Without a template:

```python
prompt1 = "Explain Python to a beginner."
prompt2 = "Explain Java to a beginner."
prompt3 = "Explain Machine Learning to a beginner."
```

With `PromptTemplate`:

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} to a beginner."
)
```

We can reuse the same template with any topic.

### Benefits

- Reduces repetitive code.
- Makes prompts reusable.
- Supports dynamic variables.
- Separates prompt instructions from application data.
- Integrates with LangChain models and workflows.

---

## 3. Creating a PromptTemplate

There are two common ways to create a prompt template.

### Method 1 — Using from_template()

This is the simpler approach.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple words."
)

result = prompt.invoke({
    "topic": "Python"
})

print(result.to_string())
```

Expected output:

```text
Explain Python in simple words.
```

### Explanation

- `from_template()` creates a prompt template.
- `{topic}` is a placeholder.
- `invoke()` supplies its value.
- `to_string()` converts the resulting prompt value to text.

LangChain can identify variables automatically from the template.

### Method 2 — Using the PromptTemplate Constructor

We can also define the template and its input variables explicitly.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Explain {topic} to a {level} student.",
    input_variables=["topic", "level"]
)

result = prompt.invoke({
    "topic": "Python",
    "level": "beginner"
})

print(result.to_string())
```

Expected output:

```text
Explain Python to a beginner student.
```

For most beginner examples, `from_template()` is easier.

---

## 4. Using Multiple Input Variables

A template can contain several placeholders.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in {language} for a {level} student."
)

result = prompt.invoke({
    "topic": "Artificial Intelligence",
    "language": "English",
    "level": "beginner"
})

print(result.to_string())
```

Expected output:

```text
Explain Artificial Intelligence in English for a beginner student.
```

### Important Point

The keys in the input dictionary must match the required template variables.

For example, if the template contains `{topic}`, we must provide a value for `topic`.

---

## 5. Understanding invoke() vs format()

Both methods can insert values into a prompt, but they return different types.

### Using invoke()

```python
prompt = PromptTemplate.from_template(
    "Explain {topic}."
)

result = prompt.invoke({
    "topic": "Python"
})

print(result)
print(type(result))
```

`invoke()` returns a LangChain prompt-value object, typically a `StringPromptValue`.

We can convert it into text:

```python
print(result.to_string())
```

### Using format()

```python
result = prompt.format(
    topic="Python"
)

print(result)
print(type(result))
```

`format()` returns a Python string.

### Comparison

| Method        | Input                   | Return Type           |
| ------------- | ----------------------- | --------------------- |
| `invoke()`    | Usually a dictionary    | PromptValue object    |
| `format()`    | Keyword arguments       | String                |
| `to_string()` | Called on a PromptValue | String representation |

**Remember:** `prompt.invoke()` formats the prompt; `model.invoke()` sends input to the model.

They perform different jobs.

---

## 6. Required and Optional Variables

### Required Variables

By default, variables in a template must be supplied.

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} to a {level} student."
)
```

This template requires both `topic` and `level`.

If a required variable is missing, LangChain raises an error.

### Partial Variables

We can pre-fill some variables using `partial()`.

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} to a {level} student."
)

beginner_prompt = prompt.partial(
    level="beginner"
)

result = beginner_prompt.format(
    topic="Neural Networks"
)

print(result)
```

Expected output:

```text
Explain Neural Networks to a beginner student.
```

Here, `level` is already provided, so we only need to supply `topic`.

This is useful when one part of a prompt remains constant across multiple requests.

---

## 7. Inspecting Template Variables

We can check which input variables a template requires.

```python
prompt = PromptTemplate.from_template(
    "Translate {text} into {language}."
)

print(prompt.input_variables)
```

Expected output:

```text
['language', 'text']
```

This helps developers understand what information must be supplied before formatting a prompt.

---

## 8. Connecting PromptTemplate to Groq

Let's use your Groq GPT-OSS 120B model.

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
    "You are an experienced Python teacher. "
    "Explain {topic} to a {level} student in 3 sentences."
)

formatted_prompt = prompt.invoke({
    "topic": "Python decorators",
    "level": "beginner"
})

response = model.invoke(formatted_prompt)

print(response.content)
```

### How This Works

**Step 1:** `load_dotenv()` loads the Groq API key.

**Step 2:** `ChatGroq()` initializes the chat model.

**Step 3:** `PromptTemplate.from_template()` creates a reusable prompt.

**Step 4:** `prompt.invoke()` inserts values into the placeholders.

**Step 5:** `model.invoke()` sends the formatted prompt to Groq.

**Step 6:** `response.content` displays the generated response.

---

## 9. Connecting PromptTemplate Using LCEL

LangChain Expression Language (LCEL) allows us to connect components using the pipe operator (`|`).

For example:

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

response = chain.invoke({
    "topic": "Python decorators",
    "level": "beginner"
})

print(response)
```

### Execution Flow

```text
Input Dictionary
       |
       v
PromptTemplate
       |
       v
    ChatGroq
       |
       v
StrOutputParser
       |
       v
 Final Text
```

### Explanation

- `prompt` formats the input.
- `model` generates the response.
- `StrOutputParser()` converts the model response into plain text.
- `chain.invoke()` executes the entire workflow.

This is a simple chain. We'll study chains and LCEL in their dedicated sections.

---

## 10. Saving a Template in a Separate Variable

Separating instructions from Python logic makes code easier to maintain.

```python
template = """
You are a helpful educational assistant.

Topic: {topic}
Student Level: {level}

Explain the topic using:
1. A simple definition
2. A real-world example
3. One important takeaway
"""

prompt = PromptTemplate.from_template(template)

result = prompt.format(
    topic="Machine Learning",
    level="beginner"
)

print(result)
```

Triple-quoted strings are particularly useful for longer prompts.

---

## 11. Handling Missing Variables

If we forget to provide a required variable, formatting will fail.

For example:

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} in {language}."
)

try:
    result = prompt.invoke({
        "topic": "Python"
    })

    print(result.to_string())

except KeyError as error:
    print("Missing prompt variable:", error)
```

The template requires both `topic` and `language`, but only `topic` was supplied.

### Best Practice

Check user inputs before calling the prompt.

```python
topic = input("Enter topic: ").strip()
language = input("Enter language: ").strip()

if not topic or not language:
    print("Topic and language are required.")
else:
    result = prompt.format(
        topic=topic,
        language=language
    )

    print(result)
```

---

## 12. Real-World Applications

### Educational Chatbot

```text
Explain {topic} to a {level} student.
```

### Resume Summary Generator

```text
Write a professional summary for a {job_title}
with {years} years of experience.
```

### Customer Support Assistant

```text
Write a {tone} reply to this customer message:

{message}
```

### Code Explainer

```text
Explain this {language} code to a beginner:

{code}
```

### Document Summarizer

```text
Summarize the following text in {number_of_points} points:

{text}
```

---

## 13. Common Beginner Mistakes

**Mistake 1 — Forgetting required variables**

Every required placeholder must receive a value.

**Mistake 2 — Confusing invoke methods**

`prompt.invoke()` formats input, while `model.invoke()` generates a response.

**Mistake 3 — Assuming PromptTemplate calls an LLM**

Prompt templates do not call models automatically.

**Mistake 4 — Using unescaped curly braces**

By default, LangChain templates use curly braces for variables.

If we want literal braces, we should escape them using double braces.

Example:

```python
prompt = PromptTemplate.from_template(
    'Return JSON like {{"name": "{name}"}}'
)

print(prompt.format(name="Ali"))
```

Expected output:

```json
{ "name": "Ali" }
```

**Mistake 5 — Treating external input as trusted instructions**

If a template includes content from users or documents, that content may contain malicious instructions. Applications should treat such content as untrusted and enforce important rules outside the prompt.

---

## 14. Quick Revision Questions

**Q1. What is PromptTemplate?**

A LangChain class for creating reusable text prompts.

**Q2. What does from_template() do?**

Creates a prompt template and identifies its variables.

**Q3. What does prompt.invoke() return?**

A formatted PromptValue object.

**Q4. What does format() return?**

A formatted Python string.

**Q5. What is partial()?**

A method for pre-filling some template variables.

**Q6. Can PromptTemplate use multiple variables?**

Yes.

**Q7. What happens when a required variable is missing?**

LangChain raises an error.

**Q8. Does PromptTemplate automatically call an AI model?**

No.

**Q9. What does the pipe operator (`|`) do in LangChain?**

It connects compatible components into a processing workflow.

**Q10. Why should prompts be reusable?**

Reusability reduces repetition and makes applications easier to maintain.

---

## 15. Key Takeaways

- `PromptTemplate` creates reusable text-based prompts.
- `from_template()` is a convenient constructor.
- Templates support multiple input variables.
- `invoke()` returns a formatted prompt-value object.
- `format()` returns a string.
- `partial()` pre-fills selected variables.
- Required input variables must be supplied.
- Templates can be connected to Groq using `model.invoke()` or LCEL.
- Prompt formatting and model inference are separate operations.

---

## Learning Resources

- [CampusX LangChain Prompts Repository](https://github.com/campusx-official/langchain-prompts)
- [LangChain Prompt Documentation](https://docs.langchain.com/oss/python/langchain/models)
- [CampusX LangChain Playlist](https://www.youtube.com/playlist?list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0)

**Learning Journey:** Section 04 — Topic 02
